from typing import TypedDict, List, Optional

class TestGenerationState(TypedDict):
    project_path: str
    modules: List[str]
    current_module: Optional[str]
    module_code: Optional[str]
    test_code: Optional[str]
    test_errors: Optional[str]
    retry_count: int
    max_retries: int
    completed_modules: List[str]
