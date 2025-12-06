from dataclasses import dataclass
from typing import List


@dataclass
class SolucionVendedor:
    """
    Solución para el problema del Vendedor Viajero.
    """
    camino: List[str]
    costo: int
    soluciones_factibles: int = 0


def letra(ciudad: int) -> str:
    """
    Convierte un número 1 -> 'a', 2 -> 'b', etc.
    """
    return chr(ciudad + 96)


class ProblemaVendedor:
    def __init__(self, matriz: List[List[int]], n: int):
        """
        Inicializa el problema del Vendedor Viajero.

        Args:
            matriz: Matriz de distancias.
            n: Número de ciudades.
        """
        self.matriz = matriz
        self.n = n

    def busqueda_greedy(self) -> SolucionVendedor:
        """
        Búsqueda Greedy: siempre elige la ciudad no visitada más cercana.

        Returns:
            Solución del problema.
        """

        sol = SolucionVendedor(
            camino=[None] * (self.n + 2),
            costo=0
        )

        visitado = [False] * (self.n + 1)
        actual = 1

        visitado[1] = True
        sol.camino[1] = letra(1)
        costo_total = 0

        for pos in range(2, self.n + 1):
            mejor = None
            mejor_costo = float('inf')

            for j in range(1, self.n + 1):
                if j != actual and not visitado[j]:
                    if self.matriz[actual][j] < mejor_costo:
                        mejor = j
                        mejor_costo = self.matriz[actual][j]

            visitado[mejor] = True
            costo_total += mejor_costo
            sol.camino[pos] = letra(mejor)
            actual = mejor

        costo_total += self.matriz[actual][1]
        sol.camino[self.n + 1] = letra(1)
        sol.costo = costo_total

        return sol

    def busqueda_exhaustiva_pura(self) -> SolucionVendedor:
        """
        Búsqueda Exhaustiva Pura:
        Explora todas las permutaciones posibles de ciudades.

        Returns:
            Solución óptima (de menor costo).
        """

        sol = SolucionVendedor(
            camino=[None] * (self.n + 2),
            costo=0,
            soluciones_factibles=0
        )

        mejor_camino = None
        mejor_costo = float('inf')

        visitado = [False] * (self.n + 1)
        camino = [None] * (self.n + 2)

        def backtrack(k: int, actual: int, costo_actual: int):
            """
            Función recursiva para explorar todas las rutas posibles.

            Args:
                k: posición actual dentro del camino
                actual: ciudad actual
                costo_actual: costo acumulado hasta este punto
            """
            nonlocal mejor_camino, mejor_costo

            if k == self.n + 1:
                costo_total = costo_actual + self.matriz[actual][1]
                sol.soluciones_factibles += 1

                if costo_total < mejor_costo:
                    mejor_costo = costo_total
                    mejor_camino = camino[:]
                    mejor_camino[self.n + 1] = letra(1)

                return

            for ciudad in range(2, self.n + 1):
                if not visitado[ciudad]:
                    visitado[ciudad] = True
                    camino[k] = letra(ciudad)

                    backtrack(k + 1, ciudad,
                              costo_actual + self.matriz[actual][ciudad])

                    visitado[ciudad] = False

        visitado[1] = True
        camino[1] = letra(1)

        backtrack(2, 1, 0)

        sol.camino = mejor_camino
        sol.costo = mejor_costo

        return sol

    def busqueda_exhaustiva_ra(self) -> SolucionVendedor:
        """
        Búsqueda Exhaustiva con Ramificación y Acotamiento.

        Utiliza una cota inferior de:
            (ciudades restantes) * (menor arista del grafo)

        Returns:
            Mejor solución encontrada.
        """
        sol = SolucionVendedor(
            camino=[None] * (self.n + 2),
            costo=0,
            soluciones_factibles=0
        )

        mejor_camino = None
        mejor_costo = float('inf')

        visitado = [False] * (self.n + 1)
        camino = [None] * (self.n + 2)

        min_arista = min(
            self.matriz[i][j]
            for i in range(1, self.n + 1)
            for j in range(1, self.n + 1)
            if i != j
        )

        def backtrack(k: int, actual: int, costo_actual: int):
            """
            Función recursiva con poda por cota.
            """
            nonlocal mejor_camino, mejor_costo

            restantes = self.n - k + 1
            costo_estimado = costo_actual + restantes * min_arista

            if costo_estimado >= mejor_costo:
                return
            
            if k == self.n + 1:
                costo_total = costo_actual + self.matriz[actual][1]
                sol.soluciones_factibles += 1

                if costo_total < mejor_costo:
                    mejor_costo = costo_total
                    mejor_camino = camino[:]
                    mejor_camino[self.n + 1] = letra(1)

                return

            for ciudad in range(2, self.n + 1):
                if not visitado[ciudad]:
                    visitado[ciudad] = True
                    camino[k] = letra(ciudad)

                    backtrack(k + 1, ciudad,
                              costo_actual + self.matriz[actual][ciudad])

                    visitado[ciudad] = False

        visitado[1] = True
        camino[1] = letra(1)

        backtrack(2, 1, 0)

        sol.camino = mejor_camino
        sol.costo = mejor_costo

        return sol
