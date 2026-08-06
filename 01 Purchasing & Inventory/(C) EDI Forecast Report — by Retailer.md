---
type: edi-forecast-report
brand: SPA (Spa Sciences) + NFMD lines sold through CVS
source: EDI service — edisupport@ecom-specialist.com
generated: 2026-08-06
horizon: 2026-08-23 → 2026-10-24 (latest CVS 830)
companion: "[[01 Purchasing & Inventory/(C) EDI Retail Orders Tracker.md]]"
status: living
---

# 📈 EDI Forecast Report — by Retailer

Per-retailer view of what the EDI channel is actually telling us to plan for. **Only CVS sends a true forecast** (the 830 Planning Schedule); JCP and Walmart send discrete/administrative EDI only, so their "forecast" is order run-rate, not a transmitted plan.

| Retailer | EDI forecast? | What flows | Planning signal |
|---|---|---|---|
| **CVS** | ✅ **Yes — 830** | Weekly 830 Planning Schedule (per vendor acct) + 812 deductions | **5,562 u** on order horizon (8/23–10/24) |
| **JCP** | ❌ No | 860 changes/rejections + 812 only; **real POs come by email** | Run-rate only; 1 EDI order **REJECTED** (32461438) |
| **Walmart** | ❌ No | 816 org-relationship + 812 chargebacks only | **Nothing to fulfill via EDI** currently |

---

## 🟢 CVS — 830 Forecast (latest, received 2026-08-02)

**CVS's forecast of record.** Buyer (Tristan Viens-Roderick, 8/3): *"refer to your EDI 830 reports for forecasting."* Quantities in **pieces**. Horizon = weeks **8/23 → 10/24** (header date 10/25). The weekly batch is **3 emails split by CVS vendor account**, not by DC:
- **40287** → NFMD item **581999** · **40867** → NFMD item **669709** · **36143** → the 10-SKU SPA / Spa-Sciences book (incl. AIVA).
- DC codes (N101, L101, C101, … Y101) are ship-to distribution centers *within* each item's breakdown.

### Forecast matrix — units per week-start (8/2 830)

| Item # | UPC | Line (family)¹ | 8/23 | 8/30 | 9/6 | 9/13 | 9/20 | 9/27 | 10/4 | 10/11 | 10/18 | **Total** |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 357217 | 860021001134 | Spa Sciences (top mover) | 756 | 132 | 84 | 96 | 84 | 108 | 120 | 48 | 120 | **1,548** |
| 669709 | 850038082627 | NFMD | 192 | 60 | 84 | 60 | 72 | 108 | 48 | 84 | 84 | **792** |
| 581999 | 850038082314 | NFMD | 222 | 54 | 72 | 66 | 90 | 72 | 78 | 66 | 66 | **786** |
| 357740 | 860021001165 | Spa Sciences | 108 | 48 | 84 | 24 | 24 | 72 | 36 | 48 | 120 | **564** |
| 357751 | 860021001172 | Spa Sciences | 60 | 36 | 72 | 12 | 48 | 12 | 60 | 72 | 72 | **444** |
| 412712 | 850026141290 | PRIMA | 144 | — | — | 96 | 12 | 120 | 24 | 12 | 24 | **432** |
| 473740 | 850003115948 | SPA | 72 | 12 | 48 | — | 48 | 12 | 48 | 36 | 84 | **360** |
| 830645 | 850003115436 | SPA | 48 | — | 36 | 24 | 96 | — | — | 36 | 48 | **288** |
| **732452** | **850003115634** | **AIVA** | — | 48 | — | 36 | 48 | — | — | — | 24 | **156** |
| 356781 | 860021001127 | Spa Sciences | 12 | 12 | 24 | 12 | 12 | 12 | — | — | 12 | **96** |
| 336884 | 850026141383 | PRIMA | 12 | — | — | 12 | — | 24 | — | 12 | — | **60** |
| 168548 | 850003115856 | SPA | — | — | — | 12 | — | — | — | 24 | — | **36** |
| **TOTAL** | | | **1,626** | **402** | **504** | **450** | **534** | **540** | **414** | **438** | **654** | **5,562** |

¹ Family is **inferred from UPC prefix** (860021001xxx = Spa Sciences · 850026141xxx = PRIMA · 850038082xxx = NFMD) — the 830 carries item#+UPC only, no descriptions. AIVA (850003115634) is confirmed. Match on **item number** (stable); the UPC check digit is truncated in the feed.

