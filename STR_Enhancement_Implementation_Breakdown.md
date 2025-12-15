# STR Power App Enhancement Implementation Breakdown

## Executive Summary

This document provides a detailed breakdown of implementation requirements for each proposed STR Power App enhancement. Each item is assessed for complexity, required changes, dependencies, and technical approach.

**Complexity Legend:**
- 🟢 **Low** - Simple UI/config change, 1-2 hours
- 🟡 **Medium** - Multiple component changes, testing required, 4-8 hours
- 🟠 **High** - Cross-system changes, workflow modifications, 1-3 days
- 🔴 **Complex** - Architecture changes, new integrations, 3-5+ days

---

## I. Base Information Tab Enhancements

### 1. Remove "Internal Dev" field (add as 'Delta Built' under Product Type)
**Complexity:** 🟢 Low

**Current State:**
- `Internal_x0020_Dev` field exists as Yes/No radio in Base Information tab
- Stored in SharePoint list as boolean field

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App UI | Remove `Internal_x0020_Dev` radio control from Base Information tab |
| Power App UI | Add "Delta Built" option to Product Type radio/combo in Request Information tab |
| SharePoint List | Hide/deprecate `Internal_x0020_Dev` column (keep for historical data) |
| Workflow | Update `STR_SubmitToSharepoint` to exclude Internal_Dev from concatenation |
| Reports | Update any reports referencing Internal_Dev |

**Technical Approach:**
1. Edit STRFormScreen → Base Information tab controls
2. Modify Product Type combo/radio ItemsSource to include "Delta Built"
3. Update workflow input parsing logic
4. Data migration: Map existing Internal_Dev=Yes to Product_Type="Delta Built"

**Dependencies:** None

---

### 2. Add Vendor Status option: "Free / Open Source"
**Complexity:** 🟢 Low

**Current State:**
- Vendor fields exist (Vendor Name, Vendor State)
- No explicit "Vendor Status" dropdown visible

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| SharePoint List | Add new column `Vendor_Status` (Choice: Commercial, Free/Open Source, etc.) |
| Power App UI | Add dropdown control in Base Information tab |
| Workflow | Include new field in submission concatenation |

**Technical Approach:**
1. Add SharePoint column: `Vendor_Status` as Choice field with options
2. Add Dropdown control to Base Information tab
3. Update `STR_SubmitToSharepoint` to include field in data string
4. Refresh data connection in Power App

**Dependencies:** SharePoint schema change first

---

### 3. Add "Is product funded: yes/no"
**Complexity:** 🟢 Low

**Current State:**
- Financial tab has cost fields but no funding status indicator

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| SharePoint List | Add new column `Is_Product_Funded` (Yes/No) |
| Power App UI | Add Yes/No radio in Base Information or Financial tab |
| Workflow | Include in submission data |

**Technical Approach:**
1. Create SharePoint column
2. Add radio control with Yes/No options
3. Wire to form submission logic

**Dependencies:** None

---

### 4. Make Business Unit a Required Field
**Complexity:** 🟢 Low

**Current State:**
- Business Unit exists as dropdown in Base Information tab
- Not currently enforced as required

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App UI | Add validation check on Business Unit before submit |
| Power App UI | Display error message if empty on submit attempt |
| SharePoint List | Mark column as required (optional, app-level enforcement preferred) |

**Technical Approach:**
1. Modify Submit button `OnSelect` to check `IsBlank(BusinessUnit.Selected)`
2. Show notification or error label if validation fails
3. Disable submit until field populated

**Dependencies:** None

---

### 5. Make Domain a Required Field
**Complexity:** 🟢 Low

**Current State:**
- "Restricted to Domain/Business Area" combo exists
- Not currently required

**Required Changes:**
Same pattern as Business Unit above.

**Dependencies:** None

---

## II. Request Information Tab Enhancements

### 6. Add options under "Cloud Based Solution": AWS Delta Cloud, Hybrid
**Complexity:** 🟢 Low

