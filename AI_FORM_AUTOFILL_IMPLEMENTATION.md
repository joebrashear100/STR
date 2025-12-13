# AI Form Autofill Implementation Guide

## Complete Field Mapping (75 Fields)

This table maps the pipe-delimited array indices to Power Apps controls and SharePoint columns.

| Index | Power Apps Control | SharePoint Column | Data Type | AI Extractable |
|-------|-------------------|-------------------|-----------|----------------|
| `[0]` | `RequestorNameCombo2.Selected.DisplayName` | `Requestor0` | Text | No (auto from user) |
| `[1]` | `RequestorNameCombo2.Selected.Mail` | `Requestor_x0020_Email` | Text | No (auto from user) |
| `[2]` | `DateRequestedPicker.SelectedDate` | `Date_Requested` | DateTime | No (auto today) |
| `[3]` | `BusUnitCmbBox.Selected.Value` | `Domain_x0020_Approved` | Choice | No |
| `[4]` | `RestrictedDomainCombo.Selected.Value` | `Restricted_x0020_to_x0020_Domain` | Choice | No |
| `[5]` | `ProductNameTxtInput.Value` | `Title` | Text | **Yes** |
| `[6]` | `DescriptionTxtInput.Value` | `Description` | Text | **Yes** |
| `[7]` | `NotesTxtInput.Value` | `Notes` | Text | **Yes** |
| `[8]` | `VendorNameTxtInput.Value` | `Vendor` | Text | **Yes** |
| `[9]` | `VendorStateComboBox.Selected.Value` | `Vendor_x0020_State` | Choice | **Yes** |
| `[10]` | `InternalBuildComboBox.Selected.Value` | `Internal_x0020_Build_x0020_Type` | Choice | **Yes** |
| `[11]` | `POCDurationTxtInpt.Value` | `POC_x002f_Pilot_x0020_Duration` | Text | **Yes** |
| `[12]` | `POCEndDatePicker.SelectedDate` | `POCEndDate` | DateTime | **Yes** |
| `[13]` | `BlockCodeTxtInput.Value` | `Block_x0020_Code` | Text | **Yes** |
| `[14]` | `ITManagerCombo.Selected.DisplayName` | `ITManagerText` | Text | No (person picker) |
| `[15]` | `ITPortfolioArchCombo.Selected.DisplayName` | `ITPortArchText` | Text | No (person picker) |
| `[16]` | `ProductTypeRadio.Selected.Value` | `Product_x0020_Type` | Choice | **Yes** |
| `[17]` | `JSON(AICombo.SelectedItems)` | `AI_x0020__x002f__x0020_GenAI_x00` | Multi-Choice | **Yes** |
| `[18]` | `JSON(AWSCombo.SelectedItems)` | `AWS` | Multi-Choice | **Yes** |
| `[19]` | `CriticalityTierRadio.Selected.Value` | `Criticality_x0020_Tier` | Choice | **Yes** |
| `[20]` | `ServiceProvidedRadio.Selected.Value` | `Cloud_x0020_Based_x0020_Solution` | Choice | **Yes** |
| `[21]` | `SaasIntegrateRadio.Selected.Value` | `SaaS_x0020_Product_x0020_Integra` | Choice | **Yes** |
| `[22]` | `OtherInformationRadio.Selected.Value` | `Other_x0020_Information` | Choice | No |
| `[23]` | `FreeOpenTextInput.Value` | `URL_x0020_for_x0020_Free_x002f_O` | Text | **Yes** |
| `[24]` | `SoftwareExecutablesTextInput.Value` | `Software_x0020_Executables` | Text | No |
| `[25]` | `AISecuirtyMandateRadio.Selected.Value` | `Confirm_x0020_AI_x0020_Mandate_x` | Choice | No |
| `[26]` | `SassSecuirtyMandateRadio.Selected.Value` | `Confirm_x0020_SaaS_x0020_Mandate` | Choice | No |
| `[27]` | `ProductSummaryTxtInpt.Value` | `Summary_x0020_of_x0020_New_x0020` | Text | **Yes** |
| `[28]` | `BusinessBenefitTxtInpt.Value` | `Describe_x0020_Business_x0020_Be` | Text | **Yes** |
| `[29]` | `BusinessCapabilitiesTxtInpt.Value` | `List_x0020_Specific_x0020_Capabi` | Text | **Yes** |
| `[30]` | `DataResidencyTxtInput.Value` | `Data_x0020_Residency_x002f_Proce` | Text | **Yes** |
| `[31]` | `EquivalentProductsTxtInpt.Value` | `List_x0020_Equivalent_x0020_Prod` | Text | **Yes** |
| `[32]` | `AlternativeSolutionsTxtInpt.Value` | `Describe_x0020_Alternative_x0020` | Text | **Yes** |
| `[33]` | `OneTimeCostTxtInpt.Value` | `Provide_x0020_One_x002d_Time_x00` | Text | **Yes** |
| `[34]` | `HardwareTxtInpt.Value` | `Ongoing_x0020_Hardware_x0020_Ope` | Text | **Yes** |
| `[35]` | `OngoingLaborTextInput.Value` | `Ongoing_x0020_Labor_x0020_Operat` | Text | **Yes** |
| `[36]` | `OperationalSupportTxtInpt.Value` | `Operational_x0020_Support_x0020_` | Text | **Yes** |
| `[37]` | `AWSTxtInpt.Value` | `Cloud_x0020__x0028_AWS_x0029__x0` | Text | **Yes** |
| `[38]` | `OverviewSupportTxtInpt.Value` | `Provide_x0020_Overview_x0020_of_` | Text | **Yes** |
| `[39]` | `SupportModelTxtInpt.Value` | `Cost_x0020_of_x0020_Support_x002` | Text | **Yes** |
| `[40]` | `ImpactToOrgTxtInpt.Value` | `Costs_x0020_that_x0020_Impact_x0` | Text | **Yes** |
| `[41]` | `ReductionTxtInput.Value` | `Reduction_x002f_Retirements_x002` | Text | **Yes** |
| `[42]` | `SupplyChainCombo.Selected.DisplayName` | `SupplyChainText` | Text | No (person picker) |
| `[43]` | `LicenseTypeTxtInpt.Value` | `Legal_x003a__x0020_License_x0020` | Text | **Yes** |
| `[44]` | `OperationalRiskTxtInpt.Value` | `Operational_x0020_Risk_x0020__x0` | Text | **Yes** |
| `[45]` | `InitialAdoptionTxtInpt.Value` | `Initial_x0020_Adoption_x0020_Pla` | Text | **Yes** |
| `[46]` | `MainStreamTxtInpt.Value` | `Mainstream_x0020_Adoption_x0020_` | Text | **Yes** |
| `[47]` | `RestrictionsTxtInpt.Value` | `Restrictions_x0020__x002f__x0020` | Text | **Yes** |
| `[48]` | `RepoLocationTxtInpt.Value` | `Repository_x0020__x002f__x0020_L` | Text | **Yes** |
| `[49-58]` | (Reserved/Empty) | - | - | - |
| `[59]` | `PIATxtInpt.Value` | `Privacy_x0020_Impact_x0020_Asses` | Text | No |
| `[60]` | `ZycusTxtInpt.Value` | - | Text | No |
| `[61]` | `RiskTxtInpt.Value` | `Security_x0020_Vendor_x0020_Risk` | Text | No |
| `[62]` | `ArchRecTxtInpt.Value` | `Sr_x0020_Portfolio_x0020_Archite` | Text | No |
| `[63]` | `FormType` | `Form_x0020_Submission_x0020_Type` | Choice | No (system) |
| `[64]` | (Update ID) | - | Number | No (system) |
| `[65]` | `DeveloperToolsRadio.Selected.Value` | `ApprovedDeveloperTool` | Choice | **Yes** |
| `[66]` | `RequestTypeRadio.Selected.Value` (Add) | `Type_x0020__x0028_POC_x002c__x00` | Choice | **Yes** |
| `[67]` | `RequestTypeRadio.Selected.Value` (Change) | `Request_x0020_Type_x0020_Change` | Choice | **Yes** |
| `[68]` | `DomainNameCmbBox_1.Selected.Value` | `Domain_x0020_Name` | Choice | No |
| `[69]` | `SaasNotesTxtInpt.Value` | `SaaSNotes` | Text | No |
| `[70]` | `AINotesTxtInpt.Value` | `AINotes` | Text | No |
| `[71]` | `ITManagerCombo.Selected.Mail` | `IT_x0020_Manager` | Person | No |
| `[72]` | `ITPortfolioArchCombo.Selected.Mail` | `IT_x0020_Portfolio_x0020_Archite` | Person | No |
| `[73]` | `SupplyChainCombo.Selected.Mail` | `Supply_x0020_Chain_x0020_Contact0` | Person | No |
| `[74]` | `DataloadTimestamp` | - | DateTime | No (system) |

