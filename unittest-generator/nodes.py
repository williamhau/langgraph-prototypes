import os
import subprocess
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.messages import SystemMessage,  AIMessage

#os.environ["GOOGLE_API_KEY"] = ""
import google.generativeai as genai

#llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)


llm = ChatGoogleGenerativeAI(           
    model="gemini-2.5-flash", # Use a current model
    version="v1",             # Force stable API version
    temperature=0
)
def load_modules(state):
    """Load all Python modules from the project."""
    project_path = Path(state["project_path"])
    modules = []
    
    for py_file in project_path.rglob("*.py"):
        if "test_" not in py_file.name and "__pycache__" not in str(py_file):
            modules.append(str(py_file))
    
    return {"modules": modules, "completed_modules": []}

def select_next_module(state):
    """Select the next module to process."""
    remaining = [m for m in state["modules"] if m not in state["completed_modules"]]
    
    if not remaining:
        return {"current_module": None}
    
    current = remaining[0]
    with open(current, "r") as f:
        code = f.read()
    
    return {
        "current_module": current,
        "module_code": code,
        "test_code": None,
        "test_errors": None,
        "retry_count": 0
    }

def generate_test(state):
    """Generate unit test using LLM."""
    module_code = state["module_code"]
    test_errors = state.get("test_errors")
    
    if test_errors:
        prompt = f"""The previous test failed with these errors:
{test_errors}

Original module code:
```python
{module_code}
```

Previous test code:
```python
{state["test_code"]}
```

Fix the test code to resolve these errors. Return ONLY the corrected test code."""
    else:
        prompt = f"""Generate comprehensive unit tests for this Python module:

```python
{module_code}
```

Requirements:
- Use pytest
- Import the module correctly
- Test all functions/classes
- Use mocks if needed
- Return ONLY the test code, no explanations"""
    
    messages = [
        SystemMessage(content="You are an expert Python test engineer."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    test_code = response.content.strip()
    
    # Clean markdown code blocks
    if test_code.startswith("```"):
        lines = test_code.split("\n")
        test_code = "\n".join(lines[1:-1])
    
    return {"test_code": test_code}

def run_test(state):
    """Run the generated test and capture results."""
    current_module = state["current_module"]
    test_code = state["test_code"]
    
    # Create test file path
    module_path = Path(current_module)
    project_path = Path(state["project_path"])
    test_dir = project_path / "tests"
    test_dir.mkdir(exist_ok=True)
    
    # Preserve directory structure
    rel_path = module_path.relative_to(project_path)
    test_file = test_dir / f"test_{rel_path.name}"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write test file
    with open(test_file, "w") as f:
        f.write(test_code)
    
    # Run pytest
    result = subprocess.run(
        ["python", "-m", "pytest", str(test_file), "-v"],
        cwd=str(project_path),
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return {
            "test_errors": None,
            "completed_modules": state["completed_modules"] + [current_module]
        }
    else:
        return {
            "test_errors": result.stdout + "\n" + result.stderr,
            "retry_count": state["retry_count"] + 1
        }

def should_retry(state):
    """Decide whether to retry test generation."""
    if state.get("test_errors") and state["retry_count"] < state["max_retries"]:
        return "retry"
    elif state.get("test_errors"):
        # Max retries reached, mark as completed anyway
        return "skip"
    else:
        return "next"

def mark_completed(state):
    """Mark current module as completed even if tests failed."""
    return {"completed_modules": state["completed_modules"] + [state["current_module"]]}

def check_completion(state):
    """Check if all modules are processed."""
    if len(state["completed_modules"]) >= len(state["modules"]):
        return "done"
    return "continue"
