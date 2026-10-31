import os

### MENÚS ###

def mostrar_menu_inicio():

    valid_options = [1,2,3,4,5,6]
    last_menu = "inicio"
    
    print()
    
    print("Menú: ")
    print()
    print("1. Cargar Archivo de problemas (Pulsar 1)")
    print("2. Ajustar parámetros de ejecución (Pulsar 2)")
    print("3. Ejecutar todo (Pulsar 3)")
    print("4. Consultar estado (Pulsar 4)")
    print("5. Exportar resultados (Pulsar 5)")
    print("6. Salir del programa (Pulsar 6)")
    print()

    return valid_options, last_menu

def mostrar_menu_parametros_ejecucion():

    last_menu = "ajustar parámetros de ejecución" #Por si luego es necesario

    try:
        numero_anular = int(input("Introduce el número de núcleos que quieres anular: "))
    except:
        print("Número erroneo")
        numero_anular = mostrar_menu_parametros_ejecucion()

    return numero_anular

def mostrar_menu_cargar_json():

    last_menu = "mostrar menú json" #Por si luego es necesario

    try:
        ruta = os.path(input("Introduce una ruta válida del equipo de donde extraer el .json: "))
    except:
        print("Ruta inválida")

    return ruta

def user_request(valid_options, last_menu):

    try: 
        comando = int(input("Introduce un comando válido: "))

        if comando not in valid_options:
            print("Comando no válido, introduzca comando válido")
            return return_last_menu(last_menu)
        elif comando in valid_options:
            if comando == 1 and last_menu == "inicio":
                return mostrar_menu_cargar_json()
            elif comando == 2 and last_menu == "inicio":
                return mostrar_menu_parametros_ejecucion()
            else:
                return comando
    except:
        print("ERROR, volviendo al último menú...")
        return return_last_menu(last_menu)
        
def return_last_menu(last_menu):

    if last_menu == "inicio":
        valid_options, last_menu = mostrar_menu_inicio()
        user_request(valid_options, last_menu)

        return None

valid_options, last_menu = mostrar_menu_inicio()
salida_user_request = user_request(valid_options, last_menu)

