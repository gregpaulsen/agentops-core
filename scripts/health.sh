#!/usr/bin/env bash
set -euo pipefail
ok(){ printf "✅ %s\n" "$*"; } warn(){ printf "⚠️  %s\n" "$*\n"; }
# storage & hooks
[ -d storage ] && ok "storage/ exists" || warn "storage/ missing"
[ -x .githooks/pre-commit ] && ok "pre-commit size guard installed" || warn "pre-commit guard missing"
# LFS + remote
git lfs version >/dev/null 2>&1 && ok "Git LFS installed" || warn "Git LFS not installed"
git remote get-url origin >/dev/null 2>&1 && ok "origin remote set" || warn "origin remote not set"
# tracked files > 50MB
big=$(git ls-files -z | xargs -0 -I{} bash -lc 'f="{}"; [ -f "$f" ] && s=$(wc -c <"$f"); [ "$s" -gt 52428800 ] && echo "$f"' | wc -l | tr -d ' ')
[ "$big" -eq 0 ] && ok "No oversized tracked files" || warn "$big tracked file(s) >50MB"
# python compile smoke
errs=0
find . -name "*.py" -not -path "./.venv/*" -not -path "./node_modules/*" -exec python3 -m py_compile {} \; 2>&1 | sed -e 's/^/PY: /' || errs=$?
[ "$errs" -eq 0 ] && ok "Python compile clean (or no errors surfaced)" || warn "Python compile surfaced messages"
exit 0
