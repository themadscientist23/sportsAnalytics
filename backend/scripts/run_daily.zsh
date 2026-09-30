#!/bin/zsh

echo "Script started"

source /Users/ciaranturner/code/sportsAnalytics/backend/venv/bin/activate
cd /Users/ciaranturner/code/sportsAnalytics/backend

LOG=scripts/daily_updater.log

for sport in nba nfl mlb; do
  python -m app.provider.daily $sport >> $LOG 2>&1
  python -m app.sports.process_games $sport >> $LOG 2>&1
done

echo "Script finished"
