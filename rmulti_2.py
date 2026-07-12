# 2_rmultiple.py
# MENU MAESTRO para Regresion Lineal Multiple (matrices de datos crudos).
# Reutiliza: matriz, inversa, modelo, anova, hipotesis, tabla_f, constructor

import modelo as mod
import anova
import hipotesis
import tabla_f
import constructor
import util_datos

# ---- datos de ejemplo ---- X_def es matriz o vector 
X_DEF = [[1.0,1.0], [2.0,1.0], [3.0,1.0], [4.0,1.0], [5.0,1.0], [6.0,2.0], [7.0,3.0], [8.0,4.0] , [9.0,5.0] , [10.0,6.0]]
Y_DEF = [3.1, 3.8, 4.2, 3.9, 4.7 , 5.6 , 4.8, 6.5 , 8.1, 15.6]

def calcular_r2(res):
    SCR = res["SCR"]
    SCT = res["SCT"]
    r2 = SCR / SCT
    r2a = 1.0 - (res["SCE"] / res["gl_err"]) / (SCT / res["gl_tot"])
    return r2, r2a

def mostrar_anova_mlr(res):
    print("--MODELO MLR--")
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

def menu_hipotesis(res):
    while True:
        op = input("Probar hipotesis? 1/0: \n")
        if op != "1":
            break
        print("1=guiado  2=manual")
        modo = input("Modo: \n")
        if modo == "2":
            print("K filas;cols: (filas sep con ;)")
            tk = input("> ")
            tm = input("m vector: ")
            K = []
            for fila in tk.split(";"):
                K.append([float(v) for v in fila.split(",")])
            m = [float(v) for v in tm.split(",")]
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
        print("== REGRESION MLR ==")
        print("1.Ajustar modelo")
        print("2.Salir")
        op = input(">")
        if op == "2":
            break
        if op != "1":
            continue

        X, y = util_datos.pedir_xy(x_mem, y_mem, X_DEF, Y_DEF, es_matriz=True)
        x_mem = X
        y_mem = y
        
        # Ajustamos el modelo (el intercepto lo agrega modelo.py automaticamente)
        res = mod.ajustar(X, y, con_intercepto=True)
        print("BETA:")
        et = constructor.etiquetas_mlr(res)
        for i in range(len(et)):
            print(" " + et[i] + "=" + str(round(res["beta"][i], 4)))
        mostrar_anova_mlr(res)
        menu_hipotesis(res)

menu_principal()
