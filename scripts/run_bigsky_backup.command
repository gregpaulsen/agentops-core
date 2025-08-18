#!/bin/zsh

echo "🚀 Starting Big Sky Ag backup..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📂 Working directory: $SCRIPT_DIR"
python3 create_backup_zip_cleaned.py

if [[ $? -eq 0 ]]; then
  osascript -e 'display notification "Backup completed successfully!" with title "BigSky AgentOps"'
  afplay /System/Library/Sounds/Glass.aiff
else
  osascript -e 'display notification "Backup failed. Check terminal." with title "BigSky AgentOps"'
  afplay /System/Library/Sounds/Basso.aiff
fi
