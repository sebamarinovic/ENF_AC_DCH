# ============================================================
# Dashboard Enfriadores CAP-3 - VERSIÓN 5.0 (REFACTORIZADO)
# ============================================================
# Mejoras v5.0:
# 1) ✅ Imports organizados y centralizados
# 2) ✅ Eliminación de código duplicado
# 3) ✅ Manejo de excepciones específico
# 4) ✅ Type hints y docstrings completos
# 5) ✅ Constantes centralizadas en dataclasses
# 6) ✅ Funciones más pequeñas y reutilizables
# 7) ✅ Mejor separación de responsabilidades
# ============================================================

from __future__ import annotations

# ===========================================
# IMPORTS - Centralizados
# ===========================================
import io
import os
import warnings
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# ML
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, StandardScaler

# PDF (opcional)
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        Image as RLImage,
        KeepTogether,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

warnings.filterwarnings("ignore")


# ===========================================
# CONFIGURACIÓN Y CONSTANTES
# ===========================================
@dataclass(frozen=True)
class AppConfig:
    """Configuración global de la aplicación."""
    PAGE_TITLE: str = "Dashboard Enfriadores CAP-3 v5.0"
    PAGE_ICON: str = "❄️"
    DATA_FILE: str = "acid_coolers_CAP3_synthetic_2years.csv"
    WASH_FILE: str = "chemical_washes_CAP3.csv"
    LOGO_PATH: str = r"C:\Users\sebam\OneDrive\Desktop\PAS_DCH\control de proceso\ENF_AC\logo_codelco.png"
    FALLBACK_WINDOW_DAYS: int = 30
    PRED_HORIZON_DAYS: int = 30
    MIN_TRAIN_ROWS: int = 300
    MIN_POSITIVES: int = 10
    MIN_NEGATIVES: int = 10


COLORS = {
    'primary': '#1f77b4', 'secondary': '#ff7f0e', 'success': '#2ca02c',
    'warning': '#ffbb33', 'danger': '#dc3545', 'info': '#17a2b8',
    'acid': '#e74c3c', 'water': '#3498db', 'reference': '#95a5a6'
}

# Mapeo de tags de instrumentación
ENGINEERING_MAP = {
    "TS": {
        "F_w": "FI25168", "T_w_in": "TI25138", "T_w_out": "TI25279",
        "T_a_in": "TI25084", "T_a_out": "TI25090", "acid_conc": "AIC25114",
        "bypass": "TV25088", "pump_amp": "322BOC301_IA", "cond_w": "CI25168",
    },
    "TAF": {
        "F_w": "FI25173", "T_w_in": "TI25138", "T_w_out": "TI25279",
        "T_a_in": "TI25269", "T_a_out": "TI25108", "acid_conc": "AIC25118",
        "bypass": "TV25106", "pump_amp": "326BOC301_II", "cond_w": "CI25173",
    },
    "TAI": {
        "F_w": "FI25163", "T_w_in": "TI25138", "T_w_out": "TI25279",
        "T_a_in": "TI24094", "T_a_out": "TI25100", "acid_conc": "AIC25116",
        "bypass": "TV25098", "pump_amp": "325BOC301_IA", "cond_w": "CI25163",
    },
}

WASH_NAME_MAP = {
    "Secado": "TS", "Absorcion Intermedia": "TAI", "Absorcion Final": "TAF",
    "TS": "TS", "TAI": "TAI", "TAF": "TAF",
    "ENF TS": "TS", "ENF TAI": "TAI", "ENF TAF": "TAF",
    "Torre Secado": "TS", "Torre Interpaso": "TAI", "Torre Final": "TAF",
}

WASH_KEY_TO_NAME = {"TS": "Secado", "TAI": "Absorcion Intermedia", "TAF": "Absorcion Final"}

DESIGN_PARAMS = {
    "TS": {
        "name": "Torre de Secado (5322-ENF-301/401)", "short_name": "Torre Secado",
        "area_m2": 366.87, "U_clean_Wm2K": 1718, "Q_design_W": 15.39e6,
        "acid_conc_design": 96.0, "T_acid_in_design": 75.0, "T_acid_out_design": 55.0,
        "T_acid_out_limit": 60.0, "T_water_in_design": 32.0, "T_water_out_design": 49.0,
        "LMTD_design": 24.4, "fouling_design_m2KW": 1.43e-4,
        "acid_flow_design_m3h": 966, "water_flow_design_m3h": 776,
        "T_acid_in_min": 50.0, "T_acid_in_max": 95.0,
        "T_acid_out_min": 40.0, "T_acid_out_max": 75.0,
    },
    "TAI": {
        "name": "Torre Interpaso (5325-ENF-301/401)", "short_name": "Torre Interpaso",
        "area_m2": 415.26, "U_clean_Wm2K": 1670, "Q_design_W": 36.13e6,
        "acid_conc_design": 98.5, "T_acid_in_design": 109.0, "T_acid_out_design": 77.0,
        "T_acid_out_limit": 85.0, "T_water_in_design": 32.0, "T_water_out_design": 49.0,
        "LMTD_design": 52.1, "fouling_design_m2KW": 1.43e-4,
        "acid_flow_design_m3h": 1439, "water_flow_design_m3h": 1823,
        "T_acid_in_min": 70.0, "T_acid_in_max": 130.0,
        "T_acid_out_min": 60.0, "T_acid_out_max": 100.0,
    },
    "TAF": {
        "name": "Torre Final (5326-ENF-301/401)", "short_name": "Torre Final",
        "area_m2": 92.98, "U_clean_Wm2K": 2070, "Q_design_W": 8.36e6,
        "acid_conc_design": 98.5, "T_acid_in_design": 91.0, "T_acid_out_design": 77.0,
        "T_acid_out_limit": 82.0, "T_water_in_design": 32.0, "T_water_out_design": 49.0,
        "LMTD_design": 43.4, "fouling_design_m2KW": 1.43e-4,
        "acid_flow_design_m3h": 756, "water_flow_design_m3h": 422,
        "T_acid_in_min": 65.0, "T_acid_in_max": 120.0,
        "T_acid_out_min": 55.0, "T_acid_out_max": 95.0,
    },
}

# Propiedades del ácido: concentración -> (Cp J/kg·K, densidad kg/m³)
ACID_PROPS = {
    0: (4186, 998), 50: (3180, 1395), 70: (2470, 1610), 80: (2100, 1727),
    90: (1760, 1814), 93: (1680, 1830), 96: (1560, 1836), 98: (1430, 1836),
    98.5: (1400, 1835), 100: (1340, 1830),
}


# ===========================================
# FUNCIONES AUXILIARES
# ===========================================
def fmt(value: Any, template: str = "{:.2f}", na: str = "N/D") -> str:
    """Formatea un valor numérico de forma segura."""
    if value is None or (isinstance(value, float) and np.isnan(value)) or pd.isna(value):
        return na
    try:
        return template.format(float(value))
    except (ValueError, TypeError):
        return na


def to_numeric(series: pd.Series) -> pd.Series:
    """Convierte una serie a numérico, limpiando valores inválidos."""
    cleaned = series.astype(str).replace(
        to_replace=[r'(?i)bad\s*input', r'(?i)error', r'(?i)nan', r'^-$', r'^\s*$'],
        value=np.nan, regex=True
    )
    return pd.to_numeric(cleaned.str.replace(",", ".", regex=False), errors="coerce")


def get_acid_properties(conc_pct: float) -> Tuple[float, float]:
    """Obtiene Cp y densidad del ácido por interpolación."""
    if pd.isna(conc_pct):
        return np.nan, np.nan
    concs = sorted(ACID_PROPS.keys())
    cps = [ACID_PROPS[c][0] for c in concs]
    rhos = [ACID_PROPS[c][1] for c in concs]
    return float(np.interp(conc_pct, concs, cps)), float(np.interp(conc_pct, concs, rhos))


def safe_lmtd(T_hot_in: float, T_hot_out: float, T_cold_in: float, T_cold_out: float) -> float:
    """Calcula LMTD de forma segura."""
    dT1 = T_hot_in - T_cold_out
    dT2 = T_hot_out - T_cold_in
    if np.isnan(dT1) or np.isnan(dT2) or dT1 <= 0 or dT2 <= 0:
        return np.nan
    if abs(dT1 - dT2) < 1e-6:
        return float(dT1)
    return float((dT1 - dT2) / np.log(dT1 / dT2))


# ===========================================
# CARGA DE DATOS
# ===========================================
def read_csv_auto(path: str) -> pd.DataFrame:
    """Lee CSV probando diferentes encodings y separadores."""
    if not os.path.exists(path):
        return pd.DataFrame()
    
    encodings = ["utf-8-sig", "utf-8", "cp1252", "latin1"]
    seps = [";", ",", "\t"]
    best_df, best_cols = None, 0
    
    for enc in encodings:
        for sep in seps:
            try:
                df = pd.read_csv(path, encoding=enc, sep=sep, engine="python", on_bad_lines="skip")
                df.columns = [str(c).strip().replace("\ufeff", "") for c in df.columns]
                if df.shape[1] > best_cols:
                    best_cols, best_df = df.shape[1], df
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
    
    if best_df is not None and best_df.columns.duplicated().any():
        best_df = best_df.loc[:, ~best_df.columns.duplicated()].copy()
    return best_df if best_df is not None else pd.DataFrame()


def find_timestamp_col(df: pd.DataFrame) -> str:
    """Encuentra la columna de timestamp."""
    for c in df.columns:
        nc = str(c).strip().lower().replace(" ", "").replace("_", "")
        if nc in ["timestamp", "datetime", "fechahora"]:
            return c
    return df.columns[0]


