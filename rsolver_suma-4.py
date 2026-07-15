# rsolver_sumas.py
# Script para resolver problemas de regresión lineal simple a partir de sumatorias.

def resolver_regresion_por_sumatorias():
    print("=== RESOLUCION DE REGRESION SIMPLE POR SUMATORIAS ===")
    print("Ingrese los valores solicitados (puede usar decimales):")
    
    try:
        n = int(input("n (número de observaciones): "))
        sum_x = float(input("Suma de X (Σx): "))
        sum_y = float(input("Suma de Y (Σy): "))
        sum_x2 = float(input("Suma de X^2 (Σx^2): "))
        sum_xy = float(input("Suma de XY (Σxy): "))
        sum_y2_in = input("Suma de Y^2 (Σy^2) [Opcional, presiona ENTER para saltar]: ").strip()
        sum_y2 = float(sum_y2_in) if sum_y2_in else None
    except ValueError:
        print("Error: Por favor ingrese valores numéricos válidos.")
        return

    # Cálculos
    numerador_b1 = n * sum_xy - sum_x * sum_y
    denominador_b1 = n * sum_x2 - sum_x**2
    
    if denominador_b1 == 0:
        print("Error: El denominador de b1 es 0, no se puede calcular la regresión (X es constante).")
        return
        
    b1 = numerador_b1 / denominador_b1
    
    x_barra = sum_x / n
    y_barra = sum_y / n
    
    b0 = y_barra - b1 * x_barra
    
    print("\n" + "="*50)
    print("--- PASO 1: Calcular la pendiente (b1) ---")
    print("Fórmula: b1 = [n * Σxy - Σx * Σy] / [n * Σx^2 - (Σx)^2]")
    print(f"Numerador  = {n}({sum_xy}) - ({sum_x})({sum_y}) = {numerador_b1}")
    print(f"Denominador= {n}({sum_x2}) - ({sum_x})^2 = {denominador_b1}")
    print(f"b1 = {numerador_b1} / {denominador_b1} = {round(b1, 5)}")
    
    print("\n--- PASO 2: Calcular el intercepto (b0) ---")
    print("Fórmula: b0 = Y_barra - b1 * X_barra")
    print(f"X_barra = {sum_x} / {n} = {round(x_barra, 5)}")
    print(f"Y_barra = {sum_y} / {n} = {round(y_barra, 5)}")
    print(f"b0 = {round(y_barra, 5)} - ({round(b1, 5)} * {round(x_barra, 5)}) = {round(b0, 5)}")
    
    print("\n--- RESULTADO FINAL ---")
    print(f"Ecuación del modelo: Y_estimada = {round(b0, 4)} + {round(b1, 4)}X")
    
    if sum_y2 is not None:
        SCT = sum_y2 - (sum_y**2) / n
        SCE = sum_y2 - b0 * sum_y - b1 * sum_xy
        if SCE < 0:
            SCE = 0.0
            
        varianza = SCE / (n - 2) if n > 2 else float('inf')
        r2 = 1 - (SCE / SCT) if SCT != 0 else 0
        
        print("\n--- PASO 3: Calcular Varianza y R^2 ---")
        print("Fórmula SCE = Σy^2 - b0*Σy - b1*Σxy")
        print(f"SCE = {sum_y2} - ({round(b0, 5)} * {sum_y}) - ({round(b1, 5)} * {sum_xy}) = {round(SCE, 5)}")
        print(f"Varianza residual (σ^2 estimada) = SCE / (n-2) = {round(SCE, 5)} / {n-2} = {round(varianza, 5)}")
        
        print("\nFórmula SCT = Σy^2 - (Σy)^2 / n")
        print(f"SCT = {sum_y2} - ({sum_y})^2 / {n} = {round(SCT, 5)}")
        print(f"Coeficiente de determinación (R^2) = 1 - (SCE / SCT) = 1 - ({round(SCE, 5)} / {round(SCT, 5)}) = {round(r2, 4)}")
        
    print("="*50)

resolver_regresion_por_sumatorias()