---

## AI Extractable Fields (34 fields)

These fields can be populated by AI from unstructured text:

### Core Product Info
| JSON Key | Control | Valid Values |
|----------|---------|--------------|
| `productName` | `ProductNameTxtInput` | Any text |
| `description` | `DescriptionTxtInput` | Any text |
| `vendor` | `VendorNameTxtInput` | Any text |
| `vendorState` | `VendorStateComboBox` | `"US"`, `"International"` |
| `productType` | `ProductTypeRadio` | `"Commercial"`, `"Open Source"`, `"Internal Build"` |
| `notes` | `NotesTxtInput` | Any text |

### Technical Classification
| JSON Key | Control | Valid Values |
|----------|---------|--------------|
| `isAI` | `AICombo` | `"Yes"`, `"No"` |
| `awsServices` | `AWSCombo` | Array: `["EC2", "S3", "Lambda", ...]` |
| `isCloud` | `ServiceProvidedRadio` | `"Yes"`, `"No"` |
| `isSaaS` | `SaasIntegrateRadio` | `"Yes"`, `"No"` |
| `criticalityTier` | `CriticalityTierRadio` | `"Tier 1"`, `"Tier 2"`, `"Tier 3"`, `"Tier 4"` |
| `internalBuild` | `InternalBuildComboBox` | `"Yes"`, `"No"` |
| `isDeveloperTool` | `DeveloperToolsRadio` | `"Yes"`, `"No"` |
| `requestType` | `RequestTypeRadio` | `"POC"`, `"Pilot"`, `"Production"` |