def load_washes(path: str) -> pd.DataFrame:
    """Carga historial de lavados."""
    empty = pd.DataFrame(columns=["wash_ts", "enfriador", "enfriador_key", "tipo", "comentario", "usuario"])
    if not os.path.exists(path):
        return empty
    
    try:
        df = pd.read_csv(path, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(path, encoding='latin1')
        except Exception:
            return empty
    
    if df.empty:
        return empty
    
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Mapear columnas
    rename = {}
    for c in df.columns:
        if ('wash' in c and 'ts' in c) or c in ['fecha', 'date', 'timestamp', 'datetime', 'fechahora']:
            rename[c] = 'wash_ts'
        elif c in ['equipo', 'cooler', 'enfriador']:
            rename[c] = 'enfriador'
    df = df.rename(columns=rename)
    
    df['wash_ts'] = pd.to_datetime(df['wash_ts'], errors='coerce', dayfirst=True)
    df = df.dropna(subset=['wash_ts'])
    df['enfriador'] = df.get('enfriador', '').astype(str)
    df['enfriador_key'] = df['enfriador'].map(lambda x: WASH_NAME_MAP.get(str(x).strip()))
    
    for c in ["tipo", "comentario", "usuario"]:
        if c not in df.columns:
            df[c] = ""
    
    return df[["wash_ts", "enfriador", "enfriador_key", "tipo", "comentario", "usuario"]].sort_values('wash_ts')


def save_wash(path: str, wash_date: datetime, enf_key: str, tipo: str, comentario: str, usuario: str) -> bool:
    """Guarda un nuevo lavado."""
    new_row = pd.DataFrame([{
        'wash_ts': wash_date.strftime('%Y-%m-%d %H:%M:%S'),
        'enfriador': WASH_KEY_TO_NAME.get(enf_key, enf_key),
        'tipo': tipo, 'comentario': comentario, 'usuario': usuario
    }])
    
    try:
        if os.path.exists(path):
            df = pd.read_csv(path, encoding='utf-8')
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            df = new_row
        df.to_csv(path, index=False, encoding='utf-8')
        return True
    except Exception:
        return False


# ===========================================
# TRANSFORMACIÓN DE DATOS
# ===========================================
def explode_wide_to_long(df_wide: pd.DataFrame, ts_col: str) -> pd.DataFrame:
    """Transforma datos de formato ancho a largo."""
    frames = []
    for key, tags in ENGINEERING_MAP.items():
        df_e = pd.DataFrame({ts_col: df_wide[ts_col]})
        df_e["Enfriador"] = f"ENF {key}"
        df_e["Enfriador_Key"] = key
        
        for col, tag in [("F_w", "F_w"), ("T_w_in", "T_w_in"), ("T_w_out", "T_w_out"),
                         ("T_a_in", "T_a_in"), ("T_a_out", "T_a_out"), ("acid_conc", "acid_conc"),
                         ("bypass", "bypass"), ("pump_amp", "pump_amp"), ("cond_w", "cond_w")]:
            df_e[col] = to_numeric(df_wide[tags[tag]]) if tags[tag] in df_wide.columns else np.nan
        
        if "HIC25020" in df_wide.columns:
            df_e["blower_speed"] = to_numeric(df_wide["HIC25020"])
        frames.append(df_e)
    
    return pd.concat(frames, ignore_index=True)


def filter_operation(df: pd.DataFrame, enf_key: str, min_blower: float = 50.0, min_flow_pct: float = 30.0) -> pd.DataFrame:
    """Filtra datos a operación normal."""
    if enf_key not in DESIGN_PARAMS:
        df = df.copy()
        df["en_operacion"] = 0
        return df
    
    dsg = DESIGN_PARAMS[enf_key]
    out = df.copy()
    
    mask = (
        (out["T_a_in"] >= dsg["T_acid_in_min"]) & (out["T_a_in"] <= dsg["T_acid_in_max"]) &
        (out["T_a_out"] >= dsg["T_acid_out_min"]) & (out["T_a_out"] <= dsg["T_acid_out_max"]) &
        (out["F_w"] >= dsg["water_flow_design_m3h"] * min_flow_pct / 100) &
        ((out["T_a_in"] - out["T_a_out"]) > 0.5) &
        (out["T_w_in"] >= 15) & (out["T_w_in"] <= 50) &
        (out["T_w_out"] > out["T_w_in"])
    )
    
    if "blower_speed" in out.columns:
        mask &= out["blower_speed"] >= min_blower
    
    out["en_operacion"] = mask.astype(int)
    return out


def apply_thermal_model(df: pd.DataFrame, ts_col: str, enf_key: str) -> pd.DataFrame:
    """Aplica modelo térmico."""
    if enf_key not in DESIGN_PARAMS:
        return df
    
    dsg = DESIGN_PARAMS[enf_key]
    out = df.copy().sort_values(ts_col)
    
    # Propiedades agua
    rho_w, cp_w = 1000.0, 4186.0
    out["F_w_kgs"] = (out["F_w"] / 3600.0) * rho_w
    
    # Propiedades ácido
    props = [get_acid_properties(c) for c in out["acid_conc"].values]
    out["cp_acid"] = [p[0] for p in props]
    out["rho_acid"] = [p[1] for p in props]
    
    # Calor
    out["Q_water_W"] = out["F_w_kgs"] * cp_w * (out["T_w_out"] - out["T_w_in"])
    dTa = (out["T_a_in"] - out["T_a_out"]).replace(0, np.nan)
    out["dT_acid"] = dTa
    out["m_acid_est"] = (out["Q_water_W"] / (out["cp_acid"] * dTa)).replace([np.inf, -np.inf], np.nan)
    out["Q_acid_est"] = out["m_acid_est"] * out["cp_acid"] * dTa
    out["Q_used_W"] = np.minimum(out["Q_water_W"].abs(), out["Q_acid_est"].abs())
    
    # LMTD y U
    out["LMTD_K"] = [safe_lmtd(ai, ao, wi, wo) for ai, ao, wi, wo in 
                     zip(out["T_a_in"], out["T_a_out"], out["T_w_in"], out["T_w_out"])]
    out["UA_WK"] = out["Q_used_W"] / out["LMTD_K"]
    out["U_Wm2K"] = out["UA_WK"] / dsg["area_m2"]
    
    # Rf
    U_clean = dsg["U_clean_Wm2K"]
    out["Rf_m2K_W"] = np.where(
        (out["en_operacion"] == 1) & (out["U_Wm2K"] > 0) & (out["U_Wm2K"] < U_clean * 1.5),
        (1.0 / out["U_Wm2K"]) - (1.0 / U_clean), np.nan
    )
    out["Rf_x1e4"] = (out["Rf_m2K_W"] * 1e4).clip(lower=-0.5)
    
    # Eficiencias
    out["eff_Q_pct"] = (out["Q_used_W"] / dsg["Q_design_W"]) * 100
    out["eff_U_pct"] = (out["U_Wm2K"] / U_clean) * 100
    
    return out


def add_wash_features(df: pd.DataFrame, washes: pd.DataFrame, ts_col: str, enf_key: str) -> pd.DataFrame:
    """Agrega features de lavados."""
    out = df.copy()
    
    if washes is None or washes.empty:
        out["days_since_wash"] = np.nan
        out["wash_in_last_30d"] = 0
        return out
    
    w = washes[washes["enfriador_key"] == enf_key]
    if w.empty:
        out["days_since_wash"] = np.nan
        out["wash_in_last_30d"] = 0
        return out
    
    last_wash = pd.to_datetime(w["wash_ts"]).max()
    out["days_since_wash"] = (out[ts_col] - last_wash).dt.total_seconds() / 86400
    out["wash_in_last_30d"] = (out["days_since_wash"] <= 30).astype(int)
    return out


def calculate_criticidad(df: pd.DataFrame, enf_key: str) -> pd.DataFrame:
    """Calcula índice de criticidad."""
    if enf_key not in DESIGN_PARAMS:
        return df
    
    dsg = DESIGN_PARAMS[enf_key]
    out = df.copy()
    mask_op = out["en_operacion"] == 1
    
    T_limit = dsg["T_acid_out_limit"]
    Rf_crit = dsg["fouling_design_m2KW"] * 1e4 * 5
    
    out["crit_temp"] = np.where(mask_op, (out["T_a_out"] / T_limit).clip(0, 1.5), np.nan)
    out["crit_fouling"] = np.where(mask_op & out["Rf_x1e4"].notna(), (out["Rf_x1e4"] / Rf_crit).clip(0, 1.5), np.nan)
    out["crit_eff"] = np.where(mask_op, (1 - out["eff_U_pct"] / 100).clip(0, 1), np.nan)
    out["crit_wash"] = np.where(out["days_since_wash"].notna(), (out["days_since_wash"] / 180).clip(0, 1.5), 0.5)
    
    out["criticidad"] = np.where(
        mask_op,
        100 * (0.30 * out["crit_temp"].fillna(0) + 0.35 * out["crit_fouling"].fillna(0) +
               0.25 * out["crit_eff"].fillna(0) + 0.10 * out["crit_wash"].fillna(0)),
        np.nan
    ).clip(0, 120)
    
    def clasificar(v):
        if pd.isna(v): return "N/D"
        if v < 30: return "Baja"
        if v < 60: return "Media"
        if v < 80: return "Alta"
        return "Crítica"
    
    out["nivel_criticidad"] = out["criticidad"].apply(clasificar)
    return out


def add_rolling_features(df_op: pd.DataFrame, ts_col: str, window_days: int = 7, enf_key: str = None) -> pd.DataFrame:
    """Agrega features rolling."""
    out = df_op.copy().sort_values(ts_col)
    if out.empty:
        return out
    
    n = max(24, window_days * 24)
    min_p = max(12, n // 4)
    
    out["T_out_ma"] = out["T_a_out"].rolling(n, min_periods=min_p).mean()
    out["Rf_ma"] = out["Rf_x1e4"].rolling(n, min_periods=min_p).mean()
    out["U_ma"] = out["U_Wm2K"].rolling(n, min_periods=min_p).mean()
    out["T_out_p95_7d"] = out["T_a_out"].rolling(n, min_periods=min_p).quantile(0.95)
    
    def slope(s):
        v = np.array(s.values, dtype=float)
        if np.any(~np.isfinite(v)):
            return np.nan
        return np.polyfit(np.arange(len(v)), v, 1)[0]
    
    out["Rf_slope"] = out["Rf_x1e4"].rolling(n, min_periods=min_p).apply(slope, raw=False)
    
    out["Rf_days_to_crit_est"] = np.nan
    if enf_key and enf_key in DESIGN_PARAMS:
        Rf_crit = DESIGN_PARAMS[enf_key]["fouling_design_m2KW"] * 1e4 * 5
        mask = out["Rf_slope"].notna() & (out["Rf_slope"] > 1e-6) & out["Rf_ma"].notna()
        over = out["Rf_ma"] >= Rf_crit
        out.loc[over, "Rf_days_to_crit_est"] = 0.0
        mask = mask & (~over)
        out.loc[mask, "Rf_days_to_crit_est"] = ((Rf_crit - out.loc[mask, "Rf_ma"]) / out.loc[mask, "Rf_slope"] / 24).clip(0, 365)
    
    return out


# ===========================================
# ESTADÍSTICAS DE VENTANA
# ===========================================
def window_stats(df_op: pd.DataFrame, dsg: dict) -> Dict[str, float]:
    """Calcula estadísticas de una ventana de datos."""
    if df_op is None or df_op.empty:
        return {}
    
    stats = {}
    
    if "T_a_out" in df_op:
        stats["T_out_mean"] = float(df_op["T_a_out"].mean())
        stats["T_out_p95"] = float(df_op["T_a_out"].quantile(0.95))
        stats["T_out_max"] = float(df_op["T_a_out"].max())
        stats["T_out_last"] = float(df_op["T_a_out"].iloc[-1])
    
    if "U_Wm2K" in df_op:
        stats["U_mean"] = float(df_op["U_Wm2K"].mean())
        stats["U_last"] = float(df_op["U_Wm2K"].iloc[-1])
        U_clean = float(dsg.get("U_clean_Wm2K", np.nan))
        stats["U_clean"] = U_clean
        stats["U_mean_pct"] = 100 * stats["U_mean"] / U_clean if U_clean > 0 else np.nan
    
    if "Rf_x1e4" in df_op:
        stats["Rf_mean"] = float(df_op["Rf_x1e4"].mean())
        stats["Rf_p95"] = float(df_op["Rf_x1e4"].quantile(0.95))
        stats["Rf_last"] = float(df_op["Rf_x1e4"].iloc[-1])
    
    if "Q_used_W" in df_op:
        stats["Q_mean_MW"] = float(df_op["Q_used_W"].mean() / 1e6)
        stats["Q_last_MW"] = float(df_op["Q_used_W"].iloc[-1] / 1e6)
        Q_des = float(dsg.get("Q_design_W", np.nan)) / 1e6
        stats["Q_design_MW"] = Q_des
        stats["Q_mean_pct"] = 100 * stats["Q_mean_MW"] / Q_des if Q_des > 0 else np.nan
    
    if "criticidad" in df_op:
        stats["crit_mean"] = float(df_op["criticidad"].mean())
        stats["crit_last"] = float(df_op["criticidad"].iloc[-1]) if pd.notna(df_op["criticidad"].iloc[-1]) else np.nan
    
    if "days_since_wash" in df_op:
        last = df_op["days_since_wash"].iloc[-1]
        stats["days_since_wash_last"] = float(last) if pd.notna(last) else np.nan
    
    return stats


# ===========================================
# INTERPRETACIONES
# ===========================================
def get_thermal_interpretation(df_op: pd.DataFrame, enf_key: str) -> Dict[str, Any]:
    """Genera interpretación térmica."""
    dsg = DESIGN_PARAMS.get(enf_key, {})
    if df_op is None or df_op.empty:
        return {"status": "error", "items": ["Sin datos en operación."]}
    
    stt = window_stats(df_op, dsg)
    T_limit = float(dsg.get("T_acid_out_limit", 85))
    items = []
    status = "normal"
    
    Tp = stt.get("T_out_p95", np.nan)
    Tm = stt.get("T_out_mean", np.nan)
    
    if pd.notna(Tp):
        if Tp >= T_limit:
            items.append(f"⚠️ **ALERTA**: P95 T salida = **{Tp:.1f}°C** excede límite **{T_limit:.0f}°C**.")
            items.append("➡️ Acción: priorizar revisión y evaluar limpieza.")
            status = "critical"
        elif Tp >= 0.97 * T_limit:
            items.append(f"🟡 P95 T salida = **{Tp:.1f}°C** cercana al límite.")
            status = "warning"
        else:
            items.append(f"✅ T salida promedio = **{Tm:.1f}°C**, P95 = **{Tp:.1f}°C** (OK).")
    
    Qm = stt.get("Q_mean_MW", np.nan)
    Qp = stt.get("Q_mean_pct", np.nan)
    if pd.notna(Qm) and pd.notna(Qp):
        if Qp > 120:
            items.append(f"📈 Carga térmica alta: **{Qm:.2f} MW** ({Qp:.0f}% diseño).")
        elif Qp < 50:
            items.append(f"📉 Carga térmica baja: **{Qm:.2f} MW** ({Qp:.0f}% diseño).")
        else:
            items.append(f"✅ Carga térmica: **{Qm:.2f} MW** ({Qp:.0f}% diseño).")
    
    return {"status": status, "items": items}


def get_fouling_interpretation(df_op: pd.DataFrame, enf_key: str) -> Dict[str, Any]:
    """Genera interpretación de ensuciamiento."""
    dsg = DESIGN_PARAMS.get(enf_key, {})
    if df_op is None or df_op.empty:
        return {"status": "error", "items": ["Sin datos en operación."]}
    
    stt = window_stats(df_op, dsg)
    Rf_design = float(dsg.get("fouling_design_m2KW", 1.43e-4)) * 1e4
    items = []
    status = "normal"
    
    Rf_p = stt.get("Rf_p95", np.nan)
    Rf_m = stt.get("Rf_mean", np.nan)
    
    if pd.notna(Rf_p):
        if Rf_p >= 5 * Rf_design:
            items.append(f"🔴 **CRÍTICO**: P95 Rf = **{Rf_p:.2f}×10⁻⁴** ≥ 5x diseño.")
            items.append("➡️ Limpieza prioritaria.")
            status = "critical"
        elif Rf_p >= 3 * Rf_design:
            items.append(f"🟠 **ALTO**: P95 Rf = **{Rf_p:.2f}×10⁻⁴** ≥ 3x diseño.")
            items.append("➡️ Programar limpieza.")
            status = "warning"
        else:
            items.append(f"✅ Rf promedio = **{Rf_m:.2f}×10⁻⁴**, P95 = **{Rf_p:.2f}×10⁻⁴** (OK).")
    
    U_m = stt.get("U_mean", np.nan)
    U_pct = stt.get("U_mean_pct", np.nan)
    if pd.notna(U_m) and pd.notna(U_pct):
        if U_pct < 60:
            items.append(f"⚠️ **U muy bajo**: {U_m:.0f} W/m²K ({U_pct:.0f}% limpio).")
        elif U_pct < 80:
            items.append(f"🟡 **U reducido**: {U_m:.0f} W/m²K ({U_pct:.0f}% limpio).")
        else:
            items.append(f"✅ U promedio: {U_m:.0f} W/m²K ({U_pct:.0f}% limpio).")
    
    return {"status": status, "items": items}


def get_criticidad_interpretation(df_op: pd.DataFrame, enf_key: str) -> Dict[str, Any]:
    """Genera interpretación de criticidad."""
    if df_op is None or df_op.empty:
        return {"status": "error", "items": ["Sin datos."], "recs": []}
    
    dsg = DESIGN_PARAMS.get(enf_key, {})
    stt = window_stats(df_op, dsg)
    crit_m = stt.get("crit_mean", np.nan)
    days = stt.get("days_since_wash_last", np.nan)
    
    items, recs = [], []
    
    if pd.notna(crit_m):
        if crit_m >= 80:
            status = "critical"
            items.append(f"🔴 **CRITICIDAD ALTA**: **{crit_m:.0f}/100**.")
            recs = ["• Limpieza química en 48-72h", "• Revisar bypass/carga térmica", "• Incrementar flujo agua"]
        elif crit_m >= 60:
            status = "warning"
            items.append(f"🟠 **CRITICIDAD MEDIA-ALTA**: **{crit_m:.0f}/100**.")
            recs = ["• Planificar limpieza (1-2 semanas)", "• Monitorear tendencia diaria"]
        elif crit_m >= 30:
            status = "attention"
            items.append(f"🟡 **CRITICIDAD MEDIA**: **{crit_m:.0f}/100**.")
            recs = ["• Incluir en mantenimiento programado"]
        else:
            status = "normal"
            items.append(f"🟢 **CRITICIDAD BAJA**: **{crit_m:.0f}/100**.")
            recs = ["• Monitoreo rutinario"]
    else:
        status = "unknown"
        items.append("⚪ Sin datos suficientes.")
    
    items.append(f"⏰ Días desde lavado: **{fmt(days, '{:.0f}', 'Sin registro')}**")
    
    return {"status": status, "items": items, "recs": recs}


# ===========================================
# SCORE OPERACIONAL Y DECISIÓN
# ===========================================
def rf_trend_to_critical(df_op: pd.DataFrame, enf_key: str, ts_col: str, lookback: int = 30) -> Tuple[Optional[float], Optional[float], str]:
    """Calcula tendencia de Rf hacia crítico."""
    if df_op is None or df_op.empty or "Rf_x1e4" not in df_op.columns:
        return None, None, "sin_datos"
    
    dsg = DESIGN_PARAMS.get(enf_key, {})
    Rf_crit = float(dsg.get("fouling_design_m2KW", 1.43e-4)) * 1e4 * 5
    
    d = df_op.dropna(subset=["Rf_x1e4", ts_col]).copy().sort_values(ts_col)
    if d.empty:
        return None, None, "sin_datos"
    
    cutoff = d[ts_col].max() - pd.Timedelta(days=lookback)
    d = d[d[ts_col] >= cutoff]
    if len(d) < 24:
        return None, None, "pocos_datos"
    
    rf = d["Rf_x1e4"].values.astype(float)
    slope, _ = np.polyfit(np.arange(len(rf)), rf, 1)
    current = float(rf[-1])
    
    if slope <= 1e-6:
        return float(slope), None, "estable"
    if current >= Rf_crit:
        return float(slope), 0.0, "empeora"
    
    days = max(0.0, (Rf_crit - current) / slope / 24)
    return float(slope), float(days), "empeora"


def operational_score(df_op: pd.DataFrame, enf_key: str, ts_col: str) -> Tuple[float, List[str]]:
    """Calcula score operacional (0-1)."""
    if df_op is None or df_op.empty:
        return 0.0, ["Sin datos."]
    
    dsg = DESIGN_PARAMS.get(enf_key, {})
    stt = window_stats(df_op, dsg)
    
    T_limit = float(dsg.get("T_acid_out_limit", 85))
    Rf_design = float(dsg.get("fouling_design_m2KW", 1.43e-4)) * 1e4
    Rf_crit = 5 * Rf_design
    
    T_p95 = stt.get("T_out_p95", np.nan)
    Rf_p95 = stt.get("Rf_p95", np.nan)
    crit_m = stt.get("crit_mean", np.nan)
    
    # Componentes 0-1
    temp_s = float(np.clip((T_p95 - 0.95 * T_limit) / (0.05 * T_limit), 0, 1)) if pd.notna(T_p95) else 0
    foul_s = float(np.clip((Rf_p95 - 1.2 * Rf_design) / (Rf_crit - 1.2 * Rf_design + 1e-9), 0, 1)) if pd.notna(Rf_p95) else 0
    crit_s = float(np.clip((crit_m - 30) / 50, 0, 1)) if pd.notna(crit_m) else 0
    
    _, days_to_crit, _ = rf_trend_to_critical(df_op, enf_key, ts_col)
    trend_s = float(np.clip((30 - days_to_crit) / 30, 0, 1)) if days_to_crit is not None else 0
    
    score = float(np.clip(0.35 * temp_s + 0.35 * foul_s + 0.20 * crit_s + 0.10 * trend_s, 0, 1))
    
    notes = [
        f"T_p95: {fmt(T_p95, '{:.1f}')}°C / límite {T_limit:.0f}°C",
        f"Rf_p95: {fmt(Rf_p95, '{:.2f}')}×10⁻⁴",
        f"Criticidad: {fmt(crit_m, '{:.0f}')}/100",
        f"Días a crítico: {fmt(days_to_crit, '{:.0f}', 'N/A')}"
    ]
    return score, notes


def requires_wash(df_op: pd.DataFrame, enf_key: str, ts_col: str) -> Tuple[bool, str]:
    """Determina si requiere lavado."""
    if df_op is None or df_op.empty:
        return False, "Sin datos."
    
    dsg = DESIGN_PARAMS.get(enf_key, {})
    stt = window_stats(df_op, dsg)
    
    T_limit = float(dsg.get("T_acid_out_limit", 85))
    Rf_crit = float(dsg.get("fouling_design_m2KW", 1.43e-4)) * 1e4 * 5
    
    triggers = []
    if pd.notna(stt.get("T_out_p95")) and stt["T_out_p95"] >= T_limit:
        triggers.append("P95 T excede límite")
    if pd.notna(stt.get("Rf_p95")) and stt["Rf_p95"] >= Rf_crit:
        triggers.append("P95 Rf ≥ crítico")
    
    _, days, _ = rf_trend_to_critical(df_op, enf_key, ts_col)
    if days is not None and days <= 14:
        triggers.append("Tendencia Rf < 14d")
    if pd.notna(stt.get("crit_mean")) and stt["crit_mean"] >= 80:
        triggers.append("Criticidad ≥ 80")
    
    if triggers:
        return True, " | ".join(triggers)
    return False, "Sin gatillos críticos."


# ===========================================
# ML
# ===========================================
def build_event_label(df_op: pd.DataFrame, washes: pd.DataFrame, ts_col: str, horizon: int = 30) -> pd.DataFrame:
    """Crea etiqueta de evento (lavado futuro)."""
    if df_op is None or df_op.empty:
        return df_op.assign(y=np.nan)
    
    out = df_op.copy().sort_values(ts_col)
    
    if washes is None or washes.empty:
        out["y"] = 0
        return out
    
    w = washes.copy()
    w["wash_ts"] = pd.to_datetime(w["wash_ts"], errors="coerce")
    w = w.dropna(subset=["wash_ts"]).sort_values("wash_ts")
    
    y = []
    for ts in out[ts_col].values:
        ts = pd.Timestamp(ts)
        future = bool(((w["wash_ts"] > ts) & (w["wash_ts"] <= ts + pd.Timedelta(days=horizon))).any())
        y.append(1 if future else 0)
    
    out["y"] = np.array(y, dtype=int)
    return out


def get_ml_features(df: pd.DataFrame) -> List[str]:
    """Obtiene lista de features para ML."""
    base = ["T_out_ma", "T_out_p95_7d", "Rf_ma", "Rf_slope", "Rf_days_to_crit_est",
            "U_ma", "Q_used_W", "LMTD_K", "dT_acid", "F_w", "eff_U_pct", 
            "Rf_x1e4", "T_a_out", "days_since_wash"]
    return [c for c in base if c in df.columns]


def prep_ml_data(df: pd.DataFrame, features: List[str]) -> Tuple[pd.DataFrame, pd.Series]:
    """Prepara datos para ML."""
    d = df.copy()
    if "days_since_wash" in d.columns:
        d["days_since_wash"] = d["days_since_wash"].clip(lower=0, upper=365)
    
    X = d[features].replace([np.inf, -np.inf], np.nan)
    y = d["y"]
    
    mask = X.notna().all(axis=1) & y.notna()
    return X.loc[mask].copy(), y.loc[mask].astype(int).copy()


def can_train(y: pd.Series, config: AppConfig) -> Tuple[bool, str]:
    """Verifica si se puede entrenar."""
    if y is None or len(y) == 0:
        return False, "Sin datos."
    
    classes = sorted(list(y.dropna().unique()))
    if len(classes) < 2:
        return False, f"Solo una clase: {classes}."
    
    c = y.value_counts()
    pos, neg = int(c.get(1, 0)), int(c.get(0, 0))
    
    if pos < config.MIN_POSITIVES or neg < config.MIN_NEGATIVES:
        return False, f"Insuficientes (pos={pos}, neg={neg})."
    if len(y) < config.MIN_TRAIN_ROWS:
        return False, f"Insuficientes filas ({len(y)})."
    
    return True, "OK"


def train_models(X: pd.DataFrame, y: pd.Series, choice: str = "AUTO") -> Dict[str, Any]:
    """Entrena y evalúa modelos."""
    cfg = AppConfig()
    ok, msg = can_train(y, cfg)
    if not ok:
        return {"trainable": False, "reason": msg}
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    
    results = []
    
    # Modelo 1: Logistic
    sc1 = RobustScaler()
    m1 = LogisticRegression(max_iter=2000, class_weight="balanced")
    m1.fit(sc1.fit_transform(X_train), y_train)
    p1 = m1.predict_proba(sc1.transform(X_test))[:, 1]
    results.append({"name": "LogisticRegression", "model": m1, "scaler": sc1,
                    "pr_auc": average_precision_score(y_test, p1), "roc_auc": roc_auc_score(y_test, p1)})
    
    # Modelo 2: GradientBoosting
    sc2 = StandardScaler()
    m2 = GradientBoostingClassifier(random_state=42, n_estimators=220, max_depth=3)
    m2.fit(sc2.fit_transform(X_train), y_train)
    p2 = m2.predict_proba(sc2.transform(X_test))[:, 1]
    results.append({"name": "GradientBoosting", "model": m2, "scaler": sc2,
                    "pr_auc": average_precision_score(y_test, p2), "roc_auc": roc_auc_score(y_test, p2)})
    
    # Modelo 3: RandomForest
    m3 = RandomForestClassifier(n_estimators=500, max_depth=10, min_samples_leaf=8, 
                                 class_weight="balanced_subsample", random_state=42, n_jobs=-1)
    m3.fit(X_train, y_train)
    p3 = m3.predict_proba(X_test)[:, 1]
    results.append({"name": "RandomForest", "model": m3, "scaler": None,
                    "pr_auc": average_precision_score(y_test, p3), "roc_auc": roc_auc_score(y_test, p3)})
    
    # Selección
    df_res = pd.DataFrame([{"Modelo": r["name"], "PR-AUC": r["pr_auc"], "ROC-AUC": r["roc_auc"]} for r in results])
    df_res = df_res.sort_values("PR-AUC", ascending=False)
    
    if choice == "AUTO":
        best = results[df_res.index[0]]
    else:
        idx = {"MODELO 1": 0, "MODELO 2": 1, "MODELO 3": 2}.get(choice, 0)
        best = results[idx]
    
    return {"trainable": True, "best": best, "results": df_res}


def predict_prob(pack: Dict, X: pd.DataFrame) -> float:
    """Predice probabilidad con modelo entrenado."""
    model = pack["best"]["model"]
    scaler = pack["best"]["scaler"]
    Xc = scaler.transform(X) if scaler else X.values
    return float(model.predict_proba(Xc)[0][1])


def model_importance(pack: Dict, features: List[str], top_n: int = 12) -> pd.DataFrame:
    """Obtiene importancia de variables."""
    if not pack.get("trainable"):
        return pd.DataFrame(columns=["Variable", "Importancia"])
    
    model = pack["best"]["model"]
    if hasattr(model, "feature_importances_"):
        imp = model.feature_importances_
    elif hasattr(model, "coef_"):
        imp = np.abs(model.coef_[0])
    else:
        return pd.DataFrame(columns=["Variable", "Importancia"])
    
    df = pd.DataFrame({"Variable": features, "Importancia": imp})
    df = df.sort_values("Importancia", ascending=False).head(top_n)
    s = df["Importancia"].sum()
    if s > 0:
        df["Importancia"] = df["Importancia"] / s
    return df


# ===========================================
# GRÁFICOS
# ===========================================
def add_wash_lines(fig: go.Figure, washes: pd.DataFrame, enf_key: str, x_min=None, x_max=None) -> go.Figure:
    """Agrega líneas de lavados al gráfico."""
    if washes is None or washes.empty:
        return fig
    
    w = washes[washes["enfriador_key"] == enf_key].copy()
    if w.empty:
        return fig
    
    w["wash_ts"] = pd.to_datetime(w["wash_ts"], errors="coerce")
    w = w.dropna(subset=["wash_ts"])
    
    if x_min:
        w = w[w["wash_ts"] >= x_min]
    if x_max:
        w = w[w["wash_ts"] <= x_max]
    
    for _, row in w.iterrows():
        fig.add_shape(type="line", x0=row["wash_ts"], x1=row["wash_ts"], y0=0, y1=1, yref="paper",
                      line=dict(color="purple", width=1.5, dash="dot"), opacity=0.7)
    return fig


def create_thermal_chart(df: pd.DataFrame, ts_col: str, enf_key: str, washes: pd.DataFrame = None) -> go.Figure:
    """Crea gráfico térmico."""
    dsg = DESIGN_PARAMS.get(enf_key, {})
    df_op = df[df["en_operacion"] == 1].copy()
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Temperaturas del Ácido", "Carga Térmica (Q)"),
                        vertical_spacing=0.12, row_heights=[0.6, 0.4])
    
    fig.add_trace(go.Scatter(x=df_op[ts_col], y=df_op["T_a_in"], name="T entrada", line=dict(width=1.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_op[ts_col], y=df_op["T_a_out"], name="T salida", line=dict(width=2)), row=1, col=1)
    
    if dsg:
        fig.add_hline(y=dsg.get("T_acid_out_limit", 85), line_dash="dash", line_color="red", 
                      annotation_text="Límite", row=1, col=1)
        fig.add_hline(y=dsg.get("T_acid_out_design", 77), line_dash="dot", line_color="green",
                      annotation_text="Diseño", row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df_op[ts_col], y=df_op["Q_used_W"]/1e6, name="Q (MW)", 
                             line=dict(width=2), fill='tozeroy'), row=2, col=1)
    
    if dsg:
        fig.add_hline(y=dsg.get("Q_design_W", 1e7)/1e6, line_dash="dot", line_color="green", row=2, col=1)
    
    fig = add_wash_lines(fig, washes, enf_key, df[ts_col].min(), df[ts_col].max())
    
    fig.update_layout(height=520, template="plotly_white", hovermode="x unified",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02),
                      margin=dict(l=60, r=30, t=80, b=40))
    fig.update_yaxes(title_text="Temperatura (°C)", row=1, col=1)
    fig.update_yaxes(title_text="Q (MW)", row=2, col=1)
    return fig


