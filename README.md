# ❄️ Sistema de Monitoreo Predictivo – Enfriadores de Ácido Sulfúrico CAP-3 (Secado / Interpaso / Final)

**Autor:** Sebastián Marinovic Leiva  
**División:** Chuquicamata – Codelco | **Gerencia:** Fundición | **Superintendencia:** Planta de Ácido y Oxígeno  
**Contexto:** Concurso “Me pongo la camiseta por Chuqui” – Innovación y Mejora Operacional (Sindicato 3)

---

## 1) Problema operacional

Los enfriadores de ácido sulfúrico CAP-3 son **equipos críticos**. La degradación térmica por ensuciamiento (fouling), variaciones de agua de enfriamiento y pérdida de área efectiva por **tubos aislados** puede provocar:

- Sobrecalentamiento del ácido (riesgo de seguridad y estabilidad operacional)
- Mantenimiento reactivo y costoso
- Limpiezas químicas no optimizadas
- Potenciales paros no programados y pérdida de disponibilidad

---

## 2) Solución

Dashboard web en **Streamlit (Python)** que:

✅ Monitorea parámetros de proceso y operación  
✅ Calcula **eficiencia térmica**, **U**, **carga térmica (Q)** y **factor de ensuciamiento (Rf / fouling)**  
✅ Construye un **Índice de Criticidad (0–100)** con reglas y ponderaciones  
✅ Predice tendencia y “días a límite” con **Machine Learning** (según disponibilidad de datos)  
✅ Incorpora módulo de **Gestión de Tubos Aislados** (recalcula capacidad/diseño automáticamente)  
✅ Genera **Reporte PDF PRO** (tabla comparativa + resumen ejecutivo + historial de lavados tipo timeline)

---

## 3) KPI principales (qué mide el sistema)

### 3.1 Carga térmica (Q)
Se estima el calor transferido con base en el balance térmico:

**Q = ṁ · Cp · ΔT**

Donde:
- ṁ = flujo másico
- Cp = calor específico
- ΔT = diferencia de temperatura entre entrada/salida

> En el sistema se reporta **Q promedio en MW** y su % vs diseño para evidenciar sobrecarga térmica.

---

### 3.2 Coeficiente global de transferencia (U)
La transferencia de calor global se expresa como:

**Q = U · A · ΔT\_lm**

- U: coeficiente global
- A: área efectiva de transferencia
- ΔT\_lm: diferencia de temperatura media logarítmica

---

### 3.3 Eficiencia térmica (%)
Mide desempeño vs diseño (ajustado por condición real):

**η\_térmica = (Q\_actual / Q\_diseño\_ajustado) · 100**

Clave: si hay **tubos aislados**, el sistema ajusta el diseño para no “castigar” artificialmente al equipo.

---

### 3.4 Factor de ensuciamiento (Rf / fouling)
Representa resistencia adicional por depósitos:

- Unidades típicas: **m²·K/W** (en el dashboard se muestra en escala “visible”, p.ej. ×10⁻⁴)

El sistema implementa un enfoque “robusto” combinando:
- Método directo vía U (resistencias térmicas)
- Método indirecto vía pérdida de eficiencia
- Suavizado (media móvil) para reducir ruido

---

### 3.5 Días desde último lavado + Historial
- “Días sin lavado” como contexto operacional
- Historial de lavados en **línea de tiempo (timeline)** y resumen por enfriador

---

### 3.6 Índice de criticidad (0–100)
Score multifactorial para priorizar intervención entre:
- Torre Secado (TS)
- Torre Absorción Intermedia (TAI)
- Torre Absorción Final (TAF)

Ejemplo de lógica (referencial):
- Temperatura (ponderación alta por seguridad y calidad)
- Eficiencia (desempeño directo)
- Conductividad (calidad de agua: causa raíz frecuente de fouling)
- Fouling (resultado acumulado del sistema)
- Tiempo sin lavado (solo como contexto)

Salida:
- 0–30: Baja 🟢
- 30–60: Media 🟡
- 60–80: Alta 🟠
- 80–100: Crítica 🔴

---

## 4) Machine Learning (ML)

El ML se utiliza para **proyección de tendencia** y estimación de “días a límite” (térmico / fouling),
**solo si existe data suficiente y representativa**.

- Modelo: selección automática (según disponibilidad y calidad de datos)
- Validación: métricas tipo R²/RMSE para regresión y diagnósticos de entrenabilidad
- Fallback: si el ML no es entrenable (p. ej., datos insuficientes), el sistema usa un **Score Operacional** (reglas) para mantener recomendaciones consistentes.

---

## 5) Reporte PDF PRO (salida ejecutiva)

El sistema genera un PDF con:
- **Resumen ejecutivo comparativo** (los 3 enfriadores)
- Tabla de KPI (T salida, U, Rf, Q, días sin lavado, criticidad)
- Recomendación priorizada automática
- Sección de ML (si aplica) y diagnóstico
- Historial de lavados en timeline

---

## 6) Arquitectura del repositorio
```text
ENF_AC_DCH/
├── app.py
├── acid_coolers_CAP3_synthetic_2years.csv
├── chemical_washes_CAP3.csv
├── requirements.txt
├── README.md
├── README.Rmd
└── docs/
    ├── Propuesta_Marinovic_FINAL.pdf
    ├── Documentacion_Tecnica_FINAL.pdf
    └── images/
        ├── 01_resumen_ejecutivo.png
        ├── 02_termico.png
        ├── 03_fouling.png
        ├── 04_criticidad.png
        ├── 05_lavados_timeline.png
        └── 06_pdf.png
```
### 📸 Vistas principales del sistema

![Resumen Ejecutivo](docs/images/01_resumen_ejecutivo.png)
![Análisis Térmico](docs/images/02_termico.png)
![Fouling y eficiencia](docs/images/03_fouling.png)
![Índice de criticidad](docs/images/04_criticidad.png)

---

## 7) Instalación y ejecución

### 7.1 Requisitos
- Python 3.9+ recomendado

### 7.2 Instalar dependencias
```bash
pip install -r requirements.txt
streamlit run app.py
```

