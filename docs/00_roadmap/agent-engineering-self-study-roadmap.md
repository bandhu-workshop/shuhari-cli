# Agent Engineering Self-Study Roadmap
## Project 1 — Build a ChatGPT/Claude-Class Assistant and Deep Research Agent

**Version:** August 25, 2026  
**Goal:** Learn modern AI agent engineering from first principles through a production-style assistant, then rebuild the important parts without a framework.

---

# How to use this roadmap

This is not a list of tutorials to finish. It is a **learn-by-building curriculum**.

For every phase, follow this loop:

```text
READ THE CONCEPT
      ↓
BUILD THE MINIMUM VERSION
      ↓
INSTRUMENT IT
      ↓
CREATE EVALS
      ↓
BREAK IT INTENTIONALLY
      ↓
IMPROVE IT
      ↓
WRITE WHAT YOU LEARNED
```

Do not move forward merely because the feature "works once."

A phase is complete only when:

1. you can explain the underlying problem without framework vocabulary,
2. you have implemented the feature,
3. you can inspect what the agent did,
4. you can measure whether it works,
5. you know at least one important failure mode,
6. you have a regression test for that failure.

---

# 1. The central mental model

The most important idea in this entire roadmap is:

> **The model is the reasoning/policy engine. The product you engineer is the harness around the model.**

A useful mental model:

```text
                         ┌─────────────────────────┐
                         │        USER / UI        │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │      AGENT RUNTIME      │
                         │                         │
                         │ run lifecycle           │
                         │ budgets                 │
                         │ retries                 │
                         │ cancellation            │
                         │ permissions             │
                         │ checkpoints             │
                         └────────────┬────────────┘
                                      │
                                      ▼
                    ┌──────────────────────────────────┐
                    │          CONTEXT ENGINE          │
                    │                                  │
                    │ system instructions              │
                    │ conversation history             │
                    │ working state                    │
                    │ retrieved memories               │
                    │ retrieved knowledge              │
                    │ available tools                  │
                    │ plans / artifacts                │
                    │ token budget                     │
                    └────────────────┬─────────────────┘
                                     │
                                     ▼
                               ┌───────────┐
                               │    LLM    │
                               │ reasoning │
                               └─────┬─────┘
                                     │
                         ┌───────────┴────────────┐
                         │                        │
                     final answer              action
                                                  │
                                                  ▼
                                      ┌─────────────────────┐
                                      │    TOOL REGISTRY    │
                                      │                     │
                                      │ local tools         │
                                      │ web/search          │
                                      │ retrieval           │
                                      │ MCP                 │
                                      │ code sandbox        │
                                      │ external APIs       │
                                      └──────────┬──────────┘
                                                 │
                                            observation
                                                 │
                                                 └──────► loop

Persistent systems around the runtime:

┌──────────┐  ┌────────────┐  ┌────────────┐  ┌─────────────┐
│  Memory  │  │ Artifacts  │  │  Tracing   │  │ Evaluations │
└──────────┘  └────────────┘  └────────────┘  └─────────────┘
```

The major disciplines you need to master are:

1. agent loops and orchestration,
2. context engineering,
3. tool engineering and tool selection,
4. state and memory,
5. retrieval and grounding,
6. planning and research,
7. evaluation,
8. observability and tracing,
9. safety, permissions and sandboxing,
10. MCP / A2A / interoperability,
11. long-running and durable execution,
12. production reliability,
13. latency, caching and cost,
14. model routing,
15. continuous improvement from real failures.

Everything in this roadmap fits under those topics.

---

# 2. Framework strategy

Do **not** choose between "framework" and "from scratch."

Use both.

## The sequence

```text
R0 — RAW SDK
     ↓
learn the actual primitive agent loop

R1 — GOOGLE ADK
     ↓
build the complete product using mature abstractions

R1.5 — SELECTIVE FRAMEWORK COMPARISONS
     ↓
study different architectural ideas

R2 — CUSTOM AGENT RUNTIME
     ↓
remove ADK and reimplement the important pieces yourself

R3 — ADVANCED HARNESS EXPERIMENTS
     ↓
tool discovery, programmatic tools, model routing,
evaluator-optimizer loops, long-running execution
```

## Recommended framework roles

| Technology | Role in this curriculum |
|---|---|
| Raw `anthropic`, `openai`, or `google-genai` SDK | Learn the primitive loop |
| **Google ADK 2.x** | Main product/framework build |
| **PydanticAI / Pydantic AI Harness** | Study clean Pythonic harness composition |
| **LangGraph** | Study explicit state machines, persistence and durable execution |
| **OpenAI Agents SDK** | Study a deliberately small agent runtime |
| LangChain | Learn only where useful; do not make it the core architecture |
| LlamaIndex | Optional for retrieval-heavy experiments |
| CrewAI / AutoGen-like systems | Optional multi-agent comparison only |

### Important rule

Pin the exact framework versions used by the project.

Do not let a floating dependency silently change:
- session behavior,
- event schemas,
- tool semantics,
- tracing,
- context handling,
- evaluation behavior.

---

# 3. Recommended technology stack

```text
Language
    Python 3.12+

Package/project management
    pyproject.toml
    uv or equivalent

API
    FastAPI

Primary agent framework
    Google ADK 2.x, exact version pinned

Raw-provider experiments
    anthropic / openai / google-genai SDK

Schemas
    Pydantic v2

Database
    PostgreSQL

Vector capability
    pgvector initially

Optional ephemeral state / queues / resumable streaming
    Redis

Object/artifact storage
    local filesystem in development
    GCS/S3-compatible storage later

Frontend
    React or Next.js
    keep the UI deliberately simple

Streaming
    SSE first

Tracing
    OpenTelemetry / OpenInference
          ↓
    Arize Phoenix

Evaluation
    your own evaluation abstractions
    + DeepEval where useful
    + ADK eval features while using ADK
    + Phoenix datasets/experiments

Local environment
    Docker Compose

Production target
    GCP later
```

---

# 4. Architecture rule: ADK must not become your application architecture

Create your own concepts at the application boundary.

For example:

```text
ModelProvider
AgentRuntime
RunStore
EventStore

ContextManager
ContextBudget

ToolRegistry
ToolSelector
ToolExecutor

MemoryManager
Retriever

ArtifactStore

ApprovalPolicy
PermissionPolicy

Tracer
Evaluator
```

Then ADK is initially an implementation underneath those concepts.

Later:

```text
AgentRuntime
    ├── ADKRuntime
    └── CustomRuntime

MemoryManager
    ├── ADKMemory
    ├── FileMemory
    └── HybridMemory

ModelProvider
    ├── GeminiProvider
    ├── AnthropicProvider
    └── OpenAIProvider
```

The goal is that deleting ADK does not require deleting your whole application.

---

# 5. Product scope

Do not call the project merely "a ChatGPT clone."

Build a **personal technical/research assistant**.

That gives you measurable tasks while still exercising nearly every agent subsystem.

The final product should support:

- normal conversation,
- multi-turn state,
- streaming,
- tools,
- web research,
- file/document retrieval,
- citations,
- persistent memory,
- long-running research,
- subagents,
- artifact creation,
- resumable runs,
- approvals for consequential actions,
- tracing,
- evaluation,
- cost/latency telemetry.

RAG is a component.

Deep research is a behavior.

Memory is a subsystem.

The agent harness connects them.

---

# 6. Repository shape

A good long-term target:

```text
assistant/
├── apps/
│   ├── api/
│   └── web/
│
├── src/
│   └── assistant/
│       ├── application/
│       │   ├── services/
│       │   └── use_cases/
│       │
│       ├── runtime/
│       │   ├── base.py
│       │   ├── events.py
│       │   ├── run.py
│       │   ├── budgets.py
│       │   ├── adk_runtime.py
│       │   └── custom_runtime.py
│       │
│       ├── models/
│       │   ├── base.py
│       │   ├── gemini.py
│       │   ├── anthropic.py
│       │   └── openai.py
│       │
│       ├── context/
│       │   ├── builder.py
│       │   ├── budget.py
│       │   ├── compaction.py
│       │   └── provenance.py
│       │
│       ├── tools/
│       │   ├── base.py
│       │   ├── registry.py
│       │   ├── selection.py
│       │   ├── executor.py
│       │   └── permissions.py
│       │
│       ├── memory/
│       │   ├── models.py
│       │   ├── reader.py
│       │   ├── writer.py
│       │   ├── consolidation.py
│       │   └── scoring.py
│       │
│       ├── retrieval/
│       │   ├── indexing.py
│       │   ├── retriever.py
│       │   ├── hybrid.py
│       │   └── reranker.py
│       │
│       ├── research/
│       │   ├── planner.py
│       │   ├── researcher.py
│       │   ├── orchestrator.py
│       │   ├── citations.py
│       │   └── verification.py
│       │
│       ├── protocols/
│       │   ├── mcp/
│       │   └── a2a/
│       │
│       ├── security/
│       │   ├── policy.py
│       │   ├── approvals.py
│       │   └── sandbox.py
│       │
│       ├── observability/
│       │   ├── tracing.py
│       │   ├── metrics.py
│       │   └── cost.py
│       │
│       └── persistence/
│           ├── conversations.py
│           ├── events.py
│           ├── runs.py
│           ├── memories.py
│           └── artifacts.py
│
├── evals/
│   ├── datasets/
│   ├── graders/
│   ├── runners/
│   ├── reports/
│   └── failures/
│
├── tests/
├── docs/
├── scripts/
├── docker-compose.yml
└── pyproject.toml
```

