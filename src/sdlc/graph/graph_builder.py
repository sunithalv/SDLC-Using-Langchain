from langgraph.graph import StateGraph, START,END
from langgraph.checkpoint.memory import MemorySaver
from src.sdlc.states.states import State
from src.sdlc.nodes.userstories_node import UserStoriesNode
from src.sdlc.nodes.userstories_feedback import UserStoriesFeedback
from src.sdlc.nodes.design_documents_node import DesignDocumentsNode
from src.sdlc.nodes.design_documents_feedback import DesignDocumentsFeedback
from src.sdlc.nodes.design_summarize import DesignSummarizeNode
from src.sdlc.nodes.code_subgraph_node import CoderSubgraphNode
from src.sdlc.nodes.code_feedback import CodeFeedback
from src.sdlc.nodes.security_check_node import SecurityCheckNode
from src.sdlc.nodes.security_feedback import SecurityReviewFeedback
from src.sdlc.nodes.test_cases_node import TestCasesNode
from src.sdlc.nodes.test_cases_feedback import TestCasesFeedback
from src.sdlc.nodes.qatesting_node import QATestingNode
from src.sdlc.nodes.qa_feedback import QAFeedback
from src.sdlc.nodes.deployment_node import DeploymentNode
from src.sdlc.nodes.monitoring_node import MonitoringNode
from src.sdlc.nodes.monitor_fb_node import MonitorFeedback
from src.sdlc.nodes.maintanence_node import MaintanenceNode
from src.sdlc.nodes.consolidated_node import ConsolidatedNode

class GraphBuilder:

    def __init__(self,model):
        self.llm=model
        self.memory=MemorySaver()
        self.graph_builder=StateGraph(State)

    def build_graph(self):
        """
        Builds a SDLC graph using LangGraph.
        This method initializes nodes using the and integrates 
        it into the graph. 
        """
        self.userstories_node=UserStoriesNode(self.llm)
        self.human_fb_userstories=UserStoriesFeedback()
        self.design_documents_node=DesignDocumentsNode(self.llm)
        self.human_fb_design=DesignDocumentsFeedback()
        self.design_summarizer=DesignSummarizeNode(self.llm)
        self.coder_subgraph=CoderSubgraphNode(self.llm)
        self.human_fb_code=CodeFeedback()
        self.security_check_node=SecurityCheckNode(self.llm)
        self.human_fb_review=SecurityReviewFeedback()
        self.test_cases_node=TestCasesNode(self.llm)
        self.human_fb_testcases=TestCasesFeedback()
        self.qa_testing_node=QATestingNode()
        self.human_fb_qatesting=QAFeedback()
        self.deployment_node=DeploymentNode(self.llm)
        self.monitoring_node=MonitoringNode(self.llm)
        self.monitor_fb_node=MonitorFeedback()
        self.maintanence_node=MaintanenceNode(self.llm)
        self.consolidated_node=ConsolidatedNode()


        self.graph_builder.add_node("userstories_generator",self.userstories_node.process)
        self.graph_builder.add_node("human_fb_userstories", self.human_fb_userstories.process)
        self.graph_builder.add_node("design_documents_generator",self.design_documents_node.process)
        self.graph_builder.add_node("human_fb_design", self.human_fb_design.process)
        self.graph_builder.add_node("design_summarizer", self.design_summarizer.process)
        self.graph_builder.add_node("coder_subgraph",self.coder_subgraph.process)
        self.graph_builder.add_node("human_fb_code", self.human_fb_code.process)
        self.graph_builder.add_node("security_check_generator",self.security_check_node.process)
        self.graph_builder.add_node("human_fb_review", self.human_fb_review.process)
        self.graph_builder.add_node("test_cases_generator",self.test_cases_node.process)
        self.graph_builder.add_node("human_fb_testcases",self.human_fb_testcases.process)
        self.graph_builder.add_node("qa_testing_node",self.qa_testing_node.process)
        self.graph_builder.add_node("human_fb_qatesting",self.human_fb_qatesting.process)
        self.graph_builder.add_node("deployment_node",self.deployment_node.process)
        self.graph_builder.add_node("monitoring_node",self.monitoring_node.process)
        self.graph_builder.add_node("monitor_fb_node",self.monitor_fb_node.process)
        self.graph_builder.add_node("maintanence_node",self.maintanence_node.process)
        self.graph_builder.add_node("consolidated_node",self.consolidated_node.process)


        self.graph_builder.add_edge(START,"userstories_generator")
        self.graph_builder.add_edge("userstories_generator","human_fb_userstories")
        self.graph_builder.add_conditional_edges("human_fb_userstories", 
                                                 self.human_fb_userstories.user_story_review, 
                                                 ["userstories_generator", "design_documents_generator"])
        self.graph_builder.add_edge("design_documents_generator","human_fb_design")
        self.graph_builder.add_conditional_edges("human_fb_design", 
                                                 self.human_fb_design.design_document_review, 
                                                 ["design_documents_generator", "design_summarizer"])
        self.graph_builder.add_edge("design_summarizer","coder_subgraph")
        self.graph_builder.add_edge("coder_subgraph","human_fb_code")
        self.graph_builder.add_edge("human_fb_code","security_check_generator")
        self.graph_builder.add_edge("security_check_generator","human_fb_review")
        self.graph_builder.add_conditional_edges("human_fb_review", 
                                                 self.human_fb_review.security_review, 
                                                 ["security_check_generator", "test_cases_generator"])
        self.graph_builder.add_edge("test_cases_generator","human_fb_testcases")
        self.graph_builder.add_conditional_edges("human_fb_testcases", 
                                                 self.human_fb_testcases.testcase_review, 
                                                 ["test_cases_generator", "qa_testing_node"])
        self.graph_builder.add_edge("qa_testing_node","human_fb_qatesting")
        self.graph_builder.add_conditional_edges("human_fb_qatesting", 
                                                 self.human_fb_qatesting.check_qa_response, 
                                                 ["deployment_node", "coder_subgraph"])
        self.graph_builder.add_edge("deployment_node","monitoring_node")
        self.graph_builder.add_edge("monitoring_node","monitor_fb_node")
        self.graph_builder.add_edge("monitor_fb_node","maintanence_node")
        self.graph_builder.add_edge("maintanence_node","consolidated_node")
        self.graph_builder.add_edge("consolidated_node",END)
        

    def setup_graph(self):
        """
        Sets up the graph 
        """
        self.build_graph()
        #print("[DEBUG] Nodes in Graph:", self.graph_builder.nodes)
        #assert "human_fb_code" in self.graph_builder.nodes, "[ERROR] human_fb_code is missing!"    
        return self.graph_builder.compile(checkpointer=self.memory)

    





    
