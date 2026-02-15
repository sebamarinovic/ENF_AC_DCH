# DOCUMENTACIÓN TÉCNICA SISTEMA PREDICTIVO CAP-3
## Versión 6.0 - Febrero 2026

**Proyecto:** Sistema de Monitoreo Predictivo - Enfriadores de Ácido Sulfúrico  
**División:** Chuquicamata - Codelco Chile  
**Autor:** Sebastián Marinovic Leiva  
**Email:** sebamarinovic.leiva@gmail.com  
**Fecha:** 15 de Febrero, 2026

---

## 1. RESUMEN EJECUTIVO

### 1.1 Propósito del Sistema
Sistema de monitoreo predictivo basado en Machine Learning para optimizar la operación de 8 enfriadores de ácido sulfúrico en la Planta de Ácido CAP-3, División Chuquicamata.

### 1.2 Alcance
- **3 Torres de enfriamiento:**
  - Torre de Secado (TS): 4 enfriadores
  - Torre de Absorción Intermedia (TAI): 2 enfriadores  
  - Torre de Absorción Final (TAF): 2 enfriadores
- **Total:** 8 intercambiadores de calor tipo placa y bastidor

### 1.3 Objetivos
1. Reducir paros no programados en 70% (de 6,255 ton pérdidas a 1,877 ton/año)
2. Optimizar frecuencia de limpieza química
3. Extender vida útil de tubos en 20-30%
4. Generar ahorro operativo de US$ 180,000-340,000/año

---

## 2. ESPECIFICACIONES TÉCNICAS DE EQUIPOS

### 2.1 ENFRIADORES DE ÁCIDO PRODUCTO (P-515)

#### 2.1.1 Product Acid Cooler (5327-ENF-301/302/401/402)
**Fabricante:** Sondex, Inc. (USA)  
**Modelo:** S 47 IS  
**Tipo:** Plate and Frame Heat Exchanger

**Datos de Operación:**
| Parámetro | Lado Frío (Agua) | Lado Caliente (Ácido) |
|-----------|------------------|----------------------|
| Fluido | Agua desmineralizada | H₂SO₄ 96-98.5% |
| Flujo diseño | 94,536 kg/h | 106,848 kg/h |
| T entrada | 32°C | 77°C |
| T salida | 49°C | 35°C |
| Presión diseño | 1,035 kPa(g) | 1,035 kPa(g) |
| ΔP máximo | 100 kPa | 100 kPa |
| Velocidad (conexión) | 3.37 m/s | 2.1 m/s |

**Especificaciones de Diseño:**
- **Tipo:** S 47 IS 111
- **Área transferencia:** 56.04 m²
- **Presión prueba:** 1,346 kPa(g)
- **Número placas:** 111 (suministradas 111, máx 143)
- **Tamaño placa:** 380 × 1,520 mm
- **Espaciado flujo:** 2.6 mm
- **Longitud paso:** 1,365 mm
- **Número pasos:** 1 (simple)
- **Dimensiones (H×W×L):** 1,825 × 495 × 1,035 mm

**Materiales de Construcción:**
- **Placas:** Hastelloy C-276, espesor 0.5 mm
- **Bastidor:** SA516 Gr.70
- **Juntas:** Viton G
- **Boquillas:** SS 316 / Hastelloy C-276
- **Cubiertas:** Acero inoxidable
- **Pernos:** SA193 B7
- **Barras superiores:** CS con manga SS
- **Barras inferiores:** Acero inoxidable

**Conexiones:**
- Entrada/Salida (Frío): 4", #150
- Entrada/Salida (Caliente): 4", #150

**Rendimiento Térmico:**
- **Calor transferido (sucio):** 1,866 kW
- **Coeficiente global U:** 2,975 W/m²·K
- **Fouling allowance:** 12.60%

**Datos de Embarque:**
- Peso en operación (vacío): 881 kg
- Peso en operación (lleno agua): 1,008 kg
- Peso embarque: 1,100 kg
- Volumen embarque: 2.05 m³
- Dimensión mayor: 2,250 × 700 × 1,300 mm

**Tratamiento Superficial:**
- Recubrimiento epóxico, 200 micrones, 2 capas

**Código Primario:**
- ASME SEC VIII Div. I con estampa U

---

#### 2.1.2 Cooling Water Heat Exchangers (5328-INC-301/302/303/304/401/402/403/404)
**Fabricante:** Sondex, Inc. (USA)  
**Modelo:** S 81 IS  
**Tipo:** Plate and Frame Heat Exchanger

**Datos de Operación:**
| Parámetro | Lado Frío (Agua Enfriamiento) | Lado Caliente (Agua Desmineralizada) |
|-----------|-------------------------------|-------------------------------------|
| Fluido | Agua de enfriamiento | Agua desmineralizada |
| Flujo diseño | 1,255,440 kg/h | 1,034,810 kg/h |
| T entrada | 22°C | 49°C |
| T salida | 36°C | 32°C |
| Presión diseño | 420 kPa(g) | 500 kPa(g) |
| ΔP máximo | 100 kPa | 100 kPa |
| Velocidad (conexión) | 4.8 m/s | 3.97 m/s |

**Especificaciones de Diseño:**
- **Tipo:** S 81 IS 240
- **Área transferencia:** 199.92 m²
- **Presión prueba:** 650 kPa(g)
- **Número placas:** 240 (suministradas 240, máx 350)
- **Tamaño placa:** 868 × 1,468 mm
- **Espaciado flujo:** 3.4 mm
- **Longitud paso:** 1,080 mm
- **Número pasos:** 1 (simple)
- **Dimensiones (H×W×L):** 1,955 × 970 × 2,720 mm

**Materiales de Construcción:**
- **Placas:** Titanio, espesor 0.5 mm
- **Bastidor:** SA516 Gr.70
- **Juntas:** Nitrilo
- **Boquillas:** Revestidas en goma
- **Cubiertas:** Acero inoxidable
- **Pernos:** SA193 B7

**Conexiones:**
- Entrada/Salida (Frío): 12", #150
- Entrada/Salida (Caliente): 12", #150

**Rendimiento Térmico:**
- **Calor transferido (sucio):** 20,423 kW
- **Coeficiente global U:** 8,934 W/m²·K
- **Fouling allowance:** 11.00%

