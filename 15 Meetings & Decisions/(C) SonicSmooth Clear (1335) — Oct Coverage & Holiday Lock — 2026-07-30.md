---
type: decision-note
topic: SonicSmooth Clear (811573031335) — October ShipBob coverage + Amazon holiday lock
sku: "811573031335"
brand: MTB
owner: Tom Sapia (SCM)
created: 2026-07-30
context: SVP flagged coverage; question was Unis→ShipBob transfer to cover Oct stockout
---

# (C) SonicSmooth Clear (1335) — Oct Coverage & Holiday Lock

**SKU:** 811573031335 · SONICSMOOTH – CLEAR REPLACEMENT KIT (8 BLADES) · ASIN B0D1GQRNRV · Class A · MTB
**Question:** How many units to move from **Unis (Amazon reservoir) → ShipBob** to mitigate the October ShipBob stockout?
**Answer:** **Zero.** Don't touch Unis. Pull ShipBob's own container **PO 3221** forward — the goods have been ready since 7/18. That closes October and keeps Amazon's holiday buffer intact.

---

## The constraint that drives everything
- **Amazon has hard deadlines:** meet the September + October cutoffs, and **Black Friday + Christmas must be locked in the Amazon network by the ~10/28 October cutoff.** After that, nothing new lands in time for the holiday.
- **ShipBob has NO deadline** — a short gap there is recoverable backorder days, not a lost peak.

→ Priority: **protect Amazon's Unis stock for the holiday. Fix ShipBob without robbing it.**

## Amazon side — Unis is fully committed to the holiday
| | Units |
|---|---|
| In-network now (FBA 6,180 + AWD 24,816 + inbound 2,192) | 33,188 |
| Burn Jul 30 → 10/28 | −25,733 |
| In-network on 10/28 (no Unis) | 7,455 |
| **+ all Unis (13,950) sent in before cutoff** | **21,405** |
| Holiday need from that stock (Oct 29 → Dec 31 = BF + Christmas) | 19,869 |
| **Surplus** | **~1,535** (goes **negative** with any January buffer) |

**PO 3263 (30,000u) lands 11/05 — after the 10/28 wall — so it does NOT count for the holiday.**
→ **Send all 13,950 Unis into the Amazon network before 10/28. Treat it as untouchable.**
→ Keep AWD→FBA transfers aggressive (FBA only ~22 days; AWD feeding ~265/day vs ~284/day demand).

## ShipBob side — fix October by pulling PO 3221 forward
ShipBob ends September ~9,000u; October demand ~24,000 → report shows end-October **−14,252**. The Oct-4 container is what's meant to cover it.

| PO | Units | Dest | Goods READY | Scheduled LOAD | Pullable? |
|---|---|---|---|---|---|
| **3221** | 25,050 | ShipBob | **7/18** ("Harry received PO 07/01") | 8/20 | ✅ **Yes — ready ~1 mo before load** |
| 3244 | 25,050 | ShipBob | 8/21 | 8/20 | ⛔ Goods not ready until late Aug |

**Already in transit / landing before the gap:** PO 3148 (18,600u, WHSE delv 8/11) · PO 3184 (10,050u, WHSE delv 8/25).

→ **THE ASK TO HARRY:** *"Load PO 3221 now — it's been ready since 7/18."* Comparable containers run ~40 days door-to-door, so loading now lands it **~mid-September** vs Oct 4 — ahead of ShipBob's ~Oct-10 depletion. 25,050u > the ~14k gap, with margin. **No Unis touched.**

## Open items
1. **PO 3263 (30,000u) destination conflict** — SAP warehouse = **SBGA-MT (ShipBob)**; Container Plan destination = **UNCA-MTB (Unis/Amazon)**; Amazon report read it as Unis. Confirm the true destination — if it's ShipBob-bound it helps the **December ShipBob gap**, not Amazon's holiday.
2. **December ShipBob gap** (~−14k) stands regardless of the 3221 pull — needs its own PO.

## Bottom line
- **Amazon 1335:** send all Unis (13,950) in before 10/28 — committed to BF + Christmas.
- **ShipBob 1335:** transfer **0 from Unis**; pull **PO 3221** forward (load now) to cover October.
- **Next:** confirm 3263 destination; size the December ShipBob PO.