### POC/Pilot Info
| JSON Key | Control | Valid Values |
|----------|---------|--------------|
| `pocDuration` | `POCDurationTxtInpt` | e.g., `"90 days"`, `"6 months"` |
| `pocEndDate` | `POCEndDatePicker` | `"YYYY-MM-DD"` |
| `blockCode` | `BlockCodeTxtInput` | e.g., `"IT-ANA"`, `"IT-SEC"` |

### Business Justification
| JSON Key | Control | Valid Values |
|----------|---------|--------------|
| `summary` | `ProductSummaryTxtInpt` | Any text |
| `businessBenefit` | `BusinessBenefitTxtInpt` | Any text |
| `businessCapabilities` | `BusinessCapabilitiesTxtInpt` | Any text |
| `equivalentProducts` | `EquivalentProductsTxtInpt` | Any text |
| `alternativeSolutions` | `AlternativeSolutionsTxtInpt` | Any text |

### Cost Information
| JSON Key | Control | Valid Values |
|----------|---------|--------------|
| `oneTimeCost` | `OneTimeCostTxtInpt` | e.g., `"$50,000"`, `"50000"` |
| `hardwareCost` | `HardwareTxtInpt` | Any text |
| `laborCost` | `OngoingLaborTextInput` | Any text |
| `operationalSupport` | `OperationalSupportTxtInpt` | Any text |
| `awsCost` | `AWSTxtInpt` | Any text |
| `supportOverview` | `OverviewSupportTxtInpt` | Any text |
| `supportModel` | `SupportModelTxtInpt` | Any text |
| `orgImpact` | `ImpactToOrgTxtInpt` | Any text |
| `reductions` | `ReductionTxtInput` | Any text |

