# anova.py
# Construye e imprime la tabla ANOVA del modelo (con o sin intercepto)

def mostrar(resultado):
    SCR = resultado["SCR"]
    SCE = resultado["SCE"]
    SCT = resultado["SCT"]
    glr = resultado["gl_reg"]
    gle = resultado["gl_err"]
    glt = resultado["gl_tot"]
    CMR = SCR / glr
    CME = SCE / gle
    F = CMR / CME

    print("--TABLA ANOVA--")
    print("REGRESION")
    print(" gl=" + str(glr))
    print(" SC=" + str(round(SCR, 4)))
    print(" CM=" + str(round(CMR, 4)))
    print("ERROR")
    print(" gl=" + str(gle))
    print(" SC=" + str(round(SCE, 4)))
    print(" CM=" + str(round(CME, 4)))
    print("TOTAL")
    print(" gl=" + str(glt))
    print(" SC=" + str(round(SCT, 4)))
    print("F GLOBAL=" + str(round(F, 4)))
    return F
