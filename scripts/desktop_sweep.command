#!/bin/bash

# Create folders if they don't exist
mkdir -p ~/Desktop/Z_Archive/DesktopLogs
mkdir -p ~/Desktop/Claude_Exports
mkdir -p ~/Desktop/_To_Delete

# Move backup logs
if [ -f ~/Desktop/backup_0805_list.txt ]; then
    mv ~/Desktop/backup_0805_list.txt ~/Desktop/Z_Archive/DesktopLogs/
    echo "Moved backup_0805_list.txt to Z_Archive/DesktopLogs/"
fi

if [ -f ~/Desktop/backup_0806_list.txt ]; then
    mv ~/Desktop/backup_0806_list.txt ~/Desktop/Z_Archive/DesktopLogs/
    echo "Moved backup_0806_list.txt to Z_Archive/DesktopLogs/"
fi

# Move August 5 backup zip to archive folder
if [ -f ~/Desktop/BigSkyAg_2025-08-05.zip ]; then
    mv ~/Desktop/BigSkyAg_2025-08-05.zip ~/Desktop/Z_Archive/
    echo "Moved BigSkyAg_2025-08-05.zip to Z_Archive/"
fi

# Prompt to delete duplicate paulyops-core
if [ -d ~/Desktop/paulyops-core ]; then
    echo "Found duplicate folder: ~/Desktop/paulyops-core"
    read -p "Do you want to move it to _To_Delete/? [y/N] " yn
    case $yn in
        [Yy]* ) mv ~/Desktop/paulyops-core ~/Desktop/_To_Delete/ && echo "Moved paulyops-core to _To_Delete/";;
        * ) echo "Skipped moving paulyops-core.";;
    esac
fi

echo "Desktop cleanup complete."
