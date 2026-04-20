# 3PL Reference
**Last updated:** April 20, 2026

Quick reference for the three fulfillment nodes currently active across MTB, SS, and NFMD.

---

## ShipBob

**Role:** DTC + non-Amazon order fulfillment (Shopify, Walmart, TikTok Shop, Nordstrom)

**Locations:**
| Facility | State |
|----------|-------|
| Sparks | NV |
| Philadelphia / Bethlehem | PA |
| Ontario / Moreno Valley | CA |
| Buford / Fairburn | GA |
| (additional) | TX |

**OTIF Target:** 95%

**Status note:** Possible transition to AmzPrep — not finalized as of April 2026. Do not update 3PL routing or SOPs until confirmed.

**Key contacts:**
- Account Manager: TBD
- Email: TBD
- Portal: app.shipbob.com

**Notes:**
- Inventory rebalancing between ShipBob locations happens internally — not a manual process
- Flag aging inventory at any single FC if DOS > 90 at that node while other FCs are low

---

## Floship

**Role:** International fulfillment — orders outside the US

**Locations:** TBD (international FCs — confirm in Floship portal)

**Key contacts:**
- Account Manager: TBD
- Email: TBD
- Portal: TBD

**Notes:**
- Rebalancing trigger: if ShipBob DOS > 45 on a SKU while Floship DOS < 14 on the same SKU → initiate transfer
- Reverse logic also applies: if Floship is overstocked while ShipBob is low, pull from Floship
- International compliance, customs, duties — separate process, see `05 International Expansion/`

---

## Amazon AWD (Amazon Warehousing & Distribution)

**Role:** Amazon bulk storage + automated FBA replenishment

**Brands using AWD:** NFMD (primary), some MTB

**How it works:** Send inventory to AWD. Amazon automatically replenishes FBA as needed based on demand signals. Lower FBA storage fees vs. standard FBA.

**Key trigger:** When FBA DOS drops below the lead time threshold, check AWD levels before placing a new PO. If AWD has enough stock, create FBA send-in (not a PO).

**Notes:**
- AWD stock is counted in DOS formula: `DOS = (FBA Stock + AWD Stock) ÷ Adj. Velocity`
- If FBA = 0 and AWD > 0 → AMAZON STOCKOUT (not a true stockout) — replenish FBA from AWD
- If FBA = 0 and AWD = 0 → TRUE STOCKOUT — new PO needed

---

## Rebalancing Logic

**ShipBob ↔ Floship:**
| Condition | Action |
|-----------|--------|
| ShipBob DOS > 45 AND Floship DOS < 14 (same SKU) | Transfer stock from ShipBob to Floship |
| Floship DOS > 45 AND ShipBob DOS < 14 (same SKU) | Transfer stock from Floship to ShipBob |

**AWD ↔ FBA:**
| Condition | Action |
|-----------|--------|
| FBA = 0, AWD > 0 | Create FBA send-in — do not place new PO |
| FBA = 0, AWD = 0 | TRUE STOCKOUT — place PO |
| FBA DOS < lead time, AWD stock available | Send AWD → FBA to avoid FBA stockout |

**Priority for rebalancing:** A items and high-velocity SKUs first. Use ABC classification from item master.

---

## 3PL Contacts (Fill In)

| 3PL | Role | Contact | Email | Phone |
|-----|------|---------|-------|-------|
| ShipBob | DTC Fulfillment | TBD | TBD | TBD |
| Floship | Intl Fulfillment | TBD | TBD | TBD |
| Amazon AWD | Bulk Storage/FBA | N/A (portal) | N/A | N/A |

---

## Notes
- OTIF = On-Time In-Full. Flag any 3PL consistently missing 95% OTIF to DOS.
- ShipBob → AmzPrep transition: if confirmed, this note needs a full update including new location list and contact info.
- All 3PL-related SOPs go in this folder: `03 3PL & Fulfillment/`
