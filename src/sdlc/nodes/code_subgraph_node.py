from src.sdlc.states.states import State
from src.sdlc.graph.subgraph_builder import SubGraphBuilder
from src.sdlc import logger

class CoderSubgraphNode:
    """
    Node logic implementation.
    """
    def __init__(self,model):
        self.llm = model

    
    def process(self, state: State):
        """
        Processes the input state and generates code files based on design documents.
        """
        sub_graph_builder = SubGraphBuilder(self.llm)
        self.sub_graph = sub_graph_builder.setup_graph()
        
        design = state["design_summary"]
        # Now execute the subgraph
        response = self.sub_graph.invoke({"design_summary": design}) 
        logger.info("INVOKING SUBGRAPH FOR CODE GENERATION...")
        return response

    
