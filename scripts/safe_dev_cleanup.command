#!/usr/bin/env bash
# safe_dev_cleanup.command  — Safe macOS dev cleanup
set -euo pipefail

LOG="${HOME}/Desktop/safe_dev_cleanup.log"
MODE="audit"   # audit | standard | full
YES="false"
DEV_DIR="${HOME}/Dev"
PROJECTS_DIR="${HOME}/Projects"

say() { printf "%s\n" "$*" | tee -a "$LOG"; }
hr() { say "----------------------------------------"; }
ts() { date "+%Y-%m-%d_%H-%M-%S"; }

ensure_mac() {
  if [[ "$(uname -s)" != "Darwin" ]]; then
    say "This script is macOS-only. Exiting."; exit 1
  fi
}

usage() {
  cat <<EOF
Usage: $(basename "$0") [--audit|--standard|--full] [--yes]
                       [--dev-dir PATH] [--projects-dir PATH]

  --audit        Report only (default)
  --standard     Safe cleanup (no Docker/Git by default)
  --full         Includes prompts for Docker, Git, and Homebrew
  --yes          Non-interactive; accept safe defaults for chosen mode
  --dev-dir      Root of dev projects (default: ~/Dev)
  --projects-dir Root of projects (default: ~/Projects)
EOF
}

confirm() {
  local prompt="$1"
  if [[ "$YES" == "true" ]]; then return 0; fi
  read -r -p "$prompt [YES/no]: " ans
  [[ "$ans" == "YES" ]]
}

to_trash() {
  local target="$1"
  if [[ ! -e "$target" ]]; then return 0; fi
  local base="$(basename "$target")"
  local dest="${HOME}/.Trash/${base}_$(ts)"
  say "→ Moving to Trash: $target"
  mv "$target" "$dest" 2>/dev/null || {
    say "⚠️ Could not move $target to Trash (possibly different volume). Skipping."
    return 1
  }
}

size_of() {
  local path="$1"
  [[ -e "$path" ]] && du -sh "$path" 2>/dev/null | awk '{print $1}' || echo "0B"
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --audit) MODE="audit";;
      --standard) MODE="standard";;
      --full) MODE="full";;
      --yes) YES="true";;
      --dev-dir) DEV_DIR="${2:-$DEV_DIR}"; shift;;
      --projects-dir) PROJECTS_DIR="${2:-$PROJECTS_DIR}"; shift;;
      -h|--help) usage; exit 0;;
      *) say "Unknown arg: $1"; usage; exit 1;;
    esac
    shift
  done
}

audit() {
  hr; say "📊 AUDIT START $(ts)"; hr
  df -h / | tee -a "$LOG"
  hr; say "Top CPU:"; ps aux | sort -nrk 3 | head -10 | tee -a "$LOG"
  hr; say "Top MEM:"; ps aux | sort -nrk 4 | head -10 | tee -a "$LOG"
  hr; say "Largest under ~:"; du -hd 1 ~ | sort -hr | head -12 | tee -a "$LOG"

  # Common caches
  say ""; hr; say "Cache sizes (report only):"
  local items=(
    "${HOME}/.npm"
    "${HOME}/Library/Caches/Yarn"
    "${HOME}/Library/pnpm/store"
    "${HOME}/.cache/pip"
    "${HOME}/Library/Application Support/Code/Cache"
    "${HOME}/Library/Application Support/Code/CachedData"
    "${HOME}/Library/Application Support/Cursor/Cache"
    "${HOME}/Library/Developer/Xcode/DerivedData"
    "${HOME}/Library/Logs"
    "${HOME}/Library/Caches"
  )
  for p in "${items[@]}"; do
    say "$(printf '%-70s' "$p"): $(size_of "$p")"
  done

  # Optional tools
  if command -v brew >/dev/null 2>&1; then
    say ""; hr; say "Homebrew cache:"; brew --cache | xargs du -sh 2>/dev/null | tee -a "$LOG" || true
  fi
  if command -v docker >/dev/null 2>&1; then
    say ""; hr; say "Docker disk usage:"; docker system df || true
  fi

  # Project junk (report)
  say ""; hr; say "Scanning project junk in: $DEV_DIR and $PROJECTS_DIR"
  find "$DEV_DIR" "$PROJECTS_DIR" -type d \( -name ".next" -o -name "dist" -o -name "build" -o -name "coverage" \) -maxdepth 4 2>/dev/null | tee -a "$LOG" || true
  find "$DEV_DIR" "$PROJECTS_DIR" -type d -name "__pycache__" -maxdepth 6 2>/dev/null | tee -a "$LOG" || true
}

close_heavy_apps() {
  hr; say "🔻 Offer to quit heavy apps"
  if confirm "Quit Chrome, Slack, Discord, Docker Desktop, Simulator, Xcode?"; then
    osascript -e 'quit app "Google Chrome"' || true
    osascript -e 'quit app "Slack"' || true
    osascript -e 'quit app "Discord"' || true
    osascript -e 'quit app "Docker Desktop"' || true
    osascript -e 'quit app "Simulator"' || true
    osascript -e 'quit app "Xcode"' || true
  fi
}

