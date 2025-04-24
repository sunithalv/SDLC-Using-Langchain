from src.sdlc.states.states import CoderState
from src.sdlc.prompts.prompts import CODE_ORCHESTRATOR__INSTRNS
from src.sdlc.schema.codefiletypes import CodeFileTypes
from langgraph.constants import Send
from src.sdlc import logger

class CodeOrchestratorNode:
    """Orchestrator that generates an architecture plan for the code"""

    def __init__(self,model):
        # Augment the LLM with schema for structured output
        self.planner = model.with_structured_output(CodeFileTypes)

    def process(self, state: CoderState):
        """
        Processes the input state and generates code file types.
        """
        response= self.planner.invoke(CODE_ORCHESTRATOR__INSTRNS.format(design_documents=state["design_summary"]))
        logger.info(f"In orchestrator node, response is : {response.codefiletypes}")
        return {"codefiletypes":response.codefiletypes}
    
    # Conditional edge function to create code_generation_node workers that each write each code file
    def assign_workers(self,state: CoderState):
        """Assign a worker to each code file in the plan"""
        code_review=state.get('generated_code_review','')
        logger.info("In orchestrator node, assigning workers for code files...")
        # Kick off section writing in parallel via Send() API
        return [Send("code_generation_node", {"generated_code_review":code_review,
                                              "codefiletype": s}) for s in state["codefiletypes"]]
    
