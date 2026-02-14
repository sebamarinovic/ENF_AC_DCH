Readme · MD
Copiar

# ❄️ Sistema de Monitoreo Predictivo – Enfriadores de Ácido Sulfúrico CAP-3

Sistema de monitoreo predictivo para enfriadores de ácido sulfúrico en **CAP-3 (Chuquicamata – Codelco)**, basado en fundamentos de transferencia de calor, análisis de ensuciamiento (fouling), criticidad operativa y modelos de Machine Learning para apoyar decisiones de operación y mantención.

**Enfriadores monitoreados (CAP-3):**

- Secado
- Absorción Intermedia
- Absorción Final

---

## 🚀 Objetivo

Detectar degradación térmica, ensuciamiento y condiciones anómalas en los enfriadores CAP-3, entregando:

- Indicadores térmicos (eficiencia y capacidad)
- Factor de fouling robusto (método dual)
- Índice de criticidad
- Predicciones y alertas con ML
- Recomendaciones operacionales y de mantención

---

## 📚 Antecedentes Teóricos

### Transferencia de calor en intercambiadores

Los enfriadores de ácido sulfúrico en CAP-3 son intercambiadores de calor de carcasa y tubos (shell & tube), donde el ácido sulfúrico circula por el lado carcasa y el agua de enfriamiento por el lado tubos. La ecuación fundamental que gobierna el intercambio térmico es:

```
Q = U · A · ΔTLM
```

Donde **Q** es la tasa de transferencia de calor (kW), **U** es el coeficiente global de transferencia (W/m²·K), **A** es el área de transferencia (m²) y **ΔTLM** es la diferencia de temperatura media logarítmica.

### Ensuciamiento (Fouling)

El ensuciamiento es el proceso de acumulación de depósitos no deseados sobre las superficies de transferencia, que genera una resistencia térmica adicional. El factor de ensuciamiento se define como:

```
Rf = (1/U_sucio) − (1/U_limpio)   [m²·K/W]
```

En enfriadores de ácido sulfúrico, las principales fuentes de fouling incluyen depósitos de sulfatos, corrosión del material de tubos y precipitación de sólidos disueltos. El sistema utiliza un **método dual robusto** que combina:

1. **Método directo:** Cálculo de Rf a partir de la caída del coeficiente global U respecto al valor de diseño (U limpio).
2. **Método indirecto:** Estimación de Rf a partir de la pérdida de eficiencia térmica (η) observada respecto al diseño.

Ambos métodos se ponderan, se suavizan con media móvil y se escalan (×10⁻⁴ m²·K/W) para facilitar la visualización y comparación.

### Eficiencia térmica (η)

La eficiencia térmica se define como la relación entre el calor efectivamente transferido y el calor de diseño (con área y condiciones ajustadas):

```
η = Q_real / Q_design_ajustado × 100 [%]
```

El Q de diseño se ajusta automáticamente cuando existen tubos aislados, evitando falsos diagnósticos de baja eficiencia que en realidad corresponden a pérdida de área de transferencia y no a ensuciamiento.

### Índice de criticidad

El score de criticidad integra tres dimensiones ponderadas:

- **Severidad:** Impacto térmico (desviación de T° salida respecto al límite, pérdida de eficiencia).
- **Probabilidad:** Tendencias de fouling y tasa de cambio de T° (dT/dt).
- **Exposición:** Estado de equipos en servicio, redundancias disponibles y condición de componentes auxiliares (demister, bombas, válvulas).

El resultado es un score 0–100 con clasificación por umbrales: Baja (0–30), Media (30–60), Alta (60–80) y Crítica (80–100).

### Gestión de tubos aislados

Cuando se detectan fugas internas, los tubos afectados se aíslan (tapan) para evitar contaminación cruzada ácido/agua. Esto reduce el área efectiva de transferencia. El sistema:

- Recalcula el área efectiva: `A_eff = A_por_tubo × (N_total − N_aislados)`
- Ajusta Q_design proporcionalmente al factor de reducción.
- Recalibra la línea base de eficiencia, evitando que una baja por pérdida de área se interprete erróneamente como fouling.

### Materiales

Los tubos de los enfriadores están fabricados en **ZeCor-Z**, una aleación resistente a la corrosión por ácido sulfúrico concentrado a alta temperatura, con diámetro de 25.4 mm y longitud de 6.0 m.

---

## ✨ Funcionalidades principales

### 1) Eficiencia térmica (η)

- Cálculo de desempeño térmico respecto a diseño.
- Interpreta degradación por ensuciamiento vs. restricciones operacionales.

### 2) Factor de Ensuciamiento (Fouling) – Método Dual Robusto

Combina:

1. **Método directo** por coeficiente global U
2. **Método indirecto** por pérdida de eficiencia

Luego pondera, suaviza (media móvil) y escala para visualización.

### 3) ⭐ Gestión de Tubos Aislados (feature clave)

Cuando hay tubos tapados/aislados por fugas:

- Ajusta automáticamente el área efectiva de transferencia.
- Ajusta el `Q_design` y la línea base de eficiencia.
- Evita falsos diagnósticos (p. ej., eficiencia "baja" por pérdida de área y no por fouling).

### 4) Índice de Criticidad

Score compuesto (ponderado) para priorización de acciones (operación/mantención).

### 5) Machine Learning

- **RandomForestRegressor** para predicción (ej. T salida ácido) usando variables de proceso.
- **Isolation Forest** para detección de anomalías operacionales (eventos súbitos, combinaciones inusuales, etc.).
- Proyección de "días hasta mantenimiento" por tendencia operacional (cuando aplique).

---

## 📊 Factibilidad Técnica

### Arquitectura (CAPEX = 0)

El sistema está diseñado para operar sin inversión de capital, utilizando herramientas open-source y recursos computacionales mínimos:

| Capa | Implementación |
|---|---|
| **Adquisición** | Extracción periódica desde PI System (API/connector) + validación de calidad |
| **Procesamiento** | Python (pandas/numpy) · feature engineering · cálculo fouling/ΔT · scoring |
| **Persistencia** | CSV/Parquet local + backup en nube (S3 o equivalente) |
| **Aplicación** | Streamlit (dashboard interactivo con 7 módulos) |
| **Alertas** | Reglas + umbrales + salida a correo/Telegram/Teams |

### Fuentes de datos

- **PI System:** >100 tags de proceso (temperaturas ácido/agua, ΔT por equipo, ΔP demister/venturi, estados bombas, caudales, conductividad, etc.).
- **Registros de lavados:** Histórico de lavados químicos/mecánicos (planificación + ejecución).
- **Datos de mantención:** Condición de demister, bombas, válvulas y componentes auxiliares.
- **Base de pérdidas operacionales:** Vínculo entre condición CAP-3 e impacto en Fusión (HF).

### Variables del modelo

**Variables base del dataset:**

| Variable | Descripción |
|---|---|
| `T_acid_in_C` / `T_acid_out_C` | Temperatura ácido entrada/salida (°C) |
| `T_water_in_C` / `T_water_out_C` | Temperatura agua entrada/salida (°C) |
| `F_water` | Caudal de agua de enfriamiento |
| `cond_uS_cm` | Conductividad (µS/cm) |
| `dT_acid` | Delta de temperatura del ácido (°C) |
| `FLUJO_CAP3` | Flujo de proceso CAP-3 |
| `%VELOCIDAD_SOPLADOR` | Velocidad del soplador (%) |
| `CARGA_HORNO_FLASH` | Carga del horno Flash |
| `EQUIPOS_CPS_EN_SERVICIO` | Equipos CPS en servicio |
| `FLUJO_TORRE_ENFRIAMIENTO_4` | Flujo torre de enfriamiento N°4 |
| `FLUJO_AGUA_DESMIN_BHZ_305` | Flujo agua desmineralizada BHZ-305 |

**Variables derivadas (feature engineering):** ΔT por equipo, medias móviles/rolling windows, tasas de cambio (dT/dt) e indicadores de ensuciamiento.

### Especificaciones de diseño por enfriador

| Parámetro | Secado | Abs. Intermedia | Abs. Final |
|---|---|---|---|
| T° entrada diseño (°C) | 75 | 77 | 71 |
| T° salida diseño (°C) | 65 | 66 | 63 |
| ΔT diseño (°C) | 10 | 11 | 8 |
| Caudal agua diseño | 900 | 990 | 960 |
| Q diseño base (kW) | 13,232 | 31,073 | 7,188 |
| T° salida máxima (°C) | 70 | 72 | 68 |
| N° tubos totales | 632 | 883 | 197 |
| Material tubos | ZeCor-Z | ZeCor-Z | ZeCor-Z |

### Volumen de datos

- Histórico: dataset sintético de 2 años (~17,500+ registros por enfriador, frecuencia horaria).
- Proyección operacional: ≥1,000,000 filas/año con datos reales de PI.

### Roadmap de implementación

| Fase | Alcance | Plazo estimado |
|---|---|---|
| **Fase 1** | Conexión de tags PI + normalización | 1–2 semanas |
| **Fase 2** | Dashboard operativo + mapa de criticidad | 2–3 semanas |
| **Fase 3** | Modelo ML supervisado + reglas de alerta + validación en terreno | 3–6 semanas |

---

## 💰 Análisis Económico (Caso de Negocio)

