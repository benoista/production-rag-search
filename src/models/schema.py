from typing_extensions import Self
from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, model_validator, Field
import hashlib

class Document(BaseModel):
    id: str
    content: str
    filepath: str
    created_at: datetime
    metadata: dict[str, str] # Keys and values are strings
    content_hash: str = Field(default="") # Hash empty string by default so the user doesn't have to set it

    # Hash the content of the document
    @model_validator(mode="after")
    def hash_content(self) -> Self:
        self.content_hash = hashlib.sha256(self.content.encode()).hexdigest()
        return self