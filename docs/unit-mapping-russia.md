# Russia unit mapping appendix

This page connects public vendor names to public Russian services or units where the public record supports the connection. It is a defensive reference for alias normalization.

| Public cluster | CrowdStrike-style name | Other common names | Public service or unit | Confidence |
|---|---|---|---|---|
| APT28 | Fancy Bear | Forest Blizzard, Strontium, Sofacy, Pawn Storm | GRU Unit 26165 | high |
| Sandworm | Voodoo Bear | Sandworm Team, Telebots, Iron Viking | GRU Unit 74455 | confirmed |
| Unit 29155 cyber activity | none recorded here | Cadet Blizzard, Ember Bear, UNC2589 | GRU Unit 29155 | confirmed |
| APT29 | Cozy Bear | Midnight Blizzard, Nobelium, The Dukes | SVR | high |

## Public action connections

- GRU Unit 74455 is tied in DOJ public records to Ukraine, Georgia, the 2017 French election context, Novichok-investigation context, and the 2018 Winter Olympics context.
- GRU Unit 29155 is tied in 2024 public records to Ukraine-related and critical-infrastructure-focused cyber activity.
- GRU Unit 26165 and SVR/APT29 should be kept separate even when both appear in Russia-related reporting.

## Source anchors

- DOJ 2020 GRU Unit 74455 / Sandworm case
- DOJ 2024 GRU Unit 29155 case
- CISA AA24-249A
- Rewards for Justice Unit 29155 page
- MITRE ATT&CK APT28, APT29, and Sandworm pages

## Handling rule

Do not merge Russian clusters just because they share a country, language, or political context. Unit attribution must be supported by a public source.
