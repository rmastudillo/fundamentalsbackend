from typing import List, Optional

from app.types.answers import Answer
from bson import ObjectId
from pydantic import BaseModel, Field, validator, ValidationError


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
    answer_options: List[Answer]  # Modificado para usar el modelo Answer
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
                "answer_options": [  # Modificado para incluir objetos de tipo Answer
                    {"answer_text": "Option 1", "is_correct": False},
                    {"answer_text": "Option 2", "is_correct": True},
                    # ... más respuestas según sea necesario
                ],
                "correct_answer": "Option 1",
                "hint_list": ["Hint 1", "Hint 2"],
                "answer_solved_list": ["Solution 1"],
                "difficulty": "Easy",
            }
        }

    @validator("answer_options", pre=True, each_item=False)
    def assign_ids_to_answers(cls, answer_options):
        validated_answers = []
        for index, answer in enumerate(answer_options):
            # Asegúrate de que 'answer' es un diccionario
            answer_dict = answer if isinstance(answer, dict) else answer.dict()
            answer_dict["id"] = index + 1
            # Asigna automáticamente un ID basado en el orden de la lista (1-4)

            try:
                # Valida y convierte el diccionario a una instancia de Answer
                validated_answer = Answer(**answer_dict)
                validated_answers.append(validated_answer)
            except ValidationError as e:
                raise ValueError(f"Error al validar respuesta: {e}")

        return validated_answers

    @validator("answer_options")
    def check_unique_answer_ids(cls, answer_options):
        # Verificar que los identificadores de las respuestas sean únicos
        ids = [answer.id for answer in answer_options]
        if len(ids) != len(set(ids)):
            raise ValueError("Answer IDs must be unique.")
        return answer_options
