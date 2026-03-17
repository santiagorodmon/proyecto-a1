from datetime import datetime
from pathlib import Path


def generar_reporte(resumen_datos: dict, analisis: str, resumen_banrep: dict = None) -> str:

    if resumen_banrep is None:
        resumen_banrep = {
            "tasa_actual": "N/A", "recorte_acumulado_pbs": 0,
            "trm_actual": 0, "trm_variacion_anual_pct": "N/A",
            "trm_tendencia": "N/A"
        }

    fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M")

    reporte = f"""# Reporte Macroeconómico Colombia
**Generado:** {fecha_hoy}
**Fuentes:** DANE (IPC) · Banrep (Tasa política monetaria) · Superfinanciera (TRM)
**Análisis:** Claude claude-sonnet-4-6 (Anthropic API)

---

## Dashboard de indicadores

| Indicador | Valor actual | Variación | Tendencia |
|---|---|---|---|
| Inflación anual (IPC) | {resumen_datos['inflacion_anual_reciente']}% | {resumen_datos['inflacion_mensual_reciente']}% mensual | {resumen_datos['tendencia'].capitalize()} |
| Brecha vs meta Banrep | +{resumen_datos['brecha_meta']} pp | Meta: 3.0% | Por convergir |
| Tasa política monetaria | {resumen_banrep['tasa_actual']}% | -{resumen_banrep['recorte_acumulado_pbs']:.0f} pbs desde pico | Ciclo bajista |
| TRM (COP/USD) | ${resumen_banrep['trm_actual']:,.0f} | {resumen_banrep['trm_variacion_anual_pct']}% anual | {resumen_banrep['trm_tendencia'].capitalize()} |

---

## Análisis económico integrado

{analisis}

---

## Metodología

- **IPC:** DANE — datos.gov.co (boletines mensuales oficiales)
- **Tasa Banrep:** Comunicados JDBR — banrep.gov.co
- **TRM:** Superintendencia Financiera vía datos.gov.co/resource/32sa-8pi3
- **Análisis:** Claude claude-sonnet-4-6 con prompt económico especializado
- **Repositorio:** github.com/santiagorodmon/proyecto-a1

*Proyecto A1-C — Portafolio Datos + AI | {datetime.now().year}*
"""

    output_path = Path("data") / f"reporte_macro_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    output_path.write_text(reporte, encoding="utf-8")
    print(f"✓ Reporte guardado en: {output_path}")
    return reporte, str(output_path)