#!/bin/zsh

echo "🔐 Git Cleanup & Demo Prep Tool"

# Prompt for file to secure
read "secret_path?Enter full path of secret or large file to remove (or press Enter to skip): "

# Secure file move (if provided)
if [[ -n "$secret_path" ]]; then
  secure_path="/Volumes/BigSkyAgSSD/BigSkyAg/00_Admin/API_Secrets/$(basename "$secret_path")"
  mkdir -p "/Volumes/BigSkyAgSSD/BigSkyAg/00_Admin/API_Secrets"
  cp "$secret_path" "$secure_path"
  echo "✅ Moved to: $secure_path"
  rm "$secret_path"
else
  echo "⚠️  No file provided. Skipping move step."
fi

# Add .gitignore rules
echo -e "\n# Ignore secrets and large files" >> .gitignore
echo "00_Admin/API_Secrets/" >> .gitignore
echo "*.json" >> .gitignore
echo "*.zip" >> .gitignore
echo "*.tif" >> .gitignore
echo "*.shp" >> .gitignore
echo "*.geojson" >> .gitignore
echo "✅ .gitignore updated"

# Clean Git history
if [[ -n "$secret_path" ]]; then
  echo "🧹 Cleaning Git history with filter-repo..."
  git filter-repo --path "$secret_path" --invert-paths --force
fi

# Commit and push
git add .gitignore
git commit -m "Cleaned repo for demo use, removed sensitive files"
git push origin main --force

echo "🎉 Repo cleaned, secrets removed, pushed to GitHub"

