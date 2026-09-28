#!/bin/zsh

# Signal script is running
echo "Script started"

# Activate virtual environment
source /Users/ciaranturner/code/sportsAnalytics/backend/venv/bin/activate

# Change to backend directory
cd /Users/ciaranturner/code/sportsAnalytics/backend

# Run NBA daily provider
python -m nba.provider.daily >> daily_updater.log 2>&1

# Run NBA process_games
python -m nba.process_games >> daily_updater.log 2>&1

# Run NFL daily provider
python -m nfl.provider.daily >> daily_updater.log 2>&1

# Run NFL process_games
python -m nfl.process_games >> daily_updater.log 2>&1

# Run MLB daily provider
python -m mlb.provider.daily >> daily_updater.log 2>&1

# Run MLB process_games
python -m mlb.process_games >> daily_updater.log 2>&1

echo "Script finished"