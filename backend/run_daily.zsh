#!/bin/zsh

# Signal script is running
echo "Script started"

# Activate virtual environment
source /Users/ciaranturner/code/sportsAnalytics/backend/venv/bin/activate

# Change to backend directory
cd /Users/ciaranturner/code/sportsAnalytics/backend

# Run NBA daily provider
python -m nba.provider.daily >> daily_updater.log 2>&1

# Change to backend directory
cd /Users/ciaranturner/code/sportsAnalytics/backend

# Run NBA process_games
python -m nba.process_games >> daily_updater.log 2>&1

echo "Script finished"