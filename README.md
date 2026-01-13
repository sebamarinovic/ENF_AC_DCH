# Sistema de Monitoreo Predictivo – Enfriadores de Ácido Sulfúrico CAP-3

**Autor:** Sebastián Marinovic Leiva  
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

La carga térmica se calcula mediante el balance energético del agua de enfriamiento:

**Q = ṁ · Cp · (T_out − T_in)**

Donde:
- **ṁ**: flujo másico de agua [kg/s]  
- **Cp**: calor específico del agua [J/kg·K]  
- **T_out**, **T_in**: temperatura de salida y entrada del agua [°C]  

En el sistema:
- Q se reporta como **promedio de ventana (MW)**  
- Se compara contra **Q de diseño ajustado** para evaluar sobrecarga térmica

---

### 4.2 Diferencia de temperatura media logarítmica (LMTD)

**LMTD = (ΔT₁ − ΔT₂) / ln(ΔT₁ / ΔT₂)**

Cálculo robusto con:
- Validación de ΔT positivos
- Manejo de casos cercanos para evitar inestabilidad numérica

---

### 4.3 Coeficiente global de transferencia de calor (U)

**U = Q / (A · LMTD)**

En el sistema:
- Se calcula U real promedio
- Se compara con condición limpia
- Se expresa como % de desempeño térmico

---

### 4.4 Factor de ensuciamiento (Rf)

**Rf = (1 / U_real) − (1 / U_limpio)**

Características:
- Filtrado por condición operacional válida
- Escalado a unidades visibles (×10⁻⁴ m²·K/W)
- Suavizado para reducción de ruido

---

### 4.5 Índice de criticidad (0–100)

Índice compuesto para priorización operacional:

- Temperatura: 30%
- Fouling: 35%
- Eficiencia térmica: 25%
- Días sin lavado: 10%

Clasificación:
- 0–30: Baja 🟢  
- 30–60: Media 🟡  
- 60–80: Alta 🟠  
- 80–100: Crítica 🔴

---

## 5. Condición de operación válida

El análisis se realiza **solo cuando el equipo está cargado**, definido por:

- Flujo de agua ≥ umbral mínimo de diseño.
- Salto térmico ácido positivo.
- Temperaturas dentro de rangos físicos.
- Velocidad de soplador sobre umbral operacional.

Esto evita diagnósticos erróneos en períodos de baja carga.

---

## 6. Tendencias y pendientes

Se calculan pendientes solo bajo condición cargada:

- Pendiente de Rf (ensuciamiento).
- Pendiente de temperatura de salida.

Además, se estima **días a condición crítica** cuando la tendencia es positiva y estable.

---

## 7. Machine Learning supervisado aplicado al sistema

El Machine Learning se utiliza como **apoyo analítico**, no como decisor principal.

- Tipo: aprendizaje supervisado.
- Modelos: Random Forest y Gradient Boosting.
- Objetivo: anticipar tendencias y escenarios críticos.

El ML:
- Proyecta deterioro térmico
- Estima días a condición crítica
- Refuerza la priorización basada en criticidad

Si no existe data suficiente:
- El ML se desactiva automáticamente
- El sistema continúa operando solo con ingeniería y reglas

---

## 8. Justificación económica del proyecto

### 8.1 Enfoque económico

Proyecto de **optimización operacional sin CAPEX**, desarrollado internamente.

---

### 8.2 Costos de implementación

| Concepto | Costo |
|--------|-------|
| Desarrollo | 0 USD |
| Licencias | 0 USD |
| Infraestructura | 0 USD |
| Instrumentación | 0 USD |

**CAPEX total:** 0 USD

---

### 8.3 Beneficios económicos

- Reducción de paros no programados
- Optimización de limpiezas químicas
- Extensión de vida útil de equipos
- Reducción de consumo energético
- Mejora de confiabilidad operacional

**Beneficio anual estimado:** ≈ **600,000 USD**

---

### 8.4 Retorno de la inversión

- ROI: Infinito  
- Payback: Inmediato  

---

## 9. Arquitectura del repositorio

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
## 10. Instalación y ejecución

### 10.1 Requisitos
- Python 3.9+ recomendado

### 10.2 Instalar dependencias
```bash
pip install -r requirements.txt
streamlit run app.py
```