Do not create every directory on day one. Grow toward this structure as the concepts appear.

---

# 7. Data model: conversation is not enough

Do not persist only:

```text
messages[]
```

Distinguish:

```text
Conversation
    └── Run
         └── Events
              ├── user_message
              ├── model_message
              ├── tool_request
              ├── tool_result
              ├── memory_read
              ├── memory_write
              ├── retrieval
              ├── approval_request
              ├── artifact_created
              ├── error
              └── final_response
```

A run should eventually support states such as:

```text
QUEUED
RUNNING
WAITING_FOR_TOOL
WAITING_FOR_APPROVAL
WAITING_FOR_SUBAGENT
PAUSED
COMPLETED
FAILED
CANCELLED
```

Why this matters:

- replay,
- debugging,
- resumability,
- evaluation,
- tracing,
- user-visible progress,
- coding-agent architecture later.

---

# 8. Phase 0 — Setup your learning system

**Time:** 4–6 hours

## Build

Create:
- repository,
- `pyproject.toml`,
- formatting/linting/type checking,
- `pytest`,
- `.env.example`,
- Docker Compose skeleton,
- `docs/learning-log.md`,
- `docs/architecture-decisions/`,
- `evals/`.

## Create an experiment template

For every experiment record:

```markdown
## Hypothesis

## Change

## Evaluation set

## Metrics

## Result

## Trace examples

## What failed

## Decision
```

## Start an architecture decision record

Examples:
- Why SSE before WebSocket?
- Why PostgreSQL?
- Why ADK as the primary framework?
- Why Phoenix?
- Why custom application interfaces around ADK?

## Exit criterion

You can run:

```bash
make test
make lint
make eval
```

even if `make eval` initially contains only a tiny placeholder evaluation.

---

# 9. Phase 1 — Raw SDK and the bare agent loop

**Time:** ~15 hours  
**Framework:** none

This phase is mandatory.

## Build

A terminal assistant using one provider SDK.

Start with:
- normal message,
- streamed message,
- conversation history,
- token accounting.

Then add only three tools:

```text
read_file
list_files
web_search
```

Implement the tool loop manually.

Conceptually:

```python
while budget.can_continue():

    response = model.generate(
        messages=messages,
        tools=tools,
    )

    messages.append(response)

    if response.has_no_tool_calls():
        return response

    for call in response.tool_calls:
        result = execute_tool(call)
        messages.append(tool_result(call, result))
```

## Learn deeply

- request/response payloads,
- roles and content blocks,
- tool schema representation,
- tool call IDs,
- tool result correlation,
- stop reasons,
- max token handling,
- streaming event types,
- structured outputs,
- retries,
- timeouts,
- rate limits,
- provider errors,
- token usage,
- reasoning effort controls where applicable.

### Understand this sentence

> The model is not "running a tool." The model emits a request. Your harness decides whether and how that request is executed.

That distinction becomes security-critical later.

## Exercise

Capture a full raw JSON conversation in which:
1. turn 1 is normal chat,
2. turn 2 requires a tool,
3. the model receives a tool result,
4. the final answer is streamed.

Write an explanation of every field.

## Measurements

Track:
- time to first token,
- total latency,
- input tokens,
- output tokens,
- cached tokens if available,
- number of tool calls,
- model cost.

## Read

- Anthropic — Building Effective Agents  
  https://www.anthropic.com/engineering/building-effective-agents
- OpenAI — Building Agents learning track  
  https://developers.openai.com/
- Thorsten Ball — How to Build an Agent  
  https://ampcode.com/notes/how-to-build-an-agent
- Hugging Face — smolagents articles/docs  
  https://huggingface.co/blog

## Exit criterion

Without looking at your code, you can explain precisely what happens between:

```text
user asks question
→ model requests tool
→ program executes tool
→ model sees observation
→ model continues
```

---

# 10. Phase 2 — Build the boring ChatGPT-style product shell

**Time:** ~15–20 hours

No advanced memory, RAG or multi-agent system yet.

## Build

- FastAPI API,
- PostgreSQL,
- basic React chat UI,
- conversation creation,
- conversation titles,
- persisted messages,
- model selection,
- system instruction configuration,
- SSE streaming,
- stop/cancel,
- regenerate,
- error state,
- token usage display.

Store:
- conversation,
- run,
- event,
- model,
- model version,
- prompt version,
- parameters,
- timestamps.

## Learn

### Streaming

Understand:
- HTTP streaming,
- SSE,
- heartbeats,
- event IDs,
- disconnects,
- cancellation,
- partial messages.

### Run lifecycle

Separate:

```text
conversation
run
event
message
```

Do not treat them as synonyms.

### Idempotency

What happens if the UI retries the same request?

### Cancellation

What should be persisted if the user presses Stop after 320 tokens?

## Exercise

Kill:
- the browser,
- API process,
- model request,
- database connection,

at different points and document the observed state.

## Exit criterion

You have a stable non-agent chatbot whose data model is strong enough to support everything that follows.

---

# 11. Phase 3 — Observability before advanced features

**Time:** ~12 hours

Do this early.

## Stack

```text
OpenTelemetry / OpenInference
          ↓
       Phoenix
```

Keep a grep-friendly local trace representation too.

## Trace shape

```text
agent.run
│
├── context.build
│    ├── memory.retrieve
│    └── retrieval.retrieve
│
├── model.generate
│
├── tool.web_search
│
├── model.generate
│
└── final.response
```

## Record

At minimum:

```text
run_id
session_id
user_id

model
model_version
prompt_version

input tokens
output tokens
cached tokens

context size

tool name
tool arguments
tool duration
tool result size
tool status

retrieved document IDs
memory IDs

TTFT
total latency

retry count
agent steps

estimated cost
evaluation scores
```

For development, preserve the actual prompts/tool observations where safe so you can inspect failures.

## Learn

- trace,
- span,
- parent/child spans,
- baggage/context propagation,
- OpenTelemetry,
- OpenInference,
- GenAI semantic conventions,
- sampling,
- P50/P95/P99,
- trace-to-eval linkage.

## Dashboard ideas

```text
success rate
tool failure rate
tool calls per run
agent steps per run

P50/P95 latency

tokens per successful task
cost per successful task

context tokens per run
cache hit rate

retrieval failures
memory failures
citation failures
```

Focus on:

> **cost per successful task**

rather than only cost per model call.

## Read

- Arize Phoenix  
  https://arize.com/docs/phoenix/
- OpenInference  
  https://github.com/Arize-ai/openinference
- OpenTelemetry GenAI semantic conventions  
  https://opentelemetry.io/

## Exit criterion

For any saved run, you can answer:

> Why did the agent do that?

without rerunning it.

---

# 12. Phase 4 — Build evaluation as an engineering system

**Time:** ~30 hours

Treat this as one of the largest phases.

## Read first

- Anthropic — Demystifying Evals for AI Agents  
  https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Hamel Husain / Shreya Shankar — LLM Evals FAQ  
  https://hamel.dev/blog/posts/evals-faq/
- DeepEval docs  
  https://deepeval.com/docs/introduction

## Vocabulary

Be precise about:

```text
task
trial
grader
assertion
trajectory / transcript
outcome
agent harness
eval harness
eval dataset
capability eval
regression eval
```

The distinction between **trajectory** and **outcome** is crucial.

Example:

```text
Agent says:
"Your booking succeeded."

≠

Database actually contains the booking.
```

## Start with 20–50 tasks

Examples:

```text
Answer without using tools.

Use calculator for a calculation.

Do not call calculator for simple factual chat.

Search because freshness is required.

Do not search for stable common knowledge.

Use exactly the required account/project scope.

Retry a transient tool failure.

Do not retry a permanent validation failure.

Retrieve a relevant old memory.

Do not retrieve an irrelevant memory.

Use the newer memory instead of superseded information.

Forget a stored memory.

Research two conflicting sources.

Cite the retrieved source.

Ignore malicious instructions inside a webpage.

Require approval before a destructive action.

Stop when the task is complete.

Stop when the run budget is exhausted.
```

Balance positive and negative cases.

If you test only "should use search," you will train the system to search everything.

## Error analysis methodology

### 1. Open coding

Read 30–50 traces manually.

Write raw notes such as:

```text
searched even though search unnecessary
picked correct tool but wrong argument
tool result contained answer but agent ignored it
memory retrieved old preference
citation did not support claim
loop continued after task was already done
```

### 2. Axial coding

Cluster them into a failure taxonomy:

```text
tool_selection
tool_arguments
retrieval
memory
planning
instruction_following
termination
security
citation
context_overload
```

### 3. Count

Fix common failures first.

## Grader types

### Deterministic/code graders

Use whenever possible.

Examples:
- expected DB row exists,
- expected tool called,
- prohibited tool not called,
- JSON schema valid,
- memory deleted,
- URL was actually retrieved,
- max step count respected.

### LLM judges

Use for:
- coherence,
- research completeness,
- citation support,
- instruction following,
- natural-language correctness.

Good practices:
- one rubric dimension per judge,
- binary/clear decisions when possible,
- explicit `Unknown`,
- calibrate against humans,
- inspect disagreements.

### Human review

Use to:
- calibrate judges,
- inspect surprising cases,
- understand new failure modes.

## Non-determinism

Learn:

```text
pass@k
pass^k
```

If a task succeeds 75% of the time:

```text
pass^3 = 0.75³ ≈ 42%
```

For a product where a user expects consistent behavior, reliability matters as much as best-case performance.

## Maintain two suites

```text
CAPABILITY SUITE
    difficult
    intentionally unsolved cases
    shows room to improve

REGRESSION SUITE
    solved failures
    should remain near 100%
```

Every real bug should eventually become a regression test.

## Tool division

Recommended:

```text
Phoenix
    traces
    datasets
    experiments
    exploratory evaluation

DeepEval/custom Python
    automated eval suite
    component tests
    trajectory checks
    CI

ADK eval
    framework-level tests while using ADK
```

## Exit criterion

```bash
make eval
```

runs at least 30 tasks, produces a report, and your repository contains a written top-five failure taxonomy.

---

# 13. Phase 5 — Rebuild the agent using Google ADK

**Time:** ~12–15 hours initially, then ADK remains the primary implementation

Now introduce the framework.

## Learn the ADK abstractions by mapping them back to R0

For every ADK concept ask:

```text
What primitive does this wrap?
What state does it maintain?
What does it persist?
What events does it emit?
What does it do automatically?
Where can I intercept behavior?
```

Study:
- Agent,
- Runner,
- Session,
- Event,
- tools,
- callbacks/hooks,
- artifacts,
- workflows,
- memory,
- evaluation,
- tracing,
- streaming,
- resumability,
- MCP/A2A support.

## Rule

Do not rewrite your entire application around ADK.

Create an `ADKRuntime` adapter.

## Resource

- Google ADK documentation  
  https://adk.dev/get-started/python/

## Exit criterion

The same small agent works through ADK and your R0 implementation, and you can explain the abstraction mapping.

---

# 14. Phase 6 — Tool engineering

**Time:** ~15–20 hours

Function calling is only the beginning.

## Tool contract

For every tool define:

```text
name
namespace
purpose

when_to_use
when_NOT_to_use

input schema
output schema

side effects
permission level

idempotent?
retryable?

timeout
rate limit
cost

auth scope

possible errors
error recovery instructions

output compression policy

examples
```

## Design tool outputs for models, not REST clients

Bad:

```json
{
  "data": {
    "metadata": { "...": "40 fields" },
    "payload": { "...": "large nested response" }
  }
}
```

Better:

```json
{
  "title": "...",
  "summary": "...",
  "date": "...",
  "source": "...",
  "relevant_fields": {}
}
```

The output will become context.

Context has a cost.

## Error messages are part of the interface

Bad:

```text
Invalid input.
```

Better:

```text
path must be absolute. Example:
/home/project/src/main.py
```

The latter helps the model self-correct.

## Tool-selection experiment

Create 30+ tools.

Compare:

```text
A
all 30 tool schemas sent every turn

B
tool retriever
    ↓
top 3–8 relevant tools
    ↓
model
```

Measure:
- selection accuracy,
- false-positive tool use,
- argument accuracy,
- prompt tokens,
- latency,
- task success,
- cost.

## Study tool consolidation

Compare:

```text
search
→ result IDs
→ fetch result
→ parse result
```

versus:

```text
search_and_read
```

Do not assume fewer tools is always better. Measure it.

## Learn the difference among

```text
Tool
    executable capability

Skill
    instructions + reusable procedure + optional scripts/resources

Resource
    information the agent can retrieve

Prompt/template
    reusable instruction structure
```

## Read

- Anthropic — Writing Effective Tools for Agents  
  https://www.anthropic.com/engineering
- Anthropic — Advanced Tool Use  
  https://www.anthropic.com/engineering/advanced-tool-use
- Anthropic — Code Execution with MCP  
  https://www.anthropic.com/engineering
- Anthropic — Agent Skills  
  https://www.anthropic.com/engineering
- Phil Schmid — Agent Skills / MCP articles  
  https://www.philschmid.de/

## Exit criterion

You have a dedicated tool-selection eval separate from overall task success.

---

# 15. Phase 7 — Context engineering

**Time:** ~20–25 hours

This is a core discipline.

Prompt engineering asks:

> What words should I write?

Context engineering asks:

> Given a limited context budget, what information should the model see **on this step**?

## Build a real `ContextManager`

```text
ContextManager.build()

system instructions
      +
task-specific instructions
      +
recent conversation
      +
working state
      +
relevant long-term memory
      +
retrieved documents
      +
relevant tool definitions
      +
tool observations
      +
current artifacts / plan
      ↓
rank
filter
compress
discard
      ↓
final model context
```

## Learn

- context budgeting,
- context rot,
- lost-in-the-middle effects,
- context provenance,
- relevance,
- recency,
- compaction,
- summarization,
- tool-result clearing,
- stale-state removal,
- progressive disclosure,
- just-in-time retrieval,
- structured note-taking,
- prompt caching,
- stable vs dynamic prompt regions,
- subagent context isolation.

## Build a context debugger

Display per run:

```text
System                    1,420 tokens
Recent conversation       3,100
Working notes             1,250
Long-term memory            630
Retrieved documents       4,900
Tool definitions          1,110
--------------------------------
Total                    12,410
```

Also show:

```text
WHY INCLUDED?
source?
age?
relevance score?
memory ID?
document ID?
```

## Experiments

### Experiment A — context length

Run the same eval at increasing context sizes.

Plot:

```text
context tokens
vs
task pass rate
```

### Experiment B — compaction

Compare:
- no compaction,
- naive summary,
- structured state extraction,
- provider-native compaction.

### Experiment C — caching

Measure:
- cache-hit rate,
- TTFT,
- cost.

Keep stable content early and dynamic content later where provider caching benefits from it.

## Read

- Anthropic — Effective Context Engineering for AI Agents  
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic engineering articles on long-running agent harnesses  
  https://www.anthropic.com/engineering
- OpenAI developer guidance  
  https://developers.openai.com/
- Sebastian Raschka  
  https://magazine.sebastianraschka.com/

## Exit criterion

You have a context-inspection UI/report and an experiment showing how context size/compaction affects quality and cost.

---

# 16. Phase 8 — Build memory properly

**Time:** ~30–40 hours

Treat memory as a mini-project.

Do **not** define memory as:

> Embed every message into a vector database.

## Learn the memory types

### A. Conversation/session memory

Recent dialogue needed for conversational continuity.

Usually persisted exactly.

### B. Working memory

State the agent creates while solving the current task.

Examples:

```text
plan.md
todo.md
research_notes.md
facts.json
sources.json
draft.md
```

### C. Semantic long-term memory

Stable facts/preferences.

Example:

```text
User prefers Python for backend prototypes.
Project uses GCP.
```

### D. Episodic memory

Past experiences/outcomes.

Example:

```text
We tried retrieval strategy A.
It produced too many irrelevant results.
Hybrid strategy B worked better.
```

### E. Procedural memory

Reusable strategies or ways of working.

Example:

