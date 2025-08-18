#!/bin/zsh

echo "🔧 AgentOps Morning System Check – Running..."

# Paths
COMMANDS_FOLDER="$HOME/Desktop/Coding_Commands"
BACKUP_FOLDER="$HOME/Google Drive/My Drive/BigSkyAgBackup"
DROPZONE_FOLDER="$HOME/Google Drive/My Drive/DropZone"

# 1. Check command files
echo "🔍 Checking essential command files..."
REQUIRED_COMMANDS=("run_gregops_backup.command" "open_dropzone.command" "clean_terminal.command")

for cmd in "${REQUIRED_COMMANDS[@]}"; do
    if [ -f "$COMMANDS_FOLDER/$cmd" ]; then
        echo "✅ Found: $cmd"
    else
        echo "❌ Missing: $cmd"
    fi
done

# 2. Check backup files
echo "📦 Checking backup folder contents..."
if [ -d "$BACKUP_FOLDER" ]; then
    backup_count=$(ls -1 "$BACKUP_FOLDER"/*.zip 2>/dev/null | wc -l | tr -d ' ')
    if [ "$backup_count" -ge 2 ]; then
        echo "✅ Backup folder has $backup_count .zip files"
        latest_backup=$(ls -lt "$BACKUP_FOLDER"/*.zip | head -1 | awk '{print $6, $7, $8}')
        echo "🕒 Most recent backup: $latest_backup"
    else
        echo "❌ Backup folder only has $backup_count .zip file(s)"
    fi
else
    echo "❌ Backup folder not found"
fi

# 3. Check DropZone
echo "📂 Checking DropZone..."
if [ -d "$DROPZONE_FOLDER" ]; then
    echo "✅ DropZone exists"
else
    echo "❌ DropZone missing"
fi

# 4. Check if Google Drive is running
echo "☁️ Checking if Google Drive is running..."
if pgrep -f "Google Drive" > /dev/null; then
    echo "✅ Google Drive is running"
else
    echo "❌ Google Drive not detected. Try launching manually."
fi

# 5. Summary
echo ""
echo "🧠 AgentOps System Status:"
if [[ "$backup_count" -ge 2 ]] && [[ -d "$DROPZONE_FOLDER" ]] && pgrep -f "Google Drive" > /dev/null; then
    echo "✅ All systems are GO — ready to code 🚀"
else
    echo "⚠️ Issues detected — fix before proceeding."
fi
