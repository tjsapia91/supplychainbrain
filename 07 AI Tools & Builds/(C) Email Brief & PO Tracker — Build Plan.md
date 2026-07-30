---
type: build-plan
status: SPEC — awaiting parameter sign-off
created: 2026-07-30
owner: Tom Sapia (SCM)
connector: Microsoft 365 (Outlook) — already authorized on claude.ai
timezone: America/New_York (ET) — all times display + schedule in ET
---

# (C) Email Brief & PO Tracker — Build Plan

Turn Tom's Outlook inbox into (A) a daily prioritized **brief + task list**, and (B) a self-updating **PO tracker** that places every vendor PO at its workflow stage and flags the stuck ones. Proven out with two live runs on 2026-07-30 (see `15 Meetings & Decisions/(C) Email Brief — 2026-07-30` + `01 Purchasing & Inventory/(C) PO Tracker — Harry (Ningbo Zeyu)`).

---

## Why (the problem)
- ~150+ emails land in 48h; most are automated (EDI, daily inventory/fulfillment reports, marketing). The 5–10 that actually need Tom get buried.
- PO status lives scattered across sent + received threads. "Which POs are signed? which are stuck waiting on approval?" has no single view.

## What it produces
1. **📬 Email Brief** — `15 Meetings & Decisions/(C) Email Brief — <date>.md`. A 1-line theme + a checkable, prioritized task list (🔴 critical / 🟠 this week / 🟡 medium / ⚪ FYI). Same format as the 7/30 POC.
2. **📑 PO Tracker refresh** — updates `01 Purchasing & Inventory/(C) PO Tracker — *.md`: each PO's stage + next action, and STUCK flags.
3. **🛒 EDI Retail Orders refresh** — updates `01 Purchasing & Inventory/(C) EDI Retail Orders Tracker.md`: parses each EDI 850/860 (retailer, PO#, type, delivery date, line items); surfaces cancellations, rolls up routine status-updates.

## Scope & filters (LOCKED 2026-07-30)
| Parameter | Setting |
|---|---|
| Brief scope | **EVERYTHING** in the last 24h (all mail, not just unread/flagged) — paginate past the 25/page cap |
| PO-tracker window | Last **120 days**, per vendor |
| Mailbox | Own inbox + Sent Items (both — sent mail is where POs + approvals originate) |
| **Auto-exclude (noise)** | Filter the robots out of the brief (still counted, never deleted): `wisesys@unisco.com`, `noreply@floship.com`, `sellersupport@shop.tiktok.com`, ShipBob marketing, `quarantine@messaging.microsoft.com`. Confirmed OK to filter (Tom 2026-07-30). |
| **EDI — TRACK, don't exclude** | `edisupport@ecom-specialist.com` = retail POs/changes (how partners order). Parse each 850/860 into the **[[01 Purchasing & Inventory/(C) EDI Retail Orders Tracker]]** (retailer · PO# · type · delivery date · line items). **Cancellations float to the brief; routine status-updates roll up as a batch.** (Tom 2026-07-30) |
| Escalate to top | Leadership + key vendors float up — see People below |

## People (org map — LOCKED 2026-07-30)
| Tier | Who |
|---|---|
| Leadership (escalate) | **Michael** — CEO (final PO signer) · **Lilia** — SVP · **Donna** — Director · **Leo** — CMO |
| PO approvers | **Lilia** (SVP) + **Donna** (Director) — either approves |
| Tom's associates | **Augusto** (Demand Planning) · **Elisa** |
| Key vendors (PO-tracked) | **Harry Zhan** — Ningbo Zeyu · **YAC Chemicals** · **Emily** · **Oxygen** *(need each one's email address to wire up)* |

> Note: the 7/29 "SVP recap" + the all-day inventory review both came from **Lilia (SVP)** via lil@michaeltoddbeauty.com.

## Prioritization logic (Tom's rules)
`supply risk / stockout → PO / reorder → expedite / transfer → approvals & meetings → FYI`, then bump anything from leadership or a key vendor. Extract the concrete ask from each actionable email (who/what/when).

## PO-tracker state machine (the smart part)
Maps email events → the [[06 Processes & SOPs/(C) PO Approval Workflow SOP]] stages. Stage ① (SAP entry) isn't email → inferred/manual; ②–⑧ are all detectable:

| Email event | → Stage |
|---|---|
| Tom → Harry, PO attached (`PPO####*.pdf`) | ② PO→Harry |
| Harry → Tom, PI attached | ③ PI received |
| Tom → Lilia/Donna/Supply Chain, PO+PI attached | ⑥ with approvers |
| Lilia/Donna → Michael (Tom cc'd) | ⑦ approved → Michael |
| Michael → Tom, signed | ⑧ signed (pending send) |
| Tom → Harry, body says "approved and signed" | ⑧ **LIVE** |

**STUCK flags:** PI received > 2 business days but not yet sent to approvers · with approvers > 3 days, no approval · signed but not yet sent to Harry · PPO number referenced with no PI after N days.

## Cadence / how it runs (LOCKED 2026-07-30)
Tom's machine isn't always on, so a fixed-time cron is unreliable. Chosen approach:
- **Run automatically when Tom opens Obsidian** (startup trigger) → the brief regenerates each time he sits down, no dependence on the machine being on at a set hour.
- **Plus on-demand** `/email-brief` (and `/po-tracker`) anytime.
- *(Not used: fixed cloud cron — a cloud agent could read Outlook with the machine off but can't write to the local vault. Revisit only if the vault moves fully to a synced/cloud store.)*

## Privacy & safety (hard rules)
- **Read-only.** Never send, reply, delete, move, or flag an email without Tom explicitly asking.
- Briefs/trackers are written only to the local vault; nothing leaves the machine.

## Tech notes / constraints
- Built on the **Microsoft 365 connector** (already authorized): `outlook_email_search` (25/page — paginate for full coverage), `read_resource` (full body + attachment list).
- **Attachments/PDFs** (PO/PI quantities, $) require opening the PDF — heavier; make it opt-in per PO, not every run.
- Timezone: API returns **UTC** → always convert to **ET** for display and scheduling.
- Volume guard: `log` how many automated messages were filtered so nothing silently dropped.

## Phases
1. **MVP** — on-demand `/email-brief` (brief + task list, with auto-noise-filter). ✅ POC done 7/30.
2. **PO tracker** — sent+received lifecycle → stage machine + stuck flags. ✅ POC done 7/30 (Harry).
3. **Schedule** — 7 AM ET morning run.
4. **Refine** — multi-vendor PO tracking; optional PDF qty/$ extraction; fold PO↔PI check into the existing **PPO Validator** web app.

## Decisions — LOCKED 2026-07-30
1. **Scope:** everything, last 24h ✅
2. **Cadence:** run on Obsidian-open + on-demand `/email-brief` (no fixed cron — machine not always on) ✅
3. **Vendors:** Harry (Ningbo Zeyu), YAC Chemicals, Emily, Oxygen ✅
4. **Auto-exclude robots from the brief:** yes (counted, not deleted) ✅
5. **Leadership/escalation:** Michael (CEO) · Lilia (SVP) · Donna (Director) · Leo (CMO); associates Augusto, Elisa ✅

### Only thing still needed to build
- **Email addresses for the 3 new vendors** — YAC Chemicals, Emily, Oxygen (Harry = harryzhan@nb-zeyu.com is known). Candidates seen in mail: `marketing9@yacgp.com`, `salesassistant2@latop.com.cn` (Hair Spray thread) — confirm which is YAC. Give me the addresses (or point me at a thread with each) and Phase 1 is ready to build.
