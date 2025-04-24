from src.sdlc.states.states import State
from src.sdlc.prompts.prompts import TESTCASES_GEN_INSTRNS
from src.sdlc import logger

class TestCasesNode:
    """
    Node logic implementation.
    """
    def __init__(self,model):
        self.llm = model

    def process(self, state: State):
        """
        Processes the input state and generates test cases for the code
        """
        design_summary=state.get('design_summary', '')        
        response=self.llm.invoke(TESTCASES_GEN_INSTRNS.format(design_documents=design_summary))
        logger.info("In TEST CASES NODE received response")
        return {"test_cases":response.content}


    

    
