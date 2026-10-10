# Run logs (testing evidence)

One row per agent run in `runs.csv`. Keep the raw step-by-step log for each
run in `runs/<run_id>.jsonl` (written by the agent loop). Never edit a raw log
after the run; add corrections in the `notes` column instead.

`runs.csv` columns:

| Column | Meaning |
|--------|---------|
| `run_id` | `YYYYMMDD-HHMM-<page>`, e.g. `20261011-1430-p4` |
| `date` | ISO date |
| `page` | test-app file, e.g. `p4-checkout.html` |
| `seeded_bug` | ID from `SEEDED_BUGS.md`, or `none` for the control page |
| `model` | e.g. `llama-3.3-70b (groq)` |
| `steps` | number of agent steps used (cap is ~15) |
| `outcome` | `pass` (reached success.html) / `fail` (step cap or gave up) / `error` (crash, bad model output) |
| `issue_reported` | what the agent said was wrong, short |
| `matches_seed` | `TP` / `FN` / `FP`, judged against `SEEDED_BUGS.md` |
| `wcag_attached` | WCAG SC the grounding stub attached, or blank |
| `notes` | what happened, anything odd |

The baseline `seed-check-*.txt` files are output from
`test-app/check_seeds.py` (a scripted keyboard user, not the agent). They show
that the ground truth behaves as documented before any agent run.
