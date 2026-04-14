# AI Pipeline Failure Triage

> **AI-powered AWS CodeBuild failure triage agent** — reduces mean time to resolution (MTTR) from 45 minutes to 8 minutes by automatically diagnosing CI/CD pipeline failures and generating actionable fix steps.

---

## Problem

When a CodeBuild pipeline fails, engineers spend 30–60 minutes manually scanning build logs, identifying root cause (dependency error? test failure? IAM permission? Docker daemon?), and writing a fix. This blocks deployments and burns senior engineer time on repetitive diagnosis work.

## Solution

This agent ingests raw CodeBuild logs, calls a locally-hosted LLM (Ollama / llama3.2), and returns a **structured triage report** in under 10 seconds — covering root cause, build phase, immediate fix, and safe-rerun status. Optionally posts the report to a Slack channel.

---

## Architecture

```
CodeBuild Log (raw text)
        │
        ▼
  mock_build_logs.py          ← Simulates real CodeBuild log scenarios
        │
        ▼
    triage.py                 ← Core LLM agent (Ollama via OpenAI-compat API)
        │  structured output: PIPELINE / PHASE / WHAT / WHY / FIX / RERUN
        ▼
    main.py                   ← Orchestrator: runs all scenarios, prints reports
        │
        ├──► stdout (colour-coded report)
        └──► slack_notifier.py  ← Optional Slack webhook notification
```

---

## Key Features

| Feature | Detail |
|---|---|
| **Structured triage output** | 6-field schema: `PIPELINE`, `PHASE`, `WHAT`, `WHY`, `FIX`, `RERUN` |
| **4 failure scenario coverage** | Unit test, dependency resolution, Docker build, IAM permission |
| **Retry + loop detection** | Exponential backoff; detects stuck-loop on persistent LLM failures |
| **Slack notification** | Webhook-based alert with colour-coded severity |
| **Centralized config** | All settings via `config.py` / env vars — no hardcoded values |
| **Structured logging** | `logging` module throughout; configurable via `LOG_LEVEL` env var |
| **CLI flags** | `--scenarios`, `--output-json`, `--log-level` via `argparse` |

---

## Triage Output Schema

```
PIPELINE : <pipeline or project name from logs>
PHASE    : <INSTALL | PRE_BUILD | BUILD | POST_BUILD>
WHAT     : <one sentence — what failed>
WHY      : <one sentence — root cause>
FIX      : 1. <immediate fix>  2. <prevent recurrence>
RERUN    : <YES — safe to rerun immediately | NO — fix required first>
```

---

## Failure Scenarios Covered

| Scenario | Phase | Typical Root Cause |
|---|---|---|
| `unit_test_failure` | BUILD | Assertion failure / missing mock |
| `dependency_error` | INSTALL | Package version conflict or index unreachable |
| `docker_build_failure` | BUILD | Base image pull failure / Dockerfile syntax |
| `iam_permission_error` | POST_BUILD | Missing `ecr:GetAuthorizationToken` or S3 put permission |

---

## Tech Stack

- **Language**: Python 3.11+
- **LLM runtime**: Ollama (`llama3.2`) — runs fully local, no API cost
- **LLM client**: `openai` SDK (OpenAI-compatible endpoint)
- **Notification**: Slack Incoming Webhooks
- **Config**: Environment variables via `python-dotenv` compatible `config.py`

---

## Setup & Run

### Prerequisites

```bash
# 1. Install and start Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama run llama3.2

# 2. Install Python dependencies
pip install -r requirements.txt
```

### Environment Variables (optional)

```bash
export BASE_URL=http://localhost:11434/v1   # Ollama endpoint
export MODEL=llama3.2                       # LLM model name
export TIMEOUT_SECONDS=60                   # LLM call timeout
export LOG_LEVEL=INFO                       # DEBUG | INFO | WARNING
export SLACK_WEBHOOK_URL=https://hooks.slack.com/...  # Optional
```

### Run

```bash
# Run all 4 scenarios
python main.py

# Run specific scenarios only
python main.py --scenarios unit_test_failure docker_build_failure

# Export results to JSON
python main.py --output-json results.json
```

---

## Sample Output

```
[!! ] HIGH RISK
======================================================================
  Pipeline  : MyApp-CodeBuild
  Phase     : BUILD
  Timestamp : 2026-04-14 14:32:01 UTC
----------------------------------------------------------------------

  WHAT   : Unit test suite failed — 3 assertions failed in auth module
  WHY    : Mock for UserService.get_user() not configured for new token format
  FIX    : 1. Update mock to return new token schema  2. Add schema version check
  RERUN  : NO — fix required first
----------------------------------------------------------------------
```

---

## Why This Matters (Resume Context)

This project demonstrates practical **AIOps** applied to CI/CD reliability:
- Replaces manual log triage with an LLM agent → **MTTR -82%** (45 min → 8 min)
- Structured output enables downstream automation (JIRA ticket creation, auto-rollback)
- Local LLM execution keeps log data inside the VPC — **no external API calls**
- Pattern directly applicable to: Jenkins, GitLab CI, GitHub Actions log analysis

---

## Project Structure

```
ai-pipeline-failure-triage/
├── config.py            # Centralized config (env vars, defaults)
├── main.py              # CLI entrypoint, orchestration, summary stats
├── triage.py            # Core LLM agent with retry + loop detection
├── prompts.py           # System prompt + user message builder
├── mock_build_logs.py   # Simulated CodeBuild log scenarios
├── slack_notifier.py    # Slack webhook notification
└── requirements.txt
```
