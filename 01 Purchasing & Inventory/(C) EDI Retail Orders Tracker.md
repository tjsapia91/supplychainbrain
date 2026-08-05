---
type: edi-order-tracker
source: EDI service — edisupport@ecom-specialist.com (→ supplychain@michaeltoddbeauty.com)
last_scanned: 2026-08-03
status: living
---

# 🛒 EDI Retail Orders Tracker

How retail partners submit and adjust orders. Each EDI email = a retail PO or a change to one. Tracked in the brain (previously nearly lost in inbox noise). Companion to the local **MTB Tools** web-app suite.

## EDI transaction types
| Set | Meaning |
|---|---|
| **850** | New Purchase Order |
| **860** | PO Change — with a *Transaction Set Purpose Code*: **STATUS UPDATE** (revision) or **CANCELLATION** |
| 855 / 856 / 810 | Ack / ASN / Invoice (if/when they appear) |

## Fields captured per EDI PO
Retailer · Brand · **PO #** · Type (New / Change-update / Change-cancel) · PO date · **Delivery requested date** · Ship-to (store/DC code) · Buyer · Line items (Purchaser Item Code · UPC · description · qty in **cases** · pack · unit $ · line $) · change action (e.g. DELETE ITEM(S)).

## Open EDI POs

### CVS — SPA 830 Planning Schedule (FORECAST, 2026-08-02 — 3 msgs)
| Doc | Vendor ID | Horizon | Detail |
|---|---|---|---|
| **830** ×3 | 40287 · 40867 · 36143 | **10/25/2026** | **Now the CVS forecast of record** — buyer Tristan Viens-Roderick (8/3): *"refer to your EDI 830 reports for forecasting."* Weekly planning qtys per DC. |

**✅ AIVA (item 732452 / UPC 8500031156…) PARSED from the 8/2 830 (Tommy 2026-08-05):**

| Qty | Week window | CVS DC |
|---:|---|---|
| 48 | 8/30–9/05 | N101 |
| 36 | 9/13–9/19 | L101 |
| 48 | 9/20–9/26 | N101 |
| 24 | 10/18–10/24 | F101 |
| **156 total** | through late Oct | N101 (96) · L101 (36) · F101 (24) |

> **NOT the September door-restore** — the 8/2 830 forecasts only ~156u of AIVA (all "Planning"/flexible weekly), basically the same low state as the 7/26 batch, **not** a 2,738-door reset. The initial 4-WOS DC buildup (already bought) covered the door restore; the 830 is just the ongoing trickle. No large one-time AIVA fill owed via EDI.

### CVS — SPA 812 Credit/Debit Adjustments (2026-08-03)
| Doc | Amount | Detail |
|---|---|---|
| 2655218WV | **$200.98 credit** | Off-invoice deduction vs 6/25 invoice → AR |
| 2657148WV | **$200.98 credit** | Off-invoice deduction vs 6/26 invoice → AR |

### CVS — SPA (2026-07-30 batch, 860 changes — 10 messages)
| PO # | Type | PO date | Delivery req | Change detail |
|---|---|---|---|---|
| **4848476** | 860 · status update | 7/28 | 8/20 | DELETE 2 cs — MIO Microdermabrasion MT (UPC 860021001130, pack 12, $205.08/cs, line $410) |
| **6682921** | 860 · **CANCELLATION** | 7/28 | — | ⚠ order cancelled — verify nothing already shipped/committed |
| **0626546** | 860 · **CANCELLATION** | 7/28 | — | ⚠ order cancelled — verify |
| 9494842 | 860 · status update | 7/28 | — | (parse line detail on next run) |
| 8353116 | 860 · status update | 7/28 | — | (parse line detail) |
| 9038477 | 860 · status update | 7/28 | — | (parse line detail) |
| 3825067 | 860 · status update | 7/28 | — | (parse line detail) |
| 5081927 | 860 · status update | 7/28 | — | (parse line detail) |
| 1661358 | 860 · status update | 7/28 | — | (parse line detail) |
| 2501262 | 860 · status update | 7/28 | — | (parse line detail) |

**Action:** confirm the 2 cancellations (6682921, 0626546) are handled; skim the status-update revised qtys.

### JCPenney — SPA
> ⚠ **JCP orders/returns come by DIRECT EMAIL (Victoria Ernst / Mary Ann Cederberg @jcp.com), NOT EDI.** Only JCP **820** (remittance) + **812** (credit/debit) flow through the EDI service. Log JCP POs here manually.

**🟠 OPEN PO — MIO Green (852 green) · deliver 8/10/2026**
- **Item:** `850003115139` MIO Green w/USB · **Qty 252** · **Deliver by 8/10/26** (Tom 8/3)
- **Source:** direct email, tail of **DI 32186678 / RA #RA18667807232026** — JCP returned the original green PO (we'd said "no longer shipping green"), then re-issued (7/27 "300 of the green" → 7/31 "new PO for 248"). Current live qty per Tom = **252**.
- **⚠ Must be TRUE GREEN**, not the commingled green/white (`850003115139` base = mix; `850003115139 - 1` = true green). JCP rejected the commingle before. The **de-kit WRO 388151795** (1,167u) is separating true green → that's the source.
- **Coverage:** 252 « on-hand ~1,626 + 1,167 de-kit green → qty is fine. **Constraints: (1) confirm de-kit done / enough true green picked; (2) ship from ShipBob→JCP DC by ~8/6–8/7 to hit 8/10; (3) confirm sales/ops actually agreed to supply green again (don't re-trip the "no longer shipping green" issue).**

| Doc | Type | Detail |
|---|---|---|
| 2 msgs | **812 · credit/debit** | 7/09 + 6/22 off-invoice adjustments (JCP.com vendor #169623) → AR |
| — | **820 · remittance/payment** | $167.56 (7/30) + $109.95 (7/23) ACH credits → AR |

---
*Auto-built from Outlook 2026-07-30 (sender edisupport@ecom-specialist.com). The email routine parses each 850/860 into this table — full line detail extracted when the run opens the body. Cancellations are always surfaced to the top; routine status-updates roll up as a batch.*
