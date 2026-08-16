import shutil
import subprocess
import urllib.parse
from datetime import datetime


def workarea():
    from gi.repository import Gdk

    display = Gdk.Display.get_default()
    monitor = display.get_primary_monitor() or display.get_monitor(0)
    return monitor.get_workarea()


def pointer():
    from gi.repository import Gdk

    display = Gdk.Display.get_default()
    seat = display.get_default_seat()
    _screen, x, y = seat.get_pointer().get_position()
    return int(x), int(y)


def open_search(query):
    q = urllib.parse.quote_plus(query)
    url = f"https://duckduckgo.com/?q={q}"
    opener = shutil.which("xdg-open")
    if not opener:
        return False
    subprocess.Popen(
        [opener, url],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    return True


def clipboard_text():
    from gi.repository import Gdk, Gtk

    clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    text = clip.wait_for_text()
    return (text or "").strip()


def spoken_time():
    now = datetime.now()
    hour = now.strftime("%I").lstrip("0") or "12"
    minute = now.strftime("%M")
    ampm = now.strftime("%p").replace("AM", "A M").replace("PM", "P M")
    day = now.strftime("%A")
    month = now.strftime("%B")
    date = now.day
    if 10 <= date % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(date % 10, "th")
    return f"It's {hour} {minute} {ampm} on {day}, {month} {date}{suffix}."
