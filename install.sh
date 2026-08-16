#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

python3 "$ROOT/scripts/process_sprites.py"

chmod +x "$ROOT/start.sh" "$ROOT/hooks/notify.py" "$ROOT/install.sh"

mkdir -p "$HOME/.local/share/applications"
mkdir -p "$HOME/.config/autostart"
mkdir -p "$HOME/.local/bin"
mkdir -p "$HOME/.grok/hooks"

# desktop launchers
sed "s|@ROOT@|$ROOT|g" "$ROOT/grok-buddy.desktop.in" > "$HOME/.local/share/applications/grok-buddy.desktop"
cp "$HOME/.local/share/applications/grok-buddy.desktop" "$HOME/.config/autostart/grok-buddy.desktop"

ln -sfn "$ROOT/start.sh" "$HOME/.local/bin/grok-buddy"
ln -sfn "$ROOT/hooks/grok-buddy.json" "$HOME/.grok/hooks/grok-buddy.json"
ln -sfn "$ROOT/hooks/notify.py" "$HOME/.grok/hooks/notify.py"

update-desktop-database "$HOME/.local/share/applications" >/dev/null 2>&1 || true

echo "Grok Buddy installed."
echo "  launcher : grok-buddy"
echo "  autostart: ~/.config/autostart/grok-buddy.desktop"
echo "  hooks    : ~/.grok/hooks/grok-buddy.json"
echo "Start it with:  grok-buddy"
