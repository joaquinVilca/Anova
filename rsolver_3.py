# 3_solver.py

import modulo_anova

XtX = [
    [ 3,  1, -2],
    [ 1,  2,  1],
    [-2,  1,  4]
]

XtY = [
    1,
    7,
    9
]

YtY = 58
n = 10

def mostrar_teoria():
    print("\n" + "="*40)
    print(" TEORIA: SOLUCION DESDE MATRICES RESUMEN")
    print("="*40)
    print("1. Resolucion a partir de (X'X), (X'Y) e Y'Y:")
    print("   Si no se tienen los datos crudos, estas 3 matrices")
    print("   son suficientes para obtener el modelo completo.")
    print("\n2. Ecuaciones Base:")
    print("   B = Inversa(X'X) * (X'Y)")
    print("   SCT = Y'Y - n*(Y_bar)^2")
    print("   SCR = B'(X'Y) - n*(Y_bar)^2")
    print("   SCE = Y'Y - B'(X'Y)")
    print("\n3. Varianzas de los Estimadores:")
    print("   V(B) = CME * Inversa(X'X)")
    print("   La diagonal de Inversa(X'X) da la varianza de cada B_i.")
    print("\n4. Ecuaciones Normales:")
    print("   El sistema lineal es: (X'X) * B = (X'Y)")
    print("="*40 + "\n")

def menu_principal():
    print("Calculando modelo...")
    res = modulo_anova.analizar_modelo(XtX, XtY, YtY, n)
    
    while True:
        print("\n--- MENU DE ANALISIS DE REGRESION ---")
        print("1. Ver Tabla ANOVA Particionada y Betas")
        print("2. Ver Contribucion Individual de Variables (Pruebas t/F)")
        print("3. Probar Hipotesis Multiple Personalizada")
        print("4. Predecir e Intervalos (Nuevo x0)")
        print("5. Ver Intervalos de Confianza de Betas")
        print("6. Ver Matriz Inversa (X^T X)^-1")
        print("7. Ejecutar Todo")
        print("8. Ver Teoria")
        print("9. Salir")
        op = input("> ")
        
        if op == "1":
            print("Beta:")
            for b in res["beta"]:
                print(round(b, 4))
            modulo_anova.imprimir_anova(res)
        elif op == "2":
            modulo_anova.imprimir_contribucion(res)
        elif op == "3":
            modulo_anova.interactuar_hipotesis(res)
        elif op == "4":
            modulo_anova.calcular_prediccion(res)
        elif op == "5":
            print("Elige alpha/2 (ej. 1% -> 0.01, 5% -> 0.05) o presiona ENTER para 95% (0.025):")
            val = input("> ")
            alpha = 0.05
            if val.strip():
                try:
                    alpha2 = float(val)
                    if alpha2 >= 1.0: alpha2 = alpha2 / 100.0 # Por si ponen 5 en lugar de 0.05
                    alpha = alpha2 * 2
                except:
                    print("Valor invalido. Se usara 95% (alpha=0.05).")
            modulo_anova.imprimir_intervalos_confianza(res, alpha)
        elif op == "6":
            print("\n--- MATRIZ INVERSA (X^T X)^-1 ---")
            inv = res["XtX_inv"]
            for fila in inv:
                print([round(v, 6) for v in fila])
        elif op == "7":
            print("Beta:")
            for b in res["beta"]:
                print(round(b, 4))
            modulo_anova.imprimir_anova(res)
            modulo_anova.imprimir_contribucion(res)
            modulo_anova.interactuar_hipotesis(res)
            modulo_anova.calcular_prediccion(res)
            modulo_anova.imprimir_intervalos_confianza(res, 0.05)
            print("\n--- MATRIZ INVERSA (X^T X)^-1 ---")
            for fila in res["XtX_inv"]:
                print([round(v, 6) for v in fila])
        elif op == "8":
            mostrar_teoria()
        elif op == "9":
            break
        else:
            print("Opcion invalida.")

menu_principal()
