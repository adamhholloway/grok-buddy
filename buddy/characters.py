CHARACTERS = {
    "buddy": {
        "id": "buddy",
        "label": "Buddy",
        "voice_engine": "speechd",
        "voice_name": "English (America)+male1",
        "voice_rate": -12,
        "voice_pitch": -6,
        "sprite_height": 210,
    },
    "annie": {
        "id": "annie",
        "label": "Annie",
        "voice_engine": "piper",
        "voice_model": "en_US-amy-medium",
        "voice_name": "English (America)+female1",
        "voice_rate": -10,
        "voice_pitch": 10,
        "voice_length": 1.05,
        "sprite_height": 300,
    },
    "miku": {
        "id": "miku",
        "label": "Hatsune Miku",
        "voice_engine": "piper",
        "voice_model": "en_US-amy-medium",
        "voice_name": "English (America)+female1",
        "voice_rate": 8,
        "voice_pitch": 35,
        "voice_length": 0.86,
        "sprite_height": 300,
    },
    "faye": {
        "id": "faye",
        "label": "Faye Valentine",
        "voice_engine": "piper",
        "voice_model": "en_US-amy-medium",
        "voice_name": "English (America)+female1",
        "voice_rate": -18,
        "voice_pitch": -4,
        "voice_length": 1.08,
        "sprite_height": 300,
    },
    "frieren": {
        "id": "frieren",
        "label": "Frieren",
        "voice_engine": "piper",
        "voice_model": "en_US-amy-medium",
        "voice_name": "English (America)+female1",
        "voice_rate": -22,
        "voice_pitch": -10,
        "voice_length": 1.14,
        "sprite_height": 300,
    },
}

DEFAULT_CHARACTER = "annie"


def resolve(name):
    if name in CHARACTERS:
        return CHARACTERS[name]
    return CHARACTERS[DEFAULT_CHARACTER]
