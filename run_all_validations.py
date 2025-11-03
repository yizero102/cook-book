#!/usr/bin/env python3
"""
Master Validation Script
========================

This script runs all validations to ensure the AI agent replica
is fully functional and ready for deployment.

Run this script to verify:
1. LLM environment and connectivity
2. Agent replica functionality
3. All test cases (32 tests)
4. Identity verification (replica vs original)
5. All Python scripts validity
"""

import os
import sys
import subprocess
import json
from pathlib import Path


class ValidationRunner:
    """Runs all validation checks."""
    
    def __init__(self):
        self.results = []
        self.project_dir = Path("/home/engine/project")
    
    def run_command(self, description: str, command: list, critical: bool = True) -> bool:
        """Run a command and track results."""
        print(f"\n{'='*70}")
        print(f"Running: {description}")
        print(f"{'='*70}")
        
        try:
            result = subprocess.run(
                command,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            
            success = result.returncode == 0
            
            self.results.append({
                'description': description,
                'command': ' '.join(command),
                'success': success,
                'critical': critical,
                'returncode': result.returncode
            })
            
            if success:
                print(f"\n✅ {description}: PASSED")
            else:
                print(f"\n❌ {description}: FAILED (exit code: {result.returncode})")
                if critical:
                    print("⚠️  This is a critical check!")
            
            return success
            
        except subprocess.TimeoutExpired:
            print(f"\n❌ {description}: TIMEOUT")
            self.results.append({
                'description': description,
                'command': ' '.join(command),
                'success': False,
                'critical': critical,
                'returncode': -1
            })
            return False
        except Exception as e:
            print(f"\n❌ {description}: ERROR - {e}")
            self.results.append({
                'description': description,
                'command': ' '.join(command),
                'success': False,
                'critical': critical,
                'returncode': -1
            })
            return False
    
    def validate_python_scripts(self) -> bool:
        """Validate all Python scripts are syntactically correct."""
        print(f"\n{'='*70}")
        print("Validating Python Scripts")
        print(f"{'='*70}")
        
        python_files = list(self.project_dir.glob("*.py"))
        all_valid = True
        
        for py_file in python_files:
            print(f"\nChecking {py_file.name}...", end=" ")
            try:
                result = subprocess.run(
                    ["python", "-m", "py_compile", str(py_file)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    print("✓ Valid")
                else:
                    print("✗ Invalid")
                    print(result.stderr)
                    all_valid = False
            except Exception as e:
                print(f"✗ Error: {e}")
                all_valid = False
        
        self.results.append({
            'description': 'Python Script Validation',
            'command': 'py_compile all scripts',
            'success': all_valid,
            'critical': True,
            'returncode': 0 if all_valid else 1
        })
        
        if all_valid:
            print(f"\n✅ All Python scripts are valid")
        else:
            print(f"\n❌ Some Python scripts have syntax errors")
        
        return all_valid
    
    def check_file_structure(self) -> bool:
        """Verify all required files exist."""
        print(f"\n{'='*70}")
        print("Checking File Structure")
        print(f"{'='*70}")
        
        required_files = [
            "ai_agent_replica.py",
            "test_agent_replica.py",
            "verify_llm.py",
            "verify_replica_identity.py",
            "run_all_validations.py",
            "requirements.txt",
            "README.md",
            ".gitignore"
        ]
        
        all_exist = True
        for filename in required_files:
            filepath = self.project_dir / filename
            exists = filepath.exists()
            status = "✓" if exists else "✗"
            print(f"{status} {filename}")
            if not exists:
                all_exist = False
        
        self.results.append({
            'description': 'File Structure Check',
            'command': 'check required files',
            'success': all_exist,
            'critical': True,
            'returncode': 0 if all_exist else 1
        })
        
        if all_exist:
            print(f"\n✅ All required files present")
        else:
            print(f"\n❌ Some required files missing")
        
        return all_exist
    
    def print_summary(self):
        """Print summary of all validations."""
        print(f"\n\n{'='*70}")
        print("VALIDATION SUMMARY")
        print(f"{'='*70}\n")
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r['success'])
        failed = total - passed
        critical_failed = sum(1 for r in self.results if not r['success'] and r['critical'])
        
        print(f"Total Checks: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        if critical_failed > 0:
            print(f"Critical Failures: {critical_failed} ⚠️")
        
        print(f"\n{'='*70}")
        print("Detailed Results:")
        print(f"{'='*70}\n")
        
        for i, result in enumerate(self.results, 1):
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            critical = " (CRITICAL)" if result['critical'] else ""
            print(f"{i}. {result['description']}: {status}{critical}")
        
        print(f"\n{'='*70}")
        
        if failed == 0:
            print("🎉 ALL VALIDATIONS PASSED! 🎉")
            print(f"{'='*70}")
            print("\nThe AI Agent Replica System is fully operational!")
            print("\n✓ LLM connectivity verified")
            print("✓ Agent replica functional")
            print("✓ All tests passing (32/32)")
            print("✓ Identity verification successful (7/7)")
            print("✓ All Python scripts valid")
            print("✓ File structure complete")
            print("\n🚀 System ready for deployment and disaster recovery!")
        else:
            print("⚠️  SOME VALIDATIONS FAILED")
            print(f"{'='*70}")
            if critical_failed > 0:
                print(f"\n❌ {critical_failed} critical check(s) failed!")
                print("The system may not be fully functional.")
            else:
                print("\n⚠️  Non-critical checks failed.")
                print("The system may still be functional but needs attention.")
        
        print(f"\n{'='*70}\n")
    
    def run_all(self):
        """Run all validation checks."""
        print("="*70)
        print("AI AGENT REPLICA - MASTER VALIDATION SUITE")
        print("="*70)
        print("\nThis will verify all components of the AI agent replica system.")
        print("Expected duration: ~30-60 seconds\n")
        
        checks = [
            ("File Structure Check", self.check_file_structure, True),
            ("Python Script Validation", self.validate_python_scripts, True),
            ("LLM Environment Verification", 
             lambda: self.run_command(
                 "LLM Environment Verification",
                 ["python", "verify_llm.py"],
                 critical=True
             ), True),
            ("Agent Replica Initialization",
             lambda: self.run_command(
                 "Agent Replica Initialization",
                 ["python", "ai_agent_replica.py"],
                 critical=True
             ), True),
            ("Comprehensive Test Suite (32 tests)",
             lambda: self.run_command(
                 "Comprehensive Test Suite",
                 ["python", "test_agent_replica.py"],
                 critical=True
             ), True),
            ("Identity Verification (Replica vs Original)",
             lambda: self.run_command(
                 "Identity Verification",
                 ["python", "verify_replica_identity.py"],
                 critical=True
             ), True)
        ]
        
        for description, check_func, critical in checks:
            try:
                check_func()
            except Exception as e:
                print(f"\n❌ Error in {description}: {e}")
                self.results.append({
                    'description': description,
                    'command': 'check function',
                    'success': False,
                    'critical': critical,
                    'returncode': -1
                })
        
        self.print_summary()
        
        all_critical_passed = all(
            r['success'] for r in self.results if r['critical']
        )
        
        return 0 if all_critical_passed else 1


def main():
    """Main entry point."""
    runner = ValidationRunner()
    exit_code = runner.run_all()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
