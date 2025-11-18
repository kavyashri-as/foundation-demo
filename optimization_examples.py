"""
Optimization Code Examples
===========================

This module demonstrates various code optimization techniques including:
1. Algorithm optimization (time complexity)
2. Memory optimization (space complexity)
3. Data structure optimization
4. Code efficiency optimization

Each example shows BEFORE (unoptimized) and AFTER (optimized) versions.
"""

import time
from functools import lru_cache
from typing import List, Dict, Set


# ============================================================================
# Example 1: Algorithm Optimization - Fibonacci Sequence
# ============================================================================

def fibonacci_unoptimized(n: int) -> int:
    """
    Unoptimized fibonacci using recursion.
    Time Complexity: O(2^n) - Exponential (very slow)
    Space Complexity: O(n) - Call stack depth
    """
    if n <= 1:
        return n
    return fibonacci_unoptimized(n - 1) + fibonacci_unoptimized(n - 2)


@lru_cache(maxsize=None)
def fibonacci_optimized(n: int) -> int:
    """
    Optimized fibonacci using memoization.
    Time Complexity: O(n) - Linear
    Space Complexity: O(n) - Cache storage
    """
    if n <= 1:
        return n
    return fibonacci_optimized(n - 1) + fibonacci_optimized(n - 2)


def fibonacci_iterative(n: int) -> int:
    """
    Most optimized fibonacci using iteration.
    Time Complexity: O(n) - Linear
    Space Complexity: O(1) - Constant
    """
    if n <= 1:
        return n
    
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr


# ============================================================================
# Example 2: Data Structure Optimization - Finding Duplicates
# ============================================================================

def find_duplicates_unoptimized(numbers: List[int]) -> List[int]:
    """
    Unoptimized approach using nested loops.
    Time Complexity: O(n²) - Quadratic
    Space Complexity: O(n) - Result list
    """
    duplicates = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j] and numbers[i] not in duplicates:
                duplicates.append(numbers[i])
    return duplicates


def find_duplicates_optimized(numbers: List[int]) -> List[int]:
    """
    Optimized approach using a set for O(1) lookup.
    Time Complexity: O(n) - Linear
    Space Complexity: O(n) - Set storage
    """
    seen = set()
    duplicates = set()
    
    for num in numbers:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    
    return list(duplicates)


# ============================================================================
# Example 3: Memory Optimization - Processing Large Lists
# ============================================================================

def sum_squares_unoptimized(n: int) -> int:
    """
    Unoptimized: Creates entire list in memory.
    Time Complexity: O(n)
    Space Complexity: O(n) - Stores entire list
    """
    numbers = [i ** 2 for i in range(n)]
    return sum(numbers)


def sum_squares_optimized(n: int) -> int:
    """
    Optimized: Uses generator to avoid storing entire list.
    Time Complexity: O(n)
    Space Complexity: O(1) - Generator doesn't store values
    """
    return sum(i ** 2 for i in range(n))


# ============================================================================
# Example 4: String Concatenation Optimization
# ============================================================================

def build_string_unoptimized(words: List[str]) -> str:
    """
    Unoptimized: String concatenation in loop creates new string each time.
    Time Complexity: O(n²) - Due to string immutability
    Space Complexity: O(n²) - Multiple intermediate strings
    """
    result = ""
    for word in words:
        result += word + " "
    return result.strip()


def build_string_optimized(words: List[str]) -> str:
    """
    Optimized: Using join() is much more efficient.
    Time Complexity: O(n) - Linear
    Space Complexity: O(n) - Single final string
    """
    return " ".join(words)


# ============================================================================
# Example 5: Loop Optimization - Avoiding Redundant Operations
# ============================================================================

def calculate_averages_unoptimized(data: List[List[int]]) -> List[float]:
    """
    Unoptimized: Recalculates len() in every iteration.
    Time Complexity: O(n*m) where n is outer list, m is inner list
    """
    averages = []
    for row in data:
        total = 0
        for value in row:
            total += value
        averages.append(total / len(row))  # len() called each time
    return averages


def calculate_averages_optimized(data: List[List[int]]) -> List[float]:
    """
    Optimized: Calculate length once, use built-in sum().
    Time Complexity: O(n*m) - Same but faster in practice
    """
    averages = []
    for row in data:
        if row:  # Check for empty list
            averages.append(sum(row) / len(row))
    return averages


def calculate_averages_most_optimized(data: List[List[int]]) -> List[float]:
    """
    Most optimized: List comprehension with single-pass calculation.
    Time Complexity: O(n*m) - Same but most Pythonic
    """
    return [sum(row) / len(row) for row in data if row]


# ============================================================================
# Example 6: Dictionary Lookup Optimization
# ============================================================================

def count_frequencies_unoptimized(items: List[str]) -> Dict[str, int]:
    """
    Unoptimized: Multiple dictionary operations per item.
    """
    frequencies = {}
    for item in items:
        if item in frequencies:
            frequencies[item] = frequencies[item] + 1
        else:
            frequencies[item] = 1
    return frequencies


