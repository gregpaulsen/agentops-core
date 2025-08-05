#!/bin/zsh

echo "🚀 Starting Big Sky Ag backup..."
python3 ~/Desktop/Coding_Commands/create_backup_zip_cleaned.py

if [[ $? -eq 0 ]]; then
  osascript -e 'display notification "Backup completed successfully!" with title "BigSky AgentOps"'
  afplay /System/Library/Sounds/Glass.aiff
else
  osascript -e 'display notification "Backup failed. Check terminal." with title "BigSky AgentOps"'
  afplay /System/Library/Sounds/Basso.aiff
fi
