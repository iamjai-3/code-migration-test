# Test Migration Tool

A tool for migrating code between different programming languages.

## Installation

```bash
poetry install
```

## Usage

1. Set up your environment variables:

   ```bash
   cp .env.example .env
   # Edit .env with your ANTHROPIC_API_KEY
   ```

2. Run the migration:
   ```bash
   poetry run migrate
   ```

## Development

```bash
# Install dev dependencies
poetry install --with dev

# Run tests
poetry run pytest
```
