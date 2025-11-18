# Code Optimization Quick Reference

## Quick Performance Tips

### 🔥 Algorithm & Data Structures
```python
# ❌ Bad: O(n²) nested loops
for i in items:
    for j in items:
        if i == j: ...

# ✅ Good: O(n) using set
seen = set()
for item in items:
    if item in seen: ...
```

### 🚀 Use Built-in Functions
```python
# ❌ Bad: Manual sum
total = 0
for x in numbers:
    total += x

# ✅ Good: Built-in sum (optimized in C)
total = sum(numbers)
```

### 💾 Memory Optimization
```python
# ❌ Bad: Creates entire list in memory
squares = [x**2 for x in range(1000000)]
total = sum(squares)

# ✅ Good: Generator (processes one at a time)
total = sum(x**2 for x in range(1000000))
```

### 📝 String Operations
```python
# ❌ Bad: O(n²) string concatenation
result = ""
for word in words:
    result += word + " "

# ✅ Good: O(n) using join
result = " ".join(words)
```

### 🔄 Early Exit
```python
# ❌ Bad: Checks all items
found = False
for item in items:
    if condition(item):
        found = True

# ✅ Good: Returns immediately
for item in items:
    if condition(item):
        return True
return False

# ✅ Best: Using any()
return any(condition(item) for item in items)
```

### 🎯 Caching & Memoization
```python
# ❌ Bad: Recalculates same values
def fibonacci(n):
    if n <= 1: return n
    return fibonacci(n-1) + fibonacci(n-2)

# ✅ Good: Caches results
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 1: return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### 📊 Dictionary Operations
```python
# ❌ Bad: Multiple lookups
if key in dict:
    dict[key] += 1
else:
    dict[key] = 1

# ✅ Good: Single lookup with default
dict[key] = dict.get(key, 0) + 1

# ✅ Best: Use Counter
from collections import Counter
counts = Counter(items)
```

### 🔍 Membership Testing
```python
# ❌ Bad: O(n) list search
items = [1, 2, 3, 4, 5]
if x in items: ...

# ✅ Good: O(1) set search
items = {1, 2, 3, 4, 5}
if x in items: ...
```

### ⚡ Loop Optimization
```python
# ❌ Bad: Recalculates in each iteration
for i in range(len(items)):
    process(items[i], len(items))

# ✅ Good: Calculate once
length = len(items)
for item in items:
    process(item, length)
```

### 🎨 List Comprehensions
```python
# ❌ Bad: Manual loop
squares = []
for x in range(10):
    if x % 2 == 0:
        squares.append(x**2)

# ✅ Good: List comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]
```

## Time Complexity Cheat Sheet

| Operation | List | Set | Dict |
|-----------|------|-----|------|
| Search | O(n) | O(1) | O(1) |
| Insert | O(1) | O(1) | O(1) |
| Delete | O(n) | O(1) | O(1) |
| Iterate | O(n) | O(n) | O(n) |

## Common Algorithm Improvements

| Problem | Naive | Optimized | Speedup |
|---------|-------|-----------|---------|
| Find duplicates | O(n²) | O(n) | ~100x |
| Sum of squares | O(n) space | O(1) space | ~20% |
| String building | O(n²) | O(n) | ~10x |
| Fibonacci | O(2ⁿ) | O(n) | Massive |
| Common elements | O(n×m) | O(n+m) | ~10-100x |

## When to Optimize

✅ **Do Optimize When:**
- Code is a proven bottleneck (profile first!)
- Working with large datasets
- Code runs frequently
- Performance impacts user experience

❌ **Don't Optimize When:**
- Code runs once/rarely
- Optimization hurts readability significantly
- Performance is already acceptable
- You haven't profiled yet

## Profiling Commands

```bash
# Time a Python script
time python3 script.py

# Profile with cProfile
python3 -m cProfile -s cumulative script.py

# Line profiler (install: pip install line_profiler)
kernprof -l -v script.py

# Memory profiler (install: pip install memory_profiler)
python3 -m memory_profiler script.py
```

## Remember

1. **Measure first** - Don't guess, profile!
2. **Readability matters** - Don't sacrifice clarity for minor gains
3. **Use the right tool** - Better algorithm > micro-optimizations
4. **Test correctness** - Ensure optimizations don't break functionality
5. **Document trade-offs** - Explain your optimization choices

---

**See OPTIMIZATION_GUIDE.md for detailed examples and explanations.**
