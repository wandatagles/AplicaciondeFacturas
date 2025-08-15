"""Pipeline de extracción de facturas.
Contempla pasos:
1. Conversión PDF -> texto estructurado (Whisper)
2. Orquestación LLM (LangChain / CrewAI) - PENDIENTE implementación real
3. Normalización a DataFrame
Las claves se cargan desde variables de entorno (dotenv).
"""
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
import os
import logging
import pandas as pd
from .whisper_client import WhisperStructuredExtractor
from . import schema

logger = logging.getLogger(__name__)

class InvoiceExtractionResult:
    def __init__(self, rows: List[Dict[str, Any]], warnings: List[str]):
        self.rows = rows
        self.warnings = warnings
    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(self.rows)
        # Reordenar columnas
        cols = [c for c in schema.FIELDS_ORDER if c in df.columns]
        return df.reindex(columns=cols)

class InvoiceExtractionPipeline:
    def __init__(self, whisper: WhisperStructuredExtractor | None = None):
        self.whisper = whisper or WhisperStructuredExtractor()
        # place-holders para futuros componentes: llm_chain, crew, etc.
        self.chat_provider = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def extract_batch(self, pdf_paths: List[Path], max_docs: int = 5) -> InvoiceExtractionResult:
        selected = pdf_paths[:max_docs]
        remaining = len(pdf_paths) - len(selected)
        warnings: List[str] = []
        rows: List[Dict[str, Any]] = []
        if remaining > 0:
            warnings.append(f"Quedan {remaining} pendientes en la cola")
        for p in selected:
            txt = self.whisper.convert_pdf(p) if self.whisper.available() else None
            if not txt:
                warnings.append(f"No se pudo convertir {p.name}")
                continue
            # TODO: invocar cadena LLM para extraer campos -> por ahora stub
            extracted = {field: None for field in schema.FIELDS_ORDER}
            extracted["numero_factura"] = p.stem
            rows.append(extracted)
        return InvoiceExtractionResult(rows, warnings)