### Compliance & Risk
| JSON Key | Control | Valid Values |
|----------|---------|--------------|
| `dataResidency` | `DataResidencyTxtInput` | Any text |
| `licenseType` | `LicenseTypeTxtInpt` | Any text |
| `operationalRisk` | `OperationalRiskTxtInpt` | Any text |
| `restrictions` | `RestrictionsTxtInpt` | Any text |
| `repoLocation` | `RepoLocationTxtInpt` | URL or path |

### Adoption Planning
| JSON Key | Control | Valid Values |
|----------|---------|--------------|
| `initialAdoption` | `InitialAdoptionTxtInpt` | Any text |
| `mainstreamAdoption` | `MainStreamTxtInpt` | Any text |

---

## Implementation

### Step 1: Create Power Automate Flow `STR_AIExtract`

**Trigger:** Power Apps (V2)
- Input: `UnstructuredText` (string)

**AI Builder GPT Prompt:**
```
You are an AI assistant extracting Software Technology Request (STR) data for Delta Airlines.
Extract information from the input text and return ONLY valid JSON.

## OUTPUT SCHEMA:
{
  "productName": "string or null",
  "description": "string or null",
  "vendor": "string or null",
  "vendorState": "US" or "International" or null,
  "productType": "Commercial" or "Open Source" or "Internal Build" or null,
  "notes": "string or null",
  "isAI": "Yes" or "No" or null,
  "awsServices": ["array of AWS service names"] or null,
  "isCloud": "Yes" or "No" or null,
  "isSaaS": "Yes" or "No" or null,
  "criticalityTier": "Tier 1" or "Tier 2" or "Tier 3" or "Tier 4" or null,
  "internalBuild": "Yes" or "No" or null,
  "isDeveloperTool": "Yes" or "No" or null,
  "requestType": "POC" or "Pilot" or "Production" or null,
  "pocDuration": "string or null",
  "pocEndDate": "YYYY-MM-DD or null",
  "blockCode": "string or null",
  "summary": "string or null",
  "businessBenefit": "string or null",
  "businessCapabilities": "string or null",
  "equivalentProducts": "string or null",
  "alternativeSolutions": "string or null",
  "oneTimeCost": "string or null",
  "hardwareCost": "string or null",
  "laborCost": "string or null",
  "operationalSupport": "string or null",
  "awsCost": "string or null",
  "supportOverview": "string or null",
  "supportModel": "string or null",
  "orgImpact": "string or null",
  "reductions": "string or null",
  "dataResidency": "string or null",
  "licenseType": "string or null",
  "operationalRisk": "string or null",
  "restrictions": "string or null",
  "repoLocation": "string or null",
  "initialAdoption": "string or null",
  "mainstreamAdoption": "string or null",
  "confidence": 0.0
}

## RULES:
1. Return ONLY JSON - no markdown code fences, no explanation
2. Use null for any field not mentioned in the input
3. Never invent data - only extract what is explicitly stated
4. For vendorState: "US" if US-based company, "International" otherwise
5. For criticalityTier: Tier 1 = critical/high, Tier 4 = low priority
6. For awsServices: extract specific AWS services mentioned (EC2, S3, Lambda, RDS, etc.)
7. Set confidence between 0.0 and 1.0 based on extraction quality
8. Normalize costs to numbers where possible (remove $ and commas)

## INPUT TEXT:
@{triggerBody()['text']}

## JSON:
```

**Response Action:**
```json
{
  "body": {
    "result": "@{outputs('Create_text_with_GPT')?['body/text']}"
  }
}
```

---

### Step 2: Add Popup Controls to STRFormScreen

Add after the existing `bttnContainer`:

