# Power Fx Code for Exporting STR SharePoint List to Excel

## Overview
This document provides Power Fx code options for exporting the "Software Technology Request (STR) Review Log" SharePoint list to Excel from a Power Apps button.

---

## Option 1: SharePoint Native Export (Recommended - Simplest)

This method uses SharePoint's built-in Excel export functionality via the `Launch()` function.

### OnSelect Code:
```powerfx
// Export STR SharePoint List to Excel using SharePoint's native export
Launch(
    "https://deltaairlines.sharepoint.com/sites/DL001597/PDO/_vti_bin/owssvr.dll?CS=65001&Using=_layouts/query.iqy&List={dcfc03d1-1c02-4870-916d-bf7f5a2f71ba}&View={00000000-0000-0000-0000-000000000000}&CacheControl=1"
);
Notify("Excel export initiated. Check your downloads.", NotificationType.Success);
```

### Alternative Native Export URL:
```powerfx
// Alternative: Direct Excel Web Query export
Launch(
    "https://deltaairlines.sharepoint.com/sites/DL001597/PDO/_layouts/15/download.aspx?SourceUrl=" &
    EncodeUrl("https://deltaairlines.sharepoint.com/sites/DL001597/PDO/Lists/Software Technology Request (STR) Review Log") &
    "&FldUrl=" &
    EncodeUrl("AllItems.aspx")
);
```

---

## Option 2: Export with Filtered Data (Current View/Gallery)

Use this when you want to export only the filtered/displayed records from a gallery.

### OnSelect Code:
```powerfx
// Collect filtered data from gallery into a collection
ClearCollect(
    colSTRExport,
    ShowColumns(
        Gallery_STR.AllItems,
        "Title",
        "Product Name",
        "Requestor Name",
        "Requestor Email Address",
        "Block Code",
        "Vendor Name",
        "Vendor State",
        "Business Unit",
        "Description",
        "STR Approved",
        "IR Approver",
        "Infosec Approver",
        "Arch Gov Approver",
        "FinOps Approver",
        "Date Requested",
        "Created",
        "Modified"
    )
);

// Trigger Power Automate flow to generate Excel
'STR-ExportToExcel'.Run(
    JSON(colSTRExport, JSONFormat.IndentFour)
);

Notify("Exporting " & CountRows(colSTRExport) & " records to Excel...", NotificationType.Information);
```

---

## Option 3: Full Export with All Columns (Power Automate Trigger)

### OnSelect Code:
```powerfx
// Set loading state
UpdateContext({varExporting: true});

// Collect all STR records with key columns
ClearCollect(
    colSTRFullExport,
    AddColumns(
        'Software Technology Request (STR) Review Log',
        "ExportDate", Text(Now(), "yyyy-mm-dd hh:mm:ss"),
        "ProductNameText", ThisRecord.'Product Name',
        "RequestorNameText", ThisRecord.'Requestor Name',
        "VendorNameText", ThisRecord.'Vendor Name',
        "STRApprovedText", ThisRecord.'STR Approved'.Value,
        "IRApproverText", ThisRecord.'IR Approver'.Value,
        "InfosecApproverText", ThisRecord.'Infosec Approver'.Value,
        "ArchGovApproverText", ThisRecord.'Arch Gov Approver'.Value,
        "FinOpsApproverText", ThisRecord.'FinOps Approver'.Value,
        "AIGenAIText", Concat(ThisRecord.'AI / GenAI Technology', Value, ", "),
        "AWSText", Concat(ThisRecord.AWS, Value, ", ")
    )
);

// Trigger the export flow
'STR-GenerateExcelReport'.Run(
    JSON(colSTRFullExport, JSONFormat.IndentFour),
    User().Email,
    Text(Now(), "yyyy-mm-dd")
);

// Reset loading state and notify
UpdateContext({varExporting: false});
Notify("Export complete! Check your email for the Excel file.", NotificationType.Success);
```

---

## Option 4: Quick Export Button with Progress Indicator

### OnSelect Code:
```powerfx
// Initialize export process
UpdateContext({
    varExportStatus: "Preparing data...",
    varIsExporting: true,
    varExportProgress: 0
});

// Get total record count
Set(varTotalRecords, CountRows('Software Technology Request (STR) Review Log'));

UpdateContext({
    varExportStatus: "Collecting " & varTotalRecords & " records...",
    varExportProgress: 25
});

// Collect the data
ClearCollect(
    colExportData,
    ShowColumns(
        'Software Technology Request (STR) Review Log',
        "ID",
        "Title",
        "Product Name",
        "Requestor Name",
        "Requestor Name (From IT)",
        "Requestor Email Address",
        "Block Code (if applicable)",
        "Criticality Tier",
        "Vendor Name",
        "Vendor State",
        "Business Unit",
        "Description",
        "Developer Tool/Library",
        "Request Type Add",
        "POC/Pilot End Date",
        "Date Requested",
        "Session Date",
        "STR Approved",
        "PIA Completed",
        "VRA Completed",
        "Contract Executed",
        "Governance Approval",
        "IR Approver",
        "Infosec Approver",
        "Arch Gov Approver",
        "CCoE Approver",
        "FinOps Approver",
        "Notes",
        "Internal Dev",
        "Restricted to Domain/Business Area",
        "Product Type",
        "AI / GenAI Technology",
        "Cloud Based Solution",
        "SaaS Product Integrates with Delta's Global Auth/MFA",
        "AWS",
        "Other Information",
        "URL for Free/Open-Source Product",
        "Software Executables",
        "Environment Type",
        "Created",
        "Modified"
    )
);

UpdateContext({
    varExportStatus: "Generating Excel file...",
    varExportProgress: 75
});

// Launch SharePoint export
Launch(
    "https://deltaairlines.sharepoint.com/sites/DL001597/PDO/_vti_bin/owssvr.dll?CS=65001&Using=_layouts/query.iqy&List={dcfc03d1-1c02-4870-916d-bf7f5a2f71ba}&CacheControl=1",
    {},
    LaunchTarget.New
);

UpdateContext({
    varExportStatus: "Complete!",
    varExportProgress: 100,
    varIsExporting: false
});

Notify("Excel export started. The file will download shortly.", NotificationType.Success);
```

