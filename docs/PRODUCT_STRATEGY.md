# Estrategia de Producto: Career Assistant AI

## 1. Visión del Producto
Convertir el proceso de búsqueda laboral de una tarea manual y exhaustiva a una **toma de decisiones ejecutiva basada en datos**. El usuario (tú) deja de ser un "buscador" para convertirse en un "evaluador" de oportunidades pre-calificadas.

No es un bot de spam para aplicar a todo; es un **filtro inteligente de alta precisión** diseñado para maximizar el ROI de tu tiempo.

## 2. Propuesta de Valor
*   **Eficiencia Extrema:** Reduce el tiempo de análisis de oferta de 30-40 minutos a < 2 minutos.
*   **Filtro Implacable:** Descarta automáticamente lo que no cumple los "Deal Breakers" (Visa, Remoto, Salario).
*   **Investigación Profunda:** No se queda con lo que dice la oferta; investiga la reputación de la empresa, noticias recientes y el equipo.
*   **Objetividad:** Elimina el sesgo emocional inicial y te da un puntaje frío basado en la compatibilidad real con tu perfil profesional.

## 3. Flujo de Usuario (User Journey)

### Paso 1: Ingesta (El "Input")
El usuario alimenta al sistema de forma rápida y sin fricción.
*   **Entrada:** URL de LinkedIn/Glassdoor/Web o Texto pegado de un correo/mensaje.
*   **Procesamiento:** Scraping avanzado con `primp` (Chrome Impersonation) para saltar bloqueos (WAF/Cloudflare) o modo manual "Copy-Paste" si falla.

### Paso 2: El Agente de Investigación (Deep Research)
El sistema actúa como un investigador privado (DuckDuckGo).
*   **Detección de Empresa:** El LLM extrae el nombre de la empresa del texto.
*   **Inteligencia de Mercado:** Busca automáticamente opiniones ("reviews"), despidos ("layoffs") y cultura en fuentes globales.
*   **Contexto Enriquecido:** El resultado de la búsqueda se inyecta en el prompt final del evaluador.

### Paso 3: El Motor de Decisión (Matching & Scoring)
El núcleo del producto. Cruza la información obtenida con tu **Base de Conocimiento Personal (YAML)**.
*   **Strict JSON Mode:** El modelo está forzado a devolver JSON estructurado, eliminando errores de parsing.
*   **Evaluación Anti-Alucinaciones:** Instrucciones estrictas para no inventar requisitos (ej. penalizar por 'Go' si no está en la oferta).

**Criterios de Evaluación (Jerárquicos):**
1.  **Hard Filters (Bloqueantes - Solo rechazo explícito):**
    *   **Remoto:** REJECT solo si menciona explícitamente "Híbrido", "Presencial", "On-site" o "% remoto < 100%".
    *   **Visa:** REJECT solo si menciona explícitamente "No visa sponsorship", "Solo ciudadanos UE/Locales" o similar. Si no lo menciona -> ASUMIR POSIBLE.
    *   **Salario:** REJECT solo si el rango *máximo* publicado es claramente inferior a 52k€ (ej: "30k-40k"). Si no hay salario -> CONTINUAR.
    *   *Principio:* Ante la ausencia de datos, el sistema asume "PASS" y se enfoca en la calidad del match técnico/cultural.
2.  **Soft Skills & Culture Fit:**
    *   Alineación con valores e intereses.
3.  **Tecnología & Experiencia:**
    *   ¿Cubres el 80% del stack crítico?
    *   ¿Tu experiencia es relevante para el desafío propuesto?

### Paso 4: El Reporte Ejecutivo (Output en Español)
El usuario recibe una tarjeta de resumen limpia y directa en la UI.

*   **Puntuación de Compatibilidad (0-100%):** Un número claro.
*   **Veredicto:** `STRONGLY_APPLY`, `APPLY`, `CONSIDER`, `IGNORE`.
*   **Resumen:** Explicación detallada en español de por qué ese score.
*   **Pros (Fortalezas):** Match específico con tu perfil (Nada de "buen sueldo").
*   **Contras (Gaps/Riesgos):** Gaps técnicos reales o alertas de reputación encontradas en web.
*   **Hard Filters Check:** Estado visual de los filtros críticos.

## 4. Requisitos para el MVP (Producto Mínimo Viable)

*   **Base de Conocimiento:** Archivo YAML robusto con tu CV, preferencias, deal breakers e historia laboral.
*   **Interfaz Simple:** CLI (Línea de comandos) o Script simple inicialmente.
*   **Output:** Markdown generado en la consola o archivo.

## 5. Diferencia Estratégica
A diferencia de los "Auto-Appliers" que disparan CVs genéricos, esta herramienta se enfoca en la **calidad de la decisión**. Te prepara para ganar la entrevista, no solo para enviar el CV.
