# MANUAL DE USUARIO
## Dashboard de Monitoreo Predictivo CAP-3 v5.0
**Guía Operativa para Enfriadores de Ácido Sulfúrico**

Codelco – División Chuquicamata  
Planta CAP-3 – Enero 2026

---

## 1. Introducción y acceso

El Dashboard de Monitoreo Predictivo CAP-3 v5.0 es una herramienta interactiva desarrollada en Streamlit que integra análisis térmico, detección de fouling y predicción de eventos de lavado mediante Machine Learning.

### 1.1 Acceso y requisitos

- **Plataforma**: Streamlit web app (navegador Chrome, Firefox, Edge, Safari).
- **URL**: Solicitar a equipo de TI o especialista de procesos.
- **Datos de entrada**:
  - Archivo CSV de histórico de mediciones (temperaturas, flujos, conductividad).
  - Archivo CSV de historial de lavados (fechas, tipos, comentarios).
  - Logo corporativo (opcional, para reportes PDF).

### 1.2 Navegación principal

El dashboard tiene **7 pestañas (tabs)** principales en la parte superior:

1. **Config. Tubos** – Gestión de tubos aislados (futuros).
2. **Análisis Térmico** – Gráficos de temperatura y carga térmica.
3. **Ensuciamiento** – Factor de fouling (Rf) y coeficiente U.
4. **Criticidad** – Índice 0–100 y alertas operacionales.
5. **Predicción ML** – Modelo de Machine Learning para lavados.
6. **Recomendaciones** – Acciones sugeridas por enfriador.
7. **Panel Resumen** – Comparativo global de los 3 enfriadores.

---

## 2. Barra lateral (Sidebar) – Configuración

En el lado izquierdo encontrarás controles de filtrado:

### 2.1 Archivos de datos

```
📁 Archivo datos:
   - Mostrar ruta actual → p.ej. acidcoolersCAP3_synthetic_2years.csv

📁 Archivo lavados:
   - Ruta del CSV de histórico → p.ej. chemicalwashes_CAP3.csv

🖼️ Logo:
   - Ruta de imagen corporativa para reportes PDF
```

### 2.2 Filtros operacionales

**Velocidad mín. soplador** (0–80 RPM)
- Excluye datos con soplador muy bajo.
- Rango típico: 40–60 RPM.
- Recomendación: Mantener en 50 RPM (default).

**Flujo agua mín. (% diseño)** (10–80%)
- Filtra operación con poco flujo de agua.
- Rango típico: 30–50%.
- Recomendación: Mantener en 30%.

### 2.3 Configuración de ML

**Modelo** (AUTO, MODELO 1, MODELO 2, MODELO 3)
- AUTO: Selecciona automáticamente el de mejor PR-AUC.
- MODELO 1: Logistic Regression (rápido, interpretable).
- MODELO 2: GradientBoosting (equilibrio).
- MODELO 3: RandomForest (más robusto, lento).

---

## 3. Pestaña "Análisis Térmico"

### 3.1 Gráfico superior: Temperaturas del ácido

**Líneas mostradas:**
- **T entrada (Tain)**: Temperatura del ácido que ingresa.
- **T salida (Taout)**: Temperatura del ácido que sale (crítica para calidad).
- **Línea roja punteada**: Límite de seguridad (p.ej. 60°C para Secado).
- **Línea verde punteada**: Temperatura de diseño (p.ej. 55°C).

**Cómo leer:**
- Si Taout supera la línea roja → **ALERTA**: Requiere revisión inmediata.
- Si Taout oscila entre verde y roja → **ATENCIÓN**: Comenzar monitoreo diario.
- Si Taout está bajo la línea verde → **NORMAL**: Equipo en buen estado.

### 3.2 Gráfico inferior: Carga térmica (Q)

**Líneas:**
- **Q real** (en MW): Calor transferido realmente.
- **Q diseño** (línea verde punteada): Capacidad de diseño.

