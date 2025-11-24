from pydantic import BaseModel, Field
from typing import Optional

class UploadDTO(BaseModel):
    extractFile: bool = Field(default=True)