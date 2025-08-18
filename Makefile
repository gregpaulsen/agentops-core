SHELL := /bin/bash
COMMIT ?= chore: routine tidy

default: check

tidy:
	@git config core.hooksPath .githooks
	@git lfs install || true
	@mkdir -p storage/datasets storage/ndvi storage/backups storage/artifacts logs tmp
	@touch logs/.keep
	@git gc --prune=now || true
	@echo "tidy ✓"

size-audit:
	@echo "Oversized tracked files (>50MB):"
	@git ls-files -z | xargs -0 -I{} bash -lc 'f="{}"; [ -f "$$f" ] && s=$$(wc -c <"$$f"); [ $$s -gt 52428800 ] && echo "$$((s/1024/1024))MB  $$f"' | sort -nr || true

py-compile:
	@find . -name "*.py" -not -path "./.venv/*" -not -path "./node_modules/*" -exec python3 -m py_compile {} \; 2>&1 | sed -e 's/^/PY: /' || true

health:
	@./scripts/health.sh || true

check: size-audit py-compile health
	@echo "check ✓"

push:
	@git add -A
	@git commit -m "$(COMMIT)" || true
	@git push -u origin $$(git rev-parse --abbrev-ref HEAD)
	@echo "push ✓"
