# STR Document Migration System

> **Production-ready automation for migrating 288 STR diagrams from OneDrive to SharePoint with comprehensive failsafes**

## 🚀 Quick Start (5 minutes)

### 1. Get SharePoint IDs
```powershell
./Get_SharePoint_IDs.ps1
```

### 2. Test Mode (Safe, No Changes)
```bash
python3 str_migration_robust.py --test
```

### 3. Run Migration
```bash
python3 str_migration_robust.py
```

### 4. Verify Results
Check SharePoint list for updated URLs.

---

## 📋 What This Does

| Step | Source | Destination | Result |
|------|--------|-------------|--------|
| 1 | OneDrive STRIntakeDocumentLibrary | ✓ Download | File content |
| 2 | File content | SharePoint STRDocuments | ✓ Upload | File in SharePoint |
| 3 | SharePoint file | ✓ Create link | Read-only org URL |
| 4 | New URL | SharePoint list | ✓ Update | URL in list |

**Total: 288 files migrated, 288 URLs created, 288 list items updated**

---

## 🛡️ 8 Built-in Failsafes

1. **Test Mode** - Dry-run with zero data changes
2. **Audit Logging** - Every operation recorded (audit.jsonl)
3. **Progress Tracking** - Resume from exact stopping point
4. **Backups** - Original list items backed up
5. **Migration Snapshots** - Complete migration plan recorded
6. **Retry Logic** - Up to 3 automatic retries with backoff
7. **Error Isolation** - One failure doesn't stop entire migration
8. **Filename Sanitization** - Invalid characters removed

---

## 📚 Documentation Files

| File | Purpose | Read Time |
|------|---------|-----------|
| **`QUICK_START_MIGRATION.md`** | 5-minute setup guide | 5 min |
| **`MIGRATION_SUMMARY.md`** | Complete overview | 10 min |
| **`MIGRATION_FAILSAFES_AND_RECOVERY.md`** | Detailed recovery procedures | 15 min |
| **`STR_Migration_Implementation_Guide.md`** | Technical architecture | 20 min |
| **`Graph_API_Test_Example.md`** | Tested API examples | 10 min |

---

## 🔧 Files Included

### Scripts
```
str_migration_robust.py         # Main migration orchestrator (600+ lines)
Get_SharePoint_IDs.ps1          # Retrieves SharePoint configuration
```

### Configuration (Auto-Generated)
```
sharepoint_ids.json             # Created by Get_SharePoint_IDs.ps1
```

### Logging (Auto-Created During Migration)
```
migration_logs/
├── audit.jsonl                 # Complete audit trail (JSON per line)
├── progress.json               # Resumable progress tracker
└── errors.log                  # Error log

migration_backups/
├── snapshot_*.json             # Migration plan snapshots
└── backup_*.json               # Original list item backups
```

---

## 📊 What Gets Logged

### Audit Trail (audit.jsonl)
Every operation recorded with timestamp:
```json
{
  "timestamp": "2025-12-10T15:30:45.123456",
  "event_type": "file_migrated",
  "status": "success",
  "data": { "product": "...", "share_url": "..." }
}
```

### Progress Tracking (progress.json)
Resumable progress for interrupted migrations:
```json
{
  "completed": 45,
  "failed": 2,
  "total": 288,
  "files": { ... }
}
```

### Backups
- Snapshot of entire migration plan before starting
- Original SharePoint list items backed up before updating

---

## ✅ Pre-Migration Checklist

- [ ] Python 3.8+ installed
- [ ] `pip install azure-identity requests`
- [ ] Ran `Get_SharePoint_IDs.ps1`
- [ ] Verified `sharepoint_ids.json` created
- [ ] Tested in test mode: `python3 str_migration_robust.py --test`
- [ ] Reviewed logs from test run
- [ ] Have 2-8 hours available
- [ ] Backed up SharePoint list (recommended)

---

## 🧪 Test Mode Examples

### Run test with 5 files
```bash
python3 str_migration_robust.py --test
```

**Output:**
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

**Nothing changes** - pure simulation.

---

## 🔄 Recovery Procedures

### Migration Interrupted?
```bash
python3 str_migration_robust.py  # Auto-resumes from last successful file
```

### Some files failed?
```bash
# Check which failed
grep '"status": "failed"' migration_logs/progress.json

# Retry - auto-skips completed files
python3 str_migration_robust.py
```

### Need to rollback?
See: `MIGRATION_FAILSAFES_AND_RECOVERY.md`
- Detailed recovery for every scenario
- Rollback procedures
- Emergency procedures

---

## ⏱️ Performance

**Time Estimate:**
- 288 files × 15-30 seconds per file = **2-8 hours**
- Respects SharePoint rate limits
- Can run in background

**Resource Usage:**
- Network: Moderate (1-2 MB average per file)
- CPU: Minimal
- Memory: ~100 MB
- Disk: Logs + backups = ~10-50 MB

---

## 🔍 Monitoring During Migration

### Watch progress real-time
```bash
tail -f migration_logs/errors.log
```

### Check progress snapshot
```bash
cat migration_logs/progress.json | grep -E "completed|failed|total"
```

### Stop safely
```bash
Ctrl+C  # Graceful shutdown, saves progress
```

---

## ✨ Success Criteria

Migration is successful when:
- ✓ Completed count matches expected
- ✓ URLs in SharePoint list are populated
- ✓ URLs are read-only and accessible
- ✓ No errors in audit.jsonl (or all errors handled)
- ✓ Original OneDrive files unchanged
- ✓ Original CSV unchanged

---

## 🚨 If Something Goes Wrong

**Step 1:** Stop migration (Ctrl+C)
**Step 2:** Check error log
```bash
cat migration_logs/errors.log
tail -20 migration_logs/audit.jsonl
```

**Step 3:** Follow recovery procedure
See: `MIGRATION_FAILSAFES_AND_RECOVERY.md`

**Step 4:** Restart migration
```bash
python3 str_migration_robust.py  # Auto-resumes
```

---

## 📖 Detailed Guides

### For quick overview
→ Read: `QUICK_START_MIGRATION.md`

### For complete picture
→ Read: `MIGRATION_SUMMARY.md`

### For recovery procedures
→ Read: `MIGRATION_FAILSAFES_AND_RECOVERY.md`

### For technical details
→ Read: `STR_Migration_Implementation_Guide.md`

### For API testing
→ Read: `Graph_API_Test_Example.md`

---

## 🔐 Security & Compliance

✓ Audit trail for compliance (`audit.jsonl`)
✓ Timestamps on all operations
✓ No credentials stored in files
✓ Read-only sharing links (organization only)
✓ Complete backups before changes
✓ No data loss possible (reversible)

---

## 📞 Support

**First:** Check `migration_logs/errors.log`
**Then:** See `MIGRATION_FAILSAFES_AND_RECOVERY.md`
**Still stuck:** Check `QUICK_START_MIGRATION.md` FAQ

---

## Version Info

- **Version:** 1.0
- **Status:** Production Ready
- **Testing:** Complete with failsafes
- **Recovery:** Fully documented
- **Last Updated:** 2025-12-10

---

## 🎯 Next Steps

1. Read: `QUICK_START_MIGRATION.md`
2. Run: `Get_SharePoint_IDs.ps1`
3. Test: `python3 str_migration_robust.py --test`
4. Review: `migration_logs/`
5. Migrate: `python3 str_migration_robust.py`
6. Verify: Check SharePoint list
7. Archive: `tar czf migration_backups/final.tar.gz migration_logs/`

---

**Ready? Let's go! 🚀**

Start with: `QUICK_START_MIGRATION.md`
