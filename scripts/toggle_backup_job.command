#!/bin/zsh

LABEL="com.bigskyag.backupzip"
PLIST=~/Library/LaunchAgents/$LABEL.plist

if launchctl list | grep -q "$LABEL"; then
    echo "🛑 Disabling 10PM Backup Job..."
    launchctl unload "$PLIST"
    echo "✅ Backup job disabled."
else
    echo "✅ Enabling 10PM Backup Job..."
    launchctl load "$PLIST"
    echo "✅ Backup job enabled."
fi

