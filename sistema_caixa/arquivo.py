from banco import *

def ler_produtos():
    try:
        produtos = session.query(Produto).all()

        lista_produtos = []
        for produto in produtos:
            lista_produtos.append((produto.id, produto.nome, produto.qntd, produto.preco))
        
        return lista_produtos
        
    except Exception as e:
        print(f"Erro na leitura do banco: {e}")

def atualizar_estoque(produto_id, quantidade_comprada):
    try:
        produto = session.query(Produto).filter_by(id=produto_id).first()

        if produto:
            produto.qntd -= quantidade_comprada
            session.commit()

    except Exception as e:
        print(f"Erro: {e}")