**Current State:**
- Cloud Based Solution is Yes/No radio
- Need to change to multi-option selection

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| SharePoint List | Modify `Cloud_Based_Solution` to Choice with values: On-Premises, AWS Delta Cloud, Hybrid, Other |
| Power App UI | Replace Yes/No radio with dropdown/combo |
| Workflow | Update parsing logic for new values |
| Reports | Update any Cloud Based Solution filters |

**Technical Approach:**
1. Modify SharePoint column type to Choice
2. Update control from radio to dropdown
3. Map historical Yes→"Cloud", No→"On-Premises"

**Dependencies:** Data migration for existing records

---

### 7. Add under AWS: "Existing AWS Services"
**Complexity:** 🟢 Low

**Current State:**
- AWS field is multi-select combo with options
- Example values: "EC2", "S3", "Lambda", etc.

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App UI | Add "Existing AWS Services" to AWS combo ItemsSource |
| SharePoint List | Update Choice options if using SharePoint choices |

**Technical Approach:**
1. Edit AWS combo control Items property
2. Add new option to choice collection

**Dependencies:** None

---

### 8. Add new Yes/No question: "Will the solution utilize MCP servers?"
**Complexity:** 🟡 Medium

**Current State:**
- No MCP server field exists
- Requirement notes need to configure automation to update ZAP catalog

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| SharePoint List | Add `MCP_Servers` column (Yes/No) |
| Power App UI | Add Yes/No radio with label in Request Information tab |
| Workflow | Add conditional logic: if Yes, trigger ZAP catalog update |
| Integration | Create ZAP catalog update API/workflow connection |
| Approval | Route to CCoE for approval if Yes |

**Technical Approach:**
1. Add SharePoint column
2. Add UI control
3. Create new Power Automate flow for ZAP integration:
   - Trigger: When MCP_Servers = Yes
   - Action: Call ZAP catalog API/update SharePoint list
   - Notify CCoE team
4. Add CCoE approval gate in workflow

**Dependencies:**
- ZAP catalog API documentation/access
- CCoE approval workflow integration

**Notes:** This is higher complexity due to external system integration

---

### 9. Add new Yes/No question: "Will the solution utilize agents?"
**Complexity:** 🟡 Medium

**Current State:**
- AI/GenAI Technology multi-select exists but no specific "agents" field

**Required Changes:**
Same pattern as MCP servers above - likely same ZAP catalog integration.

| Component | Change Required |
|-----------|-----------------|
| SharePoint List | Add `Uses_Agents` column (Yes/No) |
| Power App UI | Add Yes/No radio in Request Information tab |
| Workflow | Conditional ZAP catalog update if Yes |
| Integration | CCoE approval requirement |

**Dependencies:** Same as MCP servers enhancement

---

### 10. Add "Delta Built" under Product Type
**Complexity:** 🟢 Low

