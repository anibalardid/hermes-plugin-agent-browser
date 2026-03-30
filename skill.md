---
name: agent-browser-plugin
description: Guide for using the agent-browser plugin — web navigation, element interaction, scraping, and automation
version: 1.0.0
metadata:
  hermes:
    tags: [browser, web, automation, scraping, navigation]
    category: browser
---

# Agent Browser Plugin Usage Guide

You have two browser options, in order of priority:

## OPTION 1: Hermes native browser (PRIMARY)

Available tools:
- `browser_navigate` → Open URL
- `browser_snapshot` → View content (accessibility tree with @eN refs)
- `browser_vision` → Analyze screenshot with AI (IF snapshot is not enough)
- `browser_click`, `browser_fill`, `browser_type`, `browser_press`, `browser_scroll`
- `browser_close`

**Standard flow:**
```
browser_navigate(url) → browser_snapshot() → browser_vision(question) if needed
```

## OPTION 2: agent-browser CLI (FALLBACK)

When browser_navigate fails or returns incomplete content (SPA/JavaScript), or if the user explicitly asks to "use agent-browser", use the `agent-browser` CLI:

```bash
# Open and read page
agent-browser open "<url>"
agent-browser snapshot

# Close
agent-browser close
```

**Note:** The `agent-browser` CLI is the binary that powers this plugin. If the user asks for "agent-browser", execute it via terminal.

---

## RULES

1. **Always try browser_navigate first** (faster)
2. **If content doesn't load or is incomplete, use agent-browser as fallback**
3. **If agent-browser also has issues, use execute_code + regex**

## When to use FALLBACK (agent-browser CLI)

- browser_snapshot returns only navigation/headers without article content
- Site is a SPA (Single Page App) that loads via JavaScript
- Paywall appears without actual content
- You tried browser_navigate + browser_vision and it still doesn't work
- **User explicitly asks to "use agent-browser"**

## Complete workflow with fallback

```
1. browser_navigate(url) + browser_snapshot()
2. If content incomplete:
   → agent-browser open <url> + agent-browser snapshot
3. If still not working:
   → terminal + execute_code to extract with regex from HTML
```

## Common Issues & Workarounds

### browser_navigate returns incomplete content (SPA/JavaScript)
When `browser_snapshot` returns only navigation without actual content, or paywall appears:

**Step 1:** Try `browser_vision` to analyze the screenshot directly

**Step 2:** If still not working, use `agent-browser` CLI as fallback:
```bash
agent-browser open "<url>"
agent-browser snapshot
agent-browser close
```

**Step 3:** If `agent-browser` also has issues, use `execute_code` with regex:
```python
import urllib.request, re, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=15, context=ctx).read().decode('utf-8', errors='replace')
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text)
idx = text.lower().find('keyword')
print(text[max(0,idx-500):idx+3000])
```

## Common Workflows

### Navigate and read a page
```
browser_navigate(url) → browser_snapshot() → browser_vision(question) if needed
```

### Fill and submit a form
```
browser_navigate(url) → browser_snapshot() → browser_fill(@eN, text) → browser_press("Enter") → browser_snapshot()
```

### Close browser when done
```
browser_close()
```
