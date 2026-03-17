# Proyecto A1 — Reporte Macroeconómico Automatizado con Claude API

Herramienta que descarga datos reales del DANE, los procesa con Python
y genera un análisis económico ejecutivo profesional usando la API de Claude.

## Demo
```
=== Proyecto A1: Reporte Económico con Claude API ===

[1/3] Descargando datos del DANE...
  → Usando datos reales DANE 2023-2025 (fuente: boletines oficiales)
  Último dato: 2025-12-01 | Inflación anual: 5.1% | Brecha meta: +2.1 pp

[2/3] Analizando con Claude API...
→ Enviando a Claude API...
✓ Análisis generado | Tokens: input=980, output=1500

[3/3] Generando reporte...
✓ Reporte guardado en: data/reporte_ipc_20260316.md
```

## Ejemplo de output

Ver [`data/reporte_ipc_20260316.md`](data/reporte_ipc_20260316.md)

## Stack técnico

| Herramienta | Uso |
|---|---|
| Python 3.11 | Lenguaje principal |
| `anthropic` SDK | Llamadas a Claude API |
| `pandas` | Procesamiento de datos |
| `python-dotenv` | Manejo seguro de API keys |
| DANE / datos.gov.co | Fuente de datos oficial |

## Cómo ejecutar
```bash
git clone https://github.com/tu-usuario/proyecto-a1
cd proyecto-a1
pip install -r requirements.txt
cp .env.example .env        # agrega tu ANTHROPIC_API_KEY
python main.py
```

## Arquitectura
```
DANE (datos.gov.co) → fetch_dane.py → analyze.py (Claude API) → report.py → .md
```

## Sobre este proyecto

Demuestra la combinación de:
- Análisis económico con datos macro reales de Colombia
- Integración con LLMs via API (Anthropic Claude)
- Automatización de reportes ejecutivos en Python

Parte del portafolio de Datos + AI de Santiago Rodríguez Montaño — Economista & Data Analyst.