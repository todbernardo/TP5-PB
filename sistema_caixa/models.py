from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

Fornecedor_produto = Table(
    "produto_fornecedor",
    Base.metadata,
    Column("id_fornecedor", Integer, ForeignKey("fornecedores.id_fornecedor"), primary_key=True),
    Column("id_produto", Integer, ForeignKey("produtos.id_produto"), primary_key=True)
)

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True)
    nome = Column(String)

    compras = relationship("Compras", cascade="all, delete-orphan", back_populates="cliente")

    def __init__(self, id_cliente, nome):
        self.id_cliente = id_cliente
        self.nome = nome

    def __str__(self):
        return f"{self.id_cliente}, {self.nome}"

class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id_fornecedor = Column(Integer, primary_key=True)
    nome = Column(String)

    produtos = relationship("Produto", secondary=Fornecedor_produto, back_populates="fornecedores")

    def __init__(self, id_fornecedor, nome):
        self.id_fornecedor = id_fornecedor
        self.nome = nome

    def __str__(self):
        return f"{self.id_fornecedor}, {self.nome}"
    
class Produto(Base):
    __tablename__ = "produtos"

    id_produto = Column(Integer, primary_key=True)
    nome = Column(String)
    quantidade = Column(Integer)
    preco = Column(Float)

    fornecedores = relationship("Fornecedor", secondary=Fornecedor_produto, back_populates="produtos")
    itens_compra = relationship("Itens", back_populates="produto_referencia")

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
    
    cliente = relationship("Cliente", back_populates="compras")
    itens = relationship("Itens", cascade="all, delete-orphan", back_populates="compra")

    def __init__(self, id_compra, data_hora, id_cliente):
        self.id_compra = id_compra
        self.data_hora = data_hora
        self.id_cliente = id_cliente

    def __str__(self):
        return f"{self.id_compra}, {self.data_hora}, {self.id_cliente}"

class Itens(Base):
    __tablename__ = "itens"

    id_item = Column(Integer, primary_key=True)
    quantidade = Column(Integer)
    preco = Column(Float)
    id_compra = Column(Integer, ForeignKey("compras.id_compra"))
    id_produto = Column(Integer, ForeignKey("produtos.id_produto"))
    
    compra = relationship("Compras", back_populates="itens")
    produto_referencia = relationship("Produto", back_populates="itens_compra")
    # Tetar deletar item e ver se nao deleta o fornecedor

    def __init__(self, id_item, quantidade, preco, id_compra, id_produto):
        self.id_item = id_item
        self.quantidade = quantidade
        self.preco = preco
        self.id_compra = id_compra
        self.id_produto = id_produto

    def __str__(self):
        return f"{self.id_item}, {self.quantidade}, {self.preco}, {self.id_compra}, {self.id_produto}"
    




    