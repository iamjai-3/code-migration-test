# Code Migration Tool

A tool for migrating code between different programming languages.

## Installation

```bash
poetry install
```

## Usage

```bash
python main.py input.zip input_language target_language
```

### Arguments:

- `input.zip`: Path to the zip file containing your source code
- `input_language`: Source code language (e.g., php, python, java)
- `target_language`: Target language to migrate to (e.g., node, python, java)

### Example:

```bash
# Migrate PHP code to Node.js
python main.py my_php_app.zip php node

# Migrate Python code to Java
python main.py python_app.zip python java
```

### Supported Languages:

- Input: PHP, Python, JavaScript, Java, TypeScript, Ruby, Go, C#, C++, C
- Output: Node.js, Python, Java (more coming soon)

## Requirements

- Python 3.8+
- Poetry
- Anthropic API key (set as ANTHROPIC_API_KEY environment variable)

## Output

The converted code will be placed in the `output` directory. The directory structure will mirror the input project's structure.
