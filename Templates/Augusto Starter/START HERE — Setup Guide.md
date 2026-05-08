# 🚀 START HERE — Augusto Setup Guide

> Welcome. This zip contains your personal Supply Chain Brain + the Weekly Analysis Agent.
>
> **Total time to set up:** ~90 minutes. Best done with Tommy on screen-share for the first 30 min.

---

## What's in this zip

```
Augusto Starter/
├── START HERE — Setup Guide.md     ← you are here
├── README.md                       ← quick orientation
├── CLAUDE.md                       ← your brain's "soul"
├── 06 Processes & SOPs/            ← daily routine, ABC ref, onboarding
├── 15 Meetings & Decisions/        ← daily action plan template
├── (other 13 numbered folders)     ← your workspace, mostly empty
└── MTB-SupplyChain/                ← the Weekly Analysis Agent
    ├── scripts/                    ← Python scripts (don't edit unless you know what you're doing)
    ├── reports/                    ← drop weekly inputs here
    ├── outputs/                    ← where reports get generated
    └── docs/                       ← reference docs
```

---

## ✅ STEP 1 — Install Tools (20 min)

In order:

### 1A. Obsidian (knowledge management)
- Download: https://obsidian.md
- Install with default settings

### 1B. Python 3.11+ (runs the supply chain scripts)
- Download: https://www.python.org/downloads/
- ⚠️ **CHECK THE BOX** "Add Python to PATH" during install
- Verify: open Command Prompt → `python --version` → should show 3.11 or higher

### 1C. Visual Studio Code (text editor)
- Download: https://code.visualstudio.com
- Default settings

### 1D. Git (optional — for syncing script updates from Tommy)
- Download: https://git-scm.com/download/win
- Default settings

---

## ✅ STEP 2 — Place the Folders (5 min)

Unzip this archive. Drop the two main folders to:

```
C:\Users\[YourName]\supplychainbrain\         ← rename "Augusto Starter" to "supplychainbrain"
C:\Users\[YourName]\MTB-SupplyChain\          ← the agent folder
```

**Important:** Keep these as **separate top-level folders**, not nested inside each other.

---

## ✅ STEP 3 — Open the Brain in Obsidian (5 min)

1. Launch Obsidian
2. First-time screen → click **"Open folder as vault"**
3. Navigate to `C:\Users\[YourName]\supplychainbrain` → click **Select**
4. Trust the vault when prompted (yes, enable plugins)
5. You should see a sidebar with `00 Forecast & Demand Planning`, `01 Purchasing & Inventory`, etc.

✅ If you see those folders — you're in.

---

## ✅ STEP 4 — Install & Configure Claudian (~25 min)

Claudian is the Obsidian plugin that puts Claude Code **inside your vault**. This is what turns your brain from a notebook into a **thinking partner** — Claude can read your files, write new ones, run Python scripts, search across notes, and execute multi-step workflows.

This is the trickiest step. Take your time. If anything's confusing, screen-share with Tommy.

---

### 4A — Get your Anthropic API key (5 min)

Tommy will provide your API key — it's already set up under our team account.

If Tommy hasn't sent it yet:
- Slack/Teams him: **"Hey, can you send me an Anthropic API key for Claudian?"**
- He'll generate one and share it via a secure channel (1Password, encrypted note, etc.)
- The key starts with `sk-ant-...`

⚠️ **Treat the key like a password** — don't paste it in shared docs, don't email it in plain text. Save it in your password manager. If you accidentally expose it, tell Tommy and he'll rotate it.

Paste it temporarily into Notepad so you can use it in step 4C.

---

### 4B — Install Claudian in Obsidian (5 min)

Two paths. **Try Path A first.** If the plugin doesn't appear in the search, fall back to Path B.

#### Path A — Community Plugin marketplace (preferred)

1. **In Obsidian** → click the **gear icon** (bottom-left) → **Settings**
2. In the left sidebar of Settings, scroll down to **Community plugins**
3. **First time using community plugins?**
   - You'll see a "Turn on community plugins" button. Click it.
   - Obsidian shows a warning about "Restricted mode." Click **Turn off restricted mode**.
4. Click **Browse** (next to "Community plugins")
5. In the search bar at the top, type: **`Claudian`**
6. You should see a result with the description: *"Embeds Claude Code as an AI collaborator in your vault..."*
7. Click on it → click **Install**
8. After install, click **Enable**

#### Path B — Manual install (if Claudian isn't in the marketplace)

If Path A doesn't find Claudian, install it manually from GitHub:

