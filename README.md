# Multi-Agent LLM Orchestrator

This repository contains a production-ready multi-agent orchestration framework
that collaborates with an OpenAI-compatible large language model to deliver
strategic plans, research insights, executable blueprints, and risk assessments
for ambitious missions.

## Getting Started

1. **Create and activate a virtual environment** (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Provide your LLM configuration** via environment variables:

   | Variable            | Description                                           |
   | ------------------- | ----------------------------------------------------- |
   | `_OPENAI_API_KEY`   | API key for the OpenAI-compatible endpoint            |
   | `_OPENAI_BASE_URL`  | (Optional) Override base URL for the API              |
   | `_MODEL_NAME`       | Default model identifier (e.g., `gpt-4.1-mini`)       |

4. **Run the workflow**:

   ```bash
   python run_multiagent.py --mission "Launch a climate-positive smart city" --context "Focus on coastal resilience" --output artifacts/report.md
   ```

   The command prints each agent's deliverable to the terminal and writes a
   consolidated Markdown report if the `--output` flag is supplied. All LLM
   requests and responses are logged to `logs/llm.log`.

## Logs

The application automatically persists every LLM request and response in
`logs/llm.log`. These logs exclude API credentials while capturing prompts,
model metadata, outputs, and usage metrics to support reproducibility and
auditing.
