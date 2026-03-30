BROWSER_OPEN = {
    "name": "browser_open",
    "description": (
        "Navigate the browser to a URL. Use this as the first step whenever you need to "
        "visit a website, load a page, or start a web automation task. "
        "After calling this, use browser_snapshot to inspect the page content."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The full URL to navigate to, including https://",
            }
        },
        "required": ["url"],
    },
}

BROWSER_SNAPSHOT = {
    "name": "browser_snapshot",
    "description": (
        "Get the current page's accessibility tree with element references (@e1, @e2, ...). "
        "This is the best way to inspect page content and find interactive elements. "
        "Use the returned refs (@eN) with browser_click, browser_fill, browser_get, etc. "
        "Call this after navigation or after interacting with the page to see the updated state."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}

BROWSER_CLICK = {
    "name": "browser_click",
    "description": (
        "Click an element on the page. Use element refs (@e1, @e2, ...) from browser_snapshot, "
        "CSS selectors (#id, .class, tag), or ARIA roles. "
        "Use for buttons, links, checkboxes, or any clickable element."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "selector": {
                "type": "string",
                "description": "Element ref (@e2), CSS selector (#submit), or text selector",
            },
            "new_tab": {
                "type": "boolean",
                "description": "If true, open the click target in a new tab",
                "default": False,
            },
        },
        "required": ["selector"],
    },
}

BROWSER_FILL = {
    "name": "browser_fill",
    "description": (
        "Clear an input field and fill it with the given text. "
        "Use for form fields, search boxes, text areas. "
        "Prefer over browser_type when you want to replace existing content entirely."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "selector": {
                "type": "string",
                "description": "Element ref (@e3), CSS selector, or ARIA locator",
            },
            "text": {
                "type": "string",
                "description": "The text to fill into the field",
            },
        },
        "required": ["selector", "text"],
    },
}

BROWSER_TYPE = {
    "name": "browser_type",
    "description": (
        "Type text into an element using real keystrokes (appends to existing content). "
        "Use when you need to simulate actual typing or when the app listens to keydown events. "
        "For replacing content, prefer browser_fill instead."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "selector": {
                "type": "string",
                "description": "Element ref or CSS selector",
            },
            "text": {
                "type": "string",
                "description": "Text to type",
            },
        },
        "required": ["selector", "text"],
    },
}

BROWSER_PRESS = {
    "name": "browser_press",
    "description": (
        "Press a keyboard key or key combination. "
        "Use after filling a form to submit it (Enter), to trigger shortcuts (Control+a, Tab), "
        "or to navigate with arrow keys."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "key": {
                "type": "string",
                "description": (
                    "Key name or combo: Enter, Tab, Escape, ArrowDown, Control+a, Shift+Tab, etc."
                ),
            }
        },
        "required": ["key"],
    },
}

BROWSER_GET = {
    "name": "browser_get",
    "description": (
        "Get information from the current page or a specific element. "
        "Use 'text' to extract readable text, 'html' for raw HTML, 'value' for input values, "
        "'title' for page title, 'url' for the current URL, or 'attr' to get an element attribute."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "what": {
                "type": "string",
                "enum": ["text", "html", "value", "title", "url", "attr", "count"],
                "description": "What to retrieve",
            },
            "selector": {
                "type": "string",
                "description": "Element ref or CSS selector. Not needed for 'title' or 'url'.",
            },
            "attr": {
                "type": "string",
                "description": "Attribute name, required when what='attr' (e.g. 'href', 'src')",
            },
        },
        "required": ["what"],
    },
}

BROWSER_FIND = {
    "name": "browser_find",
    "description": (
        "Find and interact with elements using semantic locators (role, text, label, placeholder). "
        "Use when you know the element's purpose but not its CSS selector or ref. "
        "Examples: find a button by its label, find an input by its placeholder text."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "by": {
                "type": "string",
                "enum": ["role", "text", "label", "placeholder", "alt", "testid"],
                "description": "How to locate the element",
            },
            "value": {
                "type": "string",
                "description": "The role name, text content, label, or testid to match",
            },
            "action": {
                "type": "string",
                "enum": ["click", "fill", "type", "hover", "focus", "check", "uncheck", "text"],
                "description": "What to do with the found element",
            },
            "fill_value": {
                "type": "string",
                "description": "Text to fill/type, required when action is 'fill' or 'type'",
            },
            "name": {
                "type": "string",
                "description": "Filter by accessible name (use with by='role')",
            },
            "exact": {
                "type": "boolean",
                "description": "Require exact text match",
                "default": False,
            },
        },
        "required": ["by", "value", "action"],
    },
}

