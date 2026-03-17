from datetime import datetime
from pathlib import Path

def generar_reporte(resumen_datos: dict, analisis: str) -> str:



    fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M")

    reporte = f"""# Reporte Macroeconómico Colombia — IPC
**Generado:** {fecha_hoy}
**Fuente:** DANE — Índice de Precios al Consumidor
**Análisis:** Claude claude-sonnet-4-6 (Anthropic API)
**Período cubierto:** {resumen_datos['registros_analisis']} meses recientes de {resumen_datos['total_registros']} disponibles

---

## Datos clave

| Métrica | Valor |
|---|---|
| Último dato | {resumen_datos['ultimo_dato']} |
| Inflación anual | {resumen_datos['inflacion_anual_reciente']}% |
| Variación mensual | {resumen_datos['inflacion_mensual_reciente']}% |
| Promedio del período | {resumen_datos['promedio_anual_periodo']}% |
| Máximo registrado | {resumen_datos['maximo_anual']}% |
| Mínimo registrado | {resumen_datos['minimo_anual']}% |
| Tendencia | {resumen_datos['tendencia'].capitalize()} |
| Brecha vs meta Banrep (3%) | +{resumen_datos['brecha_meta']} pp |
| Tasa Banrep actual | {resumen_datos['tasa_banrep_actual']}% |

---

## Análisis económico
{advertencia}
{analisis}

---

## Metodología

- **Fuente de datos:** DANE — datos.gov.co (boletines IPC oficiales)
- **Procesamiento:** Python + pandas
- **Análisis:** Claude claude-sonnet-4-6 via Anthropic API
- **Repositorio:** github.com/tu-usuario/proyecto-a1

*Proyecto A1 — Portafolio Datos + AI | {datetime.now().year}*
"""

    output_path = Path("data") / f"reporte_ipc_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    output_path.write_text(reporte, encoding="utf-8")
    print(f"✓ Reporte guardado en: {output_path}")
    return reporte, str(output_path)