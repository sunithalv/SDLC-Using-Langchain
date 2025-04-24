from src.sdlc.states.states import State
from langgraph.graph import END
from langgraph.types import interrupt
from src.sdlc import logger

class DesignDocumentsFeedback:
    """
    Node logic implementation.
    """
    def process(self, state: State):
        """ No-op node that should be interrupted on """
        logger.info("[DEBUG] Entering human_fb_design process")
        human_design_review = interrupt(
        {
          "design_documents_review": state.get('design_documents_review', "")
        }
        )
        # Update the state with the human's input or route the graph based on the input.
        logger.info(f"RESUMING DESIGN FEEDBACK NODE, feedback received : {human_design_review}")
        return {
            "design_documents_review": human_design_review
        }
    
    def design_document_review(self,state: State):
        """ Return the next node to execute """
        # Check if human feedback
        design_review=state.get('design_documents_review', "")
        logger.info("IN DESIGN REVIEW, determining flow based on design review...")
        if design_review:
            return "design_documents_generator"
        
        # Otherwise summarize design docs
        else:
            return "design_summarizer"

