#!/usr/bin/env python3
"""Validate SpyWatch datasets for schema, citations, cross-references, and data minimization."""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path

import yaml

from build_datasets import FBI_IN_SCOPE, OFAC_PREFIXES

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CONFIDENCE = {"confirmed", "high", "medium", "low", "disputed"}
TIMELINE_DATE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?|-\d{4})?$")
FORBIDDEN_KEYS = {
    "dob", "date_of_birth", "dates_of_birth_used", "place_of_birth", "height", "height_min", "height_max",
    "weight", "weight_min", "weight_max", "race", "race_raw", "sex", "eyes", "eyes_raw", "hair", "hair_raw",
    "complexion", "build", "scars_and_marks", "images", "remarks", "field_offices", "locations",
    "reward_min", "reward_max", "reward_text", "nationality", "address", "passport", "phone", "email",
}
ATTACK_PATH = "data/groups/mitre-attack-intrusion-sets.json"
GENERATED = {
    "data/wanted/fbi-wanted.json": (
        {"id", "title", "url", "published", "fbi_categories", "status", "aliases", "offense_summary",
         "related_actor_profiles", "related_attack_groups"},
        "id",
        "https://www.fbi.gov/wanted/",
    ),
    ATTACK_PATH: (
        {"id", "name", "url", "aliases", "local_profile_ids", "profile_status"},
        "id",
        "https://attack.mitre.org/groups/",
    ),
    "data/sanctions/ofac-cyber-dprk.json": (
        {"ent_num", "name", "sdn_type", "programs", "aliases", "related_actor_profiles", "related_attack_groups"},
        "ent_num",
        None,
    ),
    "data/advisories/ic3-psa-index.json": (
        {"id", "title", "url", "published"},
        "id",
        "https://www.ic3.gov/PSA/",
    ),
}


def actor_ids() -> set[str]:
    return {
        str(yaml.safe_load(path.read_text(encoding="utf-8"))["id"])
        for path in (DATA / "actors").rglob("*.yml")
        if path.name != "index.yml"
    }


def check_archive(errors: list[str]) -> set[str]:
    data = json.loads((DATA / "public-case-archive.json").read_text(encoding="utf-8"))
    ids: set[str] = set()
    for case in data.get("case_studies", []):
        case_id = str(case.get("id"))
        if case_id in ids:
            errors.append(f"archive: duplicate case id {case_id}")
        ids.add(case_id)
        if case.get("confidence") not in CONFIDENCE:
            errors.append(f"archive {case_id}: invalid confidence {case.get('confidence')!r}")
        if not case.get("sources"):
            errors.append(f"archive {case_id}: no sources")
        for source in case.get("sources", []):
            if not str(source.get("url", "")).startswith("https://"):
                errors.append(f"archive {case_id}: source {source.get('title')!r} is not an https URL")
    return ids | {str(item.get("id")) for item in data.get("backlog", [])}


def check_timeline(case_ids: set[str], errors: list[str]) -> None:
    data = json.loads((DATA / "timelines" / "public-intelligence-cases.json").read_text(encoding="utf-8"))
    for event in data.get("events", []):
        label = f"timeline {event.get('date')}"
        if not TIMELINE_DATE.match(str(event.get("date", ""))):
            errors.append(f"{label}: unrecognized date format")
        if event.get("case_id") not in case_ids:
            errors.append(f"{label}: unknown case_id {event.get('case_id')}")
        if not event.get("source"):
            errors.append(f"{label}: missing source")


def forbidden_paths(node: object, path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            child = f"{path}.{key}" if path else str(key)
            if str(key).lower() in FORBIDDEN_KEYS:
                found.append(child)
            found.extend(forbidden_paths(value, child))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(forbidden_paths(value, f"{path}[{index}]"))
    return found


def load_generated(relative: str, errors: list[str]) -> list[dict]:
    fields, id_key, prefix = GENERATED[relative]
    data = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    meta, records = data.get("meta", {}), data.get("records", [])
    for key in ("name", "source", "snapshot_date", "record_count"):
        if key not in meta:
            errors.append(f"{relative}: meta is missing {key}")
    if meta.get("record_count") != len(records):
        errors.append(f"{relative}: record_count does not match records")
    try:
        date.fromisoformat(str(meta.get("snapshot_date")))
    except ValueError:
        errors.append(f"{relative}: snapshot_date is not an ISO date")
    if not str(meta.get("source", "")).startswith("https://"):
        errors.append(f"{relative}: meta source must be https")
    seen: set[str] = set()
    for record in records:
        key = str(record.get(id_key))
        label = f"{relative} [{key}]"
        missing = fields - set(record)
        if missing:
            errors.append(f"{label}: missing {sorted(missing)}")
        if key in seen:
            errors.append(f"{label}: duplicate {id_key}")
        seen.add(key)
        if prefix and not str(record.get("url", "")).startswith(prefix):
            errors.append(f"{label}: url must start with {prefix}")
    for path in forbidden_paths(data):
        errors.append(f"{relative}: personal-data field '{path}' is not allowed")
    return records


def check_rules(relative: str, records: list[dict], errors: list[str], profile_ids: set[str], attack_ids: set[str]) -> None:
    for record in records:
        key = str(record.get("id", record.get("ent_num")))
        label = f"{relative} [{key}]"
        links = list(record.get("related_actor_profiles", []))
        links += [{"id": profile_id} for profile_id in record.get("local_profile_ids", [])]
        for link in links:
            if link.get("id") not in profile_ids:
                errors.append(f"{label}: unknown actor profile {link.get('id')}")
        for link in record.get("related_attack_groups", []):
            if link.get("id") not in attack_ids:
                errors.append(f"{label}: unknown ATT&CK group {link.get('id')}")
        if relative == ATTACK_PATH and (record.get("profile_status") == "profiled") != bool(record.get("local_profile_ids")):
            errors.append(f"{label}: profile_status disagrees with local_profile_ids")
        if relative.startswith("data/wanted/"):
            if not FBI_IN_SCOPE.intersection(record.get("fbi_categories", [])):
                errors.append(f"{label}: no in-scope FBI category")
            if record.get("published"):
                try:
                    datetime.fromisoformat(str(record["published"]))
                except ValueError:
                    errors.append(f"{label}: published is not an ISO datetime")
        if relative.startswith("data/sanctions/"):
            if not any(program.startswith(OFAC_PREFIXES) for program in record.get("programs", [])):
                errors.append(f"{label}: no cyber or DPRK program")
            if record.get("sdn_type") not in {"individual", "entity"}:
                errors.append(f"{label}: unexpected sdn_type {record.get('sdn_type')!r}")
        if relative.startswith("data/advisories/"):
            try:
                published = date.fromisoformat(str(record.get("published")))
            except ValueError:
                errors.append(f"{label}: published is not an ISO date")
                continue
            if record.get("id") != "PSA" + published.strftime("%y%m%d"):
                errors.append(f"{label}: identifier does not match published date")


def main() -> int:
    errors: list[str] = []
    profile_ids = actor_ids()
    case_ids = check_archive(errors)
    check_timeline(case_ids, errors)
    loaded = {relative: load_generated(relative, errors) for relative in GENERATED}
    attack_ids = {str(record["id"]) for record in loaded[ATTACK_PATH]}
    for relative, records in loaded.items():
        check_rules(relative, records, errors, profile_ids, attack_ids)
    for error in errors:
        print(f"[FAIL] {error}")
    if errors:
        print(f"{len(errors)} problem(s) found")
        return 1
    print(f"[ OK ] archive, timeline, and {len(GENERATED)} generated datasets validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
