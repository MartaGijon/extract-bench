#!/bin/bash

METHODS=(
    "docling_header"
    "pymupdf_header"
    "pymupdf"
    "pymupdf_text"
    "mineru"
    "mineru_header"
)

for METHOD in "${METHODS[@]}"
do
    echo "=========================================="
    echo "Iniciando evaluación para: $METHOD"
    echo "=========================================="
    .venv/bin/python evaluate_method.py "$METHOD"
    echo "Evaluación para $METHOD completada."
    echo ""
done
