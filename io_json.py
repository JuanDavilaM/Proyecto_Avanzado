import json

# Opening JSON file

def read_json(ruta):

    with open(file=ruta) as json_file:
        data = json.load(json_file)

    return data