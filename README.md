# ❄️ Sistema de Monitoreo Predictivo – Enfriadores de Ácido Sulfúrico CAP-3 (Secado / Interpaso / Final)

**Autor:** Sebastián Marinovic Leiva  
**División:** Chuquicamata – Codelco | **Gerencia:** Fundición | **Superintendencia:** Planta de Ácido y Oxígeno  
**Contexto:** Concurso “Me pongo la camiseta por Chuqui” – Innovación y Mejora Operacional (Sindicato 3)

---

## 1) Problema operacional
Los enfriadores de ácido sulfúrico CAP-3 son equipos críticos dentro del circuito de absorción. La degradación térmica por ensuciamiento (fouling) y las variaciones en las condiciones de agua de enfriamiento pueden provocar:

- Sobrecalentamiento del ácido, con riesgo para la seguridad del proceso y la estabilidad operacional.
​
- Mantenimiento reactivo y más costoso, al no anticipar la evolución del fouling.​

- Limpiezas químicas poco oportunas (muy tempranas o demasiado tardías), que reducen la eficiencia global del sistema.
​
- Potenciales paros no programados y pérdida de disponibilidad de los enfriadores y de la planta asociada.
​
---

## 2) Solución

Dashboard web en **Streamlit (Python)** que:
- Monitorea parámetros de proceso y operación (temperaturas ácido/agua, flujos, conductividad, velocidad soplador, bypass, etc.)​
- Calcula eficiencia térmica, coeficiente U, carga térmica (Q) y factor de ensuciamiento (Rf / fouling) con ecuaciones termodinámicas implementadas en applythermalmodel()
​- Construye un Índice de Criticidad (0–100) con 4 componentes ponderados (temperatura 30%, fouling 35%, eficiencia 25%, días desde lavado 10%) y clasificación cualitativa (Baja/Media/Alta/Crítica)
- ​Predice tendencia de fouling y "días a límite crítico" con Machine Learning (RandomForestClassifier + GradientBoosting para predicción de lavados en 30 días, según datos históricos disponibles)
- Genera Reporte PDF PRO con tabla comparativa de los 3 enfriadores, resumen ejecutivo automático, gráficos de tendencia y timeline de lavados históricos (usando ReportLab)

### 2.1) Justificación económica
CAPEX = USD 0, OPEX = USD 0/año (desarrollo interno + IT).
Beneficios anuales: USD 600,000 → ROI = ∞, Payback = Inmediato, VPN 10 años = USD 3.68M
Fuente ahorro	Beneficio anual
Paros evitados	USD 358K
Limpieza optimizada	USD 16K
Energía	USD 64K
Calidad producto	USD 62K

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
```
├── app.py                                  # Aplicación principal Streamlit
├── acid_coolers_CAP3_synthetic_2years.csv  # Datos históricos de operación (ejemplo)
├── chemical_washes_CAP3.csv                # Historial de lavados (ejemplo)
├── Documentacion_Tecnica_v5.md             # Documento técnico del sistema
├── Manual_Usuario_Dashboard_v5.md          # Manual de usuario del dashboard
├── Analisis_Economico_ROI_v5.md            # Análisis económico y ROI del proyecto
└── README.md                               # Este archivo
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

