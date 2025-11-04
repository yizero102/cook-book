#!/usr/bin/env python3
"""
Basic Usage Examples for AI Assistant Replica

This script demonstrates basic usage patterns for the assistant.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assistant_replica import Assistant


def example_1_initialization():
    """Example 1: Initialize the assistant."""
    print("=" * 70)
    print("Example 1: Initializing the Assistant")
    print("=" * 70)
    
    assistant = Assistant()
    print(f"✅ Assistant initialized!")
    print(f"   Model: {assistant.model_name}")
    print(f"   Available tools: {len(assistant.tools)}")
    print(f"   Tools: {', '.join(assistant.tools.keys())}")
    print()
    
    return assistant


def example_2_simple_question(assistant):
    """Example 2: Ask a simple question."""
    print("=" * 70)
    print("Example 2: Simple Question")
    print("=" * 70)
    
    question = "What is the capital of France? Answer in one word."
    print(f"Question: {question}")
    
    response = assistant.execute_simple_task(question)
    print(f"Response: {response}")
    print()


def example_3_create_file(assistant):
    """Example 3: Create a file."""
    print("=" * 70)
    print("Example 3: Create a File")
    print("=" * 70)
    
    result = assistant.use_tool(
        "WriteFile",
        filePath="/home/engine/project/example_output.txt",
        content="Hello from the AI Assistant!\nThis is a test file."
    )
    
    if result["success"]:
        print(f"✅ File created successfully: {result['path']}")
    else:
        print(f"❌ Error: {result['error']}")
    print()


def example_4_read_file(assistant):
    """Example 4: Read a file."""
    print("=" * 70)
    print("Example 4: Read a File")
    print("=" * 70)
    
    result = assistant.use_tool(
        "ReadFile",
        filePath="/home/engine/project/example_output.txt"
    )
    
    if result["success"]:
        print(f"✅ File read successfully!")
        print(f"Content:\n{result['content']}")
    else:
        print(f"❌ Error: {result['error']}")
    print()


def example_5_list_directory(assistant):
    """Example 5: List directory contents."""
    print("=" * 70)
    print("Example 5: List Directory")
    print("=" * 70)
    
    result = assistant.use_tool(
        "LsTool",
        path="/home/engine/project"
    )
    
    if result["success"]:
        print(f"✅ Found {result['total']} items:")
        for entry in result['entries'][:5]:
            print(f"   - {entry}")
        if result['total'] > 5:
            print(f"   ... and {result['total'] - 5} more")
    else:
        print(f"❌ Error: {result['error']}")
    print()


def example_6_search_files(assistant):
    """Example 6: Search for files."""
    print("=" * 70)
    print("Example 6: Search for Python Files")
    print("=" * 70)
    
    result = assistant.use_tool(
        "GlobTool",
        pattern="*.py",
        path="/home/engine/project"
    )
    
    if result["success"]:
        print(f"✅ Found {result['count']} Python files:")
        for match in result['matches'][:5]:
            print(f"   - {match}")
        if result['count'] > 5:
            print(f"   ... and {result['count'] - 5} more")
    else:
        print(f"❌ Error: {result['error']}")
    print()


def example_7_terminal_command(assistant):
    """Example 7: Execute a terminal command."""
    print("=" * 70)
    print("Example 7: Execute Terminal Command")
    print("=" * 70)
    
    result = assistant.use_tool(
        "TerminalTool",
        input="echo 'Hello from terminal!'"
    )
    
    if result["success"]:
        print(f"✅ Command executed successfully!")
        print(f"Output: {result['stdout'].strip()}")
        print(f"Return code: {result['returncode']}")
    else:
        print(f"❌ Error: {result['error']}")
    print()


def example_8_memory_management(assistant):
    """Example 8: Use memory."""
    print("=" * 70)
    print("Example 8: Memory Management")
    print("=" * 70)
    
    # Store information
    assistant.update_memory("example_key", "example_value")
    print("✅ Stored: example_key = 'example_value'")
    
    # Retrieve information
    value = assistant.get_memory("example_key")
    print(f"✅ Retrieved: example_key = '{value}'")
    
    # View all memory
    memory = assistant.get_memory()
    print(f"✅ Total memory keys: {len(memory)}")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("  AI ASSISTANT REPLICA - BASIC USAGE EXAMPLES")
    print("=" * 70)
    print()
    
    try:
        # Initialize
        assistant = example_1_initialization()
        
        # Run examples
        example_2_simple_question(assistant)
        example_3_create_file(assistant)
        example_4_read_file(assistant)
        example_5_list_directory(assistant)
        example_6_search_files(assistant)
        example_7_terminal_command(assistant)
        example_8_memory_management(assistant)
        
        print("=" * 70)
        print("✅ All examples completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
