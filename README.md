# ❄️ Sistema de Monitoreo Predictivo – Enfriadores de Ácido Sulfúrico CAP-3

> **Versión:** 4.0 (Con Gestión de Tubos Aislados)
> **Autor:** Sebastián Marinovic Leiva
> **División:** Chuquicamata – Codelco (Chile)
> **Fecha:** Octubre 2025 – Febrero 2026

Sistema de monitoreo predictivo para enfriadores de ácido sulfúrico en **CAP-3 (Planta de Ácido Sulfúrico, Chuquicamata – Codelco)**, basado en fundamentos de transferencia de calor, análisis de ensuciamiento (fouling), criticidad operativa y modelos de Machine Learning para apoyar decisiones de operación y mantención.

**Enfriadores monitoreados (CAP-3):**

- **Secado** – 632 tubos ZeCor-Z
- **Absorción Intermedia** – 883 tubos ZeCor-Z
- **Absorción Final** – 197 tubos ZeCor-Z

---

## 🚀 Objetivo

Detectar degradación térmica, ensuciamiento y condiciones anómalas en los enfriadores CAP-3, entregando:

- Indicadores térmicos (eficiencia y capacidad)
- Factor de fouling robusto (método dual v4.0)
- Índice de criticidad multifactorial (0–100)
- Predicciones y alertas con Machine Learning
- Gestión integral de tubos aislados ⭐
- Recomendaciones operacionales y de mantención priorizadas

---

## 📚 Antecedentes Teóricos

### 2.1 Ecuación fundamental de transferencia de calor

Los enfriadores de ácido sulfúrico en CAP-3 son intercambiadores de calor de carcasa y tubos (*shell & tube*), donde el ácido sulfúrico circula por el lado carcasa y el agua de enfriamiento por el lado tubos. La transferencia de calor se rige por:

```
Q = ṁ × Cp × ΔT = U × A × ΔTLM
```

Donde:

| Símbolo | Descripción | Unidades |
|---|---|---|
| **Q** | Calor transferido | kcal/h |
| **ṁ** | Flujo másico | kg/h |
| **Cp** | Calor específico | kcal/kg·°C |
| **ΔT** | Diferencia de temperatura | °C |
| **U** | Coeficiente global de transferencia | kcal/h·m²·°C |
| **A** | Área de transferencia | m² |
| **ΔTLM** | Diferencia de temperatura media logarítmica | °C |

### 2.2 Coeficiente global U

El coeficiente global depende de las resistencias térmicas en serie:

```
1/U = 1/h_i + 1/h_o + Rf_i + Rf_o + (e/k)
```

Donde `h_i` y `h_o` son los coeficientes de convección interno y externo, `Rf_i` y `Rf_o` las resistencias de ensuciamiento, `e` el espesor de pared del tubo y `k` la conductividad térmica del material (Perry, 2019; Hewitt, 2008).

### 2.3 Ensuciamiento (Fouling)

El ensuciamiento es la acumulación de depósitos no deseados sobre las superficies de transferencia que genera una resistencia térmica adicional (Müller-Steinhagen, 2000). El factor de ensuciamiento se define como:

```
Rf = (1/U_sucio) − (1/U_limpio)   [m²·K/W]
```

En enfriadores de ácido sulfúrico, las principales fuentes de fouling incluyen depósitos de sulfatos, corrosión del material de tubos y precipitación de sólidos disueltos.

**Rangos típicos de Rf:**

| Estado | Rf (m²·K/W) |
|---|---|
| Limpio | < 0.0001 |
| Moderado | 0.0001 – 0.0005 |
| Alto | 0.0005 – 0.001 |
| Crítico | > 0.001 |

Referencia de validación: **TEMA RCB-7.41** establece valores de referencia de Rf para agua de torre de enfriamiento en el rango detectado por el sistema (TEMA Standards, 10th Edition).

### 2.4 Eficiencia térmica (η)

La eficiencia térmica mide qué tan bien el enfriador cumple su función respecto al diseño:

```
η = (Q_actual / Q_design_ajustado) × 100  [%]
```

Donde `Q_actual = dT_acid × F_water` y `Q_design` se ajusta automáticamente por tubos aislados. La interpretación es:

