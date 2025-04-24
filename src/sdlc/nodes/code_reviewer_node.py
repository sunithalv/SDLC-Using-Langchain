from src.sdlc.states.states import CoderState
from src.sdlc.prompts.prompts import CODE_REVIEW_INSTRNS
from src.sdlc.schema.codefiletypes import CodeFileTypes
from src.sdlc import logger
import time
import groq

class CodeReviewerNode:
    """
    Node logic implementation.
    """
    def __init__(self,model):
        self.llm = model

    def process(self, state: CoderState):
        """
        Processes the input state and reviews the code based on the design documents.
        Sends the files in batches of 3 for token limit management.
        """
        generated_code = state.get("generated_code", {})
        design_summary = state["design_summary"]

        # Convert the dictionary into a list of (filename, content) pairs
        files_list = list(generated_code.items())

        batch_size = 3
        num_batches = min((len(files_list) + batch_size - 1) // batch_size, 4)  # Limit to 10 files 

        all_reviews = []

        for i in range(num_batches):
            batch = dict(files_list[i * batch_size : (i + 1) * batch_size])  # Create a dictionary from the batch
            try:
                response = self.llm.invoke(CODE_REVIEW_INSTRNS.format(
                    design_documents=design_summary,
                    generated_code=batch
                ))

                logger.info(f"In code reviewer node. Batch {i+1} Response: {response.content}")
                all_reviews.append(response.content)
            except groq.RateLimitError as e:
                wait_time = 70  # Wait a bit more than 1 minute
                logger.info(f"Rate limit reached. Waiting for {wait_time} seconds...")
                time.sleep(wait_time)  # Sleep and retry
                response = self.llm.invoke(CODE_REVIEW_INSTRNS.format(
                    design_documents=design_summary,
                    generated_code=batch
                ))
                logger.info(f"Batch {i+1} Review after wait: ", response.content)
                all_reviews.append(response.content)

        # Combine all reviews into a single string
        combined_review = "\n\n".join(all_reviews)

        return {"generated_code_review": combined_review}

    
