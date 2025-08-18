#!/bin/zsh
# 🔄 reset_bigsky_backup.command
# Kills backup script, deletes old zips, and runs fresh clean backup

echo "🛑 Killing active backup script..."
pkill -f create_backup_zip_cleaned.py

echo "🧹 Cleaning up partial .zip files..."
rm -f /Volumes/BigSkyAgSSD/BigSkyAg/00_Admin/Backups/BigSkyAg_Backup_*.zip
rm -f /tmp/BigSkyAg_Backup_*.zip

echo "🚀 Running fresh backup with size cap..."
python3 ~/Desktop/Coding_Commands/create_backup_zip_cleaned.py
