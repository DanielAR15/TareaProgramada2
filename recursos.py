import time
import math
from dataclasses import dataclass
from typing import List


@dataclass
class SolucionDistribucion:
    """
    Representa la solución del Problema de Distribución de un Recurso.

    Atributos:
        distribucion: Lista que indica cuántas unidades se asignan a cada columna.
        ganancia: Ganancia total obtenida para la asignación dada.
        soluciones_factibles: Número de soluciones evaluadas (cuando aplica).
        intentos: Cantidad de nodos o asignaciones generadas.
        tiempo: Tiempo total de ejecución del método.
    """
    distribucion: List[int]
    ganancia: float
    soluciones_factibles: int = 0
    intentos: int = 0
    tiempo: float = 0.0


class DistribucionRecursos:
    """
    Implementación del Problema de Distribución de un Recurso.

    El problema consiste en distribuir una cantidad total R de un recurso
    entre M columnas, donde la tabla tabla[u][j] indica la ganancia de asignar
    u unidades del recurso a la columna j.

    Se implementan tres métodos:
    - Búsqueda Greedy
    - Búsqueda Exhaustiva Pura
    - Búsqueda Exhaustiva con Ramificación y Acotamiento
    """

    def __init__(self, tabla, R, M=None):
        """
        Inicializa el problema.

        Args:
            tabla: Matriz donde tabla[u][j] indica la ganancia por u unidades en la columna j.
            R: Cantidad total de unidades de recurso a repartir.
        """
        self.tabla = tabla
        self.R = R
        self.M = M if M else len(tabla[0])
        self.maximo = len(tabla) - 1 # Máximo de unidades que se puede dar a una columna

    # --------------------------------------------------------------------
    # MÉTODO GREEDY
    # --------------------------------------------------------------------
    def busqueda_greedy(self) -> SolucionDistribucion:
        """
        Búsqueda Greedy:

        En cada paso se asigna UNA unidad de recurso a la columna cuyo
        incremento marginal sea mayor.

        Returns:
            Instancia de SolucionDistribucion con la asignación y ganancia obtenidas.
        """
        distribucion = [0] * (self.M + 1)
        tiempo = time.time()

        # Función que calcula el valor marginal de agregar 1 unidad a la columna j
        def margen(j):
            u = distribucion[j]
            if u >= self.maximo:
                return -math.inf
            return self.tabla[u + 1][j] - self.tabla[u][j]

        # Se asignan R unidades, una por una
        for _ in range(self.R):
            # Escoger la columna con mejor ganancia marginal
            mejor = max(range(self.M), key=lambda j: margen(j))
            if margen(mejor) == -math.inf:  # No se puede asignar más
                break
            distribucion[mejor] += 1

        # Calcular ganancia total
        ganancia = sum(self.tabla[distribucion[j]][j] for j in range(self.M))
        t = time.time() - tiempo

        return SolucionDistribucion(
            distribucion=distribucion,
            ganancia=ganancia,
            tiempo=t
        )

    # --------------------------------------------------------------------
    # BÚSQUEDA EXHAUSTIVA PURA
    # --------------------------------------------------------------------
    def busqueda_exhaustiva_pura(self) -> SolucionDistribucion:
        """
        Búsqueda Exhaustiva Pura:

        Explora todas las posibles composiciones de R unidades en M columnas.

        Solo se consideran soluciones válidas donde ninguna columna recibe
        más unidades que el máximo permitido.

        Returns:
            La mejor solución encontrada en todo el espacio de búsqueda.
        """
        mejor_valor = -math.inf
        mejor_distribucion = None
        intentos = 0
        tiempo = time.time()

        def compositions(T, M):
            """
            Genera todas las composiciones de T unidades en M columnas.
            Ejemplo: compositions(3,2) → (0,3),(1,2),(2,1),(3,0)
            """
            if M == 1:
                yield (T,)
            else:
                for i in range(T + 1):
                    for rest in compositions(T - i, M - 1):
                        yield (i,) + rest

        # Explorar cada composición posible
        for distribucion in compositions(self.R, self.M):
            intentos += 1

            # Establece el límite máximo por columna
            if any(a > self.maximo for a in distribucion):
                continue

            # Calcular ganancia
            valor = sum(self.tabla[distribucion[j]][j] for j in range(self.M))

            # Guardar mejor
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_distribucion = distribucion

        t = time.time() - tiempo

        return SolucionDistribucion(
            distribucion=[0] + list(mejor_distribucion),
            ganancia=mejor_valor,
            soluciones_factibles=intentos,
            intentos=intentos,
            tiempo=t
        )

    # --------------------------------------------------------------------
    # BÚSQUEDA CON RAMIFICACIÓN Y ACOTAMIENTO
    # --------------------------------------------------------------------
    def busqueda_exhaustiva_ra(self) -> SolucionDistribucion:
        """
        Búsqueda con Ramificación y Acotamiento (RA):

        Explora recursivamente las distribuciones posibles, pero poda ramas
        que no pueden superar la mejor solución encontrada.

        Utiliza una cota superior optimista basada en la mejor ganancia por columna.

        Returns:
            Mejor solución obtenida con podas.
        """
        mejor_valor = -math.inf
        mejor_distribucion = None
        intentos = 0
        tiempo = time.time()

        # Cálculo previo: mejor ganancia disponible por columna
        col_maximo = [0] * (self.M + 1)
        for j in range(1, self.M + 1):
            col_maximo[j] = max(self.tabla[u][j] for u in range(self.maximo + 1))

        def dfs(j, restante, actual_distribucion, suma_actual):
            """
            Función recursiva DFS con poda.

            Args:
                j: Índice de columna actual.
                restante: Unidades por asignar.
                actual_distribucion: Lista con la asignación parcial.
                suma_actual: Ganancia acumulada.
            """
            nonlocal mejor_valor, mejor_distribucion, intentos
            intentos += 1

            # Cota superior optimista: suma_actual + sumatorio de máximos restantes
            optimistic = suma_actual + sum(col_maximo[k] for k in range(j, self.M))

            # Poda si ya no puede superar la mejor solución
            if optimistic <= mejor_valor:
                return

            # Si llegamos al final, validar solución
            if j > self.M:
                if restante == 0 and suma_actual > mejor_valor:
                    mejor_valor = suma_actual
                    mejor_distribucion = actual_distribucion.copy()
                return

            # Probar todas las asignaciones posibles para esta columna
            for u in range(min(self.maximo, restante), -1, -1):
                actual_distribucion.append(u)
                dfs(
                    j + 1,
                    restante - u,
                    actual_distribucion,
                    suma_actual + self.tabla[u][j]
                )
                actual_distribucion.pop()

        dfs(1, self.R, [], 0)
        t = time.time() - tiempo

        return SolucionDistribucion(
            distribucion=[0] + mejor_distribucion,
            ganancia=mejor_valor,
            soluciones_factibles=intentos,
            intentos=intentos,
            tiempo=t
        )
