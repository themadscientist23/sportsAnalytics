#!/bin/zsh

# Signal script is running
echo "Script started"

# Activate virtual environment
source /Users/ciaranturner/code/sportsAnalytics/backend/venv/bin/activate

# Run NBA daily provider
python /Users/ciaranturner/code/sportsAnalytics/backend/nba/provider/daily.py >> /Users/ciaranturner/code/sportsAnalytics/backend/daily_updater.log 2>&1

# Run NBA process_game
python /Users/ciaranturner/code/sportsAnalytics/backend/nba/process_game.py >> /Users/ciaranturner/code/sportsAnalytics/backend/daily_updater.log 2>&1