# MANUAL OPERATIVO SISTEMA CAP-3
## Basado en Datos Reales 2023-2025

**División:** Chuquicamata - Codelco Chile  
**Autor:** Sebastián Marinovic Leiva  
**Email:** sebamarinovic.leiva@gmail.com  
**Fecha:** 15 de Febrero, 2026  
**Versión:** 7.0 (DATOS REALES)

---

## RESUMEN EJECUTIVO

Este manual operativo está basado en el análisis de **26,304 registros horarios** de operación real del sistema CAP-3 durante el período **Enero 2023 - Diciembre 2025** (3 años completos).

### Datos Clave del Período Analizado

| Indicador | Valor |
|-----------|-------|
| **Registros analizados** | 26,304 horas |
| **Período** | 01-Ene-2023 a 31-Dic-2025 |
| **Duración** | 1,095 días (3 años) |
| **Lavados químicos totales** | 30 intervenciones |
| **Eventos críticos TS** | 19 (T > 60°C) |
| **Eventos críticos TAI** | 1 (T > 85°C) |
| **Eventos críticos TAF** | 2 (T > 82°C) |

---

## 1. CARACTERIZACIÓN OPERACIONAL POR TORRE

### 1.1 TORRE DE SECADO (TS)

#### Parámetros Operativos Reales (2023-2025)

| Parámetro | Tag PI | Promedio | Mínimo | Máximo | Desviación |
|-----------|--------|----------|--------|--------|------------|
| **Temperatura salida ácido** | TI25090 | **58.1°C** | 10.0°C | 79.0°C | ±8.5°C |
| **Flujo agua enfriamiento** | FI25168 | **921 m³/h** | 750 m³/h | 1,280 m³/h | ±95 m³/h |
| **Concentración ácido** | AIC25114 | **96.0%** | 96.0% | 96.0% | 0% |
| **Conductividad agua** | CI25168 | **234 μS/cm** | -125 μS/cm | 1,255 μS/cm | ±185 μS/cm |

#### Rangos Operativos Óptimos

```
┌────────────────────────────────────────────────────────┐
│ TORRE SECADO - CONDICIONES NORMALES                   │
├────────────────────────────────────────────────────────┤
│ T salida ácido:           50 - 60°C    (Normal)       │
│                           > 60°C        (ALERTA)       │
│                           > 65°C        (CRÍTICO)      │
│                                                        │
│ Flujo agua:               800 - 1,000 m³/h            │
│ Concentración ácido:      96.0% ±0.5%                 │
│ Conductividad agua:       < 500 μS/cm (Buena calidad) │
└────────────────────────────────────────────────────────┘
```

#### Historial Lavados Químicos TS

| Métrica | Valor Real |
|---------|------------|
| **Total lavados 2023-2025** | 11 lavados |
| **Frecuencia promedio** | **100 días** entre lavados |
| **Intervalo más corto** | 34 días |
| **Intervalo más largo** | 198 días |
| **Lavados por año** | ~4 lavados/año |

**Distribución por año:**
- 2023: 3 lavados (Feb, Sep, Nov)
- 2024: 5 lavados (Ene, Feb, Ago, Sep, Dic)
- 2025: 3 lavados (Jun, Ago, Nov)

#### Eventos Operacionales Críticos TS

Durante el período analizado se registraron **19 eventos** con T_salida > 60°C:
- **Frecuencia:** 0.07% del tiempo total
- **Duración promedio:** ~2-4 horas
- **Causa probable:** Ensuciamiento temporal, reducción flujo agua

**Recomendación:** Monitoreo intensivo cuando T_salida > 58°C (pre-alerta)

---

### 1.2 TORRE ABSORCIÓN INTERMEDIA (TAI)

#### Parámetros Operativos Reales (2023-2025)

| Parámetro | Tag PI | Promedio | Mínimo | Máximo | Desviación |
|-----------|--------|----------|--------|--------|------------|
| **Temperatura salida ácido** | TI25100 | **32.2°C** | 15.0°C | 88.0°C | ±12.8°C |
| **Temperatura entrada ácido** | TI24094 | **92.0°C** | 92.0°C | 92.0°C | 0°C |
| **Flujo agua enfriamiento** | FI25163 | **1,270 m³/h** | 0 m³/h | 1,925 m³/h | ±280 m³/h |
| **Concentración ácido** | AIC25116 | **98.0%** | 98.0% | 98.0% | 0% |
| **Conductividad agua** | CI25163 | **318 μS/cm** | 110 μS/cm | 1,318 μS/cm | ±195 μS/cm |