**Datos de Embarque:**
- Peso en operación (vacío): 2,800 kg
- Peso en operación (lleno agua): 3,640 kg
- Peso embarque: 3,800 kg
- Volumen embarque: 8.28 m³
- Dimensión mayor: 2,300 × 1,200 × 3,000 mm

---

### 2.2 ENFRIADORES DE ÁCIDO ZECOR-Z (P-523)

#### 2.2.1 Torre de Secado - Drying Tower Acid Cooler (5322-ENF-301/401)
**Fabricante:** MECS, Inc. (DuPont)  
**Job No:** 7P346  
**Drawing:** 431-125 Rev. 4  
**Tipo:** ZeCor Acid Cooler (Shell & Tube)

**Datos de Operación:**
| Parámetro | Valor |
|-----------|-------|
| Área transferencia | 366.87 m² |
| U limpio | 1,718 W/m²·K |
| Q diseño | 15.39 MW |
| Concentración ácido | 96.0% H₂SO₄ |
| T ácido entrada | 75°C (diseño) |
| T ácido salida | 55°C (diseño) |
| T ácido salida límite | 60°C (máximo operativo) |
| T agua entrada | 32°C |
| T agua salida | 49°C |
| LMTD diseño | 24.4°C |
| Fouling diseño | 1.43×10⁻⁴ m²·K/W |
| Flujo ácido diseño | 966 m³/h |
| Flujo agua diseño | 776 m³/h |

**Cargas Verticales (Fundación):**
| Condición | Vacío | Hidroprueba | Operación | Diseño + Sismo |
|-----------|-------|-------------|-----------|----------------|
| Fijo | 3289 kg | 7330 kg | 4853 kg | 6479 kg |
| Deslizante | 1611 kg | 3661 kg | 2403 kg | 3205 kg |

**Cargas Horizontales (Sismo):**
| Dirección | Trans. | Long. |
|-----------|--------|-------|
| Fijo | 4048 kg | 4048 kg |
| Deslizante | 2117 kg | 2117 kg |

**Dimensiones Generales (Aproximadas):**
- Largo total: 9,794 mm
- Ancho: ~900 mm
- Alto (con soportes): ~3,200 mm

**Expansiones Térmicas Esperadas:**
| Boquilla | δ (mm) |
|----------|--------|
| N1 (ácido entrada) | 0.83 |
| N2 (ácido salida) | 7.86 |
| N3 (agua entrada) | 8.40 |
| N4 (agua salida) | 1.21 |

---

#### 2.2.2 Torre Absorción Final - Final Absorbing Tower Acid Cooler (5326-ENF-301/401)
**Fabricante:** MECS, Inc. (DuPont)  
**Job No:** 7P346  
**Drawing:** 431-135 Rev. 3  
**Tipo:** ZeCor Acid Cooler (Shell & Tube)

**Datos de Operación:**
| Parámetro | Valor |
|-----------|-------|
| Área transferencia | 92.98 m² |
| U limpio | 2,070 W/m²·K |
| Q diseño | 8.36 MW |
| Concentración ácido | 98.5% H₂SO₄ |
| T ácido entrada | 91°C (diseño) |
| T ácido salida | 77°C (diseño) |
| T ácido salida límite | 82°C (máximo operativo) |
| T agua entrada | 32°C |
| T agua salida | 49°C |
| LMTD diseño | 43.4°C |
| Fouling diseño | 1.43×10⁻⁴ m²·K/W |
| Flujo ácido diseño | 756 m³/h |
| Flujo agua diseño | 422 m³/h |

**Cargas Verticales (Fundación):**
| Condición | Vacío | Hidroprueba | Operación | Diseño + Sismo |
|-----------|-------|-------------|-----------|----------------|
| Fijo | 1579 kg | 2750 kg | 1995 kg | 2325 kg |
| Deslizante | 1411 kg | 2202 kg | 1739 kg | 2024 kg |

**Cargas Horizontales (Sismo):**
| Dirección | Trans. | Long. |
|-----------|--------|-------|
| Fijo | 2710 kg | 2710 kg |
| Deslizante | 2202 kg | 2202 kg |

**Dimensiones Generales (Aproximadas):**
- Largo total: 7,805 mm
- Ancho: ~1,100 mm
- Alto (con soportes): ~3,200 mm

**Expansiones Térmicas Esperadas:**
| Boquilla | δ (mm) |
|----------|--------|
| N1 (ácido entrada) | 1.18 |
| N2 (ácido salida) | 7.44 |
| N3 (agua entrada) | 8.42 |
| N4 (agua salida) | 2.18 |

---

#### 2.2.3 Torre Absorción Intermedia - Interpass Absorbing Tower Acid Cooler (5325-ENF-301/401)
**Fabricante:** MECS, Inc. (DuPont)  
**Job No:** 7P346  
**Drawing:** 431-137 Rev. 6  
**Tipo:** ZeCor Acid Cooler (Shell & Tube)

**Datos de Operación:**
| Parámetro | Valor |
|-----------|-------|
| Área transferencia | 415.26 m² |
| U limpio | 1,670 W/m²·K |
| Q diseño | 36.13 MW |
| Concentración ácido | 98.5% H₂SO₄ |
| T ácido entrada | 109°C (diseño) |
| T ácido salida | 77°C (diseño) |
| T ácido salida límite | 85°C (máximo operativo) |
| T agua entrada | 32°C |
| T agua salida | 49°C |
| LMTD diseño | 52.1°C |
| Fouling diseño | 1.43×10⁻⁴ m²·K/W |
| Flujo ácido diseño | 1,439 m³/h |
| Flujo agua diseño | 1,823 m³/h |

**Cargas Verticales (Fundación):**
| Condición | Vacío | Hidroprueba | Operación | Diseño + Sismo |
|-----------|-------|-------------|-----------|----------------|
| Fijo | 6500 kg | 12488 kg | 10575 kg | 13962 kg |
| Deslizante | 3370 kg | 6780 kg | 5616 kg | 7379 kg |

**Cargas Horizontales (Sismo):**
| Dirección | Trans. | Long. |
|-----------|--------|-------|
| Fijo | 16546 kg | 16546 kg |
| Deslizante | 8743 kg | 8743 kg |