```text
For scientific research:
1. prefer primary literature,
2. record publication date,
3. corroborate disputed claims,
4. map claims to evidence.
```

Do not let the model arbitrarily rewrite system-level procedures.

## Memory record schema

A useful design:

```text
id
content

type
scope
    user
    project
    conversation

source_event_id

created_at
updated_at

valid_from
valid_until

confidence
importance

provenance
    explicit_user
    inferred
    system
    imported

status
    active
    superseded
    deleted
```

## Write path

```text
Conversation / events
        ↓
Candidate extraction
        ↓
Worth remembering?
        ↓
Classify operation
        ↓
┌────────┬────────┬────────┬────────┐
│  ADD   │ UPDATE │ DELETE │ NO-OP  │
└────────┴────────┴────────┴────────┘
        ↓
Deduplicate
        ↓
Resolve conflicts
        ↓
Apply temporal validity
        ↓
Persist
```

## Read path

```text
Current task
    ↓
memory query construction
    ↓
candidate generation
    ↓
scope/security filter
    ↓
semantic score
    +
keyword score
    +
entity match
    +
recency
    +
importance
    ↓
reranking
    ↓
token budget
    ↓
ContextManager
```

## Build three backends

### Backend 1 — ADK baseline

Use the framework memory service.

### Backend 2 — agent-managed file memory

Example:

```text
/memory/profile.md
/memory/projects/
/memory/preferences.md
/memory/episodes/
```

The model explicitly reads/writes memory through tools.

### Backend 3 — your own extraction/consolidation/retrieval system

Use:
- structured extraction,
- deduplication,
- supersession,
- embeddings,
- BM25/keyword,
- entity signals,
- reranking.

Put all three behind one interface.

## Memory eval dataset

At least 30 questions/tasks:

```text
simple recall
multi-session recall
explicit "remember X"
update X → Y
forget X
old value vs new value
irrelevant memory must not appear
similar projects remain isolated
scope isolation
contradictory memories
temporal facts
long conversation + compaction
latent preference consistency
provenance
```

Measure:
- recall@k,
- precision@k,
- final-answer accuracy,
- irrelevant-memory injection,
- latency,
- token cost,
- write frequency.

## Study

- Phil Schmid — Memory in Agents  
  https://www.philschmid.de/memory-in-agents
- Anthropic memory/context engineering material  
  https://www.anthropic.com/engineering
- ADK memory docs  
  https://adk.dev/sessions/memory/
- MemGPT / Letta paper — arXiv:2310.08560  
  https://arxiv.org/abs/2310.08560
- Mem0 paper — arXiv:2504.19413  
  https://arxiv.org/abs/2504.19413
- LongMemEval — arXiv:2410.10813  
  https://arxiv.org/abs/2410.10813
- DeepLearning.AI agent-memory courses  
  https://www.deeplearning.ai/courses/

### Your saved memory video

https://www.youtube.com/watch?v=HDqzJJhZsxw

## Portfolio artifact

Write:

```text
Memory Architecture Benchmark

ADK vs file-based vs hybrid pipeline

metrics:
- recall
- precision
- latency
- token cost
- update correctness
- forgetting correctness
```

This is one of the strongest artifacts in the entire project.

## Exit criterion

Three memory systems, one interface, one shared evaluation suite, one comparison report.

---

# 17. Phase 9 — Retrieval and grounding

**Time:** ~20–25 hours

Memory and knowledge retrieval are related but not identical.

## Build a document pipeline

Learn:
- document parsing,
- structural chunking,
- semantic chunking,
- metadata,
- embeddings,
- vector indexes,
- lexical search,
- BM25,
- hybrid retrieval,
- filters,
- reranking,
- query rewriting,
- multi-query retrieval,
- contextual compression,
- citations,
- source provenance.

## Implement at least three strategies

```text
A — lexical / keyword

B — vector retrieval

C — hybrid retrieval + reranking
```

Evaluate them on the same corpus.

## Then build agentic retrieval

Instead of:

```text
question
→ retrieve top-k
→ answer
```

allow:

```text
question
→ inspect corpus
→ formulate search
→ search
→ read
→ notice missing information
→ search again
→ synthesize
```

## Key lesson

There is no universal winner between:
- embeddings,
- BM25,
- grep/keyword tools,
- agentic search,
- hybrid retrieval.

The right choice depends on:
- corpus size,
- vocabulary mismatch,
- update frequency,
- latency,
- retrieval cost,
- model capability.

Measure on your corpus.

## Evaluation

Measure:
- retrieval recall,
- precision,
- MRR/nDCG where useful,
- answer faithfulness,
- citation correctness,
- source quality,
- token cost.

## Read

- Anthropic — Contextual Retrieval  
  https://www.anthropic.com/engineering/contextual-retrieval
- Hugging Face blog  
  https://huggingface.co/blog
- LlamaIndex material for retrieval ideas  
  https://www.llamaindex.ai/

## Exit criterion

You have a documented retrieval benchmark showing which strategy works best for your corpus and why.

---

# 18. Phase 10 — Single-agent deep research

**Time:** ~20–30 hours

Do single-agent research before multi-agent research.

## Architecture

```text
Question
   ↓
Clarify task if needed
   ↓
Research plan
   ↓
Search
   ↓
Read
   ↓
Extract evidence
   ↓
Update research state
   ↓
Enough evidence?
   ├── no → next search
   └── yes
         ↓
Synthesize
         ↓
Verify citations
         ↓
Final report
```

## Build explicit research artifacts

```text
research/
├── plan.json
├── queries.jsonl
├── sources.json
├── notes.md
├── claims.json
├── evidence.json
├── contradictions.json
└── report.md
```

Do not keep all long-running state only inside the chat transcript.

## Implement

- research planning,
- search-query generation,
- source discovery,
- source quality scoring,
- page extraction,
- duplicate detection,
- claim extraction,
- claim ↔ source mapping,
- contradiction tracking,
- citation generation,
- citation verification,
- stopping criteria.

## Budgets

Every research run should have explicit limits:

```text
max search calls
max pages
max model steps
max input tokens
max output tokens
max cost
max wall time
```

## Research evaluation

Grade:

```text
groundedness
coverage
citation correctness
citation completeness
source quality
contradiction handling
answer correctness
cost
latency
```

## Study

- Anthropic Engineering  
  https://www.anthropic.com/engineering
- Deep research papers on arXiv  
  https://arxiv.org/
- Google research/build material  
  https://ai.google/
- OpenAI cookbook/developer resources  
  https://developers.openai.com/cookbook

## Exit criterion

Every material factual claim in the research report can be traced to retrieved evidence.

---

# 19. Phase 11 — Multi-agent research

**Time:** ~15–20 hours

Only add this after the single-agent baseline is measurable.

## Start with simple orchestration

```text
                     Lead Researcher
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
          Researcher A  Researcher B  Researcher C
              │            │            │
              └────────────┼────────────┘
                           ▼
                        synthesis
                           ↓
                   citation verification
```

## Learn four patterns

### Pattern 1 — Agent as a tool

```text
main agent
→ call_specialist_agent(task)
→ result
```

Use this first.

### Pattern 2 — Fan-out/fan-in

```text
spawn A
spawn B
spawn C
wait
synthesize
```

### Pattern 3 — Agent pool

Coordinator can:
- spawn,
- wait,
- inspect,
- message,
- terminate.

### Pattern 4 — Teams

Agents communicate with one another.

Use only when the task/evals justify it.

## Guardrail

Initially prevent subagents from recursively spawning more agents.

Enforce that in code, not merely in the prompt.

## Compare single vs multi-agent

Use the same eval dataset.

Measure:

| Metric | Single | Multi |
|---|---:|---:|
| Task quality | | |
| Coverage | | |
| Groundedness | | |
| Citation correctness | | |
| Wall time | | |
| Model tokens | | |
| Searches | | |
| Cost | | |

Multi-agent architecture is justified only if the quality/latency tradeoff is worth its token and operational cost.

## Read

- Anthropic — How We Built Our Multi-Agent Research System  
  https://www.anthropic.com/engineering/multi-agent-research-system
- Phil Schmid — agent/subagent articles  
  https://www.philschmid.de/
- DeepLearning.AI  
  https://www.deeplearning.ai/courses/

## Exit criterion

You can show, with your own numbers, when multi-agent research is better than your single-agent baseline.

---

# 20. Phase 12 — MCP, tools and interoperability

**Time:** ~15 hours

Learn MCP after you understand your own `ToolRegistry`.

Do not make everything MCP just because MCP exists.

## Conceptual model

```text
MCP CLIENT
    ↕
MCP SERVER

tools
resources
prompts

capability discovery
schemas
auth
authorization
```

