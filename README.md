# SimUX

A multi-persona UI/UX auditor with a closed fix-and-verify loop. FYP 2026–27,
Department of AI & Data Science, FAST-NUCES. Supervisor: Ms. Saira Qamar.

LLM persona agents are **restricted in code**, not by prompt. The
accessibility persona sees only the browser's accessibility tree and acts only
with the keyboard. The agents attempt real tasks on a page, report friction
grounded in WCAG, and (later) verify fixes by re-running the same constrained
agent.

## Repository layout

| Path | What | Owner |
|------|------|-------|
| `test-app/` | Static seeded-bug test application (the team-controlled target) | Person A |
| `SEEDED_BUGS.md` | Pre-registered ground truth: every planted bug, its page and WCAG criterion | Person A |
| `logs/` | Agent run logs: testing evidence | Person A |
| `docs/demo-script.md` | Live-demo order, talking points, fallback | Person A |
| `agent/` | Playwright execution layer + LLM agent loop | Person B |
| `grounding/` | WCAG lookup stub for seeded bugs | Person C |

## Running the test app

```bash
python -m http.server 8000 -d test-app
# open http://localhost:8000/
```

Pages: `control.html` (no bugs), `p1-newsletter.html` … `p5-booking.html` (one
seeded bug each). Task success = landing on `success.html`.

To re-verify that every seeded bug is present and behaves as documented:

```bash
pip install playwright && playwright install chromium
python test-app/check_seeds.py
```
