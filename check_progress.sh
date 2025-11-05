#!/bin/bash

echo "Checking demo progress..."
echo ""

# Check if demo.py is running
if ps aux | grep -q "[p]ython demo.py"; then
    echo "✓ Demo is currently running"
else
    echo "✗ Demo is not running"
fi

# Check log directory
if [ -d "llm_logs" ]; then
    LOG_COUNT=$(find llm_logs -name "*.json" -type f | wc -l)
    echo "✓ Found $LOG_COUNT log files in llm_logs/"
fi

# Check output file
if [ -f "demo_output.txt" ]; then
    SIZE=$(wc -l < demo_output.txt 2>/dev/null || echo "0")
    echo "✓ demo_output.txt has $SIZE lines"
    if [ "$SIZE" -gt 0 ]; then
        echo ""
        echo "Last 20 lines of output:"
        tail -20 demo_output.txt
    fi
fi

# Check for results
if [ -f "demo_results.json" ]; then
    echo "✓ demo_results.json created"
fi
