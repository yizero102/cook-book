#!/bin/bash
# Final System Check Script

echo "════════════════════════════════════════════════════════════════════"
echo "  AI AGENT SELF-REPLICA SYSTEM - FINAL CHECK"
echo "════════════════════════════════════════════════════════════════════"
echo ""

# Count files
echo "📁 Files Created:"
echo "   Python Scripts: $(ls -1 *.py 2>/dev/null | wc -l)"
echo "   Documentation: $(ls -1 *.md 2>/dev/null | wc -l)"
echo "   Configuration: $(ls -1 *.txt .gitignore 2>/dev/null | wc -l)"
echo "   Total: $(ls -1 *.py *.md *.txt .gitignore 2>/dev/null | wc -l) files"
echo ""

# Check Python validity
echo "🔍 Python Scripts Validation:"
if python -m py_compile *.py 2>&1 | grep -q "SyntaxError"; then
    echo "   ❌ Syntax errors found"
else
    echo "   ✅ All scripts valid"
fi
echo ""

# Quick agent check
echo "🤖 Agent Status:"
python -c "
from ai_agent_replica import AIAgentReplica
agent = AIAgentReplica()
caps = agent.verify_capabilities()
all_working = all(caps.values())
print(f'   Status: {\"✅ ALL OPERATIONAL\" if all_working else \"❌ SOME ISSUES\"}')
print(f'   Capabilities: {len([c for c in caps.values() if c])}/{len(caps)} working')
" 2>/dev/null
echo ""

echo "════════════════════════════════════════════════════════════════════"
echo "  SYSTEM CHECK COMPLETE"
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "For complete validation, run: python run_all_validations.py"
echo ""
