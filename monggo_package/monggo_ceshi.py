from pymongo import MongoClient

client = MongoClient(host='127.0.0.1',port=27017)
print(client.address)
print(client.database_names())
db = client.hehe
print(db.collection_names())
col = db['stu']
result = col.find()
for data in result:
    print(data)