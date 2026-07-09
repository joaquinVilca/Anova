# matriz.py
# Operaciones basicas con matrices (listas de listas).
# No usa numpy: la fx-CG100 no lo soporta.

def transponer(A):
    filas = len(A)
    cols = len(A[0])
    T = []
    for j in range(cols):
        fila = []
        for i in range(filas):
            fila.append(A[i][j])
        T.append(fila)
    return T

def multiplicar(A, B):
    filasA = len(A)
    colsA = len(A[0])
    colsB = len(B[0])
    C = []
    for i in range(filasA):
        fila = []
        for j in range(colsB):
            s = 0.0
            for k in range(colsA):
                s = s + A[i][k] * B[k][j]
            fila.append(s)
        C.append(fila)
    return C

def mat_vec(A, v):
    filas = len(A)
    cols = len(A[0])
    r = []
    for i in range(filas):
        s = 0.0
        for j in range(cols):
            s = s + A[i][j] * v[j]
        r.append(s)
    return r

def dot(u, v):
    s = 0.0
    for i in range(len(u)):
        s = s + u[i] * v[i]
    return s

def resta_vec(u, v):
    r = []
    for i in range(len(u)):
        r.append(u[i] - v[i])
    return r

def imprimir_matriz(A, dec=4):
    for fila in A:
        txt = ""
        for x in fila:
            txt = txt + str(round(x, dec)) + " "
        print(txt)
