# Development Workflow

## Quick Start

1. **Create feature branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Use Cursor/Claude for generation**
   - Open in Cursor for AI-assisted development
   - Use Claude for code generation and review

3. **Stage hunks, commit small**
   ```bash
   git add -p  # Review changes interactively
   git commit -m "feat: add new feature"
   ```

4. **Run tests**
   ```bash
   make test
   ```

5. **Open PR with checklist**
   - Use the PR template
   - Ensure all checklist items are completed

## Development Environment

### VS Code Dev Container
- Command Palette → "Dev Containers: Reopen in Container"
- Identical environment across all developers
- All tools pre-installed and configured

### Local Development
```bash
# Setup
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
pre-commit install

# Development
make format    # Format code
make lint      # Check for issues
make test      # Run tests
```

## Code Quality

- **Pre-commit hooks** automatically format and lint on commit
- **CI/CD** runs on every PR and push to main
- **Black** for code formatting (100 char line length)
- **Ruff** for linting and import sorting
- **Pytest** for testing

## Project Structure

- `service/` - FastAPI backend
- `ui/` - Next.js frontend
- `bigsky-agent/` - Legacy automation scripts
- `paulyops-core/` - Core utilities
- `tests/` - Test files
- `docs/` - Documentation

## Important Notes

- **Backups**: All backups go to `00_Admin/Backups/` (excluded from Git)
- **Legacy**: No references to `07_Backups` (migrated to `00_Admin/Backups`)
- **Config**: Use `INGEST_FOLDER_NAME` for dropzone configuration (default: `BigSkyAgDropzone`)
- **Secrets**: Use `.env` file, never commit credentials