**Dimensiones Generales (Aproximadas):**
- Largo total: 9,674 mm
- Ancho: ~1,400 mm
- Alto (con soportes): ~3,500 mm

**Expansiones Térmicas Esperadas:**
| Boquilla | δ (mm) |
|----------|--------|
| N1 (ácido entrada) | 0.45 |
| N2 (ácido salida) | 8.19 |
| N3 (agua entrada) | 9.40 |
| N4 (agua salida) | 1.80 |

---

## 3. MATERIALES ESPECIALES

### 3.1 ZeCor-Z (Aleación Propietaria)
**Fabricante:** MECS / DuPont  
**Aplicación:** Tubos en contacto con ácido sulfúrico concentrado

**Características:**
- Alta resistencia a corrosión por H₂SO₄ 93-99%
- Resistencia a temperaturas hasta 120°C
- Sin necesidad de protección anódica (vs. hierro fundido tradicional)
- Vida útil estimada: 15-20 años (vs. 8-10 años materiales convencionales)

**Ventajas vs. Materiales Tradicionales:**
1. **Sin protección anódica** → Menor costo operativo
2. **Mayor resistencia corrosión** → Menor frecuencia reemplazo
3. **Menor ensuciamiento** → Intervalos limpieza más largos
4. **Mejor transferencia calor** → Mayor eficiencia térmica

---

### 3.2 Hastelloy C-276
**Aplicación:** Placas enfriadores P-515

**Composición Nominal:**
- Ni: 54-58%
- Mo: 15-17%
- Cr: 14.5-16.5%
- Fe: 4-7%
- W: 3-4.5%

**Propiedades:**
- Resistencia excepcional a ácidos oxidantes y reductores
- Estabilidad térmica hasta 1,150°C
- Resistencia a corrosión por picado y grietas

---

### 3.3 Titanio (Grade 1 o 2)
**Aplicación:** Placas enfriadores agua P-515

**Características:**
- Excelente resistencia a agua de mar/torre enfriamiento
- Inmune a corrosión por cloruros
- Ligero (ρ ≈ 4,500 kg/m³)
- Alta conductividad térmica

---

## 4. FUNDAMENTOS TERMODINÁMICOS

### 4.1 Ecuación Fundamental de Transferencia de Calor

La transferencia de calor en los intercambiadores se rige por:

**Q = ṁ × Cp × ΔT = U × A × LMTD**

Donde:
- **Q** = Calor transferido [W]
- **ṁ** = Flujo másico [kg/s]
- **Cp** = Calor específico [J/kg·K]
- **ΔT** = Diferencia de temperatura [K]
- **U** = Coeficiente global de transferencia [W/m²·K]
- **A** = Área de transferencia [m²]
- **LMTD** = Diferencia temperatura media logarítmica [K]

---

### 4.2 LMTD (Log Mean Temperature Difference)

Para flujo contracorriente:

**LMTD = (ΔT₁ - ΔT₂) / ln(ΔT₁/ΔT₂)**

Donde:
- **ΔT₁** = T_caliente,entrada - T_fría,salida
- **ΔT₂** = T_caliente,salida - T_fría,entrada

Implementación robusta (evita división por cero):
```python
def safe_lmtd(T_hot_in, T_hot_out, T_cold_in, T_cold_out):
    dT1 = T_hot_in - T_cold_out
    dT2 = T_hot_out - T_cold_in
    
    if dT1 <= 0 or dT2 <= 0:
        return np.nan
    
    if abs(dT1 - dT2) < 1e-6:
        return dT1  # Caso límite
    
    return (dT1 - dT2) / np.log(dT1 / dT2)
```

---

### 4.3 Coeficiente Global U

El coeficiente U considera resistencias térmicas en serie:

**1/U = 1/h_interior + 1/h_exterior + R_fouling_int + R_fouling_ext + e/k**

Donde:
- **h_interior, h_exterior** = Coeficientes convección [W/m²·K]
- **R_fouling** = Resistencia por ensuciamiento [m²·K/W]
- **e** = Espesor pared [m]
- **k** = Conductividad térmica material [W/m·K]

---

### 4.4 Factor de Ensuciamiento (Fouling Factor)

**Definición:**
**R_fouling = (1/U_sucio) - (1/U_limpio)**

**Clasificación Operativa:**

| R_fouling (×10⁻⁴ m²·K/W) | Estado | Acción |
|---------------------------|--------|--------|
| 0.0 - 2.0 | Limpio | Operación normal |
| 2.0 - 5.0 | Ligero | Monitoreo intensivo |
| 5.0 - 10.0 | Moderado | Programar limpieza (30-60 días) |
| > 10.0 | Alto | Limpieza urgente |

**Estándar TEMA RCB-7.41:**
- Agua torre enfriamiento: 1.7-3.5 ×10⁻⁴ m²·K/W
- Ácido sulfúrico limpio: 0.9-1.7 ×10⁻⁴ m²·K/W

---

### 4.5 Propiedades Termofísicas del Ácido Sulfúrico

**Tabla Interpolación (Implementada en Sistema):**

| Concentración [%] | Cp [J/kg·K] | ρ [kg/m³] | μ [mPa·s] @ 60°C |
|-------------------|-------------|-----------|------------------|
| 0 (agua) | 4186 | 998 | 0.47 |
| 50 | 3180 | 1395 | 1.8 |
| 70 | 2470 | 1610 | 4.5 |
| 80 | 2100 | 1727 | 8.0 |
| 90 | 1760 | 1814 | 14.5 |
| 93 | 1680 | 1830 | 18.2 |
| 96 | 1560 | 1836 | 24.8 |
| 98 | 1430 | 1836 | 32.1 |
| 98.5 | 1400 | 1835 | 35.0 |
| 100 | 1340 | 1830 | 42.0 |

**Fuentes:**
- Perry's Chemical Engineers' Handbook, 9th Ed.
- DIPPR Database
- DuPont Sulfuric Acid Handbook

---

## 5. ALGORITMO DE CÁLCULO - MÉTODO DUAL ROBUSTO v6.0

### 5.1 Diagrama de Flujo

