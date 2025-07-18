from fastapi import FastAPI, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from pydantic import BaseModel
from typing import Dict, List
from bson.errors import InvalidId
from typing import Optional
from db import get_db


app = FastAPI()

class PublicadorUpdate(BaseModel):
    nombre: Optional[str] = None
    horas: Optional[int] = None
    revisitas: Optional[int] = None

    
# Modelo Pydantic para el publicador
class Publicador(BaseModel):
    nombre: str
    horas: int
    revisitas: int

# Serializador
def serialize_publicador(pub) -> dict:
    pub["_id"] = str(pub["_id"])
    return pub


# Endpoint POST para crear un nuevo publicador
@app.post("/publicadores", response_model=Dict)
def crear_publicador(publicador: Publicador, db=Depends(get_db)):
    publicador_dict = publicador.model_dump()
    result = db["publicador"].insert_one(publicador_dict)
    publicador_dict["_id"] = result.inserted_id
    return serialize_publicador(publicador_dict)


@app.get("/publicadores", response_model=List[dict])
def get_all_publicadores(db = Depends(get_db)):
    cursor = db["publicador"].find()
    publicadores = list(cursor)
    return [serialize_publicador(pub) for pub in publicadores]


# Obtener publicador por ID
@app.get("/publicadores/{id}")
def obtener_publicador(id: str, db=Depends(get_db)):
    try:
        id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    publicador = db["publicador"].find_one({"_id": id})
    if not publicador:
        raise HTTPException(status_code=404, detail="Publicador no encontrado")
    return serialize_publicador(publicador)


# Actualizar publicador por ID
@app.put("/publicadores/{id}")
def actualizar_publicador(id: str, datos: PublicadorUpdate, db=Depends(get_db)):
    try:
        obj_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de publicador no válido")
    actualizacion = {"$set": datos.model_dump(exclude_unset=True)}
    resultado = db["publicador"].update_one({"_id": obj_id}, actualizacion)
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Publicador no encontrado")
    publicador_actualizado = db["publicador"].find_one({"_id": obj_id})
    # Puedes crear una función para serializar el ObjectId a string si es necesario
    publicador_actualizado["id"] = str(publicador_actualizado.pop("_id"))
    return publicador_actualizado

@app.delete("/publicadores/{id}")
def eliminar_publicador(id: str, db=Depends(get_db)):
    try:
        obj_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    resultado = db["publicador"].delete_one({"_id": obj_id})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Publicador no encontrado")
    return {"mensaje": "Publicador eliminado correctamente", "id": id}

