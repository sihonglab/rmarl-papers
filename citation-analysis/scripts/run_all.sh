#!/usr/bin/env bash
# Regenerate the full citation analysis from the processed paper texts.
set -e
cd "$(dirname "$0")"
python3 01_extract_references.py
python3 02_internal_graph.py
python3 03_cluster_external.py
python3 04_missing_candidates.py
python3 05_write_reports.py
python3 06_build_html.py
python3 07_check_xlsx.py
python3 08_prepare_xlsx_rows.py   # prepares rows for the master spreadsheet
# 09 / 10 are NOT run automatically: they mutate the curated master files.
# Run manually to insert the gap papers (both idempotent, back up first):
#   python3 09_append_to_xlsx.py   -> ../robust-marl-papers.xlsx (rows Source=cite-analysis)
#   python3 10_append_to_md.py     -> ../robust-marl-MASTER.md   (marked supplement section)
echo "Done. See ../reports/ and ../data/"
