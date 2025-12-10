# STR Migration - Commands Reference

Quick copy-paste commands for the entire migration process.

## Pre-Migration

### 1. Install Dependencies
```bash
pip install azure-identity requests
```

### 2. Get SharePoint IDs (Windows PowerShell)
```powershell
cd ~/STR
./Get_SharePoint_IDs.ps1
```

Verify it created:
```bash
ls -la sharepoint_ids.json
cat sharepoint_ids.json
```

## Testing

### Run Test Mode (Safe, 5 Files)
```bash
python3 str_migration_robust.py --test
```

### View Test Logs
```bash
# Check if logs created
ls -la migration_logs/
ls -la migration_backups/

# View audit trail
cat migration_logs/audit.jsonl | head -20

# View progress
cat migration_logs/progress.json | jq .

# View errors
cat migration_logs/errors.log
```

## Full Migration

### Run Full Migration (288 Files)
```bash
python3 str_migration_robust.py
```

### Run in Background (Optional)
```bash
nohup python3 str_migration_robust.py > migration_background.log 2>&1 &
```

### Stop Migration Gracefully
```bash
Ctrl+C  # Or in background: kill %1
```

## Monitoring

### Watch Progress Real-Time
```bash
tail -f migration_logs/errors.log
```

### Check Current Progress
```bash
cat migration_logs/progress.json | jq '.completed, .failed, .total'
```

### Count Completed Files
```bash
grep '"status": "completed"' migration_logs/progress.json | wc -l
```

### Check Failed Files
```bash
grep '"status": "failed"' migration_logs/progress.json | jq '.files | to_entries[] | select(.value.status == "failed")'
```

## Analysis & Reporting

### Count Total Files Processed
```bash
jq '.completed + .failed' migration_logs/progress.json
```

### List Failed Files with Errors
```bash
jq '.files | to_entries[] | select(.value.status == "failed")' migration_logs/progress.json
```

### View All Uploaded URLs
```bash
grep '"file_migrated"' migration_logs/audit.jsonl | jq '.data.share_url'
```

### Summary Statistics
```bash
echo "=== Migration Summary ==="
echo "Completed: $(grep -c '"status": "completed"' migration_logs/progress.json)"
echo "Failed: $(grep -c '"status": "failed"' migration_logs/progress.json)"
echo "Started: $(jq '.started' migration_logs/progress.json)"
```

## Recovery

### Resume Interrupted Migration
```bash
python3 str_migration_robust.py  # Auto-resumes from last successful file
```

### Check Which Files Need Retry
```bash
grep '"status": "failed"' migration_logs/progress.json | jq '.files | keys'
```

### View Specific Error
```bash
# Replace FILENAME with actual filename
grep "FILENAME" migration_logs/errors.log -A 5
```

### Restore from Backup
```bash
# List available backups
ls -la migration_backups/

# View specific backup
cat migration_backups/backup_[ITEM_ID].json | jq .
```

## Post-Migration

### Count Success Rate
```bash
COMPLETED=$(grep -c '"status": "completed"' migration_logs/progress.json)
FAILED=$(grep -c '"status": "failed"' migration_logs/progress.json)
TOTAL=$((COMPLETED + FAILED))
echo "Success Rate: $((COMPLETED * 100 / TOTAL))% ($COMPLETED/$TOTAL)"
```

### Verify URLs in Audit Log
```bash
# Count URLs created
grep '"file_migrated"' migration_logs/audit.jsonl | wc -l

# Extract all URLs
grep '"file_migrated"' migration_logs/audit.jsonl | jq '.data.share_url' | sort | uniq | wc -l
```

### Archive Migration Logs
```bash
tar czf migration_backups/final_$(date +%Y%m%d_%H%M%S).tar.gz migration_logs/ migration_backups/
```

### Create Migration Report
```bash
echo "=== STR Migration Report ===" > migration_report.txt
echo "Date: $(date)" >> migration_report.txt
echo "Completed: $(grep -c '"status": "completed"' migration_logs/progress.json)" >> migration_report.txt
echo "Failed: $(grep -c '"status": "failed"' migration_logs/progress.json)" >> migration_report.txt
echo "Total Events: $(wc -l migration_logs/audit.jsonl)" >> migration_report.txt
echo "" >> migration_report.txt
echo "Failed Files:" >> migration_report.txt
grep '"status": "failed"' migration_logs/progress.json >> migration_report.txt
cat migration_report.txt
```

## Troubleshooting

### Check Authentication Status
```bash
python3 -c "from azure.identity import InteractiveBrowserCredential; c = InteractiveBrowserCredential(client_id='04b07795-8ddb-461a-bbee-02f9e1bf7b46'); t = c.get_token('https://graph.microsoft.com/.default'); print('✓ Authenticated')"
```

### Verify SharePoint IDs
```bash
jq '.' sharepoint_ids.json
```

### Check if Files Already Uploaded
```bash
ls migration_logs/progress.json && echo "✓ Progress file found"
```

### View Last 10 Errors
```bash
tail -n 10 migration_logs/errors.log
```

### Check for Stale Locks
```bash
# Progress files shouldn't be older than current migration
stat migration_logs/progress.json | grep Modify
date
```

## Advanced

### Extract All Product Names from Audit
```bash
grep '"file_migrated"' migration_logs/audit.jsonl | jq '.data.product' | sort | uniq
```

### Find Files That Took Longest
```bash
# Note: Requires enhanced logging - check timestamps in audit.jsonl
grep '"file_migrated"' migration_logs/audit.jsonl | jq '.timestamp' | sort | tail -10
```

### Validate All URLs are Organization-Only
```bash
grep '"file_migrated"' migration_logs/audit.jsonl | jq '.data.share_url' | grep -c "deltaairlines.sharepoint.com"
```

### Compare with Original CSV
```bash
# Count STRs in original CSV
grep -c '"Product Name"' "Software Technology Request (STR) Review Log (1).csv"

# Count files migrated
grep -c '"status": "completed"' migration_logs/progress.json

# Should be close to 288
```

## One-Liners

### Quick Status Check
```bash
echo "Completed: $(grep -c '"status": "completed"' migration_logs/progress.json) | Failed: $(grep -c '"status": "failed"' migration_logs/progress.json)"
```

### Export All URLs to Text File
```bash
grep '"file_migrated"' migration_logs/audit.jsonl | jq -r '.data.share_url' > all_sharepoint_urls.txt
```

### Clean Up Test Logs (Keep Production)
```bash
# Don't run this during migration!
# rm -rf migration_logs/* migration_backups/*
```

### Validate JSON Integrity
```bash
# Check audit.jsonl is valid
jq empty migration_logs/audit.jsonl && echo "✓ audit.jsonl is valid"

# Check progress.json is valid
jq empty migration_logs/progress.json && echo "✓ progress.json is valid"
```

---

## Tips & Tricks

### Don't lose your logs!
```bash
# Backup logs before deletion
cp -r migration_logs ~/backups/logs_$(date +%Y%m%d_%H%M%S)/
```

### Run multiple times safely
```bash
# Each run creates new log files with timestamps
# Logs are never deleted, only appended
```

### Monitor with system tools
```bash
# Watch file size grow
watch -n 5 'du -sh migration_logs/'

# Monitor network usage
# (depends on your OS)
```

### Create backup before each run
```bash
tar czf migration_backups/pre_migration_$(date +%s).tar.gz migration_logs/ migration_backups/ 2>/dev/null || true
```

---

Last updated: 2025-12-10
