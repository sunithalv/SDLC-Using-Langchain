from src.sdlc.states.states import State
from langgraph.graph import END
from langgraph.types import interrupt
from src.sdlc import logger

class UserStoriesFeedback:
    """
    Node logic implementation.
    """

    def process(self, state: State):
        """ No-op node that should be interrupted on """
        logger.info("[DEBUG] Entering human_fb_user stories process")

        human_userstory_review = interrupt(
        {
          "user_stories_review": state.get('user_stories_review', "")
        }
        )
        # Update the state with the human's input or route the graph based on the input.
        logger.info(f'RESUMING HUMAN USERSTORIES FEEDBACK NODE, feedback is : {human_userstory_review}')
        
        return {
            "user_stories_review": human_userstory_review
        }
    
    def user_story_review(self,state: State):
        """ Return the next node to execute """
        # Check if human feedback
        user_stories_review=state.get('user_stories_review', "")
        logger.info("IN USER STORY REVIEW,determining flow...")
        if user_stories_review:
            return "userstories_generator"
        
        # Otherwise design_documents_node
        return "design_documents_generator"

