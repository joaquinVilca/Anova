# tabla_t.py
# Tabla de valores criticos de la distribucion t-Student (dos colas).
# Filas = grados de libertad (gl). Columnas: alpha=0.05 (t_0.025) y
# alpha=0.01 (t_0.005). Para gl > 30 se usa el valor de Z (normal).

TABLA_T = {
    1:  [12.706, 63.657],
    2:  [4.303, 9.925],
    3:  [3.182, 5.841],
    4:  [2.776, 4.604],
    5:  [2.571, 4.032],
    6:  [2.447, 3.707],
    7:  [2.365, 3.499],
    8:  [2.306, 3.355],
    9:  [2.262, 3.250],
    10: [2.228, 3.169],
    11: [2.201, 3.106],
    12: [2.179, 3.055],
    13: [2.160, 3.012],
    14: [2.145, 2.977],
    15: [2.131, 2.947],
    16: [2.120, 2.921],
    17: [2.110, 2.898],
    18: [2.101, 2.878],
    19: [2.093, 2.861],
    20: [2.086, 2.845],
    21: [2.080, 2.831],
    22: [2.074, 2.819],
    23: [2.069, 2.807],
    24: [2.064, 2.797],
    25: [2.060, 2.787],
    26: [2.056, 2.779],
    27: [2.052, 2.771],
    28: [2.048, 2.763],
    29: [2.045, 2.756],
    30: [2.042, 2.750],
}

Z_INFINITO = [1.960, 2.576]  # limite cuando gl -> infinito


def t_critico(gl, alpha=0.05):
    # Devuelve el valor critico t de dos colas mas cercano de la tabla.
    if gl < 1:
        gl = 1
    col = 0 if alpha == 0.05 else 1

    if gl > 30:
        return Z_INFINITO[col]
    if gl in TABLA_T:
        return TABLA_T[gl][col]

    # Si el gl exacto no esta (caso raro), usar el mas cercano por abajo
    claves = sorted(TABLA_T.keys())
    elegido = claves[0]
    for c in claves:
        if c <= gl:
            elegido = c
    return TABLA_T[elegido][col]
