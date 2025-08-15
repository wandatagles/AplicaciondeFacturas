"""Adaptador seguro para LLMWhisperer.
NO exponer claves en código: usar variables de entorno.
"""
from __future__ import annotations
from pathlib import Path
from typing import Optional
import logging
import os
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

try:
    from unstract.llmwhisperer import LLMWhispererClientV2
    from unstract.llmwhisperer.client_v2 import LLMWhispererClientException
    _AVAILABLE = True
except ImportError:  # pragma: no cover
    logger.warning("Cliente LLMWhisperer no instalado")
    LLMWhispererClientV2 = object  # type: ignore
    LLMWhispererClientException = Exception  # type: ignore
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
        if not _AVAILABLE:
            return
        try:
            self.client = LLMWhispererClientV2(base_url=self.base_url, api_key=self.api_key)
            logger.info("LLMWhisperer inicializado")
        except Exception as e:  # pragma: no cover
            logger.exception("Fallo inicializando LLMWhisperer: %s", e)
            self.client = None

    def available(self) -> bool:
        return self.client is not None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def convert_pdf(self, pdf_path: Path) -> Optional[str]:
        if not self.available():
            return None
        if not pdf_path.exists() or pdf_path.suffix.lower() != '.pdf':
            logger.error("Ruta inválida: %s", pdf_path)
            return None
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
            logger.error("Respuesta sin result_text válida")
            return None
        except LLMWhispererClientException as e:  # pragma: no cover
            logger.error("Error LLMWhisperer %s", e)
            raise
        except Exception as e:  # pragma: no cover
            logger.exception("Error genérico en conversión: %s", e)
            raise
