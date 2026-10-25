# Awesome Headless Agents [![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![GitHub stars](https://img.shields.io/github/stars/jackypan1989/awesome-headless-agents?style=social)](https://github.com/jackypan1989/awesome-headless-agents/stargazers)

> A curated list of tools that AI agents can operate **without a GUI** — CLIs, headless browsers, APIs, sandboxes, and MCP servers that work unattended, with no TTY and no human clicking "OK".

Most "awesome agent" lists catalog the agents themselves. This one catalogs what agents **use**: the building blocks that are legible, composable, and reliable when nobody is watching.

## Contents

- [Inclusion Criteria](#inclusion-criteria)
- [Toolchains](#toolchains)
- [Search APIs](#search-apis)
- [Web Fetch & Extraction](#web-fetch--extraction)
- [Headless Browsers](#headless-browsers)
- [Browser Automation](#browser-automation)
- [Document Conversion](#document-conversion)
- [Media & Speech](#media--speech)
- [JSON & Text Processing](#json--text-processing)
- [Data & Query](#data--query)
- [Storage & Transfer](#storage--transfer)
- [Secrets & Auth](#secrets--auth)
- [Sandboxes & Execution](#sandboxes--execution)
- [Developer Workflow](#developer-workflow)
- [Cloud & Infra CLIs](#cloud--infra-clis)
- [Notifications](#notifications)
- [MCP Servers](#mcp-servers)

## Inclusion Criteria

A tool belongs here only if it passes the **headless test**:

| Rule                     | What it means                                                                   |
| ------------------------ | ------------------------------------------------------------------------------- |
| **Runs unattended**      | Works with no TTY, no interactive prompt, no GUI step required.                 |
| **Machine-readable I/O** | Offers JSON, NDJSON, Markdown, or another structured format an agent can parse. |
| **Predictable failure**  | Non-zero exit codes / explicit errors, not silent partial success.              |
| **Scriptable auth**      | Credentials via env vars, files, or tokens; no mandatory browser login loop.    |
| **Maintained**           | Meaningful activity within the last 12 months.                                  |

Excluded: GUI-first apps with a thin CLI wrapper, the agents themselves (see [Related Lists](#related-lists)), and end-user products.

**Legend:** 🆓 open source · 💲 paid / hosted · 🔌 has an MCP server · ★ GitHub/GitLab stars, refreshed weekly

## Toolchains

Headless tools earn their place when they compose: each step reads text, writes structured output to stdout, and fails loudly. Run chains under `set -euo pipefail` so a failure anywhere stops the pipeline instead of handing the next tool empty input.

### Search → read the top results

**Tools:** Tavily → jq → Jina Reader

```sh
curl -sf https://api.tavily.com/search \
  -H "Authorization: Bearer $TAVILY_API_KEY" -H 'Content-Type: application/json' \
  -d '{"query": "headless browser for AI agents", "max_results": 3}' \
  | jq -r '.results[].url' \
  | xargs -I{} curl -sf https://r.jina.ai/{} > sources.md
```

### Web page → Markdown → matches as JSON

**Tools:** Jina Reader → ripgrep → jq

```sh
curl -sf https://r.jina.ai/https://example.com > page.md
rg --json -i 'domain' page.md \
  | jq -c 'select(.type == "match") | {line: .data.line_number, text: .data.lines.text}'
```

### Article → metadata as JSON

**Tools:** Trafilatura → jq

```sh
trafilatura -u https://simonwillison.net/2024/Dec/31/llms-in-2024/ --json --with-metadata \
  | jq '{title, author, date, chars: (.text | length)}'
```

### Any document → searchable Markdown

**Tools:** MarkItDown → ripgrep → jq

```sh
markitdown quarterly-report.pdf -o report.md
rg --json -i 'revenue' report.md | jq -c 'select(.type == "match") | .data.lines.text'
```

### Legacy CLI output → JSON

**Tools:** jc → jq

```sh
dig example.com | jc --dig | jq -r '.[].answer[].data'
```

### Codebase → TODO inventory

**Tools:** ripgrep → jq

```sh
rg --json 'TODO|FIXME' src \
  | jq -s '[.[] | select(.type == "match") | .data.path.text]
           | group_by(.) | map({file: .[0], count: length}) | sort_by(-.count)'
```

### GitHub activity → SQL

**Tools:** gh → DuckDB

```sh
gh pr list --repo cli/cli --state merged --limit 100 --json number,author,mergedAt > prs.json
duckdb -json -c "SELECT author.login AS author, count(*) AS prs FROM 'prs.json' GROUP BY 1 ORDER BY 2 DESC LIMIT 5"
```

### Remote Parquet → SQL, no download

**Tools:** DuckDB

```sh
duckdb -json -c "SELECT l_returnflag, count(*) AS n
  FROM 'https://shell.duckdb.org/data/tpch/0_01/parquet/lineitem.parquet' GROUP BY 1"
```

DuckDB reads Parquet, CSV, and JSON over HTTP(S) and S3 directly, fetching only the columns the query needs.

### Failed CI run → error lines

**Tools:** gh → ripgrep

```sh
run=$(gh run list --status failure --limit 1 --json databaseId --jq '.[0].databaseId')
gh run view "$run" --log-failed | rg '##\[error\]|Error:'
```

### Markdown links → repository health

**Tools:** ripgrep → gh → jq

```sh
rg -o 'github\.com/[^/)]+/[^/)#]+' README.md | sort -u | cut -d/ -f2- \
  | while read -r repo; do
      gh api "repos/$repo" \
        | jq -c --arg want "$repo" '{want: $want, now: .full_name, archived, pushed_at}
                                    | select(.archived or .now != .want)'
    done
```

Prints only repositories that were archived or renamed, the check this list runs on itself.

### Project tasks → JSON

**Tools:** just → jq

```sh
just --dump --dump-format json | jq -r '.recipes | to_entries[] | "\(.key)\t\(.value.doc // "")"'
```

An agent can discover what a project lets it run, with each recipe's doc comment, before running anything.

### Agent-generated code → restricted execution

**Tools:** sandbox-runtime

```sh
srt --settings srt-settings.json python3 generated.py
```

Filesystem and network access outside the allowlist in `srt-settings.json` is blocked at the OS level, so a misbehaving script fails instead of reaching your files or the internet.

## Search APIs

_Find sources. Hosted APIs that return ranked results as JSON._

- [Brave Search API](https://brave.com/search/api/) 💲 🔌 - Independent web index via API.
- [Exa](https://exa.ai) 💲 🔌 - Neural search API with content retrieval.
- [SearXNG](https://github.com/searxng/searxng) 🆓 ★ 38.8k - Self-hosted metasearch engine; its search API returns JSON with `format=json` once enabled.
- [Tavily](https://tavily.com) 💲 🔌 - Search API designed for agents and RAG.

## Web Fetch & Extraction

_Turn a URL into clean Markdown or structured data without driving a browser._

- [Crawl4AI](https://github.com/unclecode/crawl4ai) 🆓 ★ 86.3k - LLM-friendly crawler that outputs clean Markdown.
- [Crawlee](https://github.com/apify/crawlee) 🆓 ★ 26.3k - Crawling and scraping library for Node.js and Python that stores results as JSON datasets.
- [curl](https://github.com/curl/curl) 🆓 ★ 43.2k - Transfers data over HTTP and dozens of other protocols; `--fail` exits non-zero on HTTP errors and `-w '%{json}'` reports transfer details.
- [Firecrawl](https://github.com/firecrawl/firecrawl) 🆓 💲 🔌 ★ 195k - Turns websites into LLM-ready Markdown or structured data.
- [httpx](https://github.com/projectdiscovery/httpx) 🆓 ★ 10.5k - HTTP toolkit that probes URLs at scale; `-json` writes JSON Lines.
- [Jina Reader](https://github.com/jina-ai/reader) 🆓 💲 ★ 12.2k - Prefix any URL to get LLM-friendly content.
- [Katana](https://github.com/projectdiscovery/katana) 🆓 ★ 17.7k - Fast crawling and spidering framework with JSON output.
- [monolith](https://github.com/Y2Z/monolith) 🆓 ★ 15.5k - Saves a complete web page, with CSS, images, and scripts embedded, as a single HTML file.
- [Scrapy](https://github.com/scrapy/scrapy) 🆓 ★ 65k - Python crawling framework; `scrapy crawl <spider> -O items.json` writes scraped items as JSON.
- [Trafilatura](https://github.com/adbar/trafilatura) 🆓 ★ 7k - Main-text extraction from web pages; CLI and Python.
- [xh](https://github.com/ducaale/xh) 🆓 ★ 8.1k - Friendly HTTP client; scriptable alternative to curl.

## Headless Browsers

_Browser engines that run with no display._

- [Chrome Headless Shell](https://developer.chrome.com/docs/automation-and-testing/headless-chrome-shell) 🆓 - The standalone headless build of Chromium.
- [Lightpanda](https://github.com/lightpanda-io/browser) 🆓 ★ 37k - Headless browser written from scratch in Zig for AI and automation; CDP-compatible with a fraction of Chrome's memory.
- [Moli](https://github.com/lexmount/moli) 🆓 ★ 20.7k - Headless browser for AI agents written in Rust; one endpoint serves CDP, WebDriver Classic, and WebDriver BiDi.

## Browser Automation

_Drive a browser when fetching isn't enough: logins, JavaScript-heavy pages, multi-step flows._

- [agent-browser](https://github.com/vercel-labs/agent-browser) 🆓 ★ 44.6k - Browser automation CLI built for AI agents.
- [Browser Use](https://github.com/browser-use/browser-use) 🆓 ★ 119k - Makes websites accessible to AI agents.
- [Browserbase](https://www.browserbase.com) 💲 - Hosted headless browser infrastructure.
- [chromedp](https://github.com/chromedp/chromedp) 🆓 ★ 13.3k - Go library that drives Chrome over the DevTools Protocol, headless by default.
- [Playwright](https://github.com/microsoft/playwright) 🆓 🔌 ★ 98.5k - Cross-browser automation; the de facto foundation for most agent browser layers.
- [Puppeteer](https://github.com/puppeteer/puppeteer) 🆓 ★ 95.7k - JavaScript API for headless Chrome and Firefox.
- [Rod](https://github.com/go-rod/rod) 🆓 ★ 7.1k - Go driver for the Chrome DevTools Protocol with automatic waits and a headless default.
- [Selenium](https://github.com/SeleniumHQ/selenium) 🆓 ★ 34.6k - WebDriver automation for every major browser, with bindings in many languages and Selenium Grid for remote runs.
- [Skyvern](https://github.com/Skyvern-AI/skyvern) 🆓 💲 🔌 ★ 23.3k - Automates browser workflows with LLMs and computer vision through an API.
- [Stagehand](https://github.com/browserbase/stagehand) 🆓 ★ 25.8k - SDK for browser agents on top of Playwright.
- [Steel](https://github.com/steel-dev/steel-browser) 🆓 ★ 7.9k - Open-source browser API for agents with session management.

## Document Conversion

_Turn PDFs, Office files, and other formats into text an LLM can read._

- [Apache Tika](https://github.com/apache/tika) 🆓 ★ 4.1k - Detects and extracts text and metadata from over a thousand file types; `tika-app --json` prints metadata as JSON.
- [Docling](https://github.com/docling-project/docling) 🆓 ★ 69.6k - Document parsing with layout and table understanding.
- [Marker](https://github.com/datalab-to/marker) 🆓 ★ 40.6k - Converts PDFs and documents to Markdown, HTML, or JSON via `--output_format`.
- [MarkItDown](https://github.com/microsoft/markitdown) 🆓 🔌 ★ 192k - Converts Office files, PDFs, and more to Markdown for LLMs.
- [MinerU](https://github.com/opendatalab/MinerU) 🆓 ★ 82.5k - Parses PDFs into LLM-ready Markdown; `mineru parse --json` for structured output.
- [OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF) 🆓 ★ 35.1k - Adds a searchable OCR text layer to scanned PDFs; `--sidecar` writes the recognized text to a file.
- [olmOCR](https://github.com/allenai/olmocr) 🆓 ★ 19.8k - Converts PDFs and images to clean Markdown with a vision language model, keeping reading order, tables, and equations.
- [Pandoc](https://github.com/jgm/pandoc) 🆓 ★ 46.7k - Universal document converter.
- [pdfplumber](https://github.com/jsvine/pdfplumber) 🆓 ★ 10.9k - Extracts text, tables, and character positions from PDFs; the CLI emits JSON or CSV.
- [Tesseract](https://github.com/tesseract-ocr/tesseract) 🆓 ★ 77.2k - OCR engine for 100+ languages; `tsv` and hOCR output include word positions and confidence.
- [Unstructured](https://github.com/Unstructured-IO/unstructured) 🆓 💲 ★ 15.6k - Partitions PDFs, HTML, Office files, and emails into typed JSON elements for LLM pipelines.

## Media & Speech

_Download, inspect, and transcribe audio and video._

- [ExifTool](https://github.com/exiftool/exiftool) 🆓 ★ 5.2k - Reads and writes metadata in images, audio, video, and PDFs; `-json` prints it as JSON.
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) 🆓 ★ 26.1k - Whisper on CTranslate2, several times faster on CPU and GPU, with word-level timestamps.
- [FFmpeg](https://github.com/FFmpeg/FFmpeg) 🆓 ★ 65.7k - Converts and processes audio and video; `ffprobe -of json` reports stream metadata.
- [ImageMagick](https://github.com/ImageMagick/ImageMagick) 🆓 ★ 17.7k - Converts, resizes, and composites images in 200+ formats; `magick identify` and the `json:` format report image details.
- [Piper](https://github.com/OHF-Voice/piper1-gpl) 🆓 ★ 6k - Fast local neural text-to-speech that turns text arguments or stdin into WAV files.
- [whisper.cpp](https://github.com/ggml-org/whisper.cpp) 🆓 ★ 54.7k - Local speech-to-text in C/C++; `--output-json` writes timestamped transcripts.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) 🆓 ★ 202k - Downloads audio and video from thousands of sites; `-J` dumps metadata as JSON.

## JSON & Text Processing

_Filter, reshape, and search tool output inside a pipeline._

- [ast-grep](https://github.com/ast-grep/ast-grep) 🆓 ★ 16.3k - Structural code search and rewrite over syntax trees, with `--json` output.
- [dasel](https://github.com/TomWright/dasel) 🆓 ★ 8.1k - One selector syntax to query and modify JSON, YAML, TOML, XML, CSV, and more.
- [fd](https://github.com/sharkdp/fd) 🆓 ★ 44.9k - Fast `find` alternative that respects `.gitignore`; `-0` and `--exec` pipe results safely.
- [htmlq](https://github.com/mgdm/htmlq) 🆓 ★ 7.6k - Like jq for HTML: extracts elements, text, or attributes with CSS selectors.
- [jc](https://github.com/kellyjonbrazil/jc) 🆓 ★ 8.7k - Converts legacy CLI output into JSON.
- [jq](https://github.com/jqlang/jq) 🆓 ★ 35.9k - Command-line JSON processor.
- [Miller](https://github.com/johnkerl/miller) 🆓 ★ 10.1k - Like awk/sed for CSV, TSV, and JSON.
- [ripgrep](https://github.com/BurntSushi/ripgrep) 🆓 ★ 69.4k - Fast recursive search with `--json` output.
- [sd](https://github.com/chmln/sd) 🆓 ★ 7.4k - Find and replace with familiar regex syntax, as a predictable `sed` alternative for scripted edits.
- [yq](https://github.com/mikefarah/yq) 🆓 ★ 16.2k - Like jq, but for YAML, XML, and TOML.

## Data & Query

_Run SQL over files and API results without a database server._

- [ClickHouse](https://github.com/ClickHouse/ClickHouse) 🆓 💲 ★ 50.6k - Columnar analytics database; `clickhouse local` runs SQL over local or remote files with no server.
- [Datasette](https://github.com/simonw/datasette) 🆓 ★ 11.5k - Serves SQLite databases with a JSON API for every table and query.
- [Dolt](https://github.com/dolthub/dolt) 🆓 ★ 24.7k - SQL database with Git-style branches, diffs, and merges; `dolt sql -r json` returns results as JSON.
- [DuckDB](https://github.com/duckdb/duckdb) 🆓 ★ 42.5k - In-process SQL over CSV, Parquet, and JSON; `-json` output mode.
- [SQLite](https://sqlite.org) 🆓 - Embedded SQL database; `sqlite3 -json` returns structured query results.
- [sqlite-utils](https://github.com/simonw/sqlite-utils) 🆓 ★ 2.2k - Loads JSON and CSV into SQLite and runs queries that return JSON by default.
- [Steampipe](https://github.com/turbot/steampipe) 🆓 ★ 8k - Queries cloud and SaaS APIs with SQL; `--output json` for results.
- [usql](https://github.com/xo/usql) 🆓 ★ 10.2k - One CLI for PostgreSQL, MySQL, SQLite, SQL Server, and many other databases, with JSON and CSV output.

## Storage & Transfer

_Move files between local disks and cloud storage._

- [Kopia](https://github.com/kopia/kopia) 🆓 ★ 14.4k - Encrypted, deduplicated snapshots to local or cloud storage; `--json` on list commands.
- [rclone](https://github.com/rclone/rclone) 🆓 ★ 60.5k - Syncs files with dozens of cloud storage providers; `rclone lsjson` lists objects as JSON.
- [restic](https://github.com/restic/restic) 🆓 ★ 36.8k - Encrypted, deduplicated backups to local or cloud storage, with `--json` output.

## Secrets & Auth

_Hand credentials to agents without a browser login._

- [age](https://github.com/FiloSottile/age) 🆓 ★ 24.1k - Simple file encryption with small explicit keys, designed for scripting.
- [Bitwarden CLI](https://github.com/bitwarden/clients) 🆓 💲 ★ 14.1k - Password manager CLI (`bw`) with JSON output and a `BW_SESSION` token for unattended use.
- [Doppler CLI](https://github.com/DopplerHQ/cli) 🆓 💲 ★ 400 - Secrets manager CLI; `doppler run -- <cmd>` injects secrets as env vars, authenticated by a service token.
- [dotenvx](https://github.com/dotenvx/dotenvx) 🆓 ★ 5.9k - Encrypted `.env` files; `dotenvx run -- <cmd>` decrypts and injects values with a private key from the environment.
- [Infisical](https://github.com/Infisical/infisical) 🆓 💲 ★ 30k - Secrets manager; `infisical export --format=json` or `infisical run` injects secrets into a process.
- [OpenBao](https://github.com/openbao/openbao) 🆓 ★ 8.7k - Open-source fork of HashiCorp Vault for secrets management, with `-format=json` output.
- [SOPS](https://github.com/getsops/sops) 🆓 ★ 23.5k - Encrypts values inside YAML, JSON, and ENV files; `sops -d` decrypts in scripts.

## Sandboxes & Execution

_Run agent-generated code where it can't damage the host._

- [AIO Sandbox](https://github.com/agent-infra/sandbox) 🆓 🔌 ★ 6.2k - Browser, shell, file system, VS Code Server, and MCP in a single Docker container.
- [Cloudflare Sandbox SDK](https://github.com/cloudflare/sandbox-sdk) 💲 ★ 1.2k - Isolated containers on Cloudflare's network, controlled from Workers.
- [E2B](https://github.com/e2b-dev/E2B) 🆓 💲 ★ 14.6k - Secure cloud sandboxes for running AI-generated code.
- [microsandbox](https://github.com/superradcompany/microsandbox) 🆓 ★ 8.8k - Local-first microVM runtime for running untrusted code.
- [Modal](https://github.com/modal-labs/modal-client) 💲 ★ 528 - Programmatic containers with optional GPUs via Modal Sandboxes.
- [OpenSandbox](https://github.com/opensandbox-group/OpenSandbox) 🆓 ★ 16.2k - Self-hosted sandbox runtime for AI agents.
- [sandbox-runtime](https://github.com/anthropics/sandbox-runtime) 🆓 ★ 6.6k - OS-level filesystem and network restrictions for any process, no container required.
- [Vercel Sandbox](https://github.com/vercel/sandbox) 💲 ★ 215 - Ephemeral Firecracker microVMs for untrusted code, with SDK and CLI.

### Isolation Primitives

_Lower-level isolation that sandboxes like the ones above are built on._

- [bubblewrap](https://github.com/containers/bubblewrap) 🆓 ★ 9.2k - Unprivileged Linux sandboxing tool used by Flatpak.
- [Firecracker](https://github.com/firecracker-microvm/firecracker) 🆓 ★ 37.6k - Lightweight microVM monitor behind AWS Lambda and several agent sandboxes.
- [gVisor](https://github.com/google/gvisor) 🆓 ★ 19.8k - User-space application kernel that isolates containers from the host.
- [nsjail](https://github.com/google/nsjail) 🆓 ★ 4.2k - Process isolation with Linux namespaces, cgroups, rlimits, and seccomp-bpf filters.

## Developer Workflow

_Operate repositories, CI, and project tasks from the command line._

- [act](https://github.com/nektos/act) 🆓 ★ 72.4k - Runs GitHub Actions workflows locally in containers, with `--json` log output.
- [Dagger](https://github.com/dagger/dagger) 🆓 💲 ★ 16.5k - Runs build and test pipelines as code in containers, the same way locally and in CI.
- [gh](https://github.com/cli/cli) 🆓 🔌 ★ 46.7k - GitHub CLI with `--json` and `--jq` on most commands.
- [glab](https://gitlab.com/gitlab-org/cli) 🆓 ★ 1.1k - GitLab CLI with JSON output.
- [hyperfine](https://github.com/sharkdp/hyperfine) 🆓 ★ 29.2k - Command-line benchmarking with warmups and statistics; `--export-json` saves results.
- [just](https://github.com/casey/just) 🆓 ★ 36.4k - Command runner; `just --list` lets agents discover project tasks.
- [mise](https://github.com/jdx/mise) 🆓 ★ 35.4k - Pins tool versions, env vars, and tasks per project; `mise ls --json` lists installed tools.
- [pre-commit](https://github.com/pre-commit/pre-commit) 🆓 ★ 15.7k - Runs a repo's configured hooks; `pre-commit run --all-files` checks everything in one command.
- [Task](https://github.com/go-task/task) 🆓 ★ 16.3k - YAML-based task runner; `task --list --json` lets agents discover tasks.
- [uv](https://github.com/astral-sh/uv) 🆓 ★ 91.2k - Fast Python package manager; `uvx` runs any Python CLI in a throwaway environment.

## Cloud & Infra CLIs

_Provision and inspect infrastructure with machine-readable plans and state._

- [AWS CLI](https://github.com/aws/aws-cli) 🆓 ★ 17.3k - Command-line interface for AWS; `--output json` and `--query` on every command.
- [Azure CLI](https://github.com/Azure/azure-cli) 🆓 ★ 4.7k - Command-line interface for Azure; `--output json` and JMESPath `--query` on every command.
- [doctl](https://github.com/digitalocean/doctl) 🆓 ★ 3.5k - DigitalOcean CLI; `-o json` on every command and an access token from the environment.
- [flyctl](https://github.com/superfly/flyctl) 🆓 ★ 1.7k - Deploys and manages Fly.io apps; `--json` output and `FLY_API_TOKEN` auth.
- [Helm](https://github.com/helm/helm) 🆓 ★ 30.4k - Kubernetes package manager; `helm list -o json` and `helm template` render manifests without a cluster.
- [kubectl](https://github.com/kubernetes/kubectl) 🆓 ★ 3.4k - Kubernetes CLI; `-o json` returns full resource objects.
- [OpenTofu](https://github.com/opentofu/opentofu) 🆓 ★ 30.6k - Open-source Terraform fork; `tofu plan -json` and `tofu show -json` for machine-readable plans.
- [Pulumi](https://github.com/pulumi/pulumi) 🆓 💲 ★ 25.8k - Infrastructure as code in general-purpose languages; `pulumi preview --json` shows planned changes.
- [Wrangler](https://github.com/cloudflare/workers-sdk) 🆓 ★ 4.7k - Cloudflare Workers CLI for deploys, D1, KV, and R2, authenticated by `CLOUDFLARE_API_TOKEN`.

## Notifications

_Report results back to humans when the job is done._

- [Apprise](https://github.com/caronc/apprise) 🆓 ★ 17.6k - One CLI and API for notifications to Slack, Discord, email, SMS, and many more services.
- [Himalaya](https://github.com/pimalaya/himalaya) 🆓 ★ 7.5k - Reads, searches, and sends email over IMAP and SMTP, with JSON output for scripts.
- [ntfy](https://github.com/binwiederhier/ntfy) 🆓 💲 ★ 35.1k - Push notifications to phone or desktop with a plain HTTP POST; self-hostable.

## MCP Servers

_Standalone servers that expose a tool over the Model Context Protocol. Tools that ship their own MCP server are also tagged 🔌 above._

- [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) 🆓 ★ 54.1k - Chrome DevTools for agents: debugging, performance traces, and automation, with a `--headless` option.
- [Context7](https://github.com/upstash/context7) 🆓 💲 ★ 63.7k - Up-to-date, version-specific library documentation for LLMs.
- [GitHub MCP Server](https://github.com/github/github-mcp-server) 🆓 ★ 33.9k - Official GitHub MCP server.
- [MCP Reference Servers](https://github.com/modelcontextprotocol/servers) 🆓 ★ 91.6k - Official reference servers for filesystem, Git, fetch, memory, and more.
- [Playwright MCP](https://github.com/microsoft/playwright-mcp) 🆓 ★ 38.6k - Browser automation via accessibility snapshots.

## Related Lists

- [awesome-agent-native-services](https://github.com/haoruilee/awesome-agent-native-services) ★ 325 - Services designed for agents from the ground up.
- [awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents) ★ 30.6k - Directory of AI agents.
- [awesome-cli-coding-agents](https://github.com/bradAGI/awesome-cli-coding-agents) ★ 1.4k - Terminal-native coding agents.

## Contributing

Contributions welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) first; every entry must pass the headless test above.

## Footnotes

This list is released under CC0 1.0. See [LICENSE](LICENSE).

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)
