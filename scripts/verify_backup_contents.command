#!/bin/zsh
ZIP_PATH="/Volumes/BigSkyAgSSD/BigSkyAg/00_Admin/Backups/BigSkyAg_Backup_$(date +%F).zip"

if [ ! -f "$ZIP_PATH" ]; then
  echo "❌ No zip file found for today ($ZIP_PATH)"
  exit 1
fi

echo "🔍 Contents of: $ZIP_PATH"
unzip -l "$ZIP_PATH" | less