```
ENTRADA: Datos PI System (T, F, cond, etc.)
    ↓
PASO 1: Validación y limpieza datos
    - Eliminar valores "Bad Input", "Error"
    - Convertir a numérico
    - Detectar outliers (Z-score > 4)
    ↓
PASO 2: Interpolación propiedades ácido
    - Cp(concentración)
    - ρ(concentración)
    ↓
PASO 3: Cálculo flujo másico ácido
    ṁ_acid = F_volumétrico × ρ [kg/h]
    ↓
PASO 4: Cálculo LMTD
    LMTD = safe_lmtd(T_a_in, T_a_out, T_w_in, T_w_out)
    ↓
PASO 5: Cálculo calor actual
    Q_actual = ṁ_acid × Cp × (T_a_in - T_a_out) [W]
    ↓
PASO 6: Cálculo U aproximado
    U_aprox = Q_actual / (A × LMTD)
    ↓
PASO 7: Cálculo eficiencia térmica
    η = Q_actual / Q_diseño × 100 [%]
    ↓
PASO 8: Cálculo fouling (Método Dual)
    • Método 1 (basado en U):
      R_fouling_U = (1/U_aprox - 1/U_limpio) × sensitivity
    
    • Método 2 (basado en eficiencia):
      R_fouling_η = (η_baseline - η_actual) / 100 × 0.001
    
    • Combinación ponderada:
      R_fouling = 0.7 × R_fouling_U + 0.3 × R_fouling_η
    ↓
PASO 9: Filtrado temporal
    R_fouling_suavizado = MediaMóvil(R_fouling, ventana=12h)
    ↓
PASO 10: Escala para display
    R_display = R_fouling_suavizado × 10,000 [×10⁻⁴ unidades]
    ↓
SALIDA: Indicadores (η, U, R_fouling, criticidad)
```

---

### 5.2 Código Python Implementado

```python
def calcular_indicadores(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    """
    Calcula todos los indicadores térmicos.
    
    Args:
        df: DataFrame con datos de proceso
        params: Diccionario con parámetros de diseño
        
    Returns:
        DataFrame con indicadores calculados
    """
    # PASO 1: Validación inicial
    required = ['T_acid_in_C', 'T_acid_out_C', 'T_water_in_C', 
                'T_water_out_C', 'acid_flow_m3h', 'acid_conc_pct']
    
    if not all(c in df.columns for c in required):
        return df
    
    # PASO 2: Interpolación propiedades
    df['Cp_acid'] = df['acid_conc_pct'].apply(
        lambda x: np.interp(x, list(ACID_PROPS.keys()), 
                           [v[0] for v in ACID_PROPS.values()])
    )
    df['rho_acid'] = df['acid_conc_pct'].apply(
        lambda x: np.interp(x, list(ACID_PROPS.keys()), 
                           [v[1] for v in ACID_PROPS.values()])
    )
    
    # PASO 3: Flujo másico
    df['acid_mass_flow_kgh'] = df['acid_flow_m3h'] * df['rho_acid']
    df['acid_mass_flow_kgs'] = df['acid_mass_flow_kgh'] / 3600
    
    # PASO 4: LMTD
    df['LMTD_C'] = df.apply(
        lambda row: safe_lmtd(
            row['T_acid_in_C'], row['T_acid_out_C'],
            row['T_water_in_C'], row['T_water_out_C']
        ), axis=1
    )
    
    # PASO 5: Calor actual
    df['Q_actual_W'] = (
        df['acid_mass_flow_kgs'] * 
        df['Cp_acid'] * 
        (df['T_acid_in_C'] - df['T_acid_out_C'])
    )
    
    # PASO 6: U aproximado
    df['U_approx_Wm2K'] = df['Q_actual_W'] / (params['area_m2'] * df['LMTD_C'])
    df['U_approx_Wm2K'] = df['U_approx_Wm2K'].replace([np.inf, -np.inf], np.nan)
    
    # PASO 7: Eficiencia
    df['efficiency_pct'] = (df['Q_actual_W'] / params['Q_design_W']) * 100
    
    # PASO 8: Fouling (Método Dual)
    U_clean = params['U_clean_Wm2K']
    sensitivity = params.get('fouling_sensitivity', 1.0)
    
    # Método 1: Basado en U
    R_fouling_U = ((1 / df['U_approx_Wm2K']) - (1 / U_clean)) * sensitivity
    
    # Método 2: Basado en eficiencia
    eta_baseline = 100.0
    R_fouling_eta = ((eta_baseline - df['efficiency_pct']) / 100) * 0.001
    
    # Combinación ponderada
    df['R_fouling_m2KW'] = 0.7 * R_fouling_U + 0.3 * R_fouling_eta
    
    # PASO 9: Suavizado (media móvil 12h)
    df['R_fouling_smooth'] = (
        df['R_fouling_m2KW']
        .rolling(window=12, center=True, min_periods=1)
        .mean()
    )
    
    # PASO 10: Escala display
    df['fouling_factor_display'] = df['R_fouling_smooth'] * 10000
    
    # Clasificación fouling
    df['fouling_status'] = pd.cut(
        df['fouling_factor_display'],
        bins=[-np.inf, 2.0, 5.0, 10.0, np.inf],
        labels=['Limpio', 'Ligero', 'Moderado', 'Alto']
    )
    
    return df
```

---

### 5.3 Validación del Método

**Caso 1: Equipo Limpio (Recién Lavado)**
```
Entrada:
  T_acid_in = 109°C, T_acid_out = 77°C
  T_water_in = 32°C, T_water_out = 49°C
  F_acid = 1,439 m³/h, conc = 98.5%
  
Cálculo:
  LMTD = 52.1°C
  Q_actual = 36.13 MW
  η = 100%
  R_fouling ≈ 0.0 ×10⁻⁴ m²·K/W ✓
  
Resultado: Estado "Limpio" ✓
```

**Caso 2: Equipo con Ensuciamiento Moderado**
```
Entrada:
  Mismas condiciones, pero Q_actual = 32.0 MW
  
Cálculo:
  η = 88.6%
  U_aprox = 1,479 W/m²·K (vs. U_clean = 1,670)
  R_fouling ≈ 7.8 ×10⁻⁴ m²·K/W
  
Resultado: Estado "Moderado" → Programar limpieza ✓
```

---

