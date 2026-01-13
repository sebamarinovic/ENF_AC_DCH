---
title: "❄️ Sistema de Monitoreo Predictivo – Enfriadores de Ácido Sulfúrico CAP-3"
subtitle: "Secado / Interpaso / Final"
author: "Sebastián Marinovic Leiva"
date: "Enero 2026"
output:
  github_document:
    toc: true
    toc_depth: 3
---

## Contexto general

**División:** Chuquicamata – Codelco  
**Gerencia:** Fundición  
**Superintendencia:** Planta de Ácido y Oxígeno  

**Iniciativa:** Concurso *“Me pongo la camiseta por Chuqui”* – Sindicato 3  
**Tipo de proyecto:** Innovación, mejora operacional y confiabilidad de activos críticos  

Este repositorio documenta el desarrollo e implementación de un **sistema digital predictivo** para la gestión térmica y de ensuciamiento de los enfriadores de ácido sulfúrico de la planta CAP-3.

---

## 1. Problema operacional

Los enfriadores de ácido sulfúrico de CAP-3 (Torre de Secado, Torre de Absorción Intermedia y Torre de Absorción Final) son equipos críticos dentro del circuito de absorción.

La degradación térmica por ensuciamiento (*fouling*) y las variaciones en la calidad y condiciones del agua de enfriamiento pueden generar:

- Sobrecalentamiento del ácido, con riesgos para la seguridad del proceso.
- Operación cercana o fuera de límites de diseño.
- Mantenimiento reactivo y aumento de costos operacionales.
- Limpiezas químicas mal temporizadas (anticipadas o tardías).
- Pérdida de eficiencia térmica y disponibilidad de planta.
- Mayor probabilidad de paros no programados.

---

## 2. Solución implementada (`app.py`)

Se desarrolló un **dashboard web en Streamlit (Python)** que permite:

- Monitorear variables de proceso y operación:
  - Temperaturas de ácido y agua
  - Flujos
  - Conductividad
  - Carga de producción
  - Estados operacionales (sopladores, bypass, etc.)

- Calcular KPIs térmicos mediante modelos de ingeniería:
  - Carga térmica (Q)
  - Coeficiente global de transferencia (U)
  - Eficiencia térmica
  - Factor de ensuciamiento (Rf)

- Construir un **Índice de Criticidad (0–100)** para priorizar lavados químicos.

- Analizar **tendencias y pendientes** solo bajo condición cargada.

- Generar **reportes PDF ejecutivos** automáticos con tablas comparativas, gráficos y recomendaciones priorizadas.

---

## 3. Modelo de ingeniería implementado

### 3.1 Carga térmica (Q)

La carga térmica se calcula a partir del balance energético del agua de enfriamiento:

\[
Q = \dot{m} \cdot C_p \cdot (T_{out} - T_{in})
\]

Donde:

- \(\dot{m}\): flujo másico del agua  
- \(C_p\): calor específico  
- \(\Delta T\): salto térmico  

En el sistema:
- Se reporta **Q promedio (MW)** por ventana de análisis.
- Se compara con **Q de diseño ajustado**, considerando la condición real del equipo.

---

### 3.2 Diferencia de temperatura media logarítmica (LMTD)

\[
\Delta T_{lm} = \frac{\Delta T_1 - \Delta T_2}{\ln\left(\frac{\Delta T_1}{\Delta T_2}\right)}
\]

Implementada con validaciones para evitar errores numéricos en condiciones cercanas a equilibrio térmico.

---

### 3.3 Coeficiente global de transferencia (U)

\[
Q = U \cdot A \cdot \Delta T_{lm}
\]

El sistema recalcula \(U\) considerando:

- Área efectiva disponible
- Tubos aislados o fuera de servicio
- Condición real de operación

---

### 3.4 Eficiencia térmica

\[
\eta_{térmica} = \frac{Q_{real}}{Q_{diseño\ ajustado}} \cdot 100
\]

Esto evita penalizar artificialmente equipos con reducción real de área de transferencia.

---

