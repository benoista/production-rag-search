from datetime import datetime
from pydantic import BaseModel, Field
import hashlib

class Document(BaseModel):
    id: str
    content: str
    filepath: str
    created_at: datetime
    metadata: dict[str, str] # Keys and values are strings
    content_hash: str = Field(default="") # Hash empty string by default so the user doesn't have to set it

    # Hash the content of the document
    def model_post_init(self, __context):
        self.content_hash = hashlib.sha256(self.content.encode()).hexdigest()
        return self


class Chunk(BaseModel):
    id: str = Field(default="") 
    document_id: str
    content: str
    index: int 
    token_nbr: int 
    metadata: dict[str, str] = Field(default_factory=dict)

    def model_post_init(self, __context):
        self.id = self.document_id + "::" + str(self.index)
        return self