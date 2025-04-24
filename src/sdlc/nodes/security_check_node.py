from src.sdlc.states.states import State
from src.sdlc.prompts.prompts import SECURITY_REVIEW_INSTRNS
from src.sdlc import logger

class SecurityCheckNode:
    """
    Node logic implementation.
    """
    def __init__(self,model):
        self.llm = model

    def process(self, state: State):
        """
        Processes the input state and reviews the code for security.
        """
        generated_code=state.get('generated_code', '')
        
        response=self.llm.invoke(SECURITY_REVIEW_INSTRNS.format(generated_code=generated_code))
        logger.info("In SECURITY CHECK NODE,received response")
        return {"security_check":response.content}


    

    