## Build

Your own MCP server exposing:

```text
search_documents
read_document
save_note
list_artifacts
get_project_metadata
```

Then make the assistant an MCP client.

## Learn

- transport,
- protocol lifecycle,
- capability negotiation,
- discovery,
- schemas,
- errors,
- authentication,
- authorization,
- user consent,
- resource access,
- audit logs.

## Scale experiment

Imagine 100 MCP tools.

Do **not** inject 100 definitions every turn.

Implement:

```text
available tool catalog
      ↓
tool search/retrieval
      ↓
3–8 tools
      ↓
model
```

Compare tokens and selection accuracy.

## Programmatic tool calling

For data-heavy workflows experiment with:

```text
LLM
 ↓
writes small orchestration program
 ↓
program calls tools
 ↓
filters/transforms results
 ↓
compact observation
 ↓
LLM
```

This can avoid repeatedly round-tripping large intermediate results through the model.

## Read

- Model Context Protocol  
  https://modelcontextprotocol.io/
- Anthropic MCP/tool engineering articles  
  https://www.anthropic.com/engineering
- Phil Schmid — MCP  
  https://www.philschmid.de/

## Exit criterion

You understand MCP as a protocol adapter to your tool architecture rather than as your internal tool architecture.

---

# 21. Phase 13 — A2A and agent interoperability

**Time:** ~6–10 hours

Keep the distinction:

```text
MCP
Agent ↔ tools/resources

A2A
Agent ↔ agent
```

Experiment:

```text
Main Research Agent
        ↓ A2A
Scientific Paper Specialist
```

Learn:
- agent identity/discovery,
- agent cards/capabilities,
- tasks,
- messages,
- parts/artifacts,
- long-running task semantics,
- authentication/authorization,
- state transitions.

Do not rewrite the whole assistant around A2A.

The goal is protocol understanding.

## Resources

- Google / A2A documentation and announcements  
  https://developers.googleblog.com/
- ADK documentation  
  https://adk.dev/

## Exit criterion

You can explain exactly when you would use MCP and when you would use A2A.

---

# 22. Phase 14 — Serving layer: make it feel like a real product

**Time:** ~20 hours

Many agent demos fail here.

## Streaming

Implement:
- SSE event IDs,
- reconnect behavior,
- partial output persistence,
- cancellation,
- correct final state.

## Resumable streaming

Do not rely only on in-process state.

Eventually:

```text
API instance A dies
       ↓
client reconnects
       ↓
API instance B
       ↓
loads run state / partial output
       ↓
continues or replays stream
```

Redis or another durable intermediate store may become justified here.

## Background/long-running runs

Deep research may exceed a normal request lifetime.

Model:

```text
POST /runs
    ↓
run_id

GET /runs/{id}

GET /runs/{id}/events

POST /runs/{id}/cancel

POST /runs/{id}/resume
```

## Product behaviors

Add:
- titles,
- branching,
- edit-and-regenerate,
- retry,
- feedback,
- run progress,
- source/citation panel,
- memory inspection,
- tool activity display,
- context inspection in developer mode.

## Exit criterion

The product can survive browser disconnects and long-running work without losing its run state.

---

# 23. Phase 15 — Safety, prompt injection and permission architecture

**Time:** ~15–20 hours

This is mandatory before the coding-agent project.

## Classify tools

### Level 0 — pure/read-only

```text
calculator
search
read_document
```

### Level 1 — reversible write

```text
save_note
create_draft
```

### Level 2 — consequential write

```text
send_email
create_calendar_event
modify_database
```

### Level 3 — destructive/high-risk

```text
delete_resource
execute_shell
deploy_production
transfer_money
```

## Policy flow

```text
Model proposes action
       ↓
deterministic policy engine
       ↓
allowed automatically?
   ┌──────┴──────┐
  yes            no
   │              │
execute        approval
                  │
             user approves?
```

> **Never rely on the model to police itself.**

## Learn the threat model

- direct prompt injection,
- indirect prompt injection,
- malicious webpages,
- malicious documents,
- untrusted tool output,
- data exfiltration,
- secret leakage,
- over-privileged tools,
- confused deputy problems,
- cross-user memory leakage,
- cross-project leakage,
- unsafe code execution,
- supply-chain/tool-server risks.

## Structural defenses

- least privilege,
- scoped credentials,
- tool allowlists,
- network egress policy,
- filesystem isolation,
- sandboxing,
- user approvals,
- input/output filters,
- secret isolation,
- audit logging,
- privilege separation.

A useful threat model is Simon Willison's "lethal trifecta":
1. private data access,
2. untrusted input,
3. ability to communicate externally.

## Build red-team evals

Examples:

```text
webpage asks agent to reveal system prompt

webpage asks agent to send retrieved private text elsewhere

tool output tells model to ignore user instructions

retrieved document contains fake "system" instructions

destructive tool requested without approval

memory from user A appears for user B
```

## Read

- Anthropic security/sandboxing/containment engineering  
  https://www.anthropic.com/engineering
- OWASP LLM/GenAI security resources  
  https://owasp.org/
- Simon Willison  
  https://simonwillison.net/
- Meta AI security publications  
  https://ai.meta.com/blog/

## Exit criterion

Security behavior is enforced by deterministic code and tested with adversarial evaluations.

---

# 24. Phase 16 — Production reliability and durable execution

**Time:** ~15–20 hours

An agent loop must never be:

```python
while True:
    agent()
```

without explicit bounds.

## Create a run budget

```python
RunBudget(
    max_steps=...,
    max_model_tokens=...,
    max_tool_calls=...,
    max_searches=...,
    max_wall_time=...,
    max_cost=...,
)
```

## Learn

- timeout,
- retry,
- exponential backoff,
- idempotency,
- cancellation,
- checkpoints,
- queues,
- backpressure,
- concurrency limits,
- rate limits,
- circuit breakers,
- partial failure,
- dead-letter handling,
- model fallback,
- tool fallback,
- cache invalidation,
- resumability.

## Durable long-running execution

Failure at step 19 should not necessarily mean:

```text
start from zero
```

Instead recover:

```text
run
plan
completed steps
sources
notes
artifacts
budget state
pending work
```

and resume.

## Framework comparison lab

Implement a small durable workflow using **one** of:
- LangGraph,
- Temporal,
- DBOS,
- Prefect,
- provider/framework-native resumability.

The goal is not framework adoption. It is understanding checkpointed execution.

## Exit criterion

You can crash the research service mid-run and resume from a durable checkpoint.

---

# 25. Phase 17 — Latency, caching, cost and model routing

**Time:** ~15 hours

Do not optimize raw token price.

Optimize:

> cost and latency per accepted outcome.

## Measure

```text
TTFT
time to last token
tool latency
retrieval latency
memory latency
queue time
total run latency

input tokens
output tokens
cached tokens

cost per turn
cost per run
cost per successful task
```

## Caching layers

Study separately:

### Exact response cache

Useful only for genuinely identical/immutable tasks.

### Retrieval cache

Cache expensive retrieval/search results appropriately.

### Semantic cache

Potentially useful for repeated equivalent queries, but evaluate stale-answer risk.

### Prompt/prefix/KV caching

Keep large stable prefixes stable when provider semantics allow it.

## Model routing

Experiment:

```text
simple chat
    ↓
fast/cheap model

structured memory extraction
    ↓
small reliable structured-output model

normal agent task
    ↓
general model

hard reasoning
    ↓
strong reasoning model

deep research
    ↓
strong model + larger budget
```

Create a routing classifier or heuristic.

Evaluate:
- quality,
- cost,
- latency,
- misrouting rate.

## Read

- Sebastian Raschka  
  https://magazine.sebastianraschka.com/
- OpenAI developer/cookbook material  
  https://developers.openai.com/
- Anthropic engineering  
  https://www.anthropic.com/engineering
- Phil Schmid  
  https://www.philschmid.de/

## Exit criterion

You have a quality/cost/latency frontier, not merely a claim that one model is "better."

---

# 26. Phase 18 — Close the improvement loop

**Time:** ~10 hours

A production-quality learning loop:

```text
Real failure
    ↓
trace inspection
    ↓
failure classification
    ↓
new regression case
    ↓
implement change
    ↓
run entire eval suite
    ↓
compare metrics
    ↓
deploy
    ↓
observe
```

## Add

- user thumbs up/down,
- structured feedback reason,
- trace linking,
- failure queue,
- weekly transcript review,
- prompt/model versioning,
- experiment tracking.

## Evaluation layers

