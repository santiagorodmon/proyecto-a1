from src.fetch_dane import fetch_ipc, preparar_resumen
from src.fetch_banrep import fetch_trm_mensual, get_tasa_banrep, preparar_resumen_banrep
from src.analyze import analizar_con_claude
from src.report import generar_reporte

def main():
    print("\n=== Proyecto A1-C: Reporte Macro Colombia — 3 Indicadores ===\n")

    # 1. IPC — DANE
    print("[1/4] Cargando IPC (DANE)...")
    df_ipc = fetch_ipc()
    resumen_ipc = preparar_resumen(df_ipc)

    # 2. TRM — Superintendencia Financiera vía datos.gov.co
    print("\n[2/4] Cargando TRM (Superintendencia Financiera)...")
    df_trm = fetch_trm_mensual()

    # 3. Tasa Banrep — decisiones JDBR
    print("\n[3/4] Cargando tasa de política monetaria (Banrep)...")
    df_tasa = get_tasa_banrep()
    resumen_banrep = preparar_resumen_banrep(df_trm, df_tasa)

    # 4. Análisis integrado con Claude
    print("\n[4/4] Analizando con Claude API (3 indicadores)...")
    analisis = analizar_con_claude(resumen_ipc, resumen_banrep)

    # 5. Reporte
    print("\n[5/5] Generando reporte...")
    reporte, ruta = generar_reporte(resumen_ipc, analisis, resumen_banrep)

    print(f"\n=== Completado ===")
    print(f"Archivo: {ruta}")
    print("\n--- Vista previa ---\n")
    print(analisis[:400] + "...")

if __name__ == "__main__":
    main()