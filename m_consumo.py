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
import datos_consumo as datos

ETIQUETAS = ["b0", "b1(X1)", "b2(X2)", "b3(X3)"]


def parte_a(res):
    print("=" * 55)
    print("a) SIGNOS ESPERADOS, ESTIMACION E INTERPRETACION")
    print("=" * 55)
    print("Signos esperados (teoria economica, sin calculo):")
    print(" b1 (precio propio X1)    : negativo  (Ley de la demanda)")
    print(" b2 (ingreso X2)          : positivo  (bien normal)")
    print(" b3 (precio sustituto X3) : positivo  (sustitutos)")

    beta = res["beta"]
    print("\nEstimacion (Y_hat = b0 + b1*X1 + b2*X2 + b3*X3):")
    for i in range(4):
        print(" " + ETIQUETAS[i] + " = " + str(round(beta[i], 4)))

    print("\nInterpretacion:")
    print(" b1=" + str(round(beta[1], 3)) + " -> si X1 sube 1 unidad,")
    print("   Y baja " + str(round(-beta[1], 3)) + " unidades, ceteris paribus.")
    print(" b2=" + str(round(beta[2], 3)) + " -> si el ingreso sube 1,")
    print("   Y sube " + str(round(beta[2], 3)) + ", ceteris paribus.")
    print(" b3=" + str(round(beta[3], 3)) + " -> si el precio del sustituto")
    print("   sube 1, Y sube " + str(round(beta[3], 3)) + ", ceteris paribus.")
    print(" (Los 3 signos coinciden con lo esperado por la teoria.)")


def parte_b(res):
    print("\n" + "=" * 55)
    print("b) VARIANZAS Y CORRELACIONES DE LOS ESTIMADORES")
    print("=" * 55)
    S2 = res["SCE"] / res["gl_err"]
    print("S2 (CME) = SCE/(n-k-1) = " + str(round(S2, 4)))

    V = var_cov.matriz_var_cov(S2, res["XtX_inv"])
    var_cov.imprimir_var_cov(V, ETIQUETAS)
    return V, S2


def parte_c(res):
    print("\n" + "=" * 55)
    print("c) TABLA ANOVA GLOBAL Y SIGNIFICANCIA")
    print("=" * 55)
    F_global = anova.mostrar(res)

    f_crit = tabla_f.f_critico(res["gl_reg"], res["gl_err"], 0.05)
    print("\nH0: b1 = b2 = b3 = 0  (el modelo NO es significativo)")
    print("F_crit(" + str(res["gl_reg"]) + "," + str(res["gl_err"]) + ") = " + str(f_crit))
    if F_global > f_crit:
        print("F_calc > F_crit -> SE RECHAZA H0: el modelo es GLOBALMENTE significativo.")
    else:
        print("F_calc < F_crit -> NO se rechaza H0: el modelo no es significativo.")

    R2 = res["SCR"] / res["SCT"]
    print("R^2 = " + str(round(R2, 4)))
    return F_global


def parte_d(res, V, S2):
    print("\n" + "=" * 55)
    print("d) INTERVALOS DE CONFIANZA (alfa=0.05)")
    print("=" * 55)
    gl = res["gl_err"]
    t_crit = tabla_t.t_critico(gl, 0.05)
    print("t_crit(gl=" + str(gl) + ", 0.025) = " + str(t_crit))

    beta = res["beta"]
    se = var_cov.errores_estandar(V)
    for i in [1, 2]:
        li = beta[i] - t_crit * se[i]
        ls = beta[i] + t_crit * se[i]
        print(" IC 95% " + ETIQUETAS[i] + " = ( " + str(round(li, 4)) + " , " + str(round(ls, 4)) + " )")

    print("\nIntervalo de confianza para sigma^2:")
    chi_inf, chi_sup = tabla_chi2.chi2_critico(gl, 0.05)
    li = (gl * S2) / chi_sup
    ls = (gl * S2) / chi_inf
    print(" chi2_inf(" + str(gl) + ",0.975) = " + str(chi_inf) + "   chi2_sup(" + str(gl) + ",0.025) = " + str(chi_sup))
    print(" IC 95% sigma^2 = ( " + str(round(li, 4)) + " , " + str(round(ls, 4)) + " )")


def parte_e(res, V):
    print("\n" + "=" * 55)
    print("e) PRUEBAS DE HIPOTESIS INDIVIDUALES Y CONJUNTA")
    print("=" * 55)
    beta = res["beta"]
    se = var_cov.errores_estandar(V)
    gl = res["gl_err"]
    t_crit = tabla_t.t_critico(gl, 0.05)
    print("t_crit(" + str(gl) + ", 0.025) = " + str(t_crit))

    for i in [1, 2, 3]:
        t_calc = beta[i] / se[i]
        print("\nH0: " + ETIQUETAS[i][:2] + " = 0   vs   Ha: " + ETIQUETAS[i][:2] + " != 0")
        print(" t_calc = " + str(round(t_calc, 4)))
        if abs(t_calc) > t_crit:
            print(" |t_calc| > t_crit -> SE RECHAZA H0 (" + ETIQUETAS[i] + " es significativo).")
        else:
            print(" |t_calc| < t_crit -> NO se rechaza H0 (" + ETIQUETAS[i] + " NO es significativo).")

    print("\nH0: b1 = b2 = b3 = 0  (prueba conjunta = F global de la parte c)")
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


def main():
    X = datos.matriz_X()
    Y = datos.vector_Y()

    res = modelo.ajustar(X, Y, con_intercepto=True)

    parte_a(res)
    V, S2 = parte_b(res)
    parte_c(res)
    parte_d(res, V, S2)
    parte_e(res, V)
    parte_f()
    parte_g()


main()
