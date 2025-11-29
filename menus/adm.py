import sys
from pathlib import Path
from tabulate import tabulate
from datetime import datetime

sistema_caixa_path = Path(__file__).parent.parent / 'sistema_caixa'
sys.path.insert(0, str(sistema_caixa_path))

from banco import session
from models import *

def menu():
    try:
        clientes_ou_produtos = int(input("""
========== MENU ==========
1 - Clientes
2 - Produtos
3 - Sair
"""))

        if clientes_ou_produtos == 1:
            com_compras_ou_sem = int(input("""
1 - Clientes com compras
2 - Clientes sem compras
"""))
            
            if com_compras_ou_sem == 1:
                menu_clientes_compras()
            elif com_compras_ou_sem == 2:
                listar_clientes_sem_compras()
        elif clientes_ou_produtos == 2:
            crud()
        elif clientes_ou_produtos == 3:
            print("Saindo do sistema...")
            return False  
        else:
            print("Comando inválido")
        
        return True 

    except Exception as e:
        print(f"Erro: {e}")
        return True  

def listar_clientes():
    try:
        clientes = session.query(Cliente).all()

        if not clientes:
            print("Nenhum cliente cadastrado ainda.")
            return
        
        tabela_clientes = []
        for cliente in clientes:
            tabela_clientes.append([
                cliente.id_cliente,
                cliente.nome
            ])

        print("\n========== LISTA DE CLIENTES ==========")
        print(tabulate(tabela_clientes, headers=["ID", "Nome"]))
        print()

    except Exception as e:
        print(f"Erro ao listar clientes: {e}")

def menu_clientes_compras():
    try:
        opcao = int(input("""
========== CLIENTES COM COMPRAS ==========
1 - Consultar compras de um cliente
2 - Clientes que mais compram
3 - Clientes que mais gastam
Escolha uma opção: """))

        if opcao == 1:
            consultar_compras_cliente()
        elif opcao == 2:
            clientes_mais_compram()
        elif opcao == 3:
            clientes_mais_gastam()
        else:
            print("Comando inválido")
        
    except Exception as e:
        print(f"Erro: {e}")

def consultar_compras_cliente():
    try:
        id_cliente = int(input("Digite o ID do cliente para a consulta: "))
        cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()

        if not cliente:
            print("Cliente não encontrado")
            return
        
        compras = session.query(Compras).filter_by(id_cliente=id_cliente).all()
        compras_ordenadas = sorted(compras, key=lambda c: datetime.strptime(c.data_hora, "%d/%m/%Y %H:%M"), reverse=True)

        if not compras_ordenadas:
            print(f"\nCliente {cliente.nome} (ID: {id_cliente}) não tem compras.")
            return

        tabela_compras = []
        for compra in compras_ordenadas:
            itens_compra = session.query(Itens).filter_by(id_compra=compra.id_compra).all()
            total = sum(item.quantidade * item.preco for item in itens_compra)

            tabela_compras.append([
                compra.id_compra,
                compra.data_hora,
                f"R${total:.2f}"
            ])

        print(f"\n========== COMPRAS DO CLIENTE: {cliente.nome} ==========\n")
        print(tabulate(tabela_compras, headers=["ID Compra", "Data/Hora", "Total"]))
        print()

        id_compra = int(input("Digite o ID da compra para ver os detalhes (ou 0 para voltar): "))
        if id_compra != 0:
            exibir_nota_fiscal(id_compra, id_cliente)

    except ValueError:
        print("ID inválido")
    except Exception as e:
        print(f"Erro: {e}")

