# Evals

The evaluation system for this project, per
`docs/00_roadmap/agent-engineering-self-study-roadmap.md` section 12
(Phase 4) and section 30.

- `datasets/` — task definitions (JSON/JSONL), one file per capability area.
- `graders/` — deterministic/code graders and LLM-judge graders.
- `runners/` — scripts that execute a dataset against the current CLI and
  produce a report.
- `reports/` — generated eval run output (gitignored contents except this
  README, until a reporting convention is settled).
- `failures/` — real production/manual-testing failures turned into
  regression cases, per section 26.

Run the whole suite with `just eval`. Until Phase 1 exists, `just eval`
only runs the placeholder in `runners/run.py`.
