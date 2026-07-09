# ANOVA y Regresión en Python (MicroPython Compatible)

Este repositorio contiene un conjunto de scripts en Python para realizar Análisis de Varianza (ANOVA) y modelos de regresión (Lineal Múltiple y Polinomial). 

**Característica Principal:** Todo el código está escrito desde cero utilizando las estructuras de datos nativas de Python (listas). **No utiliza bibliotecas externas como `numpy`, `scipy`, `sklearn` o `statsmodels`.** Esto hace que los scripts sean ideales para ejecutarse en entornos con memoria limitada o en plataformas que ejecutan MicroPython, como calculadoras gráficas científicas (por ejemplo, la serie Casio fx-CG50 o fx-CG100).

## Características

* **Operaciones Matriciales Nativas:** Implementación propia de operaciones básicas de matrices (multiplicación, transposición, inversión, etc.) en `matriz.py` e `inversa.py`.
* **Regresión Lineal Múltiple (MLR):** Ajuste de modelos con múltiples variables predictoras (`principal_mlr.py`).
* **Regresión Polinomial:** Ajuste de curvas polinomiales de cualquier grado, con análisis de sumas de cuadrados secuenciales (`principal_pol.py`).
* **Tabla ANOVA:** Cálculo y visualización de la tabla de Análisis de Varianza global para evaluar la significancia del modelo general.
* **Pruebas de Hipótesis Estructurales:** Permite probar hipótesis sobre los coeficientes del modelo ($H_0: K\beta = m$) para tomar decisiones sobre las variables.
* **Distribución F de Fisher:** Cálculo de valores críticos integrados localmente en `tabla_f.py` sin depender de módulos estadísticos de la biblioteca estándar de sistemas de escritorio.

## Estructura del Código

* `principal_mlr.py` y `principal_pol.py`: **Puntos de entrada del programa** (interfaces interactivas CLI).
* `modelo.py`: Lógica matemática central que ajusta el modelo lineal generalizado resolviendo las ecuaciones normales ($X^T X \beta = X^T y$).
* `anova.py`: Módulo que resume los resultados (Suma de Cuadrados, Cuadrados Medios, estadístico F).
* `hipotesis.py` y `constructor.py`: Facilitan la creación de pruebas de hipótesis $K\beta=m$ personalizadas o guiadas.
* `matriz.py` e `inversa.py`: Álgebra matricial en Python puro (inversión mediante eliminación de Gauss-Jordan).
* `vandermonde.py`: Generador de matriz de diseño (Vandermonde) requerida para la regresión polinomial.
* `util_datos.py`: Helper para gestionar el ingreso de matrices de datos del usuario o datos de ejemplo predeterminados.

## Cómo usar

1. Clona o descarga el repositorio en tu dispositivo o computadora.
2. Abre tu terminal.
3. Ejecuta el módulo de regresión que necesites:

**Regresión Lineal Múltiple:**
```bash
python principal_mlr.py
```

**Regresión Polinomial:**
```bash
python principal_pol.py
```

El programa te guiará con un menú interactivo. Por defecto incluye datos de ejemplo ("datos quemados") para que puedas probar el programa inmediatamente oprimiendo 1 en las primeras opciones.

## Licencia

Este proyecto está abierto a su uso y modificación. Es un recurso excelente tanto para fines educativos (aprender el álgebra matricial detrás de los modelos predictivos) como para implementaciones prácticas en hardware incrustado.
