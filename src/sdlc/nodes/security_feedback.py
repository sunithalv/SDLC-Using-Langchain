from src.sdlc.states.states import State
from langgraph.graph import END
from langgraph.types import interrupt
from src.sdlc import logger

class SecurityReviewFeedback:
    """
    Node logic implementation.
    """

    def process(self, state: State):
        """ No-op node that should be interrupted on """
        logger.info("[DEBUG] Entering human_fb_review process")
        human_security_review = interrupt(
        {
          "security_check_review": state.get("security_check_review","")
        }
        )
        # Update the state with the human's input or route the graph based on the input.
        logger.info(f'RESUMING SECURITY FEEDBACK NODE, feedback is {human_security_review}')
        return {
            "security_check_review": human_security_review
        }
    
    def security_review(self,state: State):
        """ Return the next node to execute """
        # Check if human feedback
        security_check_review=state.get('security_check_review', "")
        logger.info("IN SECURITY REVIEW, determining flow...")
        if security_check_review:
            return "security_check_generator"
        
        # Otherwise 
        return "test_cases_generator"

