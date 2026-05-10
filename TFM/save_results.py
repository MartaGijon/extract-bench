import os
import json
from logs.logs import get_logger
from decimal import Decimal

logger = get_logger()

VLM_RESULTS_PATH = "extractions_result/vlm/"
LLM_RESULTS_PATH = "extractions_result/llm/"


def save_response(response, error, name: str, model_type: str, parser_type: str):
    os.makedirs(VLM_RESULTS_PATH, exist_ok=True)
    os.makedirs(LLM_RESULTS_PATH, exist_ok=True)
    
    if model_type == "vlm":
        base_path = VLM_RESULTS_PATH
    
        if error is not None:
            file_path = os.path.join(base_path, f"{name}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(str(error))
            logger.info(f"Error saved in {file_path}")
        else:
            file_path = os.path.join(base_path, f"{name}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(
                    response,
                    f,
                    indent=4,
                    default=lambda o: float(o) if isinstance(o, Decimal) else o,
                )

            logger.info(f"Response saved in {file_path}")
            
    else:
        if parser_type == "docling":
            base_path = LLM_RESULTS_PATH + "docling/"
            
            if error is not None:
                file_path = os.path.join(base_path, f"{name}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(error))
                logger.info(f"Error saved in {file_path}")
            else:
                file_path = os.path.join(base_path, f"{name}.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(
                        response,
                        f,
                        indent=4,
                        default=lambda o: float(o) if isinstance(o, Decimal) else o,
                    )

                logger.info(f"Response saved in {file_path}")
                
        elif parser_type == "docling_header":
            base_path = LLM_RESULTS_PATH + "docling_header/"
            
            if error is not None:
                file_path = os.path.join(base_path, f"{name}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(error))
                logger.info(f"Error saved in {file_path}")
            else:
                file_path = os.path.join(base_path, f"{name}.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(
                        response,
                        f,
                        indent=4,
                        default=lambda o: float(o) if isinstance(o, Decimal) else o,
                    )

                logger.info(f"Response saved in {file_path}")
            
        elif parser_type == "pymupdf":
            base_path = LLM_RESULTS_PATH + "pymupdf/"
            
            if error is not None:
                file_path = os.path.join(base_path, f"{name}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(error))
                logger.info(f"Error saved in {file_path}")
            else:
                file_path = os.path.join(base_path, f"{name}.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(
                        response,
                        f,
                        indent=4,
                        default=lambda o: float(o) if isinstance(o, Decimal) else o,
                    )

                logger.info(f"Response saved in {file_path}")
        elif parser_type == "pymupdf_text":
            base_path = LLM_RESULTS_PATH + "pymupdf_text/"
            
            if error is not None:
                file_path = os.path.join(base_path, f"{name}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(error))
                logger.info(f"Error saved in {file_path}")
            else:
                file_path = os.path.join(base_path, f"{name}.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(
                        response,
                        f,
                        indent=4,
                        default=lambda o: float(o) if isinstance(o, Decimal) else o,
                    )

                logger.info(f"Response saved in {file_path}")
                
        elif parser_type == "pymupdf_text_header":
            base_path = LLM_RESULTS_PATH + "pymupdf_text_header/"
            
            if error is not None:
                file_path = os.path.join(base_path, f"{name}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(error))
                logger.info(f"Error saved in {file_path}")
            else:
                file_path = os.path.join(base_path, f"{name}.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(
                        response,
                        f,
                        indent=4,
                        default=lambda o: float(o) if isinstance(o, Decimal) else o,
                    )

                logger.info(f"Response saved in {file_path}")
                
        elif parser_type == "pymupdf_header":
            base_path = LLM_RESULTS_PATH + "pymupdf_header/"
            
            if error is not None:
                file_path = os.path.join(base_path, f"{name}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(error))
                logger.info(f"Error saved in {file_path}")
            else:
                file_path = os.path.join(base_path, f"{name}.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(
                        response,
                        f,
                        indent=4,
                        default=lambda o: float(o) if isinstance(o, Decimal) else o,
                    )

                logger.info(f"Response saved in {file_path}")
                
        elif parser_type == "mineru":
            base_path = LLM_RESULTS_PATH + "mineru/"
            
            if error is not None:
                file_path = os.path.join(base_path, f"{name}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(error))
                logger.info(f"Error saved in {file_path}")
            else:
                file_path = os.path.join(base_path, f"{name}.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(
                        response,
                        f,
                        indent=4,
                        default=lambda o: float(o) if isinstance(o, Decimal) else o,
                    )

                logger.info(f"Response saved in {file_path}")
                
        elif parser_type == "mineru_header":
            base_path = LLM_RESULTS_PATH + "mineru_header/"
            
            if error is not None:
                file_path = os.path.join(base_path, f"{name}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(error))
                logger.info(f"Error saved in {file_path}")
            else:
                file_path = os.path.join(base_path, f"{name}.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(
                        response,
                        f,
                        indent=4,
                        default=lambda o: float(o) if isinstance(o, Decimal) else o,
                    )

                logger.info(f"Response saved in {file_path}")

        elif parser_type == "final_pipeline":
            base_path = LLM_RESULTS_PATH + "final_pipeline/"
            
            os.makedirs(base_path, exist_ok=True)
            if error is not None:
                file_path = os.path.join(base_path, f"{name}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(str(error))
                logger.info(f"Error saved in {file_path}")
            else:
                file_path = os.path.join(base_path, f"{name}.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(
                        response,
                        f,
                        indent=4,
                        default=lambda o: float(o) if isinstance(o, Decimal) else o,
                    )

                logger.info(f"Response saved in {file_path}")
