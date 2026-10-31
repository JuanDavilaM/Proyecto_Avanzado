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

def user_request(valid_options, last_menu):
    try: 
        comando = int(input("Introduce un comando válido: "))

        if comando not in valid_options:
            print("Comando no válido, introduzca comando válido")
            return return_last_menu(last_menu)
        elif comando in valid_options:
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

