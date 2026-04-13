# COMMANDS.md
Available skills and reusable commands for SupplyChainBrain sessions.

> Skills are stored as markdown files in `11 Skills/`. This file is the index.

---

## Skills Index

| Skill | File | Description |
|-------|------|-------------|
| *(none yet)* | — | Add skills as they're built |

---

## Common Session Prompts

### Start of session
```
git pull
```
Then open Claude and say: "Let's pick up where we left off — check CLAUDE.md Current Status."

### End of session
Tell Claude: "Session ending — update Current Status and push."
Claude will update CLAUDE.md and run:
```
git add . && git commit -m "session: <description>" && git push origin main
```

---

## Useful Claude Prompts

**Weekly supply chain review:**
> "Run the weekly supply chain check. Pull from the reports folders, flag stockouts, reorder triggers, and rebalancing needs. Save output to outputs/."

**SOP capture:**
> "I just figured out how to do [X]. Help me write an SOP for it and save it to 06 Processes & SOPs/."

**Vendor profile:**
> "Create a vendor profile for [Vendor Name]. Here's what I know: [details]."

**Demand planning:**
> "Help me analyze the forecast for [brand/SKU]. Here's the data: [paste or file path]."
