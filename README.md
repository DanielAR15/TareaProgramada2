# Proyecto - Análisis de algoritmos
### Resolución de Problemas mediante algoritmos de búsqueda

Noelia Ramírez Rodriguez - C36453

Daniel Avilan Rios - C10793 
- - -

Este proyecto implementa cuatro problemas clásicos que pueden resolverse mediante técnicas algorítmicas de búsqueda:

    - Problema de Asignación 1 a 1
    - Problema de Distribución de un Recurso
    - Problema de la Mochila 0-1
    - Problema del Vendedor (TSP)

Cada problema cuenta con una estructura orientada a objetos e implementa tres métodos de búsqueda:

    - Búsqueda Greedy
    - Búsqueda Exhaustiva Pura
    - Búsqueda Exhaustiva con Ramificación y Acotamiento (Branch & Bound)

El sistema integra un menú interactivo en consola basado en la librería Rich, que facilita la navegación y experimentación con los algoritmos.

## Requisitos

-Python 3.10 o superior
-Biblioteca Rich para visualización interactiva en consola

---
## Instalación de dependencias

    pip install rich

---
## Estructura del proyecto

<img width="527" height="188" alt="{25AAAE62-6730-48CE-B660-C6CF90DAE84F}" src="https://github.com/user-attachments/assets/97e8bd8c-4bea-43c4-913a-f9255f84dfc3" />

---
## ejecucion del programa
    Puedes probar el programa de manera interactiva ejecutando:

     - python prueba.py
    
    Si deseas probar todos, hay un file llamado demo que tiene casos escritos para verificar que todo funcione correctamente, si deseas ejecutar ese el comando sería:

    - python demo.py

---
## Menu Principal

 A. Menú de problemas: seleccion de uno de los problemas a elegir.

  A.1 Menú de Métodos de Búsqueda
  
      1. Búsqueda Greedy
      
      2. Búsqueda Exhaustiva Pura
      
      3. Búsqueda Exhaustiva con Ramificación y Acotamiento
      
      4. Regresar

Cada método presenta:

    1. La solución encontrada
    
    2. Ganancia o costo total
    
    3. Número de soluciones evaluadas
    
    4. Tiempo total de ejecución
    
    5. Distribuciones o caminos generados

