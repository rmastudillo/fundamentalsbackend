from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class Answer(BaseModel):
    id: Optional[int] = None
    answer_text: str
    is_correct: bool
