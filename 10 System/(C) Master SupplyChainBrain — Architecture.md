# (C) Master SupplyChainBrain — Architecture

> The team's central, cloud-based knowledge library on SharePoint. Where finished SOPs, reusable agents, vetted reference docs, and approved processes live so the whole supply chain team can access them.
>
> **Last updated:** April 28, 2026

---

## The two-brain model

```
┌────────────────────────┐         ┌────────────────────────┐
│  Tommy's Personal      │         │  Augusto's Personal    │
│  Brain (local)         │         │  Brain (local)         │
│  - Daily notes         │         │  - Daily notes         │
│  - Drafts              │         │  - Drafts              │
│  - Personal action     │         │  - Personal action     │
│    plans               │         │    plans               │
│  - WIP projects        │         │  - WIP projects        │
└──────────┬─────────────┘         └──────────┬─────────────┘
           │                                  │
           │   PUBLISH when finished/vetted   │
           ▼                                  ▼
        ┌──────────────────────────────────────────┐
        │   📚 MASTER SUPPLYCHAINBRAIN             │
        │   (SharePoint — cloud, team-shared)      │
        │   - Finished SOPs                        │
        │   - Reusable agents / skills             │
        │   - Reference docs (ABC, vendor lists)   │
        │   - Weekly report templates              │
        │   - Approved processes                   │
        │   - Vendor scorecards                    │
        │   - Training materials                   │
        └──────────────────────────────────────────┘
```

**Personal brain = workspace.** Where you draft, take notes, run experiments.
**Master brain = library.** Where the team's polished, approved knowledge lives.

---

## What lives where

### ✅ Master Brain (SharePoint) — published, finalized, shared

