# Multi-Agent System with LLM Request/Response Logging

A sophisticated multi-agent system that uses multiple specialized AI agents to collaboratively solve complex problems. All LLM interactions are comprehensively logged with reasoning details.

## System Architecture

### Components

1. **LLM Logger** (`llm_logger.py`)
   - Logs all LLM requests and responses
   - Captures reasoning details when available
   - Stores individual logs and session summaries
   - Tracks token usage and metadata

2. **LLM Client** (`llm_client.py`)
   - Wrapper around OpenAI client
   - Automatic logging integration
   - Supports reasoning_split for detailed thinking logs

3. **Base Agent** (`base_agent.py`)
   - Foundation class for all agents
   - Memory management
   - Standardized thinking interface

4. **Specialized Agents** (`agents.py`)
   - **ResearchAgent**: Information gathering and synthesis
   - **AnalystAgent**: Data analysis and pattern recognition
   - **ProblemSolverAgent**: Solution design and implementation planning
   - **CriticAgent**: Quality assurance and evaluation
   - **SynthesizerAgent**: Information synthesis and reporting
   - **CoordinatorAgent**: System orchestration and planning

5. **Multi-Agent System** (`multi_agent_system.py`)
   - Orchestrates agent collaboration
   - Manages workflow between agents
   - Tracks execution history

## Features

- **Comprehensive Logging**: Every LLM request and response is logged with:
  - Timestamps
  - Agent information
  - Request messages
  - Response content
  - Reasoning details
  - Token usage
  - Metadata

- **Multi-Agent Collaboration**: Agents work together through phases:
  1. Planning (Coordinator)
  2. Research (Researcher)
  3. Analysis (Analyst)
  4. Solution Design (Problem Solver)
  5. Critical Evaluation (Critic)
  6. Refinement (Problem Solver)
  7. Final Synthesis (Synthesizer)

- **Complex Problem Solving**: Demonstrates solving hard problems:
  - Climate change adaptation strategies
  - AI ethics frameworks
  - Global supply chain optimization

## Usage

### Installation

```bash
pip install -r requirements.txt
```

### Environment Setup

Set the following environment variables:
- `_OPENAI_BASE_URL`: Your LLM API base URL
- `_OPENAI_API_KEY`: Your API key
- `_MODEL_NAME`: Model name to use

### Running the System

```bash
python main.py
```

This will:
1. Initialize the multi-agent system
2. Solve three complex problems
3. Generate detailed logs for all LLM interactions
4. Save results and execution summaries

### Output

- **llm_logs/**: Directory containing all LLM interaction logs
  - Individual request logs: `{session_id}_request_{id}.json`
  - Session summary: `{session_id}_summary.jsonl`
  - Error logs (if any): `{session_id}_error_{id}.json`

- **problem_{n}_results.json**: Individual problem results
- **all_results.json**: Comprehensive results for all problems

## Log Format

### Individual Request Log
```json
{
  "request_id": 1,
  "timestamp": "2024-01-01T12:00:00",
  "agent_name": "ResearchAgent",
  "request": {
    "messages": [...],
    "model": "MiniMax-M2"
  },
  "response": {
    "content": "...",
    "reasoning": "...",
    "finish_reason": "stop",
    "usage": {
      "prompt_tokens": 100,
      "completion_tokens": 200,
      "total_tokens": 300
    }
  },
  "metadata": {...}
}
```

### Session Summary (JSONL)
Each line contains a summary of one request:
```json
{"request_id": 1, "timestamp": "...", "agent_name": "...", "user_message": "...", "response_preview": "...", "has_reasoning": true, "tokens": 300}
```

## Agent Descriptions

### CoordinatorAgent
Plans and orchestrates the problem-solving workflow. Decides which agents to involve and in what order.

### ResearchAgent
Conducts thorough research on topics, gathering and organizing relevant information.

### AnalystAgent
Analyzes data and information, identifying patterns, trends, and insights.

### ProblemSolverAgent
Designs solutions to problems, creating implementation plans and strategies.

### CriticAgent
Evaluates solutions critically, identifying weaknesses and suggesting improvements.

### SynthesizerAgent
Combines inputs from multiple agents into coherent, comprehensive reports.

## Extension

To add new agents:

1. Create a new class inheriting from `BaseAgent`
2. Define the agent's role and system prompt
3. Add it to the `MultiAgentSystem`
4. Update the workflow as needed

## License

This project demonstrates a multi-agent system with comprehensive LLM logging capabilities.
