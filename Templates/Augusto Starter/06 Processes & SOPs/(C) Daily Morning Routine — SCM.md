# (C) Daily Morning Routine — Supply Chain Manager

> The 30-minute process I run every morning to make sure I don't miss anything important and walk out of my desk with a clear list of 3-5 things to do today.

**Total time: 30 minutes.**
**Goal: Walk away with a written list of 3-5 specific actions for today, in priority order.**

---

## Before you start (the night before — 2 min)

Just before logging off:
- Note any hot item carrying into tomorrow
- Make sure these tabs are bookmarked / pinned:
  - Outlook (work email)
  - Amazon Seller Central — login per brand (MTB, NFMD, SS)
  - Sellerboard
  - SoStocked
  - ShipBob portal
  - Floship portal
  - Slack/Teams
  - This vault (Obsidian)

---

## STEP 0 — Set the scene (2 min)

1. Coffee. Don't skip this.
2. Open today's blank Daily Action Plan note in the vault:
   `15 Meetings & Decisions/Daily Action Plans/[YYYY-MM-DD].md`
   (If it doesn't exist, copy the template at the bottom of this doc.)
3. Open today's weekly report Excel:
   `C:\Users\Tom Sapia\MTB-SupplyChain\outputs\[latest date]\weekly-report-[date].xlsx`
4. Open the previous day's Daily Action Plan note (you'll need it in Step 2).

You're now ready. Start a 30-min timer.

---

## STEP 1 — 90-second pulse check (1.5 min)

**Just look. Don't act yet.** You're scanning for fires.

Scan these:
- **Email subject lines** — any with the words *stockout, delay, issue, urgent, OTIF, hold, customs, suspended*?
- **Slack / Teams** — any messages from DOS, SVP Ops, or vendors that came in overnight?
- **Amazon Seller Central (each brand)** — any red-dot account health alerts on the homepage?

**If yes to any →** write it down in today's plan under `### 🔥 Inbox Hot`.
**If no →** proceed.

> Why this matters: 80% of your "fires today" are already in your inbox. Knowing what's hot before doing analysis means you don't waste 25 min only to find out you should have responded to a vendor first.

---

## STEP 2 — Yesterday's carryover (3 min)

Open yesterday's Daily Action Plan note.

For each item under "Today's Actions" from yesterday, mark:
- ✅ **Done** — close it out
- 🔄 **Carries to today** — copy it to today's `Carried Over` section
- ❌ **Won't do** — write a one-line reason and let it die

Also check yesterday's `Waiting On` list:
- Did the person/vendor you were waiting on get back to you? If not, **chasing them might become today's action**.

> Why this matters: This is how nothing falls through the cracks. Without this step, follow-ups die quietly and become tomorrow's stockouts.

---

## STEP 3 — Inventory health scan (5 min)

Open the weekly report → **📊 Weekly Summary tab**.

### Read in this order:

**A) KPI tiles at the top.**
Look at "Priority Actions" number. Compare to last week (you'll start tracking this in your Friday retro). Higher = more risk this week.

**B) Marketplace Snapshot section.**
Any marketplace where "Need Action" jumped from last week?
- Amazon goes from 5 → 12: investigate
- Walmart goes from 2 → 8: investigate
- Floship steady: ignore for today

**C) Priority Actions section.**
For each row (max 8-12 items), read:
- **PRODUCT** — what is it
- **MARKETPLACE** — where is it stocking out (Amazon US, Shopify MTB, Walmart, etc.)
- **DOS** — days of supply remaining
- **LEAD TIME** — how long it takes to replace
- **PO QTY** — recommended order quantity

### Decision rules:

| If you see... | What to do |
|---|---|
| DOS < 7 days AND no PO in flight | **Action today**: place urgent PO or send-in from ShipBob |
| DOS < 30 days AND no PO in flight | **Action today**: confirm with vendor and place PO |
| DOS < lead time + 30 days AND no PO | **Action this week**: get on schedule |
| DOS healthy AND PO already placed | Skip — already handled |
| DOS=0 + Vel < 0.1/day | Likely a dead listing — flag for SKU review |

> Why this matters: This is the heart of your job. Most SCMs only react when something stocks out. You're catching it 30, 60, 90 days ahead.

---

## STEP 4 — Open PO check (5 min)

> ⚠️ **First-time setup**: If you don't yet have a single place where every open PO is tracked, **building this is your priority project this week**. For now, do the manual check.

### Manual check (until the tracker exists):

Scan the last 2 weeks of vendor email threads in Outlook:

- **Sent a PO, no acknowledgment back?** → vendor follow-up
- **PO past expected ETA with no shipment notice?** → vendor follow-up
- **Vendor went silent for 5+ business days?** → vendor follow-up

### Decision rules:

| If you see... | What to do |
|---|---|
| PO sent >48 hrs ago, no confirmation | Email vendor today: "confirming receipt of PO #X" |
| ETA passed by 3+ days, no shipment | Email vendor today: "where are we on PO #X?" |
| Customs / freight forwarder hold | Escalate to forwarder + DOS today |
| New vendor I haven't worked with | Block 30 min this week to review their lead times |

> Why this matters: A PO that doesn't get confirmed for a week = a 1-week shift in arrival = a 1-week shift in when the SKU stocks out. Stay on top of every one.

---

## STEP 5 — 3PL portal check (3 min)

