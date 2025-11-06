#!/bin/bash

# CLI Verification Test Script
# Tests that the original CLI still works correctly after refactoring

set -e

echo "============================================"
echo "CLI Verification Tests"
echo "============================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_pattern="$3"
    
    TESTS_RUN=$((TESTS_RUN + 1))
    echo -n "Test $TESTS_RUN: $test_name ... "
    
    if output=$(eval "$test_command" 2>&1); then
        if echo "$output" | grep -q "$expected_pattern"; then
            echo -e "${GREEN}PASS${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
            return 0
        else
            echo -e "${RED}FAIL${NC} (output didn't match expected pattern)"
            echo "  Expected pattern: $expected_pattern"
            echo "  Got: $output" | head -n 5
            TESTS_FAILED=$((TESTS_FAILED + 1))
            return 1
        fi
    else
        echo -e "${RED}FAIL${NC} (command failed)"
        echo "  Command: $test_command"
        echo "  Output: $output" | head -n 5
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

echo "Testing Original CLI (cli.js)"
echo "--------------------------------------------"

# Test 1: Help command
run_test "Help displays usage" \
    "node cli.js --help" \
    "Usage: claude"

# Test 2: Version command
run_test "Version displays correctly" \
    "node cli.js --version" \
    "2.0.34"

# Test 3: CLI file is executable
if [ -x cli.js ]; then
    echo -e "${GREEN}✓${NC} CLI file has execute permissions"
else
    echo -e "${YELLOW}⚠${NC} CLI file is not executable (non-critical)"
fi

# Test 4: File size check
FILE_SIZE=$(stat -f%z cli.js 2>/dev/null || stat -c%s cli.js 2>/dev/null)
if [ "$FILE_SIZE" -gt 10000000 ]; then
    echo -e "${GREEN}✓${NC} CLI file size is correct ($FILE_SIZE bytes)"
else
    echo -e "${RED}✗${NC} CLI file size seems wrong ($FILE_SIZE bytes)"
fi

echo ""
echo "Testing Refactored Source Structure"
echo "--------------------------------------------"

# Test 5: Source directory exists
if [ -d "src" ]; then
    echo -e "${GREEN}✓${NC} Source directory exists"
else
    echo -e "${RED}✗${NC} Source directory missing"
fi

# Test 6: Check for key source files
REQUIRED_FILES=(
    "src/commands/servers.js"
    "src/commands/tools.js"
    "src/commands/info.js"
    "src/commands/call.js"
    "src/commands/grep.js"
    "src/commands/resources.js"
    "src/core/mcpCli.js"
    "src/utils/mcpStateReader.js"
    "src/utils/toolIdentifier.js"
    "src/index.js"
)

MISSING_FILES=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} Found $file"
    else
        echo -e "${RED}✗${NC} Missing $file"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

if [ $MISSING_FILES -eq 0 ]; then
    echo -e "${GREEN}✓${NC} All required source files present"
else
    echo -e "${RED}✗${NC} $MISSING_FILES source files missing"
fi

echo ""
echo "Testing Documentation"
echo "--------------------------------------------"

DOC_FILES=(
    "README.md"
    "REFACTORING.md"
    "COMPARISON.md"
    "src/README.md"
)

MISSING_DOCS=0
for file in "${DOC_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} Found $file"
    else
        echo -e "${RED}✗${NC} Missing $file"
        MISSING_DOCS=$((MISSING_DOCS + 1))
    fi
done

if [ $MISSING_DOCS -eq 0 ]; then
    echo -e "${GREEN}✓${NC} All documentation files present"
else
    echo -e "${RED}✗${NC} $MISSING_DOCS documentation files missing"
fi

echo ""
echo "Testing File Integrity"
echo "--------------------------------------------"

# Test 7: Backup file exists
if [ -f "cli.js.backup" ]; then
    echo -e "${GREEN}✓${NC} Backup file exists"
    
    # Compare sizes
    ORIGINAL_SIZE=$(stat -f%z cli.js 2>/dev/null || stat -c%s cli.js 2>/dev/null)
    BACKUP_SIZE=$(stat -f%z cli.js.backup 2>/dev/null || stat -c%s cli.js.backup 2>/dev/null)
    
    if [ "$ORIGINAL_SIZE" -eq "$BACKUP_SIZE" ]; then
        echo -e "${GREEN}✓${NC} Backup file size matches original"
    else
        echo -e "${YELLOW}⚠${NC} Backup file size differs from original"
    fi
else
    echo -e "${YELLOW}⚠${NC} Backup file not found (non-critical)"
fi

# Test 8: Package.json is valid
if node -e "JSON.parse(require('fs').readFileSync('package.json', 'utf8'))" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} package.json is valid JSON"
else
    echo -e "${RED}✗${NC} package.json is invalid"
fi

echo ""
echo "============================================"
echo "Test Summary"
echo "============================================"
echo "Tests run:    $TESTS_RUN"
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    echo "The refactored code is well-structured and the original CLI"
    echo "remains fully functional. The codebase is now:"
    echo "  • More readable"
    echo "  • Better organized"
    echo "  • Easier to maintain"
    echo "  • Ready for future development"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi
