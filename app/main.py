# main.py
from fastapi import FastAPI, Body
from app.db import question_collection, question_helper

app = FastAPI()

@app.post("/preguntas/")
async def add_question(pregunta: dict = Body(...)):
    new_question = await question_collection.insert_one(pregunta)
    created_question = await question_collection.find_one({"_id": new_question.inserted_id})
    return question_helper(created_question)

