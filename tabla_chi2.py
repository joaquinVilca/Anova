# tabla_chi2.py
# Tabla de valores criticos de la distribucion Chi-cuadrado (dos colas).
# Se usa para el intervalo de confianza de sigma^2:
#   [ (n-k-1)*S2 / chi2_sup ,  (n-k-1)*S2 / chi2_inf ]
# Filas = grados de libertad (gl).
# Columnas para alpha=0.05 (dos colas): percentil 0.975 (cola inferior,
# valor chico) y percentil 0.025 (cola superior, valor grande).

TABLA_CHI2_05 = {
    1:  [0.000982, 5.024],
    2:  [0.0506,   7.378],
    3:  [0.216,    9.348],
    4:  [0.484,    11.143],
    5:  [0.831,    12.833],
    6:  [1.237,    14.449],
    7:  [1.690,    16.013],
    8:  [2.180,    17.535],
    9:  [2.700,    19.023],
    10: [3.247,    20.483],
    11: [3.816,    21.920],
    12: [4.404,    23.337],
    13: [5.009,    24.736],
    14: [5.629,    26.119],
    15: [6.262,    27.488],
    16: [6.908,    28.845],
    17: [7.564,    30.191],
    18: [8.231,    31.526],
    19: [8.907,    32.852],
    20: [9.591,    34.170],
    21: [10.283,   35.479],
    22: [10.982,   36.781],
    23: [11.689,   38.076],
    24: [12.401,   39.364],
    25: [13.120,   40.646],
    26: [13.844,   41.923],
    27: [14.573,   43.195],
    28: [15.308,   44.461],
    29: [16.047,   45.722],
    30: [16.791,   46.979],
}


def chi2_critico(gl, alpha=0.05):
    # Devuelve (chi2_inferior, chi2_superior) para el gl mas cercano.
    if gl < 1:
        gl = 1
    if gl in TABLA_CHI2_05:
        fila = TABLA_CHI2_05[gl]
    else:
        claves = sorted(TABLA_CHI2_05.keys())
        elegido = claves[0]
        for c in claves:
            if c <= gl:
                elegido = c
        fila = TABLA_CHI2_05[elegido]
    return fila[0], fila[1]
