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
| **830** ×3 | 40287 · 40867 · 36143 | **10/25/2026** | **Now the CVS forecast of record** — buyer Tristan Viens-Roderick (8/3): *"refer to your EDI 830 reports for forecasting."* Weekly planning qtys per DC. **⚠ Parse for AIVA (buyer item 732452) reset qty** — this is where the September door-restore demand shows up (830 = Planning Schedule With Release Capability). Earlier 7/26 batch had AIVA at ~180u (old 187-door state); check if the 8/2 batch reflects the 2,738-door reset. |

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

### JCPenney — SPA (2026-07-30)
| Doc | Type | Detail |
|---|---|---|
| — | **820 · remittance/payment** | Payment to MTB SPA: **$167.56 credit** via ACH (remittance information only). No order action — route to AR (`ar@michaeltoddbeauty.com` was CC'd). |

---
*Auto-built from Outlook 2026-07-30 (sender edisupport@ecom-specialist.com). The email routine parses each 850/860 into this table — full line detail extracted when the run opens the body. Cancellations are always surfaced to the top; routine status-updates roll up as a batch.*