### ShipBob:
1. Inventory tab → look for any item with "received but not available" sitting >3 days
2. Orders tab → any back-order count?
3. Inbound shipments → any stuck "in receiving"?

### Floship:
1. Inventory tab → same check
2. Outbound orders → any failures?
3. Customs / hold notifications → any pending?

### Decision rules:

| If you see... | What to do |
|---|---|
| Inbound stuck in receiving > 3 days | Email 3PL contact today |
| OTIF dropping below 95% | Schedule a check-in with 3PL account manager this week |
| Inventory adjustment (units lost) | Investigate today, document in vault |
| Returns spiking | Loop in CS team to find out why |

> Why this matters: Your 3PLs are your warehouse. If they fail, you fail. Catch issues before they become a Sales/CS escalation.

---

## STEP 6 — Channel velocity sanity check (3 min)

Open **Sellerboard**:
- Yesterday's revenue per brand — is it within 20% of the 7-day average?
- Big spike (>30% up): a SKU is going viral or had a promo — does inventory match this new pace?
- Big drop (>30% down): something's wrong — listing suppressed, ad campaign paused, competitor undercut?

Open **Walmart Marketplace** (if available):
- Same check

Open **Shopify** (if available):
- Same check

### Decision rules:

| If you see... | What to do |
|---|---|
| SKU selling 2x forecast | DOS calculation is wrong — flag for re-forecast, possibly expedite |
| SKU revenue dropping suddenly | Loop in marketing/sales — is the listing OK? |
| New ASIN getting traction | Make sure it has stock everywhere it sells |

> Why this matters: Forecasts are wrong. Your job is to know when they're wrong before stockouts/overstock happen.

---

## STEP 7 — Set today's 3-5 actions (5 min)

Look at everything you flagged in steps 1-6. Now ruthlessly prioritize.

### Rules:
1. **Maximum 5 actions.** If everything is priority, nothing is.
2. **Each must have an outcome by end of day.** Not "work on PO" — "PO #X sent to vendor by 4pm."
3. **Each must have a first step.** Not "follow up with Floship" — "send Tom@floship the email I drafted."
4. **Order them by impact, not by time.** Hardest/highest-impact first when your brain is fresh.

### Format (paste into today's plan):

```
## 🎯 Today's Actions — 2026-04-28

1. [WHAT] — [WHY/impact if not done] — [target time]
   First step: [specific 1-line action]

2. [WHAT] — [WHY] — [target time]
   First step: [...]

3. ...
```

**Now stop planning and DO action #1. Don't read more emails. Don't open another tab. Execute.**

---

## END OF DAY — 5 min wrap

Before you log off:

1. Reopen today's Daily Action Plan note
2. Mark each action: ✅ / 🔄 / ❌
3. Add a `### 📝 Lessons` section at the bottom:
   - Did anything blow up that I should have caught earlier?
   - Anything that should become a permanent SOP?
   - One thing I learned today
4. Save. Close. Done.

> Why this matters: 5 minutes of reflection compounds into expertise. After 90 days you'll have a written record of every lesson learned. After a year you'll know more about MTB's supply chain than anyone.

---

## DAILY ACTION PLAN — Template

Copy this into a new note each morning at:
`15 Meetings & Decisions/Daily Action Plans/[YYYY-MM-DD].md`

```markdown
# Daily Action Plan — YYYY-MM-DD

## 🔥 Inbox Hot
- [from Step 1]

## 🔄 Carried Over from Yesterday
- [from Step 2]

## 📊 Inventory Risks (from weekly report)
- [items with DOS < 30 from Step 3]

## 📦 Open PO Followups
- [from Step 4]

## 🚚 3PL Items
- [from Step 5]

## 📈 Channel Anomalies
- [from Step 6]

---

## 🎯 TODAY'S ACTIONS (3-5 max — non-negotiable)
1. [WHAT] — [WHY] — [target time]
   First step: ...
2. ...
3. ...

## ⏳ Waiting On
- [items I'm blocked on, who I'm waiting on, when I expect a response]

## 💭 Nice to Do (if time)
- [...]

---

## ✅ End of Day Wrap
1. [done/carry/cancelled]
2. ...

## 📝 Lessons
- [anything I learned, anything that should become an SOP]
```

---

## When this routine breaks down

**"I don't have time for 30 minutes."**
→ Run the **5-min Pulse Check** version: Steps 1, 2, 7. Skip the deep scans.
→ Better than nothing. Build back to 30 min when life calms down.

**"I'm in back-to-back meetings all morning."**
→ Run it the night before. Yes, every night. The morning routine is just confirmation that nothing changed overnight.

**"I keep forgetting steps."**
→ Don't rely on memory. Open this doc every morning until it's automatic (3-4 weeks).

**"I hit Step 7 and don't know how to prioritize."**
→ Slack me / Claude — paste your flagged items, ask "which 3 should I do today?"

---

## Building this into a habit

- **Week 1:** Follow the doc literally. Mechanical. 30-40 min is fine.
- **Week 2:** You'll know the order. Down to 25 min.
- **Week 3:** You'll know the decision rules without re-reading them. Down to 20 min.
- **Week 4:** You'll know which scans matter most TODAY based on yesterday's signals. Down to 15 min for a normal day.

After a month of doing this every morning, you will be ahead of 90% of supply chain managers because **you'll be operating proactively instead of reactively**.

---

*Created Apr 28, 2026 — version 1*
*Owner: Tommy*