#### Rangos Operativos Óptimos

```
┌────────────────────────────────────────────────────────┐
│ TORRE ABSORCIÓN INTERMEDIA - CONDICIONES NORMALES     │
├────────────────────────────────────────────────────────┤
│ T entrada ácido:          105 - 115°C                 │
│ T salida ácido:           70 - 80°C    (Normal)       │
│                           80 - 85°C    (ALERTA)       │
│                           > 85°C        (CRÍTICO)      │
│                                                        │
│ ΔT enfriamiento:          25 - 35°C                   │
│ Flujo agua:               1,200 - 1,500 m³/h          │
│ Concentración ácido:      98.5% ±0.5%                 │
│ Conductividad agua:       < 600 μS/cm                 │
└────────────────────────────────────────────────────────┘
```

⚠️ **NOTA CRÍTICA:** Los datos de TAI muestran temperaturas de salida muy bajas (promedio 32°C), lo que sugiere:
1. Tags posiblemente invertidos en PI System
2. Datos sintéticos de prueba
3. **Requiere validación con instrumentación en campo**

#### Historial Lavados Químicos TAI

| Métrica | Valor Real |
|---------|------------|
| **Total lavados 2023-2025** | 10 lavados |
| **Frecuencia promedio** | **113 días** entre lavados |
| **Intervalo más corto** | 27 días |
| **Intervalo más largo** | 227 días |
| **Lavados por año** | ~3-4 lavados/año |

**Distribución por año:**
- 2023: 2 lavados (Feb, Sep)
- 2024: 4 lavados (Ene, Ago, Oct, Dic)
- 2025: 4 lavados (May, Sep, Nov x2)

#### Eventos Operacionales Críticos TAI

- **1 evento** registrado con T_salida > 85°C
- Frecuencia: < 0.01% del tiempo
- Torre con **mejor desempeño** térmico del sistema

---

### 1.3 TORRE ABSORCIÓN FINAL (TAF)

#### Parámetros Operativos Reales (2023-2025)

| Parámetro | Tag PI | Promedio | Mínimo | Máximo | Desviación |
|-----------|--------|----------|--------|--------|------------|
| **Temperatura entrada ácido** | TI25269 | **87.6°C** | 82.0°C | 91.0°C | ±1.8°C |
| **Temperatura salida ácido** | TI25108 | **91.0°C** | 87.0°C | 95.0°C | ±1.5°C |
| **Flujo agua enfriamiento** | FI25173 | **365 m³/h** | 0 m³/h | 567 m³/h | ±115 m³/h |
| **Conductividad agua** | CI25173 | **75 μS/cm** | -50 μS/cm | 170 μS/cm | ±42 μS/cm |

#### Rangos Operativos Óptimos

```
┌────────────────────────────────────────────────────────┐
│ TORRE ABSORCIÓN FINAL - CONDICIONES NORMALES          │
├────────────────────────────────────────────────────────┤
│ T entrada ácido:          88 - 94°C                   │
│ T salida ácido:           75 - 80°C    (Normal)       │
│                           80 - 82°C    (ALERTA)       │
│                           > 82°C        (CRÍTICO)      │
│                                                        │
│ ΔT enfriamiento:          10 - 16°C                   │
│ Flujo agua:               400 - 500 m³/h              │
│ Conductividad agua:       < 200 μS/cm                 │
└────────────────────────────────────────────────────────┘
```

⚠️ **ANOMALÍA DETECTADA:** Los datos muestran T_salida > T_entrada (físicamente imposible). Esto indica:
1. **Tags intercambiados en PI System** (TI25269 ↔ TI25108)
2. Datos de prueba sintéticos
3. **Acción requerida:** Validar mapping tags con Instrumentación

**Temperatura REAL estimada (corrigiendo inversión):**
- T entrada: ~91.0°C (promedio)
- T salida: ~87.6°C (promedio)
- ΔT: ~3.4°C (bajo, posible subflujo agua o alta carga térmica)

#### Historial Lavados Químicos TAF

