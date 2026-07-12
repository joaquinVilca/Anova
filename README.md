# Suite de Regresión y ANOVA sin Numpy

Esta es una colección de herramientas implementadas **100% en Python puro** (sin usar `numpy`, `scipy` ni otras bibliotecas externas) para resolver problemas de Regresión Lineal Simple, Múltiple y Polinomial, además de realizar Análisis de Varianza (ANOVA). 

Es ideal para ejecutarse en entornos limitados como calculadoras gráficas programables (ej. Casio CG50/CG100 con MicroPython) o para fines netamente didácticos.

## Estructura de Scripts Principales

El proyecto se divide en tres *scripts* principales, cada uno diseñado para un caso de uso específico dependiendo de los datos que tengas disponibles:

### 1. `1_rpoli.py` - Regresión Polinomial
**¿Cuándo usarlo?**
Úsalo cuando tengas datos crudos de **una sola variable independiente** ($X$) y quieras ajustarla a un modelo curvo (polinomial). Por ejemplo, un modelo de la forma:
$\hat{Y} = \beta_0 + \beta_1 X + \beta_2 X^2 + \beta_3 X^3$

**¿Qué hace?**
- Toma el vector $X$ y el vector $Y$.
- Calcula automáticamente los grados superiores ($X^2, X^3 \dots$) utilizando la matriz de Vandermonde.
- Realiza la estimación de los coeficientes $\beta$.
- Muestra la tabla ANOVA y calcula el coeficiente de determinación ($R^2$).

---

### 2. `2_rmultiple.py` - Regresión Lineal Múltiple (Datos Crudos)
**¿Cuándo usarlo?**
Úsalo cuando un problema te proporciona **la tabla completa de datos originales** (observaciones individuales para $X_1, X_2, \dots, X_p$ y $Y$).

**¿Qué hace?**
- Permite ingresar la matriz de variables independientes y el vector de respuestas.
- Ensambla internamente la matriz $X$ (añadiendo la columna de unos para el intercepto).
- Calcula automáticamente $X^T X$ y su inversa.
- Evalúa la significancia general del modelo mediante la tabla ANOVA y entrega los $\beta$.
- Soporta la prueba de hipótesis lineal general.

---

### 3. `3_solver.py` - Solucionador Directo y Avanzado (Desde $X^TX$)
**¿Cuándo usarlo?**
Úsalo para exámenes o problemas avanzados donde **no tienes los datos crudos**, sino que te entregan directamente las matrices pre-calculadas: $X^T X$, $X^T Y$, y la suma total $Y^T Y$.

**¿Qué hace?**
Este es el *script* más potente y modular. Utiliza un menú interactivo (`modulo_anova.py`) que te permite:
1. **Ver la Tabla ANOVA Particionada:** Calcula las Sumas de Cuadrados (SS), Grados de Libertad (gl), Cuadrados Medios (CM) y Estadísticos F (para la media y la regresión ajustada) desde el origen no corregido.
2. **Evaluar Contribución Individual (Pruebas T/F parciales):** Mide cuál variable aporta más al modelo en presencia de las demás y calcula su error estándar.
3. **Probar Hipótesis Múltiple Personalizada:** Tiene un asistente interactivo que te permite probar restricciones lineales complejas (ej. $H_0: \beta_1 = \beta_2$ y $\beta_2 = \beta_3$) creando la matriz $K$ al vuelo.
4. **Predecir e Intervalos:** Permite ingresar un nuevo vector $x_0$ para obtener la predicción puntual $\hat{Y}$, la varianza de la predicción, y el intervalo de confianza de la predicción al 95%.

---

## Módulos Internos (El Motor)
Todos estos scripts se apoyan en módulos subyacentes escritos a mano:
- **`matriz.py` / `inversa.py`:** Operaciones algebraicas básicas (producto punto, transpuesta, inversa por Gauss-Jordan).
- **`tabla_f.py`:** Calculadora de valores críticos $F_{crit}$ de Fisher mediante interpolación y aproximaciones de distribución.
- **`hipotesis.py` / `constructor.py`:** Motor para la hipótesis general lineal de la forma $K\beta = m$.
- **`modulo_anova.py`:** Consolida toda la matemática profunda para `3_solver.py`.

## Cómo Usarlo
Descarga los archivos a tu calculadora o computadora. Si necesitas el solucionador, simplemente abre `3_solver.py`, edita directamente las variables `XtX`, `XtY`, `YtY` y `n` en la parte superior del archivo, guarda, y corre el script en la terminal para acceder al menú.
