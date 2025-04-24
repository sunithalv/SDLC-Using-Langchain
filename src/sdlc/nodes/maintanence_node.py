from src.sdlc.states.states import State
from src.sdlc.prompts.prompts import MAINTANENCE_INSTRNS
from src.sdlc import logger

class MaintanenceNode:
    """
    Node logic implementation.
    """
    def __init__(self,model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates maintanence instructions based on design.
        """
        monitoring_feedback=state.get('monitoring_and_feedback_review', '')
        response=self.llm.invoke(MAINTANENCE_INSTRNS.format(user_feedback=monitoring_feedback))
        logger.info(f"In MAINTANENCE NODE, received response")
        return {"maintanence_and_updates":response.content}
    
