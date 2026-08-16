import json
import os
import socket
import sys

from buddy.paths import RUNTIME_DIR, SOCKET_PATH


def send(message):
    payload = json.dumps(message, separators=(",", ":")).encode("utf-8")
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        sock.sendto(payload, str(SOCKET_PATH))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def send_cli(argv):
    if not argv:
        return 2
    cmd = argv[0]
    if cmd == "say":
        text = " ".join(argv[1:]).strip()
        if not text:
            print("usage: grok-buddy say <text>", file=sys.stderr)
            return 2
        ok = send({"type": "say", "text": text, "mood": "talk"})
    elif cmd == "tip":
        ok = send({"type": "tip"})
    elif cmd == "joke":
        ok = send({"type": "joke"})
    elif cmd in {"grok", "open"}:
        ok = send({"type": "grok"})
    elif cmd == "dance":
        ok = send({"type": "dance"})
    elif cmd == "sing":
        ok = send({"type": "sing"})
    elif cmd == "trick":
        ok = send({"type": "trick"})
    elif cmd == "wander":
        ok = send({"type": "wander"})
    elif cmd == "pose":
        ok = send({"type": "pose"})
    elif cmd == "time":
        ok = send({"type": "time"})
    elif cmd == "follow":
        flag = (argv[1].lower() if len(argv) > 1 else "on")
        ok = send({"type": "follow", "on": flag not in {"off", "0", "false", "stop"}})
    elif cmd == "hide":
        ok = send({"type": "hide"})
    elif cmd == "wake":
        ok = send({"type": "wake"})
    elif cmd == "quit":
        ok = send({"type": "quit"})
    elif cmd == "mood":
        if len(argv) < 2:
            print("usage: grok-buddy mood <name>", file=sys.stderr)
            return 2
        ok = send({"type": "mood", "mood": argv[1]})
    elif cmd == "character":
        if len(argv) < 2:
            print("usage: grok-buddy character <buddy|annie|miku>", file=sys.stderr)
            return 2
        ok = send({"type": "character", "character": argv[1]})
    elif cmd == "event":
        raw = sys.stdin.read() if len(argv) < 2 else argv[1]
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            return 0
        ok = send({"type": "event", "event": payload})
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        return 2
    if not ok:
        print("Grok Buddy is not running.", file=sys.stderr)
        return 1
    return 0


class Bus:
    def __init__(self, on_message):
        self.on_message = on_message
        self.sock = None

    def start(self):
        RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
        if SOCKET_PATH.exists():
            try:
                SOCKET_PATH.unlink()
            except OSError:
                pass
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        sock.bind(str(SOCKET_PATH))
        try:
            os.chmod(SOCKET_PATH, 0o600)
        except OSError:
            pass
        sock.setblocking(False)
        self.sock = sock
        from gi.repository import GLib

        GLib.io_add_watch(sock, GLib.IO_IN, self._readable)

    def close(self):
        if self.sock is not None:
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None
        if SOCKET_PATH.exists():
            try:
                SOCKET_PATH.unlink()
            except OSError:
                pass

    def _readable(self, _source, _condition):
        if self.sock is None:
            return False
        try:
            data = self.sock.recv(65535)
        except OSError:
            return True
        try:
            message = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return True
        if isinstance(message, dict):
            self.on_message(message)
        return True
