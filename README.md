# Awesome Headless Agents [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of tools that AI agents can operate **without a GUI** — CLIs, headless browsers, APIs, sandboxes, and MCP servers that work unattended, with no TTY and no human clicking "OK".

Most "awesome agent" lists catalog the agents themselves. This one catalogs what agents **use**: the building blocks that are legible, composable, and reliable when nobody is watching.

## Contents

- [Inclusion Criteria](#inclusion-criteria)
- [Headless Browsers](#headless-browsers)
- [Browser Automation for Agents](#browser-automation-for-agents)
- [Web Fetch & Extraction](#web-fetch--extraction)
- [Search APIs](#search-apis)
- [Document Conversion](#document-conversion)
- [Data & Query](#data--query)
- [Structured Output CLIs](#structured-output-clis)
- [Dev Platform CLIs](#dev-platform-clis)
- [Sandboxes & Execution](#sandboxes--execution)
- [MCP Servers](#mcp-servers)
- [Related Lists](#related-lists)

## Inclusion Criteria

A tool belongs here only if it passes the **headless test**:

1. **Runs unattended** — works with no TTY, no interactive prompt, no GUI step required.
2. **Machine-readable I/O** — offers JSON, NDJSON, Markdown, or another structured format an agent can parse.
3. **Predictable failure** — non-zero exit codes / explicit errors, not silent partial success.
4. **Scriptable auth** — credentials via env vars, files, or tokens; no mandatory browser login loop.
5. **Maintained** — meaningful activity within the last 12 months.

Excluded: GUI-first apps with a thin CLI wrapper, the agents themselves (see [Related Lists](#related-lists)), and end-user products.

**Legend:** 🆓 open source · 💲 paid / hosted · 🔌 has an MCP server

## Headless Browsers

- [Lightpanda](https://github.com/lightpanda-io/browser) 🆓 — Headless browser written from scratch in Zig for AI and automation; CDP-compatible with a fraction of Chrome's memory.
- [Chrome Headless Shell](https://developer.chrome.com/docs/automation-and-testing/headless-chrome-shell) 🆓 — The standalone headless build of Chromium.

## Browser Automation for Agents

- [agent-browser](https://github.com/vercel-labs/agent-browser) 🆓 — Browser automation CLI built for AI agents.
- [Browser Use](https://github.com/browser-use/browser-use) 🆓 — Makes websites accessible to AI agents.
- [Stagehand](https://github.com/browserbase/stagehand) 🆓 — SDK for browser agents on top of Playwright.
- [Playwright](https://github.com/microsoft/playwright) 🆓 🔌 — Cross-browser automation; the de facto foundation for most agent browser layers.
- [Puppeteer](https://github.com/puppeteer/puppeteer) 🆓 — JavaScript API for headless Chrome and Firefox.
- [Steel](https://github.com/steel-dev/steel-browser) 🆓 — Open-source browser API for agents with session management.
- [Browserbase](https://www.browserbase.com) 💲 — Hosted headless browser infrastructure.

## Web Fetch & Extraction

- [Crawl4AI](https://github.com/unclecode/crawl4ai) 🆓 — LLM-friendly crawler that outputs clean Markdown.
- [Firecrawl](https://github.com/firecrawl/firecrawl) 🆓 💲 🔌 — Turns websites into LLM-ready Markdown or structured data.
- [Trafilatura](https://github.com/adbar/trafilatura) 🆓 — Main-text extraction from web pages; CLI and Python.
- [Jina Reader](https://github.com/jina-ai/reader) 🆓 💲 — Prefix any URL to get LLM-friendly content.
- [Katana](https://github.com/projectdiscovery/katana) 🆓 — Fast crawling and spidering framework with JSON output.

## Search APIs

- [Tavily](https://tavily.com) 💲 🔌 — Search API designed for agents and RAG.
- [Exa](https://exa.ai) 💲 🔌 — Neural search API with content retrieval.
- [Brave Search API](https://brave.com/search/api/) 💲 🔌 — Independent web index via API.

## Document Conversion

- [MarkItDown](https://github.com/microsoft/markitdown) 🆓 🔌 — Converts Office files, PDFs, and more to Markdown for LLMs.
- [Docling](https://github.com/docling-project/docling) 🆓 — Document parsing with layout and table understanding.
- [Pandoc](https://github.com/jgm/pandoc) 🆓 — Universal document converter.

## Data & Query

- [DuckDB](https://github.com/duckdb/duckdb) 🆓 — In-process SQL over CSV, Parquet, and JSON; `-json` output mode.
- [SQLite](https://sqlite.org) 🆓 — `sqlite3 -json` for structured query results.
- [Miller](https://github.com/johnkerl/miller) 🆓 — Like awk/sed for CSV, TSV, and JSON.

## Structured Output CLIs

- [jq](https://github.com/jqlang/jq) 🆓 — Command-line JSON processor.
- [yq](https://github.com/mikefarah/yq) 🆓 — jq for YAML, XML, and TOML.
- [jc](https://github.com/kellyjonbrazil/jc) 🆓 — Converts legacy CLI output into JSON.
- [ripgrep](https://github.com/BurntSushi/ripgrep) 🆓 — Fast recursive search with `--json` output.
- [xh](https://github.com/ducaale/xh) 🆓 — Friendly HTTP client; scriptable alternative to curl.

## Dev Platform CLIs

- [gh](https://github.com/cli/cli) 🆓 🔌 — GitHub CLI with `--json` and `--jq` on most commands.
- [glab](https://gitlab.com/gitlab-org/cli) 🆓 — GitLab CLI with JSON output.
- [just](https://github.com/casey/just) 🆓 — Command runner; `just --list` lets agents discover project tasks.

## Sandboxes & Execution

- [AIO Sandbox](https://github.com/agent-infra/sandbox) 🆓 🔌 — Browser, shell, file system, VS Code Server, and MCP in a single Docker container.
- [Cloudflare Sandbox SDK](https://github.com/cloudflare/sandbox-sdk) 💲 — Isolated containers on Cloudflare's network, controlled from Workers.
- [E2B](https://github.com/e2b-dev/E2B) 🆓 💲 — Secure cloud sandboxes for running AI-generated code.
- [microsandbox](https://github.com/superradcompany/microsandbox) 🆓 — Local-first microVM runtime for running untrusted code.
- [Modal](https://github.com/modal-labs/modal-client) 💲 — Programmatic containers with optional GPUs via Modal Sandboxes.
- [OpenSandbox](https://github.com/opensandbox-group/OpenSandbox) 🆓 — Self-hosted sandbox runtime for AI agents.
- [Runloop](https://github.com/runloopai/api-client-python) 💲 — Devboxes where agents run code, edit files, and expose ports.
- [sandbox-runtime](https://github.com/anthropics/sandbox-runtime) 🆓 — OS-level filesystem and network restrictions for any process, no container required.
- [Vercel Sandbox](https://github.com/vercel/sandbox) 💲 — Ephemeral Firecracker microVMs for untrusted code, with SDK and CLI.

## MCP Servers

- [Playwright MCP](https://github.com/microsoft/playwright-mcp) 🆓 — Browser automation via accessibility snapshots.
- [GitHub MCP Server](https://github.com/github/github-mcp-server) 🆓 — Official GitHub MCP server.

## Related Lists

- [awesome-agent-cli](https://github.com/agentablesh/awesome-agent-cli) — CLI tools suited for agent workflows.
- [awesome-agent-native-services](https://github.com/haoruilee/awesome-agent-native-services) — Services designed for agents from the ground up.
- [awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents) — Directory of AI agents.
- [awesome-cli-coding-agents](https://github.com/bradAGI/awesome-cli-coding-agents) — Terminal-native coding agents.

## Contributing

Contributions welcome — read [CONTRIBUTING.md](CONTRIBUTING.md) first. Every entry must pass the [headless test](#inclusion-criteria).

## License

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)
