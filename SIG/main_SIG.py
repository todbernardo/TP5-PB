import sys
from pathlib import Path

menus_path = Path(__file__).parent.parent / 'menus'
sys.path.insert(0, str(menus_path))

from adm import menu

while True:
    continuar = menu()
    if not continuar: 
        break