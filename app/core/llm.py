import os
import json
import logging
import requests
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
        self.gemini_key = os.getenv("GEMINI_API_KEY")

    def generate(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> str:
        """
        Generates text using the configured LLM provider.
        """
        if self.provider == "ollama":
            return self._call_ollama(prompt, system_prompt, json_mode)
        elif self.provider == "gemini":
             # Placeholder for Gemini implementation
            return "Gemini support not fully implemented yet."
        else:
            raise ValueError(f"Unknown LLM Provider: {self.provider}")

    def _call_ollama(self, prompt: str, system_prompt: Optional[str] = None, json_mode: bool = False) -> str:
        url = f"{self.ollama_base_url}/api/generate"
        
        full_prompt = prompt
        if system_prompt:
            return self._call_ollama_chat(prompt, system_prompt, json_mode)

        payload = {
            "model": self.ollama_model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "num_ctx": 8192,
                "temperature": 0.1,
                "num_gpu": 999,
                "num_predict": 2048
            }
        }
        
        if json_mode:
            payload["format"] = "json"

        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except Exception as e:
            logger.error(f"Ollama API Error: {e}")
            return f"Error calling Ollama: {str(e)}"

    def _call_ollama_chat(self, prompt: str, system_prompt: str, json_mode: bool = False) -> str:
        url = f"{self.ollama_base_url}/api/chat"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.ollama_model,
            "messages": messages,
            "stream": False,
            "options": {
                "num_ctx": 8192,
                "temperature": 0.1,
                "num_gpu": 999,
                "num_predict": 2048
            }
        }
        
        if json_mode:
            payload["format"] = "json"

        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "")
        except Exception as e:
             logger.error(f"Ollama Chat API Error: {e}")
             return f"Error calling Ollama Chat: {str(e)}"
