from typing import Annotated, Literal, Optional
from typing_extensions import TypedDict
from typing import TypedDict, Annotated, List,Dict
from src.sdlc.schema.codefiletypes import CodeFileType
from src.sdlc.schema.codefiles import CodeFile
import operator

class State(TypedDict):
    user_requirements:str
    user_stories:str
    user_stories_review:str
    design_documents:str
    design_documents_review:str
    design_summary:str
    codefiletypes: List[CodeFileType]
    generated_files: Annotated[
        List[CodeFile], operator.add
    ]  # All workers write to this key in parallel
    generated_code: Dict 
    generated_code_review:str
    security_check:str
    security_check_review:str
    test_cases:str
    test_cases_review:str
    qa_testing:Dict
    qa_status:str
    deployment:str
    monitoring_and_feedback:str
    monitoring_and_feedback_review:str
    maintanence_and_updates:str
    consolidated_artifacts:Dict

# Subgraph state
class CoderState(TypedDict):
    design_summary:str
    codefiletypes: List[CodeFileType]
    generated_files: Annotated[
        List[CodeFile], operator.add
    ]  # All workers write to this key in parallel
    generated_code: Dict 
    generated_code_review:str
    security_review:str


# Worker state
class WorkerState(TypedDict):
    codefiletype: CodeFileType
    code_review:str
    security_review:str
    generated_files: Annotated[List[CodeFile], operator.add]