from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

Fornecedor_produto = Table(
    "produto_fornecedor",
    Base.metadata,
    Column("id_fornecedor", Integer, ForeignKey("fornecedores.id_fornecedor"), primary_key=True),
    Column("id_produto", Integer, ForeignKey("produto.id_produto"), primary_key=True)
)

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True)
    nome = Column(String)

    compras = relationship("Compra", cascade="all, delete-orphan", back_populates="cliente")

    def __init__(self, id_cliente, nome):
        self.id_cliente = id_cliente
        self.nome = nome

    def __str__(self):
        return f"{self.id_cliente}, {self.nome}"
    
class Produto(Base):
    __tablename__ = "produtos"

    id_produto = Column(Integer, primary_key=True)
    nome = Column(String)
    quantidade = Column(Integer)
    preco = Column(Float)

    fornecedores = relationship("Fornecedor", secondary=Fornecedor_produto, back_populates="produtos")
    itens_compra = relationship("Item", back_populates="produto_referencia")

    def __init__(self, id_produto, nome, quantidade, preco):
        self.id_produto = id_produto
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def __str__(self):
        return f"{self.id_produto}, {self.nome}, {self.quantidade}, {self.preco}"
    
class Compras(Base):
    __tablename__ = "compras"

    id_compra = Column(Integer, primary_key=True)
    data_hora = Column(String)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    
    clientes = relationship("Cliente", back_populates="compras")
    itens = relationship("Item", cascade="all, delete-orphan", back_populates="compra")

    def __init__(self, id_compra, data_hora, id_cliente):
        self.id_compra = id_compra
        self.data_hora = data_hora
        self.id_cliente = id_cliente

    def __str__(self):
        return f"{self.id_compra}, {self.data_hora}, {self.id_cliente}"


    