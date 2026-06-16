# (C) SupplyChainClaude — Index

**Mount type:** Windows directory Junction
**Vault path:** `10 System/SupplyChainClaude/`
**Real location:** `C:\Users\Tom Sapia\OneDrive - michaeltoddbeauty.com\Documents\SupplyChain1\SupplyChainClaude`
**Sync:** OneDrive (Microsoft 365). Edits in either location are reflected in both.
**Git:** the junction folder is in `.gitignore` — these files are versioned by OneDrive history, not by the vault repo.

---

## Why this is here

`SupplyChainClaude` is the operator-authored brain that drives **Claudian** (this AI assistant) when working on Tommy's supply-chain pipeline. It holds:

- Operating principles + project context that should colour every session
- Live operational briefs (fix briefs, refactor briefs, deep-dives)
- A master bug register
- A runbook
- Per-role design notes (Demand Planner, Logistics Coordinator, Procurement Specialist, Supply Chain Lead, Supply Planner)
- Sample outputs Claudian can reference

Mounting it inside the vault lets Obsidian search/index it, lets `@`-references and `[[wikilinks]]` work, and lets Claudian read it the same way as any other vault note.

---

## Top-level files

| File | Purpose |
|---|---|
| [[SupplyChainClaude/PROJECT-CONTEXT.md\|PROJECT-CONTEXT]] | What this project is and who it's for |
| [[SupplyChainClaude/SESSION-HANDOFF-2026-06-09.md\|SESSION-HANDOFF 2026-06-09]] | Last operator session handoff (pre-this-week) |

---

## Subfolders

### `Executive Assistant/`
Config that defines the Executive Assistant role. Contains its own `CLAUDE.md`, `MEMORY.md`, and `context/`.

### `Supply Chain Planning/`
The active workbench. Where Tommy drops fix briefs, refactor briefs, deep dives, and where Claudian reads them.

Key files (most recent first):

| File | Purpose |
|---|---|
| [[SupplyChainClaude/Supply Chain Planning/WEEKLY-REPORT-CORRECTIONS-for-Claudian-2026-06-15.md\|WEEKLY-REPORT-CORRECTIONS 2026-06-15]] | FIX A/B/C/D/E brief — supply-pool, EXPEDITE defer, SAP column mismatch |
| [[SupplyChainClaude/Supply Chain Planning/THIS-WEEK-TAB-FIXES-for-Claudian-2026-06-15.md\|THIS-WEEK-TAB-FIXES 2026-06-15]] | FIX 0-9 brief — stale-extract gate, sort, kit guard, interim flag, unit cost, etc. |
| [[SupplyChainClaude/Supply Chain Planning/DEEPDIVE-811573031335-811573031342-2026-06-15.md\|DEEPDIVE 811573031335/811573031342]] | Sonicsmooth Clear Replacement Kit + Pro+ Lavender — 2026-06-15 |
| [[SupplyChainClaude/Supply Chain Planning/DEEPDIVE-LELA-850003115948-2026-06-15.md\|DEEPDIVE LELA 850003115948]] | LELA Skin Spatula Pink — 2026-06-15 |
| [[SupplyChainClaude/Supply Chain Planning/STATE-OF-SUPPLY-CHAIN-2026-06-15.md\|STATE-OF-SUPPLY-CHAIN 2026-06-15]] | Snapshot of the whole network as of 2026-06-15 |
| [[SupplyChainClaude/Supply Chain Planning/OPERATING-PRINCIPLES.md\|OPERATING-PRINCIPLES]] | The rules of engagement — read these before doing anything else |
| [[SupplyChainClaude/Supply Chain Planning/RUNBOOK.md\|RUNBOOK]] | Step-by-step procedures for routine ops |
| [[SupplyChainClaude/Supply Chain Planning/MASTER-BUG-REGISTER.md\|MASTER-BUG-REGISTER]] | Known issues across the pipeline |
| [[SupplyChainClaude/Supply Chain Planning/CONDUCTOR-DESIGN-live-supply-chain-lead.md\|CONDUCTOR-DESIGN]] | Multi-agent orchestration design |
| [[SupplyChainClaude/Supply Chain Planning/CONDUCTOR-PHASE1-buildspec-for-Claudian.md\|CONDUCTOR-PHASE1 BUILDSPEC]] | Build spec for the Conductor agent — Phase 1 |
| [[SupplyChainClaude/Supply Chain Planning/REFACTOR-sku-model-wiring-for-Claudian.md\|REFACTOR sku-model-wiring]] | SKU model refactor brief |
| [[SupplyChainClaude/Supply Chain Planning/DATA-INPUTS.md\|DATA-INPUTS]] | What pipeline inputs exist and where they come from |
| [[SupplyChainClaude/Supply Chain Planning/location-crosswalk.md\|location-crosswalk]] | Warehouse-code ↔ channel crosswalk |

Role-specific design folders: `Demand Planner/`, `Logistics Coordinator/`, `Procurement Specialist/`, `Supply Chain Lead/`, `Supply Planner/`.

Other folders: `_INPUTS/`, `sample-outputs/`, `scripts/` (Conductor's script library — separate from `MTB-SupplyChain/scripts/`).

---

## When Claudian should read from here

| Trigger | Read |
|---|---|
| Start of any session | OPERATING-PRINCIPLES, PROJECT-CONTEXT, latest SESSION-HANDOFF |
| Operator drops a brief at `Supply Chain Planning/*-for-Claudian-*.md` | That brief, in full |
| Investigating a specific SKU | matching `DEEPDIVE-{upc}-*.md` if present |
| Working on the Conductor or multi-agent design | CONDUCTOR-DESIGN, CONDUCTOR-PHASE1 |
| Debugging a known issue | MASTER-BUG-REGISTER |
| Performing a routine op | RUNBOOK |

---

## How the junction was created

```cmd
mklink /J ^
  "C:\Users\Tom Sapia\supplychainbrain\10 System\SupplyChainClaude" ^
  "C:\Users\Tom Sapia\OneDrive - michaeltoddbeauty.com\Documents\SupplyChain1\SupplyChainClaude"
```

To remove it: `rmdir "C:\Users\Tom Sapia\supplychainbrain\10 System\SupplyChainClaude"` (this only removes the junction — does NOT delete the OneDrive files). Use `rmdir`, **not** `del /s` or "send to recycle bin," or you risk deleting through the junction.

Tommy 2026-06-16.
