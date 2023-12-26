from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field, validator

# Revisa la ruta del importe de Answer para asegurarte de que es correcta
from app.types.answers import Answer

# Clase PyObjectId para convertir ObjectId de MongoDB a un formato compatible con Pydantic


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, handler):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema_or_field, current_handler):
        # Actualizar el esquema JSON para el tipo personalizado
        return {"type": "string"}

# Modelo para representar una pregunta y sus respuestas


class Question(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    module: str
    topic: str
    course: str
    source: str
    subject: str
    question_text: str
    answer_options: List[Answer]
    # Índice de la respuesta correcta
    correct_answer_index: Optional[int] = None
    hint_list: List[str]
    answer_solved_list: List[str]
    difficulty: str

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        exclude_unset = True
        populate_by_name = True

    @validator("answer_options", pre=True)
    def process_answers(cls, answers):
        for index, answer in enumerate(answers):
            if isinstance(answer, dict):  # Convertir dict a Answer si es necesario
                answer['id'] = index + 1  # Asignar ID basado en la posición
        return answers

    @validator("correct_answer_index", always=True)
    def set_correct_answer_index(cls, v, values):
        answers = values.get('answer_options', [])
        correct_index = None
        for index, answer in enumerate(answers):
            if isinstance(answer, Answer) and answer.is_correct:
                correct_index = index + 1
                break  # Asumimos que solo hay una respuesta correcta
        return correct_index if correct_index is not None else v
