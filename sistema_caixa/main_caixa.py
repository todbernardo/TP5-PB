import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'menus'))

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
        print("Comando inválido.\n")

gerar_lista_clientes()


 