import os
import json
from sistema_rutas import GrafoTransporte

def mostrar_menu():
    print("\nSistema de Ruteo Inteligente")
    print("1. Buscar ruta más rápida")
    print("2. Buscar ruta con menos transbordos")
    print("3. Salir")

def cargar_datos(grafo: GrafoTransporte, datos: dict) -> GrafoTransporte:
    """Carga los datos del JSON al grafo"""
    # Cargar conexiones normales
    for linea, estaciones in datos['lineas'].items():
        for i in range(len(estaciones)-1):
            est1 = estaciones[i]
            est2 = estaciones[i+1]
            tiempo = datos['tiempos'].get(f"{est1}-{est2}", 1)
            grafo.agregar_conexion(est1, est2, linea, tiempo)
    
    # Cargar transbordos
    for transbordo, tiempo in datos['transbordos'].items():
        est1, est2 = transbordo.split('-')
        grafo.agregar_transbordo(est1, est2, tiempo)
    
    return grafo

def main():
    # Cargar datos de la red
    try:
        with open('red_transporte.json', 'r', encoding='utf-8') as f:
            datos = json.load(f)
    except FileNotFoundError:
        print("Error: No se encontró el archivo red_transporte.json")
        return
    except json.JSONDecodeError:
        print("Error: El archivo JSON tiene formato incorrecto")
        return

    grafo = GrafoTransporte()
    grafo = cargar_datos(grafo, datos)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-3): ").strip()

        if opcion == "1":
            origen = input("Ingrese estación origen: ").strip().upper()
            destino = input("Ingrese estación destino: ").strip().upper()
            
            if origen not in grafo.nodos or destino not in grafo.nodos:
                print("Error: Una o ambas estaciones no existen")
                continue
                
            ruta = grafo.encontrar_ruta_optima(origen, destino, 'tiempo')
            
            if ruta:
                tiempo = grafo.calcular_tiempo_ruta(ruta)
                transbordos = grafo.contar_transbordos(ruta)
                print(f"\nRuta más rápida: {' → '.join(ruta)}")
                print(f"Tiempo total: {tiempo} minutos")
                print(f"Transbordos: {transbordos}")
            else:
                print("\nNo se encontró ruta entre las estaciones especificadas")

        elif opcion == "2":
            origen = input("Ingrese estación origen: ").strip().upper()
            destino = input("Ingrese estación destino: ").strip().upper()
            
            if origen not in grafo.nodos or destino not in grafo.nodos:
                print("Error: Una o ambas estaciones no existen")
                continue
                
            ruta = grafo.encontrar_ruta_optima(origen, destino, 'transbordos')
            
            if ruta:
                tiempo = grafo.calcular_tiempo_ruta(ruta)
                transbordos = grafo.contar_transbordos(ruta)
                print(f"\nRuta con menos transbordos: {' → '.join(ruta)}")
                print(f"Tiempo total: {tiempo} minutos")
                print(f"Transbordos: {transbordos}")
            else:
                print("\nNo se encontró ruta entre las estaciones especificadas")

        elif opcion == "3":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Por favor seleccione 1, 2 o 3")

if __name__ == "__main__":
    main()