#!/usr/bin/env bash

source .venv/bin/activate

today=$(date +"%Y-%m-%d")

SECONDS=0

python full_scraper.py $today
python process_text.py $today
python db_functions.py $today

duration=$SECONDS
echo "==== Papers scraped and processed for $today in $((duration / 60))m $((duration % 60))s ===="
