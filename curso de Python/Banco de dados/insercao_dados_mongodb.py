from pymongo import MongoClient
import datetime
import pprint

# Conectando ao servidor MongoDB local na porta padrão (27017)
client = MongoClient('localhost', 27017)

db = client.test
collection = db.test_collection
print(db.test_collection)


# definição de infor para compor o doc
post = {
    "name":"mateus",
    "cpf":"78215687412",
    "address":"mateusdahoralopes@gmail.com",
    "tipo_conta":"conta corrente",
    "agencia":"1",
    "nun":"1",
    "saldo":"0",
    "date": datetime.datetime.now(datetime.UTC)
}

# preparando para submeter as infos
posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(post_id)

# print(db.posts.find_one())
pprint.pprint(db.posts.find_one())

