
uri = "mongodb+srv://reciosalvador:En8A21YCVUfUgUfC@cluster0.fnhcurd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Seleccionar la base de datos (se crea si no existe)
db = client["Informedb"]

# Seleccionar la colección (se crea si no existe)
coleccion = db["publicador"]


nuevo_publicador = {
    "nombre": "Pedro",
    "horas": 12,
    "revisitas": 5
}

resultado = coleccion.insert_one(nuevo_publicador)
print("ID insertado:", resultado.inserted_id)