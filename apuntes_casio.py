
from casioplot import *
#import time

# ==========================================
# PALETA DE COLORES (RGB)
# ==========================================
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
GRIS = (100, 100, 100)

def mostrar_pagina(titulo, lineas, num_pag, total_pags):
    """Limpia la pantalla y dibuja el texto de la p  gina actual"""
    clear_screen()
    
    # Dibujar Encabezado (T  tulo)
    draw_string(5, 5, titulo, AZUL, "medium")
    draw_string(5, 25, "-" * 35, GRIS, "small")
    
    # Dibujar el contenido (L  neas de texto)
    y_pos = 40
    for linea in lineas:
        draw_string(5, y_pos, linea, NEGRO, "small")
        y_pos += 15 # Espaciado entre l  neas


        
    # Dibujar Pie de p  gina
    texto_pie = "Pag " + str(num_pag) + "/" + str(total_pags) + " - Presiona [EXE]"
    draw_string(5, 170, texto_pie, ROJO, "small")
    
    # Renderizar en la pantalla
    show_screen()

# ==========================================
# BASE DE DATOS DE APUNTES Y EJEMPLOS
# ==========================================
apuntes = [
    (
        "1. MCO Y REGRESION LINEAL",
        [
            "Modelo general: Y = X*B + e",
            "Formula MCO: B = (X'X)^-1 * X'Y",
            "R^2 = SSR / SST (Bondad de ajuste)",
            "Prueba Global (F): H0: B1=B2=...=0",
            "",
            "Ejemplo (Ventas vs Gasolina):",
            "B_1 = 0.735 (Pendiente)",
            "B_0 = 25.88 (Intercepto)",
            "Y_est = 25.88 + 0.735 * X"
        ]
    ),
    (
        "2. REGRESION SIN INTERCEPTO",
        [
            "Tambien llamada 'Por el origen'.",
            "La matriz X NO tiene la columna de 1s.",
            "Teoria de Searle: Cambian los Grados",
            "de Libertad (GL).",
            "GL Numerador = 1 (si hay 1 restriccion).",
            "La sumatoria de errores no siempre es 0.",
            "No se usa el R^2 tradicional porque",
            "SST no esta centrado en la media."
        ]
    ),
    (
        "3. TIPOS DE ANOVA (SEARLE)",
        [
            "Divide la varianza total en partes.",
            "1 Factor (One-Way): 1 variable categorica.",
            "  -> Ej: 3 tipos de semaforos.",
            "2 Factores (Two-Way): 2 variables + cruz.",
            "Medidas Repetidas: Mismo sujeto en el t.",
            "Efectos Aleatorios: Niveles son muestra",
            "de una poblacion infinita (varianza)."
        ]
    ),
    (
        "4. EJEMPLO ANOVA: SEMAFOROS",
        [
            "Problema: 3 Semaforos, 5 calles c/u.",
            "SST (Var Total) = 995.66",
            "SSTr (Var Entre Grupos) = 789.64",
            "SSE (Var Interna/Error) = 206.02",
            "",
            "MS_Trat = 789.64 / 2 = 394.8",
            "MS_Error = 206.02 / 12 = 17.16",
            "Estadistico F = 394.8 / 17.16 = 23.0",
            "Conclusion: Los retrasos SI difieren."
        ]
    ),
    (
        "5. OPTIMIZACION DE MEMORIA",
        [
            "Para la Casio FX-CG100:",
            "Evitar: matriz.transponer(X)",
            "Multiplicar matrices N x P crea copias",
            "pesadas y causa 'MemoryError'.",
            "",
            "Solucion: Complejidad Espacial O(P^2).",
            "Calcula (X'X) sumando elementos a",
            "medida que lees, sin guardar toda",
            "la matriz de N datos en RAM."
        ]
    )
]

# ==========================================
# MOTOR DEL PROGRAMA PRINCIPAL
# ==========================================
total = len(apuntes)

for i in range(total):
    titulo = apuntes[i][0]
    lineas = apuntes[i][1]
    
    # Muestra en la pantalla gr  fica
    mostrar_pagina(titulo, lineas, i + 1, total)
    
    # Imprime en la consola y espera a que el usuario presione EXE
    print("Mostrando: " + titulo)
   
    if i < total - 1:
        input("Presiona [EXE] para avanzar...")
    else:
        input("Fin de los apuntes. [EXE] para salir.")


show_screen()
print("  Exito en tu curso de Modelos Lineales!")
