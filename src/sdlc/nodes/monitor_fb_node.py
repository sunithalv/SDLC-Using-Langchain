from src.sdlc.states.states import State
from langgraph.graph import END
from langgraph.types import interrupt
from src.sdlc import logger

class MonitorFeedback:
    """
    Node logic implementation.
    """

    def process(self, state: State):
        """ No-op node that should be interrupted on """
        logger.info("[DEBUG] Entering human_fb_monitoring process")

        human_monitoring_fb= interrupt(
        {
          "monitoring_and_feedback_review": state.get('monitoring_and_feedback_review', "")
        }
        )
        # Update the state with the human's input or route the graph based on the input.
        logger.info(f"RESUMING MONITORING FEEDBACK NODE,feedback received : {human_monitoring_fb}")
        
        return {
            "monitoring_and_feedback_review": human_monitoring_fb
        }
    

