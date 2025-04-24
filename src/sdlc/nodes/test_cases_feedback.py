from src.sdlc.states.states import State
from langgraph.graph import END
from langgraph.types import interrupt
from src.sdlc import logger

class TestCasesFeedback:
    """
    Node logic implementation.
    """

    def process(self, state: State):
        """ No-op node that should be interrupted on """
        logger.info("[DEBUG] Entering human_fb_testcases process")
        human_testcases_review = interrupt(
        {
          "test_cases_review": state.get("test_cases_review","")
        }
        )
        # Update the state with the human's input or route the graph based on the input.
        logger.info(f'RESUMING TEST CASES FEEDBACK NODE, feedback received : {human_testcases_review}')
        return {
            "test_cases_review": human_testcases_review
        }
    
    def testcase_review(self,state: State):
        """ Return the next node to execute """
        # Check if human feedback
        test_cases_review=state.get('test_cases_review', "")
        logger.info("IN TEST CASE REVIEW,determining flow...")
        if test_cases_review:
            return "test_cases_generator"
        
        # Otherwise 
        return "qa_testing_node"