def create_fouling_chart(df: pd.DataFrame, ts_col: str, enf_key: str, washes: pd.DataFrame = None) -> go.Figure:
    """Crea gráfico de ensuciamiento."""
    dsg = DESIGN_PARAMS.get(enf_key, {})
    df_op = df[df["en_operacion"] == 1].copy()
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        subplot_titles=("Factor de Ensuciamiento (Rf)", "Coeficiente de Transferencia (U)"),
                        vertical_spacing=0.12)
    
    fig.add_trace(go.Scatter(x=df_op[ts_col], y=df_op["Rf_x1e4"], name="Rf ×10⁻⁴", line=dict(width=2)), row=1, col=1)
    
    if dsg:
        Rf_des = dsg.get("fouling_design_m2KW", 1.43e-4) * 1e4
        fig.add_hline(y=Rf_des, line_dash="dot", line_color="green", row=1, col=1)
        fig.add_hline(y=Rf_des * 5, line_dash="dash", line_color="red", annotation_text="Crítico", row=1, col=1)
    
    fig.add_trace(go.Scatter(x=df_op[ts_col], y=df_op["U_Wm2K"], name="U real", line=dict(width=2)), row=2, col=1)
    
    if dsg:
        fig.add_hline(y=dsg.get("U_clean_Wm2K", 1700), line_dash="dot", line_color="green", row=2, col=1)
    
    fig = add_wash_lines(fig, washes, enf_key, df[ts_col].min(), df[ts_col].max())
    
    fig.update_layout(height=520, template="plotly_white", hovermode="x unified",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02),
                      margin=dict(l=60, r=30, t=80, b=40))
    fig.update_yaxes(title_text="Rf ×10⁻⁴", row=1, col=1)
    fig.update_yaxes(title_text="U (W/m²K)", row=2, col=1)
    return fig