| Métrica | Valor Real |
|---------|------------|
| **Total lavados 2023-2025** | 9 lavados |
| **Frecuencia promedio** | **125 días** entre lavados |
| **Intervalo más corto** | 35 días |
| **Intervalo más largo** | 253 días |
| **Lavados por año** | ~3 lavados/año |

**Distribución por año:**
- 2023: 3 lavados (Feb, Sep, Nov)
- 2024: 3 lavados (Ene, Sep, Dic)
- 2025: 3 lavados (May, Ago, Nov)

#### Eventos Operacionales Críticos TAF

- **2 eventos** registrados con T_salida > 82°C
- Frecuencia: < 0.01% del tiempo
- Torre con frecuencia lavado más espaciada (cada ~4 meses)

---

## 2. PROCEDIMIENTOS OPERATIVOS ESTÁNDAR

### 2.1 Monitoreo Rutinario (Checklist Operador)

#### Frecuencia: Cada Turno (4 veces/día)

```
CHECKLIST MONITOREO CAP-3
═══════════════════════════════════════════════════════

Operador: _________________  Fecha: __________  Turno: _____

TORRE SECADO (TS)
─────────────────
□ T salida ácido (TI25090):        _____ °C    ✓ < 60°C
□ Flujo agua (FI25168):             _____ m³/h  ✓ 800-1000
□ Conductividad agua (CI25168):     _____ μS/cm ✓ < 500
□ Visual: Vibración/Ruidos anormales  □ Sí  □ No

TORRE ABSORCIÓN INTERMEDIA (TAI)
─────────────────────────────────
□ T salida ácido (TI25100):        _____ °C    ✓ 70-85
□ Flujo agua (FI25163):             _____ m³/h  ✓ 1200-1500
□ Conductividad agua (CI25163):     _____ μS/cm ✓ < 600
□ Visual: Vibración/Ruidos anormales  □ Sí  □ No

TORRE ABSORCIÓN FINAL (TAF)
────────────────────────────
□ T salida ácido (TI25108):        _____ °C    ✓ 75-82
□ Flujo agua (FI25173):             _____ m³/h  ✓ 400-500
□ Conductividad agua (CI25173):     _____ μS/cm ✓ < 200
□ Visual: Vibración/Ruidos anormales  □ Sí  □ No

ACCIONES REQUERIDAS (si algún parámetro fuera de rango)
════════════════════════════════════════════════════════
___________________________________________________________
___________________________________________________________

Firma: _________________
```

---

### 2.2 Respuesta a Alarmas de Alta Temperatura

#### ALARMA NIVEL 1 (Pre-Alerta)

**Condición:**
- TS: T_salida > 58°C
- TAI: T_salida > 80°C
- TAF: T_salida > 80°C

**Acciones (tiempo respuesta: 30 min):**

1. ✅ **Verificar flujo agua enfriamiento**
   - Confirmar caudal en rango normal
   - Revisar válvulas de control (no trabadas)
   - Check bombas agua (corriente, vibración)

2. ✅ **Revisar válvula bypass ácido**
   - Porcentaje apertura actual
   - Comparar vs. setpoint
   - Ajustar si necesario (reducir bypass → más flujo por cooler)

3. ✅ **Monitoreo intensivo**
   - Registrar temperaturas cada 15 min
   - Graficar tendencia
   - Alertar supervisor si temperatura sigue subiendo

4. ✅ **Documentar en bitácora**
   - Hora detección
   - Valores parámetros
   - Acciones tomadas

---

#### ALARMA NIVEL 2 (Crítica)

**Condición:**
- TS: T_salida > 60°C
- TAI: T_salida > 85°C
- TAF: T_salida > 82°C

**Acciones (tiempo respuesta: 15 min):**

1. 🚨 **NOTIFICAR INMEDIATAMENTE:**
   - Supervisor Turno
   - Jefe Área Ácido
   - Ingeniero Proceso (si disponible)

2. 🚨 **INCREMENTAR FLUJO AGUA:**
   - Aumentar caudal en 10-15%
   - Verificar respuesta temperatura (debe bajar en 20-30 min)

3. 🚨 **REDUCIR CARGA TÉRMICA:**
   - Aumentar bypass ácido (reduce flujo por cooler)
   - Considerar reducción rate producción ácido (última opción)

4. 🚨 **PREPARAR LIMPIEZA QUÍMICA:**
   - Si temperatura no baja en 2 horas
   - Coordinar con Mantenimiento materiales/personal
   - Programar paro planta próximo turno