**Interpretación:**
- Si Q real > 1.2× Q diseño → Sobrecarga térmica, verificar datos o by‑pass.
- Si Q real < 0.5× Q diseño → Baja carga, operación normal o válvulas cerradas.
- Rango normal: 0.6–1.0× Q diseño.

### 3.3 Líneas verticales de lavados

**Líneas punteadas de color púrpura** indican momentos en que se realizó un lavado químico. Observe cómo la temperatura tiende a bajar después de un lavado.

---

## 4. Pestaña "Ensuciamiento"

### 4.1 Gráfico superior: Factor de fouling (Rf)

**Escala**: 10⁻⁵ m²K/W (valores típicos: 0–15)

**Zonas de referencia:**
- **Línea verde punteada**: Fouling de diseño (~1.43).
- **Línea roja punteada**: Fouling crítico (~7–8, aprox. 5× diseño).

**Interpretación:**
- Rf < 1.5 → Equipo limpio o recién lavado.
- 1.5 < Rf < 3.5 → Ensuciamiento moderado, monitoreo regular.
- 3.5 < Rf < 7 → Ensuciamiento alto, planificar limpieza en 1–2 semanas.
- Rf > 7 → **CRÍTICO**, realizar limpieza química en 48–72 h.

**Aumento tendencial de Rf** → Mayor urgencia de limpieza preventiva.

### 4.2 Gráfico inferior: Coeficiente U (WI m²K)

**Línea azul**: U real calculado.  
**Línea verde**: U limpio (diseño).

**Relación Rf ↔ U:**
- ↑ Rf → ↓ U (transferencia peor).
- Reducción por debajo del 60% de U limpio → Fouling severo.

---

## 5. Pestaña "Criticidad"

### 5.1 Indicador de riesgo global (0–100)

El índice de criticidad integra 4 factores:

| Componente | Peso | Impacto |
|---|---|---|
| Temperatura | 30% | Límite de seguridad del producto |
| Fouling | 35% | Degradación térmica del equipo |
| Eficiencia | 25% | Desempeño general |
| Días desde lavado | 10% | Mantenimiento preventivo |

**Rango de clasificación:**
- 0–30: **BAJA** (verde) – Operación normal.
- 30–60: **MEDIA** (amarillo) – Incluir en checklist semanal.
- 60–80: **ALTA** (naranja) – Planificar limpieza.
- 80–120: **CRÍTICA** (rojo) – Acción inmediata requerida.

### 5.2 Líneas de alerta

- Línea amarilla (30): Transición de baja a media.
- Línea naranja (60): Transición de media a alta.
- Línea roja punteada (80): Umbral crítico.

---

## 6. Pestaña "Predicción ML"

### 6.1 Probabilidad de lavado en 30 días

**Gauge (indicador circular):**
- **Rojo** (p > 0.7): "Requiere lavado" – Programar en próximos 2–3 semanas.
- **Amarillo** (0.3 ≤ p ≤ 0.7): "Zona intermedia" – Incrementar frecuencia de monitoreo.
- **Verde** (p < 0.3): "No requiere lavado" – Mantener monitoreo rutinario.

**Cálculo:**
- 60% peso de predicción ML + 40% peso de score operacional.
- Entrenado con histórico de lavados reales.

### 6.2 Tabla de desempeño de modelos

Muestra PR-AUC y ROC-AUC para cada modelo:
- **PR-AUC** (Precisión-Recall): Métrica principal para desbalance de clases.
- **ROC-AUC** (Receiver Operating Characteristic): Métrica complementaria.

Valores > 0.80 indican buen desempeño; > 0.90, excelente.

### 6.3 Importancia de variables

Gráfico de barras horizontal mostrando las 12 variables más influyentes en la predicción.

**Variables típicas de alto impacto:**
- `Rfslope`: Pendiente de fouling (tendencia).
- `Toutp957d`: Percentil 95 de temperatura salida.
- `Rfdaystocritest`: Días estimados hasta fouling crítico.
- `dayssincewash`: Tiempo desde último lavado.

---

## 7. Pestaña "Recomendaciones"

