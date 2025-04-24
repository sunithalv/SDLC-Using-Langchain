from pydantic import BaseModel,Field
from typing import List

# Schema for structured output to use in planning
class CodeFile(BaseModel):
    name: str = Field(
        description="Name of the code file with extension",
    )
    code: str = Field(
        description="Code content of the file",
    )

class CodeFiles(BaseModel):
    codefiles: List[CodeFile] = Field(
        description="List of code files.",
    )