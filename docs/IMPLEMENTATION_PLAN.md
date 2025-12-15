# Plan de Implementación: Career Assistant AI

## 1. Stack Tecnológico
*   **Infrastructure:** Docker & Docker Compose (Ejecución aislada y portable).
*   **Lenguaje:** Python 3.10+
*   **Interfaz:** Streamlit (para web UI rápida y visual).
*   **Modelado de Datos:** Pydantic (para validar estructuras).
*   **IA / LLM (Coste Zero):**
    *   **Opción A (Local):** Ollama (Modelo `llama3:8b`). Totalmente gratis, corre en tu máquina.
    *   **Opción B (Cloud Free):** Google Gemini 2.0 Flash (Free Tier) (Placeholder implementado).
*   **Web Scraping / Investigación:** `primp` (Browser Impersonation) + `duckduckgo-search` + `beautifulsoup4`.
*   **Gestión de Config:** Variables de entorno (`.env` inyectado por Docker).

## 2. Arquitectura de Módulos

### Estructura de Proyecto
```
career-assistant/
├── app/
│   ├── main.py              # Entry point Streamlit
│   ├── components/          # Widgets UI reutilizables
│   ├── core/
│   │   ├── agent.py         # Orquestador (Orchstrator)
│   │   ├── llm.py           # Abstracción para Ollama/Gemini (JSON Mode support)
│   │   ├── models.py        # Pydantic Schemas
│   │   └── profile.py       # Cargador del portfolio.yaml
│   └── tools/
│       ├── search.py        # DuckDuckGo Search Wrapper
│       └── scraper.py       # Extractor HTML con Primp (Chrome Impersonation)
├── data/
│   └── portfolio.yaml       # Tu base de conocimiento
├── .env                     # Secrets
├── Dockerfile               # Definición de la imagen
├── docker-compose.yml       # Orquestación de servicios
└── requirements.txt
```

## 3. Fases de Desarrollo

### Fase 1: Core & Ingesta (El MVP Funcional) - ✅ COMPLETADO
*   [x] Configurar entorno Python + Poetry/Pip.
*   [x] Crear `profile.py`: Cargar y parsear `portfolio.yaml` a objetos Pydantic.
*   [x] Crear UI básica en Streamlit: Input URL o Texto plano.
*   [x] Integrar `llm.py`: Prompt base para extraer información estructurada.

### Fase 2: Motor de Decisión (El "Filtro") - ✅ COMPLETADO
*   [x] Implementar lógica de "Hard Filters" (Solo rechazo explícito).
*   [x] Crear Prompt de "Match Analysis": Cruzar oferta extraída vs `portfolio.yaml` (Optimizado con JSON Mode).
*   [x] Generar visualización en Streamlit: Score, Semáforo, Listado PROS/CONS dinámicos.

### Fase 3: Deep Research (El "Investigador") - ✅ COMPLETADO
*   [x] Implementar búsqueda web simple (DuckDuckGo Search) para la empresa.
    *   Implementado con filtrado `region="wt-wt"` y gestión de errores.
*   [x] Agente investigador: Detecta nombre de empresa y busca reviews/red flags.
*   [x] Integrar info de reputación en el reporte final.

## 4. Prompt Engineering Strategy
Diseñaremos un "System Prompt" robusto que actúe como un **Headhunter Senior** que:
1.  Es escéptico (busca "trampas" en la oferta).
2.  Es defensor de tus intereses (prioriza tu work-life balance y salario).
3.  Usa tu `portfolio.yaml` como "Biblia" de tu verdad.

## 5. Next Steps
1.  Inicializar entorno.
2.  Crear estructura de carpetas.
3.  Prototipar la UI de Streamlit vacía.
