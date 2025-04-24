from src.sdlc.states.states import State
from src.sdlc.prompts.prompts import USERSTORY_GEN_INSTRNS,USERSTORY_MODIFY_INSTRNS
from src.sdlc import logger

class UserStoriesNode:
    """
    Node logic implementation.
    """
    def __init__(self,model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates user stories based on user requirements.
        """
        user_stories_review=state.get('user_stories_review', '')
        user_stories=state.get('user_stories', '')
        if user_stories_review:
            response=self.llm.invoke(USERSTORY_MODIFY_INSTRNS.format(user_stories_review=user_stories_review,
                                                            user_stories=user_stories))
            logger.info("IN MODIFY USER STORIES")
        else:
            response=self.llm.invoke(USERSTORY_GEN_INSTRNS.format(user_requirements=state["user_requirements"],
                                                            user_stories=user_stories))
            logger.info("In GENERATE USER STORIES...")
        return {"user_stories":response.content}
    
