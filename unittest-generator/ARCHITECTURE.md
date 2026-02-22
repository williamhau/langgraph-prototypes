# Workflow Architecture

## LangGraph Flow

```
START
  ↓
load_modules (scan project for .py files)
  ↓
select_next_module (pick next unprocessed module)
  ↓
  ├─→ [no modules left] → END
  └─→ [module found]
      ↓
    generate_test (LLM generates unit test)
      ↓
    run_test (execute pytest)
      ↓
      ├─→ [test passed] → select_next_module
      ├─→ [test failed & retries < max] → generate_test (with error feedback)
      └─→ [test failed & retries >= max] → mark_completed → select_next_module
```

## State Schema

- `project_path`: Target Python project directory
- `modules`: List of all Python files to test
- `current_module`: Currently processing module
- `module_code`: Source code of current module
- `test_code`: Generated test code
- `test_errors`: Error output from failed tests
- `retry_count`: Number of retry attempts
- `max_retries`: Maximum allowed retries
- `completed_modules`: List of processed modules

## Key Features

1. **Automatic Discovery**: Scans project for all Python modules
2. **Iterative Fixing**: Feeds test errors back to LLM for corrections
3. **Retry Logic**: Attempts up to N times before moving on
4. **Proper Structure**: Saves tests in `tests/` directory with proper naming
5. **Progress Tracking**: Shows real-time status of test generation