---

## Option 5: Export to OneDrive as Excel (Using Power Automate)

This requires a companion Power Automate flow that creates an Excel file in OneDrive.

### Button OnSelect Code:
```powerfx
// Prepare export parameters
Set(
    varExportParams,
    {
        FileName: "STR_Export_" & Text(Now(), "yyyymmdd_hhmmss") & ".xlsx",
        UserEmail: User().Email,
        FilterApproved: If(Toggle_ApprovedOnly.Value, "Yes", "All"),
        DateFrom: If(IsBlank(DatePicker_From.SelectedDate), "", Text(DatePicker_From.SelectedDate, "yyyy-mm-dd")),
        DateTo: If(IsBlank(DatePicker_To.SelectedDate), "", Text(DatePicker_To.SelectedDate, "yyyy-mm-dd"))
    }
);

// Call Power Automate flow
Set(
    varExportResult,
    'STR-ExportToOneDrive'.Run(
        varExportParams.FileName,
        varExportParams.UserEmail,
        varExportParams.FilterApproved,
        varExportParams.DateFrom,
        varExportParams.DateTo
    )
);

// Show result
If(
    varExportResult.Success,
    Notify("Excel file created: " & varExportResult.FileUrl, NotificationType.Success);
    Launch(varExportResult.FileUrl),
    Notify("Export failed: " & varExportResult.ErrorMessage, NotificationType.Error)
);
```

---

## Option 6: Simple One-Click Export (Most User-Friendly)

### OnSelect Code:
```powerfx
// One-click export to Excel using SharePoint's native functionality
Launch(
    Concatenate(
        "https://deltaairlines.sharepoint.com/sites/DL001597/PDO/",
        "_layouts/15/download.aspx?UniqueId={dcfc03d1-1c02-4870-916d-bf7f5a2f71ba}"
    ),
    {},
    LaunchTarget.New
);

// Provide user feedback
Notify(
    "Opening Excel export. If download doesn't start, check your popup blocker.",
    NotificationType.Information,
    5000
);
```

---

## Companion Power Automate Flow (For Options 3 & 5)

Create a Power Automate flow named "STR-ExportToOneDrive" with these steps:

### Flow Definition:
1. **Trigger**: PowerApps (V2)
   - Input: FileName, UserEmail, FilterApproved, DateFrom, DateTo

2. **Get Items**: SharePoint - Get items
   - Site: https://deltaairlines.sharepoint.com/sites/DL001597/PDO
   - List: Software Technology Request (STR) Review Log
   - Filter Query: (if FilterApproved = "Yes") `STR_x0020_Approved eq 'Approved'`

3. **Create Table**: Excel Online - Create table
   - Location: OneDrive for Business
   - File: /STRExports/@{triggerBody()['text']}

4. **Add Rows**: Apply to each
   - For each item, add row to Excel table

5. **Create Sharing Link**: OneDrive - Create sharing link

6. **Respond to PowerApps**: Return Success, FileUrl, ErrorMessage

---

## SharePoint List Details

| Property | Value |
|----------|-------|
| **Site URL** | https://deltaairlines.sharepoint.com/sites/DL001597/PDO |
| **List Name** | Software Technology Request (STR) Review Log |
| **List ID (GUID)** | dcfc03d1-1c02-4870-916d-bf7f5a2f71ba |
| **Total Columns** | 74+ |
| **Key Approval Columns** | STR Approved, IR Approver, Infosec Approver, Arch Gov Approver, FinOps Approver |

---

## Recommended Implementation

For most use cases, **Option 1** (SharePoint Native Export) is recommended because:
- No additional flows required
- Uses SharePoint's built-in export functionality
- Works immediately without setup
- Includes all columns automatically

For filtered exports or custom formatting, use **Option 3** or **Option 5** with a companion Power Automate flow.

---

## Notes

1. **Internal Column Names**: SharePoint uses encoded column names internally (e.g., `STR_x0020_Approved` for "STR Approved"). The Power Fx code above uses display names which Power Apps handles automatically.

2. **Multi-Select Columns**: Columns like "AI / GenAI Technology" and "AWS" are multi-select and need special handling with `Concat()` for text export.

3. **User Columns**: "Requestor Name" and similar user columns return complex objects. Use `.DisplayName` or `.Email` to get text values.

4. **Performance**: For large datasets (1000+ records), consider using pagination or batching in Power Automate flows.
