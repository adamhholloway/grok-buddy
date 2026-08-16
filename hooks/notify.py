#!/usr/bin/env python3
"""Grok Build hook client — forwards lifecycle events to Grok Buddy."""

import json
import os
import socket
import sys
from pathlib import Path


def socket_path():
    runtime = os.environ.get("XDG_RUNTIME_DIR", f"/tmp/grok-buddy-{os.getuid()}")
    return str(Path(runtime) / "grok-buddy.sock")


def main():
    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    try:
        event = json.loads(raw)
    except json.JSONDecodeError:
        return 0
    if not isinstance(event, dict):
        return 0

    slim = {
        "hookEventName": event.get("hookEventName") or event.get("event"),
        "cwd": event.get("cwd"),
        "toolName": event.get("toolName"),
        "notificationType": event.get("notificationType") or event.get("notification"),
        "reason": event.get("reason"),
        "sessionId": event.get("sessionId"),
    }
    payload = json.dumps({"type": "event", "event": slim}, separators=(",", ":")).encode("utf-8")
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        sock.sendto(payload, socket_path())
    except OSError:
        pass
    finally:
        sock.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
