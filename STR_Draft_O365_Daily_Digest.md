# Software Technology Request (STR) Draft
## O365 Daily Digest - Communications Mining Software

---

### REQUESTOR INFORMATION

| Field | Value |
|-------|-------|
| **Product Name** | O365 Daily Digest |
| **Requestor Name (From IT)** | [Enter Your Name] |
| **Date Requested** | [Current Date] |
| **Domain Name** | IT |
| **Business Unit** | IT / Enterprise Technology |
| **Restricted to Domain/Business Unit** | No |

---

### VENDOR INFORMATION

| Field | Value |
|-------|-------|
| **Vendor Name** | Microsoft |
| **Vendor Status** | Existing |
| **Block Code (if applicable)** | N/A |

---

### IT LEADERSHIP

| Field | Value |
|-------|-------|
| **IT Manager** | [Enter IT Manager Name] |
| **IT Portfolio Architect** | [Enter IT Portfolio Architect Name] |

---

### PRODUCT DETAILS

| Field | Value |
|-------|-------|
| **Product Type** | Internal Development |
| **Is Product Funded?** | Yes |
| **Request Type** | Permanent Production |
| **Criticality Tier** | Tier 3 (Low) |

#### Description
O365 Daily Digest is a Power Platform automation solution that mines and summarizes daily communications from Microsoft Outlook emails and Microsoft Teams chats. The solution uses AI Builder with GPT models to analyze and consolidate communications into a single, executive-ready daily digest email. Version 1.2.0.7 includes enhanced error handling for external meeting chats.

**Key Features:**
- Automated daily collection of emails from Outlook inbox (last 24 hours)
- Automated collection of Teams chat messages (last 24 hours)
- AI-powered summarization using Microsoft AI Builder custom prompts
- Consolidated daily digest email delivery
- Configurable schedule (default: daily at 5 PM UTC)
- Environment variables for enabling/disabling Outlook and Teams sources
- Comprehensive error handling with failure notification emails

---

### AI/GENAI TECHNOLOGY

| Field | Value |
|-------|-------|
| **AI/GenAI Technology** | Yes - AI Builder (GPT-4.1 Mini, Reasoning Models) |
| **Confirm Compliance with AI Mandates** | [To Be Confirmed] |

#### AI Components Used:
1. **SummarizeO365Content** - Combines and summarizes email and Teams reports into a unified daily summary
2. **SummarizeTeamsMessages** - Analyzes and summarizes Teams chat messages with structured output
3. **SummarizeEmails** - Processes and summarizes Outlook email content

**AI Model Details:**
- Model Type: GPT-4.1 Mini (for content summarization), Reasoning model (for email analysis)
- Temperature: 0 (deterministic outputs)
- Use Case: Enterprise communications summarization for leadership situational awareness

---

### CLOUD & HOSTING

| Field | Value |
|-------|-------|
| **Cloud Based Solution** | Yes |
| **Where will this be hosted?** | Microsoft Power Platform (Dataverse) |
| **SaaS Product Integrates with Delta's Global Auth/MFA?** | Yes (via Microsoft 365 SSO) |
| **Confirm Compliance with SaaS Mandates** | [To Be Confirmed] |
| **AWS Services** | None |

---

### CONNECTIONS & INTEGRATIONS

The solution uses the following Microsoft 365 connectors:

| Connector | Purpose |
|-----------|---------|
| Office365 Users | Retrieve user profile information |
| Office365 (Outlook) | Read emails, send digest emails |
| Microsoft Teams | Access Teams chat messages via Graph API |
| Common Data Service | AI Builder custom prompt execution |

**Connection References:**
- cr2de_O365Connector
- cr2de_OutlookConnector
- cr2de_TeamsConnector
- mccia_Office365SEDB

---

### DEVELOPER TOOLS / LIBRARIES

| Field | Value |
|-------|-------|
| **Developer Tools** | Power Automate (Cloud Flows), AI Builder, Microsoft Graph API |
| **Software Executables** | N/A (Cloud-based solution package) |
| **URL for Free/Open-Source** | N/A |

---

### BUSINESS JUSTIFICATION

#### Summary of Why New Product is Needed
Enterprise leaders and team members need a fast, consolidated view of daily communications across multiple channels (email and Teams). Currently, reviewing hundreds of emails and chat messages daily is time-consuming and leads to missed important updates. This automation provides situational awareness by mining and summarizing communications into an executive-ready format.

#### Business Benefit (ROI)
- **Time Savings**: Reduces 30-60 minutes of daily communication review to a 2-minute digest scan
- **Improved Awareness**: Ensures leaders don't miss critical updates, decisions, or action items
- **Productivity**: Enables faster decision-making by highlighting priorities and blockers
- **Standardization**: Provides consistent daily summaries with structured sections for actions, technical notes, and announcements