```yaml
# AI Assist Button (add to bttnContainer)
- AIAssistBttn:
    Control: Button@0.0.45
    Properties:
      Text: ="AI Assist"
      BorderColor: =RGBA(106, 90, 205, 1)
      FontColor: =RGBA(106, 90, 205, 1)
      Height: =23
      Width: =100
      OnSelect: |
        =UpdateContext({
            showAIPopup: true,
            showAIPreview: false,
            isAIExtracting: false
        });
        Reset(AIPromptInput);

# Popup Overlay Container
- AIPopupOverlay:
    Control: GroupContainer@1.3.0
    Variant: ManualLayout
    Properties:
      Visible: =showAIPopup
      Fill: =RGBA(0, 0, 0, 0.5)
      Height: =Parent.Height
      Width: =Parent.Width
      X: =0
      Y: =0
    Children:
      - AIPopupCard:
          Control: GroupContainer@1.3.0
          Variant: AutoLayout
          Properties:
            Fill: =RGBA(255, 255, 255, 1)
            Height: =550
            Width: =700
            X: =(Parent.Width - Self.Width) / 2
            Y: =(Parent.Height - Self.Height) / 2
            RadiusBottomLeft: =8
            RadiusBottomRight: =8
            RadiusTopLeft: =8
            RadiusTopRight: =8
            DropShadow: =DropShadow.Bold
            LayoutDirection: =LayoutDirection.Vertical
            PaddingTop: =20
            PaddingBottom: =20
            PaddingLeft: =20
            PaddingRight: =20
            LayoutGap: =15
```

---

### Step 3: Popup Content

