# Sources: סורקים לפני שמתקינים

| Slide | Claim | Source |
|---|---|---|
| 1 | 26.1% of 31,132 skills vulnerable | NVIDIA SkillSpector research, as quoted in the project brief |
| 2 | "Review skills before use; they run with full agent permissions." | Live output of `npx skills add`, this session |
| 3 | 6 of 9 skills got DO NOT INSTALL | `skillspector scan --no-llm`, this session (SECURITY-SCANS.md) |
| 4 | 4 grep hits, 0 real threats | Manual grep, this session (SECURITY-SCANS.md) |
| 5 | Line flagged AR2 | frontend-slides/html-template.md:15 @ 9906a34 |
| 8 | Commits | SECURITY-SCANS.md |
| 9 | 71 known patterns | SkillSpector documentation, as quoted in the project brief |
