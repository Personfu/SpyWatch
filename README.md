# SpyWatch

SpyWatch is a defensive public-source intelligence library for studying foreign intelligence activity, cyber threat groups, hybrid operations, and eCrime ecosystems.

This repository is intended for education, journalism, policy research, and security defense. It organizes public reporting into structured profiles with aliases, country alignment, known public reporting, confidence notes, and defensive lessons.

## Scope

SpyWatch tracks:

- state intelligence and military cyber units;
- state-aligned cyber espionage clusters;
- hybrid warfare and influence operators;
- major eCrime groups;
- historic intelligence organizations when they help explain modern patterns.

## Safety boundary

SpyWatch is a research catalog, not an attack manual. Content should remain high-level, sourced, defensive, and non-operational.

Do not add private personal information, unverified accusations, target lists, intrusion instructions, credential collection guidance, or executable harmful content.

## Repository map

```text
docs/                  Research policy, taxonomy, and watchlist
schema/                Machine-readable actor profile schema
data/actors/           YAML profiles for public-source actor research
prompts/               Safe AI-assisted enrichment prompts
scripts/               Validation and index tools
.github/workflows/     CI validation
```

## Current build plan

1. Define the profile schema.
2. Add a global watchlist.
3. Seed actor profiles for Russia, China, Iran, and North Korea.
4. Add validation scripts.
5. Add continuous validation through GitHub Actions.
6. Expand each profile with sourced, defensive context over time.

## Local validation

```bash
python scripts/validate_actors.py
python scripts/build_index.py
```

## Attribution note

Attribution is probabilistic. Different governments and vendors use different names for the same or overlapping clusters. SpyWatch therefore separates public claims, aliases, confidence levels, and analytic notes.
