#!/usr/bin/env python3
import re

with open('generated_password_manager.py', 'r') as f:
    content = f.read()

# Remove the box drawing characters and trailing spaces
lines = []
for line in content.split('\n'):
    # Strip leading/trailing box characters and whitespace
    cleaned = line.lstrip('│ ').rstrip('│ ')
    lines.append(cleaned)

cleaned_code = '\n'.join(lines)

with open('generated_password_manager.py', 'w') as f:
    f.write(cleaned_code)

print(f'✓ Cleaned generated code: {len(lines)} lines')
