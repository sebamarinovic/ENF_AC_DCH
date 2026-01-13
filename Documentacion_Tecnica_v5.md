# DOCUMENTACIÓN TÉCNICA
## Sistema de Monitoreo Predictivo para Enfriadores de Ácido Sulfúrico CAP-3
**Versión 5.0 – Refactorización con ML y Reportes Automáticos**

Autor: Sebastín Marinovic Leiva – División Chuquicamata, Codelco Chile  
Fecha: Enero 2026

---

## 1. Introducción

Este documento describe los fundamentos teóricos, las ecuaciones implementadas y la arquitectura de código del sistema de monitoreo predictivo para los enfriadores de ácido sulfúrico de CAP-3 (Secado, Absorción Intermedia y Absorción Final). El objetivo es facilitar el mantenimiento, la validación y la escalabilidad de la versión 5.0 del dashboard desarrollado en Streamlit.

### 1.1 Objetivos del documento

- Explicar los cálculos de eficiencia térmica, coeficiente global $U$ y factor de ensuciamiento $Rf$ usados en el sistema.
- Documentar el índice de criticidad 0–100 y el nuevo score operacional 0–1.
- Describir el módulo de Machine Learning para predicción de lavados en 30 días.
- Detallar el flujo de datos y la arquitectura modular de `app.py`.
- Documentar el generador de reportes PDF y el manejo de historial de lavados.

### 1.2 Alcance

El sistema se aplica a 3 enfriadores de ácido sulfúrico en CAP-3:

- **TS** – Torre de Secado 5322‑ENF‑301401 (366.87 m², 632 tubos, $U_{\text{limpio}} \approx 1718$ W/m²K).
- **TAI** – Torre Interpaso 5325‑ENF‑301401 (415.26 m², 883 tubos, $U_{\text{limpio}} \approx 1670$ W/m²K).
- **TAF** – Torre Final 5326‑ENF‑301401 (92.98 m², 197 tubos, $U_{\text{limpio}} \approx 2070$ W/m²K).

---

## 2. Fundamentos de transferencia de calor

### 2.1 Ecuaciones básicas

El calor transferido en un intercambiador de carcasa y tubos se modela como:

**Calor en el lado agua:**

$$Q_{\text{water}} = \dot{m}_{w} \, c_{p,w} (T_{w,\text{out}} - T_{w,\text{in}})$$

donde $\dot{m}_{w}$ es el flujo másico de agua y $c_{p,w}$ su calor específico.

**Calor en el lado ácido (modelo inverso):**

$$Q_{\text{acid}} = \dot{m}_{a} \, c_{p,a} (T_{a,\text{in}} - T_{a,\text{out}})$$

donde $c_{p,a}$ y la densidad del ácido se obtienen por interpolación en una tabla de propiedades en función de la concentración.

En el código se calcula $Q_{\text{water}}$ a partir del flujo de agua ($F_w$, m³/h) y la diferencia de temperatura de agua, y se estima la masa de ácido y sus propiedades con la función `getacidproperties`.

### 2.2 LMTD y coeficiente global U

La diferencia de temperatura media logarítmica se calcula de forma robusta mediante:

$$\Delta T_{\text{lm}} = \frac{\Delta T_1 - \Delta T_2}{\ln\left(\frac{\Delta T_1}{\Delta T_2}\right)}$$

donde $\Delta T_1 = T_{\text{hot,in}} - T_{\text{cold,out}}$ y $\Delta T_2 = T_{\text{hot,out}} - T_{\text{cold,in}}$, con manejo explícito de casos degenerados (cambios de signo, divisiones por cero) en la función `safelmtd`.

El coeficiente global $U$ se obtiene de:

$$Q_{\text{used}} = U A \Delta T_{\text{lm}}$$

$$U = \frac{Q_{\text{used}}}{A \, \Delta T_{\text{lm}}}$$

donde $A$ es el área de transferencia de calor, definida en `DESIGNPARAMS` para cada enfriador, y $Q_{\text{used}}$ es el mínimo entre el calor calculado por agua y por ácido.