### 7.1 Resumen por enfriador

Para cada uno de los 3 enfriadores (TS, TAI, TAF):

**Tarjeta con:**
- Estado actual (verde/amarillo/naranja/rojo).
- Síntesis del análisis térmico.
- Síntesis del análisis de fouling.
- Síntesis del análisis de criticidad.
- **Recomendación de acción** (operador lee en lenguaje natural).

### 7.2 Tipos de recomendaciones

1. **Monitoreo rutinario** → Equipo en buen estado, mantener vigilancia diaria.
2. **Incluir en mantenimiento programado** → Revisar en próximo paro planificado.
3. **Planificar limpieza 1–2 semanas** → Ensuciamiento moderado detectado.
4. **Limpieza química en 48–72 h** → Ensuciamiento crítico, riesgo de sobrecalentamiento.
5. **Revisar by‑pass / válvulas** → Posible desviación de flujo.
6. **Evaluar cambio de agua de enfriamiento** → Conductividad elevada.

---

## 8. Pestaña "Panel Resumen"

### 8.1 Tabla comparativa

Muestra en una tabla única los 3 enfriadores con KPIs clave:

| Enfriador | T prom(°C) | T P95(°C) | U limpio(%) | Rf(10⁻⁵) | Días s/lav | Criticidad | Estado |
|---|---|---|---|---|---|---|---|
| TS | 54.2 | 58.1 | 88 | 2.3 | 12 | 42 | Media |
| TAI | 76.5 | 81.2 | 72 | 5.8 | 45 | 78 | Alta |
| TAF | 72.1 | 74.3 | 85 | 3.1 | 23 | 55 | Media |

### 8.2 Gráficos comparativos

- **Gráfico de barras apiladas**: Tubos operativos (verde) vs aislados (rojo) por enfriador.
- **Perfil de criticidad**: Línea temporal comparando índice 0–100 de los 3 equipos.

---

## 9. Datos detallados y descarga

### 9.1 Sección "Datos Detallados" (expandible)

- **Checkbox "Incluir fuera de operación"**: Por defecto muestra solo datos en operación normal.
- **Tabla scrolleable**: Últimas 500 filas con todas las columnas procesadas.
- **Descarga interactiva**: Botón para exportar a CSV.

### 9.2 Generación de reportes PDF

En la esquina superior derecha, botón **"📊 Generar Reporte PDF"**:

- Compila resumen ejecutivo.
- Incluye gráficos de tendencia para los 3 enfriadores.
- Tabla con KPIs y recomendaciones.
- Timeline de lavados.
- Estimación de ROI esperado.

---

## 10. Manejo de lavados históricos

### 10.1 Agregar un nuevo lavado

En la sección lateral (o en tab dedicada):

1. **Selector de enfriador**: Elige TS, TAI o TAF.
2. **Fecha y hora**: Datepicker con formato datetime.
3. **Tipo de lavado**: "Químico", "Mecánico", "Combinado", etc.
4. **Comentarios**: Anotaciones (p.ej. "Presión 150 bar, duración 3 h").
5. **Usuario**: Nombre del operador responsable.
6. **Botón "Guardar"**: Registra en CSV.

La app automáticamente:
- Recalcula `dayssincewash`.
- Actualiza gráficos y reinicia features de ML.
- Regenera predicciones.

---

## 11. Alertas y notificaciones

### 11.1 Indicadores visuales

**Color de fondo en tabs:**
- Verde: Todos los enfriadores en estado normal.
- Amarillo: Al menos uno en estado medio.
- Naranja: Al menos uno en estado alto.
- Rojo: Al menos uno en estado crítico.

**Iconos en tarjetas de enfriador:**
- ✅ Verde: Buen estado.
- ⚠️ Amarillo: Atención moderada.
- 🔴 Rojo: Crítico, acción inmediata.

### 11.2 Interpretaciones automáticas

Al final de cada gráfico, la app despliega texto interpretativo:

```
"ALERTA: P95 Rf crítico en 8.5 (10⁻⁵ m²K/W), excede 
umbral de 7.1. Limpieza prioritaria requerida en 48–72 h.
Tendencia ascendente detectada."
```

---

## 12. Casos de uso operacional

### Caso 1: Monitoreo rutinario matutino

1. Abrir dashboard (tab **Análisis Térmico**).
2. Revisar gráficos de T_out y Q últimas 24 h.
3. Ir a **Panel Resumen**, validar criticidad de los 3 enfriadores.
4. Si alguno > 60, revisar **Recomendaciones** para detalles.
5. Si necesario, agendar limpieza consultando **Predicción ML**.

**Tiempo estimado**: 5–10 minutos.

### Caso 2: Investigación de evento térmico

1. Usuario reporta aumento anormal de Taout.
2. Ir a **Análisis Térmico**, zoom en rango temporal (últimos 7 días).
3. Revisar **Ensuciamiento** para validar si Rf también subió.
4. Comparar con **Criticidad** para confirmar si es fouling o problema de agua.
5. Si fouling confirmado, revisar **Predicción ML** y seguir recomendación.

**Tiempo estimado**: 10–15 minutos.

### Caso 3: Planificación de mantenimiento preventivo

1. Revisar **Panel Resumen** para estado global.
2. Ir a **Predicción ML**, validar probabilidad de lavado próximos 30 días.
3. Revisar **Recomendaciones** por enfriador.
4. Agendar limpiezas en orden de prioridad (criticidad alta primero).
5. Registrar lavados históricos después de ejecutar.

**Tiempo estimado**: 20–30 minutos.

---

## 13. Troubleshooting

### Problema: "Sin datos en operación"

**Causa**: Filtros muy restrictivos.  
**Solución**:
- Bajar "Velocidad mín. soplador" a 40–45.
- Bajar "Flujo agua mín." a 20–25%.
- Revisar que archivo CSV tenga datos con timestamp válido.

### Problema: "Modelo no entrenable"

**Causa**: Insuficientes lavados históricos.  
**Solución**:
- Recopilar al menos 300 observaciones de datos históricos.
- Contar eventos de lavado: necesitar ≥10 lavados y ≥10 no lavados.
- Esperar 1–2 meses de operación con registro completo.

### Problema: "Gráficos no actualizan después de agregar lavado"

**Causa**: Cache de Streamlit.  
**Solución**:
- Presionar **R** (recarga de navegador) o F5.
- O hacer click en botón "Clear cache" (si disponible en sidebar).

### Problema: "PDF no genera"

**Causa**: Librería ReportLab no disponible o falta logo.  
**Solución**:
- Contactar al equipo de TI para instalación de dependencias.
- O dejar ruta de logo vacía (genera sin logo corporativo).

---

## 14. Glosario de términos

| Término | Definición |
|---|---|
| **Taout** | Temperatura de salida del ácido (crítica para producto) |
| **Rf** | Factor de ensuciamiento (resistencia térmica por depósitos) |
| **U** | Coeficiente global de transferencia de calor |
| **LMTD** | Diferencia de temperatura media logarítmica |
| **Q** | Calor transferido (en W o MW) |
| **P95** | Percentil 95 (valor donde 95% de datos están bajo él) |
| **Criticidad** | Índice 0–100 que mide riesgo operacional global |
| **Fouling** | Acumulación de depósitos que reduce transferencia de calor |
| **Score operacional** | Índice 0–1 combinando múltiples indicadores de riesgo |
| **PR-AUC** | Métrica de desempeño ML (precisión vs recall) |

---

## 15. Contacto y soporte

**Especialista de procesos CAP-3:**  
Sebastín Marinovic Leiva  
✉️ sebamarinovic.leiva@codelco.com  
📱 +56 9 7624 3605

**Reportar bugs o sugerencias:**
- Enviar screenshot + descripción del problema.
- Incluir rango de fechas afectado.
- Anexar CSV de datos si es relevante.

---

**Documento versión 1.0 – Enero 2026**  
Última actualización: 13 de enero de 2026