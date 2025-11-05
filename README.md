# Multi-Agent System

This project implements a multi-agent system for research tasks.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install openai
    ```

2.  **Set environment variables:**
    Create a `.env` file in the project root and add the following:
    ```
    _OPENAI_BASE_URL="your_openai_base_url"
    _OPENAI_API_KEY="your_openai_api_key"
    _MODEL_NAME="your_model_name"
    ```

## Running the System

To run the multi-agent system, execute the following command from the project root:
```bash
python -m multi_agent_system.main
```
