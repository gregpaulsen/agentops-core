#!/bin/zsh

BIGSKY_PATH=$(find /Volumes -maxdepth 2 -type d -name "BigSkyAg" -exec test -d "{}/00_Admin" \; -print | head -n 1)

if [[ -z "$BIGSKY_PATH" ]]; then
  echo "❌ BigSkyAg drive not found or missing folders."
  exit 1
fi


echo "🔍 Running system check..."

# Disk space
echo "\n💾 Disk usage:"
df -h /

# RAM status
echo "\n🧠 Memory usage:"
vm_stat | grep "Pages"

# Check if Python exists
echo "\n🐍 Python check:"
if command -v python3 &>/dev/null; then
  echo "Python3 is installed ✅"
else
  echo "Python3 not found ❌"
fi

# Check for SSD
echo "\n💽 SSD check:"
if mount | grep -q "/Volumes/BigSkySSD"; then
  echo "⚠️ BigSkySSD is mounted — this folder is meant to be separate."
else
  echo "✅ BigSkySSD is NOT mounted — good to go."
fi

echo "\n✅ System check complete."