(See item #1 - this is the same enhancement, adding Delta Built as option to Product Type)

---

### 11. Verbiage update: "where will service provided be hosted" → "where will this be hosted?"
**Complexity:** 🟢 Low

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App UI | Update label text for Cloud Based Solution question |

**Technical Approach:**
1. Edit label control Text property in STRFormScreen

**Dependencies:** None

---

### 12. Add "processing, please wait" verbiage on submit
**Complexity:** 🟢 Low

**Current State:**
- Submit button calls workflow directly
- No loading indicator visible

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App UI | Add loading overlay/spinner component |
| Power App UI | Add "Processing, please wait..." label |
| Power App UI | Disable submit button during processing |
| Power App UI | Show overlay on submit, hide on completion |

**Technical Approach:**
```powerfx
// Add variable for loading state
Set(varIsSubmitting, true);
// Show overlay
UpdateContext({showLoadingOverlay: true});
// Call workflow
STR_SubmitToSharepoint.Run(...);
// Hide overlay
Set(varIsSubmitting, false);
UpdateContext({showLoadingOverlay: false});
```

**Dependencies:** None

---

### 13. Rename "Submit Draft Copy" → "Save Draft Copy"
**Complexity:** 🟢 Low

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App UI | Update SaveDraftBttn Text property to "Save Draft Copy" |

**Dependencies:** None

---

### 14. Rename "Forward Request to Architect" → "Forward to Architect for Review"
**Complexity:** 🟢 Low

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App UI | Update button text property |

**Dependencies:** None

---

## III. Approval Tab Enhancements

### 15. Add filter by STR Approver on Approval Tab
**Complexity:** 🟡 Medium

**Current State:**
- RequestApprovalScreen shows requests pending approval
- No filtering by specific approver visible

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App UI | Add dropdown/combo for approver selection |
| Power App UI | Add filter logic to approval gallery |
| Power App UI | Options: IR Approver, Infosec, Architecture, FinOps |

**Technical Approach:**
1. Add Dropdown with approver types
2. Modify gallery Items formula:
```powerfx
Filter('STR Review Log',
    If(ApproverFilter.Selected.Value = "IR",
        IR_Approver = "Pending",
        ApproverFilter.Selected.Value = "Infosec",
        Infosec_Approver = "Pending",
        ...
    )
)
```

**Dependencies:** None

---

### 16. Add "STR Approval Status" column (pending approval, cancelled, rejected, on hold, approved)
**Complexity:** 🟡 Medium

**Current State:**
- `STR_x0020_Approved` exists with values: Approved, Rejected, Pending
- Missing: Cancelled, On Hold

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| SharePoint List | Update `STR_Approved` column choices: add "Cancelled", "On Hold" |
| Power App UI | Add status display to right side of existing approval status |
| Power App UI | Add ability to set status to "On Hold" or "Cancelled" |
| Workflow | Update `STR_ApproveRequest` to handle new statuses |

**Technical Approach:**
1. Extend SharePoint Choice column
2. Add status controls in approval UI
3. Modify workflow conditional logic for new statuses

**Dependencies:** Workflow update required

---

## IV. Email Notification Enhancements

### 17. Modify Architect email with direct link and new subject/body
**Complexity:** 🟠 High

**Current State:**
- `STR_DOC_New_Product_Request_Notification_v0.1` workflow sends notifications
- Current subject and body format unknown (workflow not in export)

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power Automate | Create/modify notification workflow |
| Email Template | New subject: "STR #XXXX New Product (Name) Draft Review Action Required" |
| Email Template | New body with personalized greeting and deep link |
| Deep Link | Generate Power App URL with STR ID parameter |

**New Email Format:**
```
Subject: STR #{ID} New Product ({Product Name}) Draft Review Action Required

Body:
Hello {Architect Name},

STR product draft request #{ID} ({Product Name}) is pending your action to review
each tab of the STR request, and provide your analysis and recommendations in the
Requirements for Submission Tab.

If the STR has all required information including the design diagram, upon adding
your analysis and recommendations, select the 'submit final copy' button to route
for approval.

You can review and take action on the request by clicking the link below:

[Open Request in Power App](https://apps.powerapps.com/play/e/[env-id]/a/[app-id]?ID={STR_ID}&screen=RequestHistoryScreen)
```

**Technical Approach:**
1. Create/export notification workflow
2. Update Send Email action:
   - Subject: Use dynamic content for ID, Product Name
   - Body: HTML template with deep link
   - Deep link: `https://apps.powerapps.com/play/e/{env}/a/{app-id}?ID=@{triggerBody()?['ID']}&screen=RequestHistory`
3. Remove "kindly do not reply" footer

**Dependencies:**
- Access to notification workflow (not currently in export)
- Environment ID and App ID for deep link construction

---

### 18. Remove "kindly do not reply..." from automated emails
**Complexity:** 🟢 Low

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power Automate | Edit email body template to remove disclaimer |

**Dependencies:** Access to email workflow

---

## V. Mandates Tab Enhancements

### 19. Expand notes boxes on Mandates Tab
**Complexity:** 🟢 Low

**Current State:**
- Notes/text boxes have fixed height

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App UI | Increase Height property of text input controls |
| Power App UI | Or set Mode to Multiline with AutoHeight |

**Technical Approach:**
1. Select notes TextInput controls on Mandates tab
2. Increase Height property (e.g., from 100 to 200)
3. Or enable multiline with larger MinHeight

**Dependencies:** None

---

## VI. Copy/Duplicate STR Functionality

### 20. Ability to copy/duplicate a previous STR
**Complexity:** 🟠 High

**Current State:**
- No copy functionality exists
- Form always starts blank

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App UI | Add "Copy from existing STR" button on form screen |
| Power App UI | Add STR selection dialog/gallery |
| Power App UI | Populate form fields from selected STR |
| Power App UI | Clear ID and timestamps (create as new) |

**Technical Approach:**
1. Add button "Copy from Previous STR"
2. On click, show modal gallery of existing STRs
3. On selection, populate all form fields:
```powerfx
// Example for one field
Set(varProductName, SelectedSTR.Product_Name);
Set(varDescription, SelectedSTR.Description);
// ... repeat for all fields
```
4. Clear system fields (ID, Created, Modified, Approval statuses)
5. Set form as new submission

**Form Fields to Copy (~100+ fields):**
- Product Name, Description, Business Unit
- Vendor details
- Request Type, Product Type
- Financial information
- Legal/Governance details
- Architecture info (without diagram - prompt to upload new)

**Dependencies:** None, but extensive field mapping required

---

### 21. Ability to resubmit rejected STR copying original information
**Complexity:** 🟡 Medium

**Current State:**
- Rejected STRs remain in list with status "Rejected"
- No resubmission workflow

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App UI | Add "Resubmit" button on rejected STRs in Request History |
| Power App UI | Populate form with original values |
| Power App UI | Reset approval statuses to Pending |
| Workflow | Create new STR record or update existing |

**Technical Approach:**
Option A - Create new STR from rejected:
1. Copy all fields to new form submission
2. Link new STR to original (add `Previous_STR_ID` field)
3. Submit as new request

Option B - Reset and resubmit existing:
1. Use `Request_Update` workflow pattern
2. Reset all approval statuses
3. Allow form edits
4. Resubmit for approval

**Dependencies:** Business decision on approach (new record vs. update existing)

---

## VII. Request Cancellation

### 22. Ability to cancel requests (with email notification)
**Complexity:** 🟡 Medium

**Current State:**
- No cancellation functionality
- Status doesn't include "Cancelled"

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| SharePoint List | Add "Cancelled" to STR_Approved choices |
| Power App UI | Add "Cancel Request" button on Request History |
| Power App UI | Confirmation dialog before cancellation |
| Workflow | Create Cancel Request workflow |
| Email | Send cancellation notification |

**Technical Approach:**
1. Add status option
2. Add Cancel button (only visible to requestor/admin)
3. Create `STR_CancelRequest` workflow:
   - Update status to "Cancelled"
   - Send email: "Request #{ID} has been cancelled. No further action required."
   - Optionally hide from default views

**Email Template:**
```
Subject: STR #{ID} - Request Cancelled

The STR request #{ID} ({Product Name}) has been cancelled.
No further action is required.

If you have questions, please contact {Requestor Email}.
```

**Dependencies:** New workflow creation

---

## VIII. Request History Screen Enhancements

### 23. Double-click on left panel to collapse/expand for full STR view
**Complexity:** 🟡 Medium

**Current State:**
- Fixed panel layout
- Gallery on left, details on right

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App UI | Add toggle variable for panel state |
| Power App UI | Add OnDobleSelect action to gallery container |
| Power App UI | Conditional Width for left panel (e.g., 300px or 0px) |
| Power App UI | Expand right panel when left collapsed |

**Technical Approach:**
```powerfx
// Variable
Set(varPanelCollapsed, false);

// OnDoubleSelect (or use invisible button overlay)
Set(varPanelCollapsed, !varPanelCollapsed);

// Left Panel Width
If(varPanelCollapsed, 0, 300)

// Right Panel Width
If(varPanelCollapsed, Parent.Width, Parent.Width - 300)
```

**Note:** Power Apps doesn't have native OnDoubleClick. Workarounds:
- Timer-based double-click detection
- Collapse/Expand button instead
- Toggle icon

**Dependencies:** None

---

### 24. Update AI/GenAI field to yes/no selection in SharePoint
**Complexity:** 🟢 Low

**Current State:**
- AI_x002F_GenAI_Technology is multi-select combo (selected items)
- Contains specific AI types

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| SharePoint List | Add new column `Uses_AI_GenAI` (Yes/No) |
| Power App UI | Add Yes/No radio in addition to or replacing multi-select |
| Logic | If Yes, show the detailed AI types; if No, hide/skip |

**Alternative:** Keep multi-select but add boolean flag derived from it:
```powerfx
// Derived field
Set(varUsesAI, CountRows(AIGenAICombo.SelectedItems) > 0)
```

**Dependencies:** Business decision on UI approach

---

### 25. Add export data button next to refresh
**Complexity:** 🟡 Medium

**Current State:**
- Refresh button exists
- No export functionality in app

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App UI | Add "Export" button icon next to Refresh |
| Power App UI | On click, trigger export action |
| Integration | Use Power Automate to generate Excel and email to user |

**Technical Approach:**

Option A - SharePoint Direct Link:
```powerfx
// Button OnSelect - Open SharePoint export
Launch("https://deltaairlines.sharepoint.com/sites/DL001597/PDO/_layouts/15/download.aspx?...")
```

Option B - Power Automate Export:
1. Create `STR_ExportData` workflow:
   - Input: Filter criteria (date range, status, etc.)
   - Action: Get all items from SharePoint
   - Action: Create Excel file using "Create table" action
   - Action: Email Excel to requestor

Option C - Dataverse/Power Apps Premium:
- Use PDF function (requires Premium)

**Dependencies:**
- Premium license for some export options
- New workflow for automated export

---

### 26. Determine average time for STR approval (clock starts at final copy)
**Complexity:** 🟡 Medium

**Current State:**
- `Created` timestamp exists
- `Data_Approved` timestamp set on approval
- `Form_Submission_Type` distinguishes Draft/Final

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| SharePoint List | Add `Final_Copy_Submitted_Date` column (DateTime) |
| Workflow | Set timestamp when Form_Submission_Type changes to "Final Copy" |
| Power App UI | Calculate and display: `Data_Approved - Final_Copy_Submitted_Date` |
| Dashboard | Create avg approval time metric |

**Technical Approach:**
1. Add date column for final submission timestamp
2. Update `STR_SubmitToSharepoint` workflow:
   - If FormType = "Final Copy", set Final_Copy_Submitted_Date = utcNow()
3. Calculate duration in app:
```powerfx
DateDiff(Final_Copy_Submitted_Date, Data_Approved, TimeUnit.Days) & " days"
```
4. Aggregate for dashboard:
```powerfx
Average(Filter('STR Review Log', STR_Approved = "Approved"),
    DateDiff(Final_Copy_Submitted_Date, Data_Approved, TimeUnit.Hours))
```

**Dependencies:** Workflow modification

---

### 27. Update status to "Under Review" when final copy submitted (with date stamp)
**Complexity:** 🟡 Medium

**Current State:**
- Status values: Approved, Rejected, Pending
- No "Under Review" status

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| SharePoint List | Add "Under Review" to STR_Approved choices |
| SharePoint List | Add `Under_Review_Date` column |
| Workflow | Update status on final copy submission |
| Workflow | Reset to "Pending" if sent back for updates |

**Technical Approach:**
1. Extend status choices
2. Modify `STR_SubmitToSharepoint`:
   - If Final Copy → Status = "Under Review", set Under_Review_Date
3. Modify `Request_Update`:
   - Reset status to "Pending", clear Under_Review_Date

**Status Flow:**
```
Draft → Pending
Final Copy Submitted → Under Review (timestamp)
Sent Back → Pending (clear timestamp)
Final Copy Resubmitted → Under Review (new timestamp)
All Approved → Approved
Any Rejected → Rejected
```

**Dependencies:** Workflow modifications

---

### 28. Improve product search to match anywhere in name (not just first word)
**Complexity:** 🟡 Medium

**Current State:**
- Search likely uses StartsWith or exact match
- Only finds if search term is at beginning of product name

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App UI | Update gallery filter formula to use contains/in |

**Technical Approach:**

Current (assumed):
```powerfx
Filter('STR Review Log', StartsWith(Product_Name, SearchInput.Text))
```

Updated:
```powerfx
Filter('STR Review Log',
    SearchInput.Text in Product_Name ||
    SearchInput.Text in Requestor_Name ||
    SearchInput.Text in Description
)
// Or using Search function
Search('STR Review Log', SearchInput.Text, "Product_Name", "Description")
```

**Performance Note:** `in` operator may be slower than `StartsWith` on large datasets. Consider:
- Delegable query limits (2000 default)
- Increasing delegation limit
- Server-side search if needed

**Dependencies:** None, but test performance with 11,000+ records

---

### 29. Automated email for duplicate product name/requestor
**Complexity:** 🟠 High

**Current State:**
- No duplicate detection
- Multiple STRs can be created for same product

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Workflow | Add duplicate check on submission |
| Workflow | Query for existing STRs with same Product_Name AND Requestor |
| Email | Send notification if duplicate found |
| Power App UI | Optional: Show warning before submit |

**Technical Approach:**
1. Modify `STR_SubmitToSharepoint` workflow:
```
// Get items with same product name and requestor
Get items: Filter = Product_Name eq '{ProductName}' and Requestor_Email eq '{Email}'
// If count > 0
Send email: "A previous STR for {Product Name} was submitted by you on {Date}..."
// Continue with submission anyway (or block)
```

2. App-side pre-check (optional):
```powerfx
Set(varDuplicates,
    Filter('STR Review Log',
        Product_Name = txtProductName.Text &&
        Requestor_Email = User().Email
    )
);
If(CountRows(varDuplicates) > 0,
    Notify("Similar STR already exists: " & First(varDuplicates).ID)
)
```

**Dependencies:** Decision on behavior (warn vs. block)

---

## IX. Document Management Enhancements

### 30. Ability to upload additional documents
**Complexity:** 🟠 High

**Current State:**
- Single Architecture Diagram upload
- Single AI Impact Diagram upload
- Files stored in OneDrive, URLs in SharePoint

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App UI | Add "Upload Additional Documents" section |
| Power App UI | Gallery for multiple file uploads |
| SharePoint | Create document library folder per STR |
| Workflow | Handle multiple file uploads |
| Workflow | Store file URLs in related list or JSON field |

**Technical Approach:**

Option A - Attachments Library:
1. Create SharePoint document library: `STR_Attachments`
2. Create folder per STR ID
3. Upload multiple files to folder
4. Store folder URL in STR record

Option B - Attachments Field:
1. Add multi-value URL field or related list
2. Each upload creates entry
3. Display as gallery of links

**Workflow Changes:**
```
// For each file in upload collection
Create file in SharePoint: STR_Attachments/{STR_ID}/{filename}
Create sharing link
Append to attachment URLs
// Update STR record with all URLs
```

**Dependencies:**
- SharePoint library setup
- Significant workflow modification
- Consider file size limits

---

### 31. Move diagrams to central place
**Complexity:** 🟡 Medium (Already In Progress)

**Current State:**
- Migration system exists: `str_migration_robust.py`
- Migrating from OneDrive to SharePoint STRDocuments library
- 288 products identified for migration

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Migration Script | Complete remaining migrations |
| Workflow | Update `STR_SubmitToSharepoint` to save directly to SharePoint |
| Configuration | Update OneDrive references to SharePoint |

**Technical Approach:**
1. Complete migration using existing robust script
2. Modify workflow to upload to SharePoint instead of OneDrive
3. Update any hardcoded OneDrive paths

**Dependencies:** Migration completion

---

## X. Platform/Access Enhancements

### 32. Lock down Teams for opening Power App in web application
**Complexity:** 🟡 Medium

**Current State:**
- App can be opened in Teams or browser

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App Settings | Configure launch behavior |
| Teams App | Create Teams app manifest with web-only launch |
| Admin Center | Configure app policies |

**Technical Approach:**
1. In Power Apps settings, configure "Open in browser" as default
2. Create Teams app that opens web URL instead of embedded:
```json
{
  "staticTabs": [{
    "contentUrl": "https://apps.powerapps.com/play/e/{env}/a/{app-id}",
    "websiteUrl": "https://apps.powerapps.com/play/e/{env}/a/{app-id}"
  }]
}
```
3. Admin policy to enforce web launch

**Dependencies:** Admin access, Teams app publishing

---

### 33. Add high-risk criteria to create flag
**Complexity:** 🟡 Medium

**Current State:**
- No risk flagging system

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| SharePoint List | Add `High_Risk_Flag` (Yes/No) |
| SharePoint List | Add `Risk_Criteria_Met` (Multi-choice) |
| Power App UI | Add visual flag indicator (red icon/banner) |
| Logic | Auto-flag based on criteria |

**High-Risk Criteria (define with business):**
- AI/GenAI = Yes
- Cloud = External (not AWS Delta)
- Handles PII/sensitive data
- External vendor with access
- No indemnification
- High operational cost

**Technical Approach:**
```powerfx
// Auto-calculate risk flag
Set(varHighRisk,
    AIGenAI = "Yes" ||
    CloudSolution = "External" ||
    ContainsPII = "Yes" ||
    // Add other criteria
);

// Visual indicator
If(ThisItem.High_Risk_Flag,
    Icon.Warning,
    Icon.Check
)
```

**Dependencies:** Business definition of risk criteria

---

### 34. Mobile app visibility
**Complexity:** 🟡 Medium

**Current State:**
- App designed for Tablet layout (1369x2843 px)
- Portrait and Landscape enabled

**Required Changes:**
| Component | Change Required |
|-----------|-----------------|
| Power App | Create Phone layout version |
| Power App | Responsive containers for small screens |
| Testing | Test on iOS and Android devices |

**Technical Approach:**
1. Add Phone form factor in Power Apps Studio
2. Create responsive layouts using containers
3. Simplify forms for mobile (collapsible sections)
4. Test on Power Apps mobile app

**Layout Considerations:**
- Tab navigation → Bottom nav or hamburger menu
- Wide forms → Single column stack
- Galleries → Full-width cards
- Approval actions → Prominent buttons

**Dependencies:** Design decisions for mobile UX

---

## XI. Summary Table

| # | Enhancement | Complexity | Est. Effort | Dependencies |
|---|-------------|------------|-------------|--------------|
| 1 | Remove Internal Dev, add Delta Built | 🟢 Low | 2 hrs | Data migration |
| 2 | Vendor Status: Free/Open Source | 🟢 Low | 1 hr | SharePoint column |
| 3 | Is product funded yes/no | 🟢 Low | 1 hr | SharePoint column |
| 4 | Business Unit required | 🟢 Low | 1 hr | None |
| 5 | Domain required | 🟢 Low | 1 hr | None |
| 6 | Cloud options: AWS Delta, Hybrid | 🟢 Low | 2 hrs | Data migration |
| 7 | AWS: Existing Services | 🟢 Low | 30 min | None |
| 8 | MCP servers yes/no + ZAP | 🟡 Medium | 4-8 hrs | ZAP API |
| 9 | Agents yes/no + ZAP | 🟡 Medium | 4-8 hrs | ZAP API |
| 10 | Delta Built under Product Type | 🟢 Low | (same as #1) | None |
| 11 | Verbiage: hosting question | 🟢 Low | 15 min | None |
| 12 | Processing please wait | 🟢 Low | 1 hr | None |
| 13 | Save Draft Copy rename | 🟢 Low | 15 min | None |
| 14 | Forward to Architect rename | 🟢 Low | 15 min | None |
| 15 | Filter by STR Approver | 🟡 Medium | 2-4 hrs | None |
| 16 | STR Approval Status expanded | 🟡 Medium | 3-4 hrs | Workflow |
| 17 | Architect email with deep link | 🟠 High | 4-8 hrs | Workflow access |
| 18 | Remove email disclaimer | 🟢 Low | 30 min | Workflow access |
| 19 | Expand mandate notes boxes | 🟢 Low | 30 min | None |
| 20 | Copy/duplicate STR | 🟠 High | 8-16 hrs | None |
| 21 | Resubmit rejected STR | 🟡 Medium | 4-6 hrs | Business decision |
| 22 | Cancel requests + email | 🟡 Medium | 4-6 hrs | New workflow |
| 23 | Collapsible panel | 🟡 Medium | 2-4 hrs | None |
| 24 | AI/GenAI yes/no | 🟢 Low | 2 hrs | Business decision |
| 25 | Export data button | 🟡 Medium | 4-8 hrs | Workflow |
| 26 | Avg approval time | 🟡 Medium | 4-6 hrs | Workflow |
| 27 | Under Review status | 🟡 Medium | 3-4 hrs | Workflow |
| 28 | Improved product search | 🟡 Medium | 2-4 hrs | Performance test |
| 29 | Duplicate detection email | 🟠 High | 4-8 hrs | Decision on behavior |
| 30 | Additional document uploads | 🟠 High | 8-16 hrs | SharePoint setup |
| 31 | Centralize diagrams | 🟡 Medium | (in progress) | Migration completion |
| 32 | Lock Teams to web | 🟡 Medium | 2-4 hrs | Admin access |
| 33 | High-risk flag | 🟡 Medium | 4-6 hrs | Risk criteria |
| 34 | Mobile visibility | 🟡 Medium | 8-16 hrs | Design decisions |

---

## XII. Recommended Implementation Order

### Phase 1: Quick Wins (Low complexity, high visibility)
1. Verbiage updates (#11, 13, 14)
2. Required fields (#4, 5)
3. Expand notes boxes (#19)
4. Processing indicator (#12)
5. Remove email disclaimer (#18)

### Phase 2: Form Enhancements
1. Cloud/AWS options (#6, 7)
2. Vendor Status (#2)
3. Is Funded (#3)
4. Delta Built/Internal Dev (#1, 10)
5. AI/GenAI yes/no (#24)

### Phase 3: Status & Search Improvements
1. STR Approval Status (#16)
2. Under Review status (#27)
3. Improved search (#28)
4. Approver filter (#15)
5. Collapsible panel (#23)

### Phase 4: Workflow Enhancements
1. Architect email + deep link (#17)
2. Cancel requests (#22)
3. Duplicate detection (#29)
4. Avg approval time (#26)
5. Export button (#25)

### Phase 5: Advanced Features
1. Copy/duplicate STR (#20)
2. Resubmit rejected (#21)
3. Additional documents (#30)
4. Complete diagram migration (#31)

### Phase 6: Platform & Integration
1. MCP servers + ZAP (#8)
2. Agents + ZAP (#9)
3. High-risk flag (#33)
4. Teams web lock (#32)
5. Mobile app (#34)

---

## XIII. Key Dependencies to Resolve

1. **ZAP Catalog API** - Needed for #8, #9 (MCP/Agents)
2. **Notification Workflow Access** - Needed for #17, #18
3. **Business Decisions:**
   - Risk criteria definition (#33)
   - Resubmission approach (#21)
   - Duplicate handling (#29)
   - AI/GenAI UI approach (#24)
4. **Admin Access** - Needed for #32 (Teams lock)
5. **Design Decisions** - Needed for #34 (Mobile)

---

## XIV. Indirect Impacts to Consider

### Data Migration Impacts
- Changing field types requires data migration for historical records
- Boolean to Choice changes need value mapping
- New required fields can't retroactively apply to existing records

### Reporting Impacts
- Status changes affect existing dashboards/reports
- New fields need to be added to reports
- Changed field names break existing queries

### Training Impacts
- New features require user documentation updates
- Verbiage changes need communication to users
- New approval statuses need approver training

### Integration Impacts
- Email changes may need IT Gov inbox configuration
- ZAP integration needs API credentials/permissions
- Deep links need app ID and environment ID

---

*Document Version: 1.0*
*Created: December 2024*
*Based on: STR Power App v1.0.0.6, Solution export analysis*
