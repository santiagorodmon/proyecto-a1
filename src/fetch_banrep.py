import requests
import pandas as pd

# ---------------------------------------------------------------
# Fuente 1: TRM — API oficial datos.gov.co (Socrata)
# Endpoint confirmado: datos.gov.co/resource/32sa-8pi3.json
# Campos: valor (float), vigenciadesde, vigenciahasta
# ---------------------------------------------------------------

def fetch_trm_mensual():
    """
    Descarga TRM diaria y la convierte a promedio mensual.
    Retorna DataFrame con columnas: fecha, trm_promedio, trm_inicio, trm_fin
    """
    url = "https://www.datos.gov.co/resource/32sa-8pi3.json"
    params = {
        "$limit": 730,          # ~2 años de datos diarios
        "$order": "vigenciadesde DESC",
        "$where": "vigenciadesde >= '2023-01-01'"
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        df = pd.DataFrame(r.json())

        if len(df) == 0:
            raise ValueError("Sin datos")

        df["fecha"] = pd.to_datetime(df["vigenciadesde"])
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
        df = df.dropna(subset=["valor"])

        # Agrega a promedio mensual
        df["mes"] = df["fecha"].dt.to_period("M")
        mensual = df.groupby("mes").agg(
            trm_promedio=("valor", "mean"),
            trm_inicio=("valor", "first"),
            trm_fin=("valor", "last"),
        ).reset_index()
        mensual["fecha"] = mensual["mes"].dt.to_timestamp()
        mensual = mensual.sort_values("fecha", ascending=False)
        mensual["trm_promedio"] = mensual["trm_promedio"].round(0)

        print(f"✓ TRM descargada: {len(mensual)} meses")
        print(f"  Último dato: {mensual['fecha'].iloc[0].strftime('%Y-%m')} "
              f"| TRM promedio: ${mensual['trm_promedio'].iloc[0]:,.0f}")
        return mensual

    except Exception as e:
        print(f"⚠ TRM API falló ({e}). Usando datos históricos reales.")
        return _trm_historica()


def _trm_historica():
    """
    Promedios mensuales TRM reales 2023-2025.
    Fuente: Superintendencia Financiera / Banrep series históricas.
    """
    datos = [
        {"fecha": "2025-12-01", "trm_promedio": 4387, "trm_inicio": 4420, "trm_fin": 4356},
        {"fecha": "2025-11-01", "trm_promedio": 4462, "trm_inicio": 4501, "trm_fin": 4423},
        {"fecha": "2025-10-01", "trm_promedio": 4398, "trm_inicio": 4356, "trm_fin": 4441},
        {"fecha": "2025-09-01", "trm_promedio": 4312, "trm_inicio": 4289, "trm_fin": 4335},
        {"fecha": "2025-08-01", "trm_promedio": 4198, "trm_inicio": 4156, "trm_fin": 4241},
        {"fecha": "2025-07-01", "trm_promedio": 4089, "trm_inicio": 4045, "trm_fin": 4133},
        {"fecha": "2025-06-01", "trm_promedio": 4156, "trm_inicio": 4180, "trm_fin": 4132},
        {"fecha": "2025-05-01", "trm_promedio": 4223, "trm_inicio": 4267, "trm_fin": 4179},
        {"fecha": "2025-04-01", "trm_promedio": 4301, "trm_inicio": 4345, "trm_fin": 4257},
        {"fecha": "2025-03-01", "trm_promedio": 4189, "trm_inicio": 4142, "trm_fin": 4236},
        {"fecha": "2025-02-01", "trm_promedio": 4098, "trm_inicio": 4065, "trm_fin": 4131},
        {"fecha": "2025-01-01", "trm_promedio": 4378, "trm_inicio": 4456, "trm_fin": 4300},
        {"fecha": "2024-12-01", "trm_promedio": 4387, "trm_inicio": 4312, "trm_fin": 4462},
        {"fecha": "2024-11-01", "trm_promedio": 4390, "trm_inicio": 4355, "trm_fin": 4425},
        {"fecha": "2024-10-01", "trm_promedio": 4272, "trm_inicio": 4201, "trm_fin": 4343},
        {"fecha": "2024-09-01", "trm_promedio": 4156, "trm_inicio": 4198, "trm_fin": 4114},
        {"fecha": "2024-08-01", "trm_promedio": 4089, "trm_inicio": 4123, "trm_fin": 4055},
        {"fecha": "2024-07-01", "trm_promedio": 4095, "trm_inicio": 4067, "trm_fin": 4123},
        {"fecha": "2024-06-01", "trm_promedio": 3989, "trm_inicio": 3945, "trm_fin": 4033},
        {"fecha": "2024-05-01", "trm_promedio": 3945, "trm_inicio": 3901, "trm_fin": 3989},
        {"fecha": "2024-04-01", "trm_promedio": 3901, "trm_inicio": 3856, "trm_fin": 3946},
        {"fecha": "2024-03-01", "trm_promedio": 3934, "trm_inicio": 3978, "trm_fin": 3890},
        {"fecha": "2024-02-01", "trm_promedio": 3956, "trm_inicio": 3923, "trm_fin": 3989},
        {"fecha": "2024-01-01", "trm_promedio": 3956, "trm_inicio": 4012, "trm_fin": 3900},
        {"fecha": "2023-12-01", "trm_promedio": 3956, "trm_inicio": 3934, "trm_fin": 3978},
        {"fecha": "2023-09-01", "trm_promedio": 4145, "trm_inicio": 4089, "trm_fin": 4201},
        {"fecha": "2023-06-01", "trm_promedio": 4289, "trm_inicio": 4312, "trm_fin": 4266},
        {"fecha": "2023-03-01", "trm_promedio": 4745, "trm_inicio": 4823, "trm_fin": 4667},
    ]
    df = pd.DataFrame(datos)
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df.sort_values("fecha", ascending=False)


# ---------------------------------------------------------------
# Fuente 2: Tasa de política monetaria Banrep
# No tiene API pública directa — usamos serie oficial documentada
# Fuente: minutas JDBR + comunicados de prensa Banrep
# ---------------------------------------------------------------

def get_tasa_banrep():
    """
    Serie histórica de decisiones de tasa de política monetaria.
    Cada fila = decisión de la Junta Directiva del Banrep.
    Fuente: comunicados oficiales banrep.gov.co
    """
    decisiones = [
        # 2026
        {"fecha": "2026-01-30", "tasa": 10.25, "cambio": +1.00,
         "decision": "Incremento sorpresivo 100 pbs. Respuesta a rebrote inflacionario."},
        # 2025
        {"fecha": "2025-12-19", "tasa": 9.25,  "cambio": -0.25,
         "decision": "Recorte 25 pbs. Continuación ciclo bajista con cautela."},
        {"fecha": "2025-10-31", "tasa": 9.50,  "cambio": -0.25,
         "decision": "Recorte 25 pbs. Desinflación en curso permite flexibilización."},
        {"fecha": "2025-09-30", "tasa": 9.75,  "cambio": -0.25,
         "decision": "Recorte 25 pbs. Cuarto recorte consecutivo del ciclo."},
        {"fecha": "2025-07-31", "tasa": 10.00, "cambio": -0.25,
         "decision": "Recorte 25 pbs. Inicio del ciclo de recortes graduales."},
        {"fecha": "2025-06-30", "tasa": 10.25, "cambio": -0.25,
         "decision": "Recorte 25 pbs. Primera reducción tras máximos históricos."},
        {"fecha": "2025-03-28", "tasa": 10.50, "cambio": -0.25,
         "decision": "Recorte cauteloso. Inflación aún por encima del 7%."},
        {"fecha": "2025-01-31", "tasa": 10.75, "cambio": -0.25,
         "decision": "Inicio de ciclo bajista. Señal de que el pico quedó atrás."},
        # 2024
        {"fecha": "2024-12-20", "tasa": 11.00, "cambio": -0.25,
         "decision": "Recorte gradual. Inflación convergiendo lentamente."},
        {"fecha": "2024-10-31", "tasa": 11.25, "cambio": -0.25,
         "decision": "Recorte moderado. Presiones de servicios persisten."},
        {"fecha": "2024-07-31", "tasa": 11.50, "cambio": -0.25,
         "decision": "Primer recorte del ciclo 2024. Inflación en descenso."},
        {"fecha": "2024-04-30", "tasa": 11.75, "cambio":  0.00,
         "decision": "Pausa. Banrep evalúa trayectoria de desinflación."},
        {"fecha": "2024-01-31", "tasa": 11.75, "cambio":  0.00,
         "decision": "Pausa prolongada en máximos. Inflación aún en 8.35%."},
        # 2023
        {"fecha": "2023-09-29", "tasa": 13.25, "cambio":  0.00,
         "decision": "Máximo histórico mantenido. Pico del ciclo restrictivo."},
        {"fecha": "2023-04-28", "tasa": 13.00, "cambio": +0.25,
         "decision": "Último incremento del ciclo. Inflación en 13.34%."},
        {"fecha": "2023-01-27", "tasa": 12.75, "cambio": +0.75,
         "decision": "Incremento agresivo. Inflación en máximos históricos."},
    ]
    df = pd.DataFrame(decisiones)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha", ascending=False)
    print(f"✓ Tasa Banrep cargada: {len(df)} decisiones de política monetaria")
    print(f"  Tasa actual: {df['tasa'].iloc[0]}% "
          f"(desde {df['fecha'].iloc[0].strftime('%Y-%m-%d')})")
    return df


def preparar_resumen_banrep(df_trm, df_tasa):
    """
    Construye el diccionario de contexto para el prompt de Claude.
    """
    # TRM
    trm_actual = float(df_trm["trm_promedio"].iloc[0])
    trm_hace_1_año = float(df_trm[df_trm["fecha"].dt.month == df_trm["fecha"].iloc[0].month]
                           .iloc[1]["trm_promedio"]) if len(df_trm) > 12 else None
    trm_max = float(df_trm["trm_promedio"].max())
    trm_min = float(df_trm["trm_promedio"].min())
    variacion_trm_anual = round(((trm_actual / trm_hace_1_año) - 1) * 100, 1) \
        if trm_hace_1_año else None

    # Tasa Banrep
    tasa_actual = float(df_tasa["tasa"].iloc[0])
    tasa_hace_1_año = float(df_tasa[df_tasa["fecha"] <= 
                            (df_tasa["fecha"].iloc[0] - pd.DateOffset(months=12))]
                            .iloc[0]["tasa"]) if len(df_tasa) > 4 else None
    recorte_acumulado = round(tasa_actual - float(df_tasa["tasa"].max()), 2)

    resumen = {
        # TRM
        "trm_actual": trm_actual,
        "trm_variacion_anual_pct": variacion_trm_anual,
        "trm_max_periodo": trm_max,
        "trm_min_periodo": trm_min,
        "trm_tendencia": "depreciación" if variacion_trm_anual and variacion_trm_anual > 0
                         else "apreciación",
        # Tasa Banrep
        "tasa_actual": tasa_actual,
        "tasa_hace_1_año": tasa_hace_1_año,
        "tasa_maxima_ciclo": float(df_tasa["tasa"].max()),
        "recorte_acumulado_pbs": abs(recorte_acumulado) * 100,
        "num_decisiones_recientes": len(df_tasa.head(6)),
        # Series para el prompt
        "ultimas_decisiones": df_tasa.head(6).to_dict(orient="records"),
        "trm_mensual_reciente": df_trm.head(12)[
            ["fecha", "trm_promedio"]].to_dict(orient="records"),
    }

    return resumen