BROWSER_WAIT = {
    "name": "browser_wait",
    "description": (
        "Wait for a condition before proceeding. Use after triggering an action that causes "
        "page changes (navigation, form submit, AJAX load). "
        "Can wait for: an element to appear (selector), text to appear (text), "
        "URL pattern (url), milliseconds (ms), load state (load/networkidle), "
        "or a JavaScript condition (fn)."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "selector": {
                "type": "string",
                "description": "CSS selector or ref to wait for (element becomes visible)",
            },
            "ms": {
                "type": "integer",
                "description": "Milliseconds to wait",
            },
            "text": {
                "type": "string",
                "description": "Wait until this text appears on the page",
            },
            "url": {
                "type": "string",
                "description": "Wait until current URL matches this pattern (e.g. '**/dashboard')",
            },
            "load": {
                "type": "string",
                "enum": ["load", "domcontentloaded", "networkidle"],
                "description": "Wait for a page load state",
            },
            "fn": {
                "type": "string",
                "description": "JavaScript expression that returns true when ready",
            },
            "state": {
                "type": "string",
                "enum": ["visible", "hidden", "attached", "detached"],
                "description": "Expected element state (use with selector)",
            },
        },
        "required": [],
    },
}

BROWSER_SCROLL = {
    "name": "browser_scroll",
    "description": (
        "Scroll the page or a specific element. "
        "Use 'down' to reveal more content, 'up' to go back, "
        "or provide a selector to scroll to a specific element."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "direction": {
                "type": "string",
                "enum": ["up", "down", "left", "right"],
                "description": "Scroll direction",
            },
            "pixels": {
                "type": "integer",
                "description": "How many pixels to scroll (default: 300)",
                "default": 300,
            },
            "selector": {
                "type": "string",
                "description": "Scroll within this element (optional)",
            },
        },
        "required": ["direction"],
    },
}

BROWSER_SCREENSHOT = {
    "name": "browser_screenshot",
    "description": (
        "Take a screenshot of the current page. "
        "Use to visually verify page state, capture results, or debug issues. "
        "Returns the file path of the saved screenshot."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "File path to save the screenshot (PNG). Uses a temp dir if omitted.",
            },
            "full_page": {
                "type": "boolean",
                "description": "Capture the full scrollable page, not just the viewport",
                "default": False,
            },
            "annotate": {
                "type": "boolean",
                "description": "Annotate screenshot with numbered element labels",
                "default": False,
            },
        },
        "required": [],
    },
}

BROWSER_EVAL = {
    "name": "browser_eval",
    "description": (
        "Execute arbitrary JavaScript in the page context and return the result. "
        "Use for extracting data not accessible via snapshot, "
        "checking JavaScript state, or performing complex DOM operations."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "script": {
                "type": "string",
                "description": "JavaScript code to execute. Return a value to get output.",
            }
        },
        "required": ["script"],
    },
}

BROWSER_BATCH = {
    "name": "browser_batch",
    "description": (
        "Execute multiple agent-browser commands in a single call for efficiency. "
        "Use when you have a known sequence of steps (open, snapshot, click, fill, screenshot). "
        "Faster than calling each tool individually due to avoided process startup overhead."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "commands": {
                "type": "array",
                "description": "List of commands as string arrays, e.g. [['open', 'https://example.com'], ['snapshot']]",
                "items": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "bail_on_error": {
                "type": "boolean",
                "description": "Stop execution on first error",
                "default": True,
            },
        },
        "required": ["commands"],
    },
}

BROWSER_CLOSE = {
    "name": "browser_close",
    "description": (
        "Close the browser session. Call this when the browser task is complete "
        "to release resources. Use close_all=true to close all active sessions."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "close_all": {
                "type": "boolean",
                "description": "Close all active sessions, not just current",
                "default": False,
            }
        },
        "required": [],
    },
}

ALL_SCHEMAS = [
    BROWSER_OPEN,
    BROWSER_SNAPSHOT,
    BROWSER_CLICK,
    BROWSER_FILL,
    BROWSER_TYPE,
    BROWSER_PRESS,
    BROWSER_GET,
    BROWSER_FIND,
    BROWSER_WAIT,
    BROWSER_SCROLL,
    BROWSER_SCREENSHOT,
    BROWSER_EVAL,
    BROWSER_BATCH,
    BROWSER_CLOSE,
]