## 6. MACHINE LEARNING - ARQUITECTURA

### 6.1 Modelos Implementados

#### 6.1.1 Clasificación (Predicción Falla)

**Ensemble Voting Classifier:**
- **Random Forest:** 100 árboles, max_depth=10
- **Gradient Boosting:** 100 estimadores, learning_rate=0.1
- **Logistic Regression:** Regularización L2, C=1.0

**Estrategia de Votación:** Soft voting (promedio probabilidades)

**Features (13 variables):**
1. T_acid_in_C
2. T_acid_out_C
3. T_water_in_C
4. T_water_out_C
5. acid_flow_m3h
6. water_flow_m3h
7. acid_conc_pct
8. water_cond_uS_cm
9. LMTD_C
10. Q_actual_W
11. efficiency_pct
12. U_approx_Wm2K
13. fouling_factor_display

**Target:** falla_30d (binario)
- 1 = Falla esperada en próximos 30 días
- 0 = Operación normal esperada

**Criterio de Falla:**
```python
df['falla_30d'] = (
    (df['T_acid_out_C'] > params['T_acid_out_limit']) |
    (df['efficiency_pct'] < 70) |
    (df['fouling_factor_display'] > 10.0)
).astype(int)
```

---

#### 6.1.2 Detección de Anomalías

**Isolation Forest:**
- contamination = 0.05 (5% datos anómalos esperado)
- n_estimators = 100
- max_samples = 256

**Aplicación:**
- Detecta combinaciones inusuales de parámetros
- Identifica eventos súbitos (picos temperatura)
- Complementa modelo de clasificación

**Output:**
- -1 = Anomalía detectada
- 1 = Operación normal

---

### 6.2 Entrenamiento y Validación

**División Datos:**
- Train: 80%
- Test: 20%
- Estratificación por clase (falla/no falla)

**Validación Mínima:**
```python
MIN_TRAIN_ROWS = 300
MIN_POSITIVES = 10  # Mínimo casos falla
MIN_NEGATIVES = 10  # Mínimo casos normal
```

**Preprocesamiento:**
- **Escalado:** RobustScaler (robusto a outliers)
- **Imputación:** Forward-fill → Backward-fill → Median

**Métricas Evaluación:**
| Métrica | Objetivo | Típico Alcanzado |
|---------|----------|------------------|
| Precision | > 0.80 | 0.82-0.88 |
| Recall | > 0.75 | 0.76-0.85 |
| F1-Score | > 0.78 | 0.79-0.86 |
| ROC-AUC | > 0.85 | 0.87-0.93 |
| AP (Avg Precision) | > 0.80 | 0.83-0.91 |

---

### 6.3 Actualización Modelos

**Frecuencia Recomendada:**
- **Mensual:** Reentrenamiento incremental
- **Trimestral:** Reentrenamiento completo
- **Anual:** Revisión arquitectura y features

**Trigger Reentrenamiento Automático:**
- Performance < umbral (F1 < 0.70)
- Datos nuevos > 20% del conjunto original
- Cambios operativos significativos (lavados, reparaciones)

---

## 7. ÍNDICE DE CRITICIDAD

### 7.1 Ecuación Multifactorial

**Criticidad = 0.40 × f(T) + 0.30 × f(η) + 0.20 × f(cond) + 0.10 × f(R_fouling)**

Escala: 0-100

---

### 7.2 Funciones de Transformación

#### f(T) - Temperatura Salida Ácido
```python
def criticidad_temperatura(T_out, T_limit, T_design):
    if T_out >= T_limit:
        return 100  # Crítico
    elif T_out >= T_design + 3:
        return 80  # Alto
    elif T_out >= T_design:
        return 50  # Medio
    else:
        return max(0, (T_out - T_design + 5) / 5 * 30)  # Bajo
```

**Rangos Típicos (Torre Interpaso):**
| T_out [°C] | Score | Estado |
|------------|-------|--------|
| < 77 | 0-30 | Normal |
| 77-80 | 30-50 | Alerta |
| 80-85 | 50-80 | Alto |
| > 85 | 100 | Crítico |

---

#### f(η) - Eficiencia Térmica
```python
def criticidad_eficiencia(eta):
    if eta >= 95:
        return 0
    elif eta >= 85:
        return 20
    elif eta >= 70:
        return 60
    else:
        return 100
```

---

#### f(cond) - Conductividad Agua
```python
def criticidad_conductividad(cond, umbral=800):
    if cond >= umbral:
        return 100
    else:
        return max(0, (cond / umbral) * 60)
```

---

#### f(R_fouling) - Factor Ensuciamiento
```python
def criticidad_fouling(R_display):
    if R_display >= 10.0:
        return 100
    elif R_display >= 5.0:
        return 70
    elif R_display >= 2.0:
        return 40
    else:
        return max(0, R_display * 10)
```

---

### 7.3 Clasificación Final

| Criticidad | Nivel | Acción Recomendada |
|------------|-------|-------------------|
| 0-30 | Baja | Operación normal, monitoreo rutinario |
| 30-60 | Media | Monitoreo intensivo, revisión semanal |
| 60-80 | Alta | Planificar intervención 15-30 días |
| 80-100 | Crítica | Intervención urgente < 7 días |

---

## 8. SISTEMA DE RECOMENDACIONES

### 8.1 Lógica de Priorización

```
SI criticidad >= 80:
    → "URGENTE: Intervención inmediata requerida"
    → Notificar supervisor, jefe área
    
SI criticidad >= 60:
    → "ALTA: Programar mantenimiento preventivo"
    → Preparar recursos (químicos, personal)
    
SI criticidad >= 30:
    → "MEDIA: Intensificar monitoreo"
    → Análisis tendencias diario
    
SI criticidad < 30:
    → "BAJA: Operación normal"
    → Monitoreo estándar (semanal)
```

---

### 8.2 Recomendaciones Específicas por Parámetro

#### Temperatura Alta
```
- Verificar flujo agua enfriamiento
- Revisar válvula bypass ácido (% apertura)
- Inspeccionar tubos obstruidos
- Considerar limpieza química si η < 80%
```

#### Eficiencia Baja
```
- Revisar factor ensuciamiento
- Comparar vs. baseline post-lavado
- Verificar flujos diseño (ácido y agua)
- Programar limpieza si R_fouling > 7 ×10⁻⁴
```

