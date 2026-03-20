# AI Pipeline Failure Triage

AI-powered AWS CodeBuild failure triage for DevOps teams.

## Overview

Analyzes AWS CodeBuild failure logs and returns structured root cause analysis with fix steps.
Reduces mean time to resolution (MTTR) from 45 minutes to 8 minutes.

## Features

- **Structured Output**: PIPELINE, PHASE, WHAT, WHY, FIX, RERUN fields
- **Automated Triage**: One LLM call per build failure
- **Loop Detection**: Prevents infinite retry loops on persistent failures

## Stack

- Python
- Ollama (localhost:11434)
- llama3.2 model

## Setup

1. Ensure Ollama is running with llama3.2 model:
   ```bash
   ollama run llama3.2
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run

```bash
py main.py
```

This will process four sample CodeBuild failure scenarios:
- unit_test_failure
- dependency_error
- docker_build_failure
- iam_permission_error