```yaml
# Header
- AIPopupHeader:
    Control: Label
    Properties:
      Text: ="AI-Assisted STR Form Fill"
      FontSize: =18
      FontWeight: =FontWeight.Bold
      Height: =30

# Input Section
- AIPromptInput:
    Control: Text@0.0.50
    Properties:
      Mode: =TextMode.MultiLine
      HintText: ="Paste product description, email, vendor documentation, or requirements..."
      Height: =120
      Width: =Parent.Width - 40

# Extract Button
- AIExtractBtn:
    Control: Button@0.0.45
    Properties:
      Text: =If(isAIExtracting, "Extracting...", "Extract with AI")
      DisplayMode: =If(isAIExtracting || IsBlank(AIPromptInput.Value), DisplayMode.Disabled, DisplayMode.Edit)
      OnSelect: |
        =UpdateContext({isAIExtracting: true});

        Set(gblAIResponse, STR_AIExtract.Run(AIPromptInput.Value));

        If(
            !IsBlank(gblAIResponse.result),
            Set(gblAIData, ParseJSON(gblAIResponse.result));

            // Build preview collection
            ClearCollect(
                colAIPreview,
                {Field: "Product Name", Value: Text(gblAIData.productName), Control: "ProductNameTxtInput", Required: true, IsValid: !IsBlank(Text(gblAIData.productName))},
                {Field: "Description", Value: Text(gblAIData.description), Control: "DescriptionTxtInput", Required: true, IsValid: !IsBlank(Text(gblAIData.description))},
                {Field: "Vendor", Value: Text(gblAIData.vendor), Control: "VendorNameTxtInput", Required: false, IsValid: true},
                {Field: "Vendor State", Value: Text(gblAIData.vendorState), Control: "VendorStateComboBox", Required: false, IsValid: Text(gblAIData.vendorState) in ["US", "International", ""]},
                {Field: "Product Type", Value: Text(gblAIData.productType), Control: "ProductTypeRadio", Required: true, IsValid: Text(gblAIData.productType) in ["Commercial", "Open Source", "Internal Build"]},
                {Field: "AI/GenAI", Value: Text(gblAIData.isAI), Control: "AICombo", Required: true, IsValid: Text(gblAIData.isAI) in ["Yes", "No"]},
                {Field: "Cloud-Based", Value: Text(gblAIData.isCloud), Control: "ServiceProvidedRadio", Required: false, IsValid: Text(gblAIData.isCloud) in ["Yes", "No", ""]},
                {Field: "SaaS Integration", Value: Text(gblAIData.isSaaS), Control: "SaasIntegrateRadio", Required: false, IsValid: Text(gblAIData.isSaaS) in ["Yes", "No", ""]},
                {Field: "Criticality Tier", Value: Text(gblAIData.criticalityTier), Control: "CriticalityTierRadio", Required: true, IsValid: Text(gblAIData.criticalityTier) in ["Tier 1", "Tier 2", "Tier 3", "Tier 4"]},
                {Field: "Block Code", Value: Text(gblAIData.blockCode), Control: "BlockCodeTxtInput", Required: false, IsValid: true},
                {Field: "Summary", Value: Text(gblAIData.summary), Control: "ProductSummaryTxtInpt", Required: false, IsValid: true},
                {Field: "Business Benefit", Value: Text(gblAIData.businessBenefit), Control: "BusinessBenefitTxtInpt", Required: false, IsValid: true},
                {Field: "One-Time Cost", Value: Text(gblAIData.oneTimeCost), Control: "OneTimeCostTxtInpt", Required: false, IsValid: true},
                {Field: "Request Type", Value: Text(gblAIData.requestType), Control: "RequestTypeRadio", Required: false, IsValid: Text(gblAIData.requestType) in ["POC", "Pilot", "Production", ""]}
            );

            UpdateContext({showAIPreview: true});
            Set(gblAIConfidence, Value(gblAIData.confidence));
        );

        UpdateContext({isAIExtracting: false});

# Preview Gallery
- AIPreviewGallery:
    Control: Gallery
    Variant: galleryVertical
    Properties:
      Visible: =showAIPreview
      Items: =colAIPreview
      Height: =250
      Width: =Parent.Width - 40
      TemplateSize: =35
      TemplatePadding: =2
    Children:
      - lblFieldName:
          Control: Label
          Properties:
            Text: =ThisItem.Field
            Width: =150
            FontWeight: =FontWeight.Semibold
      - lblFieldValue:
          Control: Label
          Properties:
            Text: =Coalesce(ThisItem.Value, "(not extracted)")
            Width: =350
            FontColor: =If(IsBlank(ThisItem.Value), RGBA(150,150,150,1), RGBA(0,0,0,1))
      - icnFieldStatus:
          Control: Classic/Icon@2.5.0
          Properties:
            Icon: =If(ThisItem.IsValid, Icon.CheckMark, If(ThisItem.Required, Icon.Warning, Icon.Information))
            Color: =If(ThisItem.IsValid, RGBA(45,128,40,1), If(ThisItem.Required, RGBA(200,0,0,1), RGBA(255,165,0,1)))
            Width: =30
            Height: =30

# Confidence Label
- AIConfidenceLabel:
    Control: Label
    Properties:
      Visible: =showAIPreview
      Text: ="Confidence: " & Text(gblAIConfidence * 100, "0") & "%"
      FontColor: =If(gblAIConfidence >= 0.7, RGBA(45,128,40,1), If(gblAIConfidence >= 0.4, RGBA(255,165,0,1), RGBA(200,0,0,1)))

# Button Row
- AIButtonRow:
    Control: GroupContainer@1.3.0
    Variant: AutoLayout
    Properties:
      LayoutDirection: =LayoutDirection.Horizontal
      LayoutGap: =10
      Height: =40
    Children:
      - AIRepromptBtn:
          Control: Button@0.0.45
          Properties:
            Text: ="Re-prompt"
            Visible: =showAIPreview
            OnSelect: =UpdateContext({showAIPreview: false})

      - AICancelBtn:
          Control: Button@0.0.45
          Properties:
            Text: ="Cancel"
            OnSelect: |
              =UpdateContext({showAIPopup: false, showAIPreview: false});
              Clear(colAIPreview);

      - AIApproveBtn:
          Control: Button@0.0.45
          Properties:
            Text: ="Approve & Fill Form"
            Visible: =showAIPreview
            DisplayMode: =If(CountRows(Filter(colAIPreview, Required && !IsValid)) = 0, DisplayMode.Edit, DisplayMode.Disabled)
            OnSelect: |
              =// Populate form controls with AI data
              UpdateContext({
                  ctxProductName: Text(gblAIData.productName),
                  ctxDescription: Text(gblAIData.description),
                  ctxVendor: Text(gblAIData.vendor),
                  ctxVendorState: Text(gblAIData.vendorState),
                  ctxProductType: Text(gblAIData.productType),
                  ctxNotes: Text(gblAIData.notes),
                  ctxIsAI: Text(gblAIData.isAI),
                  ctxIsCloud: Text(gblAIData.isCloud),
                  ctxIsSaaS: Text(gblAIData.isSaaS),
                  ctxCriticalityTier: Text(gblAIData.criticalityTier),
                  ctxInternalBuild: Text(gblAIData.internalBuild),
                  ctxBlockCode: Text(gblAIData.blockCode),
                  ctxSummary: Text(gblAIData.summary),
                  ctxBusinessBenefit: Text(gblAIData.businessBenefit),
                  ctxBusinessCapabilities: Text(gblAIData.businessCapabilities),
                  ctxOneTimeCost: Text(gblAIData.oneTimeCost),
                  ctxRequestType: Text(gblAIData.requestType),
                  ctxPocDuration: Text(gblAIData.pocDuration),
                  ctxDataResidency: Text(gblAIData.dataResidency),
                  ctxEquivalentProducts: Text(gblAIData.equivalentProducts),
                  ctxAlternativeSolutions: Text(gblAIData.alternativeSolutions),
                  ctxLicenseType: Text(gblAIData.licenseType),
                  ctxOperationalRisk: Text(gblAIData.operationalRisk)
              });

              UpdateContext({showAIPopup: false, showAIPreview: false});
              Notify("Form populated with AI data. Please review all fields before submitting.", NotificationType.Success);
```

