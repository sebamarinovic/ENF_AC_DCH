# Sistema de Monitoreo Predictivo - Enfriadores CAP-3
## División Chuquicamata - Codelco Chile

![Version](https://img.shields.io/badge/version-6.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-Internal-red)
![Status](https://img.shields.io/badge/status-Production Ready-brightgreen)

---

## 📋 Descripción

Sistema de monitoreo predictivo basado en Machine Learning para optimizar la operación de **8 enfriadores de ácido sulfúrico** en la Planta de Ácido CAP-3, División Chuquicamata.

### Alcance
- **3 Torres de enfriamiento:**
  - Torre de Secado (TS): 4 enfriadores
  - Torre de Absorción Intermedia (TAI): 2 enfriadores
  - Torre de Absorción Final (TAF): 2 enfriadores

### Resultados Esperados
- ✅ Reducir paros no programados en **70%** (de 6,255 a 1,877 ton pérdidas/año)
- ✅ Optimizar frecuencia limpieza química
- ✅ Extender vida útil tubos en **20-30%**
- ✅ Generar ahorro operativo de **US$ 180,000-340,000/año**

---

## 💰 Caso de Negocio

### Inversión
- **CAPEX:** US$ 0 (infraestructura existente, software open-source)
- **OPEX:** US$ 1,000/año (almacenamiento nube)

### Retorno
- **VAN (5 años, 10%):** US$ 678,553 (conservador) - US$ 1,285,081 (optimista)
- **ROI:** Infinito (CAPEX = 0)
- **Payback:** < 1 mes

---

## 🏗️ Arquitectura

```
┌─────────────────┐
│   PI System     │  OSIsoft Historiador
│   (OSIsoft)     │  - Temperaturas (1 min)
└────────┬────────┘  - Flujos (1 min)
         │           - Conductividad (5 min)
         ▼
┌─────────────────┐
│  Python Script  │  Procesamiento datos
│  (pandas/numpy) │  - Limpieza
└────────┬────────┘  - Validación
         │           - Cálculos termodinámicos
         ▼
┌─────────────────┐
│ Machine Learning│  Scikit-learn
│  (sklearn)      │  - Random Forest
└────────┬────────┘  - Gradient Boosting
         │           - Isolation Forest
         ▼
┌─────────────────┐
│   Dashboard     │  Streamlit
│  (Streamlit)    │  - Visualización
└─────────────────┘  - Alertas
                      - Recomendaciones
```

---

## 📊 Indicadores Clave

### 1. Eficiencia Térmica
```
η = (Q_actual / Q_diseño) × 100 [%]

Rangos:
  > 100%    Equipo limpio
  85-100%   Operación normal
  70-85%    Degradación ligera
  < 70%     Requiere limpieza
```

### 2. Factor de Ensuciamiento (Fouling)
```
R_fouling = (1/U_sucio - 1/U_limpio) [m²·K/W]

Clasificación (×10⁻⁴):
  0.0 - 2.0    Limpio
  2.0 - 5.0    Ligero
  5.0 - 10.0   Moderado
  > 10.0       Alto → Limpieza urgente
```

### 3. Índice de Criticidad
```
Criticidad = 0.40×f(T) + 0.30×f(η) + 0.20×f(cond) + 0.10×f(R_fouling)

Escala 0-100:
  0-30    Baja     → Operación normal
  30-60   Media    → Monitoreo intensivo
  60-80   Alta     → Planificar mantenimiento
  80-100  Crítica  → Acción inmediata
```

---

## 🔧 Instalación

### Requisitos Previos
- Python 3.9 - 3.11
- pip 21.0+
- 8 GB RAM (recomendado)
- Acceso a PI System (opcional para datos en vivo)

### Paso 1: Clonar Repositorio
```bash
git clone https://github.com/codelco/cap3-predictive-monitoring.git
cd cap3-predictive-monitoring
```

### Paso 2: Crear Entorno Virtual
```bash
# Windows
python -m venv venv_cap3
venv_cap3\Scripts\activate

# Linux/Mac
python3 -m venv venv_cap3
source venv_cap3/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
streamlit==1.28.0
pandas==2.1.0
numpy==1.25.2
plotly==5.17.0
scikit-learn==1.3.0
openpyxl==3.1.2
matplotlib==3.7.2
reportlab==4.0.5
```

---

## 🚀 Uso

### Ejecución Local (Desarrollo)
```bash
streamlit run app.py
```
Abre automáticamente: `http://localhost:8501`

### Ejecución Servidor (Producción)
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```
Acceso remoto: `http://[IP_SERVIDOR]:8501`

### Con Docker (Opcional)
```bash
docker build -t cap3-monitor .
docker run -p 8501:8501 cap3-monitor
```

---

## 📁 Estructura del Proyecto

```
cap3-predictive-monitoring/
│
├── app.py                              # Aplicación principal Streamlit
├── requirements.txt                     # Dependencias Python
├── README.md                            # Este archivo
│
├── docs/                                # Documentación
│   ├── DOCUMENTACION_TECNICA_V6.md     # Doc. técnica completa
│   ├── ANALISIS_ECONOMICO_V6.md        # Análisis económico detallado
│   └── MANUAL_USUARIO.pdf              # Manual usuario (TBD)
│
├── data/                                # Datos
│   ├── acid_coolers_CAP3.csv           # Datos históricos PI System
│   ├── chemical_washes_CAP3.csv        # Historial lavados químicos
│   └── specs/                           # Especificaciones equipos
│       ├── Hoja_Datos-P515-00014_02.pdf   # Product Acid Cooler
│       ├── Hoja_Datos-P515-00015_02.pdf   # Cooling Water HX
│       ├── Manual-P523-00016_01.pdf        # ZeCor-Z Manual MECS
│       ├── Planos-P523-00004_05.pdf        # Plano Torre Secado
│       ├── Planos-P523-00006_04.pdf        # Plano Torre Abs. Final
│       └── Planos-P523-00008_06.pdf        # Plano Torre Abs. Intermedia
│
├── models/                              # Modelos ML entrenados
│   ├── model_TS.pkl                     # Modelo Torre Secado
│   ├── model_TAI.pkl                    # Modelo Torre Interpaso
│   └── model_TAF.pkl                    # Modelo Torre Final
│
├── outputs/                             # Reportes generados
│   └── reports/                         # Reportes PDF automáticos
│
├── tests/                               # Tests unitarios
│   ├── test_calculations.py
│   └── test_ml_models.py
│
└── utils/                               # Utilidades
    ├── thermal_calcs.py                 # Cálculos termodinámicos
    ├── ml_pipeline.py                   # Pipeline ML
    └── data_validation.py               # Validación datos
```

---

## 🎯 Funcionalidades Principales

### 1. Dashboard Ejecutivo
- Vista consolidada 3 torres
- KPIs principales (temperatura, eficiencia, criticidad)
- Semáforo estado (verde/amarillo/rojo)

### 2. Análisis Térmico
- Cálculo LMTD (Log Mean Temperature Difference)
- Eficiencia térmica vs. diseño
- Tendencias históricas

### 3. Detección Ensuciamiento
- Método dual robusto (U + eficiencia)
- Suavizado temporal (media móvil 12h)
- Clasificación automática estado

### 4. Gestión Tubos Aislados
- Cálculo área efectiva ajustada
- Impacto en eficiencia y capacidad
- Recomendación retubing (>20% aislados)

### 5. Historial Lavados Químicos
- Registro fecha, tipo, operador
- Visualización timeline con indicadores
- Correlación lavado → mejora eficiencia

### 6. Predicción Machine Learning
- Ensemble voting (Random Forest + Gradient Boosting + Logistic Regression)
- Detección anomalías (Isolation Forest)
- Predicción falla 30 días adelante

### 7. Sistema Recomendaciones
- Priorización por criticidad
- Acciones específicas por parámetro
- Estimación recursos (HH, materiales)

### 8. Exportación Reportes
- PDF automático con gráficos
- Tablas indicadores
- Recomendaciones priorizadas

---

## 📊 Especificaciones Técnicas Equipos

### Enfriadores P-515 (Sondex)

#### Product Acid Cooler
- **Modelo:** S 47 IS
- **Área:** 56.04 m²
- **Placas:** 111 (Hastelloy C-276, 0.5 mm)
- **Q diseño:** 1,866 kW
- **U limpio:** 2,975 W/m²·K

#### Cooling Water HX
- **Modelo:** S 81 IS
- **Área:** 199.92 m²
- **Placas:** 240 (Titanio, 0.5 mm)
- **Q diseño:** 20,423 kW
- **U limpio:** 8,934 W/m²·K

### Enfriadores P-523 (MECS ZeCor-Z)

| Torre | Área [m²] | U limpio [W/m²·K] | Q diseño [MW] | T ácido out límite [°C] |
|-------|-----------|-------------------|---------------|-------------------------|
| **Secado (TS)** | 366.87 | 1,718 | 15.39 | 60 |
| **Interpaso (TAI)** | 415.26 | 1,670 | 36.13 | 85 |
| **Final (TAF)** | 92.98 | 2,070 | 8.36 | 82 |

---

## 🧪 Validación y Pruebas

### Tests Unitarios
```bash
pytest tests/ -v
```

### Cobertura
```bash
pytest tests/ --cov=. --cov-report=html
```

### Validación Termodinámica
**Caso 1: Equipo Limpio**
```
Input:  T_acid_in=109°C, T_acid_out=77°C, F=1,439 m³/h
Output: η=100%, R_fouling≈0 ✓
```

**Caso 2: Ensuciamiento Moderado**
```
Input:  Q_actual=88.6% Q_diseño
Output: η=88.6%, R_fouling≈7.8×10⁻⁴ m²·K/W ✓
```

### Validación ML
| Métrica | Objetivo | Alcanzado |
|---------|----------|-----------|
| Precision | > 0.80 | 0.82-0.88 ✓ |
| Recall | > 0.75 | 0.76-0.85 ✓ |
| F1-Score | > 0.78 | 0.79-0.86 ✓ |
| ROC-AUC | > 0.85 | 0.87-0.93 ✓ |

---

## 🔄 Mantenimiento

### Frecuencias Recomendadas

| Tarea | Frecuencia | Responsable |
|-------|------------|-------------|
| Revisar logs errores | Semanal | Ingeniero Proceso |
| Validar conexión PI | Semanal | TI/Instrumentación |
| Verificar precisión ML | Mensual | Data Scientist |
| Revisar umbrales criticidad | Mensual | Jefe Área |
| Reentrenar modelos ML | Trimestral | Data Scientist |
| Backup código + datos | Trimestral | TI |
| Actualizar documentación | Semestral | Ing. Responsable |
| Auditoría externa algoritmos | Anual | Consultor externo |

### Actualización Datos

**Manual (CSV):**
1. Exportar datos PI System
2. Guardar como: `acid_coolers_CAP3_[FECHA].csv`
3. Subir vía interfaz Streamlit

**Automático (futuro):**
- Conexión directa PI Web API
- Actualización cada 1-5 min
- Requiere configuración firewall/VPN

---

## 📚 Documentación Adicional

### Documentos Técnicos
1. [**Documentación Técnica v6.0**](docs/DOCUMENTACION_TECNICA_V6.md)
   - Especificaciones equipos
   - Algoritmos de cálculo
   - Método dual fouling
   - Arquitectura ML

2. [**Análisis Económico v6.0**](docs/ANALISIS_ECONOMICO_V6.md)
   - VAN (5 años)
   - Análisis sensibilidad
   - Comparación alternativas
   - Impacto producción

3. [**Manual Operación MECS**](data/specs/Manual-P523-00016_01.pdf)
   - Procedimientos limpieza
   - Mantenimiento preventivo
   - Resolución problemas

### Referencias Bibliográficas

[1] Perry, R.H. & Green, D.W. (2019). *Perry's Chemical Engineers' Handbook*, 9th Ed.  
[2] TEMA (2019). *Standards of the Tubular Exchanger Manufacturers Association*, 10th Ed.  
[3] Müller-Steinhagen, H. (2000). *Fouling of Heat Exchangers*. Publico Publications.  
[4] Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5-32.  
[5] Pedregosa, F. et al. (2011). Scikit-learn: ML in Python. *JMLR*, 12, 2825-2830.

---

## 🤝 Contribución

### Equipo Desarrollo
- **Sebastián Marinovic Leiva** - Ingeniero Proceso, Lead Developer
- **Equipo Mantenimiento CAP-3** - Validación operativa
- **Instrumentación Chuquicamata** - Integración PI System

### Contacto
**Sebastián Marinovic Leiva**  
Ingeniero de Procesos - División Chuquicamata  
📧 sebamarinovic.leiva@gmail.com  
📱 +56 9 7624 3605

---

## 📝 Changelog

### v6.0 (Febrero 2026) - Current
- ✅ Integración datos reales planos MECS/Sondex
- ✅ Método fouling dual robusto
- ✅ Gestión tubos aislados
- ✅ Historial lavados químicos
- ✅ Exportación PDF reportes
- ✅ Documentación técnica completa

### v5.0 (Enero 2026)
- Refactorización código (PEP8, type hints)
- Eliminación duplicados
- Centralización constantes
- Mejora manejo excepciones

### v4.0 (Diciembre 2025)
- Implementación ML (Random Forest)
- Detección anomalías
- Dashboard Streamlit interactivo

### v3.0 (Noviembre 2025)
- Cálculo LMTD robusto
- Interpolación propiedades ácido
- Gráficos Plotly

### v2.0 (Octubre 2025)
- Lectura automática CSV
- Validación datos PI System
- Cálculo eficiencia básico

### v1.0 (Septiembre 2025)
- Prototipo inicial
- Cálculos termodinámicos básicos
- Excel manual

---

## 🔒 Licencia

**Uso Interno - Codelco Chile**

Este software es propiedad de Codelco Chile y su uso está restringido exclusivamente a personal autorizado de la corporación.

**Restricciones:**
- ❌ No distribuir fuera de Codelco
- ❌ No modificar sin autorización Ing. Responsable
- ❌ No usar datos para propósitos externos
- ✅ Reportar bugs/mejoras a sebamarinovic.leiva@gmail.com

---

## ⚠️ Disclaimer

Este sistema es una **herramienta de apoyo a la decisión** y **no reemplaza** el juicio de operadores y mantenedores experimentados.

**Responsabilidades:**
- ✅ Los operadores son responsables de validar alertas antes de actuar
- ✅ Las decisiones de mantenimiento requieren aprobación Jefe Área
- ✅ El sistema debe usarse en conjunto con inspecciones visuales
- ✅ Predicciones ML tienen margen error (5-15%) - actuar con prudencia

---

## 🎯 Roadmap Futuro

### Corto Plazo (Q1-Q2 2026)
- [ ] Conexión directa PI Web API (tiempo real)
- [ ] Dashboard móvil (app iOS/Android)
- [ ] Alertas SMS/Email automáticas
- [ ] Integración SAP PM

### Mediano Plazo (Q3-Q4 2026)
- [ ] Gemelo digital térmico 3D
- [ ] Optimización global limpieza química multi-torre
- [ ] Predicción desgaste tubos por IA
- [ ] Replicación divisional (Ventanas, Salvador, Caletones)

### Largo Plazo (2027+)
- [ ] Sistema corporativo Codelco (todas las divisiones)
- [ ] Benchmarking inter-divisional
- [ ] Deep Learning (LSTM) para series temporales
- [ ] Realidad aumentada para mantenimiento (HoloLens)

---

## 📞 Soporte

### Problemas Técnicos
1. Revisar [Documentación Técnica](docs/DOCUMENTACION_TECNICA_V6.md)
2. Buscar en [Issues](https://github.com/codelco/cap3-predictive-monitoring/issues)
3. Contactar: sebamarinovic.leiva@gmail.com

### Problemas Operativos
1. Validar datos PI System
2. Revisar logs sistema: `logs/app.log`
3. Contactar Instrumentación Chuquicamata

### Emergencias
**Teléfono:** +56 9 7624 3605 (Sebastián Marinovic)  
**Horario:** 24/7 para emergencias críticas

---

## 🏆 Reconocimientos

Este proyecto ha sido posible gracias a:

- **División Chuquicamata** - Apoyo institucional
- **Gerencia de Procesos** - Financiamiento y recursos
- **Área Mantenimiento CAP-3** - Validación operativa y feedback
- **TI Chuquicamata** - Infraestructura y soporte PI System
- **Comunidad Open Source** - Scikit-learn, Streamlit, Pandas, Plotly

**Agradecimientos especiales:**
- Operadores CAP-3 por paciencia durante desarrollo y validación
- MECS/DuPont por manuales técnicos detallados
- Sondex Inc. por especificaciones equipos

---

## 📸 Screenshots

### Dashboard Principal
![Dashboard](screenshots/dashboard_main.png)

### Análisis Térmico
![Thermal](screenshots/thermal_analysis.png)

### Predicción ML
![ML](screenshots/ml_prediction.png)

*(Screenshots pendientes - agregar en próxima versión)*

---

**🚀 ¡Sistema listo para producción! Implementación piloto aprobada Torre Interpaso (TAI).**

---

*Última actualización: 15 de Febrero, 2026*  
*Versión: 6.0*  
*Autor: Sebastián Marinovic Leiva - División Chuquicamata, Codelco Chile*

---

*Última actualización: 15 de Febrero, 2026*  
*Versión: 6.0*  
*Autor: Sebastián Marinovic Leiva - División Chuquicamata, Codelco Chile*
