import os
import multiprocessing

def request_hilos():

    numero_maquina_hilos = os.cpu_count()

    print(f"El número de hilos de la máquina es: {numero_maquina_hilos}")

    numero_anular = int(input("Introduce el número de núcleos que quieres anular: "))

    numero_hilos_usar = numero_maquina_hilos-numero_anular

    if numero_hilos_usar <= 0:
        print("Número incorrecto de hilos")
        request_hilos()
    else: 
        print(f"Número correcto de hilos, se usarán {numero_hilos_usar}")

    return numero_hilos_usar

    