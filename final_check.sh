#!/bin/bash
echo "═══════════════════════════════════════════════════════════════"
echo "           FINAL PROJECT VERIFICATION"
echo "═══════════════════════════════════════════════════════════════"
echo ""

echo "1. Checking Python files..."
python_files=("llm_logger.py" "llm_client.py" "agents.py" "multi_agent_system.py" "main.py" "quick_test.py" "verify_system.py" "examples.py")
for file in "${python_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file MISSING"
    fi
done

echo ""
echo "2. Checking documentation files..."
doc_files=("README.md" "LOGGING_DEMO.md" "VERIFICATION_REPORT.md" "SYSTEM_SUMMARY.txt" "FINAL_STATUS.md")
for file in "${doc_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file MISSING"
    fi
done

echo ""
echo "3. Checking configuration files..."
if [ -f "requirements.txt" ]; then
    echo "   ✓ requirements.txt"
else
    echo "   ✗ requirements.txt MISSING"
fi

if [ -f ".gitignore" ]; then
    echo "   ✓ .gitignore"
else
    echo "   ✗ .gitignore MISSING"
fi

echo ""
echo "4. Checking environment variables..."
if [ -n "$_ANTHROPIC_API_KEY" ]; then
    echo "   ✓ _ANTHROPIC_API_KEY is set"
else
    echo "   ✗ _ANTHROPIC_API_KEY not set"
fi

if [ -n "$_ANTHROPIC_BASE_URL" ]; then
    echo "   ✓ _ANTHROPIC_BASE_URL is set ($ANTHROPIC_BASE_URL)"
else
    echo "   ✗ _ANTHROPIC_BASE_URL not set"
fi

if [ -n "$_MODEL_NAME" ]; then
    echo "   ✓ _MODEL_NAME is set ($_MODEL_NAME)"
else
    echo "   ✗ _MODEL_NAME not set"
fi

echo ""
echo "5. Checking logs directory..."
if [ -d "logs" ]; then
    log_count=$(ls -1 logs/*.log 2>/dev/null | wc -l)
    echo "   ✓ logs/ directory exists with $log_count log files"
else
    echo "   ⚠ logs/ directory will be created on first run"
fi

echo ""
echo "6. Checking test outputs..."
if [ -f "full_run.log" ]; then
    lines=$(wc -l < full_run.log)
    echo "   ✓ full_run.log exists ($lines lines)"
else
    echo "   ⚠ full_run.log not yet generated"
fi

if [ -f "quick_test_output.log" ]; then
    lines=$(wc -l < quick_test_output.log)
    echo "   ✓ quick_test_output.log exists ($lines lines)"
else
    echo "   ⚠ quick_test_output.log not yet generated"
fi

echo ""
echo "7. Python syntax check..."
for file in "${python_files[@]}"; do
    if python -m py_compile "$file" 2>/dev/null; then
        echo "   ✓ $file syntax OK"
    else
        echo "   ✗ $file syntax ERROR"
    fi
done

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "           VERIFICATION COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
