from src.sdlc.states.states import WorkerState
from src.sdlc.prompts.prompts import CODE_GEN_INSTRUCTIONS
from src.sdlc.schema.codefiles import CodeFile
from src.sdlc import logger

class CodeGenerationNode:
    """
    Node logic implementation to generate code for each code file type from orchestrator.
    """
    def __init__(self,model):
        self.llm=model.with_structured_output(CodeFile)

    def process(self, state: WorkerState) -> dict:
        """
        Processes the input state and generates code files.
        """
        code_review=state.get('generated_code_review', '')
        code_file=self.llm.invoke(CODE_GEN_INSTRUCTIONS.format(code_review=code_review,
                                                         codefilename=state['codefiletype'].name,
                                                         codefiledescription=state['codefiletype'].description))
        logger.info(f"In Code generation node for code file : {state['codefiletype'].name}")
        return {"generated_files": [code_file]}

