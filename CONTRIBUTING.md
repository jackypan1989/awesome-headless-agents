# Contributing

Thanks for helping keep this list sharp. Quality beats quantity.

## Before you open a PR

Confirm the tool passes the **headless test**:

- [ ] Runs unattended — no TTY, interactive prompt, or GUI step required
- [ ] Machine-readable output (JSON / NDJSON / Markdown / structured)
- [ ] Predictable failure (non-zero exit codes or explicit errors)
- [ ] Scriptable auth (env vars, token files — no forced browser login)
- [ ] Meaningful activity within the last 12 months

## Entry format

```
- [Name](link) 🆓 — One-line description, ending with a period.
```

- Use tags: 🆓 open source · 💲 paid / hosted · 🔌 has an MCP server
- Describe what it does **for an agent**, not marketing copy.
- Keep entries alphabetical within a section unless the section notes otherwise.
- One tool per PR.

## Will be rejected

- GUI-first tools with a thin CLI wrapper
- The agents themselves (Claude Code, Codex, etc.) — see Related Lists
- Abandoned or unmaintained projects
- Redundant tools where a clearly better option is already listed
