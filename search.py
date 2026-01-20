#!/usr/bin/env python3
"""
Search Utility for Foundation Demo Repository
Provides text search functionality across files in the repository.
"""

import os
import sys
import argparse
import re
from pathlib import Path


class SearchEngine:
    """Search engine for finding text patterns in files."""
    
    def __init__(self, case_sensitive=False, pattern_mode=False):
        """
        Initialize the search engine.
        
        Args:
            case_sensitive (bool): Whether to perform case-sensitive search
            pattern_mode (bool): Whether to use regex pattern matching
        """
        self.case_sensitive = case_sensitive
        self.pattern_mode = pattern_mode
    
    def search_in_file(self, filepath, search_term):
        """
        Search for a term in a specific file.
        
        Args:
            filepath (Path): Path to the file to search
            search_term (str): Term to search for
            
        Returns:
            list: List of tuples (line_number, line_content) for matches
        """
        matches = []
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    if self.pattern_mode:
                        flags = 0 if self.case_sensitive else re.IGNORECASE
                        if re.search(search_term, line, flags):
                            matches.append((line_num, line.rstrip()))
                    else:
                        search_line = line if self.case_sensitive else line.lower()
                        search_target = search_term if self.case_sensitive else search_term.lower()
                        if search_target in search_line:
                            matches.append((line_num, line.rstrip()))
        except (PermissionError, UnicodeDecodeError, IOError):
            # Skip files that can't be read due to permissions or encoding issues
            pass
        
        return matches
    
    def search_directory(self, directory, search_term, exclude_dirs=None):
        """
        Search for a term in all files within a directory recursively.
        
        Args:
            directory (str): Directory path to search in
            search_term (str): Term to search for
            exclude_dirs (set): Set of directory names to exclude
            
        Returns:
            dict: Dictionary mapping file paths to their matches
        """
        if exclude_dirs is None:
            exclude_dirs = {'.git', '.github', '__pycache__', 'node_modules', '.venv', 'venv'}
        
        results = {}
        directory_path = Path(directory)
        
        for root, dirs, files in os.walk(directory_path):
            # Remove excluded directories from the walk
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for filename in files:
                filepath = Path(root) / filename
                matches = self.search_in_file(filepath, search_term)
                if matches:
                    results[str(filepath)] = matches
        
        return results
    
    def format_results(self, results):
        """
        Format search results for display.
        
        Args:
            results (dict): Search results dictionary
            
        Returns:
            str: Formatted results string
        """
        if not results:
            return "No matches found."
        
        output = []
        total_matches = 0
        
        for filepath, matches in sorted(results.items()):
            output.append(f"\n{filepath}:")
            for line_num, line_content in matches:
                output.append(f"  {line_num}: {line_content}")
                total_matches += 1
        
        output.insert(0, f"Found {total_matches} match(es) in {len(results)} file(s):")
        return "\n".join(output)


def main():
    """Main entry point for the search utility."""
    parser = argparse.ArgumentParser(
        description='Search for text patterns in files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python search.py "hello"                    # Case-insensitive search
  python search.py "Hello" -c                 # Case-sensitive search
  python search.py "hel.*world" -p            # Regex pattern search
  python search.py "test" -d ./folder1        # Search in specific directory
        """
    )
    
    parser.add_argument('search_term', help='Text or pattern to search for')
    parser.add_argument('-c', '--case-sensitive', action='store_true',
                        help='Perform case-sensitive search')
    parser.add_argument('-p', '--pattern', action='store_true',
                        help='Treat search term as a regex pattern')
    parser.add_argument('-d', '--directory', default='.',
                        help='Directory to search in (default: current directory)')
    
    args = parser.parse_args()
    
    # Initialize search engine
    search_engine = SearchEngine(
        case_sensitive=args.case_sensitive,
        pattern_mode=args.pattern
    )
    
    # Perform search
    print(f"Searching for: '{args.search_term}' in {args.directory}")
    if args.case_sensitive:
        print("Mode: Case-sensitive")
    if args.pattern:
        print("Mode: Regex pattern matching")
    
    results = search_engine.search_directory(args.directory, args.search_term)
    
    # Display results
    print(search_engine.format_results(results))
    
    # Return appropriate exit code
    return 0 if results else 1


if __name__ == '__main__':
    sys.exit(main())