| Eficiencia | Estado |
|---|---|
| > 100% | Equipo limpio, condiciones mejores que diseño |
| 85–100% | Operación normal |
| 70–85% | Ligera degradación |
| < 70% | Requiere limpieza |

**Factores que afectan la eficiencia:** ensuciamiento interno (lado ácido), ensuciamiento externo (lado agua), temperatura agua de enfriamiento (variabilidad estacional), flujo de agua (demanda variable) y tubos aislados (reduce área efectiva) ⭐.

### 2.5 Método Dual Robusto de Fouling (v4.0)

El sistema implementa un método que combina dos enfoques complementarios en 8 pasos (Müller-Steinhagen, 2000; Perry, 2019):

**Paso 1 – U aproximado:**
```
offset = 0.05 × ΔT_design
U_aprox = Q_actual / (ΔT_acid + offset)
```

**Paso 2 – Resistencia actual:**
```
R_actual = 1 / (U_aprox + 0.0001)
```

**Paso 3 – Resistencia limpia:**
```
U_limpio = Q_design / (ΔT_design + offset)
R_limpia = 1 / U_limpio
```

**Paso 4 – Fouling por método directo (U):**
```
F_U = (R_actual − R_limpia) × sensitivity
```

Donde `sensitivity` es un factor ajustable por tipo de enfriador: Secado = 1.2, Absorción Intermedia = 1.0, Absorción Final = 1.2.

**Paso 5 – Fouling por método indirecto (eficiencia):**
```
F_η = (η_baseline − η_actual) / 100 × 0.001
```

Donde `η_baseline` es el promedio de las primeras 720 horas (30 días).

**Paso 6 – Combinación ponderada:**
```
F_total = 0.7 × F_U + 0.3 × F_η
```

**Paso 7 – Suavizado:** Media móvil de 12 horas para reducir ruido.

**Paso 8 – Escala visible:**
```
F_display = F_suavizado × 10,000   [×10⁻⁴ m²·K/W]
```

**Resultado:** Valores en ×10⁻⁴ m²·K/W (rango típico 0–15).

| Fouling (×10⁻⁴ m²·K/W) | Estado | Acción |
|---|---|---|
| 0.00 – 2.00 | ✅ Limpio | Operación normal |
| 2.00 – 5.00 | Ligero | Monitoreo continuo |
| 5.00 – 10.00 | Moderado | Limpieza en 30–60 días |
| > 10.00 | Alto | Limpieza urgente |

**Ventajas del método dual:** (1) Robusto – no depende de una sola medición, (2) Sensible – detecta cambios graduales, (3) Adaptable – factor ajustable por equipo, (4) Filtrado – media móvil elimina falsos positivos.

### 2.6 Índice de criticidad

Score compuesto multifactorial (0–100) con pesos justificados:

```
Criticidad = 0.40 × f(T) + 0.30 × f(η) + 0.20 × f(conductividad) + 0.10 × f(fouling)
```

| Componente | Peso | Justificación |
|---|---|---|
| Temperatura | 40% | Factor más crítico (seguridad y calidad del producto) |
| Eficiencia | 30% | Indicador directo del desempeño |
| Conductividad | 20% | Indicador de calidad del agua (causa de fouling) |
| Fouling | 10% | Resultado de los demás factores |

**Clasificación:**

| Rango | Nivel | Acción |
|---|---|---|
| 0–30 | 🟢 Baja | Operación normal |
| 30–60 | 🟡 Media | Monitoreo intensificado |
| 60–80 | 🟠 Alta | Planificar mantenimiento |
| 80–100 | 🔴 Crítica | Acción inmediata |

### 2.7 Gestión de tubos aislados ⭐

Cuando se detectan tubos rotos o con fugas, se aíslan mecánicamente (se tapan). Esto reduce el área efectiva de transferencia y la capacidad del enfriador. **Hasta ahora, este impacto no se cuantificaba ni se ajustaban los cálculos.**

**Cálculo de área efectiva:**
```
A_tubo = π × D × L                          (D = 25.4 mm, L = 6.0 m)
A_efectiva = A_tubo × (N_total − N_aislados)
Factor_reducción = (N_total − N_aislados) / N_total
Q_design_ajustado = Q_design_base × Factor_reducción
Pérdida_capacidad = (1 − Factor_reducción) × 100  [%]
```

