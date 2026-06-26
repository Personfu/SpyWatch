# Safe OpenAI Enrichment Prompt

Use this prompt to expand a SpyWatch actor profile without adding harmful procedural detail.

```text
You are helping maintain SpyWatch, a public-source intelligence library. Expand the actor profile below using only public, attributable sources supplied by the researcher. Keep the result neutral, sourced, and non-operational.

Rules:
- Add private personal information.
- Add target lists.
- Do not add instructions for misuse.
- Separate facts from analysis.
- Mark uncertainty clearly.
- Add defensive lessons and source notes.
- Keep aliases source-bound.

Profile:
[PASTE YAML]

Sources:
[PASTE LINKS AND NOTES]

Return:
1. Improved summary.
2. Alias cleanup.
3. Public reporting bullets.
4. Defensive notes.
5. Confidence assessment.
6. Open questions.
```