#### Specific Business Capabilities
1. **Overview of the Day** - High-level summary of communication themes
2. **Major Actions and Decisions** - Key outcomes requiring follow-up
3. **System or Technical Notes** - Operational issues, automation updates, incidents
4. **Collaboration and Communications** - Meeting notes, team coordination highlights
5. **Awareness and Announcements** - HR communications, events, reminders
6. **Stand-Up for Tomorrow Morning** - Forward-looking priorities and blockers

---

### DATA & PRIVACY

| Field | Value |
|-------|-------|
| **Data Residency** | Microsoft 365 Cloud (Data processed within M365 tenant) |
| **Where will data be stored and processed?** | Microsoft Dataverse, Microsoft 365 Exchange/Teams |
| **Privacy Impact Assessment (PIA) Number** | [To Be Completed] |

**Data Handling Notes:**
- Solution accesses user's own mailbox and Teams chats only
- No data is stored outside of Microsoft 365 environment
- AI processing occurs within Microsoft AI Builder (Azure-based)
- Email digest is sent only to the user's own email address

---

### ALTERNATIVE SOLUTIONS

#### Equivalent Products/Solutions
| Product | Comparison |
|---------|------------|
| Microsoft Copilot | Provides similar summarization but requires additional licensing and is not customizable for specific output formats |
| Manual Review | Time-consuming, inconsistent, prone to missing important items |
| Third-party email digest tools | Security concerns with external data access, additional cost |

#### Alternative if Request is Denied
Continue manual review of emails and Teams messages, resulting in increased time spent on communication review and potential for missed critical updates.

---

### COST ANALYSIS

#### One-Time Implementation Costs
| Item | Cost |
|------|------|
| Development (Internal) | Absorbed in existing headcount |
| Testing & Validation | Absorbed in existing headcount |
| **Total** | $0 (Internal development) |

#### Ongoing Operational Expense

| Category | Monthly Cost | Notes |
|----------|--------------|-------|
| Hardware | $0 | Cloud-based |
| Labor (Care and Feeding) | Minimal | Occasional maintenance |
| Operational Support | Minimal | Self-service for end users |
| Cloud (AWS) | $0 | Uses Power Platform |
| AI Builder | Included | Within existing Power Platform licensing |
| **Total** | Minimal | Covered by existing M365/Power Platform licenses |

---

### SUPPORT & OWNERSHIP

#### Support Model Overview
- **Primary Support**: Internal IT team (Intelligent Automation)
- **Secondary Support**: Microsoft Premier Support (for platform issues)
- **Self-Service**: Users can enable/disable via environment variables

#### Cost of Ownership

| Category | Description |
|----------|-------------|
| Support Model | Internal L1/L2 support, Microsoft L3 |
| Impact to Organization | Minimal - leverages existing Power Platform skills |
| Reduction/Retirement Opportunities | Potential to retire manual email review processes |

---

### RISK & COMPLIANCE

| Field | Value |
|-------|-------|
| **License Type** | Microsoft Power Platform (existing enterprise agreement) |
| **Operational Risk** | Low - Solution runs on a schedule with error handling |
| **Mediation Plan** | Automated error notifications; fallback to manual review if needed |
| **Security Vendor Risk Assessment** | N/A (Microsoft - existing vendor) |

---

### ADOPTION PLAN

#### Initial Adoption Plan (Rollout)
1. Deploy solution package to target Power Platform environment
2. Configure connection references with appropriate service accounts
3. Set environment variables (schedule time, enable Outlook/Teams)
4. Pilot with IT leadership team (2-4 weeks)
5. Gather feedback and iterate on AI prompts if needed

#### Mainstream Adoption Plan
1. Publish solution to broader IT organization
2. Provide documentation for self-service configuration
3. Monitor usage and performance metrics
4. Expand to additional business units upon request

#### Restrictions / Constraints
- Users must have appropriate Microsoft 365 licenses
- Power Platform environment access required
- AI Builder capacity must be available in tenant
- Teams connector requires appropriate Graph API permissions

---

### REPOSITORY & STORAGE

| Field | Value |
|-------|-------|
| **Repository/Location** | Power Platform Solution Package (O365_1_2_0_7.zip) |
| **Version** | 1.2.0.7 |
| **Package Contents** | Cloud flow, AI Builder models, environment variable definitions |

---

### ATTACHMENTS CHECKLIST

- [ ] Architecture Diagram
- [ ] Privacy Impact Assessment (PIA)
- [ ] Security Vendor Risk Assessment (if applicable)
- [ ] Business Case Justification

---

### NOTES

- **Version History**: v1.2.0.2 introduced enhanced error handling for external meeting chats
- **Workflow Name**: GetEmailsOneNoteSched
- **AI Models**: SummarizeO365Content, SummarizeTeamsMessages, SummarizeEmails
- **STR is required because AI is utilized in the solution**

---

### FORM SUBMISSION TYPE
- [x] Final Copy

---

*This STR draft was generated based on the O365_1_2_0_7 solution package analysis. Please review and complete all fields marked with [brackets] before submission.*