**Ejemplo práctico (Absorción Intermedia):**

| Condición | Sin ajuste | Con 100 tubos aislados |
|---|---|---|
| Tubos operativos | 883 (100%) | 783 (88.7%) |
| Q_design (kcal/h) | 31,073 | 27,562 |
| Eficiencia si Q_actual = 26,500 | 85.3% ⚠️ *parece baja* | **96.1%** ✅ *equipo OK* |

**Beneficio clave:** Diferencia correctamente entre ensuciamiento real y pérdida de área por tubos aislados, evitando falsos diagnósticos y decisiones erróneas de mantenimiento.

### 2.8 Machine Learning

**Random Forest Regressor** (Susto et al., 2015; Scikit-learn):

| Parámetro | Valor |
|---|---|
| Algoritmo | RandomForestRegressor |
| n_estimators | 100 |
| max_depth | 10 |
| Test split | 20% |
| RMSE típico | < 2 °C |
| R² típico | > 0.95 |

Features: `T_acid_in_C`, `F_water`, `cond_uS_cm`, `FLUJO_CAP3`, `%VELOCIDAD_SOPLADOR`
Target: `T_acid_out_C`

**Isolation Forest** para detección de anomalías (contamination = 5%): identifica temperaturas fuera de rango, combinaciones inusuales de parámetros y eventos súbitos no explicados.

**Predicción de días hasta mantenimiento:**
```
tendencia = (T_actual − T_30d_atrás) / 30   [°C/día]
días_hasta_límite = (T_máx − T_actual) / tendencia
```

| Días hasta límite | Clasificación |
|---|---|
| < 30 | 🔴 Crítico |
| 30–90 | 🟡 Alerta |
| > 90 | 🟢 Normal |

---

## ✨ Funcionalidades del Dashboard

El sistema se despliega como un dashboard interactivo en **Streamlit** con 7 módulos (tabs):

| Tab | Módulo | Descripción |
|---|---|---|
| 1 | ⭐ Config. Tubos Aislados | Formulario de ingreso, vista previa de impacto, tabla resumen y gráfico de barras apiladas |
| 2 | Análisis Térmico | Evolución de temperaturas, ΔT, eficiencia vs. diseño, detección de desviaciones |
| 3 | Ensuciamiento (Fouling) | Método dual robusto v4.0, tendencia temporal, clasificación por umbrales |
| 4 | Criticidad | Score multifactorial, mapa de calor, clasificación por niveles |
| 5 | Predicción ML | Random Forest + Isolation Forest, proyección de días hasta mantenimiento |
| 6 | Recomendaciones | Acciones priorizadas por nivel de criticidad y enfriador |
| 7 | Panel Resumen | Vista ejecutiva de los 3 enfriadores, gauge de criticidad, tabla comparativa con colores |

---

## 📊 Factibilidad Técnica

### Arquitectura (CAPEX = 0)

| Capa | Implementación |
|---|---|
| **Adquisición** | Extracción periódica desde PI System (API/connector) + validación de calidad |
| **Procesamiento** | Python (pandas/numpy) · feature engineering · cálculo fouling/ΔT · scoring |
| **Persistencia** | CSV/Parquet local + backup en nube (S3 o equivalente) |
| **Aplicación** | Streamlit (dashboard interactivo, 7 módulos) |
| **Alertas** | Reglas + umbrales + salida a correo/Telegram/Teams |

### Fuentes de datos

- **PI System (SCADA):** >100 tags de proceso e instrumentación.
- **Registros de lavados:** Histórico de lavados químicos/mecánicos (planificación + ejecución).
- **Datos de mantenimiento/condición:** demister, bombas, válvulas, etc.
- **Base de pérdidas operacionales:** Factorial de Pérdidas Fusión HF (vínculo CAP-3 → Fusión).

### Variables del modelo

**Variables base del dataset:**

