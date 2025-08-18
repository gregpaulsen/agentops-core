#!/bin/bash

# Quick Development Cleanup Script
# Safely removes development artifacts to speed up development

echo "🧹 Starting quick development cleanup..."

# Remove Python cache files
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
echo "✅ Removed Python cache files"

# Remove .DS_Store files
find . -name ".DS_Store" -delete 2>/dev/null
echo "✅ Removed .DS_Store files"

# Remove temporary files
find . -name "*.tmp" -delete 2>/dev/null
find . -name "*.cache" -delete 2>/dev/null
echo "✅ Removed temporary files"

# Clean up old logs (keep last 5)
cd Reports
ls -t *.log | tail -n +6 | xargs rm -f 2>/dev/null
cd ..
echo "✅ Cleaned up old log files"

# Show space saved
echo ""
echo "📊 Current space usage:"
du -sh * | sort -hr | head -5

echo ""
echo "🚀 Development cleanup complete! Your system is now optimized for faster development."
