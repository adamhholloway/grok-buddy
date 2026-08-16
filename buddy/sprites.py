from pathlib import Path

from PIL import Image

from buddy.paths import POSES, RAW, SPRITES, raw_dir, sprite_dir

MAX_EDGE = 420


def is_screen(r, g, b):
    if g < 70:
        return False
    if g > r + 22 and g > b + 22:
        return True
    if g > 155 and r < 145 and b < 145 and g > r and g > b:
        return True
    return False


def _despill(r, g, b):
    if g > r and g > b:
        g = min(g, max(r, b) + 10)
    return r, g, b


def key_image(im):
    im = im.convert("RGBA")
    if max(im.size) > 700:
        im.thumbnail((700, 700), Image.Resampling.LANCZOS)
    pix = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, _a = pix[x, y]
            if is_screen(r, g, b):
                pix[x, y] = (0, 0, 0, 0)
            else:
                r, g, b = _despill(r, g, b)
                pix[x, y] = (r, g, b, 255)
    marked = []
    for y in range(h):
        for x in range(w):
            r, g, b, a = pix[x, y]
            if a == 0:
                continue
            edge = False
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= nx < w and 0 <= ny < h and pix[nx, ny][3] == 0:
                    edge = True
                    break
            if edge and g > r + 8 and g > b + 8:
                marked.append((x, y))
    for x, y in marked:
        pix[x, y] = (0, 0, 0, 0)
    bbox = im.getbbox()
    if not bbox:
        return im
    pad = 6
    left, top, right, bottom = bbox
    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(w, right + pad)
    bottom = min(h, bottom + pad)
    return im.crop((left, top, right, bottom))


def fit(im, max_edge=MAX_EDGE):
    w, h = im.size
    longest = max(w, h)
    if longest <= max_edge:
        return im
    scale = max_edge / float(longest)
    nw = max(1, int(round(w * scale)))
    nh = max(1, int(round(h * scale)))
    return im.resize((nw, nh), Image.Resampling.LANCZOS)


def process_character(character, raw=None, out=None):
    raw = Path(raw or raw_dir(character))
    out = Path(out or sprite_dir(character))
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for pose in POSES:
        src = raw / f"{pose}.jpg"
        if not src.exists():
            src = raw / f"{pose}.png"
        if not src.exists():
            continue
        im = key_image(Image.open(src))
        im = fit(im)
        dest = out / f"{pose}.png"
        im.save(dest, "PNG")
        written.append(dest)
    idle = out / "idle.png"
    if idle.exists():
        icon = Image.open(idle).convert("RGBA")
        icon.thumbnail((128, 128), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        canvas.paste(icon, ((128 - icon.width) // 2, (128 - icon.height) // 2), icon)
        canvas.save(out / "icon.png", "PNG")
        written.append(out / "icon.png")
    return written


def process_all(raw_dir_path=None, out_dir=None):
    # Legacy single-folder call still works; otherwise process every character.
    if raw_dir_path or out_dir:
        return process_character("buddy", raw=raw_dir_path, out=out_dir)
    written = []
    for child in RAW.iterdir() if RAW.exists() else []:
        if child.is_dir():
            written.extend(process_character(child.name))
    return written


def missing_poses(character="buddy"):
    folder = sprite_dir(character)
    return [pose for pose in POSES if not (folder / f"{pose}.png").exists()]
