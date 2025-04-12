from typing import Dict, List, Tuple, Optional
from collections import deque
import heapq

class GrafoTransporte:
    def __init__(self):
        """Inicializa la estructura de datos para la red de transporte"""
        self.nodos: Dict[str, Dict[str, Tuple[int, str]]] = {}  # {estación: {vecino: (tiempo, línea)}}
        self.transbordos: Dict[Tuple[str, str], int] = {}  # {(est1, est2): tiempo_transbordo}
        self.lineas: Dict[str, List[str]] = {}  # {línea: [estaciones]}

    def agregar_estacion(self, estacion: str, linea: str):
        """Añade una estación al grafo si no existe"""
        if linea not in self.lineas:
            self.lineas[linea] = []
        if estacion not in self.lineas[linea]:
            self.lineas[linea].append(estacion)
        
        if estacion not in self.nodos:
            self.nodos[estacion] = {}

    def agregar_conexion(self, est1: str, est2: str, linea: str, tiempo: int):
        """Conecta dos estaciones en la misma línea"""
        self.agregar_estacion(est1, linea)
        self.agregar_estacion(est2, linea)
        
        self.nodos[est1][est2] = (tiempo, linea)
        self.nodos[est2][est1] = (tiempo, linea)

    def agregar_transbordo(self, est1: str, est2: str, tiempo: int):
        """Añade conexión entre líneas diferentes (transbordo)"""
        if (est1, est2) not in self.transbordos:
            self.transbordos[(est1, est2)] = tiempo
            self.transbordos[(est2, est1)] = tiempo

    def encontrar_ruta_optima(self, origen: str, destino: str, criterio: str = 'tiempo') -> List[str]:
        """
        Encuentra la mejor ruta según el criterio especificado
        :param origen: Estación de inicio
        :param destino: Estación final
        :param criterio: 'tiempo' o 'transbordos'
        :return: Lista de estaciones en la ruta óptima
        """
        if origen not in self.nodos or destino not in self.nodos:
            raise ValueError("Estación no encontrada en la red")
        
        if criterio == 'tiempo':
            return self._buscar_por_tiempo(origen, destino)
        elif criterio == 'transbordos':
            return self._buscar_por_transbordos(origen, destino)
        else:
            raise ValueError("Criterio no válido. Use 'tiempo' o 'transbordos'")

    def _buscar_por_tiempo(self, origen: str, destino: str) -> List[str]:
        """Implementa A* para encontrar la ruta más rápida"""
        frontera = []
        heapq.heappush(frontera, (0, origen, []))  # (costo estimado, estación, ruta)
        visitados = set()
        
        while frontera:
            costo, actual, ruta = heapq.heappop(frontera)
            
            if actual == destino:
                return ruta + [actual]
                
            if actual in visitados:
                continue
                
            visitados.add(actual)
            
            for vecino, (tiempo, linea) in self.nodos[actual].items():
                nuevo_costo = costo + tiempo
                heapq.heappush(frontera, (
                    nuevo_costo + self._heuristica_tiempo(vecino, destino),
                    vecino,
                    ruta + [actual]
                ))
        
        return []

    def _buscar_por_transbordos(self, origen: str, destino: str) -> List[str]:
        """Implementa BFS modificado para minimizar transbordos"""
        cola = deque([(origen, [], None)])  # (estación, ruta, línea_anterior)
        visitados = set()
        
        while cola:
            actual, ruta, linea_prev = cola.popleft()
            
            if actual == destino:
                return ruta + [actual]
                
            if actual in visitados:
                continue
                
            visitados.add(actual)
            
            for vecino, (_, linea_actual) in self.nodos[actual].items():
                nueva_ruta = ruta + [actual]
                
                # Priorizar mantener la misma línea
                if linea_actual == linea_prev:
                    cola.appendleft((vecino, nueva_ruta, linea_actual))
                else:
                    cola.append((vecino, nueva_ruta, linea_actual))
        
        return []

    def _heuristica_tiempo(self, a: str, b: str) -> int:
        """Heurística optimista para A* (puede mejorarse con datos reales)"""
        return 0  # En una implementación real usaríamos distancias geográficas

    def contar_transbordos(self, ruta: List[str]) -> int:
        """Cuenta los cambios de línea en una ruta"""
        if len(ruta) < 2:
            return 0
            
        transbordos = 0
        linea_actual = self._obtener_linea(ruta[0], ruta[1])
        
        for i in range(1, len(ruta)-1):
            nueva_linea = self._obtener_linea(ruta[i], ruta[i+1])
            if nueva_linea != linea_actual:
                transbordos += 1
                linea_actual = nueva_linea
                
        return transbordos

    def calcular_tiempo_ruta(self, ruta: List[str]) -> int:
        """Calcula el tiempo total de una ruta incluyendo transbordos"""
        if len(ruta) < 2:
            return 0
            
        tiempo_total = 0
        
        for i in range(len(ruta)-1):
            tiempo, _ = self.nodos[ruta[i]][ruta[i+1]]
            tiempo_total += tiempo
            
            # Añadir tiempo de transbordo si hay cambio de línea
            if i > 0:
                linea_prev = self._obtener_linea(ruta[i-1], ruta[i])
                linea_actual = self._obtener_linea(ruta[i], ruta[i+1])
                if linea_prev != linea_actual:
                    tiempo_transbordo = self.transbordos.get((ruta[i], ruta[i]), 0)
                    tiempo_total += tiempo_transbordo
        
        return tiempo_total

    def _obtener_linea(self, est1: str, est2: str) -> str:
        """Obtiene la línea que conecta dos estaciones adyacentes"""
        return self.nodos[est1][est2][1]

    def obtener_estaciones(self) -> List[str]:
        """Devuelve lista de todas las estaciones"""
        return list(self.nodos.keys())