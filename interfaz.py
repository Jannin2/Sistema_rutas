# interfaz.py
import json
from sistema_rutas import GrafoTransporte

def mostrar_menu():
    print("\nSistema de Ruteo Inteligente")
    print("1. Buscar ruta más rápida")
    print("2. Buscar ruta con menos transbordos")
    print("3. Salir")

def cargar_datos(grafo: GrafoTransporte, datos: dict) -> GrafoTransporte:
    """
    Carga los datos de la red de transporte al grafo
    
    Args:
        grafo: Instancia de GrafoTransporte
        datos: Diccionario con la estructura de la red
    
    Returns:
        GrafoTransporte: Grafo con los datos cargados
    """
    for linea, estaciones in datos['lineas'].items():
        # Conectar estaciones consecutivas
        for i in range(len(estaciones)-1):
            grafo.agregar_conexion(
                estaciones[i], 
                estaciones[i+1], 
                linea, 
                datos['tiempos'].get(f"{estaciones[i]}-{estaciones[i+1]}", 1)
            )
    
    # Agregar transbordos
    for transbordo, tiempo in datos['transbordos'].items():
        est1, est2 = transbordo.split('-')
        grafo.transbordos[(est1, est2)] = tiempo
        grafo.transbordos[(est2, est1)] = tiempo
    
    return grafo