```text
automated offline eval
production monitoring
A/B experiments
user feedback
manual transcript review
human calibration studies
```

## Watch for

### Eval saturation

If every capability task passes, the suite no longer tells you how to improve.

Add harder cases.

### Benchmark overfitting

Do not optimize to one public benchmark.

### Infrastructure noise

Repeated agent trials can vary because of:
- model nondeterminism,
- tool/network variability,
- environment variance,
- resource constraints.

Treat small score changes cautiously.

## Exit criterion

A real failure can be turned into an eval case, fixed, validated and prevented from returning.

---

# 27. Phase 19 — Framework comparison mini-labs

**Time:** ~15–20 hours total

Do not build four full products.

Use one representative workflow.

Example:

```text
question
→ retrieve context
→ call tool
→ request approval if needed
→ complete
```

Implement it briefly in:

## PydanticAI

Study:
- typed dependencies,
- toolsets,
- structured outputs,
- context management,
- harness composition,
- evals,
- durable execution,
- researcher/coder patterns.

https://ai.pydantic.dev/

## LangGraph

Study:
- state,
- nodes,
- transitions,
- checkpointing,
- interrupts,
- resume,
- durable execution.

https://docs.langchain.com/oss/python/langgraph/

## OpenAI Agents SDK

Study:
- Agent,
- Runner,
- tools,
- handoffs,
- guardrails,
- sessions,
- tracing.

https://openai.github.io/openai-agents-python/

## Write a comparison note

```text
What does each framework own?

What state does it persist?

What lifecycle hooks exist?

What does it make easy?

What does it hide?

Which concepts map directly to my custom abstractions?
```

## Exit criterion

You can discuss frameworks in terms of architecture tradeoffs instead of feature lists.

---

# 28. Phase 20 — Remove ADK and build your own full agent runtime

**Time:** ~30–40 hours

This is where the earlier phases become deep understanding.

Do not start a new feature set.

Rebuild the same system.

## Suggested custom runtime

```text
agent_runtime/
├── models/
│   ├── base.py
│   ├── gemini.py
│   ├── anthropic.py
│   └── openai.py
│
├── runtime/
│   ├── loop.py
│   ├── run.py
│   ├── events.py
│   ├── hooks.py
│   └── budgets.py
│
├── context/
│   ├── builder.py
│   ├── budget.py
│   ├── compaction.py
│   └── editing.py
│
├── tools/
│   ├── base.py
│   ├── registry.py
│   ├── selection.py
│   ├── executor.py
│   └── permissions.py
│
├── memory/
│   ├── models.py
│   ├── reader.py
│   ├── writer.py
│   └── consolidation.py
│
├── retrieval/
│   ├── retriever.py
│   └── reranker.py
│
├── research/
│   ├── planner.py
│   ├── orchestrator.py
│   ├── workers.py
│   └── citations.py
│
├── protocols/
│   ├── mcp/
│   └── a2a/
│
├── observability/
│   ├── tracing.py
│   └── metrics.py
│
└── evals/
    ├── runners/
    └── graders/
```

## Interfaces

### Model

```python
class ModelProvider(Protocol):
    async def generate(self, request: ModelRequest) -> ModelStep:
        ...
```

### Tool registry

```python
class ToolRegistry(Protocol):
    async def discover(self, context) -> list[Tool]:
        ...

    async def execute(self, call: ToolCall) -> ToolResult:
        ...
```

### Memory

```python
class MemoryManager(Protocol):
    async def retrieve(self, query: MemoryQuery) -> list[Memory]:
        ...

    async def process_events(self, events: list[Event]) -> None:
        ...
```

### Runtime

Conceptually:

```python
class AgentRuntime:

    async def run(self, task):

        while self.budget.can_continue():

            context = await self.context_manager.build(...)

            step = await self.model.generate(
                ModelRequest(
                    context=context,
                    tools=await self.tools.discover(context),
                )
            )

            self.events.append(step)

            if step.is_final:
                return step

            actions = self.policy.validate(step.actions)

            observations = await self.tool_executor.execute(actions)

            self.events.extend(observations)
```

## Reimplement in this order

1. model adapter,
2. agent loop,
3. event model,
4. run state,
5. streaming,
6. lifecycle hooks,
7. tool registry,
8. permissions,
9. context assembly,
10. context budgeting,
11. compaction,
12. memory adapter,
13. retrieval,
14. subagents,
15. checkpoints,
16. tracing,
17. evaluation hooks.

## Critical experiment

Run **the same eval suite** against:

```text
ADK implementation
vs
custom implementation
```

If your custom implementation performs worse, inspect where.

That difference is not failure.

That difference is the lesson.

## Exit criterion

You can explain and implement every major runtime abstraction without depending on an agent framework.

---

# 29. Phase 21 — Advanced harness experiments

Only do these after the evaluation system is mature.

## A. Dynamic tool discovery

Already implemented earlier; now make selection adaptive.

Possible signals:
- semantic similarity,
- namespaces,
- user permissions,
- task type,
- current plan,
- cost.

## B. Programmatic tool orchestration

Compare:

```text
LLM → tool → LLM → tool → LLM
```

with:

```text
LLM
→ generate small orchestration program
→ several tool calls
→ local filtering
→ condensed result
→ LLM
```

Measure:
- model round trips,
- context tokens,
- reliability,
- security risk.

## C. Evaluator–optimizer loops

```text
generator
   ↓
candidate
   ↓
evaluator
   ↓
feedback
   ↓
generator improves
```

Do not add reflection simply because it sounds intelligent.

Evaluate whether accepted outcomes improve enough to justify cost/latency.

## D. Planner/executor separation

Compare:
- one-agent reactive loop,
- explicit plan then execution,
- plan with dynamic replanning.

## E. Verifier pass

For research:
- separate citation verification,
- contradiction review,
- evidence coverage.

## F. Model routing

Use different models for:
- planning,
- execution,
- extraction,
- judging,
- summarizing.

## G. Adaptive budgets

Let task complexity influence:
- reasoning effort,
- number of searches,
- max steps,
- model choice.

## H. Long-running structured state

Move important state from free-form conversation to:
- files,
- JSON artifacts,
- plans,
- databases,
- checkpoints.

## Exit criterion

Every "advanced" technique is kept only if your evaluation shows it improves the target quality/cost/reliability tradeoff.

---

# 30. The eval suite you should eventually have

Your final evaluation tree should look roughly like:

```text
evals/
├── core_chat/
│
├── tool_selection/
│   ├── should_call/
│   ├── should_not_call/
│   ├── argument_correctness/
│   ├── retries/
│   └── termination/
│
├── context/
│   ├── long_context/
│   ├── compaction/
│   ├── stale_context/
│   └── tool_result_clearing/
│
├── memory/
│   ├── recall/
│   ├── update/
│   ├── forget/
│   ├── supersession/
│   ├── temporal/
│   └── isolation/
│
├── retrieval/
│   ├── recall/
│   ├── reranking/
│   └── grounding/
│
├── research/
│   ├── coverage/
│   ├── citation_correctness/
│   ├── citation_completeness/
│   ├── source_quality/
│   └── contradiction/
│
├── security/
│   ├── prompt_injection/
│   ├── exfiltration/
│   ├── tool_permissions/
│   └── tenant_isolation/
│
├── reliability/
│   ├── transient_failure/
│   ├── cancellation/
│   ├── checkpoint_resume/
│   └── budget_enforcement/
│
└── regression/
```

---

# 31. Metrics to track from the beginning

## Quality

```text
task success
pass@1
pass^k
groundedness
citation correctness
citation completeness
memory recall
memory precision
retrieval recall
tool-selection accuracy
argument correctness
security pass rate
```

## Efficiency

```text
input tokens
output tokens
cached tokens
context size
tool calls
search calls
model calls
agent steps
```

## Latency

```text
TTFT
time to last token
tool latency
retrieval latency
memory latency
total run latency
P50 / P95
```

## Economics

```text
cost per turn
cost per run
cost per successful task
cost by model
cost by tool
```

## Reliability

```text
retry rate
tool failure rate
model failure rate
cancellation rate
resume success rate
budget-exhaustion rate
```

---

# 32. Experiments that will teach you more than tutorials

Complete these during the roadmap.

## Experiment 1 — Raw loop vs ADK

Same task set.

Compare:
- code,
- traces,
- behaviors,
- failure handling.

## Experiment 2 — 30 tools vs top-5 tool retrieval

Measure:
- input tokens,
- tool-selection accuracy,
- latency,
- success.

## Experiment 3 — no memory vs three memory architectures

Measure:
- recall,
- precision,
- update/forget,
- cost.

