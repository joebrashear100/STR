# STR Migration - Failsafes and Recovery Guide

## Overview
This document outlines all failsafes built into the migration system and how to recover if something goes wrong.

## Built-in Failsafes

### 1. TEST MODE (No Data Changes)
```bash
python3 str_migration_robust.py --test
```
- **What it does:** Simulates entire migration without modifying anything
- **Safety:** 100% - no real changes to SharePoint or OneDrive
- **Use case:** Validate setup before production run
- **Limitations:** Only tests first 5 files by default (configurable)

### 2. Comprehensive Logging
Every operation is logged to multiple files:

```
migration_logs/
├── audit.jsonl          # Complete audit trail (one JSON per line)
├── errors.log           # All errors with timestamps
└── progress.json        # Current migration progress
```

**Audit log format:**
```json
{
  "timestamp": "2025-12-10T15:30:45.123456",
  "event_type": "file_migrated",
  "status": "success",
  "data": {
    "product": "Product Name",
    "share_url": "https://..."
  }
}
```

### 3. Progress Tracking & Resumption
- **What it does:** Records every file processed
- **Location:** `migration_logs/progress.json`
- **Use case:** Resume migration if interrupted
- **Benefits:** No duplicate uploads if script crashes

**Progress file format:**
```json
{
  "started": "2025-12-10T15:30:00.000000",
  "total": 288,
  "completed": 45,
  "failed": 2,
  "files": {
    "01GRK4NMZ7X6RGAAXIAJBZRECHSDRZVTCC": {
      "status": "completed",
      "timestamp": "2025-12-10T15:30:45.123456",
      "details": {
        "share_url": "https://deltaairlines.sharepoint.com/..."
      }
    }
  }
}
```

### 4. Backup Before Updates
- **What it does:** Backs up SharePoint list items before updating
- **Location:** `migration_backups/backup_[ITEM_ID]_[TIMESTAMP].json`
- **When:** Before updating list item with new URL
- **Use case:** Restore original URL if needed

### 5. Migration Snapshot
- **What it does:** Records complete migration plan before starting
- **Location:** `migration_backups/snapshot_[TIMESTAMP].json`
- **Contains:** All 288 files to be migrated with metadata
- **Use case:** Audit what was supposed to happen

### 6. Retry Logic
- **What it does:** Automatically retries failed requests up to 3 times
- **Backoff:** 2 second delay between retries
- **Covers:** Network timeouts, temporary API failures
- **Rate limiting:** Respects SharePoint rate limits

### 7. Error Isolation
- **What it does:** If one file fails, migration continues for others
- **Error handling:** Logs error and moves to next file
- **Result:** Partial success is better than total failure
- **Recovery:** Failed files listed in audit log for retry

### 8. Filename Sanitization
- **What it does:** Removes invalid SharePoint characters
- **Invalid chars:** `< > : " / \ | ? *`
- **Prevents:** Upload failures due to bad filenames

## Recovery Procedures

### Scenario 1: Migration Interrupted (Network/Power Loss)

**Recovery Steps:**
```bash
# 1. Check progress
cat migration_logs/progress.json

# 2. Run again - will skip completed files
python3 str_migration_robust.py

# 3. Script automatically skips already-processed files
```

**How it works:**
- Script loads `progress.json`
- Checks which files already completed
- Resumes from next unprocessed file
- No duplicates created

### Scenario 2: Files Uploaded But URLs Not Applied

**Detection:**
1. Check audit log:
   ```bash
   grep "file_migrated" migration_logs/audit.jsonl | wc -l
   ```

2. Check SharePoint list for empty "Architecture Diagram" fields

**Recovery:**
```bash
# Create a recovery script that updates all URLs from audit log
python3 str_recovery_apply_urls.py migration_logs/audit.jsonl
```

(Script creation shown below)

### Scenario 3: Wrong Files Uploaded to SharePoint

**What to do:**
1. **Don't panic** - Nothing changed in the original CSV
2. Stop the migration immediately
3. Delete uploaded files from SharePoint STRDocuments library:
   ```bash
   # Use SharePoint UI to delete files, OR
   # Use provided deletion script
   python3 str_recovery_delete_uploaded.py migration_logs/progress.json
   ```

4. Fix the issue
5. Run migration again

**Why safe:** Your original OneDrive files are untouched

### Scenario 4: List Items Updated with Wrong URLs

**Detection:**
```bash
# Check what was written to list
grep "update_list_item" migration_logs/audit.jsonl
```

**Recovery - Option A: Restore from Backup**
```bash
python3 str_recovery_restore_backups.py migration_backups/backup_*
```

**Recovery - Option B: Manual Restore**
1. Go to SharePoint list: `STR_Review_Log_Post_March_2023`
2. Filter for items updated after migration start time
3. Manually restore original URLs from `migration_logs/audit.jsonl`
4. Or restore from backups created before migration

### Scenario 5: Only Some Files Failed

**What happened:**
```bash
# Check which failed
grep '"status": "error"' migration_logs/audit.jsonl
```

**Recovery:**
```bash
# Create a CSV of just failed files
python3 str_recovery_failed_files.py migration_logs/progress.json > failed_files.csv

# Update config for just failed files
python3 str_migration_robust.py --csv failed_files.csv
```

