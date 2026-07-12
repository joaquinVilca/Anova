# falta_de_ajuste.py
# Prueba de falta de ajuste (Lack of Fit) para una regresion simple
# Y = a0 + a1*X, valida solo si existen observaciones repetidas en X.
#
#   SSE_modelo         (gl = n-2)              -> del ajuste de regresion simple
#   SS_error_puro (PE)  (gl = n-c)              -> varianza DENTRO de cada
#                                                  grupo de X repetido
#   SS_falta_ajuste(LOF)=SSE_modelo - SS_PE     (gl = c-2)
#   F = (SS_LOF/(c-2)) / (SS_PE/(n-c))
#
# c = numero de valores DISTINTOS de X.

def agrupar(x, y):
    grupos = {}
    for i in range(len(x)):
        grupos.setdefault(x[i], []).append(y[i])
    return grupos


def suma_cuadrados_error_puro(x, y):
    grupos = agrupar(x, y)
    c = len(grupos)
    SS_PE = 0.0
    for clave in grupos:
        valores = grupos[clave]
        m = sum(valores) / len(valores)
        for v in valores:
            SS_PE = SS_PE + (v - m) ** 2
    return SS_PE, c


def prueba_falta_ajuste(x, y, SSE_modelo):
    n = len(y)
    SS_PE, c = suma_cuadrados_error_puro(x, y)
    SS_LOF = SSE_modelo - SS_PE

    gl_lof = c - 2
    gl_pe = n - c

    MS_lof = SS_LOF / gl_lof
    MS_pe = SS_PE / gl_pe
    F = MS_lof / MS_pe

    salida = {}
    salida["c"] = c
    salida["SS_PE"] = SS_PE
    salida["SS_LOF"] = SS_LOF
    salida["gl_lof"] = gl_lof
    salida["gl_pe"] = gl_pe
    salida["MS_lof"] = MS_lof
    salida["MS_pe"] = MS_pe
    salida["F"] = F
    return salida
