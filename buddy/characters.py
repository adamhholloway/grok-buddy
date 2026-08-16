CHARACTERS = {
    "buddy": {
        "id": "buddy",
        "label": "Buddy",
        "voice_name": "English (America)+male1",
        "voice_rate": -12,
        "voice_pitch": -6,
    },
    "annie": {
        "id": "annie",
        "label": "Annie",
        "voice_name": "English (America)+female1",
        "voice_rate": -10,
        "voice_pitch": 10,
    },
}

DEFAULT_CHARACTER = "annie"


def resolve(name):
    if name in CHARACTERS:
        return CHARACTERS[name]
    return CHARACTERS[DEFAULT_CHARACTER]
