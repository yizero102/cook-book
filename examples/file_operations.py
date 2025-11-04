#!/usr/bin/env python3
"""
File Operations Examples for AI Assistant Replica

This script demonstrates various file operation patterns.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assistant_replica import Assistant


def example_create_python_module(assistant):
    """Example: Create a complete Python module."""
    print("=" * 70)
    print("Example: Create Python Module")
    print("=" * 70)
    
    module_content = '''#!/usr/bin/env python3
"""
Example module created by AI Assistant.

This module demonstrates proper Python module structure.
"""

def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"


def farewell(name: str) -> str:
    """Say goodbye to someone."""
    return f"Goodbye, {name}!"


def main():
    """Main entry point."""
    print(greet("World"))
    print(farewell("World"))


if __name__ == "__main__":
    main()
'''
    
    result = assistant.use_tool(
        "WriteFile",
        filePath="/home/engine/project/example_module.py",
        content=module_content
    )
    
    if result["success"]:
        print(f"✅ Module created: {result['path']}")
        print("   Structure: shebang, docstring, functions, main")
    else:
        print(f"❌ Error: {result['error']}")
    print()


def example_edit_function(assistant):
    """Example: Edit a function in the module."""
    print("=" * 70)
    print("Example: Edit Function in Module")
    print("=" * 70)
    
    result = assistant.use_tool(
        "EditFile",
        filePath="/home/engine/project/example_module.py",
        oldString='def greet(name: str) -> str:\n    """Greet someone by name."""\n    return f"Hello, {name}!"',
        newString='def greet(name: str, formal: bool = False) -> str:\n    """Greet someone by name.\n    \n    Args:\n        name: Person\'s name\n        formal: Use formal greeting\n    """\n    if formal:\n        return f"Good day, {name}!"\n    return f"Hello, {name}!"'
    )
    
    if result["success"]:
        print("✅ Function edited successfully!")
        print("   Changes: Added 'formal' parameter with documentation")
    else:
        print(f"❌ Error: {result['error']}")
    print()


def example_read_specific_lines(assistant):
    """Example: Read specific lines from a file."""
    print("=" * 70)
    print("Example: Read Specific Lines")
    print("=" * 70)
    
    # First, check total lines
    result1 = assistant.use_tool(
        "ReadFile",
        filePath="/home/engine/project/example_module.py"
    )
    
    if result1["success"]:
        total_lines = len(result1["content"].split('\n'))
        print(f"✅ Total lines in file: {total_lines}")
        
        # Read lines 5-10
        result2 = assistant.use_tool(
            "ReadFile",
            filePath="/home/engine/project/example_module.py",
            offset=5,
            limit=5
        )
        
        if result2["success"]:
            print(f"✅ Lines 6-10:")
            print(result2["content"])
    else:
        print(f"❌ Error: {result1['error']}")
    print()


def example_create_config_file(assistant):
    """Example: Create a configuration file."""
    print("=" * 70)
    print("Example: Create Configuration File")
    print("=" * 70)
    
    config_content = '''{
    "app_name": "AI Assistant Example",
    "version": "1.0.0",
    "settings": {
        "debug": true,
        "log_level": "INFO",
        "max_retries": 3
    },
    "features": [
        "file_operations",
        "code_generation",
        "code_analysis"
    ]
}
'''
    
    result = assistant.use_tool(
        "WriteFile",
        filePath="/home/engine/project/config.json",
        content=config_content
    )
    
    if result["success"]:
        print(f"✅ Config file created: {result['path']}")
    else:
        print(f"❌ Error: {result['error']}")
    print()


def example_backup_and_restore(assistant):
    """Example: Backup a file before editing."""
    print("=" * 70)
    print("Example: Backup and Restore Pattern")
    print("=" * 70)
    
    original_file = "/home/engine/project/example_module.py"
    backup_file = "/home/engine/project/example_module.py.backup"
    
    # 1. Read original
    result1 = assistant.use_tool("ReadFile", filePath=original_file)
    
    if not result1["success"]:
        print(f"❌ Error reading original: {result1['error']}")
        return
    
    # 2. Create backup
    result2 = assistant.use_tool(
        "WriteFile",
        filePath=backup_file,
        content=result1["content"]
    )
    
    if result2["success"]:
        print(f"✅ Backup created: {backup_file}")
    else:
        print(f"❌ Error creating backup: {result2['error']}")
        return
    
    # 3. Make edit to original
    result3 = assistant.use_tool(
        "EditFile",
        filePath=original_file,
        oldString="Example module created by AI Assistant.",
        newString="Example module created by AI Assistant (MODIFIED)."
    )
    
    if result3["success"]:
        print("✅ Original file modified")
    else:
        print(f"❌ Error modifying file: {result3['error']}")
    
    # 4. Verify backup exists
    result4 = assistant.use_tool("ReadFile", filePath=backup_file)
    
    if result4["success"]:
        print("✅ Backup verified and intact")
    else:
        print(f"❌ Error verifying backup: {result4['error']}")
    
    print()


def example_multi_file_search(assistant):
    """Example: Search across multiple files."""
    print("=" * 70)
    print("Example: Multi-File Search")
    print("=" * 70)
    
    # 1. Find all Python files
    result1 = assistant.use_tool(
        "GlobTool",
        pattern="**/*.py",
        path="/home/engine/project"
    )
    
    if result1["success"]:
        print(f"✅ Found {result1['count']} Python files")
        
        # 2. Search for 'def ' in those files
        result2 = assistant.use_tool(
            "GrepTool",
            pattern="def ",
            path="/home/engine/project"
        )
        
        if result2["success"]:
            print(f"✅ Found {result2['count']} function definitions")
            if result2['matches']:
                print("   Sample matches:")
                for match in result2['matches'][:3]:
                    print(f"   - {match}")
        else:
            print(f"❌ Search error: {result2['error']}")
    else:
        print(f"❌ Error finding files: {result1['error']}")
    
    print()


def example_create_test_file(assistant):
    """Example: Create a test file for the module."""
    print("=" * 70)
    print("Example: Create Test File")
    print("=" * 70)
    
    test_content = '''#!/usr/bin/env python3
"""
Tests for example_module.py
"""

import unittest
from example_module import greet, farewell


class TestGreetings(unittest.TestCase):
    """Test greeting functions."""
    
    def test_greet_informal(self):
        """Test informal greeting."""
        result = greet("Alice")
        self.assertEqual(result, "Hello, Alice!")
    
    def test_greet_formal(self):
        """Test formal greeting."""
        result = greet("Alice", formal=True)
        self.assertEqual(result, "Good day, Alice!")
    
    def test_farewell(self):
        """Test farewell."""
        result = farewell("Bob")
        self.assertEqual(result, "Goodbye, Bob!")


if __name__ == "__main__":
    unittest.main()
'''
    
    result = assistant.use_tool(
        "WriteFile",
        filePath="/home/engine/project/test_example_module.py",
        content=test_content
    )
    
    if result["success"]:
        print(f"✅ Test file created: {result['path']}")
    else:
        print(f"❌ Error: {result['error']}")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("  FILE OPERATIONS EXAMPLES")
    print("=" * 70)
    print()
    
    try:
        assistant = Assistant()
        print(f"✅ Assistant initialized\n")
        
        example_create_python_module(assistant)
        example_edit_function(assistant)
        example_read_specific_lines(assistant)
        example_create_config_file(assistant)
        example_backup_and_restore(assistant)
        example_multi_file_search(assistant)
        example_create_test_file(assistant)
        
        print("=" * 70)
        print("✅ All file operation examples completed!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
