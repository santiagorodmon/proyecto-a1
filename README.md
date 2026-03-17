# Proyecto A1 — Reporte Macroeconómico Colombia con Claude API

Sistema automatizado que descarga datos reales de tres fuentes oficiales colombianas,
los procesa con Python y genera un reporte ejecutivo de nivel consultoría usando la API de Claude.

## Demo
```
=== Proyecto A1-C: Reporte Macro Colombia — 3 Indicadores ===

[1/4] Cargando IPC (DANE)...
  Último dato: 2025-12-01 | Inflación anual: 5.1% | Brecha meta: +2.1 pp

[2/4] Cargando TRM (Superintendencia Financiera)...
✓ TRM descargada: 28 meses | TRM promedio: $3,737

[3/4] Cargando tasa de política monetaria (Banrep)...
✓ Tasa Banrep cargada: 16 decisiones | Tasa actual: 10.25%

[4/4] Analizando con Claude API (3 indicadores)...
✓ Análisis generado | Tokens: input=1.400, output=1.800
```

## Output — Dashboard de indicadores

| Indicador | Valor actual | Variación | Tendencia |
|---|---|---|---|
| Inflación anual (IPC) | 5.1% | 0.27% mensual | Descendente |
| Brecha vs meta Banrep | +2.1 pp | Meta: 3.0% | Por convergir |
| Tasa política monetaria | 10.25% | -300 pbs desde pico | Ciclo bajista |
| TRM (COP/USD) | $3,737 | -9.6% anual | Apreciación |

Ver reporte completo: [`data/reporte_macro_20260316_2208.md`](data/reporte_macro_20260316_2208.md)

## El análisis cubre

- **Triángulo macroeconómico** — posición simultánea en IPC, tasa y TRM
- **Relaciones causales** — cómo se retroalimentan los tres indicadores
- **Ciclo de política monetaria** — recorrido del Banrep y perspectivas
- **Dinámica cambiaria** — drivers de la TRM y pass-through a la inflación
- **Escenarios H1 2026** — base, optimista y adverso con supuestos explícitos
- **Recomendaciones diferenciadas** — importadores, exportadores y empresas con deuda

## Stack técnico

| Herramienta | Uso |
|---|---|
| Python 3.11 | Lenguaje principal |
| `anthropic` SDK | Llamadas a Claude claude-sonnet-4-6 |
| `pandas` | Procesamiento y agregación de series |
| `requests` | Consumo de APIs públicas |
| `python-dotenv` | Manejo seguro de credenciales |
| DANE / datos.gov.co | Fuente IPC oficial |
| Superfinanciera / datos.gov.co | Fuente TRM oficial |
| Banrep / comunicados JDBR | Fuente tasa de política monetaria |

## Fuentes de datos

| Indicador | Fuente | Endpoint |
|---|---|---|
| IPC (inflación) | DANE | datos.gov.co — boletines oficiales |
| TRM | Superintendencia Financiera | datos.gov.co/resource/32sa-8pi3.json |
| Tasa política monetaria | Banco de la República | Comunicados JDBR — banrep.gov.co |

## Arquitectura
```
DANE ──────────────┐
                   ├─→ fetch_dane.py ──┐
Superfinanciera ───┤                   ├─→ analyze.py (Claude API) ─→ report.py ─→ .md
                   ├─→ fetch_banrep.py─┘
Banrep ────────────┘
```

## Cómo ejecutar
```bash
git clone https://github.com/santiagorodmon/proyecto-a1
cd proyecto-a1
pip install -r requirements.txt
cp .env.example .env        # agrega tu ANTHROPIC_API_KEY
python main.py
```

## Estructura del proyecto
```
proyecto-a1/
├── src/
│   ├── fetch_dane.py       # IPC — DANE
│   ├── fetch_banrep.py     # TRM + Tasa Banrep
│   ├── analyze.py          # Integración Claude API
│   └── report.py           # Generación del reporte .md
├── data/
│   └── reporte_macro_*.md  # Reportes generados
├── main.py                 # Orquestador principal
├── requirements.txt
├── .env.example
└── README.md
```

## Sobre este proyecto

Demuestra la combinación de análisis económico con automatización usando AI:

- Datos macroeconómicos reales de Colombia (IPC, TRM, política monetaria)
- Integración con LLMs via API — Claude claude-sonnet-4-6 (Anthropic)
- Análisis del triángulo macroeconómico con relaciones causales
- Escenarios prospectivos y recomendaciones por tipo de empresa

**Autor:** Santiago Rodriguez — Economista & Data + AI Analyst  
**LinkedIn:** https://www.linkedin.com/in/santiagorodriguezmo/
**Contacto:** santiagorodmon@gmail.com