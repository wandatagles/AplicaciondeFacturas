"""Adaptador seguro para LLMWhisperer.
NO exponer claves en código: usar variables de entorno.
"""
from __future__ import annotations
from pathlib import Path
from typing import Optional
import logging
import os
from tenacity import retry, stop_after_attempt, wait_exponential
import httpx

logger = logging.getLogger(__name__)

try:  # Intento de SDK oficial (si en el futuro existe en entorno interno)
    from unstract.llmwhisperer import LLMWhispererClientV2  # type: ignore
    from unstract.llmwhisperer.client_v2 import LLMWhispererClientException  # type: ignore
    _AVAILABLE = True
except Exception:  # pragma: no cover
    logger.info("Usando modo HTTP directo para LLMWhisperer")
    LLMWhispererClientV2 = object  # type: ignore
    class LLMWhispererClientException(Exception): ...  # type: ignore
    _AVAILABLE = False

DEFAULT_BASE_URL = "https://llmwhisperer-api.us-central.unstract.com/api/v2"

class WhisperStructuredExtractor:
    def __init__(self, api_key: Optional[str] = None, base_url: str = DEFAULT_BASE_URL):
        self.api_key = api_key or os.getenv("LLMWHISPERER_API_KEY")
        self.base_url = base_url.rstrip('/')
        self.client = None
        if not self.api_key:
            logger.error("API key de LLMWhisperer no configurada (LLMWHISPERER_API_KEY)")
            return
        if _AVAILABLE:
            try:  # pragma: no cover
                self.client = LLMWhispererClientV2(base_url=self.base_url, api_key=self.api_key)
                logger.info("LLMWhisperer inicializado (SDK)")
            except Exception as e:
                logger.exception("Fallo inicializando LLMWhisperer SDK: %s", e)
                self.client = None

    def available(self) -> bool:
        return self.client is not None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def convert_pdf(self, pdf_path: Path) -> Optional[str]:
        if not pdf_path.exists() or pdf_path.suffix.lower() != '.pdf':
            logger.error("Ruta inválida: %s", pdf_path)
            return None
        if self.client is not None:
            try:
                result = self.client.whisper(
                    file_path=str(pdf_path),
                    wait_for_completion=True,
                    wait_timeout=300,
                    mode="table",
                    output_mode="layout_preserving",
                    mark_vertical_lines=True,
                    mark_horizontal_lines=True,
                )
                if result and 'extraction' in result and 'result_text' in result['extraction']:
                    return result['extraction']['result_text']
                logger.error("Respuesta sin result_text válida (SDK)")
                return None
            except Exception as e:  # pragma: no cover
                logger.exception("Error SDK LLMWhisperer: %s", e)
                # Continuar a fallback HTTP

        # Fallback HTTP (multipart upload)
        try:
            headers = {"x-api-key": self.api_key}
            with pdf_path.open('rb') as fh:
                files = {"file": (pdf_path.name, fh, 'application/pdf')}
                data = {
                    "mode": "table",
                    "output_mode": "layout_preserving",
                    "mark_vertical_lines": "true",
                    "mark_horizontal_lines": "true",
                }
                resp = httpx.post(f"{self.base_url}/whisper", headers=headers, data=data, files=files, timeout=300)
            if resp.status_code >= 400:
                logger.error("Error HTTP %s: %s", resp.status_code, resp.text[:500])
                return None
            payload = resp.json()
            extraction = payload.get('extraction', {})
            text = extraction.get('result_text') or extraction.get('text')
            if text:
                return text
            logger.error("Respuesta sin result_text en fallback HTTP")
            return None
        except Exception as e:  # pragma: no cover
            logger.exception("Fallo en fallback HTTP: %s", e)
            return None
