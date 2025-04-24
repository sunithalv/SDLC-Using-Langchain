from src.sdlc.states.states import State
from langgraph.graph import END
from langgraph.types import interrupt
from src.sdlc import logger

class CodeFeedback:
    """
    Node logic implementation matching your working UserStoriesFeedback pattern
    """

    def process(self, state: State):
        """No-op node that gets interrupted"""
        
        logger.info("[DEBUG] Entering human_fb_code process")
        human_code_review = interrupt(
        {
          "generated_code_review": state.get("generated_code_review","")
        }
        )
        # Update the state with the human's input or route the graph based on the input.
        logger.info(f"[DEBUG] Resuming human_fb_code process.Received code review : {human_code_review}")

        return {
            "generated_code_review": human_code_review
        }
    
    # def code_file_review(self, state: State):
    #     """Return the next node to execute based on review status"""
    #     code_review = state.get('generated_code_review', '')
    #     print("IN CODE REVIEW of Code Feedback:", code_review)
        
    #     # If we have review data, decide next step
    #     if code_review:
    #         # Assuming code_review is a dict with an 'approved' flag
    #         # if code_review.get('approved', False):
    #         #     return END  # Proceed to end if approved
    #         print("Interrupting human feedback")
    #         return "human_fb_code"  # Return for revisions if not approved
        
    #     # Default path when no review exists yet
    #     return "security_review_node"
    