---

### Step 4: Update Form Control Default Properties

Modify each control to use the AI-populated context variables:

```powerapps
// ProductNameTxtInput.Default
Coalesce(ctxProductName, "")

// DescriptionTxtInput.Default
Coalesce(ctxDescription, "")

// VendorNameTxtInput.Default
Coalesce(ctxVendor, "")

// NotesTxtInput.Default
Coalesce(ctxNotes, "")

// BlockCodeTxtInput.Default
Coalesce(ctxBlockCode, "")

// ProductSummaryTxtInpt.Default
Coalesce(ctxSummary, "")

// BusinessBenefitTxtInpt.Default
Coalesce(ctxBusinessBenefit, "")

// BusinessCapabilitiesTxtInpt.Default
Coalesce(ctxBusinessCapabilities, "")

// OneTimeCostTxtInpt.Default
Coalesce(ctxOneTimeCost, "")

// POCDurationTxtInpt.Default
Coalesce(ctxPocDuration, "")

// DataResidencyTxtInput.Default
Coalesce(ctxDataResidency, "")

// EquivalentProductsTxtInpt.Default
Coalesce(ctxEquivalentProducts, "")

// AlternativeSolutionsTxtInpt.Default
Coalesce(ctxAlternativeSolutions, "")

// LicenseTypeTxtInpt.Default
Coalesce(ctxLicenseType, "")

// OperationalRiskTxtInpt.Default
Coalesce(ctxOperationalRisk, "")
```

**For ComboBox/Radio controls:**

```powerapps
// VendorStateComboBox.DefaultSelectedItems
If(!IsBlank(ctxVendorState), Filter(VendorStateComboBox.Items, Value = ctxVendorState))

// ProductTypeRadio.Default
Coalesce(ctxProductType, "")

// CriticalityTierRadio.Default
Coalesce(ctxCriticalityTier, "")

// ServiceProvidedRadio.Default (Cloud-Based)
Coalesce(ctxIsCloud, "")

// SaasIntegrateRadio.Default
Coalesce(ctxIsSaaS, "")

// InternalBuildComboBox.DefaultSelectedItems
If(!IsBlank(ctxInternalBuild), Filter(InternalBuildComboBox.Items, Value = ctxInternalBuild))

// RequestTypeRadio.Default
Coalesce(ctxRequestType, "")
```

---

### Step 5: Initialize Context on STRFormScreen.OnVisible

```powerapps
=Set(currentTabB, {Value: "Base Information"});

// Initialize AI context variables
UpdateContext({
    showAIPopup: false,
    showAIPreview: false,
    isAIExtracting: false,
    ctxProductName: Blank(),
    ctxDescription: Blank(),
    ctxVendor: Blank(),
    ctxVendorState: Blank(),
    ctxProductType: Blank(),
    ctxNotes: Blank(),
    ctxIsAI: Blank(),
    ctxIsCloud: Blank(),
    ctxIsSaaS: Blank(),
    ctxCriticalityTier: Blank(),
    ctxInternalBuild: Blank(),
    ctxBlockCode: Blank(),
    ctxSummary: Blank(),
    ctxBusinessBenefit: Blank(),
    ctxBusinessCapabilities: Blank(),
    ctxOneTimeCost: Blank(),
    ctxRequestType: Blank(),
    ctxPocDuration: Blank(),
    ctxDataResidency: Blank(),
    ctxEquivalentProducts: Blank(),
    ctxAlternativeSolutions: Blank(),
    ctxLicenseType: Blank(),
    ctxOperationalRisk: Blank()
});
```

