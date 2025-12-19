# Enterprise Rollout Plan: AI Daily Brief

## Table of Contents
1. [Deployment Model](#deployment-model)
2. [AI Credits & Cost Modeling](#ai-credits--cost-modeling)
3. [DLP & Security Policies](#dlp--security-policies)
4. [Permissions & Access](#permissions--access)
5. [COE Questions Checklist](#coe-questions-checklist)
6. [End-User Configuration Options](#end-user-configuration-options)
7. [Monitoring & Analytics](#monitoring--analytics)
8. [Abuse Prevention & Guardrails](#abuse-prevention--guardrails)
9. [Rollout Phases](#rollout-phases)

---

## Deployment Model

### Option A: Personal Productivity Environment (Recommended)
Users install flow in their own environment using a managed solution.

| Pros | Cons |
|------|------|
| User owns their data/flow | Harder to update centrally |
| No shared resource contention | Each user consumes own AI credits |
| Easier DLP compliance | Visibility into usage is limited |
| Natural access boundaries | Support burden distributed |

### Option B: Shared Environment with Per-User Connections
Central team deploys, users authenticate with own credentials.

| Pros | Cons |
|------|------|
| Centralized updates | Connection management complexity |
| Easier monitoring | Shared environment capacity limits |
| Single version control | DLP scope broader |

### Recommendation
**Option A** - Personal environment deployment with managed solution package. Provides cleanest security boundary since users only access their own data.

---

## AI Credits & Cost Modeling

### AI Builder Credit Consumption

| Component | Model | Est. Credits/Run | Notes |
|-----------|-------|------------------|-------|
| SummarizeEmails | GPT-4.1 Mini | ~5-15 credits | Varies by email volume |
| SummarizeTeams | Reasoning Model | ~10-25 credits | Higher due to reasoning model |
| SummarizeO365Content | GPT-4.1 Mini | ~5-10 credits | Final consolidation |
| **Total per user/day** | | **~20-50 credits** | Conservative estimate |

### Monthly Cost Estimates

| Users | Daily Runs | Credits/Month | Est. Cost/Month* |
|-------|------------|---------------|------------------|
| 10 | 10 | 6,000-15,000 | $60-150 |
| 50 | 50 | 30,000-75,000 | $300-750 |
| 100 | 100 | 60,000-150,000 | $600-1,500 |
| 500 | 500 | 300,000-750,000 | $3,000-7,500 |
| 1,000 | 1,000 | 600,000-1,500,000 | $6,000-15,000 |

*Based on ~$10 per 1,000 AI Builder credits. Verify current pricing with Microsoft.

### Credit Allocation Options

1. **Tenant Pool**: All users draw from tenant-wide AI Builder capacity
2. **Per-User Allocation**: Assign credit limits per user (requires Power Platform admin controls)
3. **Department Chargeback**: Track usage by cost center, bill internally

### Questions for Licensing Team
- [ ] Current AI Builder credit allocation in tenant?
- [ ] Available capacity vs. current consumption?
- [ ] Can we purchase additional capacity packs?
- [ ] Is per-user credit limiting available in our tenant?

---

## DLP & Security Policies

### Data Flow Analysis

```
User's Mailbox (Exchange) ──► Power Automate ──► AI Builder ──► User's Email
User's Teams Chats ─────────►               ──►            ──►
```

**Key Point**: Data never leaves Microsoft tenant. AI Builder processes within compliance boundary.

### DLP Policy Requirements

| Policy | Requirement | Action |
|--------|-------------|--------|
| Connector Grouping | Office 365, Teams, AI Builder must be in same group | Verify/update DLP policy |
| Business Data Only | Ensure connectors classified as "Business" | Check connector classification |
| No External Sharing | Block connectors that send data externally | Already compliant (no external connectors) |

### Required DLP Exceptions/Configurations
```
Connectors Required (must be in same DLP group):
├── Office 365 Users
├── Office 365 Outlook
├── Microsoft Teams
└── AI Builder
```

### Security Checklist
- [ ] Verify all connectors in "Business" data group
- [ ] Confirm AI Builder tenant isolation settings
- [ ] Review data residency requirements (AI processing location)
- [ ] Validate no cross-tenant data flow
- [ ] Check audit logging enabled for Power Automate

---

## Permissions & Access

### Required Permissions (Per User)

| Permission | Scope | Purpose |
|------------|-------|---------|
| Mail.Read | User's mailbox only | Read emails for summarization |
| Chat.Read | User's chats only | Read Teams messages |
| User.Read | Own profile | Get user details |
| AI Builder | Tenant | Access AI models |

### Admin Permissions Required (For Deployment)

| Permission | Who | Purpose |
|------------|-----|---------|
| Environment Maker | Users | Create flows in personal env |
| AI Builder Access | Users | Consume AI credits |
| Solution Import | Users or Admin | Install managed solution |
| DLP Policy Admin | COE/IT Admin | Configure connector policies |

### Service Principal (If Centralized)
Not recommended for this solution - delegated user permissions preferred.

---

## COE Questions Checklist

### Governance & Compliance
- [ ] Is this solution pattern approved for personal productivity use?
- [ ] What's the process for adding AI Builder workloads?
- [ ] Are there existing AI usage policies we need to follow?
- [ ] What data classification does this fall under?
- [ ] Do we need a DPIA (Data Protection Impact Assessment)?

### Technical
- [ ] Which environments can users deploy to? (Personal/Sandbox/Prod)
- [ ] Are the required connectors enabled in user environments?
- [ ] What's the current DLP policy for these connectors?
- [ ] Is AI Builder enabled tenant-wide or restricted?
- [ ] Are there flow run limits per user?

### Capacity & Funding
- [ ] Who owns AI Builder credit budget?
- [ ] Is there a chargeback model for AI consumption?
- [ ] What's the approval process for capacity increases?
- [ ] Can we get a trial/pilot allocation before full rollout?

### Support
- [ ] Who provides L1 support for user-deployed solutions?
- [ ] What's the escalation path for AI Builder issues?
- [ ] Is there a knowledge base or support channel we should publish to?
- [ ] How do we handle version updates to the solution?

### Monitoring
- [ ] What tenant-level analytics are available?
- [ ] Can we access AI Builder consumption reports?
- [ ] Are there existing dashboards we should integrate with?
- [ ] What alerting exists for unusual usage patterns?

---

## End-User Configuration Options

### Option 1: Self-Contained Flow Variables (Simplest)
Configuration stored within the flow using environment variables.

**Implementation:**
```
Environment Variables (User Sets Once):
├── IncludeOutlook (Boolean) - Toggle email mining
├── IncludeTeams (Boolean) - Toggle Teams mining
└── ScheduleTime (String) - Preferred delivery time
```

**Pros**: No additional app needed, config travels with flow
**Cons**: Users must edit flow to change settings

---

### Option 2: Configuration Power App (Recommended)

Build a simple Canvas App for user self-service configuration.

**App Features:**
- Toggle Outlook on/off
- Toggle Teams on/off
- Set preferred delivery time
- Test run / preview digest
- View run history
- Pause/resume automation

**Architecture:**
```
┌─────────────────────┐     ┌─────────────────────┐
│  Config Power App   │────►│  Dataverse Table    │
│  (User Interface)   │     │  (User Preferences) │
└─────────────────────┘     └──────────┬──────────┘
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │  Daily Digest Flow  │
                            │  (Reads Config)     │
                            └─────────────────────┘
```

**Dataverse Table: UserDigestConfig**
| Column | Type | Description |
|--------|------|-------------|
| UserId | Lookup (User) | Primary key |
| IncludeOutlook | Boolean | Email mining toggle |
| IncludeTeams | Boolean | Teams mining toggle |
| ScheduleTimeUTC | DateTime | Preferred run time |
| IsActive | Boolean | Enable/disable digest |
| CreatedOn | DateTime | Enrollment date |
| LastRunDate | DateTime | Tracking |

**Pros**: Professional UX, centralized config, easy to extend
**Cons**: Additional app to build and maintain, Dataverse storage

---

### Option 3: Adaptive Card Configuration (Middle Ground)

Send a weekly config card via Teams allowing inline adjustments.

**Pros**: No separate app, meets users where they are
**Cons**: Limited options, Teams dependency

---

### Recommendation
**Start with Option 1** for pilot, **build Option 2** for scale. The Power App provides:
- Better user experience
- Usage analytics (who's enrolled, active, etc.)
- Easy rollout of new features
- Self-service without flow editing

---

## Monitoring & Analytics

### Metrics to Track

| Metric | Source | Purpose |
|--------|--------|---------|
| Daily Active Users | Flow run history | Adoption tracking |
| AI Credit Consumption | AI Builder analytics | Cost management |
| Success/Failure Rate | Flow analytics | Reliability |
| Avg Processing Time | Flow run details | Performance |
| Error Types | Flow error logs | Support prioritization |

### Monitoring Architecture

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  User Flows      │────►│  Power Platform  │────►│  Admin Dashboard │
│  (Distributed)   │     │  Admin Center    │     │  (Power BI)      │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                │
                                ▼
                         ┌──────────────────┐
                         │  CoE Starter Kit │
                         │  (If Deployed)   │
                         └──────────────────┘
```

### Recommended Dashboards

1. **Adoption Dashboard**
   - Total enrolled users
   - Daily/weekly active users
   - Enrollment trend over time
   - Department breakdown

2. **Cost Dashboard**
   - AI credits consumed (daily/weekly/monthly)
   - Cost per user average
   - Projected vs actual spend
   - Top consumers

3. **Health Dashboard**
   - Success rate %
   - Error breakdown by type
   - Avg run duration
   - Failed runs requiring attention

### Implementation Options

| Option | Complexity | Features |
|--------|------------|----------|
| Power Platform Admin Center | Low | Basic run analytics |
| CoE Starter Kit | Medium | Comprehensive governance |
| Custom Power BI Dashboard | Medium | Tailored metrics |
| Azure Application Insights | High | Deep telemetry |

---

## Abuse Prevention & Guardrails

### Potential Abuse Vectors

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Excessive runs (manual triggers) | Medium | High AI costs | Rate limiting |
| Modified flow processing others' data | Low | Security breach | DLP + permissions |
| Large mailbox processing | Medium | Performance/cost | Input limits |
| Prompt injection via email content | Low | AI misbehavior | Output validation |

### Technical Guardrails

**1. Rate Limiting**
```
Implement in flow:
- Max 2 runs per day per user
- Minimum 4 hours between runs
- Kill switch environment variable
```

**2. Input Limits**
```
Already implemented:
- Top 1000 emails only
- Last 24 hours only
- User's own data only
```

**3. Output Validation**
```
Add to flow:
- Max output length check
- Content filtering before send
- Error if AI response anomalous
```

**4. Admin Controls**
```
Environment Variables (Admin-controlled):
- GlobalKillSwitch (Boolean) - Disable all instances
- MaxEmailsToProcess (Integer) - Cap input volume
- AllowedDomains (String) - Restrict to specific user groups
```

### Monitoring for Abuse

| Signal | Threshold | Action |
|--------|-----------|--------|
| Runs per user per day | > 3 | Alert admin |
| AI credits per user per day | > 100 | Alert + throttle |
| Failed runs per user | > 5 consecutive | Auto-disable, notify user |
| Total tenant AI consumption spike | > 150% baseline | Alert COE |

### Governance Controls

1. **Enrollment Approval** (Optional)
   - Require manager approval for access
   - Limit to specific security groups
   - Staged rollout by department

2. **Usage Agreement**
   - Terms of use acknowledgment
   - Data handling awareness
   - AI output disclaimer

3. **Audit Trail**
   - All runs logged with user, time, status
   - AI credit consumption tracked
   - Configuration changes logged

---

## Rollout Phases

### Phase 0: Pre-Flight (2-4 weeks)
- [ ] Answer COE questions checklist
- [ ] Confirm DLP policy compatibility
- [ ] Validate AI Builder capacity
- [ ] Secure pilot budget approval
- [ ] Identify pilot users (10-20)

### Phase 1: Pilot (4-6 weeks)
- [ ] Deploy to pilot group (personal environments)
- [ ] Use Option 1 configuration (flow variables)
- [ ] Weekly check-ins with pilot users
- [ ] Monitor costs and performance
- [ ] Document issues and feedback
- [ ] Refine solution based on learnings

**Success Criteria:**
- 80%+ pilot users actively using
- Error rate < 5%
- Cost within 20% of estimate
- No security incidents

### Phase 2: Limited Release (4-6 weeks)
- [ ] Expand to 50-100 users
- [ ] Build Configuration Power App (Option 2)
- [ ] Deploy monitoring dashboards
- [ ] Create user documentation
- [ ] Establish support channel
- [ ] Implement guardrails

**Success Criteria:**
- Self-service enrollment working
- Support ticket volume manageable
- Costs tracking to model

### Phase 3: General Availability
- [ ] Open enrollment (with approval workflow if needed)
- [ ] Publish to internal app catalog
- [ ] Training materials available
- [ ] Full monitoring operational
- [ ] Chargeback model active (if applicable)

### Phase 4: Optimization (Ongoing)
- [ ] Analyze usage patterns
- [ ] Cost optimization (model selection, caching)
- [ ] Feature enhancements based on feedback
- [ ] Regular security reviews

---

## Appendix: Quick Reference

### Estimated Timeline
| Phase | Duration | Cumulative |
|-------|----------|------------|
| Pre-Flight | 2-4 weeks | 4 weeks |
| Pilot | 4-6 weeks | 10 weeks |
| Limited Release | 4-6 weeks | 16 weeks |
| GA | Ongoing | - |

### Budget Planning Template
```
Pilot (20 users x 2 months):
  AI Credits: ~60,000 credits = ~$600

Limited Release (100 users x 2 months):
  AI Credits: ~300,000 credits = ~$3,000

Year 1 GA (500 users):
  AI Credits: ~3,600,000 credits = ~$36,000/year

+ Development time for Config App
+ Support overhead
+ Monitoring infrastructure
```

### Key Contacts Needed
- [ ] COE Lead
- [ ] DLP Policy Owner
- [ ] AI Builder Capacity Owner
- [ ] Licensing/Procurement
- [ ] Security/Compliance Review
- [ ] Communications (for rollout)
