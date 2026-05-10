import os
import sys

# Aseguramos que src esté en el path para poder importar los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logs.logs import get_logger
from final_pipeline.identificacion import analyze_advanced_mixed_pdf
from extraction_header.exp_llm_pymupdf_text_header import extract_pdf_lines
from extraction.llm_individual import extract_llm_individual_header, obtain_header, invoke_model_unstructured

logger = get_logger()

MINERU_MARKDOWN_PATH = "extractions_result/llm/mineru/markdown/"
PYMUPDF_MARKDOWN_PATH = "extractions_result/llm/pymupdf_text_header/markdown/"

def process_document(file_path: str):
    """
    Ejecuta el pipeline completo para un documento dado:
    1. Identifica si es texto seleccionable o escaneado.
    2. Parsea el documento con la herramienta adecuada (MinerU o PyMuPDF).
    3. Extrae la información utilizando un LLM.
    """
    logger.info(f"Starting pipeline for document: {file_path}")
    
    if not os.path.exists(file_path):
        logger.error(f"File {file_path} does not exist.")
        return
        
    filename = os.path.basename(file_path)
    filename_without_extension, ext = os.path.splitext(filename)
    
    is_scanned = False
    
    # 1. Identificación del documento
    if ext.lower() in [".jpg", ".jpeg", ".png"]:
        logger.info("Document is an image, treating as scanned.")
        is_scanned = True
    elif ext.lower() == ".pdf":
        logger.info("Analyzing PDF to determine if it is scanned or text-based...")
        analysis_result = analyze_advanced_mixed_pdf(file_path)
        
        doc_type = analysis_result.get("document_type", "unknown")
        logger.info(f"Document type detected: {doc_type}")
        
        if doc_type in ["fully_scanned", "mixed_content"]:
            is_scanned = True
        else:
            is_scanned = False
    else:
        logger.error(f"Unsupported file extension: {ext}")
        return

    logger.info("Initializing unstructured model...")
    unstructured_model = invoke_model_unstructured()

    # 2. Parseo y 3. Extracción
    if is_scanned:
        logger.info("Executing MinerU path for scanned document.")
        
        # Asumimos que el markdown ya fue generado por MinerU en la ruta especificada
        markdown_path = os.path.join(MINERU_MARKDOWN_PATH, f"{filename_without_extension}.md")
        
        if not os.path.exists(markdown_path):
            logger.error(f"MinerU markdown file not found at {markdown_path}. Please run MinerU extraction first.")
            return
            
        with open(markdown_path, "r", encoding="utf-8") as f:
            pdf_parsed = f.read()
            
        logger.info("Obtaining header from markdown (MinerU)")
        header = obtain_header(unstructured_model, pdf_parsed)
        
        logger.info(f"Extracting with LLM (with header) from MinerU markdown")
        extract_llm_individual_header(file_path, pdf_parsed, header, "llm", "mineru_header")
        
    else:
        logger.info("Executing PyMuPDF path for text-based document.")
        logger.info("Parsing document with PyMuPDF...")
        
        pdf_parsed_list = extract_pdf_lines(file_path)
        pdf_parsed = "\n".join(pdf_parsed_list)
        
        # Guardamos el markdown generado por consistencia con el flujo de PyMuPDF
        os.makedirs(PYMUPDF_MARKDOWN_PATH, exist_ok=True)
        pymupdf_markdown_path = os.path.join(PYMUPDF_MARKDOWN_PATH, f"{filename_without_extension}.md")
        
        with open(pymupdf_markdown_path, "w", encoding="utf-8") as f:
            f.write(pdf_parsed)
            
        logger.info("Obtaining header from parsed text (PyMuPDF)")
        header = obtain_header(unstructured_model, pdf_parsed)
        
        logger.info(f"Extracting with LLM (with header) from PyMuPDF parsed text")
        extract_llm_individual_header(file_path, pdf_parsed, header, "llm", "pymupdf_text_header")
        
    logger.info("PIPELINE PROCESS HAS FINISHED SUCCESSFULLY")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run the complete document extraction pipeline.")
    parser.add_argument("file_path", help="Path to the document (.pdf or .jpg) to process.")
    args = parser.parse_args()
    
    process_document(args.file_path)
