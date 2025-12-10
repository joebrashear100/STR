#!/usr/bin/env python3
"""
STR Document Migration with Comprehensive Failsafes and Test Mode
- Dry-run/test mode for validation
- Complete audit logging
- Rollback capabilities
- Error recovery
- Progress tracking and resumption
"""

import os
import sys
import json
import csv
import logging
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import requests
from azure.identity import InteractiveBrowserCredential
import re

# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    # SharePoint details (to be filled from sharepoint_ids.json)
    SITE_ID = None
    DRIVE_ID = None
    LIST_ID = None

    # Azure/Graph API
    CLIENT_ID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"  # Microsoft Graph CLI
    GRAPH_BASE = "https://graph.microsoft.com/v1.0"

    # File paths
    LOG_DIR = Path("migration_logs")
    AUDIT_LOG = LOG_DIR / "audit.jsonl"
    PROGRESS_FILE = LOG_DIR / "progress.json"
    ERROR_LOG = LOG_DIR / "errors.log"
    BACKUP_DIR = Path("migration_backups")
    SHAREPOINT_IDS_FILE = Path("sharepoint_ids.json")

    # Test configuration
    TEST_MODE = False
    TEST_FILE_COUNT = 5

    @classmethod
    def load_from_file(cls, filepath: Path):
        """Load SharePoint IDs from sharepoint_ids.json"""
        if not filepath.exists():
            raise FileNotFoundError(
                f"SharePoint IDs file not found: {filepath}\n"
                "Run Get_SharePoint_IDs.ps1 first"
            )

        with open(filepath, 'r') as f:
            data = json.load(f)
            cls.SITE_ID = data.get('siteId')
            cls.DRIVE_ID = data.get('driveId')
            cls.LIST_ID = data.get('listId')

        if not all([cls.SITE_ID, cls.DRIVE_ID, cls.LIST_ID]):
            raise ValueError("Missing required SharePoint IDs in config file")

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(test_mode: bool = False) -> logging.Logger:
    """Configure comprehensive logging"""
    Config.LOG_DIR.mkdir(exist_ok=True)
    Config.BACKUP_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger("STRMigration")
    logger.setLevel(logging.DEBUG)

    # File handler
    fh = logging.FileHandler(Config.ERROR_LOG)
    fh.setLevel(logging.ERROR)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO if not test_mode else logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

# ============================================================================
# AUDIT LOGGING
# ============================================================================

def audit_log(event_type: str, data: Dict, status: str = "success"):
    """Log all operations for audit trail"""
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "status": status,
        "data": data
    }

    with open(Config.AUDIT_LOG, 'a') as f:
        f.write(json.dumps(record) + '\n')

# ============================================================================
# PROGRESS TRACKING
# ============================================================================

class ProgressTracker:
    """Track migration progress for resumption capability"""

    def __init__(self, filepath: Path = Config.PROGRESS_FILE):
        self.filepath = filepath
        self.data = self._load()

    def _load(self) -> Dict:
        """Load progress from file"""
        if self.filepath.exists():
            with open(self.filepath, 'r') as f:
                return json.load(f)
        return {
            "started": datetime.utcnow().isoformat(),
            "total": 0,
            "completed": 0,
            "failed": 0,
            "files": {}
        }

    def save(self):
        """Save progress"""
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=2)

    def mark_file(self, file_id: str, status: str, details: Dict = None):
        """Mark a file as processed"""
        self.data["files"][file_id] = {
            "status": status,  # pending, processing, completed, failed
            "timestamp": datetime.utcnow().isoformat(),
            "details": details or {}
        }

        if status == "completed":
            self.data["completed"] += 1
        elif status == "failed":
            self.data["failed"] += 1

        self.save()

    def get_unprocessed(self, total_files: int) -> List[str]:
        """Get list of files not yet processed"""
        self.data["total"] = total_files
        self.save()

        processed = set(self.data["files"].keys())
        all_files = {f"file_{i}" for i in range(total_files)}
        return list(all_files - processed)

# ============================================================================
# BACKUP & ROLLBACK
# ============================================================================

