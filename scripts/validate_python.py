#!/usr/bin/env python3
import sys
import os
import py_compile
import ast
from pathlib import Path


def validate_python_file(file_path: Path) -> tuple[bool, str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        ast.parse(source_code)
        
        py_compile.compile(str(file_path), doraise=True)
        
        return True, "Valid"
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def find_python_files(root_dir: Path) -> list[Path]:
    python_files = []
    exclude_dirs = {'venv', '.git', '__pycache__', '.pytest_cache', 'node_modules'}
    
    for path in root_dir.rglob('*.py'):
        if not any(excluded in path.parts for excluded in exclude_dirs):
            python_files.append(path)
    
    return sorted(python_files)


def main():
    print("=" * 60)
    print("Python Script Validator")
    print("=" * 60)
    
    project_root = Path(__file__).parent.parent
    python_files = find_python_files(project_root)
    
    print(f"\nFound {len(python_files)} Python files to validate\n")
    
    valid_count = 0
    invalid_count = 0
    results = []
    
    for file_path in python_files:
        relative_path = file_path.relative_to(project_root)
        is_valid, message = validate_python_file(file_path)
        
        if is_valid:
            valid_count += 1
            status = "✓"
        else:
            invalid_count += 1
            status = "✗"
            results.append((relative_path, message))
        
        print(f"{status} {relative_path}")
        if not is_valid:
            print(f"  {message}")
    
    print("\n" + "=" * 60)
    print(f"Validation Results:")
    print(f"  Valid files: {valid_count}")
    print(f"  Invalid files: {invalid_count}")
    print("=" * 60)
    
    if invalid_count > 0:
        print("\nInvalid files:")
        for path, msg in results:
            print(f"  - {path}: {msg}")
        return 1
    
    print("\n✓ All Python files are valid!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
