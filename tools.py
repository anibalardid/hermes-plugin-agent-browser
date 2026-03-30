import json
import os
import shutil
import subprocess
from typing import Any


def _bin() -> str:
    """Resolve agent-browser binary path."""
    custom = os.environ.get("AGENT_BROWSER_BIN")
    if custom:
        return custom
    found = shutil.which("agent-browser")
    if not found:
        raise RuntimeError(
            "agent-browser not found in PATH. "
            "Install it with: npm install -g agent-browser && agent-browser install"
        )
    return found


def _run(*args: str) -> str:
    """Run agent-browser with given args, return stdout as string."""
    cmd = [_bin(), *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout.strip()
    if result.returncode != 0:
        err = result.stderr.strip() or output
        raise RuntimeError(err)
    return output


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

def browser_open(args: dict, **kwargs) -> str:
    try:
        url = args["url"]
        output = _run("open", url)
        return json.dumps({"ok": True, "output": output})
    except Exception as e:
        return json.dumps({"error": str(e)})


def browser_snapshot(args: dict, **kwargs) -> str:
    try:
        output = _run("snapshot")
        return json.dumps({"ok": True, "snapshot": output})
    except Exception as e:
        return json.dumps({"error": str(e)})


def browser_click(args: dict, **kwargs) -> str:
    try:
        selector = args["selector"]
        cmd_args = ["click", selector]
        if args.get("new_tab"):
            cmd_args.append("--new-tab")
        output = _run(*cmd_args)
        return json.dumps({"ok": True, "output": output})
    except Exception as e:
        return json.dumps({"error": str(e)})


def browser_fill(args: dict, **kwargs) -> str:
    try:
        output = _run("fill", args["selector"], args["text"])
        return json.dumps({"ok": True, "output": output})
    except Exception as e:
        return json.dumps({"error": str(e)})


def browser_type(args: dict, **kwargs) -> str:
    try:
        output = _run("type", args["selector"], args["text"])
        return json.dumps({"ok": True, "output": output})
    except Exception as e:
        return json.dumps({"error": str(e)})


def browser_press(args: dict, **kwargs) -> str:
    try:
        output = _run("press", args["key"])
        return json.dumps({"ok": True, "output": output})
    except Exception as e:
        return json.dumps({"error": str(e)})


def browser_get(args: dict, **kwargs) -> str:
    try:
        what = args["what"]
        if what in ("title", "url"):
            output = _run("get", what)
        elif what == "attr":
            output = _run("get", "attr", args["selector"], args["attr"])
        else:
            output = _run("get", what, args["selector"])
        return json.dumps({"ok": True, "value": output})
    except Exception as e:
        return json.dumps({"error": str(e)})


def browser_find(args: dict, **kwargs) -> str:
    try:
        cmd_args = ["find", args["by"], args["value"], args["action"]]
        fill_value = args.get("fill_value")
        if fill_value:
            cmd_args.append(fill_value)
        if args.get("name"):
            cmd_args += ["--name", args["name"]]
        if args.get("exact"):
            cmd_args.append("--exact")
        output = _run(*cmd_args)
        return json.dumps({"ok": True, "output": output})
    except Exception as e:
        return json.dumps({"error": str(e)})


def browser_wait(args: dict, **kwargs) -> str:
    try:
        if args.get("ms") is not None:
            output = _run("wait", str(args["ms"]))
        elif args.get("text"):
            output = _run("wait", "--text", args["text"])
        elif args.get("url"):
            output = _run("wait", "--url", args["url"])
        elif args.get("load"):
            output = _run("wait", "--load", args["load"])
        elif args.get("fn"):
            output = _run("wait", "--fn", args["fn"])
        elif args.get("selector"):
            cmd_args = ["wait", args["selector"]]
            if args.get("state"):
                cmd_args += ["--state", args["state"]]
            output = _run(*cmd_args)
        else:
            return json.dumps({"error": "Provide at least one wait condition"})
        return json.dumps({"ok": True, "output": output})
    except Exception as e:
        return json.dumps({"error": str(e)})


def browser_scroll(args: dict, **kwargs) -> str:
    try:
        direction = args["direction"]
        cmd_args = ["scroll", direction]
        if args.get("pixels"):
            cmd_args.append(str(args["pixels"]))
        if args.get("selector"):
            cmd_args += ["--selector", args["selector"]]
        output = _run(*cmd_args)
        return json.dumps({"ok": True, "output": output})
    except Exception as e:
        return json.dumps({"error": str(e)})


def browser_screenshot(args: dict, **kwargs) -> str:
    try:
        cmd_args = ["screenshot"]
        if args.get("path"):
            cmd_args.append(args["path"])
        if args.get("full_page"):
            cmd_args.append("--full")
        if args.get("annotate"):
            cmd_args.append("--annotate")
        output = _run(*cmd_args)
        return json.dumps({"ok": True, "path": output})
    except Exception as e:
        return json.dumps({"error": str(e)})


def browser_eval(args: dict, **kwargs) -> str:
    try:
        output = _run("eval", args["script"])
        return json.dumps({"ok": True, "result": output})
    except Exception as e:
        return json.dumps({"error": str(e)})


def browser_batch(args: dict, **kwargs) -> str:
    try:
        commands: list[list[str]] = args["commands"]
        payload = json.dumps(commands)
        cmd = [_bin(), "batch", "--json"]
        if args.get("bail_on_error", True):
            cmd.append("--bail")
        result = subprocess.run(
            cmd,
            input=payload,
            capture_output=True,
            text=True,
        )
        output = result.stdout.strip()
        if result.returncode != 0:
            err = result.stderr.strip() or output
            return json.dumps({"error": err})
        return json.dumps({"ok": True, "output": output})
    except Exception as e:
        return json.dumps({"error": str(e)})


def browser_close(args: dict, **kwargs) -> str:
    try:
        cmd_args = ["close"]
        if args.get("close_all"):
            cmd_args.append("--all")
        output = _run(*cmd_args)
        return json.dumps({"ok": True, "output": output})
    except Exception as e:
        return json.dumps({"error": str(e)})
