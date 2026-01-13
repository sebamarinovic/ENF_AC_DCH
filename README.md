----
title: "❄️ Sistema de Monitoreo Predictivo – Enfriadores de Ácido Sulfúrico CAP-3"
subtitle: "Secado / Interpaso / Final"
author: "Sebastián Marinovic Leiva"
date: "Enero 2026"
output:
  github_document:
    toc: true
    toc_depth: 3
---

## Contexto del proyecto

**División:** Chuquicamata – Codelco  
**Gerencia:** Fundición  
**Superintendencia:** Planta de Ácido y Oxígeno  

**Iniciativa:** Concurso *“Me pongo la camiseta por Chuqui”* – Sindicato 3  
**Tipo:** Innovación operacional y confiabilidad de activos  

Este repositorio documenta el desarrollo e implementación de un **sistema digital de monitoreo predictivo** para los enfriadores de ácido sulfúrico de la planta CAP-3, integrando modelos de ingeniería térmica, análisis de ensuciamiento y criterios objetivos de criticidad operacional.

---

## 1. Problema operacional

Los enfriadores de ácido sulfúrico CAP-3 (Torre de Secado, Torre de Absorción Intermedia y Torre de Absorción Final) son activos críticos del circuito de absorción. Su degradación térmica por ensuciamiento (*fouling*) y variaciones en la calidad del agua de enfriamiento generan:

- Incremento de temperatura del ácido, con riesgo para la seguridad del proceso.
- Operación fuera de condiciones óptimas de diseño.
- Mantención reactiva y mayores costos operacionales.
- Limpiezas químicas mal temporizadas.
- Reducción de disponibilidad y eficiencia global de planta.
- Mayor probabilidad de eventos no programados.

---

## 2. Objetivo del sistema

Desarrollar una herramienta digital que permita:

- Detectar tempranamente la degradación térmica.
- Priorizar limpiezas químicas en base a criterios objetivos.
- Reducir riesgos operacionales.
- Optimizar costos de mantención.
- Entregar soporte técnico cuantitativo a la toma de decisiones.

---

## 3. Solución implementada (`app.py`)

Se desarrolló un **dashboard web en Streamlit (Python)** que:

- Integra datos históricos de proceso y operación.
- Aplica modelos de ingeniería térmica en tiempo casi real.
- Calcula KPIs críticos por ventana de operación válida.
- Construye un **Índice de Criticidad (0–100)** como principal criterio de decisión.
- Analiza tendencias solo bajo condición cargada.
- Genera reportes PDF ejecutivos automáticos.

---

## 4. Modelo de ingeniería aplicado

### 4.1 Carga térmica (Q)

Balance energético del agua de enfriamiento:

\[
Q = \dot{m} \cdot C_p \cdot (T_{out} - T_{in})
\]

Donde:

- \(\dot{m}\): flujo másico del agua  
- \(C_p\): calor específico  
- \(\Delta T\): salto térmico  

En el sistema:
- Q se reporta como **promedio de ventana (MW)**.
- Se compara contra **Q de diseño ajustado**.

---

### 4.2 Diferencia de temperatura media logarítmica (LMTD)

\[
\Delta T_{lm} = \frac{\Delta T_1 - \Delta T_2}{\ln\left(\frac{\Delta T_1}{\Delta T_2}\right)}
\]

Implementada con validaciones para evitar inestabilidades numéricas.

---

### 4.3 Coeficiente global de transferencia (U)

\[
Q = U \cdot A \cdot \Delta T_{lm}
\]

- Se recalcula U considerando área efectiva real.
- Se compara contra U limpio de diseño.

---

### 4.4 Eficiencia térmica

\[
\eta = \frac{Q_{real}}{Q_{diseño\ ajustado}} \cdot 100
\]

Evita penalizar equipos con tubos aislados o fuera de servicio.

---

### 4.5 Factor de ensuciamiento (Rf)

El fouling se modela como resistencia térmica adicional:

- Unidad base: \(m^2K/W\)
- Visualización escalada para análisis operacional.

Se utiliza un enfoque robusto:
- Método directo vía resistencias térmicas.
- Método indirecto vía pérdida de eficiencia.
- Suavizado mediante medias móviles.

---

## 5. Condición de operación válida

El análisis se realiza **solo cuando el equipo está cargado**, definido por:

- Flujo de agua ≥ % mínimo de diseño.
- Salto térmico ácido positivo.
- Temperaturas dentro de rangos físicos.
- Velocidad de soplador sobre umbral.

Esto evita falsos diagnósticos en períodos de baja carga.

---

## 6. Índice de criticidad operacional

El **Índice de Criticidad (0–100)** es el criterio principal para recomendar limpieza química.

### Componentes y ponderación

| Variable | Peso |
|--------|------|
| Temperatura ácido salida | 30% |
| Fouling (Rf) | 35% |
| Eficiencia térmica | 25% |
| Días desde último lavado | 10% |

### Clasificación

- **0–30:** Baja 🟢  
- **30–60:** Media 🟡  
- **60–80:** Alta 🟠  
- **≥80:** Crítica 🔴  

---

## 7. Tendencias y pendientes

El sistema calcula pendientes solo bajo condición cargada:

- Pendiente de Rf (ensuciamiento).
- Pendiente de temperatura de salida.

Además, estima **días a condición crítica** cuando la tendencia es positiva y estable.

---

## 8. Reporte PDF ejecutivo

El sistema genera automáticamente un PDF que incluye:

- Resumen ejecutivo comparativo (TS / TAI / TAF).
- Tabla consolidada de KPIs.
- Índice de criticidad promedio.
- Recomendación priorizada.
- Gráficos térmicos y de fouling.
- Historial de lavados en línea de tiempo.

---

## 9. Justificación económica

### 9.1 Enfoque

Proyecto desarrollado **sin CAPEX**, utilizando:

- Datos existentes.
- Infraestructura disponible.
- Software open-source.
- Desarrollo interno.

---

### 9.2 Beneficios económicos

- Reducción de limpiezas químicas innecesarias.
- Prevención de eventos críticos.
- Menor mantención reactiva.
- Mayor disponibilidad de planta.
- Optimización energética indirecta.

---

### 9.3 Costos de implementación

| Concepto | Costo |
|-------|------|
| Desarrollo | 0 USD |
| Licencias | 0 USD |
| Infraestructura | 0 USD |
| Instrumentación | 0 USD |

**CAPEX total:** **0 USD**

---

### 9.4 Retorno de la inversión

\[
ROI = \frac{Beneficios}{Inversión} \rightarrow \infty
\]

El sistema genera valor desde el primer uso.

---

## 10. Arquitectura del repositorio

```text
ENF_AC_DCH/
├── app.py
├── acid_coolers_CAP3_synthetic_2years.csv
├── chemical_washes_CAP3.csv
├── Documentacion_Tecnica_v5.md
├── Manual_Usuario_Dashboard_v5.md
├── Analisis_Economico_ROI_v5.md
└── README.md
```
---
## 11. Instalación y ejecución

### 11.1 Requisitos
- Python 3.9+ recomendado

### 11.2 Instalar dependencias
```bash
pip install -r requirements.txt
streamlit run app.py
```

