# main.py
from app.db import question_collection, question_helper
from app.types.questions import Question
from bson import ObjectId
from fastapi import Body, FastAPI, HTTPException

app = FastAPI()


@app.post(
    "/questions/",
    tags=["Preguntas"],
    summary="Añadir una nueva pregunta",
    description="Crea una nueva pregunta y la almacena en la base de datos.",
)
async def add_question(question: Question = Body(...)):
    new_question = await question_collection.insert_one(question.dict())
    print(new_question)
    created_question = await question_collection.find_one(
        {"_id": new_question.inserted_id}
    )
    return question_helper(created_question)


@app.get(
    "/questions/",
    tags=["Preguntas"],
    summary="Obtener preguntas",
    description="Recupera todas las preguntas almacenadas en la base de datos.",
)
async def get_questions():
    questions = []
    try:
        async for question in question_collection.find():
            question_data = question_helper(question)
            questions.append(question_data)
    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(error)}"
        )
    return questions


@app.get("/questions/{id}/", tags=["Preguntas"], response_model=Question)
async def get_question(id: str):
    # Convertir el string a un ObjectId de MongoDB
    try:
        id = ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    # Buscar la pregunta en la base de datos
    question = await question_collection.find_one({"_id": id})
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    return question_helper(question)


@app.delete("/questions/{id}/", tags=["Preguntas"])
async def delete_question(id: str):
    # Convertir el string a un ObjectId de MongoDB
    try:
        id = ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    # Eliminar la pregunta de la base de datos
    question = await question_collection.find_one({"_id": id})
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    # Eliminar la pregunta de la base de datos
    await question_collection.delete_one({"_id": id})
    # Devolver mensaje y pregunta eliminada
    return {
        "message": "Question deleted successfully",
        "question": question_helper(question),
    }
