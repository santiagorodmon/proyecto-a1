from src.fetch_dane import fetch_ipc, preparar_resumen
from src.analyze import analizar_con_claude
from src.report import generar_reporte

def main():
    print("\n=== Proyecto A1: Reporte Económico con Claude API ===\n")
    
    # 1. Descarga datos
    print("[1/3] Descargando datos del DANE...")
    df = fetch_ipc()
    resumen = preparar_resumen(df)
    
    # 2. Analiza con Claude
    print("\n[2/3] Analizando con Claude API...")
    analisis = analizar_con_claude(resumen)
    
    # 3. Genera reporte
    print("\n[3/3] Generando reporte...")
    reporte, ruta = generar_reporte(resumen, analisis)
    
    print("\n=== Completado ===")
    print(f"Archivo: {ruta}")
    print("\n--- Vista previa del análisis ---\n")
    print(analisis[:500] + "...")

if __name__ == "__main__":
    main()