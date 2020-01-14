from pymongo import MongoClient

client = MongoClient()
client = MongoClient('mongodb+srv://admin:admin@cluster0-ueieq.mongodb.net/test?retryWrites=true&w=majority')
db = client['naada']

artists = []
result = db.naada_artists.find({})
for artist in result:
    artists.append({
        "artist": artist['artist'],
        "artist_img": artist['artist_img'],
        "artist_desc": artist['artist_desc']
    })

print(artists)
