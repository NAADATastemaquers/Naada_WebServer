
from pymongo import MongoClient



client = MongoClient()
client = MongoClient('mongodb+srv://admin:admin@cluster0-ueieq.mongodb.net/test?retryWrites=true&w=majority')
db = client['naada']
result = db.naada_artists.find()
for r in result:
    print(r)
