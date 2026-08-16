import os
import subprocess
import tempfile
import threading

from buddy.paths import ROOT
from buddy.speaktext import for_voice

PIPER_DIR = ROOT / "vendor" / "piper"
PIPER_BIN = PIPER_DIR / "piper"
VOICE_DIR = ROOT / "vendor" / "voices"


class Voice:
    def __init__(self, cfg):
        self.cfg = cfg
        self._client = None
        self._lock = threading.Lock()
        self._speaking = False
        self._on_end = None
        self._player = None
        self._gen = 0

    def enabled(self):
        return bool(self.cfg.get("voice"))

    def set_enabled(self, value):
        self.cfg["voice"] = bool(value)
        if not value:
            self.stop()

    def apply_character(self, spec):
        self.cfg["voice_engine"] = spec.get("voice_engine") or "speechd"
        self.cfg["voice_name"] = spec.get("voice_name")
        self.cfg["voice_model"] = spec.get("voice_model")
        self.cfg["voice_rate"] = spec.get("voice_rate", 0)
        self.cfg["voice_pitch"] = spec.get("voice_pitch", 0)
        self.close()

    def speak(self, text, on_end=None):
        if not self.enabled() or not text:
            if on_end:
                on_end()
            return False
        self.stop()
        self._gen += 1
        gen = self._gen
        self._on_end = on_end
        spoken = for_voice(text) or text
        engine = self.cfg.get("voice_engine") or "speechd"
        if engine == "piper" and PIPER_BIN.is_file():
            return self._speak_piper(spoken, gen)
        return self._speak_speechd(spoken)

    def stop(self):
        self._speaking = False
        player = self._player
        self._player = None
        if player is not None:
            try:
                player.terminate()
            except Exception:
                pass
        if self._client is not None:
            try:
                self._client.cancel()
            except Exception:
                pass

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

    def _finish(self):
        self._speaking = False
        cb = self._on_end
        self._on_end = None
        if cb:
            from gi.repository import GLib

            GLib.idle_add(cb)

    def _speak_piper(self, text, gen):
        model_name = self.cfg.get("voice_model") or "en_US-amy-medium"
        model = VOICE_DIR / f"{model_name}.onnx"
        if not model.is_file():
            return self._speak_speechd(text)
        try:
            handle, wav_path = tempfile.mkstemp(prefix="grok-buddy-", suffix=".wav")
            os.close(handle)
        except OSError:
            return self._speak_speechd(text)

        def worker():
            env = os.environ.copy()
            lib = str(PIPER_DIR)
            env["LD_LIBRARY_PATH"] = lib + (":" + env["LD_LIBRARY_PATH"] if env.get("LD_LIBRARY_PATH") else "")
            try:
                proc = subprocess.run(
                    [
                        str(PIPER_BIN),
                        "--model",
                        str(model),
                        "--output_file",
                        wav_path,
                        "--length_scale",
                        "1.05",
                        "--quiet",
                    ],
                    input=text.encode("utf-8"),
                    env=env,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
                if proc.returncode != 0 or gen != self._gen or not self._speaking:
                    return
                player = _play_wav(wav_path)
                self._player = player
                if player is not None:
                    player.wait()
            finally:
                try:
                    os.unlink(wav_path)
                except OSError:
                    pass
                if gen == self._gen and self._speaking:
                    self._finish()

        self._speaking = True
        threading.Thread(target=worker, daemon=True).start()
        return True

    def _speak_speechd(self, text):
        if not self._ensure_speechd():
            if self._on_end:
                self._on_end()
            return False
        try:
            with self._lock:
                self._speaking = True
                self._client.speak(text, self._callback)
            return True
        except Exception:
            self._speaking = False
            if self._on_end:
                self._on_end()
            return False

    def _ensure_speechd(self):
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
            name = self.cfg.get("voice_name") or "English (America)+female1"
            try:
                client.set_synthesis_voice(name)
            except Exception:
                try:
                    client.set_synthesis_voice("English (America)")
                except Exception:
                    pass
            client.set_rate(int(self.cfg.get("voice_rate", -10)))
            client.set_pitch(int(self.cfg.get("voice_pitch", 10)))
            client.set_punctuation(speechd.PunctuationMode.NONE)
            try:
                client.set_cap_let_recogn("none")
            except Exception:
                pass
            self._client = client
            return True
        except Exception:
            self._client = None
            return False

    def _callback(self, kind, *_args):
        name = str(kind).split(".")[-1].upper()
        if name in {"END", "CANCEL", "CANCELLED"}:
            self._finish()


def _play_wav(path):
    for cmd in (("pw-play", path), ("aplay", "-q", path)):
        try:
            return subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            continue
    return None