1. Go to: https://github.com/YishenTu/claudian/releases (or whatever the current repo is)
2. Download the latest **`main.js`**, **`manifest.json`**, and **`styles.css`** files
3. Navigate to: `C:\Users\[YourName]\supplychainbrain\.obsidian\plugins\`
4. Create a new folder: `claudian` (lowercase)
5. Drop the 3 files into that folder
6. Restart Obsidian
7. Settings → Community plugins → Installed plugins → toggle **Claudian** on

(If neither path works, screen-share with Tommy.)

---

### 4C — Configure Claudian (5 min)

1. Stay in **Settings**
2. In the left sidebar, scroll to the very bottom — under "Community plugins" you'll see **Claudian**. Click it.
3. You'll see Claudian's settings page. Fill in:
   - **Anthropic API Key:** paste the key from step 4A
   - **Working directory:** should auto-fill with your vault path. Confirm it shows `C:\Users\[YourName]\supplychainbrain`
   - **Model:** pick `claude-sonnet-4-5` (or whatever the latest Sonnet model is)
4. Close Settings.

---

### 4D — Test Claudian (5 min)

1. **Open Claudian's chat panel.** Two ways:
   - Look for a **chat-bubble icon** in the left ribbon (Obsidian's left edge with icons). If you see it, click.
   - OR: `Ctrl+P` → type "Claudian" → click "Claudian: Open Chat" or similar.
2. A panel opens with a chat input.
3. Type this message and hit Enter:
   ```
   Read CLAUDE.md and tell me what this vault is set up for.
   ```
4. Wait 5-10 seconds. Claude should respond with a summary of your brain (mentions Michael Todd Beauty, supply chain, the 15 numbered folders, etc.).

✅ **If you get a meaningful response → Claudian is working. Skip to Step 5.**

---

### 4E — If something doesn't work

| Symptom | Try this |
|---|---|
| "Claudian" not in marketplace search | Use Path B (manual GitHub install) |
| "Invalid API key" error | Re-copy the key from console.anthropic.com — no spaces, full string starting with `sk-ant-` |
| "Insufficient credits" or "402" error | Slack Tommy — team account credit needs a top-up |
| Chat panel doesn't open | Close & reopen Obsidian. If still nothing, check Settings → Community plugins → confirm Claudian is enabled (toggle on) |
| Claude responds but can't see files | Working directory in Claudian settings is wrong. Set to your vault root. |
| Nothing happens when you send a message | Check internet connection. Re-check API key. |

If you're stuck for more than 10 minutes — screen-share with Tommy. Don't burn an hour debugging alone.

---

## ✅ STEP 5 — Install Python Dependencies (5 min)

The Weekly Analysis Agent needs a few Python libraries.

1. Open **Command Prompt** (Start → type "cmd")
2. Run these commands:

```
cd C:\Users\[YourName]\MTB-SupplyChain
pip install pandas openpyxl
```

3. Wait for installation to finish (a minute or two)

If you see errors about Python not being found — go back to Step 1B and verify "Add Python to PATH" was checked during install.

---

## ✅ STEP 6 — Test the Weekly Analysis Agent (15 min)

Let's run the scripts and confirm everything works.

### Test 1: Check the folder structure
In Command Prompt:
```
cd C:\Users\[YourName]\MTB-SupplyChain
dir
```
You should see: `docs`, `outputs`, `reports`, `scripts`, `README.md`.

### Test 2: Run the report builder
```
python scripts\build_report.py
```

This should:
- Read the latest demand plan JSON from `outputs/2026-04-27/`
- Load the SAP item master, FBA inbound, AWD inbound, Valogix data
- Generate `outputs/2026-04-27/weekly-report-2026-04-27.xlsx`
- Print success messages

If it works — open the generated Excel file. You should see the 12 tabs (Weekly Summary, Key SKUs, Multi-Channel, etc.)

If it errors — share the error with Tommy. Don't try to debug alone the first time.

---

## ✅ STEP 7 — Connect to the Master Brain on SharePoint (10 min)

The team's shared brain (finished SOPs, agents, references) lives in SharePoint.

1. Go to the supply chain SharePoint site (Tommy will send the link)
2. Find the folder: `Master SupplyChainBrain`
3. Click **Sync** in the top toolbar
4. OneDrive opens and starts syncing
5. The folder appears under: `C:\Users\[YourName]\[Company]\Master SupplyChainBrain\`
6. Wait for green checkmarks (sync complete)

You can browse this folder in File Explorer or open it in Obsidian as a **second vault**:
- Obsidian → File menu → Open another vault → Open folder as vault → point at SharePoint folder

---

## ✅ STEP 8 — Read These in Your First Week (30 min total)

In order of importance:
1. `06 Processes & SOPs/(C) Daily Morning Routine — SCM.md` — **read first** — your morning workflow
2. `06 Processes & SOPs/(C) ABC Classification Reference.md` — the 6 codes (A/B/C/D/E/Z)
3. `06 Processes & SOPs/(C) Augusto Onboarding — Supply Chain Brain.md` — full onboarding
4. `06 Processes & SOPs/(C) Monday Demand Plan Runcard.md` — weekly cycle
5. `06 Processes & SOPs/(C) PO Creation SOP.md` — how POs flow
6. `MTB-SupplyChain/README.md` — agent overview
7. `MTB-SupplyChain/docs/WEEKLY_CHECKLIST.md` — full weekly runcard

---

## 🎯 Your First Week's Goals

- [ ] Run the morning routine **every day** (even when nothing's broken — build the habit)
- [ ] Open the latest weekly report at `MTB-SupplyChain/outputs/[date]/weekly-report-[date].xlsx` and walk through every tab
- [ ] Pick **one** brand (start with NFMD — smallest) and learn its priority items end-to-end
- [ ] Schedule a 30-min sync with Tommy at end of week
- [ ] Build your first Claude Code interaction inside Claudian — ask it to summarize the priority actions for one brand

---

## 🛠 If Things Go Wrong

| Symptom | Try this |
|---|---|
| Obsidian won't open vault | Re-launch → Open folder as vault → re-point at the path |
| Claudian shows "API key invalid" | Re-check your key from console.anthropic.com |
| Claudian can't find files | Confirm working directory is your vault path |
| Python script errors | Open Command Prompt, run the script manually, share error with Tommy |
| `pip install` fails | Run Command Prompt as **Administrator** |
| SharePoint not syncing | Check OneDrive tray icon (bottom-right) — should show green checkmarks |
| Conflict copies in SharePoint | Two people edited same file. Merge manually, delete conflict copy |

---

## 📞 Questions / Help

- Slack/Teams Tommy
- Or email tom@michaeltoddbeauty.com
- First two weeks — assume you'll have questions every day. That's normal.

---

*Created: April 29, 2026*
*Owner: Augusto*
