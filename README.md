# 🤖 Advanced Multi-Agent AI System

A comprehensive demonstration of advanced AI capabilities using Anthropic's LLM API, showcasing multiple specialized AI agents working together to solve complex problems.

## 🌟 Features

### Multi-Agent System (`ai_agent_system.py`)

Four specialized AI agents that demonstrate different capabilities:

1. **CodeAnalyzer Agent** - Analyzes code quality, identifies issues, suggests improvements, and provides refactored versions
2. **CreativeWriter Agent** - Generates compelling stories, poems, and creative content in various styles
3. **ProblemSolver Agent** - Solves complex mathematical problems, logic puzzles, and strategic challenges
4. **CodeGenerator Agent** - Generates complete, production-ready applications from descriptions

### Advanced Challenges (`advanced_demos.py`)

Demonstrates AI solving genuinely difficult computational problems:

1. **Algorithm Design** - Optimal meeting room scheduler with conflicts and priorities
2. **Code Optimization** - Extreme performance optimization with complexity analysis
3. **System Architecture** - Design of distributed, fault-tolerant real-time analytics platform
4. **Creative Technical** - Procedural music generation using mathematical concepts
5. **Mathematical Proofs** - Rigorous proof construction with verification code

## 🚀 Setup

### Prerequisites

- Python 3.8+
- Environment variables set:
  - `_ANTHROPIC_API_KEY` - Your Anthropic API key
  - `_ANTHROPIC_BASE_URL` - The API base URL
  - `_MODEL_NAME` - The model to use (e.g., MiniMax-M2)

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

### Run the Multi-Agent System

```bash
python ai_agent_system.py
```

This will demonstrate all four agents with example tasks:
- Code analysis and refactoring
- Creative story writing
- Poetry generation
- Mathematical problem solving
- Logic puzzle solving
- Complete application generation

### Run Advanced Challenges

```bash
python advanced_demos.py
```

This will run five challenging computational problems that showcase the AI's ability to:
- Design complex algorithms
- Optimize code performance
- Architect distributed systems
- Create creative technical solutions
- Construct mathematical proofs

## 📊 Output

Both scripts provide beautifully formatted output using the Rich library, including:
- Colored panels for different agents
- Progress indicators
- Formatted code blocks
- Tables showing agent capabilities

Generated code and artifacts are saved to the project directory:
- `generated_task_manager.py` - Task management application
- `generated_music_generator.py` - Procedural music generator (if applicable)

## 🎯 Key Capabilities Demonstrated

- **Code Understanding** - Deep analysis of code quality and architecture
- **Problem Solving** - Complex mathematical and logical reasoning
- **Creative Generation** - Original creative writing in multiple styles
- **Code Generation** - Production-ready application generation
- **System Design** - Enterprise-level architectural planning
- **Optimization** - Performance analysis and improvement
- **Rigorous Reasoning** - Mathematical proofs and verification

## 🔧 Architecture

The system uses:
- **Anthropic API** - For LLM inference
- **Rich library** - For beautiful terminal UI
- **Async/await** - For efficient operation orchestration
- **Modular design** - Each agent is independently extensible

## 📝 Example Use Cases

1. **Code Review Automation** - Use CodeAnalyzer to review pull requests
2. **Content Generation** - Use CreativeWriter for marketing, documentation, or creative projects
3. **Educational Tool** - Use ProblemSolver to teach complex concepts with step-by-step solutions
4. **Rapid Prototyping** - Use CodeGenerator to quickly scaffold applications
5. **Architecture Planning** - Use advanced challenges for system design validation

## 🧪 Testing

The code is self-verifying - when you run the scripts, they demonstrate all capabilities with concrete examples that you can inspect and verify.

## 🎨 Customization

Each agent can be customized by:
- Modifying the system prompt
- Adjusting max_tokens for longer/shorter responses
- Adding new specialized methods
- Creating new agent types

Example:
```python
custom_agent = AIAgent(
    name="SecurityAuditor",
    role="Security Analysis Expert",
    system_prompt="You are a security expert..."
)
```

## 🤝 Contributing

This is a demonstration project showcasing AI capabilities. Feel free to:
- Add new agents with specialized capabilities
- Create new challenge scenarios
- Improve the UI and formatting
- Add persistence and state management

## 📄 License

MIT License - Feel free to use and modify as needed.

## 🙏 Acknowledgments

Built with:
- Anthropic Claude API
- Rich library for beautiful CLI output
- Python asyncio for orchestration
