# main_semaforos.py
# Resuelve el ejercicio de ANOVA de un factor (semaforos) bajo el enfoque
# de MODELOS DE RANGO NO COMPLETO, reutilizando los modulos ya existentes:
#   matriz.py, inversa.py, modelo.py, anova.py, modulo_anova.py,
#   hipotesis.py, tabla_f.py
#
# Modelo:  y_ij = mu + tau_i + e_ij ,  i=1,2,3 (semaforo) ; j=1..4
# beta = [mu, tau1, tau2, tau3]^T ,  rango(X) = 3 (no rango completo,
# porque la columna de mu = suma de las columnas de los tau_i).
#
# Estrategia (sin modificar ningun modulo):
#  - Solucion 1 (mu=0)      -> X = indicadoras puras  -> X'X = diag(ni)
#                               (rango completo, se invierte directo)
#  - Solucion 2 (sum(tau)=0)-> se obtiene algebraicamente de la Solucion 1
#  - Parte b) ANOVA         -> X = [1, d2, d3] (codificacion de referencia,
#                               rango completo) -> encaja con modulo_anova.py
#  - Prueba H0: tau1=tau2=tau3 -> hipotesis.py (K*beta=m) sobre la Solucion 1

import matriz
import modelo
import modulo_anova
import hipotesis
import tabla_f
import datos_semaforos as datos


def parte_a():
    print("=" * 50)
    print("a) MODELO, ECUACIONES NORMALES Y DOS SOLUCIONES")
    print("=" * 50)
    print("Modelo:  y_ij = mu + tau_i + e_ij")
    print("beta = [mu, tau1, tau2, tau3]^T ; rango(X) = 3 (no completo)")

    y = datos.vector_y()

    # --- Solucion 1: restriccion mu = 0 (modelo de celdas/medias) ---
    X1 = datos.matriz_indicadora()
    res1 = modelo.ajustar(X1, y, con_intercepto=False)
    tau_hat = res1["beta"]

    print("\n--- Solucion 1  (restriccion mu = 0) ---")
    print(" mu     = 0")
    for i in range(len(tau_hat)):
        print(" tau" + str(i + 1) + "   = " + str(round(tau_hat[i], 4)))

    # --- Solucion 2: restriccion sum(tau_i) = 0 ---
    mu2 = sum(tau_hat) / len(tau_hat)
    print("\n--- Solucion 2  (restriccion tau1+tau2+tau3 = 0) ---")
    print(" mu     = " + str(round(mu2, 4)))
    for i in range(len(tau_hat)):
        print(" tau" + str(i + 1) + "   = " + str(round(tau_hat[i] - mu2, 4)))

    print("\n(Nota: cualquier funcion ESTIMABLE, como tau_i - tau_j o las")
    print(" sumas de cuadrados, es identica en ambas soluciones.)")

    return res1  # lo reutilizamos en la prueba de hipotesis de la parte b)


def parte_b():
    print("\n" + "=" * 50)
    print("b) HIPOTESIS Y ANALISIS DE VARIANZA (ANOVA)")
    print("=" * 50)
    print("H0: tau1 = tau2 = tau3   (igual retraso medio en los 3 semaforos)")
    print("Ha: al menos un tau_i es diferente")

    y = datos.vector_y()
    n = len(y)

    # Codificacion de referencia: X = [1, d2, d3]  (grupo 1 = base), rango 3
    Xd = datos.matriz_dummies_referencia()
    Xm = modelo.construir_X(Xd, con_intercepto=True)
    Xt = matriz.transponer(Xm)
    XtX = matriz.multiplicar(Xt, Xm)
    XtY = matriz.mat_vec(Xt, y)
    YtY = matriz.dot(y, y)

    res = modulo_anova.analizar_modelo(XtX, XtY, YtY, n)
    modulo_anova.imprimir_anova(res)

    print("\nConclusion (ingenieria de transito):")
    f_crit = tabla_f.f_critico(res["gl_reg"], res["gl_err"], 0.05)
    if res["F_reg"] > f_crit:
        print("Se RECHAZA H0: el tipo de semaforo SI afecta el retraso medio.")
        medias = [sum(g) / len(g) for g in datos.GRUPOS]
        for i in range(len(medias)):
            print(" Media " + datos.ETIQUETAS[i] + " = " + str(round(medias[i], 2)) + " seg")
    else:
        print("NO se rechaza H0: no hay evidencia de diferencia entre semaforos.")

    return res


def verificar_con_hipotesis_general(res_celdas):
    # Verificacion cruzada de F_reg usando el motor GENERAL de hipotesis.py
    # sobre la Solucion 1 (beta = [tau1, tau2, tau3]).
    print("\n" + "-" * 50)
    print("Verificacion cruzada con hipotesis.py :  K*beta = m")
    print("-" * 50)
    K = [[1.0, -1.0, 0.0],
         [0.0, 1.0, -1.0]]
    m = [0.0, 0.0]
    salida = hipotesis.prueba(K, m, res_celdas)

    print("Q       = " + str(round(salida["Q"], 4)))
    print("F_calc  = " + str(round(salida["F"], 4)))
    print("gl1=" + str(salida["gl1"]) + "  gl2=" + str(salida["gl2"]))
    f_crit = tabla_f.f_critico(salida["gl1"], salida["gl2"], 0.05)
    print("F_crit(.05) = " + str(round(f_crit, 4)))


def validar_supuestos(res_celdas):
    # La CG100 no tiene Shapiro-Wilk ni graficos de dispersion complejos,
    # asi que al menos imprimimos los residuos para inspeccion visual
    # (normalidad aproximada, valores atipicos, homocedasticidad).
    print("\n" + "-" * 50)
    print("Residuos del modelo (para validar supuestos clasicos)")
    print("-" * 50)
    res_list = res_celdas["residuos"]
    for i in range(len(res_list)):
        print(" e_" + str(i + 1) + " = " + str(round(res_list[i], 4)))
    print("Revisar: dispersion similar entre grupos (homocedasticidad),")
    print("ausencia de patrones (independencia) y simetria (normalidad).")


def main():
    res_celdas = parte_a()
    parte_b()
    verificar_con_hipotesis_general(res_celdas)
    validar_supuestos(res_celdas)


main()
