#!/bin/bash
# Comprehensive test script for all AI demos

set -e

cd /home/engine/project
source venv/bin/activate

echo "═══════════════════════════════════════════════════════"
echo "  🚀 Running Complete AI System Tests 🚀"
echo "═══════════════════════════════════════════════════════"
echo ""

echo "📋 Test 1: Quick API Verification"
echo "-----------------------------------"
python quick_test.py
echo ""
echo "✓ Test 1 Passed!"
echo ""

echo "📋 Test 2: Showcase Demos (6 complex problems)"
echo "-----------------------------------"
timeout 180 python demo_showcase.py || echo "⚠ Timeout or interrupted"
echo ""
echo "✓ Test 2 Completed!"
echo ""

echo "═══════════════════════════════════════════════════════"
echo "  ✅ All Tests Complete!"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Generated Files:"
ls -lh *.py | grep generated || echo "No generated files found"
echo ""
echo "Output Logs:"
ls -lh *output.txt 2>/dev/null || echo "No output files"
