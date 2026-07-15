import math

print("=== INGRESO DE DATOS ===")
# Se solicita al usuario ingresar cada dato.
# Se usa float() para decimales y int() para enteros.
n = int(input("Tu valor de n: "))
b0 = float(input("Tu valor de b0: "))
b1 = float(input("Tu valor de b1: "))
r2 = float(input("Tu valor de r2: "))
s2_res = float(input("Tu valor de S2_Res: "))
t_crit = float(input("Tu valor de t critico: "))

print("\nProcesando...")

# ==========================================
# 2. Calculos intermedios
# ==========================================
gl_res = n - 2
sse = s2_res * gl_res            # Suma de Cuadrados del Error
sst = sse / (1.0 - r2)           # Suma de Cuadrados Total
ssr = sst - sse                  # Suma de Cuadrados de la Regresion
sxx = ssr / (b1 ** 2)            # Suma de Cuadrados de x

# ==========================================
# 3. Calculos finales
# ==========================================
se_b1 = math.sqrt(s2_res / sxx)  # Error estandar de la pendiente
margen_error = t_crit * se_b1

ic_inf = b1 - margen_error       # Limite inferior del IC
ic_sup = b1 + margen_error       # Limite superior del IC

t_stat = b1 / se_b1              # Estadistico de prueba t

# ==========================================
# 4. Impresion de resultados
# ==========================================
print("\n=== RESULTADOS ===")
print("Ecuacion: y = " + str(b0) + " + " + str(b1) + "x")
print("Sxx      :", round(sxx, 4))
print("Err. Est.:", round(se_b1, 4))

print("\n--- INTERVALO ---")
print("[", round(ic_inf, 4), ";", round(ic_sup, 4), "]")

print("\n--- PRUEBA (H0: b1=0) ---")
print("t calcul:", round(t_stat, 4))
print("t critic:", t_crit)

# Evaluacion
if ic_inf > 0 or ic_sup < 0:
    print("\nCONCLUSION:")
    print("Rechaza H0.")
    print("x influye linealmente.")
else:
    print("\nCONCLUSION:")
    print("NO rechaza H0.")
    print("x NO influye linealmente.")