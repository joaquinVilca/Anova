# 3_solver.py
import modulo_anova

XtX = [
    [20,   0,    0,   0],
    [ 0, 250,  401,   0],
    [ 0, 401, 1103,   0],
    [ 0,   0,    0, 128]
]

XtY = [
    1000.00,
    970.45,
    1674.41,
    -396.80
]

YtY = 185883
n = 20

def menu_principal():
    print("Calculando modelo...")
    res = modulo_anova.analizar_modelo(XtX, XtY, YtY, n)
    
    while True:
        print("\n--- MENU DE ANALISIS DE REGRESION ---")
        print("1. Ver Tabla ANOVA Particionada y Betas")
        print("2. Ver Contribucion Individual de Variables (Pruebas t/F)")
        print("3. Probar Hipotesis Multiple Personalizada")
        print("4. Predecir e Intervalos (Nuevo x0)")
        print("5. Ejecutar Todo (1, 2, 3 y 4)")
        print("6. Salir")
        op = input("> ")
        
        if op == "1":
            print("Beta:")
            for b in res["beta"]:
                print(round(b, 4))
            modulo_anova.imprimir_anova(res)
        elif op == "2":
            modulo_anova.imprimir_contribucion(res)
        elif op == "3":
            modulo_anova.interactuar_hipotesis(res)
        elif op == "4":
            modulo_anova.calcular_prediccion(res)
        elif op == "5":
            print("Beta:")
            for b in res["beta"]:
                print(round(b, 4))
            modulo_anova.imprimir_anova(res)
            modulo_anova.imprimir_contribucion(res)
            modulo_anova.interactuar_hipotesis(res)
            modulo_anova.calcular_prediccion(res)
        elif op == "6":
            break
        else:
            print("Opcion invalida.")

if __name__ == "__main__":
    menu_principal()
