---
type: email-brief
date: 2026-08-06
window_hours: 24
generated_by: /email-brief
status: living
---

# 📬 Email Brief — Wednesday, Aug 6, 2026

**Theme:** UNIS inventory-report call is **today 2 PM ET** — bring the reconciliation. Meanwhile a JCP EDI order got **rejected**, and ShipBob spelled out how the blade air-in actually has to be routed.

---

## 🔴 Critical — today

- [ ] **UNIS "Inventory Status Report" call — TODAY 2 PM ET (11 AM PST).** *David Renteria (UNIS), sent 8/5 6:02 PM ET.* He set up the call to walk the inventory report with you + Donna. → **Attend.** Bring the on-hand reconciliation you already ran (our 13,370 vs Seller Central 13,197 = reserved-buckets + snapshot timing) — that's the exact "why don't the numbers match" conversation.

- [ ] **JCP.com EDI order 32461438 — REJECTED.** *ecom-specialist EDI, 8/4 (rejected 8/3).* Stand-alone order, Dept 960, Contract 300136667765, PO date 7/31. → Find out **why JCP bounced it** (ask Sean Mullino / ecom-specialist). ⚠ Separate from the direct-email JCP MIO Green 252u order you logged 8/3 — confirm this rejection doesn't also kill that one.

---

## 🟠 This week

- [ ] **Blade air-in routing — ShipBob rules confirmed.** *Samantha DiPaolo / Jadayra Rivera (ShipBob), 8/5.* You **cannot** air-freight directly to the PA/GA spoke sites — everything must inbound through a **receiving hub** (West / Moreno Valley or Northeast) then IPP-route to the spokes, and **hub-movement SLA times apply**. To split the air load across all 3 DCs: create **a WRO per region** (select the hub, turn OFF auto-distribute, pick the site). → This is the mechanism for the **25k blade fly-in** — plan the WROs per hub, and factor the hub→spoke SLA into the sellable-by date.

- [ ] **Missed ShipBob receiving appointment — WRO 983270** (NA-26 US West Hub 2, 8/5 11 AM PDT missed). *Gaurav Gupta sent updated appointments 8/5.* → Confirm the rebooked slots are on the calendar so this inbound doesn't age.

- [ ] **Mio 850003115139(-1) de-kit — verify the split.** *Jadayra Rivera (ShipBob), 8/5 5:33 PM ET.* ShipBob opened a ticket to confirm item **20651820** was de-kitted to **true green (no white)**. Donna's open question: were units pulled OUT of base 850003115139 before the de-kitted items were entered? → This is the accuracy check behind our **Green/White line split** — hold the split as tentative until ShipBob confirms.

- [ ] **Container ONEU6390520 (the "4th Aug" container) — DO issued, headed to UNIS.** *Harry 8/5 9:17 PM ET; Donna working drayage.* Seal **CNEB38651**; delivering to **UNIS (new warehouse — no truck needed)**; CI 039. This is the Sat→Tue-delayed boat, now moving. Drayage handled by Donna/UNIS (Steffany at unis has the DO). → Track landing; nothing on you right now.

---

## 🟡 Medium

- [ ] **Batch code `SBD0726` — Juan needs a confirm.** *Juan Isaza, 8/5 3:41 PM ET ("SBD0726?" on the Signed PPOs thread).* SBD = **SonicSmooth Blades (item 1632), July 2026** print. → Confirm the code with Juan; logged in [[01 Purchasing & Inventory/(C) Batch Code Tracker.md]].
- [ ] **Oxygen Glow Facial Oil — artwork locked.** *Smile Severino / Michael, 8/5.* Master-shipper label centered to fully cover the old barcode; batch code goes **in the flap** and on the **color-box bottom**. Pickup was targeted **8/7**. → Confirm pickup holds.
- [ ] **QVC late shipment FH94** — ShipBob can't generate labels for **PO-BOX ship-to** addresses; Elisa manually shipped 2 orders via our own stamps to make the customer whole. *Elisa, 8/5.* → Retail-compliance risk with QVC; Elisa is driving, but watch for repeats.
- [ ] **PO 3255 security tags (Ina / Shenzhen Deta)** — Donna following up again 8/5, Ina traveling, no response. → Stuck vendor thread.

---

## ⚪ FYI

- **Panama Canal suspended part of its booking system** (Tradlinx newsletter, 8/6). Ocean-freight watch — no MTB action, but relevant to the blade containers' routing.
- **Walgreens** proposing weekly → **bi-weekly** order frequency; only ~$4k online sales/yr, buyer suggesting we may drop the online listing. *Elisa's account.*
- **TikTok Shop inventory dashboard access** — Lil sent invites; Donna didn't receive hers, yours was resent (Lil, 8/5).
- **CVS 812 credit adjustments** — two $200.98 credits (already logged 8/3); **JCP 812** $10 debit (8/4).
- **Walmart 816** org-relationship change (routine).
- **NasalFresh Walmart ad campaign** alerts — "top selling items disabled" (Barcode Group / Walmart Connect). Marketing, not SC.

---

## EDI batch (routed to tracker)
- **CVS 860 STATUS UPDATEs:** 8 msgs 8/6 (PO# 5084950 · 2507268 · 7549216 · 3830025 · 8359965 · 1664069 · 0629052 · 9041769, all PO-date 8/4) + the 8/4 batch. Routine revisions.
- **⚠ CVS 860 CANCELLATIONS:** **3786008** (8/5) · **0623974** (8/4) · **1658759** (8/4) — verify nothing already shipped/committed.
- **⚠ JCP 860 REJECTIONs:** 32461438 + contract 300136667765 (8/4) — see Critical above.

---

*Footer: ~8 automated/robot messages filtered (UNIS Wise ×2, Floship ×2, quarantine, ShipBob auto-ack, Amazon Accelerate, Schneider cold-outreach); ShipBob OpenDock missed-appointment surfaced once (3 duplicate copies). EDI: 8 messages routed to the EDI tracker this window (+7-day vendor/EDI sweep for tracker upkeep). Read-only run — nothing sent, moved, or deleted.*
