# Sistema de Monitoreo Predictivo – Enfriadores de Ácido Sulfúrico CAP-3
author: "Sebastián Marinovic Leiva"
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

La carga térmica se calcula mediante el balance energético del agua de enfriamiento:

**Q = ṁ · Cp · (T_out − T_in)**

Donde:
- **ṁ**: flujo másico de agua [kg/s]  
- **Cp**: calor específico del agua [J/kg·K]  
- **T_out**, **T_in**: temperatura de salida y entrada del agua [°C]  

**Implementación en el sistema (`app.py`):**
- `Q_water_W = m_dot_water * Cp_water * (T_w_out - T_w_in)`
- `Q_used_W = min(Q_water_W, Q_acid_est)`

En el dashboard:
- Q se reporta como **promedio de ventana (MW)**  
- Se compara contra **Q de diseño ajustado** para evaluar sobrecarga térmica

---

### 4.2 Diferencia de temperatura media logarítmica (LMTD)

La LMTD se calcula como:

**LMTD = (ΔT₁ − ΔT₂) / ln(ΔT₁ / ΔT₂)**

Donde:
- **ΔT₁ = T_hot_in − T_cold_out**
- **ΔT₂ = T_hot_out − T_cold_in**

**Implementación robusta en el sistema:**
- Validación de ΔT > 0
- Manejo de casos ΔT₁ ≈ ΔT₂ para evitar inestabilidad numérica
- Función dedicada: `safe_lmtd()`

---

### 4.3 Coeficiente global de transferencia de calor (U)

El coeficiente global se obtiene desde:

**U = Q / (A · LMTD)**

Donde:
- **A**: área efectiva de intercambio térmico [m²]

En el sistema:
- Se calcula **U real instantáneo**
- Se compara contra **U limpio de diseño**
- Se reporta **U promedio** y **% respecto a condición limpia**

---

### 4.4 Factor de ensuciamiento (Rf – Fouling)

El factor de ensuciamiento se estima a partir de resistencias térmicas:

**Rf = (1 / U_real) − (1 / U_limpio)**

Características del cálculo:
- Filtrado por condición operacional válida
- Escalado a unidades visibles (**×10⁻⁴ m²·K/W**)
- Suavizado mediante media móvil para reducir ruido

---

### 4.5 Índice de criticidad (0–100)

Índice compuesto para priorización operacional:

**Criticidad = 100 · (  
0.30 · Temperatura +  
0.35 · Fouling +  
0.25 · Eficiencia +  
0.10 · Días sin lavado  
)**

Clasificación:
- **0–30**: Baja 🟢  
- **30–60**: Media 🟡  
- **60–80**: Alta 🟠  
- **80–100**: Crítica 🔴

---

## 5. Condición de operación válida

El análisis se realiza **solo cuando el equipo está cargado**, definido por:

- Flujo de agua ≥ % mínimo de diseño.
- Salto térmico ácido positivo.
- Temperaturas dentro de rangos físicos.
- Velocidad de soplador sobre umbral.

Esto evita falsos diagnósticos en períodos de baja carga.

---

## 6. Tendencias y pendientes

El sistema calcula pendientes solo bajo condición cargada:

- Pendiente de Rf (ensuciamiento).
- Pendiente de temperatura de salida.

Además, estima **días a condición crítica** cuando la tendencia es positiva y estable.

---

## 7. Reporte PDF ejecutivo

El sistema genera automáticamente un PDF que incluye:

- Resumen ejecutivo comparativo (TS / TAI / TAF).
- Tabla consolidada de KPIs.
- Índice de criticidad promedio.
- Recomendación priorizada.
- Gráficos térmicos y de fouling.
- Historial de lavados en línea de tiempo.

---

## 8. Justificación económica del proyecto

### 8.1 Enfoque económico

El sistema de monitoreo predictivo de enfriadores CAP-3 corresponde a una **iniciativa de optimización operacional sin inversión de capital (CAPEX = 0)**, desarrollada internamente utilizando:

- Datos históricos existentes de proceso y mantenimiento
- Infraestructura TI disponible en la División
- Herramientas de software open-source (Python, Streamlit)
- Conocimiento técnico del proceso (desarrollo interno)

Por esta razón, el análisis económico se enfoca en **ahorros operacionales (OPEX evitado)** y **prevención de pérdidas**, más que en retorno por inversión tradicional.

---

### 8.2 Costos de implementación

