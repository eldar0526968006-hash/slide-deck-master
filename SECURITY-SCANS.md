# Security scans: installed skills

Scanner: NVIDIA SkillSpector, static mode (`--no-llm`, no LLM provider connected). Policy: the SECURITY line in `CLAUDE.md`.
Every skill was installed from the **exact copy that was scanned**, at this commit:

| Skill | Source @ commit | Static verdict | Manual grep* | Decision |
|---|---|---|---|---|
| design-taste-frontend | Leonxlnx/taste-skill @ f6b7657 | DO NOT INSTALL (100) — P2 hidden instructions = HTML template comments; AE1 | 0 hits | CAUTION → installed |
| stageshow | benjitaylor/skills @ 299140f | DO NOT INSTALL (95) — MP3/P6 on motion-rule prose | 0 hits | CAUTION → installed |
| impeccable | pbakaus/impeccable @ d41d986 | DO NOT INSTALL (100) — AR2 on "never X" style rules; AS1 hooks write to .claude settings | 1 (rule that checks secrets are *not* in repo) | CAUTION → installed |
| frontend-slides | zarazhangrui/frontend-slides @ 9906a34 | DO NOT INSTALL (100) — `vercel login` in deploy.sh, font comment | 0 hits | CAUTION → installed |
| slideshow | heygen-com/hyperframes @ efc91fc | DO NOT INSTALL (58) — P6 on `npx hyperframes check` line | 0 hits | CAUTION → installed |
| Astryx CLI | npm @astryxdesign/cli 0.7.16 | DO NOT INSTALL (100) — writes CLAUDE.md/AGENTS.md (its purpose) | 3 (docs warning on .env, env pass-through, key redactor) | CAUTION → installed |
| make-interfaces-feel-better | jakubkrehel/... @ 1a2aa96 | SAFE (0) | — | installed |
| motion-prompt | showheyohtaki/motion-prompt @ 683ecca | CAUTION (7) — no tool scope | — | installed |
| plannotator (skills + binary v0.28.67, `--minimal`) | backnotprop/plannotator @ 842ccce3 | SAFE (0) | — | installed |

\* `curl…|sh`, `wget…|sh`, `API_KEY`, `SECRET`, `~/.ssh`, `exfil`, `.env`

Not done: an LLM-assisted scan (`skillspector scan … ` with a provider key). Run it once a key is connected.
