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

## Scope & filters (parameters — defaults, confirm)
| Parameter | Default | Confirm? |
|---|---|---|
| Brief window | Unread + flagged, last **24h** | |
| PO-tracker window | Last **120 days**, per vendor | |
| Mailbox | Own inbox + Sent Items (both — sent mail is where POs + approvals originate) | |
| **Auto-exclude (noise)** | automated senders unless they contain action keywords: `wisesys@unisco.com`, `noreply@floship.com`, `sellersupport@shop.tiktok.com`, ShipBob marketing, `edisupport@ecom-specialist.com` (EDI — summarize count, surface only cancellations), `quarantine@messaging.microsoft.com` | |
| Escalate to top | Leadership (Michael/CEO, Lil, Director/SVP) + key vendors (Harry) float up | |

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

## Cadence / how it runs
- **On-demand:** a Claude Code command `/email-brief` (and/or `/po-tracker`).
- **Scheduled (optional):** a routine every morning **7:00 AM ET** so the brief is waiting. (Uses the `schedule` skill / cron.)

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

## Open decisions to lock before build
1. Brief scope — unread+flagged 24h, or all last-24h, or key-people-only?
2. Cadence — on-demand only, or add the 7 AM ET schedule?
3. Vendors to PO-track beyond Harry?
4. Confirm the auto-exclude sender list above.
5. Who exactly are "leadership" for escalation (Michael = CEO; is Lil the Director or SVP)?