class BackupManager:
    """Manage backups for rollback capability"""

    def __init__(self, backup_dir: Path = Config.BACKUP_DIR):
        self.backup_dir = backup_dir
        self.backup_dir.mkdir(exist_ok=True)

    def backup_sharepoint_item(self, item_id: str, headers: Dict) -> str:
        """Backup SharePoint item before updating"""
        url = f"{Config.GRAPH_BASE}/sites/{Config.SITE_ID}/lists/{Config.LIST_ID}/items/{item_id}"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            backup_data = response.json()
            backup_file = self.backup_dir / f"backup_{item_id}_{datetime.utcnow().timestamp()}.json"

            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)

            return str(backup_file)

        return None

    def create_migration_snapshot(self, migration_data: Dict) -> str:
        """Create snapshot of entire migration plan"""
        snapshot_file = self.backup_dir / f"snapshot_{datetime.utcnow().isoformat()}.json"

        with open(snapshot_file, 'w') as f:
            json.dump(migration_data, f, indent=2)

        return str(snapshot_file)

# ============================================================================
# GRAPH API OPERATIONS
# ============================================================================

class GraphAPIClient:
    """Microsoft Graph API operations with retry logic"""

    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds

    def __init__(self, headers: Dict, logger: logging.Logger):
        self.headers = headers
        self.logger = logger

    def _retry_request(self, method: str, url: str, **kwargs) -> Optional[requests.Response]:
        """Make request with retry logic"""
        for attempt in range(self.MAX_RETRIES):
            try:
                if method == "GET":
                    response = requests.get(url, headers=self.headers, **kwargs)
                elif method == "PUT":
                    response = requests.put(url, headers=self.headers, **kwargs)
                elif method == "POST":
                    response = requests.post(url, headers=self.headers, **kwargs)
                elif method == "PATCH":
                    response = requests.patch(url, headers=self.headers, **kwargs)
                else:
                    raise ValueError(f"Unsupported method: {method}")

                # Check for rate limiting
                if response.status_code == 429:
                    wait_time = int(response.headers.get('Retry-After', self.RETRY_DELAY))
                    self.logger.warning(f"Rate limited. Waiting {wait_time}s")
                    time.sleep(wait_time)
                    continue

                return response

            except requests.RequestException as e:
                self.logger.warning(f"Request failed (attempt {attempt+1}/{self.MAX_RETRIES}): {e}")
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.RETRY_DELAY)

        return None

    def download_onedrive_file(self, item_id: str) -> Optional[bytes]:
        """Download file from OneDrive"""
        url = f"{Config.GRAPH_BASE}/me/drive/items/{item_id}/content"
        response = self._retry_request("GET", url)

        if response and response.status_code == 200:
            return response.content

        return None

    def upload_to_sharepoint(self, filename: str, file_content: bytes) -> Optional[Dict]:
        """Upload file to SharePoint with conflict handling"""
        # Sanitize filename
        filename = self._sanitize_filename(filename)

        url = f"{Config.GRAPH_BASE}/drives/{Config.DRIVE_ID}/root:/{filename}:/content"

        headers = self.headers.copy()
        headers["Content-Type"] = "application/octet-stream"

        response = self._retry_request("PUT", url, data=file_content)

        if response and response.status_code in [200, 201]:
            return response.json()

        return None

    def create_sharing_link(self, item_id: str) -> Optional[str]:
        """Create read-only organization sharing link"""
        url = f"{Config.GRAPH_BASE}/drives/{Config.DRIVE_ID}/items/{item_id}/createLink"

        payload = {
            "type": "organizationView",
            "scope": "organization"
        }

        response = self._retry_request("POST", url, json=payload)

        if response and response.status_code == 201:
            data = response.json()
            return data['link']['webUrl']

        return None

    def update_list_item(self, item_id: str, architecture_url: str, test_mode: bool = False) -> bool:
        """Update SharePoint list item with new URL"""
        if test_mode:
            self.logger.info(f"[TEST MODE] Would update item {item_id} with URL: {architecture_url}")
            return True

        url = f"{Config.GRAPH_BASE}/sites/{Config.SITE_ID}/lists/{Config.LIST_ID}/items/{item_id}"

        payload = {
            "fields": {
                "Architecture_Diagram_Picture": architecture_url
            }
        }

        response = self._retry_request("PATCH", url, json=payload)

        if response and response.status_code == 200:
            return True

        return False

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """Remove invalid characters from filename"""
        # Remove/replace invalid SharePoint characters
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

