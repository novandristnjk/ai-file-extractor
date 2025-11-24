from pydantic import BaseModel, Field
from typing import Optional

class ChatDTO(BaseModel):
    query: str = Field(None)