#!/bin/sh
set -eu

cd "$(dirname "$0")"

tmp="$(mktemp "${TMPDIR:-/tmp}/niri-config.XXXXXX")"
trap 'rm -f "$tmp"' EXIT

cat parts/*.kdl > "$tmp"
mv "$tmp" config.kdl
chmod 644 config.kdl
trap - EXIT

printf 'Built %s\n' "$PWD/config.kdl"
