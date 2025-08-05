#!/bin/zsh
set +H

echo "📦 Running nightly AgentOps backup..."
python3 ~/Desktop/Coding_Commands/create_backup_zip_cleaned.py
python3 ~/Desktop/Coding_Commands/upload_backup_to_drive_v3.py
echo "✅ Backup complete\!"
