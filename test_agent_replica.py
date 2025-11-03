#!/usr/bin/env python3
"""
Comprehensive Test Suite for AI Agent Replica
==============================================

This test suite verifies all capabilities of the AI agent replica
to ensure it functions identically to the original agent.
"""

import os
import sys
import unittest
import tempfile
import shutil
from pathlib import Path

from ai_agent_replica import (
    AIAgentReplica,
    FileSystemTools,
    CodeSearchTools,
    TerminalTools,
    LLMClient,
    ToolType,
    ToolResult,
    Task
)


class TestFileSystemTools(unittest.TestCase):
    """Test file system operations."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.fs_tools = FileSystemTools()
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_write_file(self):
        """Test writing a file."""
        file_path = os.path.join(self.test_dir, "test.txt")
        result = self.fs_tools.write_file(file_path, "Hello, World!")
        
        self.assertTrue(result.success)
        self.assertTrue(os.path.exists(file_path))
        
        with open(file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, "Hello, World!\n")
    
    def test_write_file_no_newline(self):
        """Test writing a file without adding newline."""
        file_path = os.path.join(self.test_dir, "test.txt")
        result = self.fs_tools.write_file(file_path, "Hello", add_newline=False)
        
        self.assertTrue(result.success)
        with open(file_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, "Hello")
    
    def test_read_file(self):
        """Test reading a file."""
        file_path = os.path.join(self.test_dir, "test.txt")
        content = "Line 1\nLine 2\nLine 3\n"
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        result = self.fs_tools.read_file(file_path)
        self.assertTrue(result.success)
        self.assertEqual(result.output, content)
    
    def test_read_file_with_limit(self):
        """Test reading a file with limit."""
        file_path = os.path.join(self.test_dir, "test.txt")
        content = "Line 1\nLine 2\nLine 3\nLine 4\n"
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        result = self.fs_tools.read_file(file_path, offset=0, limit=2)
        self.assertTrue(result.success)
        self.assertEqual(result.output, "Line 1\nLine 2\n")
        self.assertEqual(result.metadata['returned_lines'], 2)
    
    def test_read_nonexistent_file(self):
        """Test reading a file that doesn't exist."""
        file_path = os.path.join(self.test_dir, "nonexistent.txt")
        result = self.fs_tools.read_file(file_path)
        
        self.assertFalse(result.success)
        self.assertIn("not found", result.error.lower())
    
    def test_edit_file(self):
        """Test editing a file."""
        file_path = os.path.join(self.test_dir, "test.txt")
        original_content = "Hello World\nThis is a test\n"
        
        with open(file_path, 'w') as f:
            f.write(original_content)
        
        result = self.fs_tools.edit_file(
            file_path,
            "Hello World",
            "Hello Universe"
        )
        
        self.assertTrue(result.success)
        
        with open(file_path, 'r') as f:
            new_content = f.read()
        self.assertEqual(new_content, "Hello Universe\nThis is a test\n")
    
    def test_edit_file_duplicate_string(self):
        """Test editing when string appears multiple times."""
        file_path = os.path.join(self.test_dir, "test.txt")
        content = "Hello\nHello\n"
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        result = self.fs_tools.edit_file(file_path, "Hello", "Hi")
        self.assertFalse(result.success)
        self.assertIn("times", result.error.lower())
    
    def test_ls_tool(self):
        """Test listing directory contents."""
        os.makedirs(os.path.join(self.test_dir, "subdir"))
        Path(os.path.join(self.test_dir, "file1.txt")).touch()
        Path(os.path.join(self.test_dir, "file2.txt")).touch()
        
        result = self.fs_tools.ls_tool(self.test_dir)
        
        self.assertTrue(result.success)
        self.assertIn("file1.txt", result.output)
        self.assertIn("file2.txt", result.output)
        self.assertIn("subdir", result.output)
    
    def test_relative_path_rejection(self):
        """Test that relative paths are rejected."""
        result = self.fs_tools.read_file("relative/path.txt")
        self.assertFalse(result.success)
        self.assertIn("absolute", result.error.lower())


