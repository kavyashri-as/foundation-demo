"""
Unit tests for optimization examples.
Tests ensure that optimized versions produce the same results as unoptimized versions.
"""

import unittest
from optimization_examples import (
    fibonacci_unoptimized,
    fibonacci_optimized,
    fibonacci_iterative,
    find_duplicates_unoptimized,
    find_duplicates_optimized,
    sum_squares_unoptimized,
    sum_squares_optimized,
    build_string_unoptimized,
    build_string_optimized,
    calculate_averages_unoptimized,
    calculate_averages_optimized,
    calculate_averages_most_optimized,
    count_frequencies_unoptimized,
    count_frequencies_optimized,
    count_frequencies_most_optimized,
    contains_negative_unoptimized,
    contains_negative_optimized,
    contains_negative_most_optimized,
    find_common_elements_unoptimized,
    find_common_elements_optimized,
)


class TestFibonacciOptimization(unittest.TestCase):
    """Test fibonacci optimization correctness."""
    
    def test_fibonacci_small_numbers(self):
        """Test that all fibonacci implementations produce same results for small numbers."""
        for n in range(10):
            unopt = fibonacci_unoptimized(n)
            opt = fibonacci_optimized(n)
            iter_result = fibonacci_iterative(n)
            
            self.assertEqual(unopt, opt, f"Memoized version differs at n={n}")
            self.assertEqual(unopt, iter_result, f"Iterative version differs at n={n}")
    
    def test_fibonacci_larger_numbers(self):
        """Test optimized versions for larger numbers (skip unoptimized as it's too slow)."""
        test_cases = [20, 30, 50]
        for n in test_cases:
            opt = fibonacci_optimized(n)
            iter_result = fibonacci_iterative(n)
            self.assertEqual(opt, iter_result, f"Versions differ at n={n}")
    
    def test_fibonacci_edge_cases(self):
        """Test edge cases."""
        self.assertEqual(fibonacci_iterative(0), 0)
        self.assertEqual(fibonacci_iterative(1), 1)


class TestFindDuplicatesOptimization(unittest.TestCase):
    """Test duplicate finding optimization."""
    
    def test_duplicates_same_results(self):
        """Test that both versions find the same duplicates."""
        test_cases = [
            [1, 2, 3, 2, 4, 3, 5],
            [1, 1, 1, 1],
            [1, 2, 3, 4, 5],  # No duplicates
            [],  # Empty list
            [5],  # Single element
        ]
        
        for numbers in test_cases:
            unopt = set(find_duplicates_unoptimized(numbers))
            opt = set(find_duplicates_optimized(numbers))
            self.assertEqual(unopt, opt, f"Results differ for {numbers}")
    
    def test_duplicates_large_list(self):
        """Test with larger list."""
        numbers = list(range(100)) * 2  # Each number appears twice
        unopt = set(find_duplicates_unoptimized(numbers))
        opt = set(find_duplicates_optimized(numbers))
        self.assertEqual(unopt, opt)
        self.assertEqual(len(opt), 100)


class TestSumSquaresOptimization(unittest.TestCase):
    """Test sum of squares optimization."""
    
    def test_sum_squares_same_results(self):
        """Test that both versions produce same results."""
        test_cases = [0, 1, 10, 100, 1000]
        
        for n in test_cases:
            unopt = sum_squares_unoptimized(n)
            opt = sum_squares_optimized(n)
            self.assertEqual(unopt, opt, f"Results differ for n={n}")
    
    def test_sum_squares_correctness(self):
        """Test correctness against known values."""
        # Sum of squares from 0 to 3: 0² + 1² + 2² + 3² = 0 + 1 + 4 + 9 = 14
        self.assertEqual(sum_squares_optimized(4), 14)


class TestStringBuildingOptimization(unittest.TestCase):
    """Test string building optimization."""
    
    def test_string_building_same_results(self):
        """Test that both versions produce same results."""
        test_cases = [
            ["hello", "world"],
            ["a", "b", "c", "d", "e"],
            ["single"],
            [],
        ]
        
        for words in test_cases:
            unopt = build_string_unoptimized(words)
            opt = build_string_optimized(words)
            self.assertEqual(unopt, opt, f"Results differ for {words}")
    
    def test_string_building_large_list(self):
        """Test with larger word list."""
        words = ["word"] * 100
        unopt = build_string_unoptimized(words)
        opt = build_string_optimized(words)
        self.assertEqual(unopt, opt)


