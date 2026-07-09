# inversa.py
# Inversa de una matriz cuadrada por el metodo de Gauss-Jordan.

def identidad(n):
    I = []
    for i in range(n):
        fila = []
        for j in range(n):
            if i == j:
                fila.append(1.0)
            else:
                fila.append(0.0)
        I.append(fila)
    return I

def copiar(A):
    C = []
    for fila in A:
        C.append(fila[:])
    return C

def invertir(A):
    n = len(A)
    M = copiar(A)
    I = identidad(n)
    for col in range(n):
        piv = M[col][col]
        if abs(piv) < 1e-12:
            for f in range(col + 1, n):
                if abs(M[f][col]) > 1e-12:
                    M[col], M[f] = M[f], M[col]
                    I[col], I[f] = I[f], I[col]
                    piv = M[col][col]
                    break
        for j in range(n):
            M[col][j] = M[col][j] / piv
            I[col][j] = I[col][j] / piv
        for f in range(n):
            if f != col:
                factor = M[f][col]
                if factor != 0.0:
                    for j in range(n):
                        M[f][j] = M[f][j] - factor * M[col][j]
                        I[f][j] = I[f][j] - factor * I[col][j]
    return I
