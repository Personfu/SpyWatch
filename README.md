# SpyWatch

SpyWatch is a defensive public-source intelligence library for studying foreign intelligence services, state-aligned cyber groups, hybrid operations, deep-cover networks, and major eCrime ecosystems.

It is built for students, defenders, journalists, researchers, and policy teams who need structured context without turning that research into an offensive playbook.

## Mission

SpyWatch organizes public reporting into clean, sourced profiles:

- who the actor is alleged or assessed to be;
- who tracks it under what names;
- what country, service, or ecosystem it is associated with;
- what sectors appear in public reporting;
- what historical cases define the actor;
- what defenders should learn from the case;
- how confident the public record is.

## Safety line

SpyWatch is a catalog and teaching library. It does not include private personal information, live target lists, credential collection guidance, intrusion instructions, or executable harmful material.

## Repository map

```text
.github/workflows/validate.yml        CI validation
CONTRIBUTING.md                       contribution rules
docs/source-policy.md                 source standards and confidence rules
docs/taxonomy.md                      actor taxonomy
docs/watchlist.md                     global research backlog
docs/illegals-program.md              deep-cover illegals case-study framework
docs/research-playbook.md             safe research workflow
docs/defender-briefings.md            defensive briefing templates
schema/actor.schema.json              actor profile schema
data/actors/index.yml                 actor index
data/actors/*/*.yml                   actor profiles
prompts/openai-enrichment.md          safe enrichment workflow
scripts/build_index.py                rebuilds the actor index
scripts/validate_actors.py            validates actor YAML
```

## Seed profile coverage

### Russia

- GRU Unit 29155 / Cadet Blizzard / Ember Bear / UNC2589
- GRU Unit 74455 / Sandworm
- GRU Unit 26165 / APT28 / Fancy Bear
- SVR APT29 / Cozy Bear / Midnight Blizzard
- Star Blizzard / Callisto Group
- Turla / Snake

### China

- APT41 / Double Dragon
- PLA Unit 61398 / APT1
- Storm-0558
- Volt Typhoon
- APT10 / Stone Panda

### Iran

- MuddyWater / Mango Sandstorm
- Charming Kitten / APT35
- APT33 / Elfin
- APT34 / OilRig

### North Korea

- Lazarus Group / Hidden Cobra
- APT38
- Kimsuky
- Andariel

## Local use

```bash
python -m pip install pyyaml
python scripts/validate_actors.py
python scripts/build_index.py
```

## Profile model

Each actor profile uses YAML with a shared schema. Example fields:

```yaml
id: ru-gru-29155
name: GRU Unit 29155
country: Russia
sponsor: GRU / Main Directorate of the General Staff
actor_type: military intelligence / hybrid operations
aliases:
  - Cadet Blizzard
confidence: high
summary: Public-source summary.
sectors:
  - government
  - infrastructure
defensive_notes:
  - Defensive lessons only.
sources:
  - title: Public source title
    publisher: Publisher
    url: https://example.org
last_reviewed: 2026-06-25
```

## Research posture

Attribution is probabilistic. Governments, vendors, journalists, and researchers may use different names for the same or overlapping clusters. SpyWatch separates facts, claims, aliases, confidence, and analysis.
