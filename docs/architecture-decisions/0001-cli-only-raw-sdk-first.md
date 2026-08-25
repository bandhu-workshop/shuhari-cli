# 0001 — CLI-only, raw-SDK-first scope

## Status

Accepted — 2026-08-25

## Context

`docs/00_roadmap/agent-engineering-self-study-roadmap.md` is a self-study
curriculum for agent engineering, structured as "Project 1": a full
FastAPI + React + PostgreSQL personal research assistant, built first
against the raw provider SDKs (R0) and later against Google ADK (R1) and a
from-scratch runtime (R2).

The goal here is narrower: learn how the Claude and OpenAI APIs actually
work — request/response shapes, tool calling, streaming, token accounting —
by building a CLI application, not a web product.

## Decision

- Build only a CLI (Typer), never the FastAPI/React/SSE product shell
  described in the roadmap's Phase 2 and Phase 14. If a served/streaming
  variant becomes interesting later, that's a new decision, not a default.
- Follow the roadmap's own R0 sequence: raw `anthropic` and `openai` SDKs
  first (Phase 1), before any framework. Google ADK is deferred to when
  the roadmap's Phase 5 is actually reached — it is not a dependency yet.
- Do not pre-create the roadmap's full target repository shape (section 6:
  `runtime/`, `context/`, `tools/`, `memory/`, `retrieval/`, `research/`,
  `protocols/`, `security/`, `observability/`, `persistence/`, model
  provider adapters). Grow the tree one phase at a time, as the roadmap
  itself instructs ("Do not create every directory on day one").
- Drop the FastAPI-web-service-shaped skeleton (`models/`, `schemas/`,
  `services/`, `db/`, `ai/`) that was scaffolded by mirroring a sibling
  project (`creditforge`) before this roadmap was factored in — none of
  it maps onto this roadmap's phases, and empty skeletons with no near-term
  purpose are dead weight, not preparation.
- No Docker Compose yet — nothing to containerize until a service or a
  database actually exists.

## Consequences

- `src/shuhari_cli/` currently holds only `core/` (settings, logging,
  exceptions) and `cli/` (the Typer entry point). New top-level packages
  (a provider-adapter layer, a manual tool loop, etc.) get added starting
  with Phase 1, per the roadmap's "Final study order" (section 45).
- When the roadmap's naming would collide with this decision (e.g. section
  6 uses `models/` for LLM provider adapters, which would be confusing
  next to a domain-model connotation), prefer an unambiguous name —
  `providers/` — over the roadmap's literal folder name.
- `evals/` (datasets/graders/runners/reports/failures) and
  `docs/learning-log.md` exist from Phase 0 onward, per section 8, even
  though they're empty until Phase 1 produces something to evaluate.
