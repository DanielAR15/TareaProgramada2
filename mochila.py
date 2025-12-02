from dataclasses import dataclass
from typing import List
from tiempo import MedidorTiempo

@dataclass
class SolucionMochila:
    """
    Estructura del problema de la mochila 0-1.
    
    Atributos:
        seleccionados --> Lista de ítems escogidos.
        beneficio --> Beneficio total alcanzado.
        peso_total --> Peso total de los ítems seleccionados.
        soluciones_factibles --> Cantidad de soluciones evaluadas.
        tiempo --> Duración del cálculo usando MedidorTiempo.
    """
    seleccionados: List[int]
    beneficio: int
    peso_total: int
    soluciones_factibles: int = 0
    tiempo: str = ""

class ProblemaMochila:
    """
    Representa una instancia del problema de la mochila 0-1.
    """

    def __init__(self, peso, beneficio, capacidad, n):
        self.peso = peso
        self.beneficio = beneficio
        self.capacidad = capacidad
        self.n = n

    def busqueda_greedy(self) -> SolucionMochila:
        """
        Algoritmo greedy basado en la relación beneficio/peso.
        Selecciona ítems en orden descendente por su razón.
        """
        
        reloj = MedidorTiempo()
        reloj.cargar_tiempo()

        objetos = list(range(1, self.n + 1))

        objetos.sort(key=lambda i: self.beneficio[i] / self.peso[i], reverse=True)
        
        seleccionados = []
        beneficio_total = 0
        peso_total = 0
    
        for i in objetos:
            if peso_total + self.peso[i] <= self.capacidad:
                seleccionados.append(i)
                beneficio_total += self.beneficio[i]
                peso_total += self.peso[i]
        
        # Mide tiempo total
        tiempo = reloj.intervalo_tiempo()

        return SolucionMochila(
            seleccionados=seleccionados,
            beneficio=beneficio_total,
            peso_total=peso_total,
            soluciones_factibles=1,
            tiempo=reloj.formato_tiempo(tiempo)
        )

    def busqueda_exhaustiva_pura(self) -> SolucionMochila:
        """
        Búsqueda exhaustiva pura.
        Evalua las combinaciones posibles de ítems en la mochila.
        """
        
        # Inicia cronómetro
        reloj = MedidorTiempo()
        reloj.cargar_tiempo()
        
        mejor_beneficio = 0
        mejor_sol = []
        soluciones_factibles = 0
        
        def backtrack(i, peso_actual, beneficio_actual, seleccionados):
            """
            Backtracking estándar sin podas.
            i: índice del ítem actual.
            """
            nonlocal mejor_beneficio, mejor_sol, soluciones_factibles
            
            if i > self.n:
                soluciones_factibles += 1
                if beneficio_actual > mejor_beneficio:
                    mejor_beneficio = beneficio_actual
                    mejor_sol = seleccionados[:]
                return

            backtrack(i + 1, peso_actual, beneficio_actual, seleccionados)
            
            if peso_actual + self.peso[i] <= self.capacidad:
                seleccionados.append(i)
                backtrack(i + 1,
                          peso_actual + self.peso[i],
                          beneficio_actual + self.beneficio[i],
                          seleccionados)
                seleccionados.pop()
        
        backtrack(1, 0, 0, [])
        
        tiempo = reloj.intervalo_tiempo()
        
        return SolucionMochila(
            seleccionados=mejor_sol,
            beneficio=mejor_beneficio,
            peso_total=sum(self.peso[i] for i in mejor_sol),
            soluciones_factibles=soluciones_factibles,
            tiempo=reloj.formato_tiempo(tiempo)
        )

    def busqueda_exhaustiva_ra(self) -> SolucionMochila:
        """
        Búsqueda exhaustiva con Ramificación y Acot.
        No explora ramas que no pueden superar el mejor beneficio encontrado hasta el momento.
        """
        # Inicia cronómetro
        reloj = MedidorTiempo()
        reloj.cargar_tiempo()
        
        mejor_beneficio = 0
        mejor_sol = []
        soluciones_factibles = 0
        
        objetos = list(range(1, self.n + 1))
        objetos.sort(key=lambda i: self.beneficio[i] / self.peso[i], reverse=True)
        
        def cota_superior(indice, peso_actual, beneficio_actual):
            """
            Calcula la cota superior.
            Sirve para decidir si una rama debe podarse.
            """
            restante = self.capacidad - peso_actual
            cota = beneficio_actual
            
            for j in range(indice, self.n):
                obj = objetos[j]
                if self.peso[obj] <= restante:
                    cota += self.beneficio[obj]
                    restante -= self.peso[obj]
                else:
                    cota += (self.beneficio[obj] / self.peso[obj]) * restante
                    break
            return cota
        
        def backtrack(ind, p, b, sel):
            """
            Backtracking con poda por cota superior.
            """
            nonlocal mejor_beneficio, mejor_sol, soluciones_factibles

            if ind == self.n:
                soluciones_factibles += 1
                if b > mejor_beneficio:
                    mejor_beneficio = b
                    mejor_sol = sel[:]
                return
            
            if cota_superior(ind, p, b) <= mejor_beneficio:
                return
            
            obj = objetos[ind]

            if p + self.peso[obj] <= self.capacidad:
                sel.append(obj)
                backtrack(ind + 1,
                        p + self.peso[obj],
                        b + self.beneficio[obj],
                        sel)
                sel.pop()

            backtrack(ind + 1, p, b, sel)

        
        backtrack(0, 0, 0, [])
        
        tiempo = reloj.intervalo_tiempo()
        
        return SolucionMochila(
            seleccionados=mejor_sol,
            beneficio=mejor_beneficio,
            peso_total=sum(self.peso[i] for i in mejor_sol),
            soluciones_factibles=soluciones_factibles,
            tiempo=reloj.formato_tiempo(tiempo)
        )