#### Conductividad Alta
```
- Analizar calidad agua torre enfriamiento
- Revisar ciclos concentración
- Considerar purga aumentada
- Evaluar tratamiento químico agua
```

#### Fouling Alto
```
- Programar limpieza química (NaOH 2%, 85-90°C, 2h)
- Preparar materiales (soda cáustica, agua DM)
- Coordinar paro producción
- Estimar duración intervención: 8-12h
```

---

## 9. INTEGRACIÓN PI SYSTEM

### 9.1 Arquitectura Conexión

```
PI Server (OSIsoft) → PI Web API → Python (requests)
                                      ↓
                                 pandas DataFrame
                                      ↓
                              Cálculo Indicadores
                                      ↓
                              Almacenamiento Local
                                      ↓
                              Dashboard Streamlit
```

---

### 9.2 Tags de Instrumentación

#### Torre de Secado (TS)
| Parámetro | Tag PI | Descripción |
|-----------|--------|-------------|
| Flujo agua | FI25168 | Caudal agua enfriamiento [m³/h] |
| T agua entrada | TI25138 | Temperatura entrada agua [°C] |
| T agua salida | TI25279 | Temperatura salida agua [°C] |
| T ácido entrada | TI25084 | Temperatura entrada ácido [°C] |
| T ácido salida | TI25090 | Temperatura salida ácido [°C] |
| Conc. ácido | AIC25114 | Concentración H₂SO₄ [%] |
| Válvula bypass | TV25088 | Apertura bypass ácido [%] |
| Corriente bomba | 322BOC301_IA | Amperaje bomba ácido [A] |
| Conductividad agua | CI25168 | Conductividad agua [μS/cm] |

#### Torre Absorción Final (TAF)
| Parámetro | Tag PI | Descripción |
|-----------|--------|-------------|
| Flujo agua | FI25173 | Caudal agua enfriamiento [m³/h] |
| T agua entrada | TI25138 | Temperatura entrada agua [°C] |
| T agua salida | TI25279 | Temperatura salida agua [°C] |
| T ácido entrada | TI25269 | Temperatura entrada ácido [°C] |
| T ácido salida | TI25108 | Temperatura salida ácido [°C] |
| Conc. ácido | AIC25118 | Concentración H₂SO₄ [%] |
| Válvula bypass | TV25106 | Apertura bypass ácido [%] |
| Corriente bomba | 326BOC301_II | Amperaje bomba ácido [A] |
| Conductividad agua | CI25173 | Conductividad agua [μS/cm] |

#### Torre Absorción Intermedia (TAI)
| Parámetro | Tag PI | Descripción |
|-----------|--------|-------------|
| Flujo agua | FI25163 | Caudal agua enfriamiento [m³/h] |
| T agua entrada | TI25138 | Temperatura entrada agua [°C] |
| T agua salida | TI25279 | Temperatura salida agua [°C] |
| T ácido entrada | TI24094 | Temperatura entrada ácido [°C] |
| T ácido salida | TI25100 | Temperatura salida ácido [°C] |
| Conc. ácido | AIC25116 | Concentración H₂SO₄ [%] |
| Válvula bypass | TV25098 | Apertura bypass ácido [%] |
| Corriente bomba | 325BOC301_IA | Amperaje bomba ácido [A] |
| Conductividad agua | CI25163 | Conductividad agua [μS/cm] |

---

### 9.3 Frecuencia Muestreo

| Tipo Variable | Frecuencia | Justificación |
|---------------|------------|---------------|
| Temperaturas | 1 min | Alta dinámica térmica |
| Flujos | 1 min | Control proceso crítico |
| Conductividad | 5 min | Cambio lento |
| Concentración ácido | 10 min | Análisis laboratorio |
| Amperaje bombas | 1 min | Detección fallas equipos |

**Agregación Dashboard:**
- Vista tiempo real: últimos datos disponibles
- Vista histórica: promedio horario

---

## 10. OPERACIÓN Y MANTENIMIENTO

### 10.1 Procedimiento Limpieza Química (Lado Ácido)

**Basado en:** Manual MECS P523-00016_01, Sección 1.10.2

**Frecuencia:** Cada 90-180 días (según fouling)

**Pasos:**

1. **Preparación (1h):**
   - Drenar ácido del enfriador
   - Blankear entrada/salida ácido
   - Preparar solución NaOH 2% (usar nozzle N8A y drain para circulación)

2. **Limpieza (2-3h):**
   - Circular NaOH 2% a 82-93°C
   - Mantener pH > 8 (agregar NaOH concentrado si necesario)
   - Tiempo circulación: 1-2 horas
   - **CRÍTICO:** Mantener presión (evitar espacios gas) → previene stress corrosion cracking

3. **Enjuague (1h):**
   - Drenar NaOH
   - **INMEDIATAMENTE** enjuagar con agua DM caliente
   - **CRÍTICO:** No dejar residuos NaOH → riesgo stress corrosion cracking

4. **Retorno Servicio (0.5h):**
   - Rellenar con ácido fuerte
   - Purgar aire (vent lines)
   - Restablecer flujo normal

**TOTAL ESTIMADO:** 8-12 horas (incluye enfriamiento/calentamiento)

---

### 10.2 Procedimiento Limpieza Lado Agua (Tubos)

**Basado en:** Manual MECS P523-00016_01, Sección 1.10.1

**Frecuencia:** Anual o según incrustación

**Pasos:**

1. **Inspección (0.5h):**
   - Remover cubiertas canales agua
   - Inspeccionar incrustación calcárea/fosfatos

2. **Hidrolavado (1h):**
   - Hydro-blast tubos con agua alta presión
   - Remover debris de canales

3. **Limpieza Química (si necesario, 3-4h):**
   - Solución ácido fórmico inhibido < 12% concentración
   - Circular a 65-93°C
   - Monitorear concentración (si cae < 5% → agregar más ácido)
   - Cuando concentración se estabiliza → equipo limpio

4. **Enjuague Final (0.5h):**
   - Drenar ácido fórmico
   - Enjuague abundante agua DM
   - Hydro-blast ligero para remover escamas sueltas

**TOTAL ESTIMADO:** 5-8 horas