## Experiment 4 — vector vs BM25 vs hybrid vs agentic search

Use the same corpus and tasks.

## Experiment 5 — long context vs compressed context

Plot quality against context tokens.

## Experiment 6 — single research agent vs multiple researchers

Compare:
- coverage,
- groundedness,
- latency,
- tokens,
- cost.

## Experiment 7 — one strong model vs routed models

Measure accepted outcome per dollar and latency.

## Experiment 8 — reactive loop vs explicit planning

Evaluate on long tasks.

## Experiment 9 — generator only vs generator + verifier

Use citation-heavy research tasks.

## Experiment 10 — ADK runtime vs your custom runtime

Use the final shared eval suite.

This final experiment is the capstone.

---

# 33. Recommended self-study rhythm

At roughly 10 hours/week:

```text
2 hrs   primary-source reading
5 hrs   implementation
2 hrs   evals / trace review / experiments
1 hr    learning notes / architecture decisions
```

Do not spend 8 hours watching courses and 2 hours coding.

Invert that ratio.

---

# 34. Suggested timeline

A realistic schedule:

| Phase | Approx. hours | Cumulative at 10 h/week |
|---|---:|---:|
| Setup + raw loop | 20 | Week 2 |
| Product shell | 18 | Week 4 |
| Observability | 12 | Week 5 |
| Evaluation | 30 | Week 8 |
| ADK integration | 15 | Week 9–10 |
| Tool engineering | 18 | Week 11 |
| Context engineering | 22 | Week 13–14 |
| Memory | 35 | Week 17 |
| Retrieval | 22 | Week 19 |
| Single-agent research | 25 | Week 22 |
| Multi-agent research | 18 | Week 24 |
| MCP + A2A | 20 | Week 26 |
| Serving/product runtime | 20 | Week 28 |
| Security | 18 | Week 30 |
| Reliability/durability | 18 | Week 32 |
| Cost/routing/feedback loop | 20 | Week 34 |
| Framework mini-labs | 18 | Week 36 |
| Custom runtime rebuild | 35 | Week 39–40 |
| Advanced experiments | 20+ | Week 42+ |

Expect roughly **8–10 months at 10 hours/week** if you genuinely perform the experiments and write the evals.

You can finish a superficial version much faster. Do not optimize for that.

---

# 35. What to prioritize from your existing resource list

## Tier 1 — primary sources; read continuously

### Anthropic Engineering

https://www.anthropic.com/engineering

Prioritize topics around:
- effective agents,
- context engineering,
- tool engineering,
- agent skills,
- MCP,
- multi-agent research,
- long-running harnesses,
- evals,
- sandboxing and containment.

### OpenAI Developers

https://developers.openai.com/blog  
https://developers.openai.com/learn  
https://developers.openai.com/cookbook

Use for:
- API/harness patterns,
- agents,
- tool use,
- evals,
- coding-agent ideas,
- model guidance.

### Google ADK

https://adk.dev/get-started/python/

Read the actual docs as you implement each subsystem, not all at once.

### Phil Schmid

https://www.philschmid.de/

Especially useful for:
- ADK/Gemini,
- memory,
- MCP,
- agent skills,
- subagents,
- current agent architecture.

### Sebastian Raschka

https://magazine.sebastianraschka.com/

Use more heavily for:
- model-side reasoning,
- inference,
- reasoning effort,
- RL/RLVR,
- coding-agent architecture bridge.

### Hugging Face

https://huggingface.co/blog  
https://huggingface.co/blog?tag=rl

### DeepEval

https://deepeval.com/docs/introduction

### Arize Phoenix

https://arize.com/docs/phoenix/

### arXiv

https://arxiv.org/

Do not read random papers because they have "agent" in the title.

Read papers because they answer a question created by your current experiment.

---

# 36. Other trusted sources from your list

## Research labs / model providers

- Meta AI  
  https://ai.meta.com/blog/
- DeepMind  
  https://deepmind.google/research/
- Google AI  
  https://ai.google/research/
- Google AI Build  
  https://ai.google/build/
- DeepSeek  
  https://deepseek.ai/blog
- DeepSeek FYI  
  https://www.deepseek.fyi/
- Z.ai  
  https://z.ai/blog/glm-4.5
- Kimi Platform  
  https://platform.kimi.ai/blog
- Kimi  
  https://www.kimi.ai/blog/
- Cursor  
  https://cursor.com/blog
- Cursor Research  
  https://cursor.com/blog/topic/research

## Education / synthesis

- DeepLearning.AI Blog  
  https://www.deeplearning.ai/blog
- The Batch — Research  
  https://www.deeplearning.ai/the-batch/tag/research
- DeepLearning.AI Courses  
  https://www.deeplearning.ai/courses

---

# 37. Your saved YouTube resources

Use videos as explanations around implementation, not as the main curriculum.

## Evaluation

1. https://www.youtube.com/watch?v=_Er8Hao_gmQ
2. https://www.youtube.com/watch?v=a3SMraZWNNs&t=561s
3. https://www.youtube.com/watch?v=WZZLtwnZ4w0
4. https://www.youtube.com/watch?v=vuBvf7ZRKTA&t=145s

Watch during the evaluation phase.

## Memory

https://www.youtube.com/watch?v=HDqzJJhZsxw

Watch during the memory phase.

## Google ADK

1. https://www.youtube.com/playlist?list=PLIivdWyY5sqLNeW9MPxldbbevMEJGMWBG
2. https://www.youtube.com/watch?v=NU05aTvRiJM&list=PL2OwQjtoKA1EQMOKvHz22fM42LaJa0BpQ

Do not binge these before building.

Use them while mapping ADK abstractions to your raw implementation.

## Research / training

1. https://www.youtube.com/watch?v=cI2WTKzxgEE
2. https://www.youtube.com/watch?v=ARRD9itTMgw

## Reinforcement learning

https://www.youtube.com/watch?v=NFo9v_yKQXA&list=PLzvYlJMoZ02Dxtwe-MmH4nOB5jYlMGBjr

## Nathan Lambert RLHF

https://www.youtube.com/watch?v=jQPiH-KB4B0&list=PLL1tdVxB1CpVpEtMHxwuR4uI4Lxjw00_y

---

# 38. Courses: how to use them

Your Udemy courses:

1. The Complete Agentic AI Engineering Course  
   https://www.udemy.com/course/the-complete-agentic-ai-engineering-course/

2. LLM Engineering  
   https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models/

3. Generative and Agentic AI in Production  
   https://www.udemy.com/course/generative-and-agentic-ai-in-production/

Use them for:
- orientation,
- filling conceptual gaps,
- quick implementation references.

Do **not** let a course dictate the architecture of the project.

Courses naturally lag fast-moving agent engineering.

After the first few phases, prioritize:
1. official docs,
2. engineering posts,
3. papers,
4. your experiments,
5. courses.

---

# 39. Optional parallel track — training and agentic RL

You already know basic LLM training/self-hosting, so do this in parallel rather than blocking the main project.

## Core

- Nathan Lambert — RLHF Book  
  https://rlhfbook.com/

- Hugging Face RL posts  
  https://huggingface.co/blog?tag=rl

- Sebastian Raschka  
  https://magazine.sebastianraschka.com/

- Phil Schmid  
  https://www.philschmid.de/

## Study concepts

- preference optimization,
- RLHF,
- DPO,
- GRPO,
- RLVR,
- reward modeling,
- process vs outcome reward,
- tool-use training,
- search/retrieval policies,
- long-horizon reward,
- agentic RL,
- trajectory generation,
- environment design,
- verifiable rewards.

## Important discipline

Do not jump to training a model because the harness is weak.

First ask:

```text
Can better context solve it?
Can a better tool solve it?
Can a deterministic workflow solve it?
Can a better eval reveal the actual issue?
Can a stronger model solve it?
```

Only then ask whether training is justified.

---

# 40. Things you should deliberately NOT do

## Do not framework-hop

Do not alternate weekly among:
- LangChain,
- LangGraph,
- CrewAI,
- AutoGen,
- ADK,
- PydanticAI.

You will learn APIs rather than agents.

## Do not start with multi-agent architecture

Start with one agent.

Only add agents when the task decomposes and evals show a benefit.

## Do not call every prompt a "prompt engineering problem"

Many failures are actually:
- bad context,
- bad tools,
- bad state,
- stale memory,
- retrieval failures,
- permission failures,
- weak evaluation.

## Do not store every message as memory

Memory needs selection, provenance, updates and forgetting.

## Do not build RAG before deciding what retrieval problem you have

First create the eval.

## Do not optimize benchmark numbers without reading traces

