# modelo.py
# Ajuste de un modelo lineal Y = X*beta + e  (con o sin intercepto)

import matriz
import inversa

def construir_X(X, con_intercepto):
    if not con_intercepto:
        return X
    Xc = []
    for fila in X:
        Xc.append([1.0] + list(fila))
    return Xc

def ajustar(X, y, con_intercepto):
    Xm = construir_X(X, con_intercepto)
    n = len(Xm)
    p = len(Xm[0])

    Xt = matriz.transponer(Xm)
    XtX = matriz.multiplicar(Xt, Xm)
    XtX_inv = inversa.invertir(XtX)
    Xty = matriz.mat_vec(Xt, y)
    beta = matriz.mat_vec(XtX_inv, Xty)

    yhat = matriz.mat_vec(Xm, beta)
    res = matriz.resta_vec(y, yhat)
    SCE = matriz.dot(res, res)
    betaXty = matriz.dot(beta, Xty)

    if con_intercepto:
        ybarra = sum(y) / n
        SCT = matriz.dot(y, y) - n * ybarra * ybarra
        SCR = betaXty - n * ybarra * ybarra
        gl_reg = p - 1
        gl_tot = n - 1
    else:
        SCT = matriz.dot(y, y)
        SCR = betaXty
        gl_reg = p
        gl_tot = n

    gl_err = n - p

    resultado = {}
    resultado["n"] = n
    resultado["p"] = p
    resultado["beta"] = beta
    resultado["XtX_inv"] = XtX_inv
    resultado["yhat"] = yhat
    resultado["residuos"] = res
    resultado["SCE"] = SCE
    resultado["SCR"] = SCR
    resultado["SCT"] = SCT
    resultado["gl_reg"] = gl_reg
    resultado["gl_err"] = gl_err
    resultado["gl_tot"] = gl_tot
    resultado["con_intercepto"] = con_intercepto
    return resultado