---

## 3. Modelo térmico y eficiencia

### 3.1 Flujo másico y calor transferido

En `applythermalmodel`, el flujo volumétrico de agua se convierte a flujo másico con densidad 1000 kg/m³ (agua de enfriamiento):

- $\dot{m}_{w} = F_w \times \rho_w / 3600$
- $Q_{\text{water}} = \dot{m}_{w} \, c_{p,w} (T_{w,\text{out}} - T_{w,\text{in}})$

El modelo calcula:

- $\Delta T_{a} = T_{\text{acid,in}} - T_{\text{acid,out}}$
- Propiedades del ácido ($c_{p,a}$, $\rho_a$) vía `getacidproperties`.

Luego estima masa de ácido y $Q_{\text{acid}}$ y define:

$$Q_{\text{used}} = \min(|Q_{\text{water}}|, |Q_{\text{acid}}|)$$

de modo que se acota por el lado que entregue menor valor, evitando sobreestimaciones.

### 3.2 Eficiencia térmica

La eficiencia térmica respecto al diseño se calcula como:

$$\text{Eficiencia}_Q(\%) = \frac{Q_{\text{used}}}{Q_{\text{design}}} \times 100$$

$$\text{Eficiencia}_U(\%) = \frac{U}{U_{\text{limpio}}} \times 100$$

donde $Q_{\text{design}}$ y $U_{\text{limpio}}$ provienen de `DESIGNPARAMS` para TS, TAI y TAF.

En el código, estas métricas se almacenan en las columnas `effQpct` y `effUpct` en el DataFrame procesado.

---

## 4. Factor de ensuciamiento (Fouling)

### 4.1 Definición y unidades

El fouling se representa como una resistencia térmica adicional $R_f$, con unidades usuarias m²K/W. En la implementación, se escala a $R_f \times 10^4$ para visualizar valores típicos en rango 0–15.

### 4.2 Cálculo a partir de U

En `applythermalmodel`, el factor de ensuciamiento se calcula como:

$$R_{f} = \left(\frac{1}{U} - \frac{1}{U_{\text{limpio}}}\right)$$

y luego se almacena como `Rfx1e4 = R_f \times 10^4`, con clipping inferior para evitar valores negativos excesivos.

El `foulingdesignm2KW` de diseño se fija en 1.43e‑4 m²K/W para agua de torre, consistente con TEMA, y se utiliza como referencia.

### 4.3 Ensuciamiento crítico y umbrales

- Fouling de diseño: $R_{f,\text{design}} = 1.43 \times 10^{-4}$ m²K/W (escala 10 → 1.43).
- En `getfoulinginterpretation` se evalúan:
  - Si $Rf_{P95} \ge 5\,R_{f,\text{design}}$ → ensuciamiento crítico (limpieza prioritaria).
  - Si $Rf_{P95} \ge 3\,R_{f,\text{design}}$ → ensuciamiento alto (programar limpieza).

Se emplea un método dual robusto v4–v5: uso directo de $U$ y pérdida de eficiencia, combinado con suavizado temporal (media móvil) y escala visible.

---

## 5. Índice de criticidad 0–100

### 5.1 Componentes y pesos

La función `calculatecriticidad` genera un índice 0–100 que integra cuatro componentes normalizados:

1. **Temperatura de salida** ($T_{a,\text{out}}$ vs límite):
   - Componente `crittemp`: penaliza cuando $T_{a,\text{out}}$ se acerca o supera el límite `Tacidoutlimit`.
   - Peso: 30% en el índice total.

2. **Fouling** ($Rf$ vs valor crítico):
   - Componente `critfouling`: compara `Rfx1e4` con $R_{f,\text{crit}} = 5 \times R_{f,\text{design}}$.
   - Peso: 35%.

3. **Eficiencia térmica** ($U$ vs diseño):
   - Componente `criteff`: penaliza eficiencia baja (por debajo de cierta fracción de $U_{\text{limpio}}$).
   - Peso: 25%.

4. **Días desde lavado**:
   - Componente `critwash`: normaliza `dayssincewash` respecto a 180 días.
   - Peso: 10%.

El índice se forma como:

$$\text{criticidad} = 100 \left(0.30\, \text{crittemp} + 0.35\, \text{critfouling} + 0.25\, \text{criteff} + 0.10\, \text{critwash}\right)$$

con clipping a 0–120 y posterior acotamiento para usos gráficos.

### 5.2 Clasificación cualitativa

La criticidad se clasifica mediante:

- $0 \le v < 30$: **Baja**
- $30 \le v < 60$: **Media**
- $60 \le v < 80$: **Alta**
- $v \ge 80$: **Crítica**

La función `clasificar` asigna etiquetas y el dashboard muestra esta clasificación como texto y color (verde/amarillo/naranja/rojo).

---

## 6. Score operacional 0–1 y lógica de lavado

### 6.1 Score operacional

La función `operationalscore` genera un score 0–1 combinando:

- `temps`: severidad de $T_{out,P95}$ respecto a límite (`Tacidoutlimit`).
- `fouls`: severidad de $Rf_{P95}$ entre 1.2× y 5× $R_{f,\text{design}}$.
- `crits`: promedio de criticidad.
- `trends`: días estimados hasta fouling crítico (de `rftrendtocritical`).

Se pondera como:

$$\text{score} = \text{clip}\big(0.35\,\text{temps} + 0.35\,\text{fouls} + 0.20\,\text{crits} + 0.10\,\text{trends}, 0, 1\big)$$

Con el score cercano a 1 indicando condición desfavorable (riesgo alto).

La función retorna además notas descriptivas (T_P95 vs límite, Rf_P95 vs crítico, criticidad media, días a crítico).

### 6.2 Gatillos "requiere lavado"

La función `requireswash` decide si un enfriador requiere lavado inmediato con base en gatillos discretos:

- $T_{out,P95} > T_{\text{límite}}$ → "P95 T excede límite".
- $Rf_{P95} \ge R_{f,\text{crítico}}$ → "P95 Rf crítico".
- Tendencia de Rf (proyección) < 14 días para alcanzar $R_{f,\text{crítico}}$.
- Criticidad media ≥ 80.

Si alguno se cumple, `requireswash` devuelve `True` y un texto concatenado con los motivos.

---

## 7. Machine Learning – Predicción de lavados en 30 días

### 7.1 Etiquetado de eventos

La función `buildeventlabel` construye la variable objetivo $y$:

- Para cada timestamp $t$ en datos de operación (`dfop`), se busca si existe un lavado registrado en la tabla de lavados en la ventana $[t, t + \text{horizonte}]$.
- Si hay un lavado en ese horizonte (por defecto 30 días, `PREDHORIZONDAYS`), se asigna etiqueta $y = 1$; si no, $y = 0$.

Esto permite entrenar un clasificador binario que responda a "¿Habrá un lavado en los próximos 30 días?".

### 7.2 Features utilizadas

La función `addrollingfeatures` calcula features rolling en ventanas de n horas (mínimo 24 h), incluyendo:

- `Toutma`: media móvil de $T_{a,\text{out}}$.
- `Toutp957d`: percentil 95 móvil de $T_{a,\text{out}}$.
- `Rfma`: media móvil de $Rf$.
- `Rfslope`: pendiente de $Rf$ (tendencia).
- `Rfdaystocritest`: días estimados hasta $Rf$ crítico.
- `Uma`: media móvil de $U$.

La función `getmlfeatures` selecciona además:

- `QusedW`, `LMTDK`, `dTacid`, `Fw`, `effUpct`, `Rfx1e4`, `Taout`, `dayssincewash` si están presentes.

### 7.3 Entrenamiento y modelos

La función `trainmodels`:

