#!/bin/bash

# Fix Backup Rotation Script
# This script moves old backups to archive and cleans up the massive backup

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BACKUP_DIR="/Volumes/BigSkyAgSSD/BigSkyAg/00_Admin/Backups"
ARCHIVE_DIR="$BACKUP_DIR/Archive"

echo "🔧 Fixing Backup Rotation"
echo "========================"
echo "Backup Directory: $BACKUP_DIR"
echo "Archive Directory: $ARCHIVE_DIR"
echo ""

# Ensure archive directory exists
mkdir -p "$ARCHIVE_DIR"

# List current backups
echo "📋 Current backups:"
ls -lah "$BACKUP_DIR"/*.zip 2>/dev/null | grep -v "BigSkyAg_Backup_$(date +%Y-%m-%d).zip" || echo "  No old backups found"

echo ""
echo "🗑️  Removing the massive backup (158GB) that includes backup folder..."
if [[ -f "$BACKUP_DIR/BigSkyAg_Backup_$(date +%Y-%m-%d).zip" ]]; then
    rm "$BACKUP_DIR/BigSkyAg_Backup_$(date +%Y-%m-%d).zip"
    echo -e "${GREEN}✅ Removed massive backup${NC}"
else
    echo -e "${YELLOW}⚠️  No massive backup found to remove${NC}"
fi

echo ""
echo "📦 Moving old backups to archive..."

# Move old backups to archive
for backup in "$BACKUP_DIR"/BigSkyAg_Backup_*.zip; do
    if [[ -f "$backup" ]]; then
        filename=$(basename "$backup")
        echo "  Moving: $filename → Archive/"
        mv "$backup" "$ARCHIVE_DIR/"
    fi
done

# Move chunk files to archive
for chunk in "$BACKUP_DIR"/BigSkyAg_Backup_*.chunk_*; do
    if [[ -f "$chunk" ]]; then
        filename=$(basename "$chunk")
        echo "  Moving: $filename → Archive/"
        mv "$chunk" "$ARCHIVE_DIR/"
    fi
done

echo ""
echo "📊 Final status:"
echo "  Active backups: $(ls "$BACKUP_DIR"/*.zip 2>/dev/null | wc -l | tr -d ' ')"
echo "  Archived backups: $(ls "$ARCHIVE_DIR"/*.zip 2>/dev/null | wc -l | tr -d ' ')"
echo "  Archived chunks: $(ls "$ARCHIVE_DIR"/*.chunk_* 2>/dev/null | wc -l | tr -d ' ')"

echo ""
echo -e "${GREEN}✅ Backup rotation fixed!${NC}"
echo "  - Removed massive backup (158GB)"
echo "  - Moved old backups to archive"
echo "  - Ready for clean backup with exclusions"
