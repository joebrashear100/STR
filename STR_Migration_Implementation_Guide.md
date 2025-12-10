
# STR Document Migration & URL Sharing Automation

## Overview
- Copy 288 STR diagrams from OneDrive to SharePoint Document Library
- Create read-only sharing links (org-only)
- Update SharePoint list with new URLs

## Architecture

```
OneDrive (STRIntakeDocumentLibrary)
    ↓
    ├─ Get file via Graph API using FileLocator ID
    ├─ Download file content
    ↓
SharePoint Document Library (STRDocuments)
    ├─ Upload file
    ├─ Create sharing link (read-only, org-only)
    ↓
SharePoint List (STR_Review_Log_Post_March_2023)
    └─ Update "Architecture Diagram/Picture" column with new URL
```

## Key SharePoint Details

**Target Site:** https://deltaairlines.sharepoint.com/sites/DL001597/PDO
**Target Library:** STRDocuments
**Target List:** STR_Review_Log_Post_March_2023

**Site ID:** DL001597
**Library Name:** STRDocuments

## Step 1: Get Necessary IDs from Graph API

First, we need to get:
- SharePoint site ID
- Document library ID (DriveId)
- List ID

### PowerShell to get IDs:

```powershell
# Connect to Microsoft Graph
Connect-MgGraph -Scopes "Sites.Read.All", "Lists.ReadWrite.All", "Files.ReadWrite.All"

# Get site by URL
$siteUrl = "https://deltaairlines.sharepoint.com/sites/DL001597/PDO"
$site = Get-MgSite -Search "DL001597" | Where-Object {$_.WebUrl -eq $siteUrl}
$siteId = $site.Id

Write-Output "Site ID: $siteId"

# Get drive (document library) ID for STRDocuments
$drive = Get-MgSiteDrive -SiteId $siteId | Where-Object {$_.Name -eq "STRDocuments"}
$driveId = $drive.Id

Write-Output "Drive ID: $driveId"

# Get list ID for STR_Review_Log_Post_March_2023
$list = Get-MgSiteList -SiteId $siteId -Filter "displayName eq 'STR_Review_Log_Post_March_2023'"
$listId = $list.Id

Write-Output "List ID: $listId"
```

## Step 2: Python Script - Main Automation

```python
import requests
import json
import time
from azure.identity import InteractiveBrowserCredential

class STRDocumentMigration:
    def __init__(self):
        # Initialize Graph API connection
        self.credential = InteractiveBrowserCredential(
            client_id="04b07795-8ddb-461a-bbee-02f9e1bf7b46"
        )
        self.token = self.credential.get_token("https://graph.microsoft.com/.default").token
        self.headers = {"Authorization": f"Bearer {self.token}"}
        
        # SharePoint details
        self.site_id = "DL001597"  # From step above
        self.drive_id = None  # Get from PowerShell
        self.list_id = None   # Get from PowerShell
        
    def get_onedrive_file_content(self, item_id):
        """Download file from OneDrive using Graph API"""
        url = f"https://graph.microsoft.com/v1.0/me/drive/items/{item_id}/content"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to download: {response.status_code}")
    
    def upload_to_sharepoint(self, filename, file_content, folder_path=""):
        """Upload file to SharePoint document library"""
        # Construct upload path
        if folder_path:
            upload_url = f"https://graph.microsoft.com/v1.0/drives/{self.drive_id}/root:/{folder_path}/{filename}:/content"
        else:
            upload_url = f"https://graph.microsoft.com/v1.0/drives/{self.drive_id}/root:/{filename}:/content"
        
        headers = self.headers.copy()
        headers["Content-Type"] = "application/octet-stream"
        
        response = requests.put(upload_url, data=file_content, headers=headers)
        
        if response.status_code in [201, 200]:
            return response.json()
        else:
            raise Exception(f"Upload failed: {response.status_code} - {response.text}")
    
    def create_sharepoint_sharing_link(self, item_id, permission_type="view"):
        """Create read-only org-only sharing link for SharePoint item"""
        url = f"https://graph.microsoft.com/v1.0/drives/{self.drive_id}/items/{item_id}/createLink"
        
        payload = {
            "type": "organizationView",  # org-only read-only
            "scope": "organization",
            "password": None
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        
        if response.status_code == 201:
            data = response.json()
            return data['link']['webUrl']
        else:
            raise Exception(f"Link creation failed: {response.status_code}")
    
    def update_sharepoint_list_item(self, item_id, architecture_diagram_url):
        """Update the STR list item with new URL"""
        url = f"https://graph.microsoft.com/v1.0/sites/{self.site_id}/lists/{self.list_id}/items/{item_id}"
        
        payload = {
            "fields": {
                "Architecture_Diagram_Picture": architecture_diagram_url
            }
        }
        
        response = requests.patch(url, json=payload, headers=self.headers)
        
        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Update failed: {response.status_code}")
    
    def migrate_file(self, onedrive_item_id, onedrive_filename, sharepoint_list_item_id):
        """Complete migration of one file"""
        try:
            # Step 1: Download from OneDrive
            print(f"Downloading {onedrive_filename}...")
            file_content = self.get_onedrive_file_content(onedrive_item_id)
            
            # Step 2: Upload to SharePoint
            print(f"Uploading to SharePoint...")
            uploaded = self.upload_to_sharepoint(onedrive_filename, file_content)
            sharepoint_item_id = uploaded['id']
            
            # Step 3: Create sharing link
            print(f"Creating sharing link...")
            share_url = self.create_sharepoint_sharing_link(sharepoint_item_id)
            
            # Step 4: Update SharePoint list
            print(f"Updating SharePoint list...")
            self.update_sharepoint_list_item(sharepoint_list_item_id, share_url)
            
            print(f"✓ Successfully migrated: {onedrive_filename}")
            return {"status": "success", "share_url": share_url}
            
        except Exception as e:
            print(f"✗ Failed: {onedrive_filename} - {str(e)}")
            return {"status": "failed", "error": str(e)}

# Usage example
if __name__ == "__main__":
    migrator = STRDocumentMigration()
    
    # Example: migrate one file
    result = migrator.migrate_file(
        onedrive_item_id="01GRK4NMZ7X6RGAAXIAJBZRECHSDRZVTCC",
        onedrive_filename="0009de35-a0ee-4a6b-be8f-3f138249b829Cypress-Flow.png",
        sharepoint_list_item_id="123"  # From SharePoint list
    )
    print(json.dumps(result, indent=2))
```

## Step 3: Bulk Migration Script

```python
import csv
from STRDocumentMigration import STRDocumentMigration

def bulk_migrate():
    migrator = STRDocumentMigration()
    
    # Load CSV with FileLocator IDs and map to SharePoint list items
    results = []
    
    with open('str_migration_list.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            onedrive_item_id = row['onedrive_item_id']
            filename = row['filename']
            sharepoint_list_item_id = row['sharepoint_list_item_id']
            
            result = migrator.migrate_file(
                onedrive_item_id,
                filename,
                sharepoint_list_item_id
            )
            
            results.append({
                'filename': filename,
                'result': result
            })
    
    # Save results
    with open('migration_results.json', 'w') as f:
        json.dump(results, f, indent=2)

bulk_migrate()
```

## What You Need to Do

1. **Get SharePoint IDs** (run PowerShell script above)
2. **Create CSV mapping file** with:
   - OneDrive item IDs
   - Filenames
   - SharePoint list item IDs
3. **Run Python migration script**
4. **Verify results**

## Expected Outcome

- All 288 files copied to SharePoint
- Each file has read-only org-only sharing link
- All links stored in SharePoint list "Architecture Diagram/Picture" column