1. Verifica condiciones mínimas para entrenar (`cantrain`):
   - Mínimo 300 filas (`MINTRAINROWS`).
   - Al menos 10 positivos y 10 negativos.

2. Divide datos en entrenamiento y test con `train_test_split`, manteniendo estratificación.

3. Entrena tres modelos:

   - **Modelo 1**: Logistic Regression con `RobustScaler` y `class_weight=balanced`.
   - **Modelo 2**: GradientBoostingClassifier (220 árboles, max_depth=3).
   - **Modelo 3**: RandomForestClassifier (500 árboles, max_depth=10, `min_samples_leaf=8`, balance de clases).

4. Evalúa PR-AUC y ROC-AUC en el set de test y selecciona el mejor según PR-AUC (importante en datasets desbalanceados).

5. Almacena el mejor modelo y scaler (si aplica) en `pack['best']`, junto a un DataFrame de resultados por modelo.

### 7.4 Predicción en línea

En Tab ML:

- Se construye `dfml` con datos en operación, features rolling y etiqueta $y$.
- Si el modelo es entrenable, se calcula la probabilidad $p_{\text{ML}}$ para la última fila válida (`lastrow`).
- Se muestra tabla con métricas de cada modelo (PR-AUC, ROC-AUC) y se despliega un indicador tipo gauge con probabilidad combinada.

La probabilidad final se combina como:

$$p_{\text{final}} = 0.6 \, p_{\text{ML}} + 0.4 \, \text{score}_{\text{operacional}}$$

y se clasifica cualitativamente:

- $p_{\text{final}} < 0.3$: "No requiere lavado".
- $0.3 \le p_{\text{final}} < 0.7$: "Zona intermedia".
- $p_{\text{final}} \ge 0.7$: "Requiere lavado".

La función `modelimportance` calcula la importancia de variables (feature importance o $|\text{coef}|$) y muestra un gráfico de barras horizontal con las más relevantes.

---

## 8. Flujo de datos y arquitectura de código

### 8.1 Flujo de datos principal

1. **Carga de datos crudos**
   - Usando `readcsvautopath` sobre archivos de datos (`DATAFILE`) y lavados (`WASHFILE`).
   - Múltiples encodings y separadores, detección automática de timestamp.

2. **Transformación wide → long**
   - `explodewidetolong`: genera un DataFrame largo con columnas estandarizadas (`Tain`, `Taout`, `Twin`, `Twout`, `Fw`, `acidconc`, `bypass`, `pumpamp`, `condw`, `blowerspeed`).

3. **Filtrado de operación**
   - `filteroperation`: aplica ventanas operacionales por equipo (rangos de temperatura, flujo de agua mínimo, velocidad mínima de soplador).

4. **Modelo térmico + fouling + criticidad**
   - `applythermalmodel` → Q, LMTD, U, Rf, eficiencias.
   - `addwashfeatures` → días desde lavado.
   - `calculatecriticidad` → índice 0–100 y nivel cualitativo.
   - `addrollingfeatures` → features rolling para ML.

5. **Ventana de análisis**
   - `getwindowstart` y `computeglobalwindow` calculan inicio de ventana (p.ej. desde último lavado o fallback de 30 días).

6. **Interpretaciones y gráficos**
   - `getthermalinterpretation`, `getfoulinginterpretation`, `getcriticidadinterpretation`.
   - `createthermalchart`, `createfoulingchart`, `createcriticidadchart`.

7. **ML y score operacional**
   - `buildeventlabel`, `getmlfeatures`, `prepmldata`, `trainmodels`, `predictprob`.
   - `operationalscore`, `requireswash`.

8. **Generación de PDF**
   - `generatepdf` produce reporte con resumen ejecutivo, KPIs, gráficos comparativos y recomendaciones.

### 8.2 Estructura de módulos (dentro de `app.py`)

- **Configuración**
  - `AppConfig`: parámetros globales (título, archivos, horizontes, mínimos ML).
  - `DESIGNPARAMS`, `ENGINEERINGMAP`, `ACIDPROPS`, `WASHNAMEMAP`.