### Problema cuantificado

La condición de alta temperatura del ácido / circuito de enfriamiento en CAP-3 se asocia directamente a pérdidas de disponibilidad que impactan la producción de Fusión (HF). A partir de la base "Factorial Pérdidas Fusión HF" (año 2025, filtro: Unidad=PAS, Falla contiene "Disponibilidad CAP III"):

| Indicador | Valor 2025 |
|---|---|
| Eventos registrados | 33 |
| Pérdidas de Fusión asociadas | 6,255.35 ton/año |
| Duración acumulada | 108.88 h |
| Tiempo detención acumulado | 179.10 h |

### Escenario de mejora

Se adopta un **techo conservador del 70%** de reducción del impacto atribuible:

```
Toneladas evitadas/año = 6,255.35 × 0.70 = 4,378.74 ton/año
```

### Modelo de costos

| Concepto | Valor |
|---|---|
| **CAPEX** | US$ 0 (sin inversión de capital) |
| **OPEX anual** | US$ 1,000/año (almacenaje/backup en nube) |

### Modelo de VAN (NPV)

Con horizonte de **5 años** y tasa de descuento del **10%** (factor presente = 3.7908):

```
Beneficio neto anual = (Ton evitadas × Valor_US$/ton) − US$ 1,000
VAN = Beneficio neto anual × 3.7908
```

### Análisis de sensibilidad

| Valor US$/ton | Beneficio neto anual (US$) | VAN 5 años @10% (US$) |
|---|---|---|
| 25 | 108,468 | 411,181 |
| 50 | 217,937 | 826,153 |
| 75 | 327,406 | 1,241,124 |
| 100 | 436,874 | 1,656,096 |
| 150 | 655,811 | 2,486,040 |
| 200 | 874,748 | 3,315,983 |

**Punto de equilibrio:** Valor ≥ 0.228 US$/ton para cubrir OPEX. El payback del costo anual de nube es prácticamente inmediato para cualquier criterio económico realista.

> **Nota:** El VAN oficial se cerrará una vez que Control de Gestión defina el valor unitario (US$/ton de fusión no perdida) según criterio corporativo (margen, contribución o costo de oportunidad).

---

## 🧱 Arquitectura del repositorio

```
CAP3_Coolers_Monitor/
├── app.py                                          # Dashboard Streamlit (7 tabs)
├── requirements.txt
├── data/
│   ├── acid_coolers_CAP3_synthetic_2years.csv       # Dataset principal (ácido)
│   └── t_water_in_out_CAP3_synthetic_2years.csv     # Dataset agua enfriamiento
├── docs/
│   ├── Documentacion_Tecnica_ACTUALIZADA.pdf
│   ├── Propuesta_Marinovic_ACTUALIZADA.pdf
│   └── Analisis_Economico_CAP3_VAN.pdf
└── README.md
```

---

## 🛠️ Requisitos

- Python 3.9+
- Streamlit
- Numpy / Pandas
- Plotly
- Scikit-learn

---

## ⚙️ Instalación

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecución

```bash
streamlit run app.py
```

---

## 📌 Uso (flujo típico)

1. Cargar dataset histórico (CSV o fuente equivalente).
2. Seleccionar enfriador y rango de fechas.
3. Revisar:
   - Métricas térmicas y tendencia
   - Fouling (dual robusto)
   - Criticidad y clasificación
   - Predicción / anomalías (ML)
4. Registrar/ajustar tubos aislados (si aplica) para recalcular automáticamente baseline y capacidad.

---

## ✅ Validación y calibración (recomendado)

### Validar eficiencia contra escenarios

| Escenario | Resultado esperado |
|---|---|
| Equipo limpio | ≈ 100% |
| Equipo sucio | < 100% |

### Validación de tubos aislados

| Condición | Resultado esperado |
|---|---|
| 0 tubos aislados | Baseline normal |
| N tubos aislados | Capacidad reducida coherente |
| Todos los tubos aislados | Alerta / condición inválida |

### Calibración con datos reales

- Comparar predicciones vs mediciones durante 1 mes.
- Ajustar sensibilidad por equipo si corresponde.
- Reentrenar modelos periódicamente con datos nuevos.

---

## 🧩 Roadmap (ideas futuras)

- [ ] Integración con SAP PM (OT automática)
- [ ] Alertas por email / SMS / Telegram
- [ ] Persistencia de estado de tubos aislados en BD
- [ ] Dashboard móvil / Edge computing

---

## 👤 Autor

**Sebastián Marinovic Leiva**
Chuquicamata – Codelco (Chile)

📧 Contacto: [sebamarinovic.leiva@gmail.com](mailto:sebamarinovic.leiva@gmail.com)
