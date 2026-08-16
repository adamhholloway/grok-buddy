CHARACTERS = {
    "buddy": {
        "id": "buddy",
        "label": "Buddy",
        "voice_name": "English (America)+Tweaky",
        "voice_rate": 12,
        "voice_pitch": 35,
    },
    "annie": {
        "id": "annie",
        "label": "Annie",
        "voice_name": "English (America)+Annie",
        "voice_rate": 18,
        "voice_pitch": 50,
    },
}

DEFAULT_CHARACTER = "annie"


def resolve(name):
    if name in CHARACTERS:
        return CHARACTERS[name]
    return CHARACTERS[DEFAULT_CHARACTER]
