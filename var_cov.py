# var_cov.py
# Matriz de varianzas y covarianzas de los estimadores MCO, y sus
# correlaciones.   Var(beta_hat) = S2 * (X'X)^-1

def matriz_var_cov(S2, XtX_inv):
    n = len(XtX_inv)
    V = []
    for i in range(n):
        fila = []
        for j in range(n):
            fila.append(S2 * XtX_inv[i][j])
        V.append(fila)
    return V


def varianzas(V):
    # Diagonal principal de V
    return [V[i][i] for i in range(len(V))]


def errores_estandar(V):
    return [V[i][i] ** 0.5 for i in range(len(V))]


def correlacion(V, i, j):
    # r(beta_i, beta_j) = Cov(i,j) / sqrt(Var(i)*Var(j))
    return V[i][j] / ((V[i][i] * V[j][j]) ** 0.5)


def imprimir_var_cov(V, etiquetas):
    print("Matriz de Varianzas y Covarianzas de los estimadores:")
    for i in range(len(V)):
        txt = ""
        for j in range(len(V)):
            txt = txt + str(round(V[i][j], 4)) + "  "
        print(" " + txt)

    print("\nCorrelaciones entre pares de estimadores:")
    for i in range(len(V)):
        for j in range(i + 1, len(V)):
            r = correlacion(V, i, j)
            print(" r(" + etiquetas[i] + "," + etiquetas[j] + ") = " + str(round(r, 4)))
