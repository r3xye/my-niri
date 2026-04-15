#!/bin/sh
set -eu

config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/niri"
parts_dir="$config_dir/parts"
target="$config_dir/config.kdl"

mkdir -p "$config_dir"

tmp="$(mktemp "${TMPDIR:-/tmp}/niri-config.XXXXXX")"
trap 'rm -f "$tmp"' EXIT

cat "$parts_dir"/*.kdl > "$tmp"
mv "$tmp" "$target"
chmod 644 "$target"
trap - EXIT

printf 'Built %s\n' "$target"