def create_criticidad_chart(df: pd.DataFrame, ts_col: str, enf_key: str, washes: pd.DataFrame = None) -> go.Figure:
    """Crea gráfico de criticidad."""
    df_op = df[df["en_operacion"] == 1].copy()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_op[ts_col], y=df_op["criticidad"], name="Criticidad",
                             line=dict(width=2.5), fill='tozeroy'))
    
    fig.add_hline(y=30, line_dash="dot", line_color="yellow", annotation_text="Media")
    fig.add_hline(y=60, line_dash="dot", line_color="orange", annotation_text="Alta")
    fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Crítica")
    
    fig = add_wash_lines(fig, washes, enf_key, df[ts_col].min(), df[ts_col].max())
    
    fig.update_layout(height=420, template="plotly_white", hovermode="x unified",
                      title="Evolución del Índice de Criticidad",
                      yaxis_title="Criticidad (0-100)", margin=dict(l=60, r=30, t=60, b=40))
    return fig


# ===========================================
# VENTANAS
# ===========================================
def get_last_wash_ts(washes: pd.DataFrame, enf_key: str) -> Optional[pd.Timestamp]:
    """Obtiene timestamp del último lavado."""
    if washes is None or washes.empty:
        return None
    w = washes[washes["enfriador_key"] == enf_key]
    if w.empty:
        return None
    return pd.to_datetime(w["wash_ts"]).max()