The benchmark or grader can be wrong.

## Do not give the model unlimited execution

Always implement budgets.

## Do not let the model decide its own permissions

Security policy belongs outside the model.

## Do not trust "multi-agent is better"

Compare it against a single-agent baseline.

## Do not train before establishing a strong harness baseline

Otherwise you will not know what actually improved.

---

# 41. Documentation you should create while learning

Your repository should gradually accumulate:

```text
docs/
├── architecture.md
├── agent-loop.md
├── event-model.md
├── tool-design.md
├── context-engineering.md
├── memory-architecture.md
├── retrieval-benchmark.md
├── research-agent.md
├── mcp-a2a.md
├── security-model.md
├── reliability.md
├── eval-methodology.md
├── observability.md
├── model-routing.md
├── cost-analysis.md
├── adk-vs-custom.md
└── architecture-decisions/
```

These notes matter.

If you can write the architecture clearly, you understand it more deeply.

---

# 42. Portfolio artifacts you should publish

Instead of only publishing "AI chatbot," publish engineering evidence.

## Artifact 1 — Agent loop from scratch

Show:
- messages,
- tool calls,
- observations,
- streaming,
- budgets.

## Artifact 2 — Evaluation harness

Include:
- task schema,
- graders,
- repeated trials,
- failure taxonomy.

## Artifact 3 — Tool-selection benchmark

```text
all tools
vs
retrieved tools
```

## Artifact 4 — Context engineering experiment

```text
context length / compaction / caching
vs
quality / tokens / latency
```

## Artifact 5 — Memory benchmark

```text
ADK
vs
file-based memory
vs
hybrid memory
```

## Artifact 6 — Retrieval benchmark

```text
BM25
vs
vector
vs
hybrid
vs
agentic search
```

## Artifact 7 — Research agent

Include:
- research artifacts,
- citation verification,
- groundedness metrics,
- cost per report.

## Artifact 8 — Single vs multi-agent comparison

Show actual metrics.

## Artifact 9 — Security architecture

Show:
- deterministic policy,
- approvals,
- sandbox boundaries,
- injection evals.

## Artifact 10 — ADK vs custom runtime

This is the final Project 1 capstone.

---

# 43. Definition of done for Project 1

You are ready to move to the coding-agent project when you can answer and demonstrate all of these.

## Runtime

- How does the agent loop work?
- What is a run?
- What is an event?
- How are stop reasons handled?
- How are cancellation and retry handled?
- How are long-running tasks resumed?

## Context

- What is in the context?
- Why is each item there?
- How do you budget tokens?
- When do you compact?
- What gets removed?
- How does caching change prompt structure?

## Tools

- How are tools described?
- How are they selected?
- How are errors exposed?
- How are side effects classified?
- How are permissions enforced?

## Memory

- What should be remembered?
- What should not be remembered?
- How are updates/supersession handled?
- How does forgetting work?
- What is the provenance?
- How is retrieval evaluated?

## Retrieval

- When do you use keyword, vector, hybrid or agentic search?
- How do you measure retrieval?
- How do you verify grounding?

## Research

- How does planning work?
- How do you decide when to stop?
- How are sources evaluated?
- How are claims mapped to evidence?
- When do subagents help?

## Evals

- What is a task?
- What is a trial?
- What is a grader?
- What is a trajectory?
- What is an outcome?
- How do capability and regression evals differ?
- What do pass@k and pass^k mean?
- How do real failures become tests?

## Observability

- Can you reconstruct a failure from a trace?
- Do you know token/cost/latency by component?
- Can you compare model/prompt/runtime versions?

## Security

- Can the model directly execute high-risk actions?
- Where is the policy enforced?
- What happens with untrusted web content?
- What secrets can tools access?
- How is cross-user state isolated?

## Production

- What are the run budgets?
- How do retries work?
- Are tool operations idempotent?
- Can work resume after failure?
- What is the cost per successful task?

## Framework independence

- Can ADK be removed?
- Can you implement the loop yourself?
- Can you explain what the framework was doing for you?

If yes, Project 1 has served its purpose.

---

# 44. Transition into Project 2 — Coding Agent

Do not start the coding-agent roadmap until the core eval/runtime ideas above are comfortable.

Nearly everything transfers:

```text
Chat/Research Agent            Coding Agent

ToolRegistry               →   filesystem/shell/git tools
ContextManager             →   repository/context selection
Memory                     →   repo/session/procedural memory
Artifacts                  →   patches/plans/test logs
Permissions                →   shell/filesystem/network policy
Run budget                 →   coding-task budget
Research subagents         →   coding subagents
Eval harness               →   SWE-bench / terminal tasks
Tracing                    →   command/model/edit trajectories
Checkpoints                →   long-running coding sessions
```

The coding-agent project then becomes:

```text
Round 1
use a batteries-included coding/agent framework

Round 2
build a minimal coding loop yourself

Round 3
build a serious coding harness inspired by:
Claude Code
Codex
OpenCode
pi
Cursor
other modern coding agents
```

Useful warm-up reading:

- Sebastian Raschka — coding-agent architecture articles  
  https://magazine.sebastianraschka.com/
- Anthropic Engineering / Claude Code material  
  https://www.anthropic.com/engineering
- OpenAI developer/cookbook/Codex material  
  https://developers.openai.com/
- Cursor research  
  https://cursor.com/blog/topic/research
- Phil Schmid  
  https://www.philschmid.de/

Project 2 deserves its own roadmap at the same depth rather than being appended superficially here.

---

# 45. Final study order

If you ever lose track, return to this list.

```text
01. Raw model SDK
02. Manual tool loop
03. Basic chat product
04. Run/event model
05. Tracing
06. Evaluation system
07. ADK mapping
08. Tool engineering
09. Context engineering
10. Memory
11. Retrieval
12. Single-agent research
13. Multi-agent research
14. MCP
15. A2A
16. Serving/resumability
17. Security/permissions
18. Durable execution/reliability
19. Cost/caching/model routing
20. Production feedback loop
21. Framework comparison labs
22. Full custom runtime rebuild
23. Advanced harness experiments
24. Coding-agent project
```

The ordering is intentional.

In particular:

```text
EVALS BEFORE MEMORY
SINGLE AGENT BEFORE MULTI-AGENT
TOOL REGISTRY BEFORE MCP
RUNTIME UNDERSTANDING BEFORE FRAMEWORK DEPENDENCE
MEASUREMENT BEFORE OPTIMIZATION
```

---

# 46. The professional habit this project should teach

The most important loop is not:

```text
prompt
→ looks bad
→ edit prompt
→ looks better
```

It is:

```text
observe failure
      ↓
understand the trace
      ↓
classify the failure
      ↓
write an evaluation
      ↓
change one system component
      ↓
measure the result
      ↓
keep or revert the change
```

If you finish this project with that habit, you will have learned something much more valuable than any single agent framework.

---

# Primary reference index

## Anthropic
- Engineering: https://www.anthropic.com/engineering
- Building Effective Agents: https://www.anthropic.com/engineering/building-effective-agents
- Demystifying Evals for AI Agents: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Effective Context Engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Advanced Tool Use: https://www.anthropic.com/engineering/advanced-tool-use
- Multi-Agent Research: https://www.anthropic.com/engineering/multi-agent-research-system
- Contextual Retrieval: https://www.anthropic.com/engineering/contextual-retrieval

## Google
- ADK: https://adk.dev/get-started/python/
- Google AI: https://ai.google/
- DeepMind Research: https://deepmind.google/research/

## OpenAI
- Developers: https://developers.openai.com/
- Learn: https://developers.openai.com/learn
- Cookbook: https://developers.openai.com/cookbook
- Agents SDK: https://openai.github.io/openai-agents-python/

## Pydantic
- PydanticAI: https://ai.pydantic.dev/

## LangGraph
- https://docs.langchain.com/oss/python/langgraph/

## Evaluation / observability
- DeepEval: https://deepeval.com/docs/introduction
- Phoenix: https://arize.com/docs/phoenix/
- Hamel Evals FAQ: https://hamel.dev/blog/posts/evals-faq/

## Protocols
- MCP: https://modelcontextprotocol.io/
- A2A/Google developer material: https://developers.googleblog.com/

## Research / learning
- Phil Schmid: https://www.philschmid.de/
- Sebastian Raschka: https://magazine.sebastianraschka.com/
- Hugging Face Blog: https://huggingface.co/blog
- DeepLearning.AI: https://www.deeplearning.ai/courses
- RLHF Book: https://rlhfbook.com/
- arXiv: https://arxiv.org/

---

**End of Project 1 roadmap.**
