# STR Migration - Quick Start Guide

## 5-Minute Setup

### 1. Get SharePoint IDs (Windows PowerShell)
```powershell
cd ~/STR
./Get_SharePoint_IDs.ps1
```

This creates `sharepoint_ids.json` with:
- Site ID
- Drive ID (STRDocuments library)
- List ID (STR_Review_Log_Post_March_2023)

### 2. Install Python Dependencies
```bash
pip install azure-identity requests
```

### 3. Run Test Mode (5 files)
```bash
cd ~/STR
python3 str_migration_robust.py --test
```

**Expected:** Simulates migration without changing anything
**Check:** Look for `✓ Test completed successfully` messages

### 4. Verify Test Created Logs
```bash
ls -la migration_logs/
ls -la migration_backups/
```

**Should have:**
- `audit.jsonl` - Audit trail
- `progress.json` - Progress tracking
- `errors.log` - Error log
- `snapshot_*.json` - Migration plan

## Ready? Run Full Migration

```bash
python3 str_migration_robust.py
```

**This will:**
1. Download 288 files from OneDrive
2. Upload to SharePoint STRDocuments
3. Create read-only sharing links
4. Update SharePoint list with new URLs

**Time estimate:** ~30-60 minutes (288 files, respects rate limits)

**Progress:** Watch in real-time
```bash
tail -f migration_logs/errors.log
```

## If Something Goes Wrong

**Migration interrupted?**
```bash
# Just run again - skips already-processed files
python3 str_migration_robust.py
```

**Some files failed?**
```bash
# Check which ones failed
grep "error" migration_logs/audit.jsonl
```

**Need to rollback?**
See: `MIGRATION_FAILSAFES_AND_RECOVERY.md`

## What Gets Created

### In Migration Logs:
```
migration_logs/
├── audit.jsonl          ← Complete record of every file
├── progress.json        ← Can resume from here
└── errors.log           ← Any errors that occurred
```

### In Migration Backups:
```
migration_backups/
├── snapshot_*.json      ← What was planned
└── backup_*.json        ← Original SharePoint list data
```

### In SharePoint:
- STRDocuments library gets 288 new files
- STR_Review_Log_Post_March_2023 list gets updated URLs

### Your Original Files:
- OneDrive STRIntakeDocumentLibrary: **UNCHANGED**
- CSV file: **UNCHANGED**

## Verification Checklist

After migration completes:

- [ ] Check final count: `grep "completed" migration_logs/progress.json`
- [ ] Open SharePoint list and spot-check a few URLs
- [ ] Click a link to verify it works (read-only)
- [ ] Compare completed count to expected (should be 288 or close)

## Logs Location

All logs in your STR repository:
- `migration_logs/` - Live during migration
- `migration_backups/` - Saved for recovery

These are added to `.gitignore` so they won't clog your repo.

## Commands Cheat Sheet

```bash
# Run test mode (dry-run, 5 files)
python3 str_migration_robust.py --test

# Run full migration
python3 str_migration_robust.py

# Check progress
cat migration_logs/progress.json | grep -E "completed|failed|total"

# Watch errors real-time
tail -f migration_logs/errors.log

# Count successful migrations
grep '"status": "completed"' migration_logs/progress.json | wc -l

# See which files failed
grep '"status": "failed"' migration_logs/progress.json
```

## Common Questions

**Q: Is test mode really safe?**
A: 100% safe. Nothing is modified, just simulated.

**Q: Can I stop mid-migration?**
A: Yes! Just Ctrl+C. When you restart, it skips already-done files.

**Q: What if 10 files fail?**
A: See `MIGRATION_FAILSAFES_AND_RECOVERY.md` for retry procedure.

**Q: Are my original files safe?**
A: Yes! OneDrive and CSV are never modified.

**Q: How do I verify the URLs work?**
A: Click one in SharePoint list after migration. Should open read-only.

## Next Steps

1. ✓ Run `Get_SharePoint_IDs.ps1`
2. ✓ Run `python3 str_migration_robust.py --test`
3. ✓ Review logs in `migration_logs/`
4. ✓ Run `python3 str_migration_robust.py` (full migration)
5. ✓ Verify URLs in SharePoint list
6. ✓ Archive logs to `migration_backups/final_report/`

Questions? See `MIGRATION_FAILSAFES_AND_RECOVERY.md`
