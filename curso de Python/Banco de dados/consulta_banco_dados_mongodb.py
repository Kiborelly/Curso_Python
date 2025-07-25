from pymongo import MongoClient
import datetime

# Conectando ao servidor MongoDB local na porta padrão (27017)
client = MongoClient('localhost', 27017)

# Obter a lista de bancos de dados
db_list = client.list_database_names()

# Imprimir cada banco de dados na lista
print("\nBancos de dados no servidor:")
for db in db_list:
    print(db)

# Obter o banco de dados desejado
meu_banco = client['test']

# Obter a lista de coleções no banco de dados
colecao_list = meu_banco.list_collection_names()

# Imprimir cada coleção na lista
print("\nColeções de dados no banco de dados test:")
for colecao in colecao_list:
    print(colecao)

# Obter a coleção desejada
minha_colecao = meu_banco['posts']

# Obter todos os documentos na coleção
documentos = minha_colecao.find()

# Imprimir cada documento
print("\nDocumentos na coleção post de a cordo con criterios definidos:")
for documento in documentos:
    print(documento)