def get_window_start(df: pd.DataFrame, ts_col: str, washes: pd.DataFrame, enf_key: str, fallback: int = 30) -> Tuple[Optional[pd.Timestamp], bool]:
    """Obtiene inicio de ventana."""
    last = get_last_wash_ts(washes, enf_key)
    if last:
        return pd.Timestamp(last), True
    if df.empty:
        return None, False
    return pd.Timestamp(df[ts_col].max() - pd.Timedelta(days=fallback)), False


def compute_global_window(all_df: Dict[str, pd.DataFrame], ts_col: str, fallback: int = 30) -> int:
    """Calcula ventana global."""
    vals = []
    for dfk in all_df.values():
        if dfk is None or dfk.empty:
            continue
        dfop = dfk[dfk["en_operacion"] == 1]
        if dfop.empty or "days_since_wash" not in dfop.columns:
            continue
        v = dfop.iloc[-1].get("days_since_wash", np.nan)
        if pd.notna(v):
            vals.append(float(v))
    return int(np.clip(max(vals), 7, 365)) if vals else fallback


# ===========================================
# PDF PROFESIONAL
# ===========================================
def generate_pdf(all_df: Dict, washes: pd.DataFrame, ts_col: str, window_days: int, 
                 model_choice: str, logo_path: str) -> Optional[bytes]:
    """
    Genera reporte PDF profesional con gráficos e interpretaciones.
    
    Incluye:
    - Resumen ejecutivo con recomendaciones
    - Gráficos comparativos entre enfriadores
    - Análisis detallado por enfriador con gráficos de tendencia
    - Interpretaciones automáticas
    - Timeline de lavados
    """
    if not PDF_AVAILABLE:
        return None
    
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        return None
    
    # Colores corporativos
    CORP = {
        'primary': colors.HexColor("#0B2D5B"),
        'secondary': colors.HexColor("#1E5AA8"),
        'accent': colors.HexColor("#E67E22"),
        'success': colors.HexColor("#27AE60"),
        'warning': colors.HexColor("#F39C12"),
        'danger': colors.HexColor("#E74C3C"),
        'light_bg': colors.HexColor("#F8F9FA"),
        'gray': colors.HexColor("#95A5A6"),
    }
    
    # Estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='MainTitle', fontSize=24, textColor=CORP['primary'],
                              spaceAfter=6, alignment=1, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='Subtitle', fontSize=12, textColor=CORP['gray'],
                              spaceAfter=20, alignment=1))
    styles.add(ParagraphStyle(name='SectionHeader', fontSize=16, textColor=CORP['primary'],
                              spaceBefore=20, spaceAfter=10, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='SubHeader', fontSize=13, textColor=CORP['secondary'],
                              spaceBefore=14, spaceAfter=8, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='Body', fontSize=10, textColor=colors.HexColor("#2C3E50"),
                              leading=14, spaceAfter=8))
    styles.add(ParagraphStyle(name='Small', fontSize=8, textColor=CORP['gray'], leading=10))
    styles.add(ParagraphStyle(name='Recommendation', fontSize=11, textColor=CORP['primary'],
                              fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=10,
                              leftIndent=20, backColor=colors.HexColor("#FFF8E7")))
    
    def fig_to_img(fig, width_cm=17.0):
        """Convierte figura matplotlib a imagen reportlab."""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        buf.seek(0)
        img = RLImage(buf)
        aspect = img.drawHeight / img.drawWidth
        img.drawWidth = width_cm * cm
        img.drawHeight = width_cm * cm * aspect
        return img
    
    def get_crit_info(val):
        if pd.isna(val): return "N/D", "⚪", CORP['gray']
        if val >= 80: return "CRÍTICA", "🔴", CORP['danger']
        if val >= 60: return "ALTA", "🟠", CORP['accent']
        if val >= 30: return "MEDIA", "🟡", CORP['warning']
        return "BAJA", "🟢", CORP['success']
    
    # === Preparar datos ===
    summary_data = []
    priority_enf = None
    max_score = -1
    
    for enf_key in ['TS', 'TAI', 'TAF']:
        df = all_df.get(enf_key, pd.DataFrame())
        dsg = DESIGN_PARAMS.get(enf_key, {})
        if df.empty:
            continue
        
        df = df.dropna(subset=[ts_col]).sort_values(ts_col)
        max_ts = df[ts_col].max()
        win_start = max_ts - pd.Timedelta(days=window_days)
        df_win = df[(df[ts_col] >= win_start) & (df['en_operacion'] == 1)]
        
        if df_win.empty:
            continue
        
        T_mean = float(df_win['T_a_out'].mean())
        T_p95 = float(df_win['T_a_out'].quantile(0.95))
        U_mean = float(df_win['U_Wm2K'].mean())
        U_clean = float(dsg.get('U_clean_Wm2K', 1700))
        U_pct = 100 * U_mean / U_clean if U_clean > 0 else 0
        Rf_mean = float(df_win['Rf_x1e4'].mean())
        Rf_p95 = float(df_win['Rf_x1e4'].quantile(0.95))
        Rf_design = float(dsg.get('fouling_design_m2KW', 1.43e-4)) * 1e4
        Rf_crit = Rf_design * 5
        Q_mean = float(df_win['Q_used_W'].mean()) / 1e6
        crit = float(df_win['criticidad'].mean()) if 'criticidad' in df_win else 0
        days_w = float(df_win['days_since_wash'].iloc[-1]) if 'days_since_wash' in df_win else np.nan
        T_limit = float(dsg.get('T_acid_out_limit', 85))
        
        req_wash = (T_p95 >= T_limit) or (Rf_p95 >= Rf_crit) or (crit >= 80)
        
        data = {
            'key': enf_key, 'name': dsg.get('short_name', enf_key),
            'T_mean': T_mean, 'T_p95': T_p95, 'T_limit': T_limit,
            'T_design': dsg.get('T_acid_out_design', 77),
            'U_mean': U_mean, 'U_clean': U_clean, 'U_pct': U_pct,
            'Rf_mean': Rf_mean, 'Rf_p95': Rf_p95, 'Rf_design': Rf_design, 'Rf_crit': Rf_crit,
            'Q_mean': Q_mean, 'Q_design': dsg.get('Q_design_W', 1e7) / 1e6,
            'criticidad': crit, 'days_wash': days_w, 'requires_wash': req_wash,
            'df_win': df_win, 'dsg': dsg
        }
        summary_data.append(data)
        
        score = (40 if T_p95 >= T_limit else 0) + (30 if Rf_p95 >= Rf_crit else 0) + (20 if crit >= 80 else 10 if crit >= 60 else 0)
        if score > max_score:
            max_score, priority_enf = score, data
    
    # === Construir PDF ===
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.8*cm, leftMargin=1.8*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)
    story = []
    
    # Logo
    if logo_path and os.path.exists(logo_path):
        try:
            logo = RLImage(logo_path)
            logo.drawHeight, logo.drawWidth = 1.5*cm, 5.0*cm
            story.append(logo)
            story.append(Spacer(1, 10))
        except: pass
    
    # Título
    story.append(Paragraph("Reporte Operacional", styles['MainTitle']))
    story.append(Paragraph("Enfriadores de Ácido Sulfúrico - Planta CAP-3", styles['Subtitle']))
    story.append(Spacer(1, 5))
    
    # Info
    info = Table([
        ['Fecha:', datetime.now().strftime('%d/%m/%Y %H:%M')],
        ['Ventana:', f'{window_days} días'],
        ['Equipos:', 'Torre Secado, Torre Interpaso, Torre Final']
    ], colWidths=[3*cm, 14*cm])
    info.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('TEXTCOLOR', (0,0), (0,-1), CORP['gray']),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica-Bold'),
    ]))
    story.append(info)
    story.append(Spacer(1, 20))
    
    # === RESUMEN EJECUTIVO ===
    story.append(Paragraph("1. Resumen Ejecutivo", styles['SectionHeader']))
    
    # Tabla resumen
    headers = ['Enfriador', 'T prom\n(°C)', 'T P95\n(°C)', 'U\n(% limpio)', 
               'Rf prom\n×10⁻⁴', 'Días s/\nlavado', 'Criticidad', 'Estado']
    rows = [headers]
    for d in summary_data:
        nivel, emoji, _ = get_crit_info(d['criticidad'])
        rows.append([
            d['name'], fmt(d['T_mean'], '{:.1f}'), fmt(d['T_p95'], '{:.1f}'),
            fmt(d['U_pct'], '{:.0f}%'), fmt(d['Rf_mean'], '{:.2f}'),
            fmt(d['days_wash'], '{:.0f}', 'Sin registro'),
            f"{fmt(d['criticidad'], '{:.0f}')}/100", f"{emoji} {nivel}"
        ])
    
    tbl = Table(rows, colWidths=[3*cm, 1.6*cm, 1.6*cm, 1.8*cm, 1.8*cm, 1.8*cm, 2*cm, 2.2*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), CORP['primary']),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, CORP['light_bg']]),
        ('GRID', (0,0), (-1,-1), 0.5, CORP['gray']),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 15))
    
    # Recomendación
    if priority_enf and priority_enf['requires_wash']:
        story.append(Paragraph(
            f"⚠️ <b>RECOMENDACIÓN:</b> Priorizar <b>{priority_enf['name']}</b> para lavado químico.<br/>"
            f"Criticidad: {priority_enf['criticidad']:.0f}/100 | "
            f"T P95: {priority_enf['T_p95']:.1f}°C (límite: {priority_enf['T_limit']:.0f}°C) | "
            f"Rf P95: {priority_enf['Rf_p95']:.2f}×10⁻⁴",
            styles['Recommendation']
        ))
    else:
        story.append(Paragraph(
            "✅ <b>ESTADO:</b> No se detectan condiciones críticas. Mantener monitoreo de rutina.",
            styles['Body']
        ))
    
    story.append(Spacer(1, 15))
    
    # Gráfico comparativo
    story.append(Paragraph("<b>Comparación entre enfriadores:</b>", styles['Body']))
    
    fig_comp, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    names = [d['name'] for d in summary_data]
    x = np.arange(len(names))
    
    # Criticidad
    crits = [d['criticidad'] for d in summary_data]
    colors_crit = ['#27AE60' if c < 30 else '#F39C12' if c < 60 else '#E67E22' if c < 80 else '#E74C3C' for c in crits]
    axes[0].bar(x, crits, 0.6, color=colors_crit, edgecolor='white', linewidth=2)
    axes[0].axhline(80, color='red', linestyle='--', alpha=0.7)
    axes[0].axhline(60, color='orange', linestyle=':', alpha=0.5)
    axes[0].set_ylabel('Criticidad'); axes[0].set_title('Índice de Criticidad', fontweight='bold')
    axes[0].set_xticks(x); axes[0].set_xticklabels(names, fontsize=9); axes[0].set_ylim(0, 100)
    
    # T P95
    temps = [d['T_p95'] for d in summary_data]
    limits = [d['T_limit'] for d in summary_data]
    colors_t = ['#E74C3C' if t >= l else '#27AE60' for t, l in zip(temps, limits)]
    axes[1].bar(x, temps, 0.6, color=colors_t, edgecolor='white', linewidth=2)
    for i, l in enumerate(limits):
        axes[1].hlines(l, i-0.4, i+0.4, color='red', linestyle='--', linewidth=2)
    axes[1].set_ylabel('T P95 (°C)'); axes[1].set_title('Temperatura vs Límite', fontweight='bold')
    axes[1].set_xticks(x); axes[1].set_xticklabels(names, fontsize=9)
    
    # Rf P95
    rfs = [d['Rf_p95'] for d in summary_data]
    rf_crits = [d['Rf_crit'] for d in summary_data]
    colors_rf = ['#E74C3C' if r >= c else '#F39C12' if r >= c*0.6 else '#27AE60' for r, c in zip(rfs, rf_crits)]
    axes[2].bar(x, rfs, 0.6, color=colors_rf, edgecolor='white', linewidth=2)
    for i, c in enumerate(rf_crits):
        axes[2].hlines(c, i-0.4, i+0.4, color='red', linestyle='--', linewidth=2)
    axes[2].set_ylabel('Rf P95 ×10⁻⁴'); axes[2].set_title('Ensuciamiento vs Crítico', fontweight='bold')
    axes[2].set_xticks(x); axes[2].set_xticklabels(names, fontsize=9)
    
    plt.tight_layout()
    story.append(fig_to_img(fig_comp, 17))
    story.append(PageBreak())
    
    # === ANÁLISIS POR ENFRIADOR ===
    for i, data in enumerate(summary_data):
        name = data['name']
        dsg = data['dsg']
        df_win = data['df_win']
        
        story.append(Paragraph(f"2.{i+1}. {name}", styles['SectionHeader']))
        story.append(Paragraph(
            f"<b>Diseño:</b> Área: {dsg.get('area_m2', 0):.1f} m² | "
            f"U limpio: {dsg.get('U_clean_Wm2K', 0):.0f} W/m²K | "
            f"Q diseño: {dsg.get('Q_design_W', 0)/1e6:.2f} MW | "
            f"T límite: {dsg.get('T_acid_out_limit', 0):.0f}°C",
            styles['Small']
        ))
        story.append(Spacer(1, 10))
        
        # KPIs
        story.append(Paragraph("<b>Indicadores clave:</b>", styles['SubHeader']))
        kpi_rows = [
            ['Parámetro', 'Valor', 'Referencia', 'Estado'],
            ['T salida promedio', f"{data['T_mean']:.1f} °C", f"Diseño: {data['T_design']:.0f} °C", 
             '✅' if data['T_mean'] < data['T_limit'] else '⚠️'],
            ['T salida P95', f"{data['T_p95']:.1f} °C", f"Límite: {data['T_limit']:.0f} °C",
             '✅' if data['T_p95'] < data['T_limit'] else '🔴'],
            ['U promedio', f"{data['U_mean']:.0f} W/m²K ({data['U_pct']:.0f}%)", f"Limpio: {data['U_clean']:.0f}",
             '✅' if data['U_pct'] >= 80 else ('⚠️' if data['U_pct'] >= 60 else '🔴')],
            ['Rf promedio', f"{data['Rf_mean']:.2f} ×10⁻⁴", f"Diseño: {data['Rf_design']:.2f}",
             '✅' if data['Rf_mean'] < data['Rf_design'] * 3 else '⚠️'],
            ['Rf P95', f"{data['Rf_p95']:.2f} ×10⁻⁴", f"Crítico: {data['Rf_crit']:.2f}",
             '✅' if data['Rf_p95'] < data['Rf_crit'] else '🔴'],
            ['Criticidad', f"{data['criticidad']:.0f}/100", '<60 normal',
             '✅' if data['criticidad'] < 60 else ('⚠️' if data['criticidad'] < 80 else '🔴')],
        ]
        kpi_tbl = Table(kpi_rows, colWidths=[4.5*cm, 4.5*cm, 4.5*cm, 1.5*cm])
        kpi_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), CORP['primary']),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, CORP['light_bg']]),
            ('GRID', (0,0), (-1,-1), 0.5, CORP['gray']),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(kpi_tbl)
        story.append(Spacer(1, 10))
        
        # Interpretaciones
        story.append(Paragraph("<b>Interpretación:</b>", styles['SubHeader']))
        interps = []
        if data['T_p95'] >= data['T_limit']:
            interps.append(f"⚠️ ALERTA: T P95 ({data['T_p95']:.1f}°C) excede límite ({data['T_limit']:.0f}°C)")
        elif data['T_p95'] >= data['T_limit'] * 0.95:
            interps.append(f"🟡 T P95 ({data['T_p95']:.1f}°C) cercana al límite")
        else:
            interps.append(f"✅ Temperatura OK: promedio {data['T_mean']:.1f}°C, P95 {data['T_p95']:.1f}°C")
        
        if data['Rf_p95'] >= data['Rf_crit']:
            interps.append(f"🔴 CRÍTICO: Rf P95 ({data['Rf_p95']:.2f}) alcanza nivel crítico")
        elif data['Rf_p95'] >= data['Rf_design'] * 3:
            interps.append(f"🟠 Alto ensuciamiento: Rf P95 ({data['Rf_p95']:.2f}) > 3x diseño")
        else:
            interps.append(f"✅ Ensuciamiento OK: Rf promedio {data['Rf_mean']:.2f}")
        
        if data['U_pct'] < 60:
            interps.append(f"⚠️ U muy bajo ({data['U_pct']:.0f}% limpio)")
        elif data['U_pct'] < 80:
            interps.append(f"🟡 U reducido ({data['U_pct']:.0f}% limpio)")
        else:
            interps.append(f"✅ U OK ({data['U_pct']:.0f}% limpio)")
        
        nivel, emoji, _ = get_crit_info(data['criticidad'])
        interps.append(f"{emoji} Criticidad {nivel}: {data['criticidad']:.0f}/100")
        
        for interp in interps:
            story.append(Paragraph(f"• {interp}", styles['Body']))
        story.append(Spacer(1, 10))
        
        # Gráficos
        story.append(Paragraph("<b>Tendencias:</b>", styles['SubHeader']))
        
        df = df_win.dropna(subset=[ts_col]).sort_values(ts_col)
        
        # Gráfico Temperaturas
        fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 4.5), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
        ax1.plot(df[ts_col], df['T_a_in'], label='T entrada', linewidth=1.2, alpha=0.8)
        ax1.plot(df[ts_col], df['T_a_out'], label='T salida', linewidth=1.8)
        ax1.axhline(data['T_limit'], color='red', linestyle='--', label=f"Límite ({data['T_limit']:.0f}°C)")
        ax1.axhline(data['T_design'], color='green', linestyle=':', label=f"Diseño ({data['T_design']:.0f}°C)")
        ax1.fill_between(df[ts_col], data['T_limit'], df['T_a_out'].max()*1.1, alpha=0.1, color='red')
        ax1.set_ylabel('Temperatura (°C)'); ax1.legend(loc='upper left', fontsize=8); ax1.grid(True, alpha=0.3)
        ax1.set_title(f'{name} - Temperaturas y Carga Térmica', fontsize=11, fontweight='bold', color='#0B2D5B')
        
        df['Q_MW'] = df['Q_used_W'] / 1e6
        ax2.fill_between(df[ts_col], 0, df['Q_MW'], alpha=0.5, color='#3498db')
        ax2.plot(df[ts_col], df['Q_MW'], linewidth=1.2, color='#2980b9')
        ax2.axhline(data['Q_design'], color='green', linestyle=':', label=f"Diseño ({data['Q_design']:.1f} MW)")
        ax2.set_ylabel('Q (MW)'); ax2.set_xlabel('Fecha'); ax2.legend(fontsize=8); ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        plt.tight_layout()
        story.append(fig_to_img(fig1, 16.5))
        story.append(Spacer(1, 8))
        
        # Gráfico Rf y U
        fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(10, 4.5), sharex=True)
        ax3.plot(df[ts_col], df['Rf_x1e4'], linewidth=1.8, color='#e74c3c')
        ax3.axhline(data['Rf_design'], color='green', linestyle=':', label=f"Diseño ({data['Rf_design']:.2f})")
        ax3.axhline(data['Rf_crit'], color='red', linestyle='--', label=f"Crítico ({data['Rf_crit']:.2f})")
        ax3.fill_between(df[ts_col], data['Rf_crit'], df['Rf_x1e4'].max()*1.2, alpha=0.1, color='red')
        ax3.set_ylabel('Rf ×10⁻⁴'); ax3.legend(fontsize=8); ax3.grid(True, alpha=0.3)
        ax3.set_title(f'{name} - Ensuciamiento y Coeficiente U', fontsize=11, fontweight='bold', color='#0B2D5B')
        
        ax4.plot(df[ts_col], df['U_Wm2K'], linewidth=1.8, color='#3498db')
        ax4.axhline(data['U_clean'], color='green', linestyle=':', label=f"U limpio ({data['U_clean']:.0f})")
        ax4.axhline(data['U_clean']*0.6, color='orange', linestyle='--', label='60% limpio')
        ax4.fill_between(df[ts_col], 0, data['U_clean']*0.6, alpha=0.1, color='orange')
        ax4.set_ylabel('U (W/m²K)'); ax4.set_xlabel('Fecha'); ax4.legend(fontsize=8); ax4.grid(True, alpha=0.3)
        ax4.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        plt.tight_layout()
        story.append(fig_to_img(fig2, 16.5))
        story.append(Spacer(1, 8))
        
        # Gráfico Criticidad
        fig3, ax5 = plt.subplots(figsize=(10, 3))
        ax5.fill_between(df[ts_col], 0, df['criticidad'], alpha=0.4, color='#3498db')
        ax5.plot(df[ts_col], df['criticidad'], linewidth=2, color='#2980b9')
        ax5.axhspan(0, 30, alpha=0.1, color='green'); ax5.axhspan(30, 60, alpha=0.1, color='yellow')
        ax5.axhspan(60, 80, alpha=0.1, color='orange'); ax5.axhspan(80, 100, alpha=0.15, color='red')
        ax5.axhline(80, color='red', linestyle='--', alpha=0.7)
        ax5.axhline(60, color='orange', linestyle=':', alpha=0.5)
        ax5.set_ylabel('Criticidad (0-100)'); ax5.set_xlabel('Fecha'); ax5.set_ylim(0, 105)
        ax5.grid(True, alpha=0.3)
        ax5.set_title(f'{name} - Índice de Criticidad', fontsize=11, fontweight='bold', color='#0B2D5B')
        ax5.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        plt.tight_layout()
        story.append(fig_to_img(fig3, 16.5))
        
        story.append(PageBreak())
    
    # === HISTORIAL DE LAVADOS ===
    story.append(Paragraph("3. Historial de Lavados Químicos", styles['SectionHeader']))
    
    fig_wash, ax_w = plt.subplots(figsize=(10, 2.8))
    if washes is not None and not washes.empty:
        w = washes.copy()
        w['wash_ts'] = pd.to_datetime(w['wash_ts'], errors='coerce')
        w = w.dropna(subset=['wash_ts', 'enfriador_key']).sort_values('wash_ts')
        y_map = {'TS': 2, 'TAI': 1, 'TAF': 0}
        c_map = {'TS': '#3498db', 'TAI': '#e74c3c', 'TAF': '#27ae60'}
        l_map = {'TS': 'Torre Secado', 'TAI': 'Torre Interpaso', 'TAF': 'Torre Final'}
        for key in ['TS', 'TAI', 'TAF']:
            wk = w[w['enfriador_key'] == key]
            if not wk.empty:
                ax_w.scatter(wk['wash_ts'], [y_map[key]]*len(wk), s=100, c=c_map[key], marker='D',
                           label=l_map[key], edgecolors='white', linewidths=2, zorder=3)
        ax_w.set_yticks([0, 1, 2]); ax_w.set_yticklabels(['Torre Final', 'Torre Interpaso', 'Torre Secado'])
        ax_w.legend(loc='upper right', fontsize=8)
    else:
        ax_w.text(0.5, 0.5, 'Sin registros de lavados', ha='center', va='center', fontsize=14, color='gray', transform=ax_w.transAxes)
        ax_w.axis('off')
    ax_w.set_xlabel('Fecha'); ax_w.grid(True, alpha=0.3, axis='x'); ax_w.set_ylim(-0.5, 2.5)
    ax_w.set_title('Timeline de Lavados', fontsize=11, fontweight='bold', color='#0B2D5B')
    ax_w.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.tight_layout()
    story.append(fig_to_img(fig_wash, 17))
    story.append(Spacer(1, 15))
    
    # Tabla resumen lavados
    wash_rows = [['Enfriador', 'Total lavados', 'Último lavado', 'Intervalo promedio']]
    if washes is not None and not washes.empty:
        w = washes.copy()
        w['wash_ts'] = pd.to_datetime(w['wash_ts'], errors='coerce')
        w = w.dropna(subset=['wash_ts', 'enfriador_key'])
        for key in ['TS', 'TAI', 'TAF']:
            wk = w[w['enfriador_key'] == key].sort_values('wash_ts')
            name = DESIGN_PARAMS.get(key, {}).get('short_name', key)
            if wk.empty:
                wash_rows.append([name, '0', 'Sin registros', 'N/D'])
            else:
                intervals = wk['wash_ts'].diff().dt.days.dropna()
                wash_rows.append([name, str(len(wk)), wk['wash_ts'].max().strftime('%d/%m/%Y'),
                                f"{intervals.mean():.0f} días" if len(intervals) > 0 else 'N/D'])
    else:
        for key in ['TS', 'TAI', 'TAF']:
            wash_rows.append([DESIGN_PARAMS.get(key, {}).get('short_name', key), '0', 'Sin registros', 'N/D'])
    
    wash_tbl = Table(wash_rows, colWidths=[4.5*cm, 3.5*cm, 4*cm, 4*cm])
    wash_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), CORP['primary']),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, CORP['light_bg']]),
        ('GRID', (0,0), (-1,-1), 0.5, CORP['gray']),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(wash_tbl)
    story.append(Spacer(1, 20))
    
    # Notas
    story.append(Paragraph(
        "<b>Notas:</b><br/>"
        "• P95 = Percentil 95 (valor no superado por el 95% de las mediciones)<br/>"
        "• Rf = Factor de ensuciamiento (resistencia térmica adicional)<br/>"
        "• U = Coeficiente global de transferencia de calor<br/>"
        "• Criticidad combina: temperatura (30%), ensuciamiento (35%), eficiencia U (25%), tiempo sin lavado (10%)",
        styles['Small']
    ))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# ===========================================
