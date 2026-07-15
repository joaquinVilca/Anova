# rmulti_sin_intercepto.py
# MENU MAESTRO para Regresion Lineal Multiple SIN INTERCEPTO (por el origen).
# Reutiliza: matriz, inversa, modelo, anova, hipotesis, tabla_f, constructor

import modelo as mod
import anova
import hipotesis
import tabla_f
import constructor
import util_datos
import modulo_anova
import var_cov

# ---- datos de ejemplo ---- 
# Ojo: No incluimos columna de 1s en X_DEF porque el modelo no tiene intercepto.
Y_dat = [40, 45, 50, 55, 60, 70, 65, 65, 75, 75, 80, 100, 90, 95, 85]
X1_dat = [9, 8, 9, 8, 7, 6, 6, 8, 5, 5, 5, 3, 4, 3, 4]
X2_dat = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
X3_dat = [10, 14, 12, 13, 11, 15, 16, 17, 22, 19, 20, 23, 18, 24, 21]
X4_dat = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

TODAS_LAS_X = [X1_dat, X2_dat, X3_dat, X4_dat]

def calcular_r2(res):
    SCR = res["SCR"]
    SCT = res["SCT"]
    # Para modelos sin intercepto, el R2 "crudo" o sin centrar es:
    r2 = SCR / SCT
    r2a = 1.0 - (res["SCE"] / res["gl_err"]) / (SCT / res["gl_tot"])
    return r2, r2a

def mostrar_teoria():
    print("\n" + "="*40)
    print(" TEORIA: REGRESION SIN INTERCEPTO")
    print("="*40)
    print("1. Modelo General: Y = X*B + e  (sin columna de 1s)")
    print("   La linea o plano de regresion pasa obligatoriamente por el origen.")
    print("\n2. Estimacion MCO:")
    print("   B = (X'X)^-1 * X'Y")
    print("\n3. Descomposicion de Varianza (No Centrada):")
    print("   SCT (Total) = Y'Y  (No se resta n*(Y_bar)^2)")
    print("   SCR (Regresion) = B'X'Y")
    print("   SCE (Error) = Y'Y - B'X'Y")
    print("\n4. Grados de Libertad:")
    print("   gl(Total) = n")
    print("   gl(Regresion) = p  (Numero de variables en X)")
    print("   gl(Error) = n - p")
    print("\n5. Coeficiente de Determinacion R^2:")
    print("   R^2 = SCR / SCT (Basado en sumas de cuadrados no centradas)")
    print("   R^2_adj = 1 - CME/CMT")
    print("="*40 + "\n")

def mostrar_anova_mlr(res):
    print("--MODELO MLR (SIN INTERCEPTO)--")
    F = anova.mostrar(res)
    r2, r2a = calcular_r2(res)
    print("R2=" + str(round(r2, 4)))
    print("R2aj=" + str(round(r2a, 4)))
    fc  = tabla_f.f_critico(res["gl_reg"], res["gl_err"], 0.05)
    print("F_tab(.05)=" + str(fc))
    if F > fc:
        print("Regresion SIGNIFICATIVA")
    else:
        print("Regresion NO significativa")

def mostrar_ecuaciones(X, y):
    n = len(y)
    p = len(X[0])
    
    if p == 1:
        sum_x2 = sum(fila[0]**2 for fila in X)
        sum_xy = sum(X[i][0] * y[i] for i in range(n))
        
        print("-- SUMATORIAS --")
        print("n =", n)
        print("sum X^2 =", round(sum_x2, 4))
        print("sum XY =", round(sum_xy, 4))
        
        print("-- ECUACIONES NORMALES (Sin intercepto) --")
        print(str(round(sum_x2, 4)) + " b1 = " + str(round(sum_xy, 4)))
    else:
        print("-- SUMATORIAS MULTIPLES (Sin intercepto) --")
        sum_y = sum(y)
        print("n =", n)
        print("sum Y =", round(sum_y, 4))
        for j in range(p):
            sum_xj = sum(fila[j] for fila in X)
            sum_xj2 = sum(fila[j]**2 for fila in X)
            sum_xjy = sum(X[i][j] * y[i] for i in range(n))
            print("X" + str(j+1) + ": sum X = " + str(round(sum_xj, 4)) + ", sum X^2 = " + str(round(sum_xj2, 4)) + ", sum XY = " + str(round(sum_xjy, 4)))
            
        print("\nEl sistema normal es X'X * B = X'Y")

def menu_ecuaciones(X, y):
    while True:
        op = input("Ver sumatorias (Ecuaciones Normales)? 1/0: \n")
        if op != "1":
            break
        mostrar_ecuaciones(X, y)
        break

