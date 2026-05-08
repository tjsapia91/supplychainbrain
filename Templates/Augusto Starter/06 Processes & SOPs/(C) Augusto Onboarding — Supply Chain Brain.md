# (C) Augusto Onboarding — Supply Chain Brain

> Step-by-step setup so Augusto has his own working Supply Chain Brain on his Windows machine — same tools as Tommy, customized for his role (logistics + demand planning).
>
> **Time to complete:** ~90 minutes. Best done with Tommy on a screen-share for the first 30 min.
>
> **Last updated:** April 28, 2026

---

## What you're getting

- **Personal Supply Chain Brain** (your own vault) — daily notes, drafts, action plans, your work
- **Access to the Master Brain** (SharePoint) — finished SOPs, agents, references the team shares
- **Claude Code** — your AI assistant for building tools, analyzing data, automating reports
- **Same tooling Tommy uses** — so we can collaborate on projects without translation

---

## Before you start

Make sure you have:
- [ ] Admin access on your Windows laptop (to install software)
- [ ] Your Microsoft 365 / SharePoint login working
- [ ] About 90 minutes of uninterrupted time
- [ ] Tommy on screen-share for first 30 minutes (recommended)

---

## STEP 1 — Install the tools (20 min)

Install these in order. Click each link, follow defaults unless noted.

### 1A. Obsidian (knowledge management — your "brain" lives here)
- Download: https://obsidian.md
- Install with default settings
- Don't open it yet — we'll point it at the vault in Step 3

### 1B. Python 3.11+ (runs the supply chain scripts)
- Download: https://www.python.org/downloads/
- ⚠️ **CHECK THE BOX** "Add Python to PATH" during install — easy to miss
- Verify: open Command Prompt → type `python --version` → should show 3.11 or higher

### 1C. Git (version control — optional but recommended)
- Download: https://git-scm.com/download/win
- Default settings
- Verify: Command Prompt → `git --version`

### 1D. Claude Code (your AI assistant)
- Download: https://claude.ai/download (click "Claude Code" if shown)
- Or follow Anthropic's setup: https://docs.anthropic.com/claude/claude-code
- Sign in with your work or personal Anthropic account
- Tommy can help with first-time setup

### 1E. Visual Studio Code (text editor — for code/scripts)
- Download: https://code.visualstudio.com
- Default settings

---

## STEP 2 — Get the starter brain (15 min)

Tommy will share a stripped-down version of his vault with you — no personal notes, just the structure + templates.

**Option A — Copy from Tommy's machine via shared drive:**
1. Tommy zips `Augusto Starter/` from his vault
2. He drops it in: `[shared location]`
3. You unzip to: `C:\Users\[YourName]\supplychainbrain\`

**Option B — Clone from GitHub** (if Tommy sets up a starter repo):
1. Open Command Prompt
2. `cd C:\Users\[YourName]`
3. `git clone https://github.com/tjsapia91/supplychainbrain-starter.git supplychainbrain`

Either way, you should end up with this folder on your machine:
```
C:\Users\[YourName]\supplychainbrain\
```

---

## STEP 3 — Open the vault in Obsidian (5 min)

1. Launch Obsidian
2. First-time screen → click **"Open folder as vault"**
3. Navigate to your `supplychainbrain` folder, click **Select**
4. Trust the vault when prompted (yes, enable plugins)
5. You should see a sidebar with folders:
   ```
   00 Forecast & Demand Planning/
   01 Purchasing & Inventory/
   02 Vendors & Suppliers/
   03 3PL & Fulfillment/
   ...
   ```

✅ If you see those folders — you're in. Skim around for 5 min to get the lay of the land.

---

## STEP 4 — Connect to the Master Brain on SharePoint (10 min)

The team's shared brain (finished SOPs, agents, references) lives in SharePoint. You sync it once and it shows up as a folder on your machine.