class TestCodeSearchTools(unittest.TestCase):
    """Test code search operations."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.search_tools = CodeSearchTools()
        
        os.makedirs(os.path.join(self.test_dir, "src"))
        
        with open(os.path.join(self.test_dir, "test.py"), 'w') as f:
            f.write("def hello():\n    print('Hello')\n")
        
        with open(os.path.join(self.test_dir, "src", "main.py"), 'w') as f:
            f.write("def main():\n    pass\n")
        
        with open(os.path.join(self.test_dir, "README.md"), 'w') as f:
            f.write("# Test Project\n")
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_glob_simple_pattern(self):
        """Test glob with simple pattern."""
        result = self.search_tools.glob_tool("*.py", self.test_dir)
        
        self.assertTrue(result.success)
        self.assertIsInstance(result.output, list)
        self.assertTrue(any("test.py" in path for path in result.output))
    
    def test_glob_recursive_pattern(self):
        """Test glob with recursive pattern."""
        result = self.search_tools.glob_tool("**/*.py", self.test_dir)
        
        self.assertTrue(result.success)
        self.assertIsInstance(result.output, list)
        self.assertTrue(len(result.output) >= 2)
    
    def test_grep_simple_search(self):
        """Test grep for simple text search."""
        result = self.search_tools.grep_tool("def hello", self.test_dir)
        
        self.assertTrue(result.success)
        self.assertIsInstance(result.output, list)
        self.assertTrue(len(result.output) > 0)
        self.assertTrue(any("hello" in match['content'] for match in result.output))
    
    def test_grep_with_file_filter(self):
        """Test grep with file type filter."""
        result = self.search_tools.grep_tool("def", self.test_dir, include="*.py")
        
        self.assertTrue(result.success)
        matches = result.output
        self.assertTrue(all(match['file'].endswith('.py') for match in matches))
    
    def test_grep_regex_pattern(self):
        """Test grep with regex pattern."""
        result = self.search_tools.grep_tool(r"def\s+\w+", self.test_dir)
        
        self.assertTrue(result.success)
        self.assertTrue(len(result.output) > 0)


class TestTerminalTools(unittest.TestCase):
    """Test terminal operations."""
    
    def setUp(self):
        """Set up test environment."""
        self.terminal_tools = TerminalTools()
    
    def test_execute_simple_command(self):
        """Test executing a simple command."""
        result = self.terminal_tools.execute_command("echo 'Hello'")
        
        self.assertTrue(result.success)
        self.assertIn("Hello", result.output['stdout'])
        self.assertEqual(result.output['returncode'], 0)
    
    def test_execute_failing_command(self):
        """Test executing a command that fails."""
        result = self.terminal_tools.execute_command("exit 1")
        
        self.assertFalse(result.success)
        self.assertEqual(result.output['returncode'], 1)
    
    def test_execute_with_stderr(self):
        """Test command that outputs to stderr."""
        result = self.terminal_tools.execute_command(">&2 echo 'Error'")
        
        self.assertTrue(result.success)
        self.assertIn("Error", result.output['stderr'])
    
    def test_execute_command_with_cwd(self):
        """Test executing command with custom working directory."""
        result = self.terminal_tools.execute_command("pwd", cwd="/tmp")
        
        self.assertTrue(result.success)
        self.assertIn("/tmp", result.output['stdout'])


class TestLLMClient(unittest.TestCase):
    """Test LLM client operations."""
    
    def setUp(self):
        """Set up LLM client."""
        required_vars = ['_ANTHROPIC_API_KEY', '_ANTHROPIC_BASE_URL', '_MODEL_NAME']
        if not all(os.environ.get(var) for var in required_vars):
            self.skipTest("LLM environment variables not set")
        
        try:
            self.llm_client = LLMClient()
        except Exception as e:
            self.skipTest(f"Could not initialize LLM client: {e}")
    
    def test_simple_call(self):
        """Test a simple LLM call."""
        messages = [
            {"role": "user", "content": "Reply with just the word 'OK'"}
        ]
        
        result = self.llm_client.call(messages, max_tokens=10)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)
        self.assertIn('text', result.output)
    
    def test_call_with_system_message(self):
        """Test LLM call with system message."""
        messages = [
            {"role": "user", "content": "What is 2+2?"}
        ]
        system = "You are a helpful math assistant."
        
        result = self.llm_client.call(messages, system=system, max_tokens=50)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)
        self.assertIn('text', result.output)


class TestAIAgentReplica(unittest.TestCase):
    """Test the complete AI agent replica."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        
        required_vars = ['_ANTHROPIC_API_KEY', '_ANTHROPIC_BASE_URL', '_MODEL_NAME']
        self.has_llm = all(os.environ.get(var) for var in required_vars)
        
        if self.has_llm:
            self.agent = AIAgentReplica(working_directory=self.test_dir)
        else:
            self.agent = None
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_agent_initialization(self):
        """Test agent initializes correctly."""
        if not self.has_llm:
            self.skipTest("LLM not available")
        
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.working_directory, self.test_dir)
        self.assertIsInstance(self.agent.memory, dict)
        self.assertIsInstance(self.agent.task_history, list)
    
    def test_execute_read_file_tool(self):
        """Test executing read file tool through agent."""
        if not self.has_llm:
            self.skipTest("LLM not available")
        
        test_file = os.path.join(self.test_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("Test content")
        
        result = self.agent.execute_tool(
            ToolType.READ_FILE,
            file_path=test_file
        )
        
        self.assertTrue(result.success)
        self.assertIn("Test content", result.output)
    
    def test_execute_write_file_tool(self):
        """Test executing write file tool through agent."""
        if not self.has_llm:
            self.skipTest("LLM not available")
        
        test_file = os.path.join(self.test_dir, "output.txt")
        result = self.agent.execute_tool(
            ToolType.WRITE_FILE,
            file_path=test_file,
            content="New content"
        )
        
        self.assertTrue(result.success)
        self.assertTrue(os.path.exists(test_file))
    
    def test_execute_terminal_tool(self):
        """Test executing terminal tool through agent."""
        if not self.has_llm:
            self.skipTest("LLM not available")
        
        result = self.agent.execute_tool(
            ToolType.TERMINAL,
            command="echo 'test'"
        )
        
        self.assertTrue(result.success)
        self.assertIn("test", result.output['stdout'])
    
    def test_think_method(self):
        """Test the think method."""
        if not self.has_llm:
            self.skipTest("LLM not available")
        
        result = self.agent.think("What is the capital of France?")
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)
    
    def test_complete_task(self):
        """Test completing a task."""
        if not self.has_llm:
            self.skipTest("LLM not available")
        
        task = Task(
            description="Analyze what 2+2 equals",
            context={"operation": "addition"}
        )
        
        result = self.agent.complete_task(task)
        
        self.assertTrue(result.success)
        self.assertTrue(task.completed)
        self.assertEqual(len(self.agent.task_history), 1)
    
    def test_self_replicate(self):
        """Test self-replication capability."""
        if not self.has_llm:
            self.skipTest("LLM not available")
        
        target_path = os.path.join(self.test_dir, "replica.py")
        result = self.agent.self_replicate(target_path)
        
        self.assertTrue(result.success)
        self.assertTrue(os.path.exists(target_path))
        
        with open(target_path, 'r') as f:
            content = f.read()
        
        self.assertIn("class AIAgentReplica", content)
        self.assertIn("def self_replicate", content)
    
    def test_verify_capabilities(self):
        """Test capability verification."""
        if not self.has_llm:
            self.skipTest("LLM not available")
        
        capabilities = self.agent.verify_capabilities()
        
        self.assertIsInstance(capabilities, dict)
        self.assertIn('write_file', capabilities)
        self.assertIn('read_file', capabilities)
        self.assertIn('terminal', capabilities)
        self.assertIn('llm', capabilities)
    
    def test_get_status(self):
        """Test getting agent status."""
        if not self.has_llm:
            self.skipTest("LLM not available")
        
        status = self.agent.get_status()
        
        self.assertIsInstance(status, dict)
        self.assertIn('working_directory', status)
        self.assertIn('capabilities', status)
        self.assertIn('task_count', status)


