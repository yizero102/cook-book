# AI-Powered Code Assistant

An intelligent code review and improvement assistant powered by Anthropic's LLM API.

## Features

- **Code Analysis**: Analyzes code quality, identifies potential bugs, and suggests improvements
- **Documentation Generation**: Automatically generates comprehensive documentation for your code
- **Code Improvements**: Provides refactored versions with explanations
- **Creative AI**: Demonstrates creative capabilities with poetry and more

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export _ANTHROPIC_API_KEY="your-api-key"
export _ANTHROPIC_BASE_URL="https://api.minimax.io/anthropic"  # Optional: custom base URL
export _MODEL_NAME="MiniMax-M2"  # Optional: defaults to claude-3-5-sonnet-20241022
```

3. Run the assistant:
```bash
python ai_assistant.py
```

## Usage

The main script demonstrates all capabilities by analyzing a sample Fibonacci function. You can modify the `ai_assistant.py` file to analyze your own code.

## Example Output

The assistant provides:
- Detailed code analysis with quality ratings
- Comprehensive documentation with examples
- Refactored code with improvement explanations
- Creative demonstrations of AI capabilities

## Requirements

- Python 3.7+
- anthropic SDK
- rich (for beautiful terminal output)