| Variable | Descripción |
|---|---|
| `T_acid_in_C` / `T_acid_out_C` | Temperatura ácido entrada/salida (°C) |
| `T_water_in_C` / `T_water_out_C` | Temperatura agua entrada/salida (°C) |
| `F_water` | Caudal de agua de enfriamiento (m³/h) |
| `cond_uS_cm` | Conductividad del agua (µS/cm) |
| `dT_acid` | Delta de temperatura del ácido (°C) |
| `FLUJO_CAP3` | Flujo de proceso CAP-3 |
| `%VELOCIDAD_SOPLADOR` | Velocidad del soplador (%) |
| `CARGA_HORNO_FLASH` | Carga del horno Flash |
| `EQUIPOS_CPS_EN_SERVICIO` | Equipos CPS en servicio |
| `FLUJO_TORRE_ENFRIAMIENTO_4` | Flujo torre de enfriamiento N°4 |
| `FLUJO_AGUA_DESMIN_BHZ_305` | Flujo agua desmineralizada BHZ-305 |

**Variables derivadas (feature engineering):** ΔT por equipo, medias móviles (rolling 12h), tasas de cambio (dT/dt), indicadores de ensuciamiento, baseline de eficiencia (primeras 720h).

### Especificaciones de diseño por enfriador

| Parámetro | Secado | Abs. Intermedia | Abs. Final |
|---|---|---|---|
| T° entrada diseño (°C) | 75 | 77 | 71 |
| T° salida diseño (°C) | 65 | 66 | 63 |
| ΔT diseño (°C) | 10 | 11 | 8 |
| T° salida máxima (°C) | 70 | 72 | 68 |
| Caudal agua diseño (m³/h) | 900 | 990 | 960 |
| Q diseño base (kcal/h) | 13,232 | 31,073 | 7,188 |
| N° tubos totales | 632 | 883 | 197 |
| Material tubos | ZeCor-Z | ZeCor-Z | ZeCor-Z |
| Diámetro tubo (mm) | 25.4 | 25.4 | 25.4 |
| Longitud tubo (m) | 6.0 | 6.0 | 6.0 |
| Factor sensibilidad fouling | 1.2 | 1.0 | 1.2 |

### Volumen de datos

- Histórico sintético: 2 años (~17,500+ registros por enfriador, frecuencia horaria).
- Proyección operacional: ≥ 1,000,000 filas/año con datos reales de PI.

### Plan de implementación

| Fase | Alcance | Plazo | Equipo clave |
|---|---|---|---|
| **Fase 1:** Preparación | Recopilación datos, validación tags PI, definición umbrales | 2 semanas | Ing. Procesos + Esp. PI |
| **Fase 2:** Desarrollo | Implementación módulos, integración PI, testing interno | 4 semanas | Ing. Procesos |
| **Fase 3:** Piloto | Validación con operadores, ajuste parámetros, calibración ML | 4 semanas | Operadores + Mantención |
| **Fase 4:** Despliegue | Capacitación formal, documentación, go-live | 2 semanas | Todos |
| **Total** | | **12 semanas** | |

---

## 💰 Análisis Económico (Caso de Negocio)

### Problema cuantificado

La condición de alta temperatura del ácido / circuito de enfriamiento en CAP-3 se asocia directamente a pérdidas de disponibilidad que impactan la producción de Fusión (HF).

**Fuente:** Base "Factorial Pérdidas Fusión HF" (año 2025, filtro: Unidad=PAS, Falla contiene "Disponibilidad CAP III"):

| Indicador | Valor 2025 |
|---|---|
| Eventos registrados | 33 |
| Pérdidas de Fusión asociadas | 6,255.35 ton/año |
| Duración acumulada | 108.88 h |
| Tiempo detención acumulado | 179.10 h |

### Costos de la problemática actual

| Concepto | Impacto |
|---|---|
| Paro no programado (por evento) | US$ 50,000 – 80,000 |
| Paros anuales (3–4 eventos) | US$ 200,000 – 300,000 |
| Limpieza química (por evento) | US$ 15,000 – 25,000 |
| Retubing completo | US$ 150,000 – 200,000 |
| Horas mantención (400–500 HH/año) | US$ 50/HH promedio |

### Modelo de inversión

