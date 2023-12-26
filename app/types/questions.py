from typing import List, Optional

from app.types.answers import Answer  # Asegúrate de que esta ruta es correcta
from bson import ObjectId
from pydantic import BaseModel, Field, root_validator, validator


# Clase PyObjectId para convertir ObjectId de MongoDB a un formato compatible con Pydantic
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


# Modelo para representar una pregunta y sus respuestas
class Question(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    module: str
    topic: str
    course: str
    source: str
    content: str
    question_text: str
    answer_options: List[Answer]  # Lista de respuestas (modelo Answer)
    correct_answer_index: Optional[int] = None  # Índice de la respuesta correcta
    hint_list: List[str]
    answer_solved_list: List[str]
    difficulty: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

    # Validador para asignar IDs automáticamente a las respuestas y determinar la correcta
    @validator("answer_options", pre=True)
    def process_answers(cls, answers):
        for index, answer in enumerate(answers):
            if isinstance(answer, dict):  # Convertir dict a Answer si es necesario
                answer["id"] = index + 1  # Asignar ID basado en la posición
        return answers

    @root_validator
    def set_correct_answer_index(cls, values):
        answers = values.get("answer_options", [])
        correct_index = None
        for index, answer in enumerate(answers):
            if answer.is_correct:
                correct_index = index + 1
                break  # Asumimos que solo hay una respuesta correcta
        values["correct_answer_index"] = correct_index
        return values