---

### Step 6: Update ClearReqBttn.OnSelect

Add to the existing Reset statements:

```powerapps
// Add these lines to existing ClearReqBttn.OnSelect
Reset(AIPromptInput);
UpdateContext({
    showAIPopup: false,
    showAIPreview: false,
    ctxProductName: Blank(),
    ctxDescription: Blank(),
    ctxVendor: Blank(),
    ctxVendorState: Blank(),
    ctxProductType: Blank(),
    ctxNotes: Blank(),
    ctxIsAI: Blank(),
    ctxIsCloud: Blank(),
    ctxIsSaaS: Blank(),
    ctxCriticalityTier: Blank(),
    ctxInternalBuild: Blank(),
    ctxBlockCode: Blank(),
    ctxSummary: Blank(),
    ctxBusinessBenefit: Blank(),
    ctxBusinessCapabilities: Blank(),
    ctxOneTimeCost: Blank(),
    ctxRequestType: Blank(),
    ctxPocDuration: Blank(),
    ctxDataResidency: Blank(),
    ctxEquivalentProducts: Blank(),
    ctxAlternativeSolutions: Blank(),
    ctxLicenseType: Blank(),
    ctxOperationalRisk: Blank()
});
Clear(colAIPreview);
```

---

## Test Input Example

```
We're evaluating Databricks for our data engineering needs. Databricks Inc is
based in San Francisco (US company). It's a commercial SaaS product running
on AWS (uses EC2, S3, and EMR). This is for the Analytics team, block code
IT-ANA. We need it for a 90-day POC ending March 31, 2025.

The product provides unified analytics platform for data engineering and ML.
Main benefit is consolidating our Spark workloads and reducing operational
overhead by 40%. Current alternatives include running our own Spark clusters
on EMR, but that requires significant DevOps effort.

Estimated one-time cost: $25,000 for implementation
Ongoing cost: $15,000/month for compute

This is a Tier 2 critical system. No AI/GenAI features will be used initially.
The software is cloud-only, no on-prem option. License type is subscription-based.
```

**Expected AI Output:**
```json
{
  "productName": "Databricks",
  "description": "Unified analytics platform for data engineering and ML",
  "vendor": "Databricks Inc",
  "vendorState": "US",
  "productType": "Commercial",
  "notes": null,
  "isAI": "No",
  "awsServices": ["EC2", "S3", "EMR"],
  "isCloud": "Yes",
  "isSaaS": "Yes",
  "criticalityTier": "Tier 2",
  "internalBuild": "No",
  "isDeveloperTool": "No",
  "requestType": "POC",
  "pocDuration": "90 days",
  "pocEndDate": "2025-03-31",
  "blockCode": "IT-ANA",
  "summary": "Unified analytics platform for data engineering and ML workloads",
  "businessBenefit": "Consolidating Spark workloads and reducing operational overhead by 40%",
  "businessCapabilities": "Data engineering, ML, unified analytics",
  "equivalentProducts": null,
  "alternativeSolutions": "Running own Spark clusters on EMR, but requires significant DevOps effort",
  "oneTimeCost": "25000",
  "hardwareCost": null,
  "laborCost": null,
  "operationalSupport": null,
  "awsCost": "15000/month",
  "supportOverview": null,
  "supportModel": null,
  "orgImpact": null,
  "reductions": "40% reduction in operational overhead",
  "dataResidency": null,
  "licenseType": "Subscription-based",
  "operationalRisk": null,
  "restrictions": null,
  "repoLocation": null,
  "initialAdoption": null,
  "mainstreamAdoption": null,
  "confidence": 0.87
}
```
