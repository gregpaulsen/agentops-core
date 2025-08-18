#!/bin/bash

# Performance Optimization Script
# Safely closes resource-heavy apps to improve system performance

echo "🚀 Starting performance optimization..."

# Check current system load
echo "📊 Current system load:"
top -l 1 | grep "Load Avg"

echo ""
echo "🔄 Optimizing system performance..."

# Close Google Drive (biggest resource hog)
if pgrep -f "Google Drive" > /dev/null; then
    echo "🔄 Closing Google Drive..."
    pkill -f "Google Drive"
    sleep 2
fi

# Close Google Drive Helper processes
if pgrep -f "Google Drive Helper" > /dev/null; then
    echo "🔄 Closing Google Drive Helper processes..."
    pkill -f "Google Drive Helper"
    sleep 1
fi

# Restart Cursor if it's consuming too much CPU
CURSOR_CPU=$(ps aux | grep "Cursor Helper" | grep -v grep | awk '{sum+=$3} END {print sum+0}')
if (( $(echo "$CURSOR_CPU > 20" | bc -l) )); then
    echo "🔄 Cursor is consuming high CPU ($CURSOR_CPU%), restarting..."
    pkill -f "Cursor"
    sleep 3
    open -a "Cursor"
fi

# Clear system caches
echo "🧹 Clearing system caches..."
sudo purge 2>/dev/null || echo "Cache clearing requires admin privileges"

# Show improvement
echo ""
echo "📊 Performance optimization complete!"
echo "🔄 Restarting system monitoring..."
sleep 2

echo "📊 New system load:"
top -l 1 | grep "Load Avg"

echo ""
echo "💡 Tips for ongoing performance:"
echo "   • Close unused Chrome tabs"
echo "   • Only sync Google Drive when needed"
echo "   • Restart Cursor if it feels slow"
echo "   • Consider restarting your Mac weekly"
