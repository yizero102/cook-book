#!/bin/bash

# Comprehensive test runner for the multi-agent system

echo "=========================================="
echo "  Multi-Agent System - Test Suite"
echo "=========================================="
echo ""

# Activate virtual environment
source venv/bin/activate

echo "1. Environment Check"
echo "--------------------"
echo "Base URL: $_OPENAI_BASE_URL"
echo "Model: $_MODEL_NAME"
echo "API Key: ${_OPENAI_API_KEY:0:10}..."
echo ""

echo "2. Running Basic Test"
echo "--------------------"
python test_basic.py
echo ""

echo "3. Running Final Verification"
echo "-----------------------------"
python final_verification.py
echo ""

echo "4. Log File Summary"
echo "-------------------"
REQUEST_LOGS=$(find llm_logs -name "*_request_*.json" | wc -l)
SUMMARY_LOGS=$(find llm_logs -name "*_summary.jsonl" | wc -l)
echo "Total request logs: $REQUEST_LOGS"
echo "Total summary logs: $SUMMARY_LOGS"
echo ""

echo "5. Sample Log Inspection"
echo "------------------------"
LATEST_LOG=$(ls -t llm_logs/*_request_*.json | head -1)
echo "Latest log: $(basename $LATEST_LOG)"
echo "Agent: $(cat $LATEST_LOG | python -c "import sys, json; print(json.load(sys.stdin)['agent_name'])")"
echo "Has reasoning: $(cat $LATEST_LOG | python -c "import sys, json; print(bool(json.load(sys.stdin)['response']['reasoning']))")"
echo ""

echo "=========================================="
echo "  All Tests Complete!"
echo "=========================================="
