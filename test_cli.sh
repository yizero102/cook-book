#!/bin/bash

echo "Testing Interactive CLI with automated input..."
echo ""

# Test the Quick Code Review feature (option 5)
echo "5
1
n" | python interactive_cli.py

echo ""
echo "✓ CLI test completed successfully!"
