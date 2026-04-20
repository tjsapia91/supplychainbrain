# 👋 SupplyChainBrain — Start Here

This is your operational brain for running supply chain at Michael Todd Beauty. It's not a task manager, a dashboard, or a code repo. It's where you **think, document, and remember** — so nothing gets lost, and every Claude session picks up where the last one left off.

---

## What This Vault Is For

Think of it in three uses:

### 1. Your Memory (CLAUDE.md)
The `CLAUDE.md` file at the root is the most important file in this vault. Every time you open a session with me (Claudian), I read it first. It tells me:
- What's urgent right now
- What you've already built
- What decisions were made and why
- What's next

**Rule:** At the end of every session that makes decisions or changes, update CLAUDE.md. Then push to GitHub so your work machine stays in sync.

### 2. Your Process Library (Folders 00–09)
Each numbered folder is a domain of your job. As you figure out how things work — how to create a PO, how to evaluate a vendor, how to prep a 3PL shipment — you document it here as an SOP. Future you (and future Claude sessions) will thank you.

### 3. Your Project Tracker (07 AI Tools & Builds + 15 Meetings)
When you're building something (like the ERP, or the demand planning script), you document what was decided, what's in progress, and what's next. Not the code — just the thinking.

---

## What This Vault Is NOT For

- ❌ **Code** — Keep code in its own GitHub repo (the ERP lives at its own repo, not here)
- ❌ **Raw data** — CSVs, exports, reports go in `MTB-SupplyChain/reports/`, not here
- ❌ **Excel files** — Those live on your desktop/OneDrive
- ❌ **Daily task management** — That's what Asana/TrueOps is for

---

## Folder Map

```
supplychainbrain/
│
├── CLAUDE.md                    ← 🧠 The brain. Read this first every session.
├── START HERE.md                ← You're here
├── COMMANDS.md                  ← Available commands and shortcuts
│
├── 00 Forecast & Demand Planning/
│   ├── MTB/                     ← Weekly demand snapshots, forecast notes for MTB
│   ├── NFMD/                    ← Same for NasalFresh MD
│   └── SS/                      ← Same for Spa Sciences
│
├── 01 Purchasing & Inventory/   ← PO tracker, reorder notes, inventory decisions
├── 02 Vendors & Suppliers/      ← Vendor profiles, lead times, contacts, notes
├── 03 3PL & Fulfillment/        ← Floship, ShipBob, AmzPrep notes and SOPs
├── 04 Sales Channels/           ← Amazon, Walmart, TikTok, Shopify notes
├── 05 International Expansion/  ← Customs, compliance, new market notes
│
├── 06 Processes & SOPs/         ← ✅ How things work. Write one every time you
│                                     figure out a process.
│
├── 07 AI Tools & Builds/        ← Planning docs for tools you're building.
│                                     NOT the code itself — just the thinking.
│
├── 08 Key Metrics & Dashboards/ ← Numbers that matter. Weekly snapshots, KPI notes.
├── 09 People & Relationships/   ← Who's who, how to work with them, key contacts
├── 10 System/                   ← Scripts, config, reusable templates
├── 11 Skills/                   ← Skill files (reusable Claude prompts)
├── 12 Attachments/              ← Images, screenshots, supporting files
├── 13 Iteration Logs/           ← What to improve. Retrospectives.
├── 14 Learning & Development/   ← What you're learning about supply chain
└── 15 Meetings & Decisions/     ← Key meetings, decisions made, action items
```

---

## How to Use This With Me (Claudian)

### Starting a session
Just open Obsidian and talk to me. I read `CLAUDE.md` at the start of every session, so I already know the context.

**Good openers:**
- *"What's most urgent right now?"* — I'll pull the current priority list from CLAUDE.md
- *"Can we work on [topic]?"* — I'll orient to that folder and what's there
- *"Teach me about [supply chain concept]"* — I'll explain it in the context of your role at MTB

### During a session
- Ask me to **create notes** — I'll write them in the right folder with the `(C)` prefix
- Ask me to **update a doc** — I'll edit it (but ask before touching files you wrote yourself)
- Ask me to **capture a decision** — I'll add it to the right place and update CLAUDE.md
- Ask me to **look something up** — I'll read relevant vault files before answering

### Ending a session
Always say *"let's wrap up"* — I'll:
1. Summarize what we did
2. Update CLAUDE.md with the new status
3. Remind you to push to GitHub (`git add . && git commit -m "..." && git push`)

---

## The Two-Machine Setup

This vault syncs between your personal machine and work machine via GitHub:

```
Personal Mac (Obsidian)  ←→  GitHub  ←→  Work Machine (Claude Code)
```

**Before working on a new machine:** `git pull`  
**After finishing a session:** `git add . && git commit -m "session notes" && git push`

If you skip the push, the other machine will be out of date and the next Claude session won't know what happened.

---

## What's Built So Far

### Scripts (live in `MTB-SupplyChain/`, not here)
| Script | What it does |
|--------|-------------|
| `analyze_sostocked.py` | Reads SoStocked export, outputs priority list |
| `demand_planning.py` | Full demand planning with DOS, ROP, PO quantities |
| `preprocess_run.py` | Cleans/standardizes CSV reports |
| `generate_weekly_excel.py` | Generates weekly Excel workbook |

### Docs (live here in the vault)
| File | What it covers |
|------|---------------|
| `06 SOPs/(C) Demand Planning SOP.md` | How to run demand planning |
| `06 SOPs/(C) PO Creation SOP.md` | How to create a purchase order |
| `07 AI Tools & Builds/(C) SoStocked Pipeline Discovery.md` | What SoStocked can do, pipeline decisions |
| `07 AI Tools & Builds/(C) Demand Planning Audit.md` | April 20 velocity fix details |
| `01 Purchasing/(C) PO Tracker.md` | Active PO log |

---

## Your Current Priority List

**Check `CLAUDE.md` → "Current Status" section for the live list.**

As of April 20, 2026 — 17 items need action, top ones:
1. 🔴 Sonicsmooth 2.0 Lavender — TRUE STOCKOUT
2. 🔴 Viva Foot Replacement Heads — TRUE STOCKOUT
3. 🔴 NF Salt Packets (Spanish) — 3 days of supply
4. ⚠️ Sonicsmooth Pro+ Peach — 34 days, 61-day lead time

---

## Quick Reference

| I want to... | Do this |
|-------------|---------|
| Know what's urgent | Ask: *"What's most urgent right now?"* |
| Add a vendor profile | Ask: *"Create a vendor profile for [name]"* |
| Document a process | Ask: *"Write an SOP for [process]"* |
| Capture a meeting | Ask: *"Capture the decisions from this meeting: [paste notes]"* |
| Track a project | Ask: *"Create a project doc for [project name]"* |
| Update my status | Ask: *"Update CLAUDE.md — here's what we did today: [notes]"* |
| Wrap up a session | Say: *"Let's wrap up"* |

---

*Last updated: April 20, 2026*
