# North Korea unit mapping appendix

This page connects public vendor names to public North Korea-linked cyber ecosystems where the public record supports the connection. It is a defensive reference for alias normalization.

| Public cluster | CrowdStrike-style name | Other common names | Public service or unit | Confidence |
|---|---|---|---|---|
| Lazarus Group | Labyrinth Chollima | Hidden Cobra, Zinc, Guardians of Peace | DPRK state-sponsored ecosystem | high |
| APT38 / BlueNorOff | Stardust Chollima | BlueNorOff, BeagleBoyz, Nickel Gladstone | DPRK financial cyber-operations ecosystem | high |
| APT37 | Ricochet Chollima | Reaper, ScarCruft, RedEyes | DPRK state-linked actor | medium |
| Kimsuky | Velvet Chollima | Emerald Sleet, Thallium, APT43 | DPRK state-linked actor | medium |

## Public action connections

- Lazarus is often used as an umbrella label, so SpyWatch should separate broad Lazarus references from APT38 / BlueNorOff financial activity.
- APT38 / BlueNorOff should be mapped as a financial-operations sub-cluster where public sources support that split.
- Kimsuky and APT37 should be tracked separately from Lazarus unless a source explicitly links a specific case.

## Source anchors

- FBI and Treasury DPRK cyber public notices
- MITRE ATT&CK Lazarus, APT38, APT37, and Kimsuky pages
- Mandiant and other reputable vendor reporting

## Handling rule

Do not treat every DPRK-linked event as Lazarus. Preserve sub-cluster names and mission differences.
