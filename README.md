# Multi-Agent AI Research System

A sophisticated multi-agent system that uses specialized AI agents to collaboratively solve complex research tasks.

## 🌟 Features

- **6 Specialized AI Agents**: Each with unique roles and expertise
- **Complete Request/Response Logging**: All LLM interactions are logged with rich formatting
- **Multi-Phase Workflow**: Structured approach to complex problem-solving
- **Rich Console Output**: Beautiful terminal UI with progress indicators
- **Error Handling**: Robust error handling and recovery

## 🤖 Agent Roles

1. **Research Coordinator**: Breaks down complex tasks and creates execution plans
2. **Researcher**: Conducts deep research and gathers comprehensive information
3. **Data Analyst**: Analyzes information and extracts key insights
4. **Writer**: Transforms research into clear, compelling content
5. **Critic**: Provides critical review and identifies improvements
6. **Synthesizer**: Combines all outputs into polished final deliverable

## 🔄 Workflow

```
Task Input
    ↓
[Coordinator] → Creates structured plan
    ↓
[Researcher] → Conducts deep research
    ↓
[Analyst] → Analyzes and extracts insights
    ↓
[Writer] → Creates initial draft
    ↓
[Critic] → Provides critical feedback
    ↓
[Synthesizer] → Produces final output
    ↓
Final Result
```

## 📋 Requirements

- Python 3.8+
- Anthropic API access
- Environment variables:
  - `_ANTHROPIC_API_KEY`: Your API key
  - `_ANTHROPIC_BASE_URL`: API endpoint (optional)
  - `_MODEL_NAME`: Model to use (optional)

## 🚀 Installation

```bash
pip install -r requirements.txt
```

## 💻 Usage

```bash
python main.py
```

The system will:
1. Initialize all 6 agents
2. Process a complex research task about AGI
3. Display rich console output with progress
4. Log all LLM requests/responses to `logs/` directory
5. Output final synthesized result

## 📊 Logging

All LLM interactions are logged to:
- Console: Rich formatted output with color and panels
- File: `logs/llm_interactions_YYYYMMDD_HHMMSS.log`

Logs include:
- Request timestamp and agent name
- Full prompt and system messages
- Response content and metadata
- Token usage statistics
- Error information (if any)

## 🎯 Example Task

The system tackles complex questions like AGI analysis from multiple perspectives:
- Technical challenges
- Philosophical implications
- Societal impact
- Timeline predictions
- Ethical considerations

## 🏗️ Architecture

```
main.py                 # Entry point
multi_agent_system.py   # Orchestrates agent workflow
agents.py               # Agent definitions and roles
llm_client.py          # LLM API client with logging
llm_logger.py          # Comprehensive logging system
```

## 🔧 Customization

To add new agents or modify behavior:

1. Create new agent class in `agents.py`
2. Add to `MultiAgentSystem` initialization
3. Integrate into workflow in `multi_agent_system.py`

## 📝 License

MIT License
