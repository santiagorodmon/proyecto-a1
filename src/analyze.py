import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

def analizar_con_claude(resumen_ipc: dict, resumen_banrep: dict) -> str:
    """
    Análisis integrado: IPC + Tasa Banrep + TRM.
    El prompt aprovecha la formación económica del autor.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    system_prompt = """Eres un economista senior de una firma de consultoría colombiana.
Produces reportes macroeconómicos de alta calidad para clientes del sector financiero,
empresarial e institucional. Tu análisis siempre integra los tres pilares del diagnóstico
macroeconómico colombiano: inflación (IPC), política monetaria (tasa Banrep) y tasa de
cambio (TRM), mostrando las relaciones causales entre ellos.

Estructura OBLIGATORIA del reporte (completa todas las secciones):
1. Triángulo macroeconómico: posición actual en los tres indicadores
2. Relaciones causales: cómo se retroalimentan IPC, tasa y TRM en el ciclo actual
3. Análisis del ciclo de política monetaria: recorrido y perspectivas
4. Dinámica cambiaria: drivers de la TRM y su pass-through a la inflación
5. Escenarios para H1 2026: base, optimista y adverso (tabla de 3 columnas)
6. Recomendaciones diferenciadas: para importadores, exportadores y empresas de deuda

Formato: Markdown limpio, sin emojis, tablas donde aplique.
Extensión: 750-850 palabras. Cita los números exactos del contexto dado."""

    # Serializa fechas para JSON
    import json
    from datetime import datetime

    def serialize(obj):
        if hasattr(obj, "strftime"):
            return obj.strftime("%Y-%m")
        if hasattr(obj, "isoformat"):
            return obj.isoformat()
        return str(obj)

    user_message = f"""Genera el reporte macroeconómico integrado con los siguientes datos:

## INDICADOR 1 — IPC (DANE)
- Inflación anual dic-2025: {resumen_ipc['inflacion_anual_reciente']}%
- Variación mensual dic-2025: {resumen_ipc['inflacion_mensual_reciente']}%
- Promedio del período: {resumen_ipc['promedio_anual_periodo']}%
- Máximo registrado: {resumen_ipc['maximo_anual']}% (ene-2025)
- Tendencia: {resumen_ipc['tendencia']}
- Brecha vs meta Banrep (3%): +{resumen_ipc['brecha_meta']} pp

## INDICADOR 2 — TASA DE POLÍTICA MONETARIA (Banrep)
- Tasa actual: {resumen_banrep['tasa_actual']}% (desde ene-2026)
- Tasa hace 12 meses: {resumen_banrep['tasa_hace_1_año']}%
- Máximo del ciclo: {resumen_banrep['tasa_maxima_ciclo']}% (sep-2023)
- Recorte acumulado desde el pico: {resumen_banrep['recorte_acumulado_pbs']:.0f} pbs
- Últimas decisiones:
{json.dumps(resumen_banrep['ultimas_decisiones'], indent=2, default=serialize, ensure_ascii=False)}

## INDICADOR 3 — TRM (Superintendencia Financiera)
- TRM promedio dic-2025: ${resumen_banrep['trm_actual']:,.0f} COP/USD
- Variación anual TRM: {resumen_banrep['trm_variacion_anual_pct']}%
- Tendencia cambiaria: {resumen_banrep['trm_tendencia']}
- Máximo del período: ${resumen_banrep['trm_max_periodo']:,.0f}
- Mínimo del período: ${resumen_banrep['trm_min_periodo']:,.0f}
- Serie mensual reciente:
{json.dumps(resumen_banrep['trm_mensual_reciente'], indent=2, default=serialize, ensure_ascii=False)}

Genera el reporte ejecutivo completo con las 6 secciones obligatorias."""

    print("→ Enviando 3 indicadores a Claude API...")
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": user_message}],
        system=system_prompt
    )

    analisis = message.content[0].text
    print(f"✓ Análisis generado ({len(analisis)} caracteres)")
    print(f"  Tokens: input={message.usage.input_tokens}, output={message.usage.output_tokens}")
    return analisis