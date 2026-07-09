# hipotesis.py
# Prueba de hipotesis lineal general:  H0: K*beta = m
# Q = (K*beta - m)' [K (X'X)^-1 K']^-1 (K*beta - m)
# F = (Q/q) / CME   con  q = numero de filas de K (rango de K)

import matriz
import inversa

def prueba(K, m, resultado):
    beta = resultado["beta"]
    XtX_inv = resultado["XtX_inv"]
    CME = resultado["SCE"] / resultado["gl_err"]

    q = len(K)
    Kb = matriz.mat_vec(K, beta)
    dif = matriz.resta_vec(Kb, m)

    Kt = matriz.transponer(K)
    A = matriz.multiplicar(K, XtX_inv)
    M = matriz.multiplicar(A, Kt)

    if q == 1:
        Minv = [[1.0 / M[0][0]]]
    else:
        Minv = inversa.invertir(M)

    Mdif = matriz.mat_vec(Minv, dif)
    Q = matriz.dot(dif, Mdif)
    F = (Q / q) / CME

    salida = {}
    salida["Kbeta"] = Kb
    salida["diferencia"] = dif
    salida["Q"] = Q
    salida["gl1"] = q
    salida["gl2"] = resultado["gl_err"]
    salida["F"] = F
    salida["CME"] = CME
    return salida
