import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

def analizar_con_claude(resumen_datos: dict) -> str:

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    system_prompt = """Eres un economista senior especializado en economía colombiana con 
experiencia en análisis macroeconómico para el sector privado.

Cuando analices datos del IPC debes cubrir obligatoriamente:
1. Contexto: ¿dónde estamos vs la meta del Banrep (3%) y vs el ciclo histórico reciente?
2. Drivers: ¿qué sectores de la canasta explican la inflación actual?
3. Política monetaria: implicaciones de la tasa actual del Banrep para empresas y hogares
4. Impacto sectorial: qué sectores se benefician y cuáles se perjudican
5. Proyección: hacia dónde va la inflación en los próximos 6 meses
6. Recomendaciones: 3 acciones concretas para empresas colombianas

Usa formato Markdown con secciones claras. Tono profesional pero accesible.
Máximo 700 palabras. Sin emojis — usa texto plano y Markdown estándar (##, **, tablas).
Sé preciso con los números — cítalos del contexto dado.
Asegúrate de completar TODAS las secciones antes de terminar. 
No cortes la respuesta a mitad de una tabla o sección."""

    user_message = f"""Analiza la siguiente situación inflacionaria de Colombia:

**Datos principales:**
- Último dato disponible: {resumen_datos['ultimo_dato']}
- Inflación anual más reciente: {resumen_datos['inflacion_anual_reciente']}%
- Variación mensual más reciente: {resumen_datos['inflacion_mensual_reciente']}%
- Promedio del período analizado: {resumen_datos['promedio_anual_periodo']}%
- Máximo del período: {resumen_datos['maximo_anual']}%
- Mínimo del período: {resumen_datos['minimo_anual']}%
- Tendencia general: {resumen_datos['tendencia']}

**Contexto de política monetaria:**
- Meta inflación Banrep: {resumen_datos['meta_banrep']}%
- Brecha actual vs meta: +{resumen_datos['brecha_meta']} puntos porcentuales
- Tasa de interés Banrep actual: {resumen_datos['tasa_banrep_actual']}% (enero 2026)

**Serie histórica mensual (más reciente primero):**
{json.dumps(resumen_datos['datos_raw'], indent=2, ensure_ascii=False)}

Genera el reporte ejecutivo completo."""

    print("→ Enviando a Claude API...")
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1800,
        messages=[{"role": "user", "content": user_message}],
        system=system_prompt
    )

    analisis = message.content[0].text
    print(f"✓ Análisis generado ({len(analisis)} caracteres)")
    print(f"  Tokens: input={message.usage.input_tokens}, output={message.usage.output_tokens}")
    return analisis