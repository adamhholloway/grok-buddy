import json
from copy import deepcopy

from buddy.paths import CONFIG_DIR, CONFIG_PATH

DEFAULTS = {
    "voice": True,
    "idle_tips": True,
    "idle_seconds": 240,
    "x": None,
    "y": None,
    "scale": 1.0,
    "welcomed": False,
    "character": "annie",
    "voice_engine": "piper",
    "voice_model": "en_US-amy-medium",
    "voice_name": "English (America)+female1",
    "voice_rate": -10,
    "voice_pitch": 10,
}


def load():
    data = deepcopy(DEFAULTS)
    if CONFIG_PATH.exists():
        try:
            saved = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            if isinstance(saved, dict):
                data.update(saved)
        except (OSError, json.JSONDecodeError):
            pass
    return data


def save(data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
