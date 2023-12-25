from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field, conint, validator


class Answer(BaseModel):
    id: Optional[conint(ge=1, le=4)] = None
    answer_text: str
    is_correct: bool
