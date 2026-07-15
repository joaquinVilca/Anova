# main_consumo.py
# Regresion Lineal Multiple:  Y = b0 + b1*X1 + b2*X2 + b3*X3 + u
# Y = consumo, X1 = precio propio, X2 = ingreso, X3 = precio del sustituto
#
# Reutiliza: matriz.py, inversa.py, modelo.py, anova.py, hipotesis.py,
#            tabla_f.py  (ya existentes)
# Agrega:    tabla_t.py, tabla_chi2.py, var_cov.py, correlacion.py,
#            falta_de_ajuste.py

import matriz
import inversa
import modelo
import anova
import tabla_f
import tabla_t
import tabla_chi2
import var_cov
import correlacion
import falta_de_ajuste
import d_consumo as datos
import itertools


def generar_etiquetas(k):
    etiquetas = ["b0"]
    for i in range(1, k + 1):
        etiquetas.append(f"b{i}(X{i})")
    return etiquetas


def parte_a(res, etiquetas):
    print("=" * 55)
    print("a) SIGNOS ESPERADOS, ESTIMACION E INTERPRETACION")
    print("=" * 55)
    print("Signos esperados (teoria economica, sin calculo):")
    print(" b1 (precio propio X1)    : negativo  (Ley de la demanda)")
    print(" b2 (ingreso X2)          : positivo  (bien normal)")
    print(" b3 (precio sustituto X3) : positivo  (sustitutos)")

    beta = res["beta"]
    print("\nEstimacion (Y_hat = " + " + ".join(etiquetas) + "):")
    for i in range(len(beta)):
        print(" " + etiquetas[i] + " = " + str(round(beta[i], 4)))

    print("\nInterpretacion:")
    for i in range(1, len(beta)):
        print(" b" + str(i) + "=" + str(round(beta[i], 3)) + " -> si X" + str(i) + " sube 1 unidad,")
        print("   Y cambia " + str(round(beta[i], 3)) + " unidades, ceteris paribus.")



def parte_b(res, etiquetas):
    print("\n" + "=" * 55)
    print("b) VARIANZAS Y CORRELACIONES DE LOS ESTIMADORES")
    print("=" * 55)
    S2 = res["SCE"] / res["gl_err"]
    print("S2 (CME) = SCE/(n-k-1) = " + str(round(S2, 4)))

    V = var_cov.matriz_var_cov(S2, res["XtX_inv"])
    var_cov.imprimir_var_cov(V, etiquetas)
    return V, S2


def parte_c(res):
    print("\n" + "=" * 55)
    print("c) TABLA ANOVA GLOBAL Y SIGNIFICANCIA")
    print("=" * 55)
    F_global = anova.mostrar(res)

    f_crit = tabla_f.f_critico(res["gl_reg"], res["gl_err"], 0.05)
    print("\nH0: b1 = b2 = b3 = b4 = 0  (el modelo NO es significativo)")
    print("F_crit(" + str(res["gl_reg"]) + "," + str(res["gl_err"]) + ") = " + str(f_crit))
    if F_global > f_crit:
        print("F_calc > F_crit -> SE RECHAZA H0: el modelo es GLOBALMENTE significativo.")
    else:
        print("F_calc < F_crit -> NO se rechaza H0: el modelo no es significativo.")

    R2 = res["SCR"] / res["SCT"]
    print("R^2 = " + str(round(R2, 4)))
    return F_global


def parte_d(res, V, S2, etiquetas):
    print("\n" + "=" * 55)
    print("d) INTERVALOS DE CONFIANZA (alfa=0.05)")
    print("=" * 55)
    gl = res["gl_err"]
    t_crit = tabla_t.t_critico(gl, 0.05)
    print("t_crit(gl=" + str(gl) + ", 0.025) = " + str(t_crit))

    beta = res["beta"]
    se = var_cov.errores_estandar(V)
    for i in range(1, len(beta)):
        li = beta[i] - t_crit * se[i]
        ls = beta[i] + t_crit * se[i]
        print(" IC 95% " + etiquetas[i] + " = ( " + str(round(li, 4)) + " , " + str(round(ls, 4)) + " )")

    print("\nIntervalo de confianza para sigma^2:")
    chi_inf, chi_sup = tabla_chi2.chi2_critico(gl, 0.05)
    li = (gl * S2) / chi_sup
    ls = (gl * S2) / chi_inf
    print(" chi2_inf(" + str(gl) + ",0.975) = " + str(chi_inf) + "   chi2_sup(" + str(gl) + ",0.025) = " + str(chi_sup))
    print(" IC 95% sigma^2 = ( " + str(round(li, 4)) + " , " + str(round(ls, 4)) + " )")