| Concepto | Monto (US$) |
|---|---|
| Desarrollo software (análisis, diseño, programación, testing) | 0 |
| Licencias software (open source) | 0 |
| Servidor (infraestructura existente) | 0 |
| Capacitación (operaciones + mantención) | 0 |
| Integración PI System + ajuste + soporte | 0 |
| **TOTAL INVERSIÓN (CAPEX)** | **0** |
| **OPEX anual (nube: almacenaje/respaldos)** | **1,000/año** |

### Escenarios de retorno

**Escenario conservador:**

| Concepto | Valor |
|---|---|
| Evitar 2 paros no programados | US$ 120,000/año |
| Optimizar 2 limpiezas químicas | US$ 30,000/año |
| Extensión vida útil tubos (+20%) | US$ 30,000/año |
| **Total beneficio anual** | **US$ 180,000/año** |
| **ROI primer año** | **∞ (CAPEX = 0)** |
| **Payback** | **Inmediato** |

**Escenario optimista:**

| Concepto | Valor |
|---|---|
| Evitar 3–4 paros no programados | US$ 240,000/año |
| Optimizar 3 limpiezas químicas | US$ 50,000/año |
| Extensión vida útil + reducción HH | US$ 50,000/año |
| **Total beneficio anual** | **US$ 340,000/año** |
| **ROI primer año** | **∞ (CAPEX = 0)** |
| **Payback** | **Inmediato** |

### Modelo de VAN (vinculado a producción Fusión)

Con escenario de mejora del **70%** sobre pérdidas atribuibles:

```
Toneladas evitadas/año = 6,255.35 × 0.70 = 4,378.74 ton/año
Beneficio neto anual  = (Ton evitadas × Valor_US$/ton) − US$ 1,000
VAN (5 años, 10%)     = Beneficio neto anual × 3.7908
```

| Valor US$/ton | Beneficio neto anual (US$) | VAN 5 años @10% (US$) |
|---|---|---|
| 25 | 108,468 | 411,181 |
| 50 | 217,937 | 826,153 |
| 75 | 327,406 | 1,241,124 |
| 100 | 436,874 | 1,656,096 |
| 150 | 655,811 | 2,486,040 |
| 200 | 874,748 | 3,315,983 |

**Punto de equilibrio:** Valor ≥ 0.228 US$/ton para cubrir OPEX. El payback es prácticamente inmediato para cualquier criterio económico realista.

> **Nota:** El VAN oficial se cerrará una vez que Control de Gestión defina el valor unitario (US$/ton de fusión no perdida) según criterio corporativo.

---

## 🧱 Arquitectura del repositorio

```
ENF_AC_DCH/
├── script.py                                        # Dashboard Streamlit (7 tabs, 740 líneas)
├── requirements.txt
├── data/
│   ├── acid_coolers_CAP3_synthetic_2years.csv        # Dataset principal ácido (3 enfriadores, 2 años)
│   └── t_water_in_out_CAP3_synthetic_2years.csv      # Dataset agua enfriamiento (sep=";", decimales ",")
├── docs/
│   ├── Documentacion_Tecnica_FINAL.pdf               # Doc. técnica v4.0 (12 págs, ecuaciones completas)
│   ├── Propuesta_Marinovic_FINAL.pdf                 # Propuesta + caso de negocio (11 págs)
│   └── Analisis_Economico_CAP3_VAN.pdf               # Análisis VAN con sensibilidad
└── README.md
```

---

## 🛠️ Requisitos

