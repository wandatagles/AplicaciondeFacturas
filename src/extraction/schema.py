"""Definición de esquema de extracción para facturas.
Se deriva del prompt proporcionado. Aquí solo definimos estructura y normalización.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any

FIELDS_ORDER = [
    "numero_factura","nis","tarifa","periodo_inicio","periodo_fin","dias_facturados",
    "lectura_actual","lectura_anterior","consumo_kwh","consumo_kw","demanda_media_f",
    "cargo_fijo_mensual","energia_detalle","interes_mora","subsidio","total_mes","gran_total",
    "fecha_emision","fecha_vencimiento"
]

@dataclass
class FieldSpec:
    name: str
    section_anchor: str
    label_keywords: str
    strategy: str
    postprocess: str
    fallback: Any

SCHEMA: List[FieldSpec] = [
    FieldSpec("numero_factura","DATOS DE LA FACTURA","factura no|factura|no. factura","same_row","strip",""),
    FieldSpec("nis","DATOS DEL SUMINISTRO","nis","same_row","strip",""),
    FieldSpec("tarifa","DATOS DEL SUMINISTRO","tarifa","same_row","uppercase",""),
    FieldSpec("periodo_inicio","DATOS DE FACTURA","del","col+1","to_date",""),
    FieldSpec("periodo_fin","DATOS DE FACTURA","al","col+1","to_date",""),
    FieldSpec("dias_facturados","DATOS DE FACTURA","días","same_row","to_int",0),
    FieldSpec("lectura_actual","DATOS DE SU CONSUMO","lectura actual","same_row","to_decimal",0),
    FieldSpec("lectura_anterior","DATOS DE SU CONSUMO","lectura anterior","same_row","to_decimal",0),
    FieldSpec("consumo_kwh","DATOS DE SU CONSUMO","consumo kwh|consumo$","same_row","to_decimal",0),
    FieldSpec("consumo_kw","HISTÓRICO DE CONSUMO","kw$","same_row","to_decimal",0),
    FieldSpec("demanda_media_f","DATOS DE SU CONSUMO","demanda media f|demanda kw","col=CONSUMO","to_decimal",0),
    FieldSpec("cargo_fijo_mensual","DETALLE DE SU FACTURA","cargo fijo mensual|cargo fijo","same_row","to_decimal",0),
    FieldSpec("energia_detalle","INFORMACIÓN COMPLEMENTARIA","kwh","json_block(list)","identity",[]),
    FieldSpec("interes_mora","FINANCIERO","interés por mora","same_row","to_decimal",0),
    FieldSpec("subsidio","FINANCIERO","subsidio","same_row","to_decimal",0),
    FieldSpec("total_mes","TOTAL ESTE MES","total este mes","same_row","to_decimal",0),
    FieldSpec("gran_total","TOTAL ESTE MES","gran total","same_row","to_decimal",0),
    FieldSpec("fecha_emision","DATOS DE FACTURA","fecha emisión","same_row","to_date",""),
    FieldSpec("fecha_vencimiento","DATOS DE FACTURA","fecha vencimiento","same_row","to_date",""),
]
