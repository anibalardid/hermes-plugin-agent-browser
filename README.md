# hermes-agent-browser-plugin

A [Hermes Agent](https://github.com/NousResearch/hermes-agent) plugin for headless browser automation using [agent-browser](https://github.com/vercel-labs/agent-browser) (Vercel Labs) — a fast native Rust CLI.

## Install

```bash
cd ~/.hermes/plugins
git clone git@github.com:anibalardid/hermes-plugin-agent-browser.git agent-browser
```

## Validate (enable or disable)
```bash
hermes plugins list
```

Restart Hermes — the plugin loads automatically. Verify with `/plugins`.

## Prerequisites

`agent-browser` must be installed and available in your PATH before loading the plugin.

### Option 1 — npm (recommended)

```bash
npm install -g agent-browser
agent-browser install   # downloads Chrome for Testing (first time only)
```

### Option 2 — Homebrew (macOS)

```bash
brew install agent-browser
agent-browser install
```

### Option 3 — Cargo (Rust)

```bash
cargo install agent-browser
agent-browser install
```

### Linux — additional system dependencies

```bash
agent-browser install --with-deps
```

## Configuration

### Custom binary path

If `agent-browser` is not in your `PATH`, set the `AGENT_BROWSER_BIN` environment variable:

```bash
export AGENT_BROWSER_BIN=/usr/local/bin/agent-browser
```

Add to your shell profile (`~/.zshrc`, `~/.bashrc`) to persist it.

### Hermes environment

If you use a `.env` file with Hermes, add:

```env
AGENT_BROWSER_BIN=/path/to/agent-browser   # optional, only if not in PATH
```

## Tools

| Tool | Description |
|------|-------------|
| `browser_open` | Navigate to a URL |
| `browser_snapshot` | Get accessibility tree with `@eN` element refs |
| `browser_click` | Click element by ref, CSS selector, or ARIA |
| `browser_fill` | Clear and fill an input field |
| `browser_type` | Type with real keystrokes (appends to content) |
| `browser_press` | Press a key or combination (Enter, Tab, Control+a) |
| `browser_get` | Extract text, html, value, title, url, or attribute |
| `browser_find` | Locate by role, label, text, placeholder, or testid |
| `browser_wait` | Wait for element, text, URL, load state, or JS condition |
| `browser_scroll` | Scroll up/down/left/right |
| `browser_screenshot` | Take a screenshot (returns file path) |
| `browser_eval` | Execute JavaScript in the page context |
| `browser_batch` | Run multiple commands in a single fast call |
| `browser_close` | Close the browser session |

## Usage

Ask Hermes naturally:

```
open https://news.ycombinator.com and show me the top 5 headlines
go to github.com/vercel-labs/agent-browser and get the README text
fill out the contact form at example.com with my name and email, then submit it
take a screenshot of https://example.com
```

Or reference tools directly:

```
use browser_open with url=https://example.com, then browser_snapshot
```

## How it works

Each tool wraps a `agent-browser` CLI command via `subprocess`. The accessibility tree (`browser_snapshot`) returns `@eN` refs that can be passed directly to `browser_click`, `browser_fill`, etc. — no fragile CSS selectors needed.

For multi-step flows, `browser_batch` pipes a JSON command array to `agent-browser batch --json`, avoiding per-command process startup overhead.

## File Structure

```
~/.hermes/plugins/agent-browser/
├── plugin.yaml     # Hermes plugin manifest
├── __init__.py     # register(ctx) — wires 14 tools + installs skill
├── schemas.py      # Tool schemas (what the LLM sees)
├── tools.py        # Handler implementations (subprocess wrappers)
├── skill.md        # Usage guide installed to ~/.hermes/skills/
└── README.md
```

## Troubleshooting

**`agent-browser not found in PATH`**
Install it (`npm install -g agent-browser`) or set `AGENT_BROWSER_BIN=/path/to/binary`.

**`agent-browser install` fails**
Make sure you have internet access. On Linux, run `agent-browser install --with-deps` to get system dependencies.

**Browser doesn't open / crashes**
Run `agent-browser open https://example.com` manually to verify the installation works outside Hermes.

**Permission denied on binary**
```bash
chmod +x $(which agent-browser)
```

## Requirements

- `agent-browser` CLI in PATH (or `AGENT_BROWSER_BIN` set)
- No additional Python dependencies

## License

MIT
