from src.sdlc.states.states import State
from src.sdlc import logger

class ConsolidatedNode:
    """
    Node logic implementation.
    """

    def process(self, state: State) -> dict:
        """
        Gets all artifacts from state to display.
        """
        logger.info("IN CONSOLIDATED NODE,displaying artifacts...")
        return {"consolidated_artifacts":"Display artifacts"}
    
