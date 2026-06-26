# Contributing to SpyWatch

SpyWatch accepts defensive, public-source research only.

## Good contributions

- New actor profiles with public citations.
- Alias cleanup with source notes.
- Defensive summaries for organizations and students.
- Source-quality improvements.
- Schema, validator, and index improvements.
- Historical context that helps readers understand modern intelligence activity.

## Not accepted

- Private personal information.
- Unsourced accusations.
- Target lists.
- Instructions for misuse.
- Content copied from paywalled sources without permission.
- Claims that merge actors without source support.

## Profile requirements

Every profile must include:

- unique id;
- name;
- country or alignment;
- sponsor field;
- actor type;
- aliases;
- confidence rating;
- summary;
- sectors;
- defensive notes;
- sources;
- last reviewed date.

## Style

Use clear language. Prefer phrases such as `public reporting says`, `public sources associate`, or `government advisory states` when discussing allegations. Avoid presenting attribution as absolute when the public record is uncertain.

## Local checks

```bash
python -m pip install pyyaml
python scripts/validate_actors.py
python scripts/build_index.py
```
