import matriz
import inversa
import tabla_f
import constructor
import hipotesis

def analizar_modelo(XtX, XtY, YtY, n):
    p = len(XtX)
    inv_XtX = inversa.invertir(XtX)
    beta = matriz.mat_vec(inv_XtX, XtY)
    
    sum_Y = XtY[0]
    SS_media = (sum_Y**2) / n
    SCT_no_corregida = YtY
    SS_Reg_uncorrected = matriz.dot(beta, XtY)
    SCR_ajustada = SS_Reg_uncorrected - SS_media
    SCE = SCT_no_corregida - SS_Reg_uncorrected

    gl_media = 1
    gl_reg = p - 1
    gl_err = n - p
    gl_tot = n
    
    CM_media = SS_media / gl_media
    CMR = SCR_ajustada / gl_reg
    CME = SCE / gl_err
    
    F_media = CM_media / CME
    F_reg = CMR / CME
    
    resultado = {
        'beta': beta,
        'XtX_inv': inv_XtX,
        'SS_media': SS_media,
        'SCT_no_corregida': SCT_no_corregida,
        'SCR_ajustada': SCR_ajustada,
        'SCE': SCE,
        'gl_media': gl_media,
        'gl_reg': gl_reg,
        'gl_err': gl_err,
        'gl_tot': gl_tot,
        'CM_media': CM_media,
        'CMR': CMR,
        'CME': CME,
        'F_media': F_media,
        'F_reg': F_reg,
        'p': p,
        'n': n,
        'con_intercepto': True
    }
    return resultado

def imprimir_anova(res):
    print('' + '='*50)
    print(' TABLA ANOVA PARTICIONADA (NO CORREGIDA)')
    print('='*50)
    print('Fuente       | SS         | gl | CM         | F')
    print('-' * 50)
    print('Media        |', round(res['SS_media'], 2), ' |', res['gl_media'], '|', round(res['CM_media'], 2), ' |', round(res['F_media'], 2))
    print('Regr. Ajust. |', round(res['SCR_ajustada'], 2), '  |', res['gl_reg'], '|', round(res['CMR'], 2), '  |', round(res['F_reg'], 2))
    print('Error        |', round(res['SCE'], 2), ' |', res['gl_err'], '|', round(res['CME'], 2), '  |')
    print('Total NoCor. |', round(res['SCT_no_corregida'], 2), '  |', res['gl_tot'], '|            |')
    print('='*50)

    f_crit_reg = tabla_f.f_critico(res['gl_reg'], res['gl_err'], 0.05)
    f_crit_media = tabla_f.f_critico(res['gl_media'], res['gl_err'], 0.05)

    print('\n--- DECISIONES DE HIPOTESIS (alfa = 0.05) ---')
    print('1. Regresion Ajustada (Variables Independientes):')
    h0_reg = ' = '.join(['B' + str(i) for i in range(1, res['p'])]) + ' = 0'
    print('   H0:', h0_reg)

    if res['F_reg'] < f_crit_reg:
        print('   F_calc =', round(res['F_reg'], 2), '< F_crit(' + str(round(f_crit_reg, 2)) + ') -> NO SE RECHAZA H0.')
        print('   Conclusion: La regresion no es significativa.')
    else:
        print('   F_calc =', round(res['F_reg'], 2), '> F_crit(' + str(round(f_crit_reg, 2)) + ') -> SE RECHAZA H0.')

    print('\n2. Media (Intercepto):')
    print('   H0: B0 = 0')
    if res['F_media'] > f_crit_media:
        print('   F_calc =', round(res['F_media'], 2), '> F_crit(' + str(round(f_crit_media, 2)) + ') -> SE RECHAZA H0.')
        print('   Conclusion: La media/intercepto es dif. de cero.')
    else:
        print('   F_calc =', round(res['F_media'], 2), '< F_crit(' + str(round(f_crit_media, 2)) + ') -> NO SE RECHAZA H0.')