def count_frequencies_optimized(items: List[str]) -> Dict[str, int]:
    """
    Optimized: Using dict.get() with default value.
    """
    frequencies = {}
    for item in items:
        frequencies[item] = frequencies.get(item, 0) + 1
    return frequencies


def count_frequencies_most_optimized(items: List[str]) -> Dict[str, int]:
    """
    Most optimized: Using collections.Counter.
    """
    from collections import Counter
    return dict(Counter(items))


# ============================================================================
# Example 7: Early Exit Optimization
# ============================================================================

def contains_negative_unoptimized(numbers: List[int]) -> bool:
    """
    Unoptimized: Checks all numbers even after finding a negative.
    """
    found = False
    for num in numbers:
        if num < 0:
            found = True
    return found


def contains_negative_optimized(numbers: List[int]) -> bool:
    """
    Optimized: Returns immediately upon finding a negative.
    """
    for num in numbers:
        if num < 0:
            return True
    return False


def contains_negative_most_optimized(numbers: List[int]) -> bool:
    """
    Most optimized: Using any() with generator.
    """
    return any(num < 0 for num in numbers)


# ============================================================================
# Example 8: Set Operations Optimization
# ============================================================================

def find_common_elements_unoptimized(list1: List[int], list2: List[int]) -> List[int]:
    """
    Unoptimized: Nested loop approach.
    Time Complexity: O(n*m)
    """
    common = []
    for item in list1:
        if item in list2 and item not in common:
            common.append(item)
    return common


def find_common_elements_optimized(list1: List[int], list2: List[int]) -> List[int]:
    """
    Optimized: Using set intersection.
    Time Complexity: O(n + m)
    """
    return list(set(list1) & set(list2))


# ============================================================================
# Benchmarking Utilities
# ============================================================================

def benchmark_function(func, *args, iterations=1):
    """Utility function to benchmark execution time."""
    start_time = time.perf_counter()
    for _ in range(iterations):
        result = func(*args)
    end_time = time.perf_counter()
    avg_time = (end_time - start_time) / iterations
    return result, avg_time


def compare_optimizations():
    """
    Demonstrates the performance difference between optimized and unoptimized code.
    """
    print("=" * 70)
    print("CODE OPTIMIZATION COMPARISON")
    print("=" * 70)
    
    # Example 1: Fibonacci
    print("\n1. Fibonacci Calculation (n=30)")
    print("-" * 70)
    n = 30
    
    # Skip unoptimized version for large n as it's too slow
    # _, time_unopt = benchmark_function(fibonacci_unoptimized, n)
    # print(f"Unoptimized (recursive):    {time_unopt:.6f} seconds")
    
    _, time_opt = benchmark_function(fibonacci_optimized, n)
    print(f"Optimized (memoization):    {time_opt:.6f} seconds")
    
    _, time_iter = benchmark_function(fibonacci_iterative, n)
    print(f"Most optimized (iterative): {time_iter:.6f} seconds")
    print(f"Speedup: {time_opt/time_iter:.2f}x faster")
    
    # Example 2: Find Duplicates
    print("\n2. Finding Duplicates (1000 numbers)")
    print("-" * 70)
    test_list = list(range(500)) * 2  # 1000 numbers with duplicates
    
    _, time_unopt = benchmark_function(find_duplicates_unoptimized, test_list)
    print(f"Unoptimized (nested loops): {time_unopt:.6f} seconds")
    
    _, time_opt = benchmark_function(find_duplicates_optimized, test_list)
    print(f"Optimized (set):            {time_opt:.6f} seconds")
    print(f"Speedup: {time_unopt/time_opt:.2f}x faster")
    
    # Example 3: Sum of Squares
    print("\n3. Sum of Squares (n=100000)")
    print("-" * 70)
    n = 100000
    
    _, time_unopt = benchmark_function(sum_squares_unoptimized, n)
    print(f"Unoptimized (list):         {time_unopt:.6f} seconds")
    
    _, time_opt = benchmark_function(sum_squares_optimized, n)
    print(f"Optimized (generator):      {time_opt:.6f} seconds")
    print(f"Speedup: {time_unopt/time_opt:.2f}x faster")
    
    # Example 4: String Building
    print("\n4. String Building (1000 words)")
    print("-" * 70)
    words = ["word"] * 1000
    
    _, time_unopt = benchmark_function(build_string_unoptimized, words)
    print(f"Unoptimized (concatenation): {time_unopt:.6f} seconds")
    
    _, time_opt = benchmark_function(build_string_optimized, words)
    print(f"Optimized (join):            {time_opt:.6f} seconds")
    print(f"Speedup: {time_unopt/time_opt:.2f}x faster")
    
    print("\n" + "=" * 70)
    print("OPTIMIZATION SUMMARY")
    print("=" * 70)
    print("Key Takeaways:")
    print("1. Choose the right algorithm (reduce time complexity)")
    print("2. Use appropriate data structures (set vs list)")
    print("3. Avoid redundant operations (caching, memoization)")
    print("4. Use built-in functions (they're optimized in C)")
    print("5. Consider memory vs speed tradeoffs")
    print("=" * 70)


if __name__ == "__main__":
    compare_optimizations()
