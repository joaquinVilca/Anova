# util_datos.py
# Modulo compartido para pedir y mantener datos en memoria RAM

def leer_lista(txt):
    r = []
    for p in txt.split(","):
        if p.strip() != "":
            r.append(float(p.strip()))
    return r

def leer_matriz(txt):
    # Formato: 1,2 : 3,4 : 5,6
    M = []
    filas = txt.split(":")
    for f in filas:
        if f.strip() == "":
            continue
        fila = []
        for v in f.split(","):
            if v.strip() != "":
                fila.append(float(v.strip()))
        if len(fila) > 0:
            M.append(fila)
    return M

def asegurar_matriz(X):
    # Si X es una lista simple (1D), la convertimos a matriz de 1 columna (2D)
    if len(X) > 0 and not isinstance(X[0], list):
        return [[val] for val in X]
    return X

def pedir_xy(x_mem, y_mem, X_DEF, Y_DEF, es_matriz=False):
    if len(x_mem) > 0:
        print("1.Usar datos en memoria RAM")
        print("ENTER=Nuevos o Ejemplo")
        op_mem = input("> ")
        if op_mem == "1":
            return x_mem, y_mem
            
    print("ENTER=usar ejemplo")
    if es_matriz:
        print("O teclea la matriz X:")
    else:
        print("O teclea vector X:")
        
    op = input("> ")
    if op.strip() == "":
        x = asegurar_matriz(X_DEF) if es_matriz else X_DEF
        y = Y_DEF
    else:
        if es_matriz:
            x = asegurar_matriz(leer_matriz(op))
        else:
            x = leer_lista(op)
            
        print("y vector (ej: 1,2,3):")
        ty = input("> ")
        y = leer_lista(ty)
        
    return x, y