# APLICACIÓN STREAMLIT
# ===========================================
cfg = AppConfig()
st.set_page_config(page_title=cfg.PAGE_TITLE, page_icon=cfg.PAGE_ICON, layout="wide", initial_sidebar_state="expanded")

st.title("❄️ CAP-3 – Enfriadores de Ácido (v5.0)")
st.caption("Dashboard refactorizado con mejor estructura y mantenibilidad.")

# Sidebar
st.sidebar.header("⚙️ Configuración")
data_file = st.sidebar.text_input("Archivo datos", value=cfg.DATA_FILE)
wash_file = st.sidebar.text_input("Archivo lavados", value=cfg.WASH_FILE)
logo_path = st.sidebar.text_input("Logo", value=cfg.LOGO_PATH)

st.sidebar.markdown("---")
st.sidebar.subheader("🔧 Filtros")
min_blower = st.sidebar.slider("Velocidad mín. soplador (%)", 0, 80, 50)
min_flow = st.sidebar.slider("Flujo agua mín. (% diseño)", 10, 80, 30)

st.sidebar.markdown("---")
st.sidebar.subheader("🤖 ML")
model_choice = st.sidebar.selectbox("Modelo", ["AUTO", "MODELO 1", "MODELO 2", "MODELO 3"])

# Cargar datos
df_wide = read_csv_auto(data_file)
df_washes = load_washes(wash_file)

