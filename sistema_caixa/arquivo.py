from banco import *

def ler_produtos():
    try:
        produtos = session.query(Produto).all()

        lista_produtos = []
        for produto in produtos:
            lista_produtos.append((produto.id_produto, produto.nome, produto.quantidade, produto.preco))
        
        return lista_produtos
        
    except Exception as e:
        print(f"Erro na leitura do banco: {e}")

def atualizar_estoque(produto_id, quantidade_comprada):
    try:
        produto = session.query(Produto).filter_by(id_produto=produto_id).first()

        if produto:
            produto.quantidade -= quantidade_comprada
            session.commit()

    except Exception as e:
        print(f"Erro: {e}")