| Category | Examples |
|---|---|
| **SOPs** | Daily Morning Routine, PO Creation SOP, ABC Classification, Monday Demand Plan Runcard |
| **Agents / Skills** | Reusable Claude Code agents (e.g. "Run Weekly Demand Plan", "Pull FBA Shipment Status") |
| **Reference docs** | ABC code table, urgency tier definitions, formulas, lead time table |
| **Vendor info** | Master vendor list, contact info, lead times, MOQs, payment terms |
| **3PL info** | ShipBob/Floship account info, OTIF SLAs, escalation contacts |
| **Templates** | Daily action plan template, weekly retro template, vendor scorecard template |
| **Training** | Onboarding docs (Augusto's), FAQ, glossary |
| **Approved scripts** | Final versions of demand_planning.py, build_report.py, etc. |
| **Master inputs** | Item master export, SAP refreshes — versioned, dated |

### 🔒 Personal Brain (local) — drafts, notes, daily work

| Category | Examples |
|---|---|
| **Daily action plans** | `15 Meetings & Decisions/Daily Action Plans/` — your morning routine output |
| **Drafts** | Half-written SOPs, ideas you're testing |
| **Personal notes** | Meeting notes, learning notes, ideas |
| **WIP projects** | Active projects before the deliverable is published |
| **Iteration logs** | What you tried, what failed |
| **Personal context** | Your task lists, priorities, calendar mirroring |

---

## SharePoint folder structure (proposed)

```
[Supply Chain SharePoint Site]
└── Master SupplyChainBrain/
    ├── README.md                          ← Start here. What this is, how to use it.
    ├── 00 Forecast & Demand Planning/
    │   ├── Forecasting SOPs/
    │   ├── Demand Plan Templates/
    │   └── Brand-specific notes/ (MTB / SS / NFMD)
    ├── 01 Purchasing & Inventory/
    │   ├── PO Templates/
    │   ├── Approved PO SOPs/
    │   └── Inventory health checklists/
    ├── 02 Vendors & Suppliers/
    │   ├── Vendor Master List.xlsx
    │   ├── Per-vendor profiles/
    │   └── Vendor scorecards/
    ├── 03 3PL & Fulfillment/
    │   ├── ShipBob/
    │   ├── Floship/
    │   ├── AmzPrep (if/when transitioned)/
    │   └── 3PL OTIF tracking/
    ├── 04 Sales Channels/
    │   ├── Amazon (per brand)/
    │   ├── Walmart Marketplace/
    │   ├── Shopify/
    │   ├── TikTok Shop/
    │   └── Nordstrom/
    ├── 05 International Expansion/
    ├── 06 Processes & SOPs/                ← The good stuff. Daily/weekly/monthly cadence
    │   ├── (C) Daily Morning Routine — SCM.md
    │   ├── (C) Monday Demand Plan Runcard.md
    │   ├── (C) PO Creation SOP.md
    │   ├── (C) ABC Classification Reference.md
    │   └── (Other approved SOPs)/
    ├── 07 AI Tools & Builds/
    │   ├── Approved Skills & Agents/
    │   │   ├── Run Weekly Demand Plan/
    │   │   ├── Pull FBA Shipment Status/
    │   │   └── Vendor Email Drafts/
    │   ├── Build documentation/
    │   └── Prompt library/
    ├── 08 Key Metrics & Dashboards/
    │   ├── Weekly report archive (one folder per date)/
    │   └── KPI definitions/
    ├── 09 People & Relationships/
    │   ├── Team contact list/
    │   └── Org chart/
    ├── 10 System/
    │   ├── (C) Master SupplyChainBrain — Architecture.md (this doc)
    │   ├── SharePoint Migration Guide.md
    │   └── Setup & sync instructions/
    ├── 11 Skills/                          ← Markdown skill files
    ├── 12 Attachments/                     ← Images, PDFs, screenshots
    ├── 14 Learning & Development/          ← Team training materials
    ├── 15 Meetings & Decisions/            ← Team meeting notes (NOT personal daily plans)
    └── Templates/
        ├── Daily Action Plan template.md
        ├── Weekly Retro template.md
        ├── Vendor Scorecard template.xlsx
        └── Augusto Starter/                ← Stripped vault for new team members
```

---

## Sync workflow — how to publish to the master brain

### When something is "ready" to publish:

1. **You finished an SOP / agent / template in your personal brain**
2. **Tommy reviews it** (or Augusto reviews Tommy's — whichever)
3. **Move (or copy) the file to the SharePoint folder** at the right location
4. **Update the `(C)` prefix** if it's now an approved version (e.g., `(C)` becomes `(SOP)` or just remove the prefix)
5. **Add to the Master Brain index** if it deserves visibility

### Conflict prevention:

- **One person edits at a time** for any single Master Brain file
- **Your personal brains are personal** — never edit Tommy's vault, never edit Augusto's vault from the other person
- **Central files have "owners"** — Tommy owns weekly report SOP; Augusto owns logistics SOPs (TBD)

### File naming conventions:

| Prefix | Meaning |
|---|---|
| `(C)` | Claude-generated — needs human review |
| (no prefix) or `(SOP)` | Reviewed and approved |
| `(WIP)` | Work-in-progress in master brain |
| `(ARCHIVE)` | Outdated but kept for reference |

---

## Permissions model

| Role | Access | Notes |
|---|---|---|
| Tommy | Full edit | Owner of the master brain |
| Augusto | Full edit | Co-owner |
| DOS (Director of Supply Chain) | Full edit | Reviews and approves |
| SVP Operations | View | Read access; can comment |
| IT / Admin | Full edit (technical) | For SharePoint config |
| Other supply chain team members | View or Edit (case-by-case) | Default View; upgrade to Edit when they're contributing |

---

## Migration plan — getting from "all-local" to "SharePoint master + local personal"

### Phase 1 — Set up SharePoint (Week 1)
- [ ] Create the master folder in supply chain SharePoint site
- [ ] Set permissions per matrix above
- [ ] Create the folder structure (just empty folders matching the layout above)
- [ ] Add a `README.md` at the root explaining the structure

### Phase 2 — Populate (Week 2)
- [ ] Tommy publishes the **finished** SOPs from his personal brain to SharePoint:
  - Daily Morning Routine SOP
  - Monday Demand Plan Runcard
  - PO Creation SOP
  - ABC Classification Reference
  - SharePoint Migration Guide
  - This doc (Master Brain Architecture)
- [ ] Tommy publishes the **starter vault** (`Templates/Augusto Starter/`) for future team members
- [ ] Tommy publishes the **approved scripts** from `MTB-SupplyChain/scripts/` — final reviewed versions only

### Phase 3 — Onboard Augusto (Week 2)
- [ ] Run through `(C) Augusto Onboarding — Supply Chain Brain.md` together
- [ ] Confirm he can sync the SharePoint folder
- [ ] Confirm Claude Code is wired up to his vault
- [ ] Schedule weekly 1:1 for first month

### Phase 4 — Iterate (ongoing)
- [ ] As Augusto builds new agents/SOPs, publish them to the master brain
- [ ] As Tommy refines processes, update the master versions
- [ ] Quarterly: prune outdated content, archive what's not needed

---

## Why this architecture works

1. **Personal brains stay nimble** — you don't worry about "is this ready for the team?" while drafting
2. **Master brain stays clean** — only vetted, finished content
3. **Onboarding new people is a copy-paste** — point them at the SharePoint folder + the starter vault
4. **No single point of failure** — if Tommy's laptop dies, the master brain is fine
5. **Knowledge survives turnover** — when someone leaves, their personal brain is theirs to take. The master brain stays with the company.

---

## Open questions

- [ ] Exact SharePoint site URL where the master folder will live? (Tommy to confirm with IT)
- [ ] Does the master brain need its own GitHub backup separately from SharePoint? (likely no — SharePoint versioning + OneDrive sync is enough)
- [ ] Naming: "Master SupplyChainBrain" vs "SC Library" vs "SC Knowledge Hub"? (Tommy/team to decide)
- [ ] Do we want the master brain's structure to mirror Tommy's vault exactly, or simplify? (Recommend: same structure for low cognitive overhead)

---

## Related docs

- [[06 Processes & SOPs/(C) Augusto Onboarding — Supply Chain Brain]] — onboarding step-by-step
- [[10 System/SharePoint Migration Guide]] — sync setup
- [[Projects/Team Brain — SharePoint Migration/Overview]] — project tracker

---

*Created: April 28, 2026*
*Owner: Tommy*