class TestIntegrationScenarios(unittest.TestCase):
    """Test complete integration scenarios."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        
        required_vars = ['_ANTHROPIC_API_KEY', '_ANTHROPIC_BASE_URL', '_MODEL_NAME']
        self.has_llm = all(os.environ.get(var) for var in required_vars)
        
        if self.has_llm:
            self.agent = AIAgentReplica(working_directory=self.test_dir)
        else:
            self.agent = None
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_complete_workflow_create_and_modify_file(self):
        """Test complete workflow: create, read, modify file."""
        if not self.has_llm:
            self.skipTest("LLM not available")
        
        file_path = os.path.join(self.test_dir, "workflow.txt")
        
        write_result = self.agent.execute_tool(
            ToolType.WRITE_FILE,
            file_path=file_path,
            content="Initial content\nSecond line"
        )
        self.assertTrue(write_result.success)
        
        read_result = self.agent.execute_tool(
            ToolType.READ_FILE,
            file_path=file_path
        )
        self.assertTrue(read_result.success)
        self.assertIn("Initial content", read_result.output)
        
        edit_result = self.agent.execute_tool(
            ToolType.EDIT_FILE,
            file_path=file_path,
            old_string="Initial content",
            new_string="Modified content"
        )
        self.assertTrue(edit_result.success)
        
        verify_result = self.agent.execute_tool(
            ToolType.READ_FILE,
            file_path=file_path
        )
        self.assertTrue(verify_result.success)
        self.assertIn("Modified content", verify_result.output)
    
    def test_search_and_analyze_workflow(self):
        """Test workflow: create files, search, analyze."""
        if not self.has_llm:
            self.skipTest("LLM not available")
        
        py_file = os.path.join(self.test_dir, "example.py")
        self.agent.execute_tool(
            ToolType.WRITE_FILE,
            file_path=py_file,
            content="def example_function():\n    return 42"
        )
        
        glob_result = self.agent.execute_tool(
            ToolType.GLOB,
            pattern="*.py",
            path=self.test_dir
        )
        self.assertTrue(glob_result.success)
        self.assertTrue(len(glob_result.output) > 0)
        
        grep_result = self.agent.execute_tool(
            ToolType.GREP,
            pattern="def",
            path=self.test_dir
        )
        self.assertTrue(grep_result.success)
        self.assertTrue(len(grep_result.output) > 0)
    
    def test_self_replication_and_verification(self):
        """Test self-replication creates functional copy."""
        if not self.has_llm:
            self.skipTest("LLM not available")
        
        replica_path = os.path.join(self.test_dir, "agent_copy.py")
        
        replication_result = self.agent.self_replicate(replica_path)
        self.assertTrue(replication_result.success)
        self.assertTrue(os.path.exists(replica_path))
        
        original_file = "/home/engine/project/ai_agent_replica.py"
        if os.path.exists(original_file):
            with open(original_file, 'r') as f:
                original_content = f.read()
            
            with open(replica_path, 'r') as f:
                replica_content = f.read()
            
            self.assertEqual(original_content, replica_content)


def run_test_suite():
    """Run the complete test suite with detailed output."""
    print("=" * 70)
    print("AI Agent Replica - Comprehensive Test Suite")
    print("=" * 70)
    print()
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    test_classes = [
        TestFileSystemTools,
        TestCodeSearchTools,
        TestTerminalTools,
        TestLLMClient,
        TestAIAgentReplica,
        TestIntegrationScenarios
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_test_suite())