def menu_analisis_extendido(res, X, y, et):
    while True:
        print("\n-- ANALISIS EXTENDIDO --")
        print("1. Matriz de Varianzas-Covarianzas")
        print("2. Pruebas t (Significancia Individual)")
        print("3. Prediccion Futura")
        print("4. Volver al menu de hipotesis / principal")
        op = input(">")
        if op == "4":
            break
        elif op == "1":
            S2 = res["SCE"] / res["gl_err"]
            V = var_cov.matriz_var_cov(S2, res["XtX_inv"])
            var_cov.imprimir_var_cov(V, et)
        elif op == "2":
            modulo_anova.imprimir_contribucion(res)
        elif op == "3":
            modulo_anova.calcular_prediccion(res)

def menu_hipotesis(res):
    while True:
        op = input("Probar hipotesis? 1/0: \n")
        if op != "1":
            break
        print("1=guiado  2=manual  3=multiples ceros (ej. b2=b3=0)")
        modo = input("Modo: \n")
        if modo == "2":
            print("K filas;cols: (filas sep con ;)")
            tk = input("> ")
            tm = input("m vector: ")
            K = []
            for fila in tk.split(";"):
                K.append([float(v) for v in fila.split(",")])
            m = [float(v) for v in tm.split(",")]
        elif modo == "3":
            K, m = constructor.construir_ceros(res, tipo="mlr")
        else:
            K, m = constructor.construir(res, tipo="mlr")

        sal = hipotesis.prueba(K, m, res)
        print("Q=" + str(round(sal["Q"], 4)))
        print("F=" + str(round(sal["F"], 4)))
        print("gl1=" + str(sal["gl1"]) + " gl2=" + str(sal["gl2"]))
        fc = tabla_f.f_critico(sal["gl1"], sal["gl2"], 0.05)
        print("F_tab(.05)=" + str(fc))
        if sal["F"] > fc:
            print("SE RECHAZA H0")
        else:
            print("NO se rechaza H0")

def menu_principal():
    x_mem = []
    y_mem = []
    while True:
        print("\n== REGRESION MLR (SIN INTERCEPTO) ==")
        print("1. Ajustar modelo base (guiado)")
        print("2. Analisis completo automatico (Todo de frente)")
        print("3. Ver teoria")
        print("4. Salir")
        op = input(">")
        if op == "4":
            break
        if op == "3":
            mostrar_teoria()
            continue
        if op not in ["1", "2"]:
            continue

        try:
            k = int(input("¿Cuantos X de ejemplo quieres usar? (ENTER=todos): "))
        except ValueError:
            k = len(TODAS_LAS_X)
        k = min(k, len(TODAS_LAS_X))
        
        X_DEF = []
        Y_DEF = Y_dat
        for i in range(len(Y_DEF)):
            X_DEF.append([TODAS_LAS_X[j][i] for j in range(k)])

        X, y = util_datos.pedir_xy(x_mem, y_mem, X_DEF, Y_DEF, es_matriz=True)
        x_mem = X
        y_mem = y
        
        # Ajustamos el modelo (SIN intercepto)
        res = mod.ajustar(X, y, con_intercepto=False)
        et = constructor.etiquetas_mlr(res)
        
        print("\nBETA:")
        for i in range(len(et)):
            print(" " + et[i] + "=" + str(round(res["beta"][i], 4)))
            
        if op == "1":
            # Guiado
            mostrar_anova_mlr(res)
            
            op_ic = input("Ver intervalos de confianza (95%)? 1/0: \n")
            if op_ic == "1":
                modulo_anova.imprimir_intervalos_confianza(res)
                
            menu_analisis_extendido(res, X, y, et)
            menu_ecuaciones(X, y)
            menu_hipotesis(res)
        else:
            # Automático
            mostrar_anova_mlr(res)
            modulo_anova.imprimir_intervalos_confianza(res)
            
            print("\n--- PRUEBAS t INDIVIDUALES ---")
            modulo_anova.imprimir_contribucion(res)
            
            print("\n--- VARIANZAS Y COVARIANZAS ---")
            S2 = res["SCE"] / res["gl_err"]
            V = var_cov.matriz_var_cov(S2, res["XtX_inv"])
            var_cov.imprimir_var_cov(V, et)
            
            print("\n--- ECUACIONES NORMALES ---")
            mostrar_ecuaciones(X, y)
            
            print("\n--- PREDICCION ---")
            modulo_anova.calcular_prediccion(res)
            
            menu_hipotesis(res)

menu_principal()
