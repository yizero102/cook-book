#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║       AI Code Assistant - Full Test Suite                 ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Activate virtual environment
source venv/bin/activate

echo "✓ Virtual environment activated"
echo ""

# Test 1: Main AI Assistant
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 1: Running main AI assistant demo..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python ai_assistant.py
TEST1_EXIT=$?

echo ""
echo ""

# Test 2: Additional Examples
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 2: Running additional examples..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python test_examples.py
TEST2_EXIT=$?

echo ""
echo ""

# Test 3: Interactive CLI (automated)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test 3: Running interactive CLI test..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5
1
n" | python interactive_cli.py
TEST3_EXIT=$?

echo ""
echo ""

# Summary
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                  Test Results Summary                      ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

if [ $TEST1_EXIT -eq 0 ]; then
    echo "✓ Test 1: Main AI Assistant - PASSED"
else
    echo "✗ Test 1: Main AI Assistant - FAILED (exit code: $TEST1_EXIT)"
fi

if [ $TEST2_EXIT -eq 0 ]; then
    echo "✓ Test 2: Additional Examples - PASSED"
else
    echo "✗ Test 2: Additional Examples - FAILED (exit code: $TEST2_EXIT)"
fi

if [ $TEST3_EXIT -eq 0 ]; then
    echo "✓ Test 3: Interactive CLI - PASSED"
else
    echo "✗ Test 3: Interactive CLI - FAILED (exit code: $TEST3_EXIT)"
fi

echo ""

# Overall result
if [ $TEST1_EXIT -eq 0 ] && [ $TEST2_EXIT -eq 0 ] && [ $TEST3_EXIT -eq 0 ]; then
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║          🎉 ALL TESTS PASSED SUCCESSFULLY! 🎉             ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    exit 0
else
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║          ⚠️  SOME TESTS FAILED ⚠️                          ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    exit 1
fi
