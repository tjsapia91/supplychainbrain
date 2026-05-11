# TrueOPS Shipment Module — Open Questions & Backlog

> Park ideas, open questions, system improvements, and parked workflows here. Don't let useful thoughts die in a chat thread.

---

## 🔓 Open questions

*(none yet — add as they come up)*

---

## 🛠 System improvements / backlog

### 🆕 Daily sync — flag new additions

**Goal:** Each morning's `dailySync()` run should make it obvious which shipments are new since yesterday.

**Three layers:**

1. **Row-level highlight** — when `Created` date is within the last 24h, fill row with light-cream background (`#FFF8DC`). Color fades next sync as those rows age out of the 24h window.
2. **"🆕 NEW THIS SYNC" section on Triage tab** — pin to the top, above existing Needs Action / Aging Watch sections. One row per new shipment, sorted by Estimated Amount desc. Clears next morning.
3. **Email digest banner** — top line of the 7am digest reads `X new shipments today · $Y at risk · top: {Shipment ID}`. Already-emailed-yesterday shipments stay below.

**Implementation notes:**
- Use `PropertiesService.getScriptProperties()` to persist `lastSyncTime` between runs — that's the "what's new" anchor
- New = Created date > lastSyncTime
- Highlight via `range.setBackground('#FFF8DC')`; clear stale highlights via a `clearOldHighlights_()` helper that wipes any background older than 25h
- Skeleton code captured in chat May 8, 2026 — Claudian conversation

**Status:** Parked — hand to operational Claude Project (claude.ai) to actually patch the Apps Script.

**Prompt to give the operational Claude:**
> "Update `dailySync()` to flag new shipments — row highlight + Triage 'New This Sync' section + digest banner. See backlog doc for spec."

---

---

## 🚧 Parked workflows

### 🅿️ Operational Claude Project setup — PARKED May 8, 2026

**Where we left off:**
- Docs-side Claude (folder-bound to `07 AI Tools & Builds/TrueOPS Shipment Module/`) is live and absorbed the brief ✅
- Operational Claude Project (claude.ai) is NOT yet set up
- Tommy verified claude.ai connectors — only **Google Drive** is available (no Google Sheets or Apps Script MCPs)

**What still needs to happen:**
1. Create the Project on claude.ai → name: `TrueOPS Shipment Operations`
2. Paste the full system brief into Project knowledge
3. Connect Google Drive to the Project
4. Run the first-chat test prompt:
   > Read the brief in Project knowledge. Then read the Master_Shipment_Log sheet (Drive file ID `1VXQUGn1dwpUqv2wW0ZWksZB3LbBZPlQR3IKjRMPdYU8`) and tell me: today's overdue count, the 5 highest-$ items currently on the Triage tab, and any STAR-prefixed items in Awaiting Vendor status that haven't been contacted in >7 days.
5. Verify Drive can read `.gsheet` files. If yes → proceed. If no → fallback to manual copy/paste workflow.
6. Patch `dailySync()` for new-shipment highlighting (spec already in `🛠 System improvements` section above)
   - Workflow: open Apps Script editor → copy current `dailySync()` → paste into Project chat → Claude returns patched code → paste back into editor → save → run once to test

**Key constraint:**
- No Sheets MCP and no Apps Script MCP — every Apps Script edit is copy/paste between the Project chat and the script editor
- Daily 7am trigger fires automatically regardless of Claude availability

**Trigger phrases to revisit:**
- *"Let's pick up TrueOPS setup"*
- *"Resume the TrueOPS Shipment Module work"*
- *"Continue the operational Claude Project setup"*

---

---

## ✅ Done — completed improvements

- 2026-05-08 — Module brief captured in vault for source-of-truth tracking
