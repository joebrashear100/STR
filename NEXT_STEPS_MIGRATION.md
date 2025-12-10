# STR Document Migration - Next Steps

## You Now Have:
1. ✓ Implementation guide (`STR_Migration_Implementation_Guide.md`)
2. ✓ PowerShell script to get IDs (`Get_SharePoint_IDs.ps1`)
3. ✓ OneDrive file metadata with FileLocator IDs (`STRDocumentOneDriveTXT.rtf`)
4. ✓ CSV with 288 STRs that need diagrams uploaded

## Immediate Action Items:

### Step 1: Get SharePoint IDs (5 minutes)

**Run PowerShell:**
```powershell
cd ~/STR
./Get_SharePoint_IDs.ps1
```

**What you'll get:**
- Site ID
- Drive ID (for STRDocuments library)
- List ID (for STR_Review_Log_Post_March_2023)

These will be saved to `sharepoint_ids.json`

### Step 2: Extract FileLocator IDs from OneDrive (Done, but needs formatting)

You have the metadata in `STRDocumentOneDriveTXT.rtf` which contains:
- File IDs
- FileLocator IDs
- Filenames

We need to create a mapping CSV with:
```
onedrive_item_id, filename, sharepoint_list_item_id
01GRK4NMZ7X6RGAAXIAJBZRECHSDRZVTCC, "0009de35...Cypress-Flow.png", "1"
```

### Step 3: Map OneDrive Files to SharePoint List Items

We need to correlate:
- **OneDrive FileLocator IDs** → from STRDocumentOneDriveTXT.rtf
- **Filenames** → from OneDrive metadata
- **SharePoint List Item IDs** → from the STR_Review_Log_Post_March_2023 list

This is the crucial mapping step.

### Step 4: Create Python Migration Script

Once we have the IDs and mapping, the Python script will:
1. Download each file from OneDrive
2. Upload to SharePoint STRDocuments library
3. Create read-only org-only sharing link
4. Update the SharePoint list with the new URL

### Step 5: Run Migration

```bash
python3 str_migration_script.py
```

## Key Questions to Resolve:

1. **How do we map OneDrive files to SharePoint list items?**
   - Option A: Match by filename from the STR CSV
   - Option B: Match by creation date/modified date
   - Option C: Manual mapping file

2. **What's the relationship between:**
   - The 288 STRs in CSV with diagram URLs
   - The 1,652 files in OneDrive STRIntakeDocumentLibrary
   - Which files should go to SharePoint?

**Answer from conversation:** The 288 STRs that currently have OneDrive URLs in the "Architecture Diagram/Picture" column

## Files You Already Have:

| File | Purpose |
|------|---------|
| Software Technology Request (STR) Review Log (1).csv | CSV with all 1,468 STRs |
| STRDocumentOneDriveTXT.rtf | OneDrive metadata with FileLocator IDs |
| STRIntakeDocumentLibrary/ | Bulk export of 1,652 OneDrive documents |
| Graph_API_Test_Example.md | Tested Graph API call example |
| STR_Migration_Implementation_Guide.md | Technical implementation guide |
| Get_SharePoint_IDs.ps1 | Script to get SharePoint IDs |

## Recommended Next Action:

**I recommend we create an automated script that:**

1. Extracts the 288 STRs with existing OneDrive URLs from CSV
2. For each STR:
   - Gets the OneDrive file ID from FileLocator
   - Finds the matching file in OneDrive
   - Copies it to SharePoint STRDocuments
   - Creates sharing link
   - Updates SharePoint list item

This would be fully automated and traceable.

**Would you like me to:**
- [ ] Create the FileLocator extraction script?
- [ ] Build the complete end-to-end migration script?
- [ ] Start with a test migration of 5 files?

