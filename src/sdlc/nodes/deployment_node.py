from src.sdlc.states.states import State
from src.sdlc.prompts.prompts import DEPLOYMENT_INSTRUCTIONS
from src.sdlc import logger

class DeploymentNode:
    """
    Node logic implementation.
    """
    def __init__(self,model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates deployment instructions based on design document.
        """
        design_summary=state.get('design_summary', '')
        response=self.llm.invoke(DEPLOYMENT_INSTRUCTIONS.format(design_document=design_summary))
        logger.info(f"In DEPLOYMENT NODE ,response received")
        return {"deployment":response.content}
    
