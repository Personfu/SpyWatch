#!/usr/bin/env python3
"""Rebuild SpyWatch's machine-readable public-record datasets from official sources."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import date, datetime
from html import unescape
from io import StringIO
from pathlib import Path
from urllib.request import Request, urlopen

import yaml

ROOT = Path(__file__).resolve().parents[1]
ACTOR_DIR = ROOT / "data" / "actors"
SNAPSHOT_DATE = date.today().isoformat()
USER_AGENT = "SpyWatch public records index/1.0"

ATTACK_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
FBI_API = "https://api.fbi.gov/wanted/v1/list"
OFAC_SDN_URL = "https://www.treasury.gov/ofac/downloads/sdn.csv"
OFAC_ALT_URL = "https://www.treasury.gov/ofac/downloads/alt.csv"
IC3_PSA_URL = "https://www.ic3.gov/PSA"

FBI_IN_SCOPE = {
    "Ten Most Wanted Fugitives",
    "Cyber's Most Wanted",
    "Most Wanted Fraudster",
    "White-Collar Crime",
    "Counterintelligence",
    "Transnational Repression",
    "China Threat",
    "Iran",
    "Most Wanted Terrorists",
    "Seeking Information - Terrorism",
    "Domestic Terrorism",
}
FBI_SUBJECT_FIXES = {"While-Collar Crime": "White-Collar Crime"}
OFAC_PREFIXES = ("CYBER", "DPRK", "NKOREA")
OFAC_SDN_TYPES = {"individual": "individual", "-0-": "entity"}  # OFAC marks entity records with "-0-"
GENERIC_TOKENS = {
    "activities", "actor", "actors", "cyber", "espionage", "group", "groups",
    "hackers", "members", "subjects", "team", "threat", "unit", "workers",
}
MIN_KEY_LENGTH = 4
MATCH_RULE = (
    "Exact match after splitting names on '/', removing generic words such as group, cyber, actors, and unit, "
    "and requiring at least four remaining characters. A match is a research link, not an attribution finding."
)
PSA_LINK = re.compile(r'<a[^>]*href="/PSA/(\d{4})/(PSA(\d{6}))"[^>]*>(.*?)</a>', re.S)


def fetch(url: str, timeout: int = 60) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    failure: Exception | None = None
    for _ in range(3):
        try:
            with urlopen(request, timeout=timeout) as response:
                return response.read()
        except OSError as error:
            failure = error
    raise RuntimeError(f"could not fetch {url}: {failure}")


def clean_text(value: object) -> str:
    text = re.sub(r"<[^>]*>", " ", str(value or ""))
    return re.sub(r"\s+", " ", unescape(text)).strip()


def unique(values: list[object]) -> list[str]:
    seen: dict[str, str] = {}
    for value in values:
        text = clean_text(value)
        if text:
            seen.setdefault(text.casefold(), text)
    return sorted(seen.values(), key=str.casefold)


def name_keys(names: list[object]) -> dict[str, str]:
    keys: dict[str, str] = {}
    for name in names:
        for part in clean_text(name).split("/"):
            tokens = re.findall(r"[a-z0-9]+", part.casefold())
            key = "".join(token for token in tokens if token not in GENERIC_TOKENS)
            if len(key) >= MIN_KEY_LENGTH:
                keys.setdefault(key, clean_text(part))
    return keys


def link_names(source_names: list[object], candidate_names: list[object]) -> list[dict[str, str]]:
    source = name_keys(source_names)
    candidate = name_keys(candidate_names)
    return [
        {"matched_text": source[key], "candidate_text": candidate[key]}
        for key in sorted(source.keys() & candidate.keys())
    ]


def load_actor_profiles() -> list[dict]:
    profiles = []
    for path in sorted(ACTOR_DIR.rglob("*.yml")):
        if path.name == "index.yml":
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        profiles.append({
            "id": data["id"],
            "name": data["name"],
            "aliases": [str(alias) for alias in data.get("aliases") or []],
        })
    return profiles


def profile_hits(names: list[object], profiles: list[dict]) -> list[dict]:
    hits = []
    for profile in profiles:
        matches = link_names(names, [profile["name"], *profile["aliases"]])
        if matches:
            hits.append({"id": profile["id"], "name": profile["name"], "matched_text": matches[0]["matched_text"]})
    return hits


def related_links(names: list[object], profiles: list[dict], attack_groups: list[dict]) -> tuple[list[dict], list[dict]]:
    attack = []
    for group in attack_groups:
        matches = link_names(names, [group["name"], *group["aliases"]])
        if matches:
            attack.append({"id": group["id"], "name": group["name"], "matched_text": matches[0]["matched_text"]})
    return profile_hits(names, profiles), attack


def build_attack_groups(profiles: list[dict]) -> list[dict]:
    bundle = json.loads(fetch(ATTACK_URL, timeout=180))
    groups = []
    for obj in bundle["objects"]:
        if obj.get("type") != "intrusion-set" or obj.get("revoked") or obj.get("x_mitre_deprecated"):
            continue
        ref = next((item for item in obj.get("external_references", []) if item.get("source_name") == "mitre-attack"), None)
        if ref is None:
            continue
        aliases = unique([obj["name"], *obj.get("aliases", [])])
        hits = profile_hits(aliases, profiles)
        groups.append({
            "id": ref["external_id"],
            "name": obj["name"],
            "url": ref["url"],
            "aliases": aliases,
            "local_profile_ids": sorted({hit["id"] for hit in hits}),
            "profile_status": "profiled" if hits else "not_profiled",
        })
    return sorted(groups, key=lambda group: group["id"])


def fetch_fbi_items() -> list[dict]:
    def page(number: int) -> dict:
        return json.loads(fetch(f"{FBI_API}?page={number}&pageSize=50", timeout=60))

    first = page(1)
    total = int(first["total"])
    items = list(first["items"])
    number = 2
    while len(items) < total:
        batch = page(number)["items"]
        if not batch:
            raise RuntimeError(f"FBI API returned no items on page {number}")
        items.extend(batch)
        number += 1
    if len({item["uid"] for item in items}) != total:
        raise RuntimeError("FBI API returned duplicate or missing records")
    return items


def fbi_categories(item: dict) -> list[str]:
    raw = item.get("subjects") or []
    values = [raw] if isinstance(raw, str) else raw
    return sorted({FBI_SUBJECT_FIXES.get(value, value) for value in values})


def split_aliases(raw: object) -> list[str]:
    values = re.split(r"[,;]", raw) if isinstance(raw, str) else (raw or [])
    return unique([str(value).strip().strip("\"'") for value in values])


def build_fbi(profiles: list[dict], attack_groups: list[dict]) -> tuple[dict, list[dict]]:
    records = []
    for item in fetch_fbi_items():
        categories = fbi_categories(item)
        if not FBI_IN_SCOPE.intersection(categories):
            continue
        title = clean_text(item.get("title"))
        aliases = split_aliases(item.get("aliases"))
        actors, attack = related_links([title, *aliases], profiles, attack_groups)
        status = clean_text(item.get("status")).lower()
        records.append({
            "id": item["uid"],
            "title": title,
            "url": item["url"],
            "published": item.get("publication"),
            "modified": item.get("modified"),
            "fbi_categories": categories,
            "status": None if status in {"", "na"} else status,
            "aliases": aliases,
            "offense_summary": clean_text(item.get("description"))[:700],
            "related_actor_profiles": actors,
            "related_attack_groups": attack,
        })
    records.sort(key=lambda record: record["title"].casefold())
    meta = {
        "name": "FBI wanted notices, selected threat categories",
        "source": FBI_API,
        "included_fbi_categories": sorted(FBI_IN_SCOPE),
        "status_counts": dict(Counter(record["status"] or "not reported" for record in records)),
        "note": "Published notices and FBI-reported status at snapshot time. A notice is not a conviction; check the linked FBI page before relying on status.",
        "data_minimization": "Excludes dates of birth, physical descriptors, images, locations, reward amounts, and remarks.",
        "profile_match_rule": MATCH_RULE,
    }
    return meta, records


def fetch_csv(url: str) -> list[list[str]]:
    return list(csv.reader(StringIO(fetch(url, timeout=120).decode("utf-8", errors="replace"))))


def build_ofac(profiles: list[dict], attack_groups: list[dict]) -> tuple[dict, list[dict]]:
    selected: dict[str, dict] = {}
    for row in fetch_csv(OFAC_SDN_URL):
        if len(row) < 4:
            continue
        ent_num = row[0].strip()
        programs = sorted(set(re.findall(r"[A-Z][A-Z0-9-]+", row[3])))
        sdn_type = OFAC_SDN_TYPES.get(row[2].strip())
        if sdn_type is None or not any(program.startswith(OFAC_PREFIXES) for program in programs):
            continue
        selected[ent_num] = {
            "ent_num": ent_num,
            "name": clean_text(row[1]),
            "sdn_type": sdn_type,
            "programs": programs,
            "aliases": [],
        }
    for row in fetch_csv(OFAC_ALT_URL):
        if len(row) >= 4 and row[0].strip() in selected:
            selected[row[0].strip()]["aliases"].append(row[3])
    records = []
    for entry in selected.values():
        entry["aliases"] = unique(entry["aliases"])
        entry["related_actor_profiles"], entry["related_attack_groups"] = related_links(
            [entry["name"], *entry["aliases"]], profiles, attack_groups
        )
        records.append(entry)
    records.sort(key=lambda record: record["name"].casefold())
    meta = {
        "name": "OFAC SDN entries under cyber and DPRK programs",
        "source": OFAC_SDN_URL,
        "alias_source": OFAC_ALT_URL,
        "included_program_prefixes": list(OFAC_PREFIXES),
        "included_sdn_types": sorted(set(OFAC_SDN_TYPES.values())),
        "note": "Sanctions designations are administrative measures, not criminal convictions. Verify current status on OFAC's sanctions list service.",
        "data_minimization": "Excludes remarks, titles, call signs, addresses, dates of birth, identifiers, and vessel or aircraft records.",
        "profile_match_rule": MATCH_RULE,
    }
    return meta, records


def build_ic3() -> tuple[dict, list[dict]]:
    html = fetch(IC3_PSA_URL).decode("utf-8", errors="replace")
    found: dict[str, dict] = {}
    for year, psa_id, code, label in PSA_LINK.findall(html):
        published = datetime.strptime(code, "%y%m%d").date()
        if published.year != int(year):
            raise RuntimeError(f"{psa_id} does not match URL year {year}")
        title = clean_text(label) or psa_id
        current = found.get(psa_id)
        if current is None or current["title"] == psa_id:
            found[psa_id] = {
                "id": psa_id,
                "title": title,
                "url": f"https://www.ic3.gov/PSA/{year}/{psa_id}",
                "published": published.isoformat(),
            }
    records = sorted(found.values(), key=lambda record: record["published"], reverse=True)
    meta = {
        "name": "IC3 public service announcements, index page",
        "source": IC3_PSA_URL,
        "note": "PSAs linked from the IC3 index at snapshot time; not a complete archive. Dates come from the PSA identifier and are checked against the URL year. Warnings describe reported patterns, not findings about named people.",
    }
    return meta, records


def write_dataset(relative: str, meta: dict, records: list[dict]) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"meta": {**meta, "snapshot_date": SNAPSHOT_DATE, "record_count": len(records)}, "records": records}
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(records)} records to {relative}")


def main() -> int:
    profiles = load_actor_profiles()
    attack_groups = build_attack_groups(profiles)
    attack_meta = {
        "name": "MITRE ATT&CK intrusion-set aliases",
        "source": ATTACK_URL,
        "note": "Derived from MITRE ATT&CK Enterprise data. Cite MITRE ATT&CK when reusing. Aliases are naming labels, not proof of attribution.",
        "profile_match_rule": MATCH_RULE,
    }
    write_dataset("data/groups/mitre-attack-intrusion-sets.json", attack_meta, attack_groups)
    write_dataset("data/wanted/fbi-wanted.json", *build_fbi(profiles, attack_groups))
    write_dataset("data/sanctions/ofac-cyber-dprk.json", *build_ofac(profiles, attack_groups))
    write_dataset("data/advisories/ic3-psa-index.json", *build_ic3())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
