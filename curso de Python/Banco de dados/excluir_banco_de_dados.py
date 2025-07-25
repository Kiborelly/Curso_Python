from pymongo import MongoClient

# Conecte-se ao servidor MongoDB local
client = MongoClient('localhost', 27017)

# Exclua o banco de dados 'teste'
client.drop_database('test')

# Verifique se o banco de dados foi excluído
db_list = client.list_database_names()
print("\nBancos de dados no servidor:")
for db in db_list:
    print(db)