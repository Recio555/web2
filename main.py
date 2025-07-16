
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from contextlib import asynccontextmanager
from bson.json_util import dumps
from fastapi.responses import JSONResponse


# Initialize FastAPI app
uri = "mongodb+srv://hnorecio:Filipenses48@cluster0.xiwaxdd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, database, collection
    
    client = MongoClient(uri)
    # Ensure the database is available:
    database = client["sample_mflix"]
    pong = database.command("ping")
    if int(pong["ok"]) != 1:
        raise Exception("Cluster connection is not okay!")

    todo_lists = database.get_collection('comments')
    
    #app.todo_dal = ToDoDAL(todo_lists)

    # Yield back to FastAPI Application:
    yield

    # Shutdown:
    client.close()

app = FastAPI()

# Serializador para documentos MongoDB
def serializar_documento(documento):
    try:
        documento["_id"] = str(documento["_id"])
        return documento
    except Exception as e:
        print(f"Error al serializar el documento: {e}")
        raise HTTPException(status_code=500, detail="Error al serializar el documento")

@app.get("/")
async def get_all_lists():
    try:
        coleccion = database["comments"]
        documentos = coleccion.find()
        
        # Convertir cada documento usando serializar_documento
        lista_documentos = [serializar_documento(doc) for doc in documentos]
        
        return JSONResponse(content=lista_documentos)
    
    except Exception as e:
        print(f"Error en el endpoint /: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor") 


 