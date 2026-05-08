# (C) Augusto Day 1 — Walkthrough Script

> 60-minute screen-share session. Run this with Augusto on his first day. Goal: he walks away with his brain set up + understands the day-to-day.
>
> **Created:** April 28, 2026

---

## Before the session

**Tommy preps (5 min):**
- [ ] Have the onboarding doc open: [[06 Processes & SOPs/(C) Augusto Onboarding — Supply Chain Brain]]
- [ ] Zip up `Templates/Augusto Starter/` (or have GitHub starter repo ready)
- [ ] Confirm SharePoint folder exists and Augusto has access
- [ ] Have your weekly report Excel open as a demo
- [ ] Have your Daily Action Plan from today open

**Augusto preps (5 min before call):**
- [ ] Admin access on laptop confirmed
- [ ] M365 / SharePoint login working
- [ ] Slack/Teams open
- [ ] 60-min calendar block

---

## Session structure (60 min)

### 0–10 min — The big picture

Show Augusto the **two-brain model** (whiteboard or share architecture doc).

> "You're getting your own brain — local on your machine. The team has a shared brain on SharePoint. Your personal brain is your workspace; the master brain is the library. We publish finished work to the master brain, but daily notes stay personal."

Walk through:
- Why we use Obsidian (markdown, fast, syncs nicely)
- Why Claude Code (your AI assistant for building tools, not just chatting)
- Why SharePoint master brain (team-shared, never lost)

---

### 10–35 min — Hands-on setup (do it together)

Walk through `(C) Augusto Onboarding` document **steps 1-5** with him sharing his screen.

- ✅ Install tools (Obsidian, Python, Claude Code, VS Code)
- ✅ Drop the starter brain folder
- ✅ Open vault in Obsidian
- ✅ Sync SharePoint master folder
- ✅ Wire Claude Code to his vault

**Common gotchas — watch for these:**
- Python "Add to PATH" checkbox — easy to miss
- SharePoint sync needs OneDrive client running (check tray icon)
- Claude Code first auth — needs Anthropic account login
- Vault path in Claude Code — must be exact

---

### 35–50 min — The daily workflow

Walk Augusto through:

#### A. The Morning Routine (5 min)
- Open `[[06 Processes & SOPs/(C) Daily Morning Routine — SCM.md]]`
- Skim the 7 steps
- Show him how you actually run it (open your Daily Action Plan from today as live example)

#### B. The Weekly Report (5 min)
- Open `weekly-report-2026-04-27.xlsx`
- Click through the tabs:
  - 📊 Weekly Summary — the executive view
  - 🌐 Multi-Channel — all marketplaces
  - 🎯 Key SKUs — priority watchlist
  - 🔚 Phase-Out Review (E→Z) — items to potentially obsolete
  - 🗑 Obsolete (Z) — already-obsolete tracker
- Show him how to read a Priority Action row

#### C. Building with Claude Code (5 min)
Live demo: have Claude Code do something useful in his vault.

Try something simple:
> "Read CLAUDE.md and tell me what's on the priority actions list this week."

Or:
> "Look at the daily morning routine doc and create today's action plan template for me."

Goal: he sees that Claude Code does **real work**, not just chat.

---

### 50–60 min — Roles + first week's goals

#### Discuss roles:
- **Tommy** — Amazon (FBA + AWD), 3PL strategy, weekly demand planning, ERP/dashboards
- **Augusto** — Logistics, freight, demand planning support, agent building
- **Both** — Vendor relationships, monthly leadership review

#### First week's goals:
- [ ] Run morning routine every day
- [ ] Walk through weekly report once with Tommy (already done above)
- [ ] Pick one brand (NFMD recommended — smallest) and learn its priority items
- [ ] First Claude Code build: pick something small (e.g., script to summarize the inbox)
- [ ] End-of-week sync with Tommy — what worked, what didn't

#### How we collaborate:
- Slack/Teams for quick questions
- Project folders for shared work (`Projects/[Project Name]/`)
- Each person edits their own `[Name].md` file in those projects
- Weekly 1:1s for first month, then move to bi-weekly

---

## After the session

**Tommy follow-up (within 24 hrs):**
- [ ] Send Augusto the SharePoint folder link
- [ ] Send him the starter brain (zip or GitHub link)
- [ ] Add him to relevant Slack/Teams channels
- [ ] Schedule weekly 1:1 for next 4 weeks
- [ ] Add him to vendor email distribution lists (when relevant)

**Augusto homework (week 1):**
- [ ] Read morning routine SOP
- [ ] Read ABC classification reference
- [ ] Build first daily action plan
- [ ] Run morning routine every day (even if rough)
- [ ] Identify 2-3 things he doesn't understand → bring to weekly 1:1

---

## Things to NOT cover on Day 1 (save for later)

Day 1 is overload — keep it focused. **Skip these for now:**
- Git workflow (add only if/when he needs it)
- Building agents/skills in detail (cover Day 2 or week 2)
- Demand planning script internals (week 3+)
- Custom dashboard work (month 2+)
- Vendor email automation (month 2+)
- ERP/Django stuff (don't show until he's settled)

---

## What success looks like 30 days in

- ✅ Augusto runs his morning routine without thinking about it
- ✅ He's published 1-2 SOPs or agents to the master brain
- ✅ He owns at least one ongoing project (logistics-related likely)
- ✅ He's the go-to for at least one area Tommy doesn't deep-dive on
- ✅ He's training the next person if/when one joins

---

*Created: April 28, 2026*
*Owner: Tommy*