1. Go to the supply chain SharePoint site (Tommy will send the link)
2. Find the folder: `Master SupplyChainBrain` (or whatever Tommy named it)
3. Click **Sync** in the top toolbar
4. OneDrive opens and starts syncing
5. The folder appears under: `C:\Users\[YourName]\[Company]\Master SupplyChainBrain\`
6. Wait until OneDrive shows green checkmarks (sync complete)

You can browse this folder in File Explorer or open it in Obsidian as a **second vault**:
- Obsidian → File → Open another vault → Open folder as vault → point at SharePoint folder

---

## STEP 5 — Set up Claude Code with your vault (10 min)

Claude Code needs to know where your vault is so it can read/write files there.

1. Open Claude Code
2. When asked for working directory, point at: `C:\Users\[YourName]\supplychainbrain`
3. First message — try this:
   ```
   Read CLAUDE.md and tell me what this vault is set up for.
   ```
4. Claude should respond with a summary of the brain's purpose.

If something looks off — Tommy can hop on screenshare to debug.

---

## STEP 6 — Customize for you (15 min)

The starter brain has placeholders. Update these:

### 6A. Edit `CLAUDE.md` (the brain's "soul")
- Open `CLAUDE.md` in Obsidian
- Find the line: `Last updated: [date]`
- Replace: `Last updated: April 28, 2026 — Augusto's brain`
- Find any references to "Tommy" — leave them where they're correct, but add yourself where it makes sense (e.g., "Augusto — Logistics & Demand Planning")
- Save

### 6B. Create your first daily action plan
- Open Obsidian → press `Ctrl+N` (new note)
- Save in: `15 Meetings & Decisions/Daily Action Plans/`
- Filename: today's date, e.g. `2026-04-29.md`
- Use this template:

```markdown
# Daily Action Plan — [Date]

## 🔥 Inbox Hot
- 

## 🔄 Carried Over from Yesterday
- 

## 📊 Inventory Risks (from weekly report)
- 

## 📦 Open PO Followups
- 

## 🚚 3PL Items
- 

## 📈 Channel Anomalies
- 

---

## 🎯 TODAY'S ACTIONS (3-5 max)
1. 

## ⏳ Waiting On
- 

## 💭 Nice to Do (if time)
- 

---

## ✅ End of Day Wrap
- 

## 📝 Lessons
- 
```

This is the same template Tommy uses every morning — see `06 Processes & SOPs/(C) Daily Morning Routine — SCM.md` for the full routine.

---

## STEP 7 — Read these in your first week (30 min total)

In order of importance:
1. `06 Processes & SOPs/(C) Daily Morning Routine — SCM.md` — your morning workflow (30 min/day forever)
2. `06 Processes & SOPs/(C) ABC Classification Reference.md` — the 6 codes (A/B/C/D/E/Z) you'll see everywhere
3. `CLAUDE.md` — full brain orientation
4. `06 Processes & SOPs/(C) Monday Demand Plan Runcard.md` — weekly cycle
5. `06 Processes & SOPs/(C) PO Creation SOP.md` — how POs flow

---

## STEP 8 — Your first week's wins

Goals for week 1:
- [ ] Run the morning routine **every day** (even when nothing's broken — build the habit)
- [ ] Open the latest weekly report at `MTB-SupplyChain/outputs/[date]/weekly-report-[date].xlsx` and walk through every tab
- [ ] Pick **one** brand (start with NFMD — smallest, easiest) and learn its priority items end-to-end
- [ ] Schedule a 30-min sync with Tommy at end of week — what you learned, what's still confusing
- [ ] Build your first Claude Code interaction — ask it to summarize the priority actions for one brand

---

## How you and Tommy collaborate

**Daily/weekly:**
- Each of you maintains your own personal brain
- You share work via the SharePoint Master Brain (publish finished agents/skills/SOPs there)
- Daily standup or Slack check-ins

**Splitting work:**
- **Tommy** — Amazon (FBA + AWD), 3PL strategy, weekly demand planning runs, ERP/dashboards
- **Augusto** — Logistics (containers, freight, 3PL ops), demand planning support, agent building
- **Both** — Vendor relationships, monthly review with leadership

**When you need to share something:**
- Finished agent/skill → publish to SharePoint Master Brain → Tommy pulls it
- Project collaboration → both work in `Projects/[Project Name]/` folder. Each person edits their own `[Name].md` file. Shared `Overview.md` and `Log.md` — one person at a time.

---

## When things go wrong

| Symptom | Try this |
|---|---|
| Obsidian won't open vault | Re-launch Obsidian → Open folder as vault → re-point at the path |
| Claude Code can't find files | Confirm working directory is your vault path |
| Python script errors | Open Command Prompt, run the script manually, share the error with Tommy |
| SharePoint not syncing | Check OneDrive tray icon (bottom-right of taskbar) — should show green check |
| Conflict copies in SharePoint | Two people edited same file. Merge manually, delete the conflict copy |

---

## Questions / blockers — reach out

- Slack/Teams Tommy
- Or email tom@michaeltoddbeauty.com
- First week — assume you'll have questions every day. That's normal.

---

*Created: April 28, 2026*
*Owner: Augusto (with help from Tommy)*
