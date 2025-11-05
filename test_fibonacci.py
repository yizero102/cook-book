```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Negative arguments are not supported")
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```