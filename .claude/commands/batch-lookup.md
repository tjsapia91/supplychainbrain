---
description: Search the Prizm batch export (in the vault) by batch code / item # / UPC / PPO #. Replaces the external Batch Code Lookup web app.
argument-hint: "<batch code | item # | UPC | PPO #>  e.g. NFMD03152026X or 850038082574 or 3265"
---

# /batch-lookup — search batch codes in the brain

Look up `$ARGUMENTS` in the Prizm batch-tracking export that lives in the vault. This is the in-brain replacement for the external Batch Code Lookup web app — no outside files.

## Steps
1. Find the newest CSV in `01 Purchasing & Inventory/_batch-data/` (Glob `*.csv`, pick most recent). If none, tell Tom to drop the Prizm export there and stop.
2. Read it (Bash/Grep). Prizm exports have title/date rows above the header — the real header row is the one containing keywords like item / upc / sku / batch / lot / ppo / region / date / qty / desc. Detect it, then treat rows below as data.
3. Match `$ARGUMENTS` case-insensitively across ALL columns (batch code, item #, UPC, PPO #, description, region…). Support partial matches. If multiple terms, AND them.
4. Return a compact table of the matches (batch code · item/UPC · description · PPO# · region · date · qty — whatever columns exist), newest/most-relevant first. If >40 matches, show the first 40 and the count, and suggest narrowing.
5. If the query looks like a salt code, cross-reference the conventions in [[01 Purchasing & Inventory/(C) Batch Code Tracker]] (RGS/XYS prefixes, legacy codes, 5-yr exp) and note it.

Read-only — never modify the CSV. For efficiency, prefer `Grep` over reading the whole file when the query is a specific code.
