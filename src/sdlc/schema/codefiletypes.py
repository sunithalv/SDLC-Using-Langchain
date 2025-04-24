from pydantic import BaseModel,Field
from typing import List

class CodeFileType(BaseModel):
    name: str = Field(
        description="Name of the code file with extension",
    )
    description: str = Field(
        description="Description of the functionality in the file",
    )

class CodeFileTypes(BaseModel):
    codefiletypes: List[CodeFileType] = Field(
        description="List of code files.",
    )

