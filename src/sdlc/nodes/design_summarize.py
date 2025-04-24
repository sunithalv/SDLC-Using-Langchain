from src.sdlc.states.states import State
from src.sdlc.prompts.prompts import SUMMARIZE_DESIGN_DOCS
from src.sdlc import logger

class DesignSummarizeNode:
    """
    Node logic implementation.
    """
    def __init__(self,model):
        self.llm = model

    def process(self, state: State):
        """
        Processes the input state and generates design document based on user stories.
        """
        #Summarize the design documents for the code generation
        summarized_docs=self.llm.invoke(SUMMARIZE_DESIGN_DOCS.format(design_documents=state["design_documents"]))
        logger.info(f"In DESIGN SUMMARIZN NODE,response received  : {summarized_docs.content}")
        return {"design_summary": summarized_docs.content}
    
