from src.sdlc.states.states import State
from langgraph.graph import END
from langgraph.types import interrupt
from src.sdlc import logger

class QAFeedback:
    """
    Node logic implementation.
    """
    def process(self, state: State):
        """ No-op node that should be interrupted on """
        logger.info("[DEBUG] Entering human_fb_qatesting process")
        qa_result = interrupt(
        {
          "qa_result": state.get('qa_testing', "")
        }
        )
        # Update the state with the human's input or route the graph based on the input.
        logger.info(f"RESUMING QATESTING FEEDBACK NODE ,qa etsting result : {qa_result['result']}")
        return {
            "qa_status": qa_result["result"]
        }
    
    def check_qa_response(self,state):
        qa_status=state.get("qa_status","")
        if qa_status=="Passed":
            return "deployment_node"
        else:
            return "coder_subgraph"