clean_js() {
  hr; say "🧹 JS/Node caches"
  command -v npm >/dev/null && npm cache verify || true
  if command -v npm >/dev/null && confirm "Run 'npm cache clean --force'?"; then npm cache clean --force || true; fi
  command -v yarn >/dev/null && confirm "Run 'yarn cache clean'?" && yarn cache clean || true
  command -v pnpm >/dev/null && confirm "Run 'pnpm store prune'?" && pnpm store prune || true

  # Project build junk
  if confirm "Move common build caches (dist/build/coverage/.next/cache/node_modules/.cache) in $DEV_DIR and $PROJECTS_DIR to Trash?"; then
    mapfile -t targets < <(find "$DEV_DIR" "$PROJECTS_DIR" -type d \( -name "dist" -o -name "build" -o -name "coverage" -o -path "*/.next/cache" -o -path "*/node_modules/.cache" \) 2>/dev/null)
    for t in "${targets[@]}"; do to_trash "$t"; done
  fi
}

clean_python() {
  hr; say "🐍 Python caches"
  local pipc="${HOME}/.cache/pip"
  say "pip cache: $(size_of "$pipc")"
  confirm "Move pip cache to Trash?" && to_trash "$pipc" || true
  if confirm "Move all __pycache__ dirs under $DEV_DIR and $PROJECTS_DIR to Trash?"; then
    mapfile -t pyc < <(find "$DEV_DIR" "$PROJECTS_DIR" -type d -name "__pycache__" 2>/dev/null)
    for d in "${pyc[@]}"; do to_trash "$d"; done
  fi
}

clean_editors() {
  hr; say "📝 VS Code / Cursor caches"
  local vsc1="${HOME}/Library/Application Support/Code/Cache"
  local vsc2="${HOME}/Library/Application Support/Code/CachedData"
  local cur="${HOME}/Library/Application Support/Cursor/Cache"
  say "VS Code Cache: $(size_of "$vsc1")"
  say "VS Code CachedData: $(size_of "$vsc2")"
  say "Cursor Cache: $(size_of "$cur")"
  confirm "Move these editor caches to Trash?" && {
    to_trash "$vsc1"; to_trash "$vsc2"; to_trash "$cur"
  }
}

clean_xcode() {
  local dd="${HOME}/Library/Developer/Xcode/DerivedData"
  if [[ -d "$dd" ]]; then
    hr; say "🧱 Xcode DerivedData: $(size_of "$dd")"
    confirm "Move Xcode DerivedData to Trash?" && to_trash "$dd"
  fi
}

system_maint() {
  hr; say "⚙️ System maintenance (optional)"
  command -v sudo >/dev/null 2>&1 && confirm "Flush DNS cache?" && {
    sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder || true
  }
  confirm "Rebuild LaunchServices (fixes slow 'Open With')?" && {
    /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user || true
  }
  confirm "Clear Quick Look cache?" && { qlmanage -r cache || true; }
}

brew_clean() {
  if command -v brew >/dev/null 2>&1; then
    hr; say "🍺 Homebrew"
    confirm "brew update + cleanup -s ?" && {
      brew update || true
      brew cleanup -s || true
    }
  fi
}

docker_clean() {
  if command -v docker >/dev/null 2>&1; then
    hr; say "🐳 Docker"
    docker system df || true
    confirm "Run 'docker system prune'?" && docker system prune -f || true
    confirm "Run 'docker image prune -a' (aggressive)?" && docker image prune -a -f || true
  fi
}

git_housekeeping() {
  hr; say "🌿 Git housekeeping"
  if confirm "Run 'git gc --prune=now --aggressive' and 'git remote prune origin' on repos under $DEV_DIR and $PROJECTS_DIR?"; then
    mapfile -t repos < <(find "$DEV_DIR" "$PROJECTS_DIR" -type d -name ".git" 2>/dev/null | xargs -I{} dirname {})
    for r in "${repos[@]}"; do
      say "→ $r"
      (cd "$r" && git gc --prune=now --aggressive && git remote prune origin) || true
    done
  fi
}

logs_and_trash() {
  hr; say "🗑 Logs & Trash"
  local logs="${HOME}/Library/Logs"
  say "Logs dir: $(size_of "$logs")"
  confirm "Move old logs to Trash?" && to_trash "$logs"
  confirm "Empty Trash now?" && rm -rf "${HOME}/.Trash/"* || true
}

summary() {
  hr; say "✅ DONE $(ts)"
  say "Tip: consider a reboot if many apps/caches were closed."
  say "Log: $LOG"
}

main() {
  : > "$LOG"
  ensure_mac
  parse_args "$@"
  audit

  [[ "$MODE" == "audit" ]] && { say "Run with --standard or --full to clean."; exit 0; }

  close_heavy_apps
  clean_js
  clean_python
  clean_editors
  clean_xcode
  system_maint

  if [[ "$MODE" == "full" ]]; then
    brew_clean
    docker_clean
    git_housekeeping
  fi

  logs_and_trash
  summary
}

main "$@"
