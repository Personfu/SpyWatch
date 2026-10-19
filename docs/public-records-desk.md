# Public Records Desk

This desk routes researchers to public, primary-source records for fugitives, cybercrime, fraud, espionage, sanctions, and national-security cases. It is a research index, not an exhaustive watchlist or a live tracking service.

The requested research cutoff is 2026-10-18. The case archive itself still reports its own review date in its metadata; this page does not imply that every archived claim has been re-verified through the cutoff. Wanted lists and enforcement pages change frequently, so use their current official entries for present status and preserve the date checked when adding a case.

## Fugitives and public enforcement

The [FBI wanted snapshot](../data/wanted/fbi-wanted.json) holds 354 FBI API records in threat-related categories as of its snapshot date: Ten Most Wanted Fugitives, Cyber's Most Wanted, fraud, counterintelligence, China, Iran, transnational repression, and terrorism. FBI-reported status is `captured` for 11 records and `surrendered` for 1; the rest report no status. The set includes group pages and individuals, and a notice is not a conviction. Rebuild all official-source datasets with `python scripts/build_datasets.py`, and check each linked FBI page for current status.

| Source | Use | Important limit |
| --- | --- | --- |
| [FBI Ten Most Wanted Fugitives](https://www.fbi.gov/wanted/topten) | Current FBI public fugitive notices and reward information. | A listing is not a conviction. Check the live page before quoting status. |
| [FBI Cyber's Most Wanted](https://www.fbi.gov/wanted/cyber) | Public cyber-fugitive notices and case summaries. | Distinguish wanted, charged, arrested, extradited, and convicted. |
| [FBI press releases](https://www.fbi.gov/news/press-releases) | Arrest, indictment, sentencing, seizure, and investigation announcements. | An agency announcement is a source for what the agency alleges or announces, not a substitute for the court's final disposition. |
| [DOJ Most Wanted](https://www.justice.gov/action-center/justice-department-most-wanted) | Department-wide public wanted notices. | Check the linked agency or court record for case status. |
| [U.S. Marshals Most Wanted](https://www.usmarshals.gov/what-we-do/fugitive-apprehension/most-wanted) | Federal fugitive notices maintained by the Marshals Service. | The roster is dynamic and should not be copied as a permanent list. |
| [INTERPOL Red Notices](https://www.interpol.int/How-we-work/Notices/Red-Notices/View-Red-Notices) | Public notices requested by member countries. | A Red Notice is a request to locate and provisionally arrest, not an international arrest warrant or proof of guilt. |

## Cybercrime, fraud, and public safety

| Source | Use | Important limit |
| --- | --- | --- |
| [FBI Internet Crime Complaint Center](https://www.ic3.gov/) | Report suspected internet-enabled crime and find public alerts. | IC3 complaint data are reports, not a census of verified crimes or findings about a named suspect. |
| [IC3 annual reports](https://www.ic3.gov/AnnualReport/Reports) | Trends in complaints, reported losses, and crime types. | Keep the report year and its definitions attached to any statistic; reported losses are not equivalent to adjudicated losses. |
| [IC3 public service announcements](https://www.ic3.gov/PSA) | Current public warnings and victim-protection guidance. | Warnings describe reported patterns; they do not establish guilt by themselves. |
| [CISA cybersecurity advisories](https://www.cisa.gov/news-events/cybersecurity-advisories) | Technical context and defensive guidance for publicly attributed activity. | Use the advisory's own attribution wording and confidence; do not infer an individual's identity from a group label. |
| [FTC consumer protection topics](https://www.ftc.gov/news-events/topics/protecting-consumers) | Public fraud alerts and enforcement context. | Separate civil enforcement allegations, settlements, and court judgments. |
| [SEC litigation releases](https://www.sec.gov/litigation/litreleases) | Public securities-fraud and related enforcement actions. | A complaint is an allegation; report a settlement or judgment separately. |

## Intelligence, sanctions, and declassified records

| Source | Use | Important limit |
| --- | --- | --- |
| [DOJ National Security Division](https://www.justice.gov/nsd) | Public prosecutions and policy materials involving foreign-agent, counterintelligence, and national-security matters. | Read the underlying charging document and later disposition where available. |
| [DOJ news](https://www.justice.gov/news) | Department-wide releases and case outcomes. | A press release can describe allegations; identify whether the named person has been charged, convicted, or sentenced. |
| [CIA Reading Room](https://www.cia.gov/readingroom/) | Declassified historical records and released documents. | This is an archival/FOIA resource, not a current wanted-person list or a public case-status service. |
| [Rewards for Justice](https://rewardsforjustice.net/) | Public reward notices for designated national-security threats. | A notice is not a judicial determination. Use the notice's date and its stated legal posture. |
| [OFAC Sanctions List Service](https://ofac.treasury.gov/sanctions-list-service) | Searchable sanctions lists and official list updates. | Sanctions are administrative measures, not criminal convictions; record the program and effective date. |

## Public safety and constitutional rights

| Source | Use | Important limit |
| --- | --- | --- |
| [FBI terrorism investigations](https://www.fbi.gov/investigate/terrorism) | Public descriptions of the FBI's terrorism investigative mission and related notices. | Apply the source's legal definitions; ideology, identity, association, and protected speech alone are not evidence of criminal conduct. |
| [DOJ Civil Rights Division](https://www.justice.gov/crt) | Public civil-rights enforcement, cases, and guidance. | Distinguish a complaint or investigation from a court finding; include the rights and affected communities at issue. |
| [CISA election security](https://www.cisa.gov/topics/election-security) | Public election-security information and defensive resources. | Avoid treating lawful political activity or disagreement as evidence of foreign direction or criminality. |

Document conduct and evidence, not political viewpoint. Keep public-safety, foreign-influence, and constitutional-rights claims distinct, and identify the legal status of each case.

## ShinyHunters and named cyber cases

Treat “ShinyHunters” as a public cluster label, not as one person whose status can be inferred from a single arrest. The archive cites a DOJ release for French national Sebastien Raoult's reported three-year sentence in a hacking-and-stolen-data case. The release text and date were not retrieved in this environment, so the outcome is recorded as unverified (confidence low). Even if verified, one individual outcome is not proof that all ShinyHunters operators were identified or caught. For any other reported capture, find the named defendant's official FBI or DOJ announcement and then the court disposition. Record the individual, exact alias as used by the source, jurisdiction, event date, charge, plea or verdict, sentence, and source date separately. Do not convert an arrest or indictment into “the group was caught,” and do not merge aliases without an explicit source link.

Cited URL, not verified (DOJ bot protection blocked retrieval): [DOJ release for Sebastien Raoult](https://www.justice.gov/usao-wdwa/pr/french-hacker-sentenced-three-years-prison-hacking-and-selling-stolen-data).

Start with [FBI search for ShinyHunters](https://www.fbi.gov/search?SearchableText=ShinyHunters) and [DOJ search for ShinyHunters](https://www.justice.gov/search?keys=ShinyHunters). These are discovery links, not citations for a specific event. Cite the resulting case release or court record in any SpyWatch entry.

## Machine-readable official-source datasets

| Dataset | Source | Scope | Limit |
| --- | --- | --- | --- |
| `data/wanted/fbi-wanted.json` | FBI Wanted API | Threat-related FBI notices with FBI-reported status | Notices are not convictions; status reflects the snapshot date. |
| `data/groups/mitre-attack-intrusion-sets.json` | MITRE ATT&CK Enterprise data | Intrusion-set names, aliases, and ATT&CK IDs | Aliases are naming labels, not attribution proof; cite MITRE when reusing. |
| `data/sanctions/ofac-cyber-dprk.json` | OFAC SDN and alias lists | Individuals and entities under cyber and DPRK programs | Administrative sanctions, not criminal findings; remarks and identifiers are excluded. |
| `data/advisories/ic3-psa-index.json` | IC3 PSA index page | Public service announcements linked from the index | Not a complete archive; warnings describe patterns, not findings about named people. |

Actor links use exact normalized name matches. They are research pointers for reviewer checks, not attribution findings. CISA advisories were not included because the CISA feed returned HTTP 403 to automated requests. DOJ's press-release API did not filter by case name in testing, and the CIA Reading Room has no bulk feed.

## Case-entry standard

Every person-level entry should state only public, relevant identity information and include:

- The record date, jurisdiction, court or agency, and direct source URL.
- Whether the event is an investigation, wanted notice, arrest, charge, extradition, plea, conviction, sentence, acquittal, dismissal, exchange, or release.
- The source's exact level of attribution and any public denial or unresolved dispute.
- A separate last-checked date for dynamic status, without overwriting the historical event date.
- A concise public-safety or defensive lesson, with no private addresses, family details, real-time whereabouts, or instructions for locating a person.

Use “alleged” for unadjudicated conduct, “charged” for a filed charge, and “convicted” only after a plea or judgment. “Captured” is not a case disposition; prefer the precise event (for example, arrested, extradited, or sentenced).