class TestCalculateAveragesOptimization(unittest.TestCase):
    """Test average calculation optimization."""
    
    def test_averages_same_results(self):
        """Test that all versions produce same results."""
        test_cases = [
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[10], [20], [30]],
            [[1, 1, 1], [2, 2, 2]],
        ]
        
        for data in test_cases:
            unopt = calculate_averages_unoptimized(data)
            opt = calculate_averages_optimized(data)
            most_opt = calculate_averages_most_optimized(data)
            
            self.assertEqual(unopt, opt, f"Optimized differs for {data}")
            self.assertEqual(unopt, most_opt, f"Most optimized differs for {data}")
    
    def test_averages_correctness(self):
        """Test correctness against known values."""
        data = [[1, 2, 3], [10, 20]]
        result = calculate_averages_most_optimized(data)
        self.assertEqual(result, [2.0, 15.0])


class TestCountFrequenciesOptimization(unittest.TestCase):
    """Test frequency counting optimization."""
    
    def test_frequencies_same_results(self):
        """Test that all versions produce same results."""
        test_cases = [
            ["a", "b", "c", "a", "b", "a"],
            ["x", "x", "x", "x"],
            ["single"],
            [],
        ]
        
        for items in test_cases:
            unopt = count_frequencies_unoptimized(items)
            opt = count_frequencies_optimized(items)
            most_opt = count_frequencies_most_optimized(items)
            
            self.assertEqual(unopt, opt, f"Optimized differs for {items}")
            self.assertEqual(unopt, most_opt, f"Most optimized differs for {items}")
    
    def test_frequencies_correctness(self):
        """Test correctness against known values."""
        items = ["a", "b", "a", "c", "b", "a"]
        result = count_frequencies_most_optimized(items)
        expected = {"a": 3, "b": 2, "c": 1}
        self.assertEqual(result, expected)


class TestContainsNegativeOptimization(unittest.TestCase):
    """Test negative number detection optimization."""
    
    def test_contains_negative_same_results(self):
        """Test that all versions produce same results."""
        test_cases = [
            ([1, 2, 3, -1, 4], True),
            ([1, 2, 3, 4, 5], False),
            ([-1, -2, -3], True),
            ([0], False),
            ([], False),
        ]
        
        for numbers, expected in test_cases:
            unopt = contains_negative_unoptimized(numbers)
            opt = contains_negative_optimized(numbers)
            most_opt = contains_negative_most_optimized(numbers)
            
            self.assertEqual(unopt, expected, f"Unoptimized wrong for {numbers}")
            self.assertEqual(opt, expected, f"Optimized wrong for {numbers}")
            self.assertEqual(most_opt, expected, f"Most optimized wrong for {numbers}")


class TestFindCommonElementsOptimization(unittest.TestCase):
    """Test common elements finding optimization."""
    
    def test_common_elements_same_results(self):
        """Test that both versions find same common elements."""
        test_cases = [
            ([1, 2, 3, 4], [3, 4, 5, 6]),
            ([1, 2, 3], [4, 5, 6]),  # No common elements
            ([1, 1, 2, 2], [2, 2, 3, 3]),
            ([], [1, 2, 3]),
            ([1, 2, 3], []),
        ]
        
        for list1, list2 in test_cases:
            unopt = set(find_common_elements_unoptimized(list1, list2))
            opt = set(find_common_elements_optimized(list1, list2))
            self.assertEqual(unopt, opt, f"Results differ for {list1}, {list2}")
    
    def test_common_elements_correctness(self):
        """Test correctness against known values."""
        list1 = [1, 2, 3, 4, 5]
        list2 = [3, 4, 5, 6, 7]
        result = set(find_common_elements_optimized(list1, list2))
        expected = {3, 4, 5}
        self.assertEqual(result, expected)


class TestPerformanceImprovement(unittest.TestCase):
    """Test that optimized versions are indeed faster."""
    
    def test_fibonacci_performance(self):
        """Optimized fibonacci should be much faster."""
        import time
        
        n = 25
        
        # Optimized version
        start = time.perf_counter()
        fibonacci_optimized(n)
        opt_time = time.perf_counter() - start
        
        # Iterative version should be fastest
        start = time.perf_counter()
        fibonacci_iterative(n)
        iter_time = time.perf_counter() - start
        
        # Both should complete quickly (< 0.1 seconds)
        self.assertLess(opt_time, 0.1, "Optimized version too slow")
        self.assertLess(iter_time, 0.1, "Iterative version too slow")
    
    def test_duplicates_performance(self):
        """Optimized duplicate finding should be faster."""
        import time
        
        numbers = list(range(500)) * 2
        
        # Unoptimized version
        start = time.perf_counter()
        find_duplicates_unoptimized(numbers)
        unopt_time = time.perf_counter() - start
        
        # Optimized version
        start = time.perf_counter()
        find_duplicates_optimized(numbers)
        opt_time = time.perf_counter() - start
        
        # Optimized should be faster
        self.assertLess(opt_time, unopt_time, "Optimized version not faster")


if __name__ == "__main__":
    unittest.main()
