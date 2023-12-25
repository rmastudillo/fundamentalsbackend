from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Question(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    module: str
    topic: str
    course: str
    source: str
    content: str
    question_text: str
    answer_options: List[str]
    correct_answer: str
    hint_list: List[str]
    answer_solved_list: List[str]
    difficulty: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "module": "Module 1",
                "topic": "Topic 1",
                "course": "Course 1",
                "source": "Source 1",
                "content": "Content 1",
                "question_text": "What is ...?",
                "answer_options": ["Option 1", "Option 2"],
                "correct_answer": "Option 1",
                "hint_list": ["Hint 1", "Hint 2"],
                "answer_solved_list": ["Solution 1"],
                "difficulty": "Easy",
            }
        }
