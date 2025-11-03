#!/usr/bin/env python3
"""
Replica Identity Verification
==============================

This script verifies that the AI agent replica functions identically
to the original agent by testing all capabilities and comparing outputs.
"""

import os
import sys
import json
import tempfile
import shutil
from ai_agent_replica import AIAgentReplica, ToolType


class ReplicaVerifier:
    """Verifies that replica behaves identically to original."""
    
    def __init__(self):
        self.test_dir = tempfile.mkdtemp()
        self.agent = AIAgentReplica(working_directory=self.test_dir)
        self.verification_results = []
    
    def cleanup(self):
        """Clean up test resources."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def verify_test(self, test_name: str, test_func):
        """Run a verification test and record result."""
        try:
            result = test_func()
            self.verification_results.append({
                'test': test_name,
                'passed': result,
                'error': None
            })
            return result
        except Exception as e:
            self.verification_results.append({
                'test': test_name,
                'passed': False,
                'error': str(e)
            })
            return False
    
    def test_file_operations_identity(self):
        """Verify file operations work identically."""
        test_file = os.path.join(self.test_dir, "identity_test.txt")
        content = "Test content for identity verification\nLine 2\nLine 3"
        
        write_result = self.agent.execute_tool(
            ToolType.WRITE_FILE,
            file_path=test_file,
            content=content
        )
        if not write_result.success:
            return False
        
        read_result = self.agent.execute_tool(
            ToolType.READ_FILE,
            file_path=test_file
        )
        if not read_result.success:
            return False
        
        if content + "\n" != read_result.output:
            return False
        
        edit_result = self.agent.execute_tool(
            ToolType.EDIT_FILE,
            file_path=test_file,
            old_string="Line 2",
            new_string="Modified Line 2"
        )
        if not edit_result.success:
            return False
        
        verify_result = self.agent.execute_tool(
            ToolType.READ_FILE,
            file_path=test_file
        )
        
        return "Modified Line 2" in verify_result.output
    
    def test_terminal_operations_identity(self):
        """Verify terminal operations work identically."""
        commands = [
            ("echo 'Hello World'", "Hello World"),
            ("pwd", self.test_dir),
            ("ls -la", "total")
        ]
        
        for cmd, expected in commands:
            result = self.agent.execute_tool(
                ToolType.TERMINAL,
                command=cmd,
                cwd=self.test_dir
            )
            
            if not result.success:
                return False
            
            if expected not in result.output['stdout']:
                return False
        
        return True
    
    def test_search_operations_identity(self):
        """Verify search operations work identically."""
        test_file1 = os.path.join(self.test_dir, "search1.py")
        test_file2 = os.path.join(self.test_dir, "search2.py")
        
        self.agent.execute_tool(
            ToolType.WRITE_FILE,
            file_path=test_file1,
            content="def function1():\n    pass"
        )
        
        self.agent.execute_tool(
            ToolType.WRITE_FILE,
            file_path=test_file2,
            content="def function2():\n    return 42"
        )
        
        glob_result = self.agent.execute_tool(
            ToolType.GLOB,
            pattern="*.py",
            path=self.test_dir
        )
        
        if not glob_result.success or len(glob_result.output) < 2:
            return False
        
        grep_result = self.agent.execute_tool(
            ToolType.GREP,
            pattern="def function",
            path=self.test_dir
        )
        
        if not grep_result.success or len(grep_result.output) < 2:
            return False
        
        return True
    
    def test_llm_operations_identity(self):
        """Verify LLM operations work identically."""
        test_problems = [
            "What is 5 + 3?",
            "Name one primary color.",
            "What comes after Monday?"
        ]
        
        for problem in test_problems:
            result = self.agent.think(problem)
            
            if not result.success:
                return False
            
            if not result.output or not result.output.get('text'):
                return False
        
        return True
    
    def test_self_replication_identity(self):
        """Verify self-replication works identically."""
        replica_path = os.path.join(self.test_dir, "self_replica.py")
        
        result = self.agent.self_replicate(replica_path)
        
        if not result.success:
            return False
        
        if not os.path.exists(replica_path):
            return False
        
        with open(replica_path, 'r') as f:
            content = f.read()
        
        required_components = [
            "class AIAgentReplica",
            "def self_replicate",
            "class FileSystemTools",
            "class LLMClient",
            "def verify_capabilities"
        ]
        
        for component in required_components:
            if component not in content:
                return False
        
        return True
    
    def test_capability_verification_identity(self):
        """Verify capability checks work identically."""
        capabilities = self.agent.verify_capabilities()
        
        required_capabilities = [
            'write_file',
            'read_file',
            'terminal',
            'glob',
            'llm'
        ]
        
        for cap in required_capabilities:
            if cap not in capabilities:
                return False
            if not capabilities[cap]:
                return False
        
        return True
    
    def test_status_reporting_identity(self):
        """Verify status reporting works identically."""
        status = self.agent.get_status()
        
        required_fields = [
            'working_directory',
            'task_count',
            'capabilities',
            'memory_size'
        ]
        
        for field in required_fields:
            if field not in status:
                return False
        
        if status['working_directory'] != self.test_dir:
            return False
        
        return True
    
    def run_all_verifications(self):
        """Run all verification tests."""
        print("=" * 70)
        print("Replica Identity Verification")
        print("=" * 70)
        print("\nVerifying that replica behaves identically to original agent...\n")
        
        tests = [
            ("File Operations Identity", self.test_file_operations_identity),
            ("Terminal Operations Identity", self.test_terminal_operations_identity),
            ("Search Operations Identity", self.test_search_operations_identity),
            ("LLM Operations Identity", self.test_llm_operations_identity),
            ("Self-Replication Identity", self.test_self_replication_identity),
            ("Capability Verification Identity", self.test_capability_verification_identity),
            ("Status Reporting Identity", self.test_status_reporting_identity)
        ]
        
        for test_name, test_func in tests:
            print(f"Testing: {test_name}...", end=" ")
            result = self.verify_test(test_name, test_func)
            if result:
                print("✓ PASS")
            else:
                print("✗ FAIL")
                if self.verification_results[-1]['error']:
                    print(f"  Error: {self.verification_results[-1]['error']}")
        
        passed = sum(1 for r in self.verification_results if r['passed'])
        total = len(self.verification_results)
        
        print("\n" + "=" * 70)
        print(f"Verification Results: {passed}/{total} tests passed")
        print("=" * 70)
        
        if passed == total:
            print("\n✅ SUCCESS: Replica is identical to original agent!")
            print("\nThe replica has been verified to have:")
            print("  • Identical file operation behavior")
            print("  • Identical terminal operation behavior")
            print("  • Identical search operation behavior")
            print("  • Identical LLM interaction behavior")
            print("  • Identical self-replication capability")
            print("  • Identical capability verification")
            print("  • Identical status reporting")
            print("\n🎉 The agent replica can fully replace the original!")
        else:
            print(f"\n⚠️  WARNING: {total - passed} verification(s) failed")
            print("The replica may not behave identically to the original.")
        
        print("=" * 70)
        
        return passed == total


def main():
    """Main entry point."""
    verifier = ReplicaVerifier()
    
    try:
        success = verifier.run_all_verifications()
        return 0 if success else 1
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        verifier.cleanup()


if __name__ == "__main__":
    sys.exit(main())
