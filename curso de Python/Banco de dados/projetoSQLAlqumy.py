"""
    Primeiro programa de integração com banco de dados
    utilizando SQLAlchemy e modelo ORM

"""
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()


class Cliente(Base):
    """
        Esta classe representa a tabela user_user dentro
        do SQlite.
    """
    __tablename__ = "cliente_user"
    # atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String(11))
    address = Column(String(100))

    conta = relationship(
        "Conta", back_populates="cliente"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, name={self.name}, cpf={self.cpf}, address={self.address})"


class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True)
    tipo_conta = Column(String(30), nullable=False, default="Conta Corrente")
    agencia = Column(Integer)
    nun = Column(Integer, ForeignKey("cliente_user.id"), nullable=False)
    saldo = (float)

    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Conta(id={self.id}, tipo_conta={self.tipo_conta}, id_usuario={self.nun})"


# conexão com o banco de dados
engine = create_engine("sqlite://")

# criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)



with Session(engine) as session:
    mateus = Cliente(
        name='mateus',
        cpf='45856965874',
        address='mateusdahoralopes@gmail.com'
    )

    eduardo = Cliente(
        name='eduardo',
        cpf='45265464354',
        address='eduardo@gmail.com'
    )
    
    mateus_conta = Conta(
        
        tipo_conta = "conta corrente",
        agencia = "1",
        nun = 1,
        saldo = 0
    )

    eduardo_conta = Conta(

        tipo_conta = "conta corrente",
        agencia = "1",
        nun = 2,
        saldo = 0
    )
    
    
    # enviando para o BD (persitência de dados)
    session.add_all([mateus, eduardo, mateus_conta, eduardo_conta])

    session.commit()


stmt = select(Cliente).where(Cliente.name.in_(["mateus"]))
print('Recuperando usuários a partir de condição de filtragem')
for cliente in session.scalars(stmt):
    print(cliente)

stmt = select(Conta).where(Conta.tipo_conta.in_(["conta corrente"]))
print('Recuperando contas a partir de condição de filtragem')
for conta in session.scalars(stmt):
    print(conta)


# encerrando de fato a session
session.close()