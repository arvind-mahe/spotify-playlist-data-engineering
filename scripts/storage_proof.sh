#!/usr/bin/env bash
# Writes docs/storage_proof.txt: a timestamped, reproducible record of the storage measurement.
# Run from the repo root:   bash scripts/storage_proof.sh
set -euo pipefail

RAW="${1:-data/raw/mpd.slice.0-999.json}"
OUT="docs/storage_proof.txt"
mkdir -p docs

bytes_of() { find "$1" -type f -printf '%s\n' | awk '{s+=$1} END{print s+0}'; }
files_of() { find "$1" -type f | wc -l; }
mb()  { awk -v b="$1" 'BEGIN{printf "%.2f", b/1048576}'; }
pct() { awk -v n="$1" -v d="$2" 'BEGIN{printf "%.1f", 100*(1-n/d)}'; }

raw_b=$(stat -c%s "$RAW")
bronze=$(bytes_of data/bronze); silver=$(bytes_of data/silver); gold=$(bytes_of data/gold)
all=$((bronze + silver + gold))

{
  echo "STORAGE PROOF - Spotify Million Playlist pipeline"
  echo "Generated : $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
  echo "Host      : $(hostname)"
  echo "Git commit: $(git rev-parse --short HEAD 2>/dev/null || echo 'n/a (not a git checkout)')"
  echo
  echo "Raw input : $RAW"
  echo "  bytes   : $raw_b"
  echo "  sha256  : $(sha256sum "$RAW" | awk '{print $1}')"
  echo
  printf '%-12s %14s %8s %10s\n' "Layer" "Bytes" "Files" "MB"
  printf '%-12s %14s %8s %10s\n' "Raw JSON"   "$raw_b" 1 "$(mb "$raw_b")"
  printf '%-12s %14s %8s %10s\n' "Bronze"     "$bronze" "$(files_of data/bronze)" "$(mb "$bronze")"
  printf '%-12s %14s %8s %10s\n' "Silver"     "$silver" "$(files_of data/silver)" "$(mb "$silver")"
  printf '%-12s %14s %8s %10s\n' "Gold"       "$gold"   "$(files_of data/gold)"   "$(mb "$gold")"
  printf '%-12s %14s %8s %10s\n' "All layers" "$all" "-" "$(mb "$all")"
  echo
  echo "Raw JSON -> Bronze Parquet reduction : $(pct "$bronze" "$raw_b")%   (1 - bronze/raw)"
  echo "Raw JSON -> All layers reduction     : $(pct "$all" "$raw_b")%   (1 - (bronze+silver+gold)/raw)"
  echo
  echo "Per-table size (Silver and Gold):"
  for d in data/silver/* data/gold/*; do printf '  %-32s %12s bytes\n' "$d" "$(bytes_of "$d")"; done
} | tee "$OUT"

echo
echo "Saved to $OUT - commit it:  git add $OUT && git commit -m 'Add storage measurement proof'"