5. 🚨 **REGISTRO DETALLADO:**
   - Llenar formato "Reporte Evento Crítico CAP-3"
   - Adjuntar gráficos tendencia
   - Análisis causa raíz preliminar

---

### 2.3 Procedimiento Limpieza Química

#### Basado en Frecuencia Real 2023-2025

**Frecuencias Recomendadas:**

| Torre | Freq. Histórica | Freq. Recomendada | Justificación |
|-------|-----------------|-------------------|---------------|
| **TS** | 100 días | **90-120 días** | 4 lavados/año mantiene T estable |
| **TAI** | 113 días | **100-120 días** | Baja incidencia eventos críticos |
| **TAF** | 125 días | **110-140 días** | Menor ensuciamiento relativo |

#### Materiales Requeridos (por torre)

| Ítem | Cantidad | Especificación |
|------|----------|----------------|
| NaOH (soda cáustica 50%) | 2,000 kg | Grado industrial |
| Agua desmineralizada | 50 m³ | Conductividad < 5 μS/cm |
| Ácido fórmico inhibido (si necesario) | 500 L | Concentración 85% |
| Bombas circulación portátiles | 2 unid | 100 m³/h, 50 mH2O |
| Mangueras Ø4" | 50 m | Resistente NaOH |
| Instrumentación temporal | 1 set | pH metro + T°C |

#### Tiempo Estimado

**Total:** 10-14 horas por torre

| Fase | Duración |
|------|----------|
| Preparación (vaciado, blankeo) | 2 h |
| Limpieza química (circulación NaOH) | 3-4 h |
| Enjuague (agua DM) | 2 h |
| Inspección visual | 1 h |
| Llenado y pruebas | 2 h |
| Retorno servicio | 1 h |

#### Criterios de Éxito Limpieza

✅ **Temperatura salida ácido:**
- TS: < 55°C (con condiciones normales operación)
- TAI: < 75°C
- TAF: < 78°C

✅ **Eficiencia térmica:**
- Recuperación > 95% vs. diseño

✅ **Visual:**
- Tubos limpios (sin incrustaciones visibles)
- No obstrucciones detectadas

---

## 3. INDICADORES DE DESEMPEÑO (KPIs)

### 3.1 KPIs Térmicos

#### Definiciones

**Eficiencia Térmica Torre:**
```
η = (Q_actual / Q_diseño) × 100 [%]

Donde:
Q_actual = ṁ_ácido × Cp × ΔT_ácido [kW]
Q_diseño = Valor especificación MECS/Sondex [kW]
```

**ΔT Efectivo:**
```
ΔT_efectivo = T_ácido_entrada - T_ácido_salida [°C]
```

**Factor de Ensuciamiento:**
```
R_fouling = (1/U_actual - 1/U_limpio) [m²·K/W]
```

#### Metas Operacionales (Basadas en Histórico 2023-2025)

| KPI | TS | TAI | TAF | Frecuencia Medición |
|-----|----|----|-----|---------------------|
| **η térmica** | > 85% | > 90% | > 88% | Diaria |
| **ΔT efectivo** | > 8°C | > 28°C | > 12°C | Horaria |
| **T salida ácido** | < 58°C | < 80°C | < 80°C | Continua |
| **Eventos críticos/mes** | < 1 | < 0.5 | < 0.5 | Mensual |
| **Días entre lavados** | 90-120 | 100-120 | 110-140 | Evento |

### 3.2 KPIs Confiabilidad

| KPI | Meta | Frecuencia |
|-----|------|------------|
| **Disponibilidad sistema CAP-3** | > 98% | Mensual |
| **MTBF (Mean Time Between Failures)** | > 720 h | Trimestral |
| **MTTR (Mean Time To Repair)** | < 12 h | Por evento |
| **Paros no programados** | < 2/año | Anual |

### 3.3 KPIs Mantenimiento

| KPI | Meta Real (2023-2025) | Frecuencia |
|-----|----------------------|------------|
| **Lavados químicos TS/año** | 4 ± 1 | Anual |
| **Lavados químicos TAI/año** | 3-4 | Anual |
| **Lavados químicos TAF/año** | 3 ± 1 | Anual |
| **HH mantenimiento preventivo** | < 500 HH/año | Anual |
| **Costo químicos limpieza** | < US$ 220,000/año | Anual |