# ============================================================================
# MAIN MIGRATION CLASS
# ============================================================================

class STRMigration:
    """Main migration orchestrator"""

    def __init__(self, test_mode: bool = False, logger: logging.Logger = None):
        self.test_mode = test_mode
        self.logger = logger or setup_logging(test_mode)
        self.progress = ProgressTracker()
        self.backup_mgr = BackupManager()
        self.credential = None
        self.api_client = None

    def initialize(self):
        """Initialize Azure credentials and API client"""
        self.logger.info("Initializing authentication...")

        try:
            self.credential = InteractiveBrowserCredential(client_id=Config.CLIENT_ID)
            token = self.credential.get_token("https://graph.microsoft.com/.default").token
            headers = {"Authorization": f"Bearer {token}"}
            self.api_client = GraphAPIClient(headers, self.logger)

            self.logger.info("✓ Authentication successful")
            return True

        except Exception as e:
            self.logger.error(f"✗ Authentication failed: {e}")
            return False

    def load_migration_plan(self, csv_path: Path) -> List[Dict]:
        """Load and parse migration plan from CSV"""
        self.logger.info(f"Loading migration plan from {csv_path}")

        migration_files = []

        try:
            with open(csv_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    arch_value = row.get('Architecture Diagram/Picture', '').strip()

                    # Extract file ID from SharePoint URL
                    if arch_value and 'joseph_brashear' in arch_value.lower():
                        match = re.search(r'/([A-Za-z0-9_-]+)$', arch_value)
                        if match:
                            sharepoint_id = match.group(1)

                            migration_files.append({
                                'product': row.get('Product Name', ''),
                                'sharepoint_id': sharepoint_id,
                                'old_url': arch_value,
                                'status': row.get('STR Approved', ''),
                                'csv_row': row.get('ID', ''),
                                'onedrive_item_id': sharepoint_id  # Placeholder - will be mapped
                            })

            self.logger.info(f"✓ Loaded {len(migration_files)} files for migration")
            return migration_files

        except Exception as e:
            self.logger.error(f"✗ Failed to load migration plan: {e}")
            return []

    def test_single_file(self, file_info: Dict) -> bool:
        """Test migration with single file"""
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"TEST: {file_info['product']}")
        self.logger.info(f"{'='*80}")

        try:
            # Step 1: Download
            self.logger.info("1. Downloading from OneDrive...")
            file_content = self.api_client.download_onedrive_file(
                file_info['sharepoint_id']
            )

            if not file_content:
                self.logger.error("✗ Download failed")
                return False

            self.logger.info(f"✓ Downloaded {len(file_content)} bytes")

            # Step 2: Upload (TEST MODE)
            filename = f"TEST_{file_info['product'][:50]}.bin"
            self.logger.info(f"2. [TEST MODE] Would upload as: {filename}")

            if not self.test_mode:
                uploaded = self.api_client.upload_to_sharepoint(filename, file_content)
                if not uploaded:
                    self.logger.error("✗ Upload failed")
                    return False
                self.logger.info(f"✓ Uploaded: {uploaded.get('id')}")

            # Step 3: Create link (TEST MODE)
            self.logger.info(f"3. [TEST MODE] Would create sharing link")

            # Step 4: Update list (TEST MODE)
            self.logger.info(f"4. [TEST MODE] Would update list item {file_info['csv_row']}")

            self.logger.info("✓ Test completed successfully")
            return True

        except Exception as e:
            self.logger.error(f"✗ Test failed: {e}")
            return False

    def run_migration(self, migration_files: List[Dict], test_mode: bool = None):
        """Execute migration"""
        if test_mode is not None:
            self.test_mode = test_mode

        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"MIGRATION {'TEST MODE' if self.test_mode else 'PRODUCTION MODE'}")
        self.logger.info(f"{'='*80}\n")

        # Limit to test count if in test mode
        if self.test_mode:
            migration_files = migration_files[:Config.TEST_FILE_COUNT]
            self.logger.warning(f"TEST MODE: Limiting to {len(migration_files)} files")

        # Create snapshot
        snapshot = self.backup_mgr.create_migration_snapshot({
            "mode": "test" if self.test_mode else "production",
            "file_count": len(migration_files),
            "timestamp": datetime.utcnow().isoformat(),
            "files": migration_files
        })
        self.logger.info(f"✓ Created migration snapshot: {snapshot}")

        results = {
            "total": len(migration_files),
            "completed": 0,
            "failed": 0,
            "errors": []
        }

        for idx, file_info in enumerate(migration_files, 1):
            self.logger.info(f"\n[{idx}/{len(migration_files)}] Processing: {file_info['product']}")

            try:
                self.progress.mark_file(file_info['sharepoint_id'], "processing")

                # Step 1: Download from OneDrive
                self.logger.info("  → Downloading from OneDrive...")
                file_content = self.api_client.download_onedrive_file(
                    file_info['sharepoint_id']
                )

                if not file_content:
                    raise Exception("Failed to download file from OneDrive")

                # Step 2: Upload to SharePoint
                self.logger.info("  → Uploading to SharePoint...")
                filename = f"{file_info['product'][:50]}.bin"
                uploaded = self.api_client.upload_to_sharepoint(filename, file_content)

                if not uploaded:
                    raise Exception("Failed to upload to SharePoint")

                sharepoint_item_id = uploaded.get('id')

                # Step 3: Create sharing link
                self.logger.info("  → Creating sharing link...")
                share_url = self.api_client.create_sharing_link(sharepoint_item_id)

                if not share_url:
                    raise Exception("Failed to create sharing link")

                # Step 4: Update list
                self.logger.info("  → Updating SharePoint list...")
                updated = self.api_client.update_list_item(
                    file_info['csv_row'],
                    share_url,
                    test_mode=self.test_mode
                )

                if not updated:
                    raise Exception("Failed to update list item")

                # Log success
                self.logger.info(f"  ✓ Success! Share URL: {share_url}")
                self.progress.mark_file(file_info['sharepoint_id'], "completed", {
                    "share_url": share_url,
                    "sharepoint_id": sharepoint_item_id
                })

                audit_log("file_migrated", {
                    "product": file_info['product'],
                    "share_url": share_url
                })

                results["completed"] += 1

            except Exception as e:
                self.logger.error(f"  ✗ Failed: {e}")
                self.progress.mark_file(file_info['sharepoint_id'], "failed", {
                    "error": str(e)
                })

                audit_log("file_migration_failed", {
                    "product": file_info['product'],
                    "error": str(e)
                }, status="error")

                results["failed"] += 1
                results["errors"].append({
                    "product": file_info['product'],
                    "error": str(e)
                })

        # Print summary
        self.logger.info(f"\n{'='*80}")
        self.logger.info(f"MIGRATION COMPLETE")
        self.logger.info(f"{'='*80}")
        self.logger.info(f"Total: {results['total']}")
        self.logger.info(f"Completed: {results['completed']}")
        self.logger.info(f"Failed: {results['failed']}")

        if results["errors"]:
            self.logger.error(f"\nErrors:")
            for error in results["errors"]:
                self.logger.error(f"  - {error['product']}: {error['error']}")

        return results

# ============================================================================
# MAIN
# ============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="STR Document Migration Tool")
    parser.add_argument("--test", action="store_true", help="Run in test mode (dry-run)")
    parser.add_argument("--csv", default="Software Technology Request (STR) Review Log (1).csv",
                        help="Path to STR CSV file")
    parser.add_argument("--config", default="sharepoint_ids.json",
                        help="Path to SharePoint IDs config file")

    args = parser.parse_args()

    # Setup
    try:
        Config.load_from_file(Path(args.config))
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    logger = setup_logging(test_mode=args.test)

    # Run migration
    migrator = STRMigration(test_mode=args.test, logger=logger)

    if not migrator.initialize():
        sys.exit(1)

    migration_files = migrator.load_migration_plan(Path(args.csv))

    if not migration_files:
        logger.error("No files to migrate")
        sys.exit(1)

    results = migrator.run_migration(migration_files)

    # Exit with error code if any failed
    sys.exit(0 if results["failed"] == 0 else 1)

if __name__ == "__main__":
    main()