- **Utilidades**
  - `fmtvalue`, `tonumeric`, `findtimestampcol`.

- **I/O y lavados**
  - `readcsvautopath`, `loadwashes`, `savewash`.

- **Procesamiento principal**
  - `explodewidetolong`, `filteroperation`, `applythermalmodel`, `addwashfeatures`, `calculatecriticidad`, `addrollingfeatures`.

- **Interpretación y scoring**
  - `windowstats`, `getthermalinterpretation`, `getfoulinginterpretation`, `getcriticidadinterpretation`.
  - `rftrendtocritical`, `operationalscore`, `requireswash`.

- **Machine Learning**
  - `buildeventlabel`, `getmlfeatures`, `prepmldata`, `cantrain`, `trainmodels`, `predictprob`, `modelimportance`.

- **Visualización y reportes**
  - `addwashlines`, `createthermalchart`, `createfoulingchart`, `createcriticidadchart`.
  - `generatepdf` y helpers internos (estilos ReportLab, KPIs, tablas).

---

## 9. Validación y calibración

### 9.1 Validación de eficiencia térmica

- **Caso limpio**: Datos de referencia con equipo recién lavado y condiciones cercanas a diseño; se espera $\text{Eficiencia}_Q \approx 95–105\%$.
- **Caso sucio**: Datos previos a limpieza; se espera eficiencia reducida y $Rf$ cercano a umbral crítico.

Se comparan valores promedio de Q y U con especificaciones de diseño (`QdesignW` y `UcleanWm2K`).

### 9.2 Validación de fouling

- Comparación con valores de fouling según TEMA para agua de torre (RCB‑7.41).
- Verificación de que equipos limpios muestran $Rf \approx R_{f,\text{design}}$ y que equipos sucios alcanzan valores 3–5 veces el diseño.

### 9.3 Validación de criticidad y score operacional

- Se revisan eventos históricos de incremento de temperatura y fouling y se comprueba que el índice aumenta (>60, >80) en momentos coherentes.
- Se calibra el peso de componentes para que criticidad alta coincida con condiciones que operadores consideran peligrosas.

### 9.4 Validación de ML

- División entrenamiento/test controlada, cálculo de PR-AUC y ROC-AUC.
- Comparación de predicciones de "lavado en 30 días" vs lavados reales históricos durante al menos 1 mes adicional.
- Ajuste de umbral de decisión (p_final ≈ 0.7) para balancear falsos positivos y falsos negativos.

---

## 10. Mantenimiento y mejoras futuras

### 10.1 Mantenimiento preventivo

- Revisar logs y excepciones en la app (errores de lectura, NaNs).
- Validar conexión con PI System y rutas de archivos CSV.
- Actualizar datos históricos para reentrenar ML cada 6–12 meses.
- Revisar umbrales de criticidad con operadores (workshops periódicos).
- Ajustar `DESIGNPARAMS` si cambian especificaciones de enfriadores.

### 10.2 Mejoras futuras (roadmap técnico)

- Persistencia completa de lavados y tubos aislados en base de datos (no solo CSV).
- Integración con SAP PM para generación automática de órdenes de trabajo.
- Uso de LSTM u otros modelos de Deep Learning para patrones no lineales complejos.
- Dashboard móvil dedicado y alertas push (SMS, e‑mail).
- Optimización multi-objetivo para recomendaciones de limpieza.
- Gemelo digital integrado con otros sistemas (torres de enfriamiento, convertidores).

---

## 11. Referencias

[1] Perry's Chemical Engineers' Handbook, 9th Edition.

[2] Heat Exchanger Design Handbook, Hewitt, 2008.

[3] Fouling of Heat Exchangers, Müller‑Steinhagen, 2000.

[4] TEMA Standards, 10th Edition.

[5] Machine Learning for Predictive Maintenance, Susto et al., 2015.

[6] Scikit‑learn Documentation v1.3.

[7] Streamlit Documentation v1.28.