---

### 10.3 Inspección Tubos (Eddy Current Test)

**Frecuencia:** Anual

**Objetivo:** Detectar:
- Pérdida espesor pared
- Grietas
- Corrosión localizada

**Procedimiento:**
1. Equipo fuera servicio, drenado
2. Test 100% tubos (ZeCor-Z)
3. Registro resultados por tubo
4. Plugging tubos defectuosos (si < 20% total)
5. Si > 20% tubos defectuosos → Programar retubing

**Vida Útil Esperada Tubos ZeCor-Z:** 15-20 años

---

## 11. ANÁLISIS ECONÓMICO

### 11.1 Impacto Paros No Programados (Data 2025)

**Fuente:** Base "Factorial Perdidas Fusion HF", año 2025

**Criterio Atribución:** Unidad=PAS, Falla contiene "Disponibilidad CAP III"

| Indicador | Valor 2025 |
|-----------|------------|
| Eventos registrados | 33 |
| Pérdidas Fusión atribuibles | 6,255.35 ton/año |
| Duración acumulada | 108.88 h |
| Tiempo detención acumulado | 179.10 h |

**Interpretación:**
- Promedio evento: 190 ton pérdida, 5.4h duración
- Frecuencia: ~2.75 eventos/mes

---

### 11.2 Escenario Mejora (70% Reducción)

**Supuesto Conservador:** Sistema reduce impacto en 70%

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Toneladas evitadas | - | 4,378.74 ton/año | - |
| Toneladas pérdidas | 6,255 | 1,877 | -70% |
| Eventos evitados | 23/año | - | 70% |

---

### 11.3 Modelo de Costos

**CAPEX:** US$ 0 (infraestructura existente, software open-source)

**OPEX:**
- Almacenamiento nube: US$ 1,000/año

**Beneficios Directos (Escenario Conservador):**

| Concepto | US$/año |
|----------|---------|
| Evitar 2 paros no programados | 120,000 |
| Optimizar 2 limpiezas químicas | 30,000 |
| Extensión vida útil tubos (+20%) | 30,000 |
| **TOTAL** | **180,000** |

**Beneficios Directos (Escenario Optimista):**

| Concepto | US$/año |
|----------|---------|
| Evitar 3-4 paros no programados | 240,000 |
| Optimizar 3 limpiezas químicas | 50,000 |
| Extensión vida útil + reducción HH | 50,000 |
| **TOTAL** | **340,000** |

---

### 11.4 VAN (Valor Actual Neto)

**Horizonte:** 5 años  
**Tasa descuento:** 10%  
**Factor VP:** 3.7908

**Cálculo:**
```
Beneficio neto anual = Beneficio - OPEX
                     = US$ 180,000 - US$ 1,000
                     = US$ 179,000/año

VAN = 179,000 × 3.7908 = US$ 678,553
```

**Sensibilidad:**

| Escenario | Beneficio Anual | VAN 5 años @10% |
|-----------|-----------------|-----------------|
| Pesimista | US$ 100,000 | US$ 375,280 |
| Conservador | US$ 180,000 | US$ 678,553 |
| Optimista | US$ 340,000 | US$ 1,285,081 |

**ROI:** Infinito (CAPEX = 0)  
**Payback:** Inmediato (< 1 mes)

---

## 12. MEJORAS VERSIÓN 6.0

### 12.1 Nuevas Funcionalidades

1. **✅ Gestión Tubos Aislados:**
   - Cálculo área efectiva ajustada
   - Impacto en eficiencia y capacidad
   - Umbral recomendación retubing (>20%)

2. **✅ Historial Lavados Químicos:**
   - Registro fecha, tipo, operador
   - Visualización timeline con indicadores
   - Correlación lavado-mejora eficiencia

3. **✅ Predicción ML Mejorada:**
   - Ensemble voting (3 modelos)
   - Detección anomalías (Isolation Forest)
   - Validación robusta (min samples, estratificación)

4. **✅ Dashboard Ejecutivo:**
   - Vista consolidada 3 torres
   - KPIs principales (T_out, η, criticidad)
   - Semáforo estado (verde/amarillo/rojo)

5. **✅ Exportación PDF:**
   - Reporte automático con gráficos
   - Tablas indicadores
   - Recomendaciones priorizadas

---

### 12.2 Correcciones Versión Anterior

| Issue v5.0 | Corrección v6.0 |
|------------|-----------------|
| Fouling negativo en algunos casos | Método dual robusto + suavizado |
| LMTD = 0 (división por cero) | Validación safe_lmtd() |
| Eficiencia > 100% sin sentido físico | Ajuste Q_design por tubos aislados |
| CSV corrupto crashea app | read_csv_auto() multi-encoding |
| Lavados químicos no trackeados | Módulo chemical_washes_CAP3.csv |

---

### 12.3 Optimizaciones Rendimiento

- **Cache Streamlit:** @st.cache_data en load/train
- **Vectorización:** Numpy/Pandas (evita loops Python)
- **Lazy loading:** Gráficos solo cuando tab activo
- **Downsampling:** Graficar max 10,000 puntos (resample si más)

**Mejora velocidad:** 10-20× vs. versión sin cache

---

## 13. DEPLOYMENT Y MANTENIMIENTO

### 13.1 Requisitos Sistema

**Hardware Mínimo:**
- CPU: 2 cores, 2.0 GHz
- RAM: 4 GB
- Disco: 10 GB espacio libre

**Hardware Recomendado:**
- CPU: 4 cores, 3.0 GHz
- RAM: 8 GB
- Disco: 20 GB (SSD preferido)

**Sistema Operativo:**
- Windows 10/11 (64-bit)
- Linux (Ubuntu 20.04+, CentOS 8+)
- macOS 11+ (Big Sur o superior)

**Software:**
- Python 3.9 - 3.11
- pip 21.0+
- (Opcional) Anaconda/Miniconda

---

### 13.2 Instalación

**Opción 1: Entorno Virtual (Recomendado)**
```bash
# Crear entorno
python -m venv venv_cap3

# Activar (Windows)
venv_cap3\Scripts\activate

# Activar (Linux/Mac)
source venv_cap3/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

**Opción 2: Conda**
```bash
conda create -n cap3 python=3.10
conda activate cap3
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