def imprimir_contribucion(res):
    print('' + '='*50)
    print('--- B) CONTRIBUCION INDIVIDUAL (Pruebas t / F parciales) ---')
    print('='*50)
    print('Se prueba H0: Bj = 0 para cada variable en presencia de las demas.')
    f_crit_indiv = tabla_f.f_critico(1, res['gl_err'], 0.05)
    
    for i in range(1, res['p']):
        C_ii = res['XtX_inv'][i][i]
        var_beta = res['CME'] * C_ii
        se_beta = var_beta ** 0.5
        t_calc = res['beta'][i] / se_beta
        F_calc = t_calc ** 2
        print('Variable X' + str(i) + ' (B' + str(i) + ' = ' + str(round(res['beta'][i], 4)) + '):')
        print('   SE(Bj) = ' + str(round(se_beta, 4)) + ', t_calc = ' + str(round(t_calc, 4)) + ', F_calc = ' + str(round(F_calc, 4)))
        if F_calc > f_crit_indiv:
            print('   -> SIGNIFICATIVA (F_calc > ' + str(round(f_crit_indiv, 2)) + '). Rechaza H0.')
        else:
            print('   -> NO SIGNIFICATIVA (F_calc < ' + str(round(f_crit_indiv, 2)) + '). No rechaza H0.')

def interactuar_hipotesis(res):
    print('' + '='*50)
    print('--- C) PRUEBA DE HIPOTESIS MULTIPLE PERSONALIZADA ---')
    print('='*50)
    print('Sigue las instrucciones en pantalla para ingresar restricciones.')
    K, m_vec = constructor.construir(res, tipo='mlr')
    sal = hipotesis.prueba(K, m_vec, res)

    print('\nRESULTADOS DE LA PRUEBA:')
    print('Q =', round(sal['Q'], 4))
    print('F_calc =', round(sal['F'], 4))
    print('gl1 =', sal['gl1'], ' gl2 =', sal['gl2'])
    fc_hip = tabla_f.f_critico(sal['gl1'], sal['gl2'], 0.05)
    print('F_crit(.05) =', round(fc_hip, 4))
    if sal['F'] > fc_hip:
        print('Conclusion: SE RECHAZA H0')
    else:
        print('Conclusion: NO se rechaza H0')

def calcular_prediccion(res):
    print("\n" + "="*50)
    print("--- D) PREDICCION E INTERVALOS ---")
    print("="*50)
    entrada = input("Ingresa el vector x0 separado por comas (ej. 1, 0, 3, 0): ")
    if not entrada.strip():
        return
    partes = entrada.split(',')
    x0 = [float(p.strip()) for p in partes]
    
    # 1. Y_hat = x0^T * beta
    y_hat = sum([x0[i] * res["beta"][i] for i in range(len(x0))])
    
    # 2. h00 = x0^T * (X^T X)^-1 * x0
    M_x0 = matriz.mat_vec(res["XtX_inv"], x0)
    h00 = matriz.dot(x0, M_x0)
    
    # 3. Varianza de la prediccion (observacion nueva)
    var_pred = res["CME"] * (1 + h00)
    se_pred = var_pred ** 0.5
    
    # 4. t critico
    # t_critico de dos colas es igual a la raiz cuadrada de F(1, gl_err)
    f_crit = tabla_f.f_critico(1, res["gl_err"], 0.05)
    t_crit = f_crit ** 0.5
    
    lim_inf = y_hat - t_crit * se_pred
    lim_sup = y_hat + t_crit * se_pred
    
    print("\nResultados para x0 =", x0)
    print("Y_hat (prediccion puntual):", round(y_hat, 4))
    print("Varianza de la prediccion:", round(var_pred, 4))
    print("Error Estandar (SE_pred):", round(se_pred, 4))
    print("Valor t_critico (alfa/2=0.025):", round(t_crit, 4))
    print("Intervalo de Prediccion al 95%:")
    print("(", round(lim_inf, 4), ",", round(lim_sup, 4), ")")
