# foundation-demo
# foundation-demo
New Edits in this read me file
This repository demonstrates foundational concepts for application development.

## Features
- Basic project structure
- Sample code for getting started
- Instructions for building and running the project
- **Search Feature**: Powerful text search utility for finding content across files

## Getting Started
1. Clone the repository:
   ```sh
   git clone https://github.com/Hemavathi15sg/foundation-demo.git
   ```
2. Navigate to the project directory:
   ```sh
   cd foundation-demo
   ```
3. Install dependencies:
   ```sh
   <package manager> install
   ```
4. Run the application:
   ```sh
   <language> main.<ext>
   ```

## Dependencies
- Uses <package manager> for <language> dependencies.

## Contributing
- Fork the repo and submit pull requests.
- Open issues for bugs or feature requests.

## License
- MIT License

## Search Feature

The repository includes a powerful search utility (`search.py`) that allows you to find text patterns across all files in the repository.

### Usage

Basic search (case-insensitive):
```sh
python search.py "search term"
```

Case-sensitive search:
```sh
python search.py "SearchTerm" -c
```

Regex pattern matching:
```sh
python search.py "pattern.*regex" -p
```

Search in a specific directory:
```sh
python search.py "term" -d ./folder1
```

### Features
- Recursive file search through all directories
- Case-sensitive and case-insensitive search modes
- Regular expression pattern matching support
- Excludes common directories (.git, node_modules, etc.)
- Shows line numbers and content for each match
- Summary of total matches and files found
