# SharePoint Migration Guide
**Purpose:** Move the SupplyChainBrain vault from a local machine to SharePoint so the whole team can access it.
**Last updated:** April 21, 2026

---

## Step 1 — Create the SharePoint folder

1. Go to your team's SharePoint site
2. Create a new folder: `SupplyChainBrain` (or `SC Team Brain` — whatever fits your naming)
3. Place it somewhere the supply chain team already has access (e.g., your team's document library)

---

## Step 2 — Sync SharePoint to your local machine

1. In SharePoint, click **Sync** (top toolbar)
2. This opens OneDrive and creates a local synced copy at:
   `C:\Users\Tom Sapia\[Company Name]\SupplyChainBrain\`
3. Confirm the folder appears in File Explorer under OneDrive

---

## Step 3 — Move the vault

1. Copy the entire contents of:
   `C:\Users\Tom Sapia\supplychainbrain\`
   into the new SharePoint-synced folder
2. Wait for OneDrive sync to complete (check tray icon — should show checkmarks)

---

## Step 4 — Update Obsidian vault path

1. Open Obsidian
2. Bottom left → **Open another vault** → **Open folder as vault**
3. Point it at the new SharePoint-synced path
4. Confirm everything looks right

---

## Step 5 — Update Claude Code working directory

Update your Claude Code project to point at the new vault path:
- Old: `C:\Users\Tom Sapia\supplychainbrain`
- New: `C:\Users\Tom Sapia\[Company Name]\SupplyChainBrain\` *(confirm exact OneDrive path)*

---

## Step 6 — Set up each team member

For each person on the team:

1. **Install Obsidian** (free — obsidian.md)
2. **Sync the SharePoint folder** to their machine via OneDrive (same Step 2 above)
3. **Open vault in Obsidian:** Open folder as vault → point at their local OneDrive path
4. **They're in.** Real-time sync through SharePoint.

---

## Step 7 — Set SharePoint permissions

In SharePoint folder settings:
- **Tommy:** Edit (full read/write)
- **DOS:** Edit (full read/write)
- **Other team members:** Edit or View depending on their role
- **SVP Ops:** View (read-only, or Edit if they'll contribute)

---

## Conflict prevention rules (important)

SharePoint sync creates conflict copies if two people edit the same file at the same time.

**How to avoid:**
- Each person edits **only their own `[Name].md` file** in project folders
- `Overview.md` and `Log.md` — one person edits at a time
- Don't have two people in the same note simultaneously

---

## After migration

- Update `CLAUDE.md` with the new vault path
- Run `git remote` — decide if you still want GitHub backup (recommended yes)
- Old local vault can be archived or deleted after confirming everything synced correctly

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| OneDrive shows sync errors | Check file names for special characters (`#`, `%`, `&`) — SharePoint doesn't allow them |
| Obsidian shows broken links | Vault path changed — re-open vault from new location |
| Conflict copies appearing | Two people edited same file — merge manually, delete conflict copy |
| Team member can't see files | Check SharePoint permissions — must be granted access to the folder |
