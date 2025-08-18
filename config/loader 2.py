from __future__ import annotations
import os, json
from pathlib import Path
from typing import Any, Dict, Optional

# YAML support is optional; we degrade gracefully if not installed
try:
    import yaml  # type: ignore
except Exception:
    yaml = None  # noqa

# TOML: Python 3.11+ has tomllib; else try tomli if present
try:
    import tomllib  # type: ignore
except Exception:
    tomllib = None  # noqa

def project_root(start: Optional[Path] = None) -> Path:
    p = (start or Path(__file__)).resolve()
    for _ in range(6):
        if (p / ".git").exists() or (p / ".projectroot").exists():
            return p
        p = p.parent
    return Path(__file__).resolve().parents[2]

BASE_DIR = project_root(Path(__file__))

def load_env(dotenv: Optional[Path] = None) -> None:
    """
    Loads .env if python-dotenv is available; otherwise no-op.
    """
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv(dotenv_path=str(dotenv or (BASE_DIR / ".env")), override=False)
    except Exception:
        # best-effort only
        pass

def get_env(key: str, default: Optional[str] = None, required: bool = False) -> str:
    val = os.getenv(key, default)
    if required and (val is None or val == ""):
        raise RuntimeError(f"Missing required env var: {key}")
    return "" if val is None else str(val)

def _read_yaml(p: Path) -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML not installed; cannot read YAML config.")
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def _read_json(p: Path) -> Dict[str, Any]:
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def _read_toml(p: Path) -> Dict[str, Any]:
    if tomllib is None:
        try:
            import tomli as tomllib  # type: ignore
        except Exception:
            raise RuntimeError("No TOML reader available (tomllib/tomli).")
    with p.open("rb") as f:
        return tomllib.load(f) or {}

def load_config(path: Optional[Path] = None, defaults: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Loads config from YAML/JSON/TOML into a dict.
    Search order if path not provided: config/app.yaml, app.yaml, config/app.json, app.json, pyproject.toml
    """
    candidates = []
    if path:
        candidates = [Path(path)]
    else:
        candidates = [
            BASE_DIR / "config" / "app.yaml",
            BASE_DIR / "app.yaml",
            BASE_DIR / "config" / "app.yml",
            BASE_DIR / "config" / "app.json",
            BASE_DIR / "app.json",
            BASE_DIR / "pyproject.toml",
        ]

    data: Dict[str, Any] = {}
    for p in candidates:
        if not p.exists():
            continue
        if p.suffix in (".yaml", ".yml"):
            data = _read_yaml(p)
            break
        if p.suffix == ".json":
            data = _read_json(p)
            break
        if p.suffix == ".toml" or p.name == "pyproject.toml":
            try:
                raw = _read_toml(p)
                # common location if you put config under [tool.paulyops]
                data = raw.get("tool", {}).get("paulyops", raw)
            except Exception:
                raise
            break

    if defaults:
        # defaults only fill missing keys
        merged = defaults.copy()
        merged.update(data or {})
        return merged
    return data or {}

def path_in_project(*parts: str) -> Path:
    return (BASE_DIR.joinpath(*parts)).resolve()
