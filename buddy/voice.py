import threading


class Voice:
    def __init__(self, cfg):
        self.cfg = cfg
        self._client = None
        self._lock = threading.Lock()
        self._speaking = False
        self._on_end = None

    def enabled(self):
        return bool(self.cfg.get("voice"))

    def set_enabled(self, value):
        self.cfg["voice"] = bool(value)
        if not value:
            self.stop()

    def apply_character(self, spec):
        self.cfg["voice_name"] = spec["voice_name"]
        self.cfg["voice_rate"] = spec["voice_rate"]
        self.cfg["voice_pitch"] = spec["voice_pitch"]
        self.close()

    def speak(self, text, on_end=None):
        if not self.enabled() or not text:
            if on_end:
                on_end()
            return False
        self._on_end = on_end
        if not self._ensure():
            if on_end:
                on_end()
            return False
        try:
            with self._lock:
                self._speaking = True
                self._client.speak(text, self._callback)
            return True
        except Exception:
            self._speaking = False
            if on_end:
                on_end()
            return False

    def stop(self):
        client = self._client
        if client is None:
            return
        try:
            client.cancel()
        except Exception:
            pass
        self._speaking = False

    def close(self):
        self.stop()
        client = self._client
        self._client = None
        if client is None:
            return
        try:
            client.close()
        except Exception:
            pass

    def _ensure(self):
        if self._client is not None:
            return True
        try:
            import speechd
        except ImportError:
            return False
        try:
            client = speechd.SSIPClient("grok-buddy")
            client.set_output_module("espeak-ng")
            client.set_language("en-US")
            name = self.cfg.get("voice_name") or "English (America)+Annie"
            try:
                client.set_synthesis_voice(name)
            except Exception:
                try:
                    client.set_synthesis_voice("English (America)")
                except Exception:
                    pass
            client.set_rate(int(self.cfg.get("voice_rate", 12)))
            client.set_pitch(int(self.cfg.get("voice_pitch", 35)))
            client.set_punctuation(speechd.PunctuationMode.SOME)
            self._client = client
            return True
        except Exception:
            self._client = None
            return False

    def _callback(self, kind, *_args):
        name = str(kind).split(".")[-1].upper()
        if name in {"END", "CANCEL", "CANCELLED"}:
            self._speaking = False
            cb = self._on_end
            self._on_end = None
            if cb:
                from gi.repository import GLib

                GLib.idle_add(cb)