### 3.5 Factor de ensuciamiento (Rf / fouling)

El ensuciamiento se modela como una resistencia térmica adicional:

- Unidad base: \(m^2 \cdot K / W\)
- Visualización escalada para análisis operacional

El sistema utiliza un enfoque robusto:

- Método directo vía resistencias térmicas
- Método indirecto vía pérdida de eficiencia
- Suavizado temporal (media móvil)

---

## 4. Índice de criticidad operacional

Se define un **índice adimensional entre 0 y 100**, compuesto por:

| Componente            | Peso |
|----------------------|------|
| Temperatura ácido    | 30%  |
| Fouling (Rf)         | 35%  |
| Eficiencia térmica   | 25%  |
| Días desde lavado    | 10%  |

Clasificación:

- **0–30:** Baja 🟢  
- **30–60:** Media 🟡  
- **60–80:** Alta 🟠  
- **80–100:** Crítica 🔴  

Este índice es el **criterio principal** para recomendar limpieza química.

---

## 5. Tendencias y análisis bajo condición cargada

El sistema calcula pendientes solo cuando el equipo se encuentra **realmente cargado**, definido por:

- Carga térmica sobre umbral mínimo
- Flujo de agua válido
- Operación estable del sistema

Ejemplos:
- Pendiente de Rf \([m^2K/W \cdot día]\)
- Pendiente de temperatura de salida \([°C/día]\)

Esto evita falsas alarmas durante períodos de baja carga.

---

## 6. Reporte PDF ejecutivo

El sistema genera automáticamente un **PDF profesional**, que incluye:

- Resumen ejecutivo comparativo (TS / TAI / TAF)
- Tabla de KPIs principales
- Índice de criticidad y recomendación priorizada
- Gráficos térmicos y de fouling
- Historial de lavados en línea de tiempo

---

## 7. Justificación económica del proyecto

### 7.1 Enfoque del análisis económico

Este proyecto corresponde a una **iniciativa sin CAPEX**, desarrollada internamente utilizando:

- Datos existentes
- Conocimiento técnico del proceso
- Herramientas open-source

El análisis económico se centra en **ahorros OPEX** y **evitación de pérdidas operacionales**.

---

### 7.2 Costos evitados por lavados químicos no óptimos

Cada lavado químico implica:

- Insumos
- Mano de obra
- Pérdida de disponibilidad
- Riesgos post-intervención

El sistema permite optimizar la frecuencia, evitando lavados innecesarios o tardíos.

---

### 7.3 Costos evitados por eventos críticos

La detección temprana de degradación térmica reduce la probabilidad de:

- Restricciones de carga
- Intervenciones no planificadas
- Eventos de sobretemperatura

Estos costos evitados representan un beneficio económico significativo.

---

### 7.4 Optimización energética

Mantener los enfriadores en condición óptima implica:

- Menor consumo energético específico
- Operación más estable
- Menor estrés térmico del sistema

---

### 7.5 Costos de implementación

| Concepto                    | Costo |
|----------------------------|-------|
| Desarrollo del sistema     | 0 USD |
| Licencias de software      | 0 USD |
| Infraestructura adicional | 0 USD |
| Sensores adicionales      | 0 USD |

**CAPEX total:** **0 USD**

---

### 7.6 Retorno de la inversión (ROI)

\[
ROI = \frac{Beneficios}{Inversión} \rightarrow \infty
\]

El sistema genera valor económico desde el primer uso.

---

## 8. Arquitectura del repositorio

```text
ENF_AC_DCH/
├── app.py
├── acid_coolers_CAP3_synthetic_2years.csv
├── chemical_washes_CAP3.csv
├── Documentacion_Tecnica_v5.md
├── Manual_Usuario_Dashboard_v5.md
├── Analisis_Economico_ROI_v5.md
└── README.md

---

## 7) Instalación y ejecución

### 7.1 Requisitos
- Python 3.9+ recomendado

### 7.2 Instalar dependencias
```bash
pip install -r requirements.txt
streamlit run app.py
```

