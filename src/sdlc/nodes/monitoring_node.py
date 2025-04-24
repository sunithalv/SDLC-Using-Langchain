from src.sdlc.states.states import State
from src.sdlc.prompts.prompts import MONITORING_FB_INSTRNS
from src.sdlc import logger

class MonitoringNode:
    """
    Node logic implementation.
    """
    def __init__(self,model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates monitoring and feedback instructions based on deployment.
        """
        deployment_instructions=state.get('deployment', '')
        response=self.llm.invoke(MONITORING_FB_INSTRNS.format(deployment_instructions=deployment_instructions))
        logger.info(f"In GEN MONITORING AND FEEDBACK INSTRUCTIONS,response received...")
        return {"monitoring_and_feedback":response.content}
    
