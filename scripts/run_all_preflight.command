#!/bin/zsh

echo "🛠️ Running all preflight cleanup tools..."

# Clean user cache
echo "🧹 Clearing user cache..."
rm -rf ~/Library/Caches/*

# Purge RAM
echo "🧠 Purging RAM..."
sudo purge

# Clear diagnostic logs
echo "🧾 Clearing logs..."
rm -rf ~/Library/Logs/DiagnosticReports/*
sudo rm -rf /private/var/log/*

# Launch Coding Commands folder
echo "📂 Opening Coding_Commands folder..."
open ~/Desktop/Coding_Commands

echo "✅ Preflight complete. Ready to code."
