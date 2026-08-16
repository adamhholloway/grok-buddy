import os
import shutil
import subprocess
from pathlib import Path


def grok_bin():
    env_path = shutil.which("grok")
    candidates = [
        Path.home() / ".grok" / "bin" / "grok",
        Path(env_path) if env_path else None,
    ]
    for path in candidates:
        if path and path.is_file() and os.access(path, os.X_OK):
            return path
    return None


def open_grok(cwd=None):
    binary = grok_bin()
    if binary is None:
        return False, "I can't find Grok Build. Is it installed?"
    cwd = str(Path(cwd).expanduser() if cwd else Path.home())
    env = os.environ.copy()
    grok_dir = str(binary.parent)
    path_parts = env.get("PATH", "").split(":")
    if grok_dir not in path_parts:
        env["PATH"] = grok_dir + ":" + env.get("PATH", "")
    env.pop("GDK_BACKEND", None)

    gnome = shutil.which("gnome-terminal")
    fallback = shutil.which("x-terminal-emulator")
    if gnome:
        cmd = [
            gnome,
            "--window",
            "--title=Grok Build",
            "--geometry=132x40",
            f"--working-directory={cwd}",
            "--",
            str(binary),
        ]
    elif fallback:
        cmd = [fallback, "-e", str(binary)]
    else:
        return False, "I found Grok, but no terminal to put it in."

    try:
        subprocess.Popen(
            cmd,
            cwd=cwd,
            env=env,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError as exc:
        return False, f"Couldn't open Grok Build: {exc}"
    return True, None
