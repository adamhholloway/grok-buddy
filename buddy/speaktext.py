import re

_CODE = re.compile(r"[`*#_~]+")
_SLASH_CMD = re.compile(r"/(?P<cmd>[a-z][\w-]*)")
_PATH = re.compile(r"~/?\.[\w./-]+")
_DASH = re.compile(r"[—–]+")
_MULTI_SPACE = re.compile(r"\s+")


def for_voice(text):
    """Make on-screen copy speakable. espeak will otherwise read punctuation aloud."""
    if not text:
        return ""
    spoken = text
    spoken = _SLASH_CMD.sub(lambda m: m.group("cmd").replace("-", " "), spoken)
    spoken = _PATH.sub("that folder", spoken)
    spoken = _CODE.sub("", spoken)
    spoken = spoken.replace("Ctrl+L", "control L")
    spoken = spoken.replace("Ctrl+", "control ")
    spoken = spoken.replace("`rm`", "R M")
    spoken = spoken.replace("rm -rf", "R M dash R F")
    spoken = _DASH.sub(", ", spoken)
    spoken = spoken.replace("…", ",")
    spoken = spoken.replace("...", ",")
    spoken = spoken.replace("/", " ")
    spoken = spoken.replace("\\", " ")
    spoken = spoken.replace("@", " at ")
    spoken = spoken.replace("&", " and ")
    spoken = spoken.replace("%", " percent")
    spoken = spoken.replace("→", " to ")
    spoken = _MULTI_SPACE.sub(" ", spoken).strip()
    return spoken
