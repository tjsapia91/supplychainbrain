# _ppo-validate — PO + PI drop folder

Drop the **PO (PPO) PDF** and the vendor's **PI PDF** here (name each with the PO number,
e.g. `PPO3276.pdf` + `PI-3276.pdf`). Then run **`/ppo-validate 3276`**.

In-brain replacement for the PPO/PI Validator web app's **validation** step (item #s,
quantities, master-carton qty, full-carton multiples, order pairing, buyer/address/incoterm,
vendor). It does NOT merge the two PDFs into one (no PDF-merge in the vault) — do the merge
step in the web app if you still need the combined file.
