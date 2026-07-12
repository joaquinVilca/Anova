# correlacion.py
# Correlacion de Pearson y prueba de hipotesis H0: rho = rho0
# usando la Transformacion Z de Fisher (util cuando rho0 != 0,
# ya que la distribucion de r no es normal en ese caso).

def pearson(x, y):
    n = len(x)
    mx = sum(x) / n
    my = sum(y) / n
    sxy = 0.0
    sxx = 0.0
    syy = 0.0
    for i in range(n):
        dx = x[i] - mx
        dy = y[i] - my
        sxy = sxy + dx * dy
        sxx = sxx + dx * dx
        syy = syy + dy * dy
    return sxy / ((sxx ** 0.5) * (syy ** 0.5))


def fisher_z(r):
    # Z = 0.5 * ln( (1+r) / (1-r) )
    return 0.5 * _ln((1.0 + r) / (1.0 - r))


def _ln(x):
    # ln(x) via serie/Newton, para no depender de la libreria math
    # en la fx-CG100 (por si no esta disponible import math).
    # Metodo: ln(x) = 2*atanh((x-1)/(x+1)) usando serie de Taylor.
    if x <= 0:
        raise ValueError("ln de numero no positivo")
    z = (x - 1.0) / (x + 1.0)
    z2 = z * z
    suma = 0.0
    termino = z
    k = 1
    while True:
        aporte = termino / k
        suma = suma + aporte
        if abs(aporte) < 1e-12:
            break
        termino = termino * z2
        k = k + 2
    return 2.0 * suma


def prueba_rho(r, rho0, n, alpha=0.05):
    # H0: rho = rho0   vs   Ha: rho != rho0
    Zr = 0.5 * _ln((1.0 + r) / (1.0 - r))
    Zrho0 = 0.5 * _ln((1.0 + rho0) / (1.0 - rho0))
    Z0 = (Zr - Zrho0) / (1.0 / ((n - 3) ** 0.5))
    z_crit = 1.96 if alpha == 0.05 else 2.576

    salida = {}
    salida["r"] = r
    salida["Zr"] = Zr
    salida["Zrho0"] = Zrho0
    salida["Z0"] = Z0
    salida["z_crit"] = z_crit
    salida["rechaza"] = abs(Z0) > z_crit
    return salida