def exibir_nota_fiscal(id_compra, id_cliente):
    try:
        compra = session.query(Compras).filter_by(id_compra=id_compra, id_cliente=id_cliente).first()

        if not compra:
            print("Compra não encontrado")
            return
        
        cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
        itens = session.query(Itens).filter_by(id_compra=id_compra).all()

        if not itens:
            print("Compra sem itens.")
            return

        tabela_itens = []
        total_compra = 0

        for i, item in enumerate(itens):
            produto = session.query(Produto).filter_by(id_produto=item.id_produto).first()
            total_item = item.quantidade * item.preco
            total_compra += total_item

            tabela_itens.append([
                i,
                produto.nome if produto else f"Produto ID {item.id_produto}",
                item.quantidade,
                f"R${item.preco:.2f}",
                f"R${total_item:.2f}"
            ])

        print("========== NOTA FISCAL ==========")
        print(f"Cliente: {cliente.nome} (ID: {cliente.id_cliente})")
        print(f"Data/Hora: {compra.data_hora}")
        print(f"ID da Compra: {compra.id_compra}\n")
        print(tabulate(tabela_itens, headers=["Item", "Produto", "Quantidade", "Preço Unit.", "Total"]))
        print(f"\nTotal da Compra: R$ {total_compra:.2f}")

    except Exception as e:
        print(f"Erro {e}")

def clientes_mais_compram():
    try:
        clientes = session.query(Cliente).all()

        clientes_com_contagem = []
        for cliente in clientes:
            num_compras = session.query(Compras).filter_by(id_cliente=cliente.id_cliente).count()
            
            if num_compras > 0:
                clientes_com_contagem.append({
                    'cliente': cliente,
                    'num_compras': num_compras
                })

        if not clientes_com_contagem:
            print("Nenhum cliente com compras registradas.")
            return

        clientes_com_contagem.sort(key=lambda x: x['num_compras'], reverse=True)

        tabela = []
        for item in clientes_com_contagem:
            tabela.append([
                item['cliente'].id_cliente,
                item['cliente'].nome,
                item['num_compras']
            ])

        print("\n========== CLIENTES QUE MAIS COMPRAM ==========")
        print(tabulate(tabela, headers=["ID", "Nome", "Número de Compras"]))
        print()

    except Exception as e:
        print(f"Erro {e}")

def clientes_mais_gastam():
    try:
        clientes = session.query(Cliente).all()

        clientes_com_total = []
        for cliente in clientes:
            compras = session.query(Compras).filter_by(id_cliente=cliente.id_cliente).all()
            total_gasto = 0

            for compra in compras:
                itens = session.query(Itens).filter_by(id_compra=compra.id_compra).all()
                total_compra = sum(item.quantidade * item.preco for item in itens)
                
                total_gasto += total_compra

            if total_gasto > 0:
                clientes_com_total.append({
                    'cliente': cliente,
                    'total_gasto': total_gasto
                })
        
        if not clientes_com_total:
            print("Nenhum cliente com compras registradas.")
            return

        clientes_com_total.sort(key=lambda x: x['total_gasto'], reverse=True)

        tabela = []
        for item in clientes_com_total:
            tabela.append([
                item['cliente'].id_cliente,
                item['cliente'].nome,
                f"R${item['total_gasto']:.2f}"
            ])

        print("\n========== CLIENTES QUE MAIS GASTAM ==========")
        print(tabulate(tabela, headers=["ID", "Nome", "Total Gasto"]))
        print()

    except Exception as e:
        print(f"Erro {e}")

def listar_clientes_sem_compras():
    try:
        clientes = session.query(Cliente).all()
        
        clientes_sem_compras = []
        for cliente in clientes:
            num_compras = session.query(Compras).filter_by(id_cliente=cliente.id_cliente).count()
            if num_compras == 0:
                clientes_sem_compras.append([
                    cliente.id_cliente,
                    cliente.nome
                ])
        
        if not clientes_sem_compras:
            print("\nTodos os clientes possuem compras registradas.")
            return
        
        print("\n========== CLIENTES SEM COMPRAS ==========")
        print(tabulate(clientes_sem_compras, headers=["ID", "Nome"]))
        print()
        
    except Exception as e:
        print(f"Erro ao listar clientes sem compras: {e}")




