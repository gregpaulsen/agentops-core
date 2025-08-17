# Developer Guide

## Overview

This guide covers development workflows, testing, and contribution guidelines for PaulyOps.

## Development Environment

### Prerequisites

- Python 3.11+
- Node.js 18+ (for UI development)
- Git
- VS Code or Cursor

### Setup

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd repo-size-check
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -U pip
   pip install -r requirements.txt -r requirements-dev.txt
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

### Dev Container (VS Code)

1. **Open in Dev Container**
   - Install Dev Containers extension
   - Command Palette → "Dev Containers: Reopen in Container"

2. **Container includes**
   - Python 3.11
   - Git
   - Docker
   - All development tools

## Code Quality

### Linting and Formatting

```bash
# Format code
make format

# Lint code
make lint

# Run both
make precommit
```

### Pre-commit Hooks

Automatically run on commit:
- Black (code formatting)
- Ruff (linting)
- isort (import sorting)

### Manual Checks

```bash
# Check formatting
black --check .

# Check linting
ruff check .

# Check imports
isort --check-only .
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_e2e_ingest.py

# Run with markers
pytest -m "local"
pytest -m "not s3 and not dropbox"
```

### Test Markers

- `@pytest.mark.local`: Local storage tests
- `@pytest.mark.s3`: S3 storage tests
- `@pytest.mark.dropbox`: Dropbox tests
- `@pytest.mark.google`: Google Drive tests
- `@pytest.mark.integration`: Integration tests

### Writing Tests

```python
def test_example():
    """Test example function."""
    result = example_function("input")
    assert result == "expected_output"

@pytest.mark.local
def test_local_storage():
    """Test local storage functionality."""
    # Test implementation
    pass
```

## Branching Strategy

### Branch Naming

- `feat/feature-name`: New features
- `fix/bug-description`: Bug fixes
- `infra/infrastructure`: Infrastructure changes
- `docs/documentation`: Documentation updates

### Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feat/new-feature
   ```

2. **Make changes**
   - Write code
   - Add tests
   - Update documentation

3. **Run checks**
   ```bash
   make format
   make lint
   pytest
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push and create PR**
   ```bash
   git push origin feat/new-feature
   ```

## Pull Request Process

### PR Checklist

- [ ] Branch named `feat/*` or `fix/*` or `infra/*`
- [ ] `make format` and `make lint` pass
- [ ] `pytest` passes locally
- [ ] No secrets committed; `.env` used
- [ ] Removed/avoided any references to `07_Backups`
- [ ] Verified `00_Admin/Backups` stays out of Git & CI
- [ ] Updated docs/comments where logical

### PR Template

```markdown
## Summary
- What changed and why

## Checklist
- [ ] Branch named `feat/*` or `fix/*` or `infra/*`
- [ ] `make format` and `make lint` pass
- [ ] `pytest` passes locally
- [ ] No secrets committed; `.env` used
- [ ] Removed/avoided any references to `07_Backups`
- [ ] Verified `00_Admin/Backups` stays out of Git & CI
- [ ] Updated docs/comments where logical
```

## CI/CD

### GitHub Actions

Automated checks on PR:
- Linting (Ruff, Black, isort)
- Testing (pytest)
- Security scanning

### Local CI

```bash
# Run CI checks locally
make ci
```

## Code Style

### Python

- **Formatting**: Black (100 character line length)
- **Linting**: Ruff
- **Imports**: isort
- **Type hints**: Use where helpful

### Documentation

- **Docstrings**: Google style
- **Comments**: Clear and concise
- **README**: Keep updated

## Architecture

### Project Structure

```
repo-size-check/
├── config/           # Configuration management
├── tenancy/          # Multi-tenant support
├── auth/             # Authentication
├── compliance/       # Compliance modes
├── rbac/             # Role-based access control
├── utils/            # Utilities
├── tests/            # Tests
├── docs/             # Documentation
├── plans/            # Plan configurations
├── tenants/          # Tenant configurations
└── reports/          # Generated reports
```

### Key Components

- **Config**: Environment-based configuration with tenant overrides
- **Tenancy**: Multi-tenant support with plans and branding
- **Auth**: Provider-agnostic OIDC/OAuth2
- **Compliance**: SOC2, PII masking, data residency
- **RBAC**: Role-based access control

## Debugging

### Logging

```python
from utils.logging import logger

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Debug Mode

```bash
export LOG_LEVEL=DEBUG
python your_script.py
```

### VS Code Debugging

1. **Set breakpoints** in code
2. **Create launch configuration**
3. **Start debugging** (F5)

## Performance

### Profiling

```bash
# Profile Python code
python -m cProfile -o profile.stats your_script.py

# Analyze results
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(10)"
```

### Memory Usage

```bash
# Monitor memory usage
python -m memory_profiler your_script.py
```

## Security

### Best Practices

- **Never commit secrets** to Git
- **Use environment variables** for sensitive data
- **Validate input** from external sources
- **Use secure defaults** for configuration

### Security Scanning

```bash
# Run security scan
bandit -r .

# Check for vulnerabilities
safety check
```

## Contributing

### Getting Started

1. **Fork repository**
2. **Create feature branch**
3. **Make changes**
4. **Add tests**
5. **Submit PR**

### Code Review

- **Review for security** issues
- **Check performance** implications
- **Verify documentation** updates
- **Test functionality**

### Release Process

1. **Update version** in `pyproject.toml`
2. **Update changelog**
3. **Create release** tag
4. **Deploy** to production
