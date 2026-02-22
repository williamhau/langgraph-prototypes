# Unit Test Generator

A LangGraph-based tool that automatically generates unit tests for Python modules, runs them, and iteratively fixes them until they pass.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your API key
```

## Usage

```bash
python main.py --project-path /path/to/your/python/project
```

## Architecture

- `graph.py`: LangGraph workflow definition
- `nodes.py`: Individual node implementations
- `state.py`: State schema definition
- `main.py`: Entry point


## Example Output

```
Starting test generation for: ./sample_project
Max retries per module: 3

Found 2 modules to test

Processing: ./sample_project/calculator.py
  ✅ Test passed

Processing: ./sample_project/string_utils.py
  ❌ Test failed (attempt 1)
  ✅ Test passed

✨ Test generation complete!
```

## Project Structure

```
unit-generator/
├── graph.py              # LangGraph workflow definition
├── nodes.py              # Node implementations (load, generate, test, retry)
├── state.py              # State schema
├── main.py               # CLI entry point
├── requirements.txt      # Dependencies
├── setup.sh              # Quick setup script
├── .env.example          # Environment template
├── ARCHITECTURE.md       # Workflow documentation
└── sample_project/       # Demo Python project
    ├── calculator.py
    └── string_utils.py
```

## How It Works

1. **Load**: Discovers all Python modules in target project
2. **Generate**: LLM creates unit tests for each module
3. **Run**: Executes tests with pytest
4. **Retry**: If tests fail, feeds errors back to LLM for fixes
5. **Save**: Stores passing tests in `tests/` directory
6. **Repeat**: Continues until all modules processed
