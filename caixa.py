from arquivo import *
from tabulate import *
import datetime
import pandas as pd

headers = ["Item", "Produto", "Quantidade", "Preço", "Total"]
headers_sem_item = ["ID", "Produto", "Quantidade", "Preço",]
lista_clientes = []
lista_totais = []
lista_quantidades = []
produto_selecionado = None
cliente = 3

def identificar_cliente():
    global cliente

    try:
        id_cliente_input = int(input("Digite o ID do cliente: \n"))
        cliente_encontrado = session.query(Cliente).filter_by(id_cliente=id_cliente_input).first()

        if cliente_encontrado:
            cliente = cliente_encontrado.id_cliente

        else:
            nome_cliente = f"Cliente {id_cliente_input}"
            novo_cliente_db = Cliente(id_cliente=id_cliente_input, nome=nome_cliente)
    
            session.add(novo_cliente_db)
            session.commit()

            cliente = novo_cliente_db.id_cliente

    except Exception as ex:
        print(ex)

def iniciar_atendimento():
    try:
        print("========== ATENDIMENTO ==========")
        print("1 - Iniciar atendimento")
        print("2 - Fechar caixa")
        comecar = int(input())
        print()

        if comecar == 1:
            identificar_cliente()
            print(tabulate(ler_produtos(), headers=headers_sem_item))

    except Exception as e:
        print(f"Erro: {e}")

    return comecar

def atendimento():
    global cliente, produto_selecionado, produtos_comprados, lista_quantidades
    
    produtos_comprados = []
    lista_quantidades = []
    
    while True:
        try:
            produto_selecionado = int(input("\nDigite o ID do produto para adicioná-lo ao carrinho ou 0 para finalizar a compra: "))
            if produto_selecionado == 0: 
                break

            quantidade = int(input("Digite a quantidade: "))
            if quantidade < 1:
                print("Erro: quantidade deve ser maior que zero.")
            else: 
                produto_encontrado = False
                carrinho_str = "" 
                
                for produto in ler_produtos():
                    if produto[0] == produto_selecionado:
                        produto_encontrado = True

                        if quantidade > produto[2]:
                            print("Estoque do produto incompatível.")
                        else:
                            lista_quantidades.append(quantidade)
                            produtos_comprados.append(produto)
                            print(f"'{produto[1]}' adicionado ao carrinho!")

                            for i, prod in enumerate(produtos_comprados):
                                carrinho_str += f"{prod[1]} ({lista_quantidades[i]}x) | "
                            print(f"Carrinho: {carrinho_str}")
                        
                if not produto_encontrado:
                    print("Produto não encontrado.")

        except Exception as e:
            print(f"Erro no loop de atendimento: {e}")

    print("Compra finalizada!")

    if not produtos_comprados:
        print("Carrinho estava vazio.")
        lista_clientes.append(cliente) 
        lista_totais.append(0)        
        return 

    tabela = []
    for i, produto in enumerate(produtos_comprados):
        tabela.append({
            'ID_Produto': produto[0],
            'Produto': produto[1],
            'Preço': produto[3],
            'Quantidade': lista_quantidades[i]
        })
    df = pd.DataFrame(tabela)

    df_agrupado = df.groupby(['ID_Produto', 'Produto', 'Preço']).agg(
        Quantidade_Total=('Quantidade', 'sum')
    ).reset_index()

    print("Atualizando estoque...")
    try:
        for i, linha in df_agrupado.iterrows():
            id_do_produto = int(linha['ID_Produto'])
            quantidade_total_comprada = int(linha['Quantidade_Total'])
            
            atualizar_estoque(id_do_produto, quantidade_total_comprada)
            
        print("Estoque atualizado com sucesso.")
    except Exception as e:
        print(e)
    
    total_compra = (df_agrupado['Preço'] * df_agrupado['Quantidade_Total']).sum()
    lista_clientes.append(cliente)
    lista_totais.append(total_compra)

    gerar_recibo(df_agrupado, total_compra)
    
    return produto_selecionado
    
def gerar_recibo(df_agrupado, total_compra):

    df_agrupado['Total_Item'] = df_agrupado['Preço'] * df_agrupado['Quantidade_Total']   

    tabela_final = []
    for i, linha in df_agrupado.iterrows():
        tabela_final.append([
            i + 1,                 
            linha['Produto'],          
            linha['Quantidade_Total'],  
            linha['Preço'],             
            linha['Total_Item']         
        ]) 
    print(f"""
Cliente {cliente}
Data: {datetime.datetime.now().strftime("%d/%m/%Y")} {datetime.datetime.now().strftime("%H:%M")}\n
{tabulate(tabela_final, headers=headers)}\n
Itens: {len(tabela_final)} 
Total: R${total_compra:.2f}
""")  
    
def gerar_lista_clientes():    
    print("Fechamento do caixa")
    print(f"Data: {datetime.datetime.now().strftime("%d/%m/%Y")} {datetime.datetime.now().strftime("%H:%M")}\n")
    print(tabulate(list(zip(lista_clientes, lista_totais)), headers=["Cliente", "Total"]))
    print()

    produtos_fora_estoque = []
    print("\nProdutos fora de estoque:")
    for produto in ler_produtos():
        if produto[2] < 1:
            produtos_fora_estoque.append(produto[1])
            print(produto[1])
    if len(produtos_fora_estoque) == 0:
        print("Não há produtos fora de estoque.")