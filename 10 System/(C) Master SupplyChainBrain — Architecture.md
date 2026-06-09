# (C) Master SupplyChainBrain — Architecture

> The team's central, cloud-based knowledge library on SharePoint. Where finished SOPs, reusable agents, vetted reference docs, and approved processes live so the whole supply chain team can access them.
>
> **Last updated:** June 8, 2026

---

## The publish model

```
┌────────────────────────────┐
│   Personal Brain (local)   │
│   ─────────────────────    │
│   - Daily notes            │
│   - Drafts                 │
│   - WIP projects           │
│   - Daily action plans     │
│   - Iteration logs         │
└──────────────┬─────────────┘
               │
               │   PUBLISH when finished + vetted
               ▼
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

**Personal brain = workspace.** Where you draft, take notes, run experiments. Lives at `C:\Users\Tom Sapia\supplychainbrain\`.
**Master brain = library.** Where the team's polished, approved knowledge lives. On SharePoint.

---

## What lives where

### ✅ Master Brain (SharePoint) — published, finalized, shared

| Category | Examples |
|---|---|
| **SOPs** | Daily Morning Routine, PO Creation SOP, ABC Classification, Weekly Analysis SOP |
| **Agents / Skills** | Reusable Claude Code agents ("Run Weekly Demand Plan", "Pull FBA Shipment Status") |
| **Reference docs** | ABC code table, urgency tier definitions, formulas, lead time table |
| **Vendor info** | Master vendor list, contact info, lead times, MOQs, payment terms |
| **3PL info** | ShipBob / Floship / Alliance account info, OTIF SLAs, escalation contacts |
| **Templates** | Daily action plan template, weekly retro template, vendor scorecard template |
| **Training** | FAQ, glossary, role-specific docs for new hires |
| **Approved scripts** | Final versions of `demand_planning.py`, `build_report.py`, etc. |
| **Master inputs** | Item master export, SAP refreshes — versioned, dated |

### 🔒 Personal Brain (local) — drafts, notes, daily work

| Category | Examples |
|---|---|
| **Daily action plans** | `15 Meetings & Decisions/Daily Action Plans/` — morning routine output |
| **Drafts** | Half-written SOPs, ideas being tested |
| **Personal notes** | Meeting notes, learning notes, ideas |
| **WIP projects** | Active projects before the deliverable is published |
| **Iteration logs** | What got tried, what failed |
| **Personal context** | Task lists, priorities, calendar mirroring |

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
    │   ├── Alliance/
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
    │   ├── (C) Weekly Analysis SOP — Step by Step.md
    │   ├── (C) Weekly Analysis Cheat Sheet — 1 Page.md
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
    └── 15 Meetings & Decisions/            ← Team meeting notes (NOT personal daily plans)
```

---

## Sync workflow — how to publish to the master brain

### When something is "ready" to publish:

1. **Finish the SOP / agent / template in the personal brain**
2. **Review the doc** — check that it reflects current state, no stale tab names, no broken links
3. **Move (or copy) the file to the SharePoint folder** at the right location
4. **Update the prefix** if it's now an approved version (e.g., `(C)` becomes `(SOP)` or remove the prefix entirely)
5. **Add to the Master Brain index** if it deserves visibility

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
| Director of Supply Chain | Full edit | Reviews and approves changes |
| SVP Operations | View + comment | Read access |
| IT / Admin | Full edit (technical) | For SharePoint config |
| Other supply chain team members | View or Edit (case-by-case) | Default View; upgrade to Edit when contributing |

---

## Migration plan — getting from "all-local" to "SharePoint master + local personal"

### Phase 1 — Set up SharePoint
- [ ] Create the master folder in supply chain SharePoint site
- [ ] Set permissions per matrix above
- [ ] Create the folder structure (just empty folders matching the layout above)
- [ ] Add a `README.md` at the root explaining the structure

### Phase 2 — Populate
- [ ] Publish the **finished** SOPs from the personal brain to SharePoint:
  - Daily Morning Routine SOP
  - Weekly Analysis SOP — Step by Step (just refreshed Jun 8)
  - Weekly Analysis Cheat Sheet — 1 Page (just refreshed Jun 8)
  - PO Creation SOP
  - ABC Classification Reference
  - SharePoint Migration Guide
  - This doc (Master Brain Architecture)
- [ ] Publish the **approved scripts** from `MTB-SupplyChain/scripts/` — final reviewed versions only

### Phase 3 — Ongoing
- [ ] As new SOPs / agents are built, publish to the master brain (per Always-Update Rule)
- [ ] Quarterly: prune outdated content, archive what's not needed

---

## Why this architecture works

1. **Personal brain stays nimble** — no worry about "is this ready for the team?" while drafting
2. **Master brain stays clean** — only vetted, finished content
3. **Onboarding new people is a copy-paste** — point them at the SharePoint folder
4. **No single point of failure** — if the laptop dies, the master brain is fine on SharePoint
5. **Knowledge survives turnover** — when someone leaves, their personal brain is theirs; the master brain stays with the company

---

## Open questions

- [ ] Exact SharePoint site URL where the master folder will live? (TBD with IT)
- [ ] Does the master brain need its own GitHub backup separately from SharePoint? (likely no — SharePoint versioning + OneDrive sync is enough)
- [ ] Naming: "Master SupplyChainBrain" vs "SC Library" vs "SC Knowledge Hub"? (TBD)
- [ ] Do we want the master brain's structure to mirror the local vault exactly, or simplify? (Recommend: same structure for low cognitive overhead)

---

## Related docs

- [[10 System/SharePoint Migration Guide]] — sync setup steps
- [[06 Processes & SOPs/(C) Weekly Analysis SOP — Step by Step]] — example of a SharePoint-ready SOP

---

*Created: April 28, 2026 · Last updated: June 8, 2026*
*Owner: Tommy*