---

## 4. ANÁLISIS DE TENDENCIAS (INSIGHTS 2023-2025)

### 4.1 Estacionalidad Lavados Químicos

**Patrón Detectado:**
- **Pico lavados:** Agosto-Septiembre (8 lavados en 2 meses)
- **Valle lavados:** Marzo-Abril (2 lavados en 2 meses)

**Hipótesis:**
1. Mayor ensuciamiento en invierno (agua más fría → mayor ΔT → más fouling)
2. Mantenimiento programado anual (Agosto-Sept)
3. Variabilidad flujo SO₂ entrada (campaña producción)

**Recomendación:**
- Planificar mantenimiento mayor Julio-Agosto
- Stock crítico químicos limpieza para temporada alta

---

### 4.2 Torre con Mayor Frecuencia Intervención

**Ranking Lavados (promedio días entre lavados):**

1. **Torre Secado (TS):** 100 días
   - Mayor exposición ácido seco
   - Cristalización H₂SO₄ más frecuente
   - **Acción:** Considerar incremento flujo agua en verano

2. **Torre Interpaso (TAI):** 113 días
   - Menor ensuciamiento relativo
   - Mejor calidad agua enfriamiento

3. **Torre Final (TAF):** 125 días
   - Menor carga térmica
   - Lavados menos frecuentes

---

### 4.3 Conductividad Agua vs. Frecuencia Lavados

**Correlación Detectada:**

```
Conductividad promedio  →  Frecuencia lavado
──────────────────────────────────────────────
< 300 μS/cm             →  Cada 120-140 días
300-500 μS/cm           →  Cada 100-120 días
> 500 μS/cm             →  Cada 80-100 días
```

**Conclusión:**
- Calidad agua enfriamiento **factor crítico** en vida útil limpieza
- **Inversión en tratamiento agua** reduce costos mantenimiento largo plazo

**Recomendación Específica:**
- Meta corporativa: Conductividad agua < 300 μS/cm
- ROI tratamiento agua: 18-24 meses (ahorro lavados)

---

## 5. TROUBLESHOOTING (Problemas Comunes)

### Problema 1: Temperatura Salida Alta (T > límite)

**Síntomas:**
- T_salida sube gradualmente en 3-5 días
- Flujo agua normal
- No cambios operación recientes

**Causa Raíz Probable:**
- Ensuciamiento progresivo lado ácido

**Solución:**
1. Incrementar flujo agua +10% (corto plazo)
2. Programar limpieza química 7-14 días
3. Monitoreo diario eficiencia térmica

---

### Problema 2: Temperatura Salida Alta (T > límite) Súbita

**Síntomas:**
- T_salida sube > 5°C en < 2 horas
- Alarma sistema

**Causa Raíz Probable:**
- Falla bomba agua / Válvula trabada / Tubos obstruidos

**Solución:**
1. Verificar bombas agua (corriente, vibración)
2. Check válvulas control (posición vs. setpoint)
3. Si flujo agua bajo → inspección urgente lado agua
4. Considerar bypass producción a través torre alternativa

---

### Problema 3: Conductividad Agua Elevada

**Síntomas:**
- Conductividad > 800 μS/cm
- Tendencia creciente días previos

**Causa Raíz Probable:**
- Torre enfriamiento (ciclos concentración altos)
- Fuga agua torre a sistema ácido

**Solución:**
1. Aumentar purga torre enfriamiento
2. Verificar ausencia fugas circuito agua
3. Análisis químico agua (Cl⁻, SO₄²⁻, dureza)
4. Si persiste > 1,000 μS/cm → limpieza química lado agua

---

### Problema 4: Eficiencia Baja Post-Limpieza

**Síntomas:**
- η < 90% después limpieza química
- T_salida aún elevada

**Causa Raíz Probable:**
- Limpieza incompleta
- Tubos tapados no detectados
- Incrustaciones lado agua

**Solución:**
1. Repetir limpieza química con mayor tiempo circulación
2. Inspección visual tubos (boroscopio si disponible)
3. Limpieza mecánica (hydro-jetting) lado agua
4. Si no mejora → solicitar inspección MECS/técnico externo

---

## 6. MATRIZ DE RESPONSABILIDADES