- Python 3.9+
- Streamlit
- Pandas / Numpy
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
streamlit run script.py
```

---

## 📌 Uso (flujo típico)

1. Cargar dataset histórico (los CSV se leen automáticamente desde el directorio local).
2. Seleccionar enfriador y rango de fechas en la barra lateral.
3. **Tab 1:** Configurar tubos aislados (si aplica) para recalcular baseline automáticamente.
4. **Tabs 2–5:** Revisar métricas térmicas, fouling, criticidad y predicciones ML.
5. **Tab 6:** Consultar recomendaciones priorizadas de operación/mantención.
6. **Tab 7:** Vista ejecutiva comparativa de los 3 enfriadores para decisión rápida.
7. Exportar datos filtrados en CSV desde Tab 6.

---

## ✅ Validación y calibración

### Eficiencia

| Test Case | Condición | Resultado esperado |
|---|---|---|
| 1 | Q_actual = Q_design | η = 100% ✅ |
| 2 | Q_actual = 80% Q_design | η = 80% ✅ |

### Fouling

| Test Case | Condición | Resultado esperado |
|---|---|---|
| 1 | Equipo limpio | Rf ≈ 0 ×10⁻⁴ ✅ |
| 2 | Equipo sucio | Rf > 5 ×10⁻⁴ ✅ |

### Tubos aislados ⭐

| Test Case | Condición | Resultado esperado |
|---|---|---|
| 1 | 0 tubos aislados | Factor = 1.0, Q_design = base ✅ |
| 2 | 50 tubos (Secado) | Factor = 0.921, Q_design = 12,189 kcal/h ✅ |
| 3 | Todos aislados | Factor = 0, sistema alerta error ✅ |

### Calibración con datos reales (recomendado)

- Comparar predicciones vs. mediciones reales durante 1 mes.
- Ajustar factores de sensibilidad por equipo si corresponde.
- Reentrenar modelos ML periódicamente con datos nuevos.
- Validar umbrales de criticidad con operadores en terreno.

---

## 🧩 Roadmap

| Fase | Plazo | Iniciativas |
|---|---|---|
| **Fase 2** | 6–12 meses | Integración SAP PM (OT automáticas), alertas email/SMS, dashboard móvil, reportes semanales automáticos |
| **Fase 3** | 12–24 meses | Deep Learning (LSTM series temporales), optimización multi-objetivo, gemelo digital, integración con torres y convertidores |
| **Fase 4** | 24+ meses | IA generativa para reportes, realidad aumentada para mantención, edge computing tiempo real, replicación divisional |

### Escalabilidad

El sistema es **100% replicable** a otros equipos con esfuerzo marginal (arquitectura ya desarrollada):

- Torres de Absorción
- Convertidores (monitoreo temperatura lecho catalítico)
- Secadores de Gas (control punto de rocío)
- Enfriadores de Aire (eficiencia compresores)

---

## 📖 Referencias bibliográficas

1. **Perry, R.H. & Green, D.W.** (2019). *Perry's Chemical Engineers' Handbook*, 9th Edition. McGraw-Hill.
2. **Hewitt, G.F., Shires, G.L. & Bott, T.R.** (2008). *Heat Exchanger Design Handbook*. Begell House.
3. **Müller-Steinhagen, H.** (2000). *Fouling of Heat Exchangers: Fundamentals and Mitigation*. Publico Publications.
4. **TEMA** (2019). *Standards of the Tubular Exchanger Manufacturers Association*, 10th Edition.
5. **Susto, G.A., Schirru, A., Pampuri, S., McLoone, S. & Beghi, A.** (2015). Machine Learning for Predictive Maintenance: A Multiple Classifier Approach. *IEEE Transactions on Industrial Informatics*, 11(3), 812–820.
6. **Bott, T.R.** (1995). *Fouling of Heat Exchangers*. Elsevier Science.
7. **Incropera, F.P., DeWitt, D.P., Bergman, T.L. & Lavine, A.S.** (2007). *Fundamentals of Heat and Mass Transfer*, 6th Edition. John Wiley & Sons.
8. **Pedregosa, F. et al.** (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.
9. **Breiman, L.** (2001). Random Forests. *Machine Learning*, 45(1), 5–32.
10. **Liu, F.T., Ting, K.M. & Zhou, Z.H.** (2008). Isolation Forest. *IEEE International Conference on Data Mining*, 413–422.
11. **Codelco** (2020). *Especificaciones Técnicas Enfriadores CAP-3*. Documentación interna, División Chuquicamata.
12. **Streamlit Documentation** – https://docs.streamlit.io

---

## 👤 Autor

**Sebastián Marinovic Leiva**
Ingeniero de Procesos
Superintendencia Planta de Ácido y Oxígeno
Gerencia de Fundición – División Chuquicamata, Codelco Chile

📧 [sebamarinovic.leiva@gmail.com](mailto:sebamarinovic.leiva@gmail.com)
📱 +56 9 7624 3605

---

> *"Primera implementación de monitoreo predictivo con gestión integral de tubos aislados en enfriadores de ácido sulfúrico CAP-3, División Chuquicamata."*
