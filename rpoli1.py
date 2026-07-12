# 1_rpoli.py

import modelo as mod
import anova
import hipotesis
import tabla_f
import vandermonde
import constructor
import util_datos

# ---- datos de ejemplo ---- X_DEF es vector para polinomial
X_DEF = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0 , 9.0 , 10.0]
Y_DEF = [3.1, 3.8, 4.2, 3.9, 4.7 , 5.6 , 4.8, 6.5 , 8.1, 15.6]
K_DEF = 2

# ---- R2 y R2 ajustado ----
def calcular_r2(res):
    SCR = res["SCR"]
    SCT = res["SCT"]
    n   = res["n"]
    p   = res["p"]
    gl_err = res["gl_err"]
    gl_tot = res["gl_tot"]
    r2 = SCR / SCT
    r2a = 1.0 - (res["SCE"] / gl_err) / (SCT / gl_tot)
    return r2, r2a

# ---- ANOVA extendido con R2 ----
def mostrar_anova_pol(res, grado):
    print("--MODELO GRADO " + str(grado) + "--")
    F = anova.mostrar(res)
    r2, r2a = calcular_r2(res)
    print("R2=" + str(round(r2, 4)))
    print("R2aj=" + str(round(r2a, 4)))
    CME = res["SCE"] / res["gl_err"]
    fc  = tabla_f.f_critico(res["gl_reg"], res["gl_err"], 0.05)
    print("F_tab(.05)=" + str(fc))
    if F > fc:
        print("Regresion SIGNIFICATIVA")
    else:
        print("Regresion NO significativa")

# ---- SS secuencial ----
def rellenar(texto, longitud):
    s = str(texto)
    espacios = longitud - len(s)
    if espacios > 0:
        return s + " " * espacios
    return s

def ss_secuencial(x, y, grado_max):
    print("--SS SECUENCIAL--")
    resultados = {}
    for k in range(1, grado_max + 1):
        if len(x) < k + 2:
            print("Grado " + str(k) + ": sin gl")
            continue
        X = vandermonde.construir(x, k)
        resultados[k] = mod.ajustar(X, y, con_intercepto=True)

    print("Grd|SCE     |CME    ")
    for k in sorted(resultados.keys()):
        r = resultados[k]
        cme = r["SCE"] / r["gl_err"]
        print(str(k) + "  |" +
              rellenar(round(r["SCE"], 4), 9) + "|" +
              str(round(cme, 4)))

    print()
    print("Termino|SS(xj) |F     |Dec")
    for k in range(2, grado_max + 1):
        if k not in resultados or k - 1 not in resultados:
            continue
        r_f = resultados[k]
        r_r = resultados[k - 1]
        SS  = r_r["SCE"] - r_f["SCE"]
        CME = r_f["SCE"] / r_f["gl_err"]
        gl_num = r_f["gl_reg"] - r_r["gl_reg"]
        if gl_num == 0:
            gl_num = 1
        F   = (SS / gl_num) / CME if CME != 0 else 0
        fc  = tabla_f.f_critico(gl_num, r_f["gl_err"], 0.05)
        dec = "SI" if F > fc else "NO"
        num_vars = len(x[0]) if isinstance(x[0], list) else 1
        et  = "x^" + str(k) if num_vars == 1 else "x1..v^" + str(k)
        print(rellenar(et, 8) + "|" +
              rellenar(round(SS, 4), 8) + "|" +
              rellenar(round(F, 3), 7) + "|" + dec)

# ---- prueba de hipotesis ----
def menu_hipotesis(res):
    while True:
        op = input("Probar hipotesis? 1/0: \n")
        if op != "1":
            break
        print("1=guiado  2=manual")
        modo = input("Modo: \n")
        if modo == "2":
            print("K filas;cols,: (filas sep con :)")
            tk = input("> ")
            tm = input("m vector,: \n")
            K = []
            for fila in tk.split(":"):
                K.append([float(v) for v in fila.split(",")])
            m = [float(v) for v in tm.split(",")]
        else:
            K, m = constructor.construir(res, tipo="pol")

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

# ---- menu principal ----
def menu_principal():
    x_mem = []
    y_mem = []
    while True:
        print("==REG.POLINOMIAL==")
        print("1.Ajustar modelo")
        print("2.SS secuencial")
        print("3.Ambos")
        print("4.Salir")
        op = input(">")
        if op == "4":
            break
        if op not in ["1", "2", "3"]:
            continue

        x, y = util_datos.pedir_xy(x_mem, y_mem, X_DEF, Y_DEF, es_matriz="auto")
        x_mem = x
        y_mem = y
        
        tk = input("Que grado polinomial (k) deseas probar?\n> ")
        k = 2 if tk.strip() == "" else int(tk)

        if op in ["1", "3"]:
            X = vandermonde.construir(x, k)
            res = mod.ajustar(X, y, con_intercepto=True)
            num_vars = len(x[0]) if isinstance(x[0], list) else 1
            res["num_vars"] = num_vars
            print("BETA:")
            et = vandermonde.etiquetas_pol(k, num_vars)
            for i in range(len(et)):
                print(" " + et[i] + "=" + str(round(res["beta"][i], 4)))
            mostrar_anova_pol(res, k)
            menu_hipotesis(res)

        if op in ["2", "3"]:
            ss_secuencial(x, y, k)

menu_principal()
