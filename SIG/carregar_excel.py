import pandas as pd

def ler_fornecedores_planilha():
    df = pd.read_excel("dados/planilha_fornecedores.xlsx", sheet_name="fornecedores")
    return df

def ler_produtos_planilha():
    df = pd.read_excel("dados/planilha_fornecedores.xlsx", sheet_name="produtos-fornecedores")
    return df

def carregar_fornecedores():
    for linha in df.itertuples():
        fornecedor = Fornecedor(linha.id_fornecedor, linha.nome)
        adicionar_fornecedor_no_banco(fornecedor)

def carregar_produtos_fornecedores():
    for linha in df.itertuples():
        session.execute(Produto_fornecedor.insert().values(id_produto=linha.id_produto, id_fornecedor=linha.id_fornecedor))

def carregar_fornecedores_e_produtos_no_banco():
    df_fornecedores = ler_fornecedores_planilha()
    df_produtos = ler_produtos_planilha()

    carregar_fornecedores(df_fornecedores)
    carregar_produtos_fornecedores(df_produtos)