**Read:** front-loaded — **1,626 u (29%) in the first week (8/23)**, then a steady ~400–650/wk tail. Top 3 SKUs (357217 + the two NFMD) = **3,126 u = 56%** of the whole book.

---

## 🟢 CVS — Forecast trend (week-over-week)

| 830 batch (received) | Horizon end | Grand total | Δ vs prior |
|---|---|--:|--:|
| 7/19/2026 | 10/11 | 5,430 | — |
| 7/26/2026 | 10/18 | 5,196 | −234 (−4.3%) |
| **8/2/2026** | 10/24 | **5,562** | **+366 (+7.0%)** |

Net over 2 weeks **+132 (+2.4%)** — essentially flat. The wobble is almost entirely **NFMD 581999** (1,254 → 396 → 786). The SPA book is steadier and trending **up**, led by the top mover 357217 (1,116 → 1,428 → 1,548).

Per-SKU (8/2 / 7/26 / 7/19): 357217 **1548/1428/1116** · 669709 792/660/744 · 581999 **786/396/1254** · 357740 564/540/468 · 357751 444/504/528 · 412712 432/528/444 · 473740 360/432/348 · 830645 288/300/216 · AIVA 156/180/132 · 356781 96/108/96 · 336884 60/48/36 · 168548 36/72/48.

> **Planning note:** the 830 is a rolling *planning* forecast, not firm POs — treat the near weeks as reliable and the tail as directional. AIVA's 156 u through late Oct is the ongoing trickle, **not** a door-restore (the door build-up was already bought). See EDI tracker.

---

## 🟡 JCP — Orders (last 60 days)

**No fulfillable JCP orders came through EDI.** JCP's real POs arrive by **direct email**, not EDI — only 812/820 and 860 change/rejection notices flow through the EDI service.

| Doc | PO # | Blanket/Contract | PO date | Status |
|---|---|---|---|---|
| 860 change | **32461438** | 300136667765 (qty-firm blanket) | 7/31 | 🔴 **REJECTED 8/3** — Vendor 169623 · Dept 960 |

- **No line items recoverable** — the rejection notice is header-only; qty/UPC/price/ship-to and the reject reason code were not transmitted. → Chase Sean Mullino / ecom-specialist for the reason; confirm it doesn't affect the direct-email JCP MIO Green 252u (logged 8/3).
- Also in window (AR, not orders): 812 credit/debit memos vs older JCP POs 31857762 and 31981751.
- **Run-rate:** 0 fulfillable EDI units in 60 days. JCP planning must come from the email-order history, not this channel.

---

## 🟡 Walmart — EDI activity (last 60 days)

**No Walmart EDI purchase orders.** The Walmart EDI relationship is currently **administrative + chargeback only** — zero 850/855/860/997 order-cycle docs.

- **816 (Organizational Relationships):** ~9 weekly store/company-hierarchy "Change" files (reference data, not orders) — 6/7 → 8/2, often duplicated 2–3×.
- **812 (Credit/Debit):** ~8 debit-memo/chargeback batches vs the SPA account, referencing existing Walmart PO#s (5684167996, 2384532816, 9634175665, claim 0000000163). These are **deductions**, not new demand.
- Walmart demand for planning still comes from Seller Center / Valogix — **not** this EDI feed.

---

## How this report is built / refresh
- **Forecast = CVS 830 only.** Parsed from the weekly `edisupport@ecom-specialist.com` "830 Planning Schedule" emails (3 per week, by vendor account). Sum the SDQ week quantities per item# across all DCs.
- **Refresh:** re-run when a new 830 batch lands (weekly, ~Sun/Mon 6 AM ET). Update the matrix + append the new total to the trend table.
- **Descriptions:** the 830 has none — map item#→product via the SKU/item master offline; families here are inferred from UPC prefix.
- Detail on individual orders/cancellations lives in the [[01 Purchasing & Inventory/(C) EDI Retail Orders Tracker.md|EDI Retail Orders Tracker]].

*Generated 2026-08-06 from Outlook EDI mail (CVS 830 batches 6/7 → 8/2 reviewed; latest 8/2 parsed in full). Quantities reconciled line-by-line to header totals.*
