from caixa import *
from banco import *
from web_scraping import *

construir_csv()
carregar_clientes()
carregar_produtos()

while True:
    comecar_result = iniciar_atendimento()
    if comecar_result == 1: 
        atendimento()
    elif comecar_result == 2:
        break
    else:
        print("\nComando inválido.\n")

gerar_lista_clientes()


 