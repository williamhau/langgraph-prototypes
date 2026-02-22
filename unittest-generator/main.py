import argparse
import os
from pathlib import Path
from dotenv import load_dotenv
from graph import create_graph

def main():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    key = os.getenv("OPENAI_API_KEY")
    
    if key:
        print("✅ Success! API Key found.")
    else:
        print("❌ Failure. API Key is None. Check your .env file location.")    
    parser = argparse.ArgumentParser(description="Generate unit tests for Python projects")
    parser.add_argument("--project-path", required=True, help="Path to the Python project")
    parser.add_argument("--max-retries", type=int, default=2, help="Max retry attempts per test")
    args = parser.parse_args()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment")
        return
    
    graph = create_graph()
    
    initial_state = {
        "project_path": args.project_path,
        "modules": [],
        "current_module": None,
        "module_code": None,
        "test_code": None,
        "test_errors": None,
        "retry_count": 0,
        "max_retries": args.max_retries,
        "completed_modules": []
    }
    
    print(f"Starting test generation for: {args.project_path}")
    print(f"Max retries per module: {args.max_retries}\n")
    
    for state in graph.stream(initial_state):
        node_name = list(state.keys())[0]
        node_state = state[node_name]
        
        if node_name == "load_modules":
            print(f"Found {len(node_state['modules'])} modules to test")
        elif node_name == "select_next_module" and node_state.get("current_module"):
            print(f"\nProcessing: {node_state['current_module']}")
        elif node_name == "run_test":
            if node_state.get("test_errors"):
                print(f"  ❌ Test failed (attempt {node_state['retry_count']})")
            else:
                print(f"  ✅ Test passed")
    
    print("\n✨ Test generation complete!")

if __name__ == "__main__":
    main()
