# constructor.py
# Asistente para construir H0: K*beta = m de forma guiada.
# Funciona para MLR y para modelos polinomiales.
# La unica diferencia es el parametro 'tipo':
#   "mlr" -> etiquetas b0, b1, b2, ...  o  b1, b2, b3, ...
#   "pol" -> etiquetas b0, x, x^2, x^3, ...
# En ambos casos el resto del flujo (indices, multiplicadores, m) es identico.

import vandermonde

def etiquetas_mlr(resultado):
    p = resultado["p"]
    con_int = resultado["con_intercepto"]
    et = []
    if con_int:
        et.append("b0")
        for i in range(1, p):
            et.append("b" + str(i))
    else:
        for i in range(1, p + 1):
            et.append("b" + str(i))
    return et

def obtener_etiquetas(resultado, tipo):
    if tipo == "pol":
        num_vars = resultado.get("num_vars", 1)
        grado = (resultado["p"] - 1) // num_vars
        return vandermonde.etiquetas_pol(grado, num_vars)
    return etiquetas_mlr(resultado)

def mostrar_coeficientes(resultado, tipo):
    et = obtener_etiquetas(resultado, tipo)
    beta = resultado["beta"]
    print("COEFICIENTES:")
    for i in range(len(et)):
        print(str(i+1) + ") " + et[i] + " = " + str(round(beta[i], 4)))
    return et

def texto_restriccion(fila, et, mv):
    partes = []
    for j in range(len(fila)):
        c = fila[j]
        if c != 0.0:
            if c == 1.0:
                partes.append(et[j])
            elif c == -1.0:
                partes.append("-" + et[j])
            else:
                partes.append(str(c) + "*" + et[j])
    linea = ""
    for k in range(len(partes)):
        p = partes[k]
        if k == 0:
            linea = p
        elif p.startswith("-"):
            linea = linea + " - " + p[1:]
        else:
            linea = linea + " + " + p
    return linea + " = " + str(mv)

def construir(resultado, tipo="mlr"):
    et = mostrar_coeficientes(resultado, tipo)
    p = len(et)
    K = []
    m = []
    q = int(input("Num. restricciones (q): \n"))
    for r in range(q):
        print("--Restriccion " + str(r+1) + " de " + str(q) + "--")
        fila = [0.0] * p
        t = int(input("Cuantos coef. intervienen: \n"))
        for j in range(t):
            idx = int(input(" indice (1-" + str(p) + "): \n")) - 1
            txt = input(" multiplicador (ENTER=1): \n")
            mult = 1.0 if txt.strip() == "" else float(txt)
            fila[idx] = mult
        mv = float(input(" valor m:  \n"))
        K.append(fila)
        m.append(mv)
    print("H0:")
    for r in range(q):
        print(" " + texto_restriccion(K[r], et, m[r]))
    return K, m

def construir_ceros(resultado, tipo="mlr"):
    et = mostrar_coeficientes(resultado, tipo)
    p = len(et)
    print("Indices (1-" + str(p) + ") a igualar a 0, sep por comas:")
    indices = input("> ")
    idx_list = []
    for x in indices.split(","):
        if x.strip() != "":
            idx_list.append(int(x.strip()) - 1)
            
    q = len(idx_list)
    K = []
    m = []
    for idx in idx_list:
        fila = [0.0] * p
        fila[idx] = 1.0
        K.append(fila)
        m.append(0.0)
    
    print("H0:")
    for r in range(q):
        print(" " + texto_restriccion(K[r], et, m[r]))
    return K, m
