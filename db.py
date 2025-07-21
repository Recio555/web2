from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://reciosalvador:En8A21YCVUfUgUfC@cluster0.fnhcurd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')

except Exception as e:
    print(e)

def get_db():
    return client["Informedb"]
