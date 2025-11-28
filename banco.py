from sqlalchemy import *
from sqlalchemy.orm import * 
import os
import pandas as pd

DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DIR, "dados/banco.db")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Base = declarative_base()

class Produto(Base):
    __tablename__ = "Produtos"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    qntd = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)

class Cliente(Base):
     __tablename__ = "Clientes"

     id_cliente = Column(Integer, primary_key=True)
     nome = Column(String, nullable=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

json_path = os.path.join(DIR, 'dados/clientes.json')

def carregar_clientes():
    try:
        if session.query(Cliente).count() == 0:
            df = pd.read_json(json_path, encoding='utf-8')
            df.to_sql(
                Cliente.__tablename__,
                engine,
                if_exists='append',
                index=False
            )
    except Exception as ex:
        print(ex)

def carregar_produtos():
    try:
        if session.query(Produto).count() == 0:
            df = pd.read_csv('dados/produtos.csv', sep=';')

            df['preco'] = df['preco'].str.replace('R$', '', regex=False)
            df['preco'] = df['preco'].str.replace('\xa0', '', regex=False)
            df['preco'] = df['preco'].str.replace(',', '.', regex=False)
            df['preco'] = df['preco'].astype(float)

            df['qtd'] = df['qtd'].astype(int)

            df = df.rename(columns={'qtd': 'qntd'})

            df.to_sql(
                Produto.__tablename__,
                engine,
                if_exists='append',
                index=False
            )
    except Exception as ex:
        print(ex)
