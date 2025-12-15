import json
import logging
from typing import Dict, Any

from app.core.llm import LLMClient
from app.core.models import Portfolio, AnalysisResult

logger = logging.getLogger(__name__)

class CareerAgent:
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio
        self.llm = LLMClient()

    def perform_research(self, company_name: str) -> str:
        """Performs deep research on the company."""
        from app.tools.search import search_company_reputation
        return search_company_reputation(company_name)

    def extract_company_name(self, job_text: str) -> str:
        """Simple extraction of company name using LLM to ensure accuracy."""
        prompt = f"""
        Extract ONLY the company name from this job text.
        Output ONLY the name. Do not write full sentences like "The company is...".
        If not found, return 'Unknown'. 
        
        Text substring: {job_text[:500]}
        """
        # Cleaner extraction
        raw_name = self.llm.generate(prompt).strip()
        # Remove common chat prefixes if they still appear
        clean_name = raw_name.replace("The company name is", "").replace("is ", "").replace(".", "").strip()
        return clean_name

    def analyze(self, job_text: str, research_context: str = "") -> AnalysisResult:
        # 1. Prepare Profile Context
        profile_summary = {
            "name": self.portfolio.personal_info.name,
            "title": self.portfolio.personal_info.title,
            "summary": self.portfolio.professional_summary['short'],
            "hard_filters": {
                "salary_min": "52000 EUR",
                "remote": "100% Remote required (or very flexible)",
                "visa": "Needs Sponsorship (Spain/EU) if not already valid"
            },
            "skills": [s.dict() for s in self.portfolio.skills],
        }
        
        profile_json = json.dumps(profile_summary, indent=2, ensure_ascii=False)

        # 2. Construct Prompt
        system_prompt = f"""
        Actúa como un Coach de Carrera y Reclutador Técnico experto para Álvaro (El Candidato).
        
        PERFIL CANDIDATO (JSON):
        {profile_json}

        CONTEXTO INVESTIGACIÓN EMPRESA:
        {research_context if research_context else "No external research available."}

        ESTRATEGIA DE EVALUACIÓN:
        1. **Filtros Duros (CRÍTICOS)**: 
           - **Remoto**: Si dice explícitamente "Presencial", "Híbrido (obligatorio)" -> VERDICT: IGNORE.
           - **Visa**: Si dice "No sponsor", "EU citizens only" -> VERDICT: IGNORE.
           - **Salario**: Si el max es < 52k EUR -> VERDICT: IGNORE.

        2. **Ajuste Técnico y Rol (El Score)**:
           - Analiza gaps entre Skills del Candidato vs Requisitos.
           - **CRÍTICO: NO ALUCINES NI INVENTES REQUISITOS.**
             - Solo evalúa stack técnico mencionado explícitamente en la descripción.
             - Si la oferta NO menciona "Go", NO penalices por falta de Go.
             - Si la oferta NO menciona "AWS", NO penalices por falta de AWS.
           - **Si el Score < 100%**: OBLIGATORIAMENTE debes explicar POR QUÉ en 'cons' (ej: "Falta experiencia en Go", "El rol es Junior", "Stack desconocido").
           - **Si el Score es 100%**: Debe ser un match perfecto en todo.

        INSTRUCCIONES DE SALIDA (ESPAÑOL):
        - Todos los textos de `reasoning_summary`, `pros` y `cons` DEBEN estar en **ESPAÑOL**.
        - **PROS**: Sé ESPECÍFICO sobre el match técnico/cultural.
          - MAL: "Buen salario", "100% remoto".
          - BIEN: "Tu experiencia de 15 años en Java coincide con el stack core", "Haber sido CTO encaja con el liderazgo requerido".
        - **CONS**: Gaps técnicos específicos, dudas sobre la empresa o seniority.

        FORMATO OUTPUT (JSON PURO):
        Debes responder ÚNICAMENTE con el objeto JSON válido.
        NO escribas texto introductorio (ej: "Here is...").
        NO uses bloques de código markdown (```json). Devuelve SOLO el RAW JSON.
        
        {{
          "match_score": <int 0-100>,
          "verdict": "<STRONGLY_APPLY | APPLY | CONSIDER | IGNORE>",
          "reasoning_summary": "<Explicación detallada en ESPAÑOL>",
          "pros": ["<Match específico 1>", "<Match específico 2>"],
          "cons": ["<Gap o Red Flag 1>", "<Gap o Red Flag 2>"],
          "hard_filter_check": {{
            "remote_pass": <boolean true/false>,
            "visa_pass": <boolean true/false>,
            "salary_pass": <boolean true/false>
          }}
        }}
        """

        user_prompt = f"JOB DESCRIPTION:\n{job_text[:6000]}" # Limit job text

        try:
            logger.info("Sending prompt to LLM...")
            # FORCE JSON MODE
            response_text = self.llm.generate(prompt=user_prompt, system_prompt=system_prompt, json_mode=True)
            
            # Robust extraction strategy
            extracted_json = None
            import re

            # Since we forced JSON mode, the response SHOULD be valid JSON directly
            try:
                data = json.loads(response_text)
                return AnalysisResult(**data)
            except json.JSONDecodeError:
                 # Logic for when even json-mode fails or returns extra text (rare in Llama3 but possible)
                 pass

            # Fallback (same as before just in case)
            pattern = re.compile(r'\{.*"match_score".*\}', re.DOTALL)
            match = pattern.search(response_text)
            
            if match:
                potential_json = match.group(0)
                potential_json = re.sub(r'^\s*//.*$', '', potential_json, flags=re.MULTILINE)
                potential_json = re.sub(r',\s*\}', '}', potential_json)
                potential_json = re.sub(r',\s*\]', ']', potential_json)
                data = json.loads(potential_json)
                return AnalysisResult(**data)

            # If all fails
            logger.error(f"LLM Response (Failed extraction): {response_text}")
            raise ValueError(f"Could not extract valid JSON. Raw text: {response_text[:500]}...")

        except Exception as e:
            logger.error(f"Agent Analysis Error: {e}")
            return AnalysisResult(
                match_score=0, 
                verdict="ERROR", 
                reasoning_summary=f"**Error de Análisis de IA**:\n\n{str(e)}\n\n**Texto recibido (Debug)**:\n```\n{response_text if 'response_text' in locals() else 'No response'}\n```",
                pros=[], cons=[]
            )
