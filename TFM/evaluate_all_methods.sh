#!/bin/bash

# Este script evalúa todos los métodos de extracción disponibles
# y asume que se ejecuta desde el directorio raíz del proyecto (extract-bench)

METHODS=(
    "docling"
    "docling_header"
    "mineru"
    "mineru_header"
    "pymupdf"
    "pymupdf_header"
    "pymupdf_text"
    "pymupdf_text_header"
)

# Activar el entorno virtual si existe
if [ -d ".venv" ]; then
    PYTHON_CMD=".venv/bin/python"
else
    PYTHON_CMD="python"
fi

# Buscar dónde está evaluate_method.py
if [ -f "TFM/evaluate_method.py" ]; then
    SCRIPT_PATH="TFM/evaluate_method.py"
elif [ -f "evaluate_method.py" ]; then
    SCRIPT_PATH="evaluate_method.py"
else
    echo "Error: No se encontró evaluate_method.py en el directorio actual ni en TFM/"
    exit 1
fi

for METHOD in "${METHODS[@]}"
do
    echo "=========================================="
    echo "Iniciando evaluación para: $METHOD"
    echo "=========================================="
    
    $PYTHON_CMD $SCRIPT_PATH "$METHOD"
    
    echo "Evaluación para $METHOD completada."
    echo ""
done

echo "=========================================="
echo "Todas las evaluaciones han finalizado."
echo "=========================================="
