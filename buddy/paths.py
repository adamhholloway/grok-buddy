import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
RAW = ASSETS / "raw"
SPRITES = ASSETS / "sprites"
HOOKS = ROOT / "hooks"

CONFIG_DIR = Path.home() / ".config" / "grok-buddy"
CONFIG_PATH = CONFIG_DIR / "config.json"

RUNTIME_DIR = Path(os.environ.get("XDG_RUNTIME_DIR", f"/tmp/grok-buddy-{os.getuid()}"))
SOCKET_PATH = RUNTIME_DIR / "grok-buddy.sock"

POSES = (
    "idle",
    "blink",
    "talk",
    "wave",
    "think",
    "work",
    "celebrate",
    "sad",
    "sleep",
    "alert",
    "look_left",
    "look_right",
    "point",
    "lean",
    "step",
)

WALK_POSES = ("step", "lean", "wave", "idle")
FIDGET_POSES = ("look_left", "look_right", "think", "point", "wave", "lean")
SHOW_POSES = (
    "idle",
    "wave",
    "think",
    "point",
    "look_left",
    "look_right",
    "lean",
    "step",
    "celebrate",
    "alert",
    "work",
    "sad",
)
NO_FLIP = {"look_left", "look_right"}


def raw_dir(character):
    return RAW / character


def sprite_dir(character):
    return SPRITES / character
