#!/usr/bin/env bash
# Download Piper and the Amy neural voice used by Annie.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR="$ROOT/vendor"
mkdir -p "$VENDOR/piper" "$VENDOR/voices"

if [ ! -x "$VENDOR/piper/piper" ]; then
  tmp="$(mktemp -d)"
  curl -fsSL -o "$tmp/piper.tgz" \
    https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz
  tar -xzf "$tmp/piper.tgz" -C "$tmp"
  if [ -d "$tmp/piper" ]; then
    cp -a "$tmp/piper/." "$VENDOR/piper/"
  else
    cp -a "$tmp/." "$VENDOR/piper/"
  fi
  rm -rf "$tmp"
fi

if [ ! -f "$VENDOR/voices/en_US-amy-medium.onnx" ]; then
  curl -fL -o "$VENDOR/voices/en_US-amy-medium.onnx" \
    "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx?download=true"
  curl -fL -o "$VENDOR/voices/en_US-amy-medium.onnx.json" \
    "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx.json?download=true"
fi

echo "Piper voice ready: $VENDOR/voices/en_US-amy-medium.onnx"
