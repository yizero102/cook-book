#!/usr/bin/env python3
import sys

content = open('showcase_output.txt').read()
start = content.find('```python', content.find('Generated Password Manager'))
if start > 0:
    start += 9
    end = content.find('```', start)
    if end > start:
        code = content[start:end].strip()
        with open('generated_password_manager.py', 'w') as f:
            f.write(code)
        print(f'✓ Password manager extracted: {len(code)} characters')
    else:
        print('✗ Could not find end marker')
else:
    print('✗ Could not find code block')