def parte_e(res, V, etiquetas):
    print("\n" + "=" * 55)
    print("e) PRUEBAS DE HIPOTESIS INDIVIDUALES Y CONJUNTA")
    print("=" * 55)
    beta = res["beta"]
    se = var_cov.errores_estandar(V)
    gl = res["gl_err"]
    t_crit = tabla_t.t_critico(gl, 0.05)
    print("t_crit(" + str(gl) + ", 0.025) = " + str(t_crit))

    for i in range(1, len(beta)):
        t_calc = beta[i] / se[i]
        print("\nH0: " + etiquetas[i][:2] + " = 0   vs   Ha: " + etiquetas[i][:2] + " != 0")
        print(" t_calc = " + str(round(t_calc, 4)))
        if abs(t_calc) > t_crit:
            print(" |t_calc| > t_crit -> SE RECHAZA H0 (" + etiquetas[i] + " es significativo).")
        else:
            print(" |t_calc| < t_crit -> NO se rechaza H0 (" + etiquetas[i] + " NO es significativo).")

    print("\nH0: b1 = b2 = b3 = b4 = 0  (prueba conjunta = F global de la parte c)")
    F_global = res["SCR"] / res["gl_reg"] / (res["SCE"] / res["gl_err"])
    f_crit = tabla_f.f_critico(res["gl_reg"], res["gl_err"], 0.05)
    print(" F_calc = " + str(round(F_global, 4)) + "   F_crit = " + str(f_crit))
    if F_global > f_crit:
        print(" SE RECHAZA H0 (igual conclusion que en la parte c).")
    else:
        print(" NO se rechaza H0.")


def parte_f():
    print("\n" + "=" * 55)
    print("f) FALTA DE AJUSTE: regresion simple Y vs X1")
    print("=" * 55)
    X1 = datos.X1
    Y = datos.Y
    n = len(Y)

    Xs = [[1.0, float(x)] for x in X1]
    Xt = matriz.transponer(Xs)
    XtX = matriz.multiplicar(Xt, Xs)
    XtXinv = inversa.invertir(XtX)
    XtY = matriz.mat_vec(Xt, Y)
    beta = matriz.mat_vec(XtXinv, XtY)
    yhat = matriz.mat_vec(Xs, beta)
    res_s = matriz.resta_vec(Y, yhat)
    SSE_modelo = matriz.dot(res_s, res_s)

    print("Modelo simple: Y_hat = " + str(round(beta[0], 4)) + " + (" + str(round(beta[1], 4)) + ")*X1")
    print("SSE_modelo (gl=" + str(n - 2) + ") = " + str(round(SSE_modelo, 4)))

    salida = falta_de_ajuste.prueba_falta_ajuste(X1, Y, SSE_modelo)
    print("\nValores distintos de X1: c = " + str(salida["c"]))
    print("SS_error_puro (gl=" + str(salida["gl_pe"]) + ") = " + str(round(salida["SS_PE"], 4)))
    print("SS_falta_ajuste (gl=" + str(salida["gl_lof"]) + ") = " + str(round(salida["SS_LOF"], 4)))
    print("MS_LOF = " + str(round(salida["MS_lof"], 4)) + "   MS_PE = " + str(round(salida["MS_pe"], 4)))
    print("F_calc = " + str(round(salida["F"], 4)))

    f_crit = tabla_f.f_critico(salida["gl_lof"], salida["gl_pe"], 0.05)
    print("F_crit(" + str(salida["gl_lof"]) + "," + str(salida["gl_pe"]) + ") = " + str(f_crit))
    print("\nH0: el modelo lineal simple es adecuado (no hay falta de ajuste)")
    if salida["F"] > f_crit:
        print("F_calc > F_crit -> SE RECHAZA H0: SI hay falta de ajuste.")
    else:
        print("F_calc < F_crit -> NO se rechaza H0: NO hay evidencia de falta de ajuste.")


