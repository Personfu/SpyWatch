# SpyWatch

SpyWatch is a defensive public-source intelligence library for studying foreign intelligence services, state-aligned cyber groups, hybrid operations, deep-cover networks, and major eCrime ecosystems.

It is built for students, defenders, journalists, researchers, and policy teams who need structured context without turning that research into an offensive playbook.

## Public archive UI

This repo includes a static public case archive at `index.html` backed by `data/public-case-archive.json`.

Current archive coverage includes:

- Operation Ghost Stories / 2010 Russian Illegals Program
- Maria Adela Kuhfeldt Rivera / Olga Kolobova
- Artem Dultsev and Anna Dultseva / Slovenia Argentina-cover case
- Sergey Cherkasov / Victor Muller Ferreira
- Mikhail Mikushin / Jose Assis Giammaria
- Pablo Gonzalez / Pavel Rubtsov, marked as disputed
- Evgeny Buryakov / SVR New York economic-intelligence case
- GRU Unit 29155 public names and source-handling notes

The archive is intentionally source-first and defensive. It includes public case names, aliases, story beats, confidence labels, and defender lessons. It intentionally excludes private addresses, private family targeting details, scraped photos, live target tracking, credential material, intrusion instructions, and birth-date harvesting.

## Vendor alias mapping

SpyWatch now includes CrowdStrike-style vendor alias mapping appendices. These files connect common public names to real units or services only when official records or strong public reporting support the connection.

- `docs/vendor-alias-mapping.md` - naming guide and priority crosswalk
- `docs/unit-mapping-russia.md` - Bear-family / Russia mapping appendix
- `docs/unit-mapping-china.md` - Panda-family / China mapping appendix
- `docs/unit-mapping-dprk.md` - Chollima-family / North Korea mapping appendix
- `docs/unit-mapping-iran.md` - Kitten-family / Iran mapping appendix

The key rule: vendor names are useful search labels, not proof by themselves. Unit attribution must be sourced.

## New expansion files

- `docs/casefiles/README.md` - casefile index and expansion queue
- `docs/casefiles/operation-ghost-stories.md` - Ghost Stories educational casefile
- `docs/casefiles/buryakov-svr-new-york.md` - New York SVR economic-intelligence casefile
- `docs/casefiles/gru-unit-29155-public-names.md` - Unit 29155 public-source handling notes
- `docs/source-standards-expanded.md` - source tiers, confidence labels, and image handling
- `data/timelines/public-intelligence-cases.json` - structured timeline for archive events

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

For photographs or images, link to official case pages, court exhibits, reputable news image pages, or public-media repositories. Do not scrape or republish private profile photos.

## Repository map

```text
index.html                                      static public archive UI
assets/site.css                                 static archive styling
data/public-case-archive.json                   public case archive dataset
data/timelines/public-intelligence-cases.json   public intelligence timeline
docs/vendor-alias-mapping.md                    vendor-name normalization guide
docs/unit-mapping-russia.md                     Russia unit mapping appendix
docs/unit-mapping-china.md                      China unit mapping appendix
docs/unit-mapping-dprk.md                       DPRK unit mapping appendix
docs/unit-mapping-iran.md                       Iran unit mapping appendix
docs/casefiles/README.md                        casefile index
docs/casefiles/*.md                             expanded public casefiles
docs/source-standards-expanded.md               expanded source standards
.github/workflows/validate.yml                  CI validation
CONTRIBUTING.md                                 contribution rules
docs/source-policy.md                           source standards and confidence rules
docs/taxonomy.md                                actor taxonomy
docs/watchlist.md                               global research backlog
docs/illegals-program.md                        deep-cover illegals case-study framework
docs/illegals-operator-roster.md                safe roster expansion notes
docs/research-playbook.md                       safe research workflow
docs/defender-briefings.md                      defensive briefing templates
schema/actor.schema.json                        actor profile schema
data/actors/index.yml                           actor index
data/actors/*/*.yml                             actor profiles
prompts/openai-enrichment.md                    safe enrichment workflow
scripts/build_index.py                          rebuilds the actor index
scripts/validate_actors.py                      validates actor YAML
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