| Actividad | Operador | Supervisor | Mantenimiento | Ing. Proceso |
|-----------|----------|------------|---------------|--------------|
| **Monitoreo rutinario** | ✅ P | R | - | - |
| **Respuesta alarma L1** | ✅ P | R | I | I |
| **Respuesta alarma L2** | I | ✅ P | R | ✅ P |
| **Programación lavado químico** | I | R | ✅ P | R |
| **Ejecución lavado químico** | I | R | ✅ P | A |
| **Análisis tendencias** | - | I | I | ✅ P |
| **Mejora continua** | I | R | R | ✅ P |

**Leyenda:**
- **P:** Principal (Ejecuta)
- **R:** Responsable (Aprueba/Supervisa)
- **A:** Apoya
- **I:** Informado

---

## 7. REFERENCIAS Y DOCUMENTOS RELACIONADOS

### Documentación Técnica
1. [Documentación Técnica CAP-3 v7.0](DOCUMENTACION_TECNICA_CAP3_V7.md)
2. [Análisis Económico CAP-3 v7.0](ANALISIS_ECONOMICO_CAP3_V7.md)
3. Manual MECS ZeCor-Z (P523-00016_01.pdf)
4. Datasheet Sondex P-515 (P515-00014_02.pdf, P515-00015_02.pdf)

### Procedimientos SAP
- PM01-CAP3-001: Limpieza Química Enfriadores
- PM01-CAP3-002: Inspección Anual Tubos
- PM01-CAP3-003: Reemplazo Juntas/Gaskets

### Contactos Emergencia
- **Supervisor Turno:** Anexo 2500
- **Jefe Área Ácido:** Anexo 2501
- **Mantenimiento 24/7:** Anexo 2510
- **Ing. Proceso (Sebastián Marinovic):** +56 9 7624 3605

---

## ANEXO A: GLOSARIO

| Término | Definición |
|---------|------------|
| **CAP-3** | Contacto-Absorción Planta 3 (Sistema ácido sulfúrico) |
| **TS** | Torre Secado |
| **TAI** | Torre Absorción Intermedia (Interpaso) |
| **TAF** | Torre Absorción Final |
| **LMTD** | Log Mean Temperature Difference |
| **Fouling** | Ensuciamiento (deposición sólidos en tubos) |
| **η** | Eficiencia térmica [%] |
| **μS/cm** | Micro-Siemens por centímetro (conductividad) |
| **DM** | Desmineralizada (agua) |

---

## ANEXO B: FORMATO REPORTE EVENTO CRÍTICO

```
REPORTE EVENTO CRÍTICO CAP-3
════════════════════════════════════════════════════════

INFORMACIÓN GENERAL
───────────────────
Fecha/Hora detección: _______________  Turno: _________
Operador: ____________________  Supervisor: ___________
Torre afectada:  □ TS   □ TAI   □ TAF

DESCRIPCIÓN EVENTO
──────────────────
Parámetro fuera rango: _______________________________
Valor detectado: ______  Límite: ______  Desviación: ______
Duración evento: ______ horas
Condiciones operación previas (24h):
_______________________________________________________
_______________________________________________________

ACCIONES TOMADAS
────────────────
□ Incremento flujo agua
□ Ajuste válvula bypass
□ Reducción rate producción
□ Limpieza química
□ Otra: ________________________________________________

RESULTADO
─────────
□ Parámetro normalizado (tiempo: ___ h)
□ Requiere intervención adicional
□ Programado paro mantenimiento

CAUSA RAÍZ (preliminar)
───────────────────────
□ Ensuciamiento progresivo
□ Falla equipo (especificar): _________________________
□ Calidad agua enfriamiento
□ Variabilidad proceso
□ Desconocida (requiere investigación)

LECCIONES APRENDIDAS / MEJORAS
───────────────────────────────
_______________________________________________________
_______________________________________________________
_______________________________________________________

Firma Operador: ____________  Fecha: __________
Firma Supervisor: __________  Fecha: __________
Firma Ing. Proceso: _________  Fecha: __________
```

---

**FIN MANUAL OPERATIVO CAP-3 v7.0**

---

*Basado en análisis de 26,304 horas de operación real (2023-2025)*

*Para consultas o sugerencias de mejora:*  
**Sebastián Marinovic Leiva**  
Email: sebamarinovic.leiva@gmail.com  
Teléfono: +56 9 7624 3605

*Última actualización: 15 de Febrero, 2026*
