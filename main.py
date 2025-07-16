from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from contextlib import asynccontextmanager
from bson.json_util import dumps


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

def serializar_documento(documento):
    documento["_id"] = str(documento["_id"])
    return documento



@app.get("/")
async def get_all_lists():
    coleccion =  database["comments"]
    documentos = coleccion.find()
    json_string = dumps(documentos)
    return json_string 


 
