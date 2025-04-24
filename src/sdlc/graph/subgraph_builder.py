from langgraph.graph import StateGraph, START,END
from src.sdlc.states.states import CoderState
from src.sdlc.nodes.code_orchestrator import CodeOrchestratorNode
from src.sdlc.nodes.code_generation_node import CodeGenerationNode
from src.sdlc.nodes.synthesizer_node import SynthesizerNode
from src.sdlc.nodes.code_reviewer_node import CodeReviewerNode

class SubGraphBuilder:

    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(CoderState)

    def build_graph(self):
        """
        Builds a subgraph for code generation. 
        """
        self.code_orchestrator_node=CodeOrchestratorNode(self.llm)
        self.code_generation_node=CodeGenerationNode(self.llm)
        self.synthesizer_node=SynthesizerNode(self.llm)
        self.code_reviewer_node=CodeReviewerNode(self.llm)
        
        self.graph_builder.add_node("code_orchestrator",self.code_orchestrator_node.process)
        self.graph_builder.add_node("code_generation_node", self.code_generation_node.process)
        self.graph_builder.add_node("code_synthesizer",self.synthesizer_node.process)
        self.graph_builder.add_node("code_reviewer",self.code_reviewer_node.process)
    

        self.graph_builder.add_edge(START,"code_orchestrator")
        self.graph_builder.add_conditional_edges("code_orchestrator", 
                                                 self.code_orchestrator_node.assign_workers, 
                                                 path_map=["code_generation_node"])
        self.graph_builder.add_edge("code_generation_node", "code_synthesizer")
        self.graph_builder.add_edge("code_synthesizer", "code_reviewer")
        self.graph_builder.add_edge("code_reviewer", END)
        

    def setup_graph(self):
        """
        Sets up the graph 
        """
        self.build_graph()
        return self.graph_builder.compile()

    





    
