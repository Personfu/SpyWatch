# Vendor alias mapping guide

SpyWatch uses vendor names as research labels, not as final proof of identity. CrowdStrike, Microsoft, Mandiant, MITRE, governments, and news outlets often use different names for overlapping activity clusters.

## CrowdStrike-style families

CrowdStrike-style public names often use animal families. Examples commonly seen in public reporting include:

- Bear: Russia-linked activity
- Panda: China-linked activity
- Kitten: Iran-linked activity
- Chollima: North Korea-linked activity
- Spider: financially motivated criminal activity
- Jackal: hacktivist or disruption-focused activity in some reporting streams

These labels are useful for memory and search, but they are not the same thing as a legal unit, government service, or court-proven identity.

## Unit mapping rule

Only connect a vendor name to a real unit when one of these exists:

1. A court record or indictment.
2. A government advisory or sanctions notice.
3. A rewards notice or official public attribution.
4. Multiple high-quality investigative reports that clearly explain their evidence.

If the public record only supports country-level sponsorship, keep the unit field blank or mark it as unknown.

## Priority mappings to track

| SpyWatch profile | Common vendor names | Real-world unit or service | Confidence |
|---|---|---|---|
| APT28 | Fancy Bear, Forest Blizzard, Strontium, Sofacy | GRU Unit 26165 | high |
| Sandworm | Voodoo Bear, Sandworm Team, Telebots, Iron Viking | GRU Unit 74455 | confirmed |
| Unit 29155 cyber activity | Cadet Blizzard, Ember Bear, UNC2589 | GRU Unit 29155 | confirmed |
| APT29 | Cozy Bear, Midnight Blizzard, Nobelium, The Dukes | SVR | high |
| APT1 | Comment Crew, Comment Panda | PLA Unit 61398 | confirmed |
| APT41 | Wicked Panda, Double Dragon, Barium, Winnti | China state-linked / MSS-associated ecosystem | medium |
| Volt Typhoon | Vanguard Panda, Bronze Silhouette | PRC state-sponsored, unit unknown | medium |
| Lazarus Group | Labyrinth Chollima, Hidden Cobra, Zinc | DPRK state-sponsored ecosystem | high |
| APT38 / BlueNorOff | Stardust Chollima, BeagleBoyz | DPRK financial cyber-operations ecosystem | high |
| APT33 | Refined Kitten, Elfin, Peach Sandstorm | Iran state-linked, unit unknown | medium |
| APT34 | Helix Kitten, OilRig, Hazel Sandstorm | Iran state-linked, unit unknown | medium |
| APT35 | Charming Kitten, Mint Sandstorm, Phosphorus | Iran state-linked, unit unknown | medium |

## Source anchors

- DOJ 2014 PLA Unit 61398 case
- DOJ 2020 GRU Unit 74455 / Sandworm case
- DOJ 2024 and RFJ public material for GRU Unit 29155
- CISA and allied advisories for SVR/APT29 and Volt Typhoon
- Treasury and FBI public notices for DPRK cyber finance cases
- MITRE ATT&CK group pages for alias cross-checking

## Safety boundary

This guide does not provide tradecraft, live infrastructure, targeting instructions, private personal data, or copied portraits. It is a normalization layer for public defensive research.
