# _ppo-validate — PO + PI drop folder

Drop the **PO (PPO) PDF** and the vendor's **PI PDF** here (name each with the PO number,
e.g. `PPO3276.pdf` + `PI-3276.pdf`). Then run **`/ppo-validate 3276`**.

Full in-brain replacement for the PPO/PI Validator web app: **validates** (item #s,
quantities, master-carton qty, full-carton multiples, order pairing, buyer/address/incoterm,
vendor) **and merges** the PO + PI into one packet `PPO<num>-PO-PI.pdf` (via `_merge.py` /
PyMuPDF, PO first). Nothing external needed.