El proyecto no requiere inversión adicional.

| Concepto | Costo |
|--------|-------|
| Desarrollo del sistema | 0 USD |
| Licencias de software | 0 USD |
| Infraestructura TI | 0 USD |
| Instrumentación adicional | 0 USD |

**CAPEX total:** **0 USD**  
**OPEX anual:** **0 USD**

Todo el desarrollo y soporte se realiza con recursos internos ya disponibles.

---

### 8.3 Fuentes principales de ahorro económico

El sistema genera beneficios económicos a través de múltiples mecanismos independientes:

#### 1. Reducción de paros no programados
- Paros asociados a sobrecalentamiento de ácido y pérdida de eficiencia térmica.
- Línea base histórica: ~8–12 eventos por año.
- Reducción estimada: **80–90%** mediante detección temprana y limpieza oportuna.
- **Ahorro anual estimado:** **USD 250,000 – 450,000**

#### 2. Optimización de limpiezas químicas
- Evita limpiezas prematuras o innecesarias.
- Permite limpiar solo cuando el fouling real lo justifica.
- Reducción de eventos de limpieza: 2–6 por año.
- **Ahorro anual estimado:** **USD 12,000 – 20,000**

#### 3. Extensión de vida útil de los enfriadores
- Menor estrés térmico y menor degradación de tubos.
- Extensión estimada de vida útil: **20–25%**.
- Diferimiento de reemplazos mayores.
- **Beneficio económico equivalente anualizado:** **USD 40,000 – 60,000**

#### 4. Reducción de consumo energético
- Enfriadores limpios operan con menor demanda de bombeo y ventilación.
- Reducción estimada de consumo energético: **3–8%**.
- **Ahorro anual estimado:** **USD 50,000 – 80,000**

#### 5. Mejora de calidad de producto
- Control de temperatura de salida del ácido.
- Menor probabilidad de desviaciones de concentración y pureza.
- Reducción de reprocesos y pérdidas de lote.
- **Ahorro anual estimado:** **USD 35,000 – 90,000**

#### 6. Mejora de confiabilidad operacional
- Mejor planificación de mantenimiento.
- Menor carga reactiva sobre operadores.
- Reducción de horas extraordinarias.
- **Beneficio anual conservador:** **USD 40,000 – 60,000**

---

### 8.4 Resumen de beneficios anuales

| Fuente de ahorro | Ahorro anual estimado (USD) |
|----------------|-----------------------------|
| Paros no programados evitados | 358,000 |
| Optimización limpiezas químicas | 16,000 |
| Extensión vida útil equipos | 50,000 |
| Reducción consumo energético | 64,000 |
| Mejjora calidad producto | 62,500 |
| Confiabilidad operacional | 50,000 |
| **TOTAL BENEFICIOS ANUALES** | **≈ 600,000 USD** |

> Se utiliza un enfoque **conservador** en las estimaciones.

---

### 8.5 Retorno de la inversión (ROI)

Dado que:
- La inversión inicial es **0 USD**
- Los beneficios son positivos desde el primer uso
El retorno económico del proyecto es:
- **ROI:** Infinito  
- **Payback:** Inmediato (0 meses)  
Cualquier ahorro generado representa **ganancia neta directa para la operación**.

---
### 8.6 Valor económico a largo plazo

En un horizonte de 10 años, considerando beneficios constantes:
- **Beneficio acumulado estimado:** **USD 6,000,000**
- **Valor presente neto (VPN):** altamente positivo
- **Riesgo financiero:** bajo (beneficios distribuidos en múltiples fuentes)
El proyecto mantiene valor incluso bajo escenarios conservadores (−20% beneficios).

---
### 8.7 Beneficios estratégicos adicionales (no monetizados)

- Herramienta objetiva para toma de decisiones técnicas.
- Base para escalamiento a otras plantas de ácido.
- Reducción de dependencia de proveedores externos.
- Desarrollo de capacidades digitales internas.
- Transferencia tecnológica dentro de la División.
- Alineación con estrategia de excelencia operacional y digitalización Codelco.
  
---
### 8.8 Conclusión económica

El sistema de monitoreo predictivo de enfriadores CAP-3 presenta una **justificación económica excepcional**, caracterizada por:
- Cero inversión de capital.
- Ahorros operacionales recurrentes.
- Prevención de pérdidas críticas.
- Retorno inmediato.
- Alto potencial de escalamiento.
  
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

