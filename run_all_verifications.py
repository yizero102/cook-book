#!/usr/bin/env python3
"""
Comprehensive Verification Script

This script runs all tests and verifications to ensure the AI Assistant
Replica is working correctly and behaves as expected.
"""

import sys
import subprocess
import os
from pathlib import Path


class VerificationRunner:
    """Runs all verification tests."""
    
    def __init__(self):
        self.results = []
        self.project_root = Path(__file__).parent
        
    def run_command(self, name: str, command: list, description: str):
        """Run a command and track results."""
        print("\n" + "=" * 80)
        print(f"🔍 {name}")
        print("=" * 80)
        print(f"Description: {description}")
        print(f"Command: {' '.join(command)}")
        print("-" * 80)
        
        try:
            result = subprocess.run(
                command,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Print output
            if result.stdout:
                print(result.stdout)
            if result.stderr and result.returncode != 0:
                print("STDERR:", result.stderr)
            
            success = result.returncode == 0
            
            if success:
                print(f"\n✅ {name} PASSED")
            else:
                print(f"\n❌ {name} FAILED (exit code: {result.returncode})")
            
            self.results.append({
                "name": name,
                "success": success,
                "exit_code": result.returncode
            })
            
            return success
            
        except subprocess.TimeoutExpired:
            print(f"\n❌ {name} TIMEOUT")
            self.results.append({
                "name": name,
                "success": False,
                "exit_code": -1
            })
            return False
            
        except Exception as e:
            print(f"\n❌ {name} ERROR: {e}")
            self.results.append({
                "name": name,
                "success": False,
                "exit_code": -2
            })
            return False
    
    def verify_environment(self):
        """Verify environment setup."""
        print("\n" + "=" * 80)
        print("🔍 Environment Verification")
        print("=" * 80)
        
        required_vars = ["_ANTHROPIC_API_KEY", "_ANTHROPIC_BASE_URL", "_MODEL_NAME"]
        all_set = True
        
        for var in required_vars:
            value = os.getenv(var)
            if value:
                masked = f"{value[:20]}..." if len(value) > 20 else value
                print(f"✅ {var}: {masked}")
            else:
                print(f"❌ {var}: NOT SET")
                all_set = False
        
        self.results.append({
            "name": "Environment Variables",
            "success": all_set,
            "exit_code": 0 if all_set else 1
        })
        
        return all_set
    
    def verify_python_version(self):
        """Verify Python version."""
        print("\n" + "=" * 80)
        print("🔍 Python Version")
        print("=" * 80)
        
        version = sys.version_info
        print(f"Python {version.major}.{version.minor}.{version.micro}")
        
        success = version.major >= 3 and version.minor >= 8
        
        if success:
            print("✅ Python version is compatible (3.8+)")
        else:
            print("❌ Python version is too old (need 3.8+)")
        
        self.results.append({
            "name": "Python Version",
            "success": success,
            "exit_code": 0 if success else 1
        })
        
        return success
    
    def verify_dependencies(self):
        """Verify required dependencies are installed."""
        print("\n" + "=" * 80)
        print("🔍 Dependencies")
        print("=" * 80)
        
        try:
            import anthropic
            print(f"✅ anthropic: {anthropic.__version__}")
            success = True
        except ImportError:
            print("❌ anthropic: NOT INSTALLED")
            success = False
        
        self.results.append({
            "name": "Dependencies",
            "success": success,
            "exit_code": 0 if success else 1
        })
        
        return success
    
    def print_summary(self):
        """Print final summary."""
        print("\n" + "=" * 80)
        print("📊 VERIFICATION SUMMARY")
        print("=" * 80)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r["success"])
        failed = total - passed
        
        print(f"\nTotal Checks: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        if failed > 0:
            print("\n" + "-" * 80)
            print("Failed Checks:")
            for result in self.results:
                if not result["success"]:
                    print(f"  ❌ {result['name']} (exit code: {result['exit_code']})")
        
        print("\n" + "=" * 80)
        
        if failed == 0:
            print("🎉 ALL VERIFICATIONS PASSED!")
            print("The AI Assistant Replica is fully functional and ready to use.")
        else:
            print(f"⚠️  {failed} verification(s) failed.")
            print("Please review the errors above and fix them.")
        
        print("=" * 80)
        
        return failed == 0


def main():
    """Main entry point."""
    print("\n" + "=" * 80)
    print("  AI ASSISTANT REPLICA - COMPREHENSIVE VERIFICATION")
    print("=" * 80)
    print()
    print("This script will verify all components of the system:")
    print("  1. Environment configuration")
    print("  2. Python version")
    print("  3. Dependencies")
    print("  4. LLM connection")
    print("  5. Unit tests")
    print("  6. Behavior tests")
    print("  7. Main assistant functionality")
    print()
    
    runner = VerificationRunner()
    
    # Run verifications
    runner.verify_python_version()
    runner.verify_environment()
    runner.verify_dependencies()
    
    # Test 1: LLM Connection
    runner.run_command(
        "LLM Connection Test",
        ["python3", "test_llm_connection.py"],
        "Verify that the LLM API is accessible and working"
    )
    
    # Test 2: Unit Tests
    runner.run_command(
        "Unit Tests",
        ["python3", "test_assistant.py"],
        "Run comprehensive unit tests for all components"
    )
    
    # Test 3: Behavior Tests
    runner.run_command(
        "Behavior Comparison Tests",
        ["python3", "test_behavior_comparison.py"],
        "Verify behavior matches expected standards"
    )
    
    # Test 4: Main Assistant
    runner.run_command(
        "Assistant Replica",
        ["python3", "assistant_replica.py"],
        "Run the main assistant program"
    )
    
    # Test 5: Basic Usage Examples
    runner.run_command(
        "Basic Usage Examples",
        ["python3", "examples/basic_usage.py"],
        "Test basic usage patterns"
    )
    
    # Test 6: File Operations Examples
    runner.run_command(
        "File Operations Examples",
        ["python3", "examples/file_operations.py"],
        "Test file operation patterns"
    )
    
    # Print summary
    success = runner.print_summary()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
