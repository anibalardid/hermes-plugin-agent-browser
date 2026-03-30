"""Hermes agent-browser plugin.

Wraps the agent-browser CLI (Vercel Labs) to give Hermes 14 browser tools
for web navigation, element interaction, scraping, and automation.

Requires: agent-browser installed and in PATH (or AGENT_BROWSER_BIN set).
  npm install -g agent-browser && agent-browser install
"""

import logging
import shutil
from pathlib import Path

from . import schemas
from . import tools

logger = logging.getLogger(__name__)

_PLUGIN_DIR = Path(__file__).parent


def _install_skill():
    """Copy bundled skill.md to ~/.hermes/skills/ on first load."""
    try:
        from hermes_cli.config import get_hermes_home
        dest = get_hermes_home() / "skills" / "agent-browser-plugin" / "SKILL.md"
    except Exception:
        dest = Path.home() / ".hermes" / "skills" / "agent-browser-plugin" / "SKILL.md"

    source = _PLUGIN_DIR / "skill.md"
    if not source.exists() or dest.exists():
        return

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)
    logger.info("Installed agent-browser-plugin skill to %s", dest)


def register(ctx):
    """Register all 14 agent-browser tools."""

    schema_map = {s["name"]: s for s in schemas.ALL_SCHEMAS}

    _tool_handlers = {
        "browser_open": tools.browser_open,
        "browser_snapshot": tools.browser_snapshot,
        "browser_click": tools.browser_click,
        "browser_fill": tools.browser_fill,
        "browser_type": tools.browser_type,
        "browser_press": tools.browser_press,
        "browser_get": tools.browser_get,
        "browser_find": tools.browser_find,
        "browser_wait": tools.browser_wait,
        "browser_scroll": tools.browser_scroll,
        "browser_screenshot": tools.browser_screenshot,
        "browser_eval": tools.browser_eval,
        "browser_batch": tools.browser_batch,
        "browser_close": tools.browser_close,
    }

    for name, handler in _tool_handlers.items():
        ctx.register_tool(
            name=name,
            toolset="browser",
            schema=schema_map[name],
            handler=handler,
        )

    _install_skill()

    logger.info("agent-browser plugin loaded: %d tools", len(_tool_handlers))