## Pre-Migration Checklist

Before running migration:

- [ ] Run `Get_SharePoint_IDs.ps1` and verify IDs in `sharepoint_ids.json`
- [ ] Verify you have read/write access to:
  - [ ] OneDrive STRIntakeDocumentLibrary
  - [ ] SharePoint site: https://deltaairlines.sharepoint.com/sites/DL001597/PDO
  - [ ] Library: STRDocuments
  - [ ] List: STR_Review_Log_Post_March_2023
- [ ] Back up current SharePoint list:
  ```bash
  python3 -m sharepoint_list_backup.py
  ```
- [ ] Test with 1 file in test mode:
  ```bash
  python3 str_migration_robust.py --test
  ```
- [ ] Review test mode output for any errors
- [ ] Verify logs created in `migration_logs/`

## Test Mode Walkthrough

### Step 1: Run Test Mode
```bash
python3 str_migration_robust.py --test
```

**Expected output:**
```
================================
MIGRATION TEST MODE
================================

[1/5] Processing: Product Name
  → Downloading from OneDrive...
  ✓ Downloaded 144762 bytes
  → Uploading to SharePoint...
  [TEST MODE] Would upload as: TEST_Product_Name.bin
  → Creating sharing link...
  [TEST MODE] Would create sharing link
  → Updating SharePoint list...
  [TEST MODE] Would update list item 123
  ✓ Test completed successfully
```

### Step 2: Verify Logs
```bash
# Check audit log exists
ls -lh migration_logs/audit.jsonl

# Check progress file
cat migration_logs/progress.json | head -20

# Check for errors
cat migration_logs/errors.log
```

### Step 3: Verify No Changes
```bash
# Nothing should be in SharePoint yet
# List should be unchanged
# OneDrive should be unchanged
```

### Step 4: Run Real Migration
```bash
python3 str_migration_robust.py
```

## Monitoring During Migration

### Real-time Monitoring
```bash
# Watch progress in real-time
tail -f migration_logs/errors.log

# Or check progress
watch -n 5 'cat migration_logs/progress.json | jq ".completed, .failed, .total"'
```

### Stopping Safely
```bash
# Press Ctrl+C to stop
# Script will:
# 1. Save progress
# 2. Exit cleanly
# 3. Allow resumption later
```

## Post-Migration Validation

### 1. Count Uploaded Files
```bash
# Should match number in progress.json
grep '"status": "completed"' migration_logs/progress.json | wc -l
```

### 2. Verify URLs in SharePoint List
```bash
# Open SharePoint list
# Filter "Architecture Diagram/Picture" column
# Should have URLs like: https://deltaairlines.sharepoint.com/...
```

### 3. Test One URL
```bash
# Click a URL to verify it's accessible
# Should show read-only view
# Should not allow editing
```

### 4. Create Final Report
```bash
python3 str_generate_report.py migration_logs/
```

## Emergency Rollback

If something catastrophic happens:

### Option 1: Restore from Backup
```bash
# Restore list items from backups
for backup in migration_backups/backup_*.json; do
    python3 str_recovery_restore_single.py "$backup"
done
```

### Option 2: Delete All Uploaded Files
```bash
# Delete all files uploaded by migration
python3 str_recovery_delete_uploaded.py migration_logs/progress.json
```

### Option 3: Manual SharePoint List Reset
1. Go to SharePoint list
2. View "Architecture Diagram/Picture" column
3. Find items with new URLs (after migration timestamp)
4. Restore original URLs from your CSV backup

## File Structure

```
STR/
├── str_migration_robust.py           # Main migration script
├── sharepoint_ids.json               # Generated by Get_SharePoint_IDs.ps1
├── migration_logs/                   # Created during migration
│   ├── audit.jsonl                   # Complete audit trail
│   ├── errors.log                    # Error log
│   └── progress.json                 # Migration progress
├── migration_backups/                # Created during migration
│   ├── snapshot_*.json               # Migration plan snapshot
│   └── backup_*.json                 # Individual item backups
└── Software Technology Request (STR) Review Log (1).csv  # Your original CSV
```

## Support & Troubleshooting

### Common Issues

**"Authentication failed"**
- Solution: Run script again, complete browser login

**"Rate limited"**
- Solution: Script automatically waits, continue or restart

**"File upload failed"**
- Check: Filename for invalid characters (sanitized automatically)
- Check: Permissions on STRDocuments library

**"List update failed"**
- Check: Field name is "Architecture_Diagram_Picture"
- Check: List item ID is correct
- Check: URL format is valid

### Getting Help

1. Check `migration_logs/errors.log`
2. Review relevant audit entries in `migration_logs/audit.jsonl`
3. Check backups in `migration_backups/`
4. See "Recovery Procedures" section above

## Key Takeaways

✓ **Test first** with `--test` flag
✓ **Monitor progress** in `migration_logs/`
✓ **Can resume** if interrupted
✓ **Can rollback** with backups
✓ **Can fix partial** failures individually
✓ **Original data untouched** on OneDrive/CSV
✓ **Complete audit trail** for compliance
