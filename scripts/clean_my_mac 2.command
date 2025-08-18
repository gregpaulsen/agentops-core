#!/bin/zsh

echo "🔧 Starting safe system cleanup..."

# 1. Clear user cache
echo "🧹 Clearing user cache..."
rm -rf ~/Library/Caches/*

# 2. Purge RAM
echo "🧠 Purging RAM..."
sudo purge

# 3. Clear diagnostic logs
echo "📋 Clearing diagnostic logs..."
rm -rf ~/Library/Logs/DiagnosticReports/*
sudo rm -rf /private/var/log/*

echo "✅ All done. Recommend rebooting if it’s been a while."
