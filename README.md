# 🚀 Career Assistant AI

Un asistente de carrera personal potenciado por Inteligencia Artificial Local (Ollama) diseñado para ingenieros de software. Automatiza el análisis de ofertas de empleo, investiga la reputación de las empresas y evalúa el encaje con tu perfil profesional para maximizar tu eficiencia en la búsqueda de empleo.

## ✨ Características Principales

- **🕵️‍♂️ Deep Research (Investigación Profunda)**: Detecta automáticamente el nombre de la empresa y busca referencias en la web (Glassdoor, Reddit, noticias de despidos) para identificar "red flags" culturales.
- **🧠 Motor de Decisión Inteligente**: Utiliza `llama3:8b` (vía Ollama) para analizar la descripción del trabajo contra tu portfolio profesional.
- **🛡️ Filtros Duros (Hard Filters)**: Evaluación automática de requisitos críticos: Remoto 100%, Visa Sponsorship y Rango Salarial.
- **📊 Scoring y Feedback Detallado**:
    - Puntuación de compatibilidad (0-100%).
    - Veredicto claro: `STRONGLY_APPLY`, `APPLY`, `CONSIDER`, `IGNORE`.
    - Pros y Contras personalizados (nada de respuestas genéricas).
    - Justificación detallada del score.
- **🌐 Scraping Avanzado**: Capacidad para extraer texto de URLs protegidas (anti-bot) utilizando suplantación de huella digital de navegador (Chrome/Googlebot).
- **🔒 Privacidad Total**: Ejecución 100% local. Tus datos y tu portfolio nunca salen de tu máquina.

## 🛠️ Stack Tecnológico

- **Frontend**: Streamlit
- **Lenguaje**: Python 3.10+
- **LLM/IA**: Ollama (Modelo `llama3:8b`)
- **Web Scraping**: `primp` (Browser Impersonation), `BeautifulSoup`
- **Internet Search**: `duckduckgo-search`
- **Gestión de Datos**: Pydantic
- **Contenedorización**: Docker & Docker Compose

## 🚀 Instalación y Uso Local

### Prerrequisitos
1.  **Python 3.10+** instalado.
2.  **Ollama** instalado y corriendo.
    - Descarga el modelo: `ollama pull llama3:8b`
3.  (Opcional) **Docker** si prefieres no instalar dependencias de Python directamente.

### 1. Configuración del Entorno
Clona el repositorio y configura las variables de entorno:

```bash
git clone https://github.com/aandmaldonado/career-assistant.git
cd career-assistant

# Crea y configura el archivo .env
echo "LLM_PROVIDER=ollama" > .env
echo "OLLAMA_BASE_URL=http://localhost:11434" >> .env
echo "OLLAMA_MODEL=llama3:8b" >> .env
```

### 2. Ejecución con Python (Recomendado para desarrollo)

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app/main.py
```

### 3. Ejecución con Docker

```bash
docker-compose up --build
```

Visita `http://localhost:8501` en tu navegador.

## 📂 Estructura del Proyecto

```
career-assistant/
├── app/
│   ├── core/
│   │   ├── agent.py       # Lógica del Agente de Carrera (Prompting & Analysis)
│   │   ├── llm.py         # Cliente para Ollama/Gemini (JSON Mode enabled)
│   │   ├── models.py      # Modelos de datos Pydantic
│   │   └── profile.py     # Carga del portfolio.yaml
│   ├── tools/
│   │   ├── scraper.py     # Extracción de contenido web (Primp/Requests)
│   │   └── search.py      # Búsqueda en DuckDuckGo
│   └── main.py            # Interfaz de Usuario (Streamlit)
├── data/                  # Datos locales (no versionados)
├── portfolio.yaml         # Tu base de conocimiento profesional (CV, Skills, Preferencias)
├── .env                   # Configuración de entorno
├── docker-compose.yml
└── requirements.txt
```

## 📝 Personalización

Para que el asistente funcione contigo, debes editar el archivo `portfolio.yaml` con tu información:
- **Skills**: Tus tecnologías y nivel de experiencia.
- **Projects**: Tus proyectos más relevantes.
- **Hard Filters**: Tus condiciones innegociables (Salario, Remoto, etc).

## 🤝 Contribución

PRs son bienvenidos. Por favor, asegúrate de mantener la limpieza del código y seguir el estilo de commits convencional.

## 📄 Licencia

MIT License.