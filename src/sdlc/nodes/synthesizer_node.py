from src.sdlc.states.states import CoderState
from src.sdlc.prompts.prompts import FILE_MODIFY_INSTRNS
from src.sdlc.schema.codefiletypes import CodeFileTypes
from src.sdlc import logger

class SynthesizerNode:
    """Node logic implementation for synthesizing full code from multiple files."""

    def __init__(self, model):
        self.llm = model.with_structured_output(CodeFileTypes)

    def process(self, state: CoderState):
        """Synthesize full code from multiple generated files."""
        #expected_files = state["codefiletypes"]  # List of expected file types
        generated_files = state.get("generated_files", [])

        logger.info(f"IN code_synthesizer, generated code files : {generated_files}")

        # Wait for all expected files before proceeding
        # if len(generated_files) < len(expected_files):
        #     print(f"⚠️ Waiting for all generated files. Current: {len(generated_files)}, Expected: {len(expected_files)}")
        #     return  # Do nothing, let LangGraph retry when more data arrives

        # Convert to dictionary format: {filename: code}
        generated_code = {code_file.name: code_file.code for code_file in generated_files}

        return {"generated_code": generated_code}
