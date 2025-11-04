#!/usr/bin/env python3
"""
Behavior Comparison Test Suite

This module tests whether the Assistant Replica behaves similarly to the
original cto.new AI assistant by testing various scenarios and comparing
responses and actions.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from assistant_replica import Assistant


class BehaviorTest:
    """Test harness for comparing assistant behavior."""
    
    def __init__(self):
        self.test_dir = tempfile.mkdtemp()
        self.assistant = Assistant(project_path=self.test_dir)
        self.test_results = []
        
    def cleanup(self):
        """Clean up test environment."""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def log_result(self, test_name: str, passed: bool, details: str = ""):
        """Log test result."""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = {
            "test": test_name,
            "passed": passed,
            "details": details
        }
        self.test_results.append(result)
        print(f"{status}: {test_name}")
        if details:
            print(f"   {details}")
    
    def test_file_creation_behavior(self):
        """Test: File creation should follow best practices."""
        print("\n" + "=" * 70)
        print("Test: File Creation Behavior")
        print("=" * 70)
        
        test_file = Path(self.test_dir) / "example.py"
        
        # Use the assistant to create a file
        result = self.assistant.use_tool(
            "WriteFile",
            filePath=str(test_file),
            content='#!/usr/bin/env python3\n"""Example module."""\n\ndef main():\n    pass\n'
        )
        
        # Verify file was created
        passed = result["success"] and test_file.exists()
        self.log_result(
            "File Creation",
            passed,
            f"File created: {test_file.exists()}"
        )
        
        # Verify content has proper structure
        if test_file.exists():
            content = test_file.read_text()
            has_shebang = content.startswith("#!/usr/bin/env python3")
            has_docstring = '"""' in content
            
            self.log_result(
                "Python File Structure",
                has_shebang and has_docstring,
                f"Shebang: {has_shebang}, Docstring: {has_docstring}"
            )
    
    def test_file_editing_behavior(self):
        """Test: File editing should be precise and safe."""
        print("\n" + "=" * 70)
        print("Test: File Editing Behavior")
        print("=" * 70)
        
        test_file = Path(self.test_dir) / "edit_test.py"
        original_content = """def greet(name):
    print(f"Hello, {name}!")

def farewell(name):
    print(f"Goodbye, {name}!")
"""
        test_file.write_text(original_content)
        
        # Edit the file
        result = self.assistant.use_tool(
            "EditFile",
            filePath=str(test_file),
            oldString='print(f"Hello, {name}!")',
            newString='print(f"Hi there, {name}!")'
        )
        
        passed = result["success"]
        self.log_result(
            "File Edit Execution",
            passed,
            f"Edit successful: {passed}"
        )
        
        # Verify only the target was changed
        if passed:
            new_content = test_file.read_text()
            target_changed = "Hi there" in new_content
            others_unchanged = "Goodbye" in new_content
            
            self.log_result(
                "Edit Precision",
                target_changed and others_unchanged,
                f"Target changed: {target_changed}, Others intact: {others_unchanged}"
            )
    
    def test_error_handling_behavior(self):
        """Test: Should handle errors gracefully."""
        print("\n" + "=" * 70)
        print("Test: Error Handling Behavior")
        print("=" * 70)
        
        # Try to read non-existent file
        result = self.assistant.use_tool(
            "ReadFile",
            filePath="/nonexistent/file.txt"
        )
        
        handles_error = not result["success"] and "error" in result
        self.log_result(
            "Non-existent File Handling",
            handles_error,
            f"Error handled gracefully: {handles_error}"
        )
        
        # Try to edit with duplicate string
        test_file = Path(self.test_dir) / "duplicate.txt"
        test_file.write_text("test\ntest\ntest")
        
        result = self.assistant.use_tool(
            "EditFile",
            filePath=str(test_file),
            oldString="test",
            newString="changed"
        )
        
        detects_duplicate = not result["success"]
        self.log_result(
            "Duplicate String Detection",
            detects_duplicate,
            f"Duplicate detected: {detects_duplicate}"
        )
    
    def test_tool_integration_behavior(self):
        """Test: Should use multiple tools effectively."""
        print("\n" + "=" * 70)
        print("Test: Tool Integration Behavior")
        print("=" * 70)
        
        # Create multiple files
        for i in range(3):
            (Path(self.test_dir) / f"file{i}.py").write_text(f"# File {i}\n")
        
        # List files
        result1 = self.assistant.use_tool("LsTool", path=self.test_dir)
        list_works = result1["success"] and result1["total"] >= 3
        
        self.log_result(
            "Directory Listing",
            list_works,
            f"Found {result1.get('total', 0)} files"
        )
        
        # Search files
        result2 = self.assistant.use_tool("GlobTool", pattern="*.py", path=self.test_dir)
        search_works = result2["success"] and result2["count"] >= 3
        
        self.log_result(
            "Pattern Search",
            search_works,
            f"Found {result2.get('count', 0)} Python files"
        )
        
        # Grep content
        result3 = self.assistant.use_tool("GrepTool", pattern="File", path=self.test_dir)
        grep_works = result3["success"] and result3["count"] > 0
        
        self.log_result(
            "Content Search",
            grep_works,
            f"Found {result3.get('count', 0)} matches"
        )
    
    def test_llm_reasoning_behavior(self):
        """Test: Should provide intelligent responses."""
        print("\n" + "=" * 70)
        print("Test: LLM Reasoning Behavior")
        print("=" * 70)
        
        try:
            # Test basic reasoning
            response1 = self.assistant.execute_simple_task(
                "What programming language uses .py file extension? Answer in one word."
            )
            
            understands_python = "python" in response1.lower()
            self.log_result(
                "Basic Knowledge",
                understands_python,
                f"Correctly identified Python: {understands_python}"
            )
            
            # Test task understanding
            response2 = self.assistant.execute_simple_task(
                "If I ask you to create a Python file, what would be the first line you should add? Answer briefly."
            )
            
            knows_conventions = "shebang" in response2.lower() or "#!/usr" in response2
            self.log_result(
                "Convention Knowledge",
                knows_conventions,
                f"Understands Python conventions: {knows_conventions}"
            )
            
        except Exception as e:
            self.log_result(
                "LLM Reasoning",
                False,
                f"Error: {str(e)}"
            )
    
    def test_memory_behavior(self):
        """Test: Should maintain and use memory."""
        print("\n" + "=" * 70)
        print("Test: Memory Behavior")
        print("=" * 70)
        
        # Store information in memory
        self.assistant.update_memory("test_info", "test_value")
        
        # Retrieve it
        retrieved = self.assistant.get_memory("test_info")
        
        memory_works = retrieved == "test_value"
        self.log_result(
            "Memory Storage",
            memory_works,
            f"Value stored and retrieved: {memory_works}"
        )
        
        # Test persistence
        memory_file = Path(self.test_dir) / "assistant_memory.json"
        file_exists = memory_file.exists()
        
        self.log_result(
            "Memory Persistence",
            file_exists,
            f"Memory file created: {file_exists}"
        )
    
    def test_autonomous_decision_behavior(self):
        """Test: Should make autonomous decisions."""
        print("\n" + "=" * 70)
        print("Test: Autonomous Decision Behavior")
        print("=" * 70)
        
        try:
            # Ask a question that requires decision making
            response = self.assistant.execute_simple_task(
                "If you need to create a configuration file, would you use JSON or YAML? "
                "Choose one and explain in one sentence."
            )
            
            makes_decision = ("json" in response.lower() or "yaml" in response.lower())
            self.log_result(
                "Decision Making",
                makes_decision,
                f"Made a clear choice: {makes_decision}"
            )
            
        except Exception as e:
            self.log_result(
                "Autonomous Decision",
                False,
                f"Error: {str(e)}"
            )
    
    def test_code_quality_behavior(self):
        """Test: Should follow code quality standards."""
        print("\n" + "=" * 70)
        print("Test: Code Quality Behavior")
        print("=" * 70)
        
        try:
            # Ask to evaluate code structure
            response = self.assistant.execute_simple_task(
                "Should production code include print statements for debugging? Answer yes or no with brief reason."
            )
            
            knows_quality = "no" in response.lower()
            self.log_result(
                "Code Quality Standards",
                knows_quality,
                f"Understands code quality: {knows_quality}"
            )
            
        except Exception as e:
            self.log_result(
                "Code Quality",
                False,
                f"Error: {str(e)}"
            )
    
    def run_all_tests(self):
        """Run all behavior tests."""
        print("\n" + "=" * 80)
        print(" BEHAVIOR COMPARISON TEST SUITE")
        print("=" * 80)
        print("\nTesting if Assistant Replica behaves like cto.new AI Assistant")
        print("-" * 80)
        
        try:
            self.test_file_creation_behavior()
            self.test_file_editing_behavior()
            self.test_error_handling_behavior()
            self.test_tool_integration_behavior()
            self.test_llm_reasoning_behavior()
            self.test_memory_behavior()
            self.test_autonomous_decision_behavior()
            self.test_code_quality_behavior()
            
        finally:
            self.print_summary()
            self.cleanup()
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 80)
        print(" TEST SUMMARY")
        print("=" * 80)
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["passed"])
        failed = total - passed
        
        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed} (✅)")
        print(f"Failed: {failed} (❌)")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        if failed > 0:
            print("\n" + "-" * 80)
            print("Failed Tests:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"  ❌ {result['test']}")
                    if result["details"]:
                        print(f"     {result['details']}")
        
        print("\n" + "=" * 80)
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Behavior matches expected standards.")
        else:
            print(f"⚠️  {failed} test(s) need attention.")
        
        print("=" * 80)
        
        return passed == total


def main():
    """Main entry point."""
    tester = BehaviorTest()
    
    try:
        tester.run_all_tests()
        # Check if all tests passed
        passed = sum(1 for r in tester.test_results if r["passed"])
        total = len(tester.test_results)
        return 0 if passed == total else 1
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        return 130
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
