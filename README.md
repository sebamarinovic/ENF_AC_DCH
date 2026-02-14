
Readme · MD
Copiar

# Sistema de Monitoreo Predictivo – Enfriadores de Ácido Sulfúrico CAP-3

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

## 🧱 Arquitectura del repositorio

```
CAP3_Coolers_Monitor/
├── app.py
├── requirements.txt
├── data/
│   ├── acid_coolers_CAP3_synthetic_2years.csv
│   └── chemical_washes_CAP3.csv
├── docs/
│   ├── Documentacion_Tecnica_CAP3.pdf
│   ├── Manual_Usuario.pdf
│   └── Analisis_Economico_VAN.pdf
└── README.md
```

---

## 🛠️ Requisitos

- Python 3.9+
- Streamlit
- Numpy / Pandas
- Plotly / Matplotlib (si aplica)
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

## 🧩 Roadmap (ideas)

- [ ] Integración con SAP PM (OT automática)
- [ ] Alertas por email / SMS / Telegram
- [ ] Persistencia de estado de tubos aislados en BD
- [ ] Dashboard móvil / Edge computing

---

## 👤 Autor

**Sebastián Marinovic Leiva**
Chuquicamata – Codelco (Chile)

📧 Contacto: [sebamarinovic.leiva@gmail.com](mailto:sebamarinovic.leiva@gmail.com)
