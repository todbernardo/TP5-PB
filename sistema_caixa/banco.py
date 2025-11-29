from sqlalchemy import *
from sqlalchemy.orm import * 
import os
import pandas as pd
import datetime 
from models import Base, Cliente, Produto, Compras, Itens 

DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(DIR)
DB_PATH = os.path.join(BASE_DIR, "dados", "banco.db")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

json_path = os.path.join(BASE_DIR, "dados", "clientes.json") 
csv_path = os.path.join(BASE_DIR, "dados", "produtos.csv")  

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
            df = pd.read_csv(csv_path, sep=';') 

            df['preco'] = df['preco'].str.replace('R$', '', regex=False)
            df['preco'] = df['preco'].str.replace('\xa0', '', regex=False)
            df['preco'] = df['preco'].str.replace(',', '.', regex=False)
            df['preco'] = df['preco'].astype(float)

            df['qtd'] = df['qtd'].astype(int)

            df = df.rename(columns={'qtd': 'quantidade'})  
            df.to_sql(
                Produto.__tablename__,
                engine,
                if_exists='append',
                index=False
            )
    except Exception as ex:
        print(ex)

def salvar_compra(df_agrupado, cliente_id):
    try:
        data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        ultima_compra = session.query(Compras).order_by(Compras.id_compra.desc()).first()
        proximo_id_compra = 1 if ultima_compra is None else ultima_compra.id_compra + 1

        nova_compra = Compras(
            id_compra=proximo_id_compra,
            data_hora=data_hora,
            id_cliente=cliente_id
        )
        session.add(nova_compra)
        session.flush()

        ultimo_item = session.query(Itens).order_by(Itens.id_item.desc()).first()
        proximo_id_item = 1 if ultimo_item is None else ultimo_item.id_item + 1

        for _, linha in df_agrupado.iterrows():
            session.add(Itens(
                id_item=proximo_id_item,
                quantidade=int(linha["Quantidade_Total"]),
                preco=float(linha["Preço"]),
                id_compra=nova_compra.id_compra,
                id_produto=int(linha["ID_Produto"])
            ))
            proximo_id_item += 1

        session.commit()
        print("Compra salva no banco de dados com sucesso.")

    except Exception as ex:
        session.rollback()
        print(f"Erro ao salvar compra: {ex}")