if df_wide.empty:
    st.error(f"No se pudo cargar: {data_file}")
    st.stop()

ts_col = find_timestamp_col(df_wide)
df_wide[ts_col] = pd.to_datetime(df_wide[ts_col], errors="coerce", dayfirst=True)
df_wide = df_wide.dropna(subset=[ts_col]).sort_values(ts_col)

df_long = explode_wide_to_long(df_wide, ts_col)

# Procesar enfriadores
all_df = {}
all_last = {}
enf_names = {k: DESIGN_PARAMS[k]["short_name"] for k in ["TS", "TAI", "TAF"]}

for enf_key in ["TS", "TAI", "TAF"]:
    df = df_long[df_long["Enfriador_Key"] == enf_key].copy()
    df = filter_operation(df, enf_key, min_blower, min_flow)
    df = apply_thermal_model(df, ts_col, enf_key)
    df = add_wash_features(df, df_washes, ts_col, enf_key)
    df = calculate_criticidad(df, enf_key)
    
    df_op = df[df["en_operacion"] == 1].copy().sort_values(ts_col)
    df_op = add_rolling_features(df_op, ts_col, 7, enf_key)
    
    roll_cols = [c for c in ["T_out_ma", "T_out_p95_7d", "Rf_ma", "Rf_slope", "U_ma", "Rf_days_to_crit_est"] if c in df_op.columns]
    if roll_cols:
        df = df.merge(df_op[[ts_col] + roll_cols].drop_duplicates(ts_col), on=ts_col, how="left")
    
    all_df[enf_key] = df
    if not df_op.empty:
        all_last[enf_key] = df_op.iloc[-1].to_dict()

# Ventana global
window_global = compute_global_window(all_df, ts_col, cfg.FALLBACK_WINDOW_DAYS)

# Sidebar selector
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Enfriador")

max_days, critical_key = -1, "TS"
for k in ["TS", "TAI", "TAF"]:
    d = all_last.get(k, {}).get("days_since_wash", np.nan)
    if pd.notna(d) and d > max_days:
        max_days, critical_key = d, k

st.sidebar.info(f"Más días s/lavado: **{enf_names[critical_key]}** ({max_days:.0f}d)" if max_days >= 0 else "Sin registros.")
st.sidebar.success(f"Ventana GLOBAL: **{window_global}** días")

enf_sel = st.sidebar.selectbox("Seleccionar", ["TS", "TAI", "TAF"], 
                                format_func=lambda x: f"{enf_names[x]} (ENF {x})",
                                index=["TS", "TAI", "TAF"].index(critical_key))

dsg = DESIGN_PARAMS[enf_sel]
st.sidebar.markdown(f"**{dsg['name']}**\n- Área: {dsg['area_m2']:.1f} m²\n- Límite T: {dsg['T_acid_out_limit']:.0f}°C")

# Datos seleccionados
df_full = all_df[enf_sel].copy()
df_full_op = df_full[df_full["en_operacion"] == 1].copy()

