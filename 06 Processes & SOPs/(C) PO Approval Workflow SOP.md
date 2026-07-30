---
type: sop
topic: PO approval workflow (US)
owner: Tom Sapia (SCM)
created: 2026-07-30
scope: US POs — current process (international may differ)
---

# (C) PO Approval Workflow — US (Harry / Ningbo Zeyu)

The full lifecycle from SAP entry to a live, signed PO with the supplier. Drives the **[[01 Purchasing & Inventory/(C) PO Tracker — Harry (Ningbo Zeyu)]]** stage column.

## The steps

| # | Step | Who | Detail |
|---|---|---|---|
| **1** | **Enter the PO in SAP** | Tom | Verify **quantities** and set the **dates** (see date math below). **No pricing on the PO** — we are **DDP with Harry**, so price does not go on our PO. |
| **2** | **Send PO → Harry** | Tom → Harry | Email the PO to Harry. |
| **3** | **Receive PI ← Harry** | Harry → Tom | Harry returns the Proforma Invoice. |
| **4** | **Review / adjust** | Tom (↔ Harry) | Check the PI; if items/info need changing, ask Harry to revise. Loop until correct. |
| **5** | **Run the PPO Validator** | Tom | Load the **PO + PI** into the validator tool and confirm they match. Tool: `C:\Users\Tom Sapia\OneDrive - michaeltoddbeauty.com\Desktop\Web Apps\PPO Validator.html` |
| **6** | **Send to approvers** | Tom → Lilia, Donna, Supply Chain | Send the **PDF (PO + PI)** to Lilia, Donna, and Supply Chain. |
| **7** | **Approve → Michael** | Lilia **or** Donna | Approver forwards the document to **Michael** (Tom attached/cc'd) for signature. |
| **8** | **Signed → back to Harry** | Michael → Tom → Harry | Michael signs; Tom emails the **approved & signed** document back to Harry → **PO is LIVE**. |

## SAP date math (step 1)
Build the SAP **delivery window** date by stacking from the **PO posting date**:

| Leg | Days | Running total |
|---|---:|---:|
| Production (posting → ready) | **~40** | ~40 |
| Ocean transit | **~45** | ~85 |
| Receiving into destination (landed → put away where needed) | **~40** | **~125** |

→ The **later (~125-day) date** goes in SAP's **delivery window**. (This is the door-to-usable timeline; ties to the ~140-day supplier lead-time floor used in the planners.)

## Rules that bite if missed
- **No pricing on the PO** — DDP with Harry (price omitted on purpose).
- **Michael's signature is the authoritative "signed"** (step 8), not Tom's send.
- Step 4 can loop (PI revisions) before validation/approval.
- **This is the US process "at the moment"** — international / other vendors may differ; revisit as they're documented.

## People
| Role | Who |
|---|---|
| Vendor | **Harry Zhan** — Ningbo Zeyu (harryzhan@nb-zeyu.com) |
| Buyer / owner | **Tom Sapia** — SCM |
| Approvers | **Lilia** and **Donna** (either) |
| Dist list | **Supply Chain** (supplychain@michaeltoddbeauty.com) |
| Final signer | **Michael Friend** — President & CEO |

## Tracker stage legend
`① SAP entered → ② PO→Harry → ③ PI←Harry → ④ adjusting → ⑤ validated → ⑥ with approvers → ⑦ approved (to Michael) → ⑧ signed→Harry = LIVE`
