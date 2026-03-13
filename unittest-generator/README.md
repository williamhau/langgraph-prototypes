## Unittest Generator

A small tool that walks a Python project, uses an LLM to generate `pytest`-based unit tests for each module, and runs them with automatic retries for failing tests. It is implemented as a LangGraph workflow.

### Requirements

- **Python**: 3.9+ recommended  
- **LLM access**:
  - `OPENAI_API_KEY` (optional, currently commented out in code), and/or
  - `GOOGLE_API_KEY` (used for Gemini via `langchain-google-genai` / `google-generativeai`)

Python dependencies are listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file inside `unittest-generator` (same directory as `main.py`) with your keys:

```env
OPENAI_API_KEY=your-openai-key
GOOGLE_API_KEY=your-google-api-key
```

`main.py` will load `.env` and verify that `OPENAI_API_KEY` is present before running.

### Installation

From the project root:

```bash
cd unittest-generator
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Usage

Run the generator by pointing it at a Python project:

```bash
python main.py --project-path /path/to/your/python/project --max-retries 2
```

- **`--project-path`**: root directory of the target Python project.  
- **`--max-retries`**: how many times to regenerate tests for a module if the tests fail (default: 2).

During execution you will see:

- Confirmation that the API key was found.  
- How many modules were discovered.  
- Per-module status, including whether tests passed or failed on each attempt.

Generated tests are written under a `tests/` directory inside the target project, with filenames like:

```text
tests/test_<module_name>.py
```

### How it works

- **`graph.py`** defines a LangGraph `StateGraph` with the main workflow.  
- **`state.py`** defines the `TestGenerationState` structure.  
- **`nodes.py`** contains the node functions that:
  - Discover Python modules under `project_path`.
  - Ask the LLM to generate or fix tests using Gemini (`gemini-2.5-flash`).
  - Save the generated tests.
  - Run `pytest` on the tests and capture errors.
  - Decide whether to retry, skip, or move on to the next module.

### Notes and limitations

- Generated tests may need manual review and cleanup.  
- Complex projects (custom imports, heavy I/O, external services) might require editing prompts or adding mocks.  
- Adjust the model, temperature, or prompts in `nodes.py` if you want different test styles or verbosity.

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
