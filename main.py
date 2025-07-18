from fastapi import FastAPI, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from pydantic import BaseModel
from typing import Dict, List
from bson.errors import InvalidId
from db import get_db





app = FastAPI()


#client = get_db()
#db = client["Informedb"]

# Seleccionar la colección (se crea si no existe)
#coleccion = db["publicador"]

# Modelo Pydantic para el publicador
class Publicador(BaseModel):
    nombre: str
    horas: int
    revisitas: int

# Serializador
def serialize_publicador(pub) -> dict:
    pub["_id"] = str(pub["_id"])
    return pub



#resultado = coleccion.insert_one(nuevo_publicador)
#print("ID insertado:", resultado.inserted_id)

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
@app.get("/publicadores/{id}", response_model=Dict)
def obtener_publicador(id: str, db=Depends(get_db)):
    try:
        oid = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    publicador = db["publicadores"].find_one({"_id": oid})
    if not publicador:
        raise HTTPException(status_code=404, detail="Publicador no encontrado")
    return serialize_publicador(publicador)

# Actualizar publicador por ID
@app.put("/publicadores/{id}", response_model=Dict)
def actualizar_publicador(id: str, datos: Publicador, db=Depends(get_db)):
    actualizacion = {k: v for k, v in datos.dict().items() if v is not None}
    resultado = db["publicadores"].update_one({"_id": ObjectId(id)}, {"$set": actualizacion})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Publicador no encontrado")
    publicador_actualizado = db["publicadores"].find_one({"_id": ObjectId(id)})