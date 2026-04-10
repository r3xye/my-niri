#!/usr/bin/env python3

import json
import subprocess
import threading
import time


def _focused_window_present():
    try:
        proc = subprocess.run(
            ["niri", "msg", "--json", "focused-window"],
            capture_output=True,
            text=True,
            check=False,
            timeout=0.5,
        )
    except Exception:
        return None

    if proc.returncode != 0 or not proc.stdout.strip():
        return None

    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None

    response = payload.get("Ok", {})
    if "FocusedWindow" not in response:
        return None
    return response["FocusedWindow"] is not None


def _focus_guard(proc):
    saw_layer_shell_focus = False

    while proc.poll() is None:
        focused_window_present = _focused_window_present()
        if focused_window_present is False:
            saw_layer_shell_focus = True
        elif saw_layer_shell_focus and focused_window_present is True:
            proc.terminate()
            return
        time.sleep(0.12)


def run_wofi_menu(command, input_text):
    proc = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    watcher = threading.Thread(target=_focus_guard, args=(proc,), daemon=True)
    watcher.start()

    stdout, _stderr = proc.communicate(input_text)
    if proc.returncode != 0:
        return None
    return stdout.strip() or None
