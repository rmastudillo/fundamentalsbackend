import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar las variables de entorno desde .env
load_dotenv()

# Ahora puedes usar os.getenv para acceder a las variables de entorno
uri = os.getenv('MONGODB_URI')
client = AsyncIOMotorClient(uri)
database = client.fundamentalsbdd  # nombre de tu base de datos
question_collection = database.get_collection("questions_collection")  # nombre de la colección

# Función para obtener la colección de preguntas
def question_helper(question) -> dict:
    return {
        "id": str(question["_id"]),
        "texto_pregunta": question["texto_pregunta"],
        "categoria": question["categoria"],
        "dificultad": question["dificultad"],
        "respuestas": question["respuestas"],
        "pistas": question["pistas"],
    }
