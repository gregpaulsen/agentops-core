#!/bin/zsh
set +H

echo "📦 Running nightly AgentOps backup..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📂 Working directory: $SCRIPT_DIR"

# Run backup
python3 create_backup_zip_cleaned.py

# Run upload if backup was successful
if [[ $? -eq 0 ]]; then
  echo "✅ Backup successful, proceeding with upload..."
  python3 upload_backup_to_drive_v3.py
  echo "✅ Backup and upload complete!"
else
  echo "❌ Backup failed, skipping upload"
  exit 1
fi
