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

You have 14 browser tools. Always start with `browser_open` + `browser_snapshot` before interacting with anything.

## Tool Selection

**"Go to / open / navigate to [url]"** → `browser_open`
**"What's on the page? / read the page / inspect"** → `browser_snapshot` (returns accessibility tree with @eN refs)
**"Click [button/link/element]"** → `browser_click` with `@eN` ref from snapshot
**"Fill in / type in [field]"** → `browser_fill` (replaces content) or `browser_type` (appends)
**"Press Enter / Tab / Escape"** → `browser_press`
**"Get the text / title / URL / value"** → `browser_get`
**"Find a button by name / find input by label"** → `browser_find` (semantic locators, no selector needed)
**"Wait for page to load / wait for element"** → `browser_wait`
**"Scroll down / scroll up"** → `browser_scroll`
**"Take a screenshot"** → `browser_screenshot`
**"Run JavaScript"** → `browser_eval`
**"Do multiple steps at once"** → `browser_batch` (faster, avoids per-command startup overhead)
**"Close / quit the browser"** → `browser_close`

## IMPORTANT: Only these 14 tools exist

`browser_open`, `browser_snapshot`, `browser_click`, `browser_fill`, `browser_type`,
`browser_press`, `browser_get`, `browser_find`, `browser_wait`, `browser_scroll`,
`browser_screenshot`, `browser_eval`, `browser_batch`, `browser_close`

Do NOT try to call any other tool names.

## Rules

1. **Always snapshot first.** After `browser_open` or any action that changes the page, call `browser_snapshot` to see the current state and get fresh `@eN` refs.
2. **Use refs, not guesses.** Prefer `@eN` refs from the snapshot over CSS selectors or text. Refs are stable for the current page state.
3. **Wait after navigation.** After clicking a link or submitting a form, use `browser_wait` before snapshotting again.
4. **Use `browser_find` for semantic elements.** When you know a button's label or an input's placeholder, `browser_find` is more reliable than CSS selectors.
5. **Use `browser_batch` for known sequences.** When you have a predictable multi-step flow (open → fill → click → screenshot), batch them for efficiency.
6. **Use `browser_fill` over `browser_type`** unless the app specifically requires keystroke events (autocomplete dropdowns, etc.).
7. **Don't screenshot unnecessarily.** Only call `browser_screenshot` when the user asks to see something visually.
8. **Always close when done.** Call `browser_close` at the end of a task to release resources.

## Common Workflows

### Navigate and read a page
```
browser_open(url) → browser_snapshot() → browser_get(what="text", selector="@e1")
```

### Fill and submit a form
```
browser_open(url) → browser_snapshot() → browser_fill(@eN, text) → browser_press("Enter") → browser_wait(load="networkidle") → browser_snapshot()
```

### Click a button by label (no snapshot needed)
```
browser_find(by="role", value="button", action="click", name="Submit")
```

### Extract a value from a page
```
browser_open(url) → browser_snapshot() → browser_get(what="text", selector="@eN")
```

### Login to a site
```
browser_open(url) → browser_snapshot() →
browser_find(by="label", value="Email", action="fill", fill_value="user@example.com") →
browser_find(by="label", value="Password", action="fill", fill_value="...") →
browser_press("Enter") → browser_wait(url="**/dashboard")
```

### Batch example (fast multi-step)
```
browser_batch(commands=[
  ["open", "https://example.com"],
  ["snapshot"],
  ["fill", "@e3", "search term"],
  ["press", "Enter"],
  ["wait", "--load", "networkidle"],
  ["screenshot", "/tmp/result.png"]
])
```

## Selector Formats

| Format | Example | When to use |
|--------|---------|-------------|
| `@eN` ref | `@e5` | Best — from snapshot, stable for current state |
| CSS selector | `#submit`, `.btn` | When ref not available |
| `browser_find` | `by="role"` + `value="button"` | When you know the element's purpose, not its ref |

## Notes on `browser_get`

- `what="title"` and `what="url"` don't need a selector
- `what="attr"` requires both `selector` and `attr` (e.g. `attr="href"`)
- `what="count"` returns the number of elements matching the selector