window_start, has_wash = get_window_start(df_full, ts_col, df_washes, enf_sel, cfg.FALLBACK_WINDOW_DAYS)
df_window = df_full[df_full[ts_col] >= window_start].copy() if window_start else df_full.copy()
df_window_op = df_window[df_window["en_operacion"] == 1].copy()

# Ventana global para comparativa
max_ts = df_full[ts_col].max()
global_start = max_ts - pd.Timedelta(days=window_global)
df_global = df_full[df_full[ts_col] >= global_start].copy()
df_global_op = df_global[df_global["en_operacion"] == 1].copy()

st.sidebar.markdown("---")
st.sidebar.info(f"Total: {len(df_full):,} | Op: {len(df_full_op):,}")

# Estado Actual
st.markdown("### 📊 Estado Actual")
if window_start:
    st.caption(f"Ventana: {'desde último lavado' if has_wash else f'últimos {cfg.FALLBACK_WINDOW_DAYS}d'} ({window_start.strftime('%Y-%m-%d')})")

if df_window_op.empty:
    st.warning("Sin datos en operación.")
else:
    stt = window_stats(df_window_op, dsg)
    
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("T salida (prom)", fmt(stt.get("T_out_mean"), "{:.1f}°C"), 
              f"P95: {fmt(stt.get('T_out_p95'), '{:.1f}')}°C")
    c2.metric("U (prom)", fmt(stt.get("U_mean"), "{:.0f}"), 
              f"{fmt(stt.get('U_mean_pct'), '{:.0f}')}% limpio")
    c3.metric("Rf ×10⁻⁴ (prom)", fmt(stt.get("Rf_mean"), "{:.2f}"),
              f"P95: {fmt(stt.get('Rf_p95'), '{:.2f}')}")
    c4.metric("Q MW (prom)", fmt(stt.get("Q_mean_MW"), "{:.2f}"),
              f"{fmt(stt.get('Q_mean_pct'), '{:.0f}')}% diseño")
    c5.metric("Días s/lavado", fmt(stt.get("days_since_wash_last"), "{:.0f}", "Sin registro"))
    
    crit = stt.get("crit_mean", np.nan)
    nivel = "N/D"
    if pd.notna(crit):
        nivel = "Baja" if crit < 30 else ("Media" if crit < 60 else ("Alta" if crit < 80 else "Crítica"))
    emoji = {"Baja": "🟢", "Media": "🟡", "Alta": "🟠", "Crítica": "🔴"}.get(nivel, "⚪")
    c6.metric("Criticidad", f"{emoji} {nivel}", fmt(crit, "{:.0f}"))

# PDF
col1, col2 = st.columns([3, 1])
with col2:
    if PDF_AVAILABLE and st.button("📄 Generar PDF", type="primary"):
        with st.spinner("Generando..."):
            pdf = generate_pdf(all_df, df_washes, ts_col, window_global, model_choice, logo_path)
            if pdf:
                st.download_button("⬇️ Descargar PDF", pdf, f"reporte_{datetime.now():%Y%m%d_%H%M}.pdf", "application/pdf")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Térmico", "🔥 Ensuciamiento", "⚠️ Criticidad", "🧪 Lavados", "🤖 ML"])

with tab1:
    st.subheader(f"Análisis Térmico - {enf_names[enf_sel]}")
    interp = get_thermal_interpretation(df_window_op, enf_sel)
    with st.expander("📋 Interpretación", expanded=True):
        for item in interp.get("items", []):
            st.markdown(item)
    st.plotly_chart(create_thermal_chart(df_window, ts_col, enf_sel, df_washes), use_container_width=True)

with tab2:
    st.subheader(f"Ensuciamiento - {enf_names[enf_sel]}")
    interp = get_fouling_interpretation(df_window_op, enf_sel)
    with st.expander("📋 Interpretación", expanded=True):
        for item in interp.get("items", []):
            st.markdown(item)
    st.plotly_chart(create_fouling_chart(df_window, ts_col, enf_sel, df_washes), use_container_width=True)

with tab3:
    st.subheader(f"Criticidad - {enf_names[enf_sel]}")
    interp = get_criticidad_interpretation(df_window_op, enf_sel)
    with st.expander("📋 Interpretación", expanded=True):
        for item in interp.get("items", []):
            st.markdown(item)
        if interp.get("recs"):
            st.markdown("**Acciones:**")
            for r in interp["recs"]:
                st.markdown(r)
    st.plotly_chart(create_criticidad_chart(df_window, ts_col, enf_sel, df_washes), use_container_width=True)
    
    st.markdown("#### Comparativa (ventana global)")
    comp = []
    for k in ["TS", "TAI", "TAF"]:
        dfk = all_df.get(k, pd.DataFrame())
        if dfk.empty:
            continue
        max_ts_k = dfk[ts_col].max()
        dfk_op = dfk[(dfk[ts_col] >= max_ts_k - pd.Timedelta(days=window_global)) & (dfk["en_operacion"] == 1)]
        if dfk_op.empty:
            continue
        stt_k = window_stats(dfk_op, DESIGN_PARAMS[k])
        need, reason = requires_wash(dfk_op, k, ts_col)
        comp.append({"Enfriador": enf_names[k], "Criticidad": fmt(stt_k.get("crit_mean"), "{:.0f}"),
                     "T P95": fmt(stt_k.get("T_out_p95"), "{:.1f}"), "Rf P95": fmt(stt_k.get("Rf_p95"), "{:.2f}"),
                     "¿Lavado?": "Sí" if need else "No", "Motivo": reason})
    if comp:
        st.dataframe(pd.DataFrame(comp), use_container_width=True)

with tab4:
    st.subheader("Historial de Lavados")
    
    with st.expander("➕ Registrar Lavado"):
        c1, c2 = st.columns(2)
        new_date = c1.date_input("Fecha", value=datetime.now())
        new_enf = c1.selectbox("Enfriador", ["TS", "TAI", "TAF"], format_func=lambda x: enf_names[x])
        new_tipo = c2.selectbox("Tipo", ["Limpieza Química", "Limpieza Mecánica", "Otro"])
        new_user = c2.text_input("Usuario")
        new_comment = st.text_area("Comentario")
        
        if st.button("💾 Guardar"):
            if save_wash(wash_file, datetime.combine(new_date, datetime.min.time()), new_enf, new_tipo, new_comment, new_user):
                st.success("✅ Guardado")
                st.rerun()
    
    st.markdown("---")
    w = df_washes[df_washes["enfriador_key"] == enf_sel].copy()
    w["wash_ts"] = pd.to_datetime(w["wash_ts"], errors="coerce")
    w = w.dropna(subset=["wash_ts"]).sort_values("wash_ts")
    
    if w.empty:
        st.warning("Sin registros.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total", len(w))
        intervals = w["wash_ts"].diff().dt.days.dropna()
        c2.metric("Intervalo prom", f"{intervals.mean():.0f}d" if len(intervals) > 0 else "N/D")
        c3.metric("Último", w["wash_ts"].max().strftime("%Y-%m-%d"))
        
        fig = go.Figure(go.Scatter(x=w["wash_ts"], y=[1]*len(w), mode='markers+text',
                                   marker=dict(size=15, symbol='diamond'),
                                   text=[d.strftime('%Y-%m') for d in w["wash_ts"]], textposition="top center"))
        fig.update_layout(height=200, yaxis=dict(visible=False), showlegend=False, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(w.sort_values("wash_ts", ascending=False)[["wash_ts", "tipo", "comentario", "usuario"]], use_container_width=True)

with tab5:
    st.subheader(f"🤖 ML - {enf_names[enf_sel]}")
    st.markdown(f"Predicción de lavado en ≤ **{cfg.PRED_HORIZON_DAYS}** días usando ML + score operacional.")
    
    if df_full_op.empty:
        st.warning("Sin datos.")
    else:
        w_sel = df_washes[df_washes["enfriador_key"] == enf_sel]
        df_ml = df_full[df_full["en_operacion"] == 1].copy().sort_values(ts_col)
        df_ml = add_rolling_features(df_ml, ts_col, 7, enf_sel)
        df_ml = build_event_label(df_ml, w_sel, ts_col, cfg.PRED_HORIZON_DAYS)
        
        features = get_ml_features(df_ml)
        X, y = prep_ml_data(df_ml, features)
        
        c = y.value_counts()
        st.info(f"Datos: n={len(y)}, pos={c.get(1,0)}, neg={c.get(0,0)}")
        
        pack = train_models(X, y, model_choice)
        rule_score, rule_notes = operational_score(df_window_op, enf_sel, ts_col)
        
        prob_ml = None
        if pack.get("trainable"):
            last_row = df_ml.dropna(subset=features).iloc[-1:]
            if not last_row.empty:
                prob_ml = predict_prob(pack, last_row[features])
            st.success(f"✅ ML: **{pack['best']['name']}**")
            st.dataframe(pack["results"], use_container_width=True)
        else:
            st.warning(f"⚠️ ML no entrenable: {pack.get('reason')}")
        
        prob_final = 0.6 * prob_ml + 0.4 * rule_score if prob_ml else rule_score
        
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure(go.Indicator(mode="gauge+number", value=prob_final * 100,
                                         title={'text': "Probabilidad combinada"},
                                         gauge={'axis': {'range': [0, 100]}, 'bar': {'color': COLORS['primary']},
                                                'steps': [{'range': [0, 30], 'color': '#d4edda'},
                                                          {'range': [30, 70], 'color': '#fff3cd'},
                                                          {'range': [70, 100], 'color': '#f8d7da'}]}))
            fig.update_layout(height=320)
            st.plotly_chart(fig, use_container_width=True)
        
        with c2:
            if prob_final < 0.3:
                st.success(f"✅ **{prob_final*100:.0f}%** - No requiere lavado.")
            elif prob_final < 0.7:
                st.warning(f"🟡 **{prob_final*100:.0f}%** - Zona intermedia.")
            else:
                st.error(f"🔴 **{prob_final*100:.0f}%** - Requiere lavado.")
            
            if prob_ml:
                st.write(f"• ML: **{prob_ml*100:.0f}%**")
            st.write(f"• Operacional: **{rule_score*100:.0f}%**")
            for n in rule_notes:
                st.write(f"- {n}")
        
        st.markdown("#### Importancia de variables")
        imp = model_importance(pack, features)
        if not imp.empty:
            fig = go.Figure(go.Bar(x=imp["Importancia"], y=imp["Variable"], orientation='h'))
            fig.update_layout(height=360, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

# Datos detallados
with st.expander("📋 Datos Detallados"):
    cols = [ts_col, "en_operacion", "T_a_in", "T_a_out", "F_w", "LMTD_K", "U_Wm2K", 
            "Rf_x1e4", "Q_used_W", "days_since_wash", "criticidad", "nivel_criticidad"]
    cols = [c for c in cols if c in df_global.columns]
    
    show_all = st.checkbox("Incluir fuera de operación")
    st.dataframe((df_global if show_all else df_global_op)[cols].tail(500), use_container_width=True)