import json

from cli import mostrar_menu_cargar_json

# Opening JSON file

def read_json(ruta):

    with open(file=ruta) as json_file:
        data = json.load(json_file)

    return data

