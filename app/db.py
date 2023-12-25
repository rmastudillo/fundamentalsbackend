import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from app.types.questions import Question

# Cargar las variables de entorno desde .env
load_dotenv()

# Ahora puedes usar os.getenv para acceder a las variables de entorno
uri = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(uri)
database = client.fundamentalsbdd  # nombre de tu base de datos
question_collection = database.get_collection(
    "questions_collection"
)  # nombre de la colección


# Función para obtener la colección de preguntas
def question_helper(question) -> Question:
    print('ERROR',question)
    question_dict = question.copy()  # Asegúrate de que 'question' es un diccionario
    question_dict["id"] = str(question_dict.pop("_id", None))  # Convertir ObjectId a str
    return Question(**question_dict)