def parte_g():
    print("\n" + "=" * 55)
    print("g) CORRELACION Y vs X1:  H0: rho = 0.5  vs  Ha: rho != 0.5")
    print("=" * 55)
    r = correlacion.pearson(datos.X1, datos.Y)
    print("r (Pearson, Y vs X1) = " + str(round(r, 4)))

    n = len(datos.Y)
    salida = correlacion.prueba_rho(r, 0.5, n, alpha=0.05)
    print("Zr (r muestral)      = " + str(round(salida["Zr"], 4)))
    print("Z(rho0=0.5)          = " + str(round(salida["Zrho0"], 4)))
    print("Z0_calc              = " + str(round(salida["Z0"], 4)))
    print("Z_crit (0.05, dos colas) = " + str(salida["z_crit"]))

    if salida["rechaza"]:
        print("|Z0| > Z_crit -> SE RECHAZA H0: rho es significativamente distinto de 0.5.")
    else:
        print("|Z0| < Z_crit -> NO se rechaza H0.")


def parte_h(k):
    print("\n" + "=" * 55)
    print("h) PREGUNTA 13: MEJOR SUBCONJUNTO DE REGRESION")
    print("=" * 55)
    print("Si el horizonte se repite a partir de 2012, evaluaremos")
    print("que variables son las mejores para predecir el futuro.\n")

    Y = datos.vector_Y()
    n = len(Y)
    
    nombres = [f"X{i+1}" for i in range(k)]
    var_dict = {f"X{i+1}": datos.TODAS_LAS_X[i] for i in range(k)}

    # Calcular el modelo completo para obtener CME_full (para Cp)
    full_X = []
    for i in range(n):
        full_X.append([var_dict[nom][i] for nom in nombres])
        
    full_res = modelo.ajustar(full_X, Y, con_intercepto=True)
    CME_full = full_res["SCE"] / full_res["gl_err"]
    SCT = full_res["SCT"]

    resultados = []

    for r in range(1, k + 1):
        for combo in itertools.combinations(nombres, r):
            X_sub = []
            for i in range(n):
                X_sub.append([var_dict[v][i] for v in combo])
            
            res = modelo.ajustar(X_sub, Y, con_intercepto=True)
            p = len(combo) + 1  # Incluye b0
            
            R2 = res["SCR"] / SCT
            R2_adj = 1 - (res["SCE"] / (n - p)) / (SCT / (n - 1))
            CME = res["SCE"] / (n - p)
            Cp = (res["SCE"] / CME_full) - n + 2 * p
            
            resultados.append({
                "vars": ", ".join(combo),
                "p": p,
                "R2": R2,
                "R2_adj": R2_adj,
                "CME": CME,
                "Cp": Cp
            })

    # Ordenar por R^2 Ajustado descendente
    resultados.sort(key=lambda x: x["R2_adj"], reverse=True)

    print(f"{'Subconjunto':<15} | {'p':<2} | {'R^2':<8} | {'R^2 Aj.':<8} | {'CME':<8} | {'Cp':<8}")
    print("-" * 65)
    for r in resultados:
        print(f"{r['vars']:<15} | {r['p']:<2} | {r['R2']:<8.4f} | {r['R2_adj']:<8.4f} | {r['CME']:<8.4f} | {r['Cp']:<8.4f}")

    print("\nConclusion:")
    if len(resultados) > 0:
        mejor = resultados[0]
        print(f"El mejor modelo es el que usa: {mejor['vars']}")
        print(f"Tiene el mayor R^2 Ajustado ({mejor['R2_adj']:.4f}), el menor CME ({mejor['CME']:.4f}) y un")
        print(f"Cp de Mallows de {mejor['Cp']:.4f} para p={mejor['p']}.")
        print("Este subconjunto es el ideal para realizar proyecciones.")


def main():
    X, k = datos.matriz_X()
    Y = datos.vector_Y()
    
    etiquetas = generar_etiquetas(k)

    try:
        res = modelo.ajustar(X, Y, con_intercepto=True)
    except ValueError as e:
        print("\n[ERROR]: " + str(e))
        return

    parte_a(res, etiquetas)
    V, S2 = parte_b(res, etiquetas)
    parte_c(res)
    parte_d(res, V, S2, etiquetas)
    parte_e(res, V, etiquetas)
    parte_f()
    parte_g()
    parte_h(k)


main()
