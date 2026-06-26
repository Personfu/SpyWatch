#!/usr/bin/env python3
"""Validate SpyWatch actor YAML profiles."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency: pyyaml. Install with: python -m pip install pyyaml", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parents[1]
ACTOR_DIR = ROOT / "data" / "actors"
REQUIRED = {
    "id", "name", "country", "sponsor", "actor_type", "aliases",
    "confidence", "summary", "sectors", "defensive_notes", "sources", "last_reviewed",
}
CONFIDENCE = {"confirmed", "high", "medium", "low", "disputed"}


def iter_profiles() -> list[Path]:
    return sorted(p for p in ACTOR_DIR.rglob("*.yml") if p.name != "index.yml")


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    missing = sorted(REQUIRED - set(data))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")

    if data.get("confidence") and data["confidence"] not in CONFIDENCE:
        errors.append(f"invalid confidence: {data['confidence']}")

    for field in ["aliases", "sectors", "defensive_notes", "sources"]:
        if field in data and not isinstance(data[field], list):
            errors.append(f"{field} must be a list")

    for i, source in enumerate(data.get("sources", []) or []):
        if not isinstance(source, dict):
            errors.append(f"sources[{i}] must be an object")
            continue
        if not source.get("title") or not source.get("url"):
            errors.append(f"sources[{i}] must include title and url")

    return errors


def main() -> int:
    paths = iter_profiles()
    if not paths:
        print("No actor profiles found.", file=sys.stderr)
        return 1

    failed = False
    for path in paths:
        errors = validate_file(path)
        if errors:
            failed = True
            print(f"[FAIL] {path.relative_to(ROOT)}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"[ OK ] {path.relative_to(ROOT)}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
