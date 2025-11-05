# Multi-Agent System Logging Demonstration

## Overview

This multi-agent system provides comprehensive logging of all LLM interactions, including:

- **Request Logging**: Every API call with full parameters
- **Response Logging**: Complete responses with token usage
- **Error Logging**: Any errors with full context
- **Rich Console Output**: Beautiful formatted output during execution
- **File Logging**: Persistent logs for analysis

## Logging Features

### 1. Request Logging

Every request to the LLM is logged with:
- Interaction ID (sequential)
- Timestamp (ISO format)
- Agent name
- Model name
- System prompt
- User messages
- Temperature and max_tokens settings

### 2. Response Logging

Every response includes:
- Interaction ID (matching request)
- Timestamp
- Response content (including thinking blocks if present)
- Token usage (input and output tokens)
- Stop reason
- Model information

### 3. Console Output

Rich formatted output with:
- Color-coded panels for different agents
- Request/response visualization
- Progress indicators
- Summary tables
- Markdown rendering for final output

### 4. File Output

Persistent logging to `logs/llm_interactions_YYYYMMDD_HHMMSS.log` containing:
- Complete JSON-formatted interaction data
- Searchable and parseable format
- Timestamped entries
- Error details

## Example Log Entry

```json
{
  "interaction_id": 1,
  "timestamp": "2025-11-05T16:36:54.071912",
  "type": "request",
  "agent": "Research Coordinator",
  "data": {
    "model": "MiniMax-M2",
    "messages": [
      {
        "role": "user",
        "content": "Analyze the concept of 'Artificial General Intelligence (AGI)'..."
      }
    ],
    "max_tokens": 4096,
    "temperature": 0.7,
    "system": "You are a Research Coordinator Agent..."
  }
}
```

## Viewing Logs

### Real-time Console Output

When running the system, you'll see:
- Request panels in cyan
- Response panels in green  
- Error panels in red
- Agent status updates
- Summary table at the end

### Log Files

```bash
# View latest log
ls -lt logs/ | head -1

# Read log file
cat logs/llm_interactions_YYYYMMDD_HHMMSS.log

# Search for specific agent
grep "Research Coordinator" logs/*.log

# Count interactions
grep "interaction_id" logs/*.log | wc -l
```

## Multi-Agent Workflow Logging

The system logs 6 phases:

1. **Phase 1 - Coordination**: Research Coordinator breaks down task
2. **Phase 2 - Research**: Researcher gathers comprehensive information
3. **Phase 3 - Analysis**: Data Analyst extracts insights
4. **Phase 4 - Writing**: Writer creates initial draft
5. **Phase 5 - Critique**: Critic reviews and suggests improvements
6. **Phase 6 - Synthesis**: Synthesizer produces final output

Each phase generates its own logged interactions.

## Log Analysis Examples

### Count total tokens used:
```bash
grep -o '"input_tokens": [0-9]*' logs/*.log | \
  awk -F': ' '{sum += $2} END {print "Total input tokens:", sum}'

grep -o '"output_tokens": [0-9]*' logs/*.log | \
  awk -F': ' '{sum += $2} END {print "Total output tokens:", sum}'
```

### View agent activity:
```bash
grep '"agent":' logs/*.log | sort | uniq -c
```

### Extract thinking blocks:
```bash
grep -o '"thinking": "[^"]*"' logs/*.log
```

## Performance Metrics

From our test run:

- **Total Interactions**: 6 (one per agent)
- **Total Output**: ~84,097 characters across all phases
- **Phases Completed**: 6/6 (100%)
- **Success Rate**: 100%

| Phase | Agent | Output Size |
|-------|-------|-------------|
| Planning | Research Coordinator | 4,932 chars |
| Research | Researcher | 22,325 chars |
| Analysis | Data Analyst | 8,789 chars |
| Writing | Writer | 18,377 chars |
| Critique | Critic | 7,233 chars |
| Synthesis | Synthesizer | 22,441 chars |

## Debugging with Logs

The comprehensive logging enables:

1. **Request Debugging**: See exact prompts sent to LLM
2. **Response Analysis**: Analyze LLM outputs for quality
3. **Performance Tuning**: Measure token usage and optimize
4. **Error Investigation**: Full error context with stack traces
5. **Workflow Verification**: Confirm all agents executed correctly

## Environment Variables Used

The system logs which environment variables were active:

- `_ANTHROPIC_API_KEY`: API authentication (partially masked in logs)
- `_ANTHROPIC_BASE_URL`: Custom API endpoint
- `_MODEL_NAME`: LLM model selection

All logged in the initial system setup phase.
