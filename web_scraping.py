from urllib.request import urlopen
from io import StringIO
from bs4 import BeautifulSoup
import pandas as pd
import requests


URL = "https://pedrovncs.github.io/lindosprecos/produtos.html#"

def acessar_url():
    try:
        html = urlopen(URL)
    except Exception as ex:
        print(ex)  
        exit()
    return html

def obter_produtos(bs):
    cards_produtos = bs.find_all("div", class_="card-body")
    if not cards_produtos:
        print("Erro: produto não encontrado")
        exit()
        return []

    lista_produtos = []

    for card in cards_produtos:
        nome_tag = card.find("h5", attrs={"data-nome": True})
        nome = nome_tag['data-nome'].strip() if nome_tag else None

        preco_tag = card.find("p", attrs={"data-preco": True})
        preco = preco_tag['data-preco'].strip() if preco_tag else None

        qtd_tag = card.find("p", attrs={"data-qtd": True})
        qtd = qtd_tag['data-qtd'].strip() if qtd_tag else None

        produto = {
            "nome": nome,
            "preco": preco,
            "qtd": qtd
        }
        lista_produtos.append(produto)

    return lista_produtos

def construir_csv():
    html = acessar_url()

    if html:
        bs = BeautifulSoup(html, "html.parser")
        lista_produtos = obter_produtos(bs)

        if lista_produtos:
            df = pd.DataFrame(lista_produtos)
            df.to_csv("dados/produtos.csv", index=False, sep=';')

