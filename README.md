# Sistema de Diagnóstico Difuso Automotriz

Un sistema de diagnóstico basado en lógica difusa, desarrollado en Python. Utiliza una interfaz gráfica con Tkinter para simular y visualizar cómo se determina la urgencia de una revisión mecánica a partir de variables continuas como la temperatura del motor y la presión del aceite.



---

## Tabla de contenidos

- [Introducción](#introducción)
- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Modelo de Lógica Difusa](#modelo-de-lógica-difusa)
  - [Variables de Entrada](#variables-de-entrada)
  - [Variable de Salida](#variable-de-salida)
- [Base de Conocimiento (Reglas Difusas)](#base-de-conocimiento-reglas-difusas)

---

## Introducción

A diferencia de un sistema experto con reglas booleanas, este proyecto utiliza **lógica difusa** para manejar la incertidumbre y la imprecisión. El sistema no se basa en síntomas discretos (si/no), sino en valores continuos (temperatura y presión) para calcular un nivel de "urgencia" para una revisión mecánica.

El sistema está implementado con la biblioteca `scikit-fuzzy` y visualiza en tiempo real las funciones de membresía y el resultado de la inferencia usando `matplotlib`.

---

## Características

- **Interfaz Gráfica Interactiva:** Creada con Tkinter, permite al usuario modificar los valores de entrada mediante deslizadores.
- **Motor de Inferencia Difuso:** Implementado con `scikit-fuzzy` para modelar el conocimiento de manera flexible.
- **Visualización en Tiempo Real:** Gráficos de `matplotlib` integrados en la interfaz que muestran las funciones de membresía, los valores de entrada y el resultado agregado y defuzzificado.
- **Diagnóstico Gradual:** El resultado no es una simple respuesta, sino un valor numérico que indica el grado de urgencia de la acción a tomar.

---

## Instalación

1.  **Clona el repositorio en tu máquina:**
    ```bash
    git clone https://github.com/jpchavarria2/sistema-difuso-automotriz.git
    ```
2.  **Navega al directorio del proyecto:**
    ```bash
    cd sistema-difuso-automotriz
    ```
3.  **Instala las dependencias necesarias:**
    ```bash
    pip install scikit-fuzzy matplotlib numpy
    ```

---

## Uso

1.  Ejecuta el script `sd_autos.py` con Python.
    ```bash
    python sd_autos.py
    ```
2.  La interfaz se abrirá mostrando los controles y los gráficos.
3.  Mueve los deslizadores de **Temperatura** y **Presión** para simular diferentes condiciones del vehículo.
4.  Observa cómo el diagnóstico y los gráficos se actualizan en tiempo real reflejando el cálculo del sistema difuso.

---

## Modelo de Lógica Difusa

El sistema se compone de dos variables de entrada (antecedentes) y una de salida (consecuente).

### Variables de Entrada

1.  **Temperatura del Motor (°C):** Rango de `0` a `120`.
    - `frio`: Temperatura por debajo de lo normal.
    - `normal`: Rango de operación óptimo.
    - `caliente`: Sobrecalentamiento.

2.  **Presión de Aceite (PSI):** Rango de `0` a `100`.
    - `baja`: Presión insuficiente, riesgo de daño.
    - `adecuada`: Nivel de presión correcto.
    - `alta`: Presión excesiva, puede indicar un problema.

### Variable de Salida

- **Acción del Mecánico (Nivel de Urgencia):** Rango de `0` a `100`.
  - `revision_rutina`: Nivel bajo de urgencia.
  - `precaucion`: Urgencia moderada, se recomienda revisar pronto.
  - `atencion_inmediata`: Urgencia alta, riesgo inminente.

---

## Base de Conocimiento (Reglas Difusas)

El sistema toma decisiones basándose en las siguientes reglas de lógica difusa:

| Regla                                                              | Diagnóstico Sugerido        |
| ------------------------------------------------------------------ | --------------------------- |
| `SI` la **temperatura** es `caliente` `O` la **presión** es `baja`   | `ENTONCES` la acción es **atención inmediata**. |
| `SI` la **temperatura** es `normal` `Y` la **presión** es `adecuada` | `ENTONCES` la acción es **revisión de rutina**. |
| `SI` la **temperatura** es `fria` `O` la **presión** es `alta`       | `ENTONCES` la acción es **precaución**.         |