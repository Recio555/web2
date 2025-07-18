from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson import ObjectId
from typing import Optional, List, Dict

app = FastAPI()

# Modelo Pydantic
class Publicador(BaseModel):
    nombre: Optional[str]
    horas: Optional[int]
    revisitas: Optional[int]

# Serializador para ObjectId -> str
def serialize_publicador(pub: dict) -> dict:
    pub["_id"] = str(pub["_id"])
    return pub

# Cliente y base de datos MongoDB asíncrono
MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client["mi_basedatos"]

# Dependencia para la base de datos
def get_db() -> AsyncIOMotorDatabase:
    return db

# Crear publicador
@app.post("/publicadores", response_model=Dict)
async def crear_publicador(publicador: Publicador, db: AsyncIOMotorDatabase = Depends(get_db)):
    publicador_dict = {k: v for k, v in publicador.dict().items() if v is not None}
    result = await db["publicadores"].insert_one(publicador_dict)
    publicador_dict["_id"] = result.inserted_id
    return serialize_publicador(publicador_dict)

# Listar publicadores
@app.get("/publicadores", response_model=List[Dict])
async def listar_publicadores(db: AsyncIOMotorDatabase = Depends(get_db)):
    cursor = db["publicadores"].find()
    publicadores = await cursor.to_list(length=100)
    return [serialize_publicador(pub) for pub in publicadores]

# Obtener publicador por ID
@app.get("/publicadores/{id}", response_model=Dict)
async def obtener_publicador(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    publicador = await db["publicadores"].find_one({"_id": ObjectId(id)})
    if not publicador:
        raise HTTPException(status_code=404, detail="Publicador no encontrado")
    return serialize_publicador(publicador)

# Actualizar publicador por ID
@app.put("/publicadores/{id}", response_model=Dict)
async def actualizar_publicador(id: str, datos: Publicador, db: AsyncIOMotorDatabase = Depends(get_db)):
    actualizacion = {k: v for k, v in datos.dict().items() if v is not None}
    resultado = await db["publicadores"].update_one({"_id": ObjectId(id)}, {"$set": actualizacion})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Publicador no encontrado")
    publicador_actualizado = await db["publicadores"].find_one({"_id": ObjectId(id)})
    return serialize_publicador(publicador_actualizado)

# Eliminar publicador por ID
@app.delete("/publicadores/{id}", response_model=Dict)
async def eliminar_publicador(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    resultado = await db["publicadores"].delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Publicador no encontrado")
    return {"mensaje": "Publicador eliminado correctamente"}
