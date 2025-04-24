from src.sdlc.states.states import State
from src.sdlc.prompts.prompts import DESIGNDOCS_GEN_INSTRNS,DESIGN_MODIFY_INSTRNS
from src.sdlc import logger

class DesignDocumentsNode:
    """
    Node logic implementation.
    """
    def __init__(self,model):
        self.llm = model

    def process(self, state: State):
        """
        Processes the input state and generates design document based on user stories.
        """
        design_review=state.get("design_documents_review", "")
        design_doc=state.get("design_documents", "")
        if design_review:
            response=self.llm.invoke(DESIGN_MODIFY_INSTRNS.format(design_review=design_review,
                                                            design_documents=design_doc))
            logger.info("IN MODIFY DESIGN DOCS...")
        else:
            response=self.llm.invoke(DESIGNDOCS_GEN_INSTRNS.format(user_stories=state["user_stories"],
                                                                design_documents=design_doc,
                                                                design_review=design_review))
            logger.info("IN DESIGN DOCS GENERATION...")
        return {"design_documents":response.content}
    

    
