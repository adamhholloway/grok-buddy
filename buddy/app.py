import math
import os
import random
import signal
import sys
import time

os.environ.setdefault("GDK_BACKEND", "x11")

import cairo
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Gdk, GdkPixbuf, GLib, Gtk, Pango, PangoCairo

from buddy import bus, config, launch, lines
from buddy.characters import CHARACTERS, DEFAULT_CHARACTER, resolve as resolve_character
from buddy.paths import sprite_dir
from buddy.sprites import missing_poses, process_character
from buddy.voice import Voice

WIN_W = 460
WIN_H = 500
CHAR_TARGET_H = 210
BUBBLE_MAX_W = 280
BUBBLE_PAD_X = 14
BUBBLE_PAD_Y = 10


class BuddyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.cfg = config.load()
        spec = resolve_character(self.cfg.get("character") or DEFAULT_CHARACTER)
        self.cfg["character"] = spec["id"]
        self.voice = Voice(self.cfg)
        self.voice.apply_character(spec)
        self.pack = lines.Pack(spec["id"])
        self.sprites = {}
        self.base_mood = "idle"
        self.overlay = None
        self.overlay_until = 0.0
        self.talking = False
        self.talk_toggle = False
        self.hidden = False
        self.dragging = False
        self.drag_ox = 0
        self.drag_oy = 0
        self.moved = False
        self._click_id = None
        self.bubble_text = ""
        self.bubble_until = 0.0
        self.bubble_rect = None
        self.last_blink = time.monotonic()
        self.next_blink = 3.5
        self.last_tip = time.monotonic()
        self.busy = False
        self.t0 = time.monotonic()
        self.frame = 0
        self._shape = None
        self._save_pos_id = None

        if missing_poses(self.cfg["character"]):
            process_character(self.cfg["character"])
        self._load_sprites()
        self._setup_window()
        self._build_menu()

        self.bus = bus.Bus(self._on_bus)
        self.bus.start()

        self.connect("draw", self._on_draw)
        self.connect("button-press-event", self._on_press)
        self.connect("button-release-event", self._on_release)
        self.connect("motion-notify-event", self._on_motion)
        self.connect("enter-notify-event", self._on_enter)
        self.connect("delete-event", self._on_close)
        self.connect("realize", self._on_realize)
        self.connect("configure-event", self._on_configure)

        GLib.timeout_add(50, self._tick)
        GLib.timeout_add(400, self._after_map)

    def _setup_window(self):
        spec = resolve_character(self.cfg.get("character"))
        self.set_title(f"Grok Buddy — {spec['label']}")
        self.set_decorated(False)
        self.set_app_paintable(True)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_accept_focus(False)
        self.set_focus_on_map(False)
        self.set_resizable(False)
        self.set_default_size(WIN_W, WIN_H)
        self.set_size_request(WIN_W, WIN_H)
        self.stick()
        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.set_visual(self.get_screen().get_rgba_visual() or self.get_screen().get_system_visual())
        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK
            | Gdk.EventMask.BUTTON_RELEASE_MASK
            | Gdk.EventMask.POINTER_MOTION_MASK
            | Gdk.EventMask.ENTER_NOTIFY_MASK
            | Gdk.EventMask.LEAVE_NOTIFY_MASK
        )

    def _load_sprites(self):
        folder = sprite_dir(self.cfg.get("character") or DEFAULT_CHARACTER)
        self.sprites = {}
        for pose in (
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
        ):
            path = folder / f"{pose}.png"
            if not path.exists():
                continue
            self.sprites[pose] = GdkPixbuf.Pixbuf.new_from_file(str(path))
        if "idle" not in self.sprites:
            raise SystemExit(f"Grok Buddy is missing {folder / 'idle.png'}")

    def _build_menu(self):
        menu = Gtk.Menu()

        def item(label, cb):
            it = Gtk.MenuItem(label=label)
            it.connect("activate", cb)
            menu.append(it)
            return it

        item("Open Grok Build", lambda *_: self.open_grok())
        item("Tell a joke", lambda *_: self.say(self.pack.pick("jokes"), "talk"))
        item("Grok Build tip", lambda *_: self.say(self.pack.pick("tips"), "think"))
        menu.append(Gtk.SeparatorMenuItem())
        item("Say something", lambda *_: self.say(self.pack.pick("greetings"), "talk"))
        menu.append(Gtk.SeparatorMenuItem())
        char_menu = Gtk.Menu()
        self.char_items = {}
        group = None
        for key, spec in CHARACTERS.items():
            if group is None:
                it = Gtk.RadioMenuItem.new_with_label(None, spec["label"])
                group = it
            else:
                it = Gtk.RadioMenuItem.new_with_label(group.get_group(), spec["label"])
            it.set_active(key == self.cfg.get("character"))
            it.connect("toggled", self._on_character_item, key)
            char_menu.append(it)
            self.char_items[key] = it
        char_root = Gtk.MenuItem(label="Character")
        char_root.set_submenu(char_menu)
        menu.append(char_root)
        menu.append(Gtk.SeparatorMenuItem())
        self.voice_item = Gtk.CheckMenuItem(label="Voice")
        self.voice_item.set_active(bool(self.cfg.get("voice")))
        self.voice_item.connect("toggled", self._toggle_voice)
        menu.append(self.voice_item)
        self.tips_item = Gtk.CheckMenuItem(label="Idle chatter")
        self.tips_item.set_active(bool(self.cfg.get("idle_tips")))
        self.tips_item.connect("toggled", self._toggle_tips)
        menu.append(self.tips_item)
        menu.append(Gtk.SeparatorMenuItem())
        item("Take a nap", lambda *_: self.nap())
        item("Hide for 15 minutes", lambda *_: self.snooze(15 * 60))
        item("Sit in the corner", lambda *_: self.park_corner())
        menu.append(Gtk.SeparatorMenuItem())
        item("Quit Grok Buddy", lambda *_: self.quit())
        menu.show_all()
        self.menu = menu

    def _on_realize(self, *_args):
        self.place_window()

    def _after_map(self):
        self.place_window()
        if not self.cfg.get("welcomed"):
            self.say(self.pack.get("welcome"), "wave")
            self.cfg["welcomed"] = True
            config.save(self.cfg)
        else:
            self.flash("wave", 1.8)
        return False

    def place_window(self, force_corner=False):
        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor() or display.get_monitor(0)
        work = monitor.get_workarea()
        if not force_corner and self.cfg.get("x") is not None and self.cfg.get("y") is not None:
            x, y = int(self.cfg["x"]), int(self.cfg["y"])
        else:
            x = work.x + work.width - WIN_W - 12
            y = work.y + work.height - WIN_H - 12
        x = max(work.x, min(x, work.x + work.width - 80))
        y = max(work.y, min(y, work.y + work.height - 80))
        self.move(x, y)

    def open_grok(self):
        ok, err = launch.open_grok()
        if ok:
            self.say(self.pack.pick("launch"), "work")
        else:
            self.say(err or self.pack.pick("launch_fail"), "sad")

    def park_corner(self):
        self.cfg["x"] = None
        self.cfg["y"] = None
        config.save(self.cfg)
        self.place_window(force_corner=True)
        self.say("I'll sit in the corner. Drag me anytime.", "wave")

    def _on_configure(self, _widget, event):
        if self.dragging:
            return False
        if self._save_pos_id:
            GLib.source_remove(self._save_pos_id)
        self._save_pos_id = GLib.timeout_add(400, self._save_pos, event.x, event.y)
        return False

    def _save_pos(self, x, y):
        self._save_pos_id = None
        self.cfg["x"] = int(x)
        self.cfg["y"] = int(y)
        config.save(self.cfg)
        return False

    def current_pose(self):
        now = time.monotonic()
        if self.overlay and now < self.overlay_until:
            if self.overlay == "talk":
                return "talk" if self.talk_toggle else "idle"
            return self.overlay
        if self.overlay and now >= self.overlay_until:
            self.overlay = None
        if self.base_mood == "idle" and not self.talking:
            if now - self.last_blink >= self.next_blink:
                self.last_blink = now
                self.next_blink = random.uniform(3.2, 6.5)
                return "blink"
            if now - self.last_blink < 0.12:
                return "blink"
        return self.base_mood if self.base_mood in self.sprites else "idle"

    def _char_scale(self, pixbuf):
        user = float(self.cfg.get("scale") or 1.0)
        h = pixbuf.get_height()
        if h <= 0:
            return user
        return (CHAR_TARGET_H / float(h)) * user

    def _char_geom(self, pose=None):
        pose = pose or self.current_pose()
        pixbuf = self.sprites.get(pose) or self.sprites["idle"]
        scale = self._char_scale(pixbuf)
        w = pixbuf.get_width() * scale
        h = pixbuf.get_height() * scale
        cx = WIN_W / 2.0
        feet_y = WIN_H - 18.0
        bob = 0.0
        if self.base_mood != "sleep" and pose not in {"sleep"}:
            bob = math.sin((time.monotonic() - self.t0) * 2.15) * 3.2
        return pixbuf, scale, cx - w / 2.0, feet_y - h + bob, w, h

    def _on_draw(self, _widget, cr):
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.set_source_rgba(0, 0, 0, 0)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

        pixbuf, scale, x, y, w, h = self._char_geom()

        # ground shadow
        cr.save()
        cr.set_source_rgba(0, 0, 0, 0.22)
        cr.translate(WIN_W / 2.0, WIN_H - 16)
        cr.scale(1.0, 0.38)
        cr.arc(0, 0, w * 0.38, 0, 2 * math.pi)
        cr.fill()
        cr.restore()

        cr.save()
        cr.translate(x, y)
        cr.scale(scale, scale)
        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        cr.paint()
        cr.restore()

        if self.bubble_text:
            self._draw_bubble(cr, WIN_W / 2.0, y - 8)
        else:
            self.bubble_rect = None

        self._update_input_shape(x, y, w, h)
        return False

    def _draw_bubble(self, cr, cx, bottom):
        layout = self.create_pango_layout(self.bubble_text)
        layout.set_width(int(BUBBLE_MAX_W * Pango.SCALE))
        layout.set_wrap(Pango.WrapMode.WORD_CHAR)
        font = Pango.FontDescription("Ubuntu 12")
        layout.set_font_description(font)
        tw, th = layout.get_pixel_size()
        bw = tw + BUBBLE_PAD_X * 2
        bh = th + BUBBLE_PAD_Y * 2
        bx = max(10, min(cx - bw / 2.0, WIN_W - bw - 10))
        by = max(8, bottom - bh - 16)
        radius = 14
        tail_x = cx
        tail_y = by + bh

        cr.save()
        cr.new_path()
        self._round_rect(cr, bx, by, bw, bh, radius)
        # tail
        cr.move_to(tail_x - 10, tail_y - 2)
        cr.line_to(tail_x, tail_y + 14)
        cr.line_to(tail_x + 12, tail_y - 2)
        cr.close_path()
        cr.set_source_rgb(1.0, 0.97, 0.86)
        cr.fill_preserve()
        cr.set_source_rgb(0.72, 0.36, 0.92)
        cr.set_line_width(2.2)
        cr.stroke()
        cr.set_source_rgb(0.14, 0.12, 0.16)
        cr.move_to(bx + BUBBLE_PAD_X, by + BUBBLE_PAD_Y)
        PangoCairo.show_layout(cr, layout)
        cr.restore()
        self.bubble_rect = (bx, by, bw, bh + 16)

    def _round_rect(self, cr, x, y, w, h, r):
        cr.move_to(x + r, y)
        cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
        cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
        cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
        cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
        cr.close_path()

    def _update_input_shape(self, x, y, w, h):
        rects = [cairo.RectangleInt(int(x) - 4, int(y) - 4, int(w) + 8, int(h) + 16)]
        if self.bubble_rect:
            bx, by, bw, bh = self.bubble_rect
            rects.append(cairo.RectangleInt(int(bx) - 2, int(by) - 2, int(bw) + 4, int(bh) + 4))
        region = cairo.Region(rects[0])
        for rect in rects[1:]:
            region.union(cairo.Region(rect))
        key = (region.get_extents().x, region.get_extents().y, region.get_extents().width, region.get_extents().height, bool(self.bubble_text))
        if key != self._shape:
            self._shape = key
            self.input_shape_combine_region(region)

    def _on_press(self, _widget, event):
        if event.button == 3:
            self.menu.popup_at_pointer(event)
            return True
        if event.button == 2:
            self.open_grok()
            return True
        if event.button == 1:
            if event.type == Gdk.EventType.DOUBLE_BUTTON_PRESS:
                if self._click_id:
                    GLib.source_remove(self._click_id)
                    self._click_id = None
                self.dragging = False
                if self.base_mood == "sleep":
                    self.wake()
                else:
                    self.nap()
                return True
            if self.bubble_rect:
                bx, by, bw, bh = self.bubble_rect
                if bx <= event.x <= bx + bw and by <= event.y <= by + bh:
                    self.dismiss()
                    return True
            self.dragging = True
            self.moved = False
            self.drag_ox = int(event.x_root)
            self.drag_oy = int(event.y_root)
            return True
        return False

    def _on_motion(self, _widget, event):
        if not self.dragging:
            return False
        dx = int(event.x_root) - self.drag_ox
        dy = int(event.y_root) - self.drag_oy
        if abs(dx) + abs(dy) < 3 and not self.moved:
            return False
        wx, wy = self.get_position()
        self.move(wx + dx, wy + dy)
        self.drag_ox = int(event.x_root)
        self.drag_oy = int(event.y_root)
        self.moved = True
        return True

    def _on_release(self, _widget, event):
        if event.button != 1:
            return False
        was_drag = self.dragging
        moved = self.moved
        self.dragging = False
        if was_drag and not moved:
            if self._click_id:
                GLib.source_remove(self._click_id)
            self._click_id = GLib.timeout_add(280, self._delayed_click)
        elif moved:
            x, y = self.get_position()
            self.cfg["x"] = int(x)
            self.cfg["y"] = int(y)
            config.save(self.cfg)
        return True

    def _on_enter(self, *_args):
        gdk_win = self.get_window()
        if gdk_win:
            cursor = Gdk.Cursor.new_from_name(self.get_display(), "pointer")
            gdk_win.set_cursor(cursor)
        return False

    def _delayed_click(self):
        self._click_id = None
        self._clicked()
        return False

    def _clicked(self):
        if self.bubble_text:
            self.dismiss()
            return
        if self.base_mood == "sleep":
            self.wake()
            return
        if self.busy:
            self.say(self.pack.pick("click_busy"), "talk")
            return
        pool = list(self.pack.get("jokes")) + list(self.pack.get("greetings"))
        self.say(random.choice(pool), random.choice(["talk", "wave", "think"]))

    def say(self, text, mood="talk", voice=True):
        if not text:
            return
        self.bubble_text = text
        hold = max(4.5, min(16.0, 1.6 + len(text) / 18.0))
        self.bubble_until = time.monotonic() + hold
        if mood in {"wave", "celebrate", "alert", "sad", "think"}:
            self.flash(mood, 1.6 if mood != "talk" else hold)
        if mood == "talk" or voice:
            self.overlay = "talk"
            self.overlay_until = time.monotonic() + hold
            self.talking = True
        spoken = False
        if voice:
            spoken = self.voice.speak(text, on_end=self._speech_ended)
        if not spoken:
            GLib.timeout_add(int(hold * 1000), self._speech_ended)
        self.queue_draw()

    def _speech_ended(self):
        self.talking = False
        if self.overlay == "talk":
            self.overlay = None
        self.queue_draw()
        return False

    def dismiss(self):
        self.bubble_text = ""
        self.bubble_until = 0
        self.talking = False
        if self.overlay == "talk":
            self.overlay = None
        self.voice.stop()
        self.queue_draw()

    def flash(self, mood, seconds):
        if mood not in self.sprites:
            return
        self.overlay = mood
        self.overlay_until = time.monotonic() + seconds
        self.queue_draw()

    def set_mood(self, mood):
        if mood not in self.sprites:
            mood = "idle"
        self.base_mood = mood
        self.queue_draw()

    def nap(self):
        self.busy = False
        self.set_mood("sleep")
        self.say(self.pack.pick("nap"), "sleep", voice=True)
        self.overlay = "sleep"
        self.overlay_until = time.monotonic() + 2.0

    def wake(self):
        self.set_mood("idle")
        self.say(self.pack.pick("wake"), "wave")

    def snooze(self, seconds):
        self.hidden = True
        self.dismiss()
        self.hide()
        GLib.timeout_add(int(seconds * 1000), self._unsnooze)

    def _unsnooze(self):
        self.hidden = False
        self.show_all()
        self.set_keep_above(True)
        self.say("Miss me? I'm back.", "wave")
        return False

    def _toggle_voice(self, item):
        self.voice.set_enabled(item.get_active())
        config.save(self.cfg)
        if item.get_active():
            self.say("Okay. I'll talk.", "talk")
        else:
            self.bubble_text = "Voice off. I can still mime."
            self.bubble_until = time.monotonic() + 4
            self.flash("sad", 1.4)
            self.queue_draw()

    def _toggle_tips(self, item):
        self.cfg["idle_tips"] = bool(item.get_active())
        config.save(self.cfg)

    def _on_character_item(self, item, key):
        if not item.get_active():
            return
        if key == self.cfg.get("character"):
            return
        self.set_character(key)

    def set_character(self, name):
        spec = resolve_character(name)
        self.cfg["character"] = spec["id"]
        self.pack = lines.Pack(spec["id"])
        self.voice.apply_character(spec)
        if missing_poses(spec["id"]):
            process_character(spec["id"])
        self._load_sprites()
        self.set_title(f"Grok Buddy — {spec['label']}")
        self.base_mood = "idle"
        self.overlay = None
        self._shape = None
        config.save(self.cfg)
        item = self.char_items.get(spec["id"])
        if item and not item.get_active():
            item.set_active(True)
        self.say(self.pack.get("switch"), "wave")

    def _tick(self):
        now = time.monotonic()
        self.frame += 1
        if self.talking and self.frame % 2 == 0:
            self.talk_toggle = not self.talk_toggle
        if self.bubble_text and self.bubble_until and now > self.bubble_until and not self.talking:
            self.dismiss()
        idle_for = float(self.cfg.get("idle_seconds") or 240)
        if (
            self.cfg.get("idle_tips")
            and not self.busy
            and not self.hidden
            and self.base_mood != "sleep"
            and not self.bubble_text
            and now - self.last_tip > idle_for
        ):
            self.last_tip = now
            self.say(self.pack.chatter(), random.choice(["talk", "think"]))
        self.queue_draw()
        return True

    def _on_bus(self, message):
        kind = message.get("type")
        if kind == "say":
            self.say(message.get("text") or "", message.get("mood") or "talk")
        elif kind == "tip":
            self.say(self.pack.pick("tips"), "think")
        elif kind == "joke":
            self.say(self.pack.pick("jokes"), "talk")
        elif kind == "grok":
            self.open_grok()
        elif kind == "hide":
            self.snooze(15 * 60)
        elif kind == "wake":
            if self.hidden:
                self._unsnooze()
            else:
                self.wake()
        elif kind == "quit":
            self.quit()
        elif kind == "mood":
            self.set_mood(message.get("mood") or "idle")
        elif kind == "character":
            self.set_character(message.get("character") or DEFAULT_CHARACTER)
        elif kind == "event":
            self._handle_event(message.get("event") or {})

    def _handle_event(self, event):
        name = (
            event.get("hookEventName")
            or event.get("event")
            or event.get("name")
            or ""
        )
        name = str(name).replace("-", "_")
        notif = event.get("notificationType") or event.get("notification") or ""
        if name in {"session_start", "SessionStart"}:
            self.busy = False
            self.set_mood("idle")
            self.say(self.pack.pick("session_start"), "wave")
        elif name in {"session_end", "SessionEnd"}:
            self.busy = False
            self.set_mood("idle")
            self.say(self.pack.pick("session_end"), "wave")
        elif name in {"user_prompt_submit", "UserPromptSubmit"}:
            self.busy = True
            self.set_mood("think")
            self.last_tip = time.monotonic()
        elif name in {"pre_tool_use", "PreToolUse"}:
            self.busy = True
            self.set_mood("work")
        elif name in {"post_tool_use_failure", "PostToolUseFailure"}:
            self.set_mood("sad")
            self.flash("sad", 2.0)
        elif name in {"stop", "Stop"}:
            self.busy = False
            self.set_mood("idle")
            self.flash("celebrate", 1.6)
            if random.random() < 0.35:
                self.say(self.pack.pick("turn_done"), "celebrate")
        elif name in {"stop_failure", "StopFailure"}:
            self.busy = False
            self.set_mood("idle")
            self.say(self.pack.pick("turn_fail"), "sad")
        elif name in {"stop_cancelled", "StopCancelled"}:
            self.busy = False
            self.set_mood("idle")
            reason = event.get("reason") or ""
            if reason in {"permission_rejected", "permission_cancelled"}:
                self.flash("alert", 1.4)
            else:
                self.flash("alert", 1.2)
        elif name in {"notification", "Notification"}:
            if str(notif) == "permission_prompt":
                self.say(self.pack.pick("permission"), "alert")
        elif name in {"subagent_start", "SubagentStart"}:
            self.set_mood("work")

    def _on_close(self, *_args):
        self.quit()
        return True

    def quit(self):
        try:
            self.voice.close()
        except Exception:
            pass
        try:
            self.bus.close()
        except Exception:
            pass
        Gtk.main_quit()


def another_instance_alive():
    return bus.send({"type": "ping"})


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in {
        "say",
        "hide",
        "quit",
        "wake",
        "tip",
        "joke",
        "grok",
        "mood",
        "event",
        "character",
    }:
        return bus.send_cli(argv)

    if another_instance_alive():
        if argv:
            return bus.send_cli(argv)
        bus.send({"type": "say", "text": "I'm already on the desktop.", "mood": "wave"})
        return 0

    Gtk.init([])
    win = BuddyWindow()
    win.show_all()

    def handle_stop(_signum, _frame):
        GLib.idle_add(win.quit)

    signal.signal(signal.SIGTERM, handle_stop)
    signal.signal(signal.SIGINT, handle_stop)
    Gtk.main()
    return 0