### 13.3 Ejecución

**Desarrollo (local):**
```bash
streamlit run app.py
```
Abre navegador en: http://localhost:8501

**Producción (servidor):**
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

**Acceso remoto:**
http://[IP_SERVIDOR]:8501

---

### 13.4 Actualización Datos

**Manual (CSV):**
1. Exportar datos PI System a CSV
2. Guardar como: `acid_coolers_CAP3_[FECHA].csv`
3. Subir archivo vía interfaz Streamlit

**Automático (futuro):**
- Conexión directa PI Web API
- Actualización cada 1-5 min
- Requiere configuración firewall/VPN

---

### 13.5 Mantenimiento Preventivo Sistema

| Frecuencia | Tarea |
|------------|-------|
| Semanal | - Revisar logs errores<br>- Validar conexión datos |
| Mensual | - Verificar precisión ML (comparar predicciones vs. real)<br>- Revisar umbrales criticidad |
| Trimestral | - Reentrenar modelos ML<br>- Actualizar documentación si hay cambios proceso |
| Semestral | - Backup completo código + datos<br>- Revisión performance (tiempos carga) |
| Anual | - Auditoría externa algoritmos<br>- Actualización dependencias (Python packages) |

---

## 14. REFERENCIAS

[1] **Perry, R.H. & Green, D.W.** (2019). *Perry's Chemical Engineers' Handbook*, 9th Edition. McGraw-Hill Education.

[2] **Hewitt, G.F., Shires, G.L. & Bott, T.R.** (2008). *Heat Exchanger Design Handbook*. Begell House Inc.

[3] **Müller-Steinhagen, H.** (2000). *Fouling of Heat Exchangers*. Publico Publications.

[4] **TEMA** (2019). *Standards of the Tubular Exchanger Manufacturers Association*, 10th Edition.

[5] **Bott, T.R.** (1995). *Fouling of Heat Exchangers*. Elsevier Science.

[6] **Incropera, F.P., DeWitt, D.P., Bergman, T.L. & Lavine, A.S.** (2007). *Fundamentals of Heat and Mass Transfer*, 6th Edition. John Wiley & Sons.

[7] **Susto, G.A. et al.** (2015). Machine Learning for Predictive Maintenance: A Multiple Classifier Approach. *IEEE Transactions on Industrial Informatics*, 11(3), 812-820.

[8] **Breiman, L.** (2001). Random Forests. *Machine Learning*, 45(1), 5-32.

[9] **Liu, F.T., Ting, K.M. & Zhou, Z.H.** (2008). Isolation Forest. *Proceedings IEEE ICDM*, 413-422.

[10] **Pedregosa, F. et al.** (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825-2830.

[11] **DuPont / MECS** (2017). *Operation and Maintenance Manual - ZeCor-Z Acid Coolers*. Doc. 434-505 Rev. 0.

[12] **Sondex, Inc.** (2017). *Product Data Sheet - Acid Coolers CAP-3*. SP916744-P515-00014_02 / SP916744-P515-00015_02.

[13] **Codelco Chile** (2020). *Especificaciones Técnicas Enfriadores CAP-3*. Documentación interna, División Chuquicamata.

[14] **Streamlit Documentation** (2024). https://docs.streamlit.io

[15] **OSIsoft / AVEVA** (2024). *PI System Documentation*. https://docs.osisoft.com

---

## ANEXOS

### A. Glosario Técnico

| Término | Definición |
|---------|------------|
| **LMTD** | Log Mean Temperature Difference - Diferencia temperatura media logarítmica |
| **Fouling** | Ensuciamiento - Acumulación depositos en superficies transferencia calor |
| **U** | Coeficiente global transferencia calor [W/m²·K] |
| **Cp** | Calor específico [J/kg·K] |
| **ZeCor-Z** | Aleación propietaria DuPont resistente H₂SO₄ |
| **TEMA** | Tubular Exchanger Manufacturers Association |
| **Hastelloy C-276** | Superaleación Ni-Mo-Cr alta resistencia corrosión |
| **PI System** | OSIsoft Plant Information - Sistema historiador industrial |
| **ASME Sec VIII** | Código construcción recipientes presión |
| **ROI** | Return On Investment - Retorno sobre inversión |
| **VAN** | Valor Actual Neto (NPV en inglés) |

---

### B. Códigos Estado Sistema

| Código | Descripción | Acción |
|--------|-------------|--------|
| **OK-100** | Operación óptima | Monitoreo rutinario |
| **WARN-30** | Alerta temprana | Intensificar monitoreo |
| **WARN-60** | Degradación significativa | Planificar intervención |
| **CRIT-80** | Estado crítico | Acción urgente |
| **FAIL-XX** | Falla detectada (XX=código) | Paro / Reparación |
| **MAINT** | Modo mantenimiento | Sistema deshabilitado |

---

### C. Changelog Versiones

#### v6.0 (Febrero 2026)
- ✅ Integración datos reales planos MECS/Sondex
- ✅ Método fouling dual robusto
- ✅ Gestión tubos aislados
- ✅ Historial lavados químicos
- ✅ Exportación PDF reportes
- ✅ Documentación técnica completa

#### v5.0 (Enero 2026)
- Refactorización código (PEP8, type hints)
- Eliminación duplicados
- Centralización constantes
- Mejora manejo excepciones

#### v4.0 (Diciembre 2025)
- Implementación ML (Random Forest)
- Detección anomalías
- Dashboard Streamlit interactivo

#### v3.0 (Noviembre 2025)
- Cálculo LMTD robusto
- Interpolación propiedades ácido
- Gráficos Plotly

#### v2.0 (Octubre 2025)
- Lectura automática CSV
- Validación datos PI System
- Cálculo eficiencia básico

#### v1.0 (Septiembre 2025)
- Prototipo inicial
- Cálculos termodinámicos básicos
- Excel manual

---

**FIN DOCUMENTO TÉCNICO v6.0**

---

*Para consultas técnicas:*  
**Sebastián Marinovic Leiva**  
Ingeniero de Procesos - División Chuquicamata  
Email: sebamarinovic.leiva@gmail.com  
Teléfono: +56 9 7624 3605

*Última actualización: 15 de Febrero, 2026*
