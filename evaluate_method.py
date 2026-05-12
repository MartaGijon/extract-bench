import sys
import csv
import asyncio
import json
import os
from pathlib import Path
from extract_bench import ReportBuilder, ReportConfig

async def main(method_name, document_type="pdf"):
    extractions_dir = Path(f"extractions_result/llm/{document_type}s/{method_name}")
    ground_truth_dir = Path("ground_truth")
    schema_dir = Path("ground_truth_schema")
    
    if not extractions_dir.exists():
        print(f"Error: {extractions_dir} no existe.")
        return
        
    output_dir = Path(f"evaluations_result/{document_type}s/{method_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    reports_dir = output_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    csv_path = output_dir / "results.csv"
    md_path = output_dir / "results.md"
    
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Archivo", "Puntuación"])
        
    with open(md_path, "w") as f:
        f.write(f"# Resultados de Evaluación - {method_name}\n\n")
        f.write("| Archivo | Puntuación |\n")
        f.write("|---------|------------|\n")
    
    for extracted_file in extractions_dir.glob("*.json"):
        filename = extracted_file.name
        schema_path = schema_dir / f"{extracted_file.stem}-schema.json"
        gold_path = ground_truth_dir / filename
        
        if not schema_path.exists() or not gold_path.exists():
            print(f"Skipping {filename}: missing schema or gold file.")
            continue
            
        print(f"[{method_name}] Evaluating {filename}...")
        try:
            with open(schema_path, "r") as sf, open(gold_path, "r") as gf, open(extracted_file, "r") as ef:
                schema = json.load(sf)
                gold = json.load(gf)
                try:
                    extracted = json.load(ef)
                except json.JSONDecodeError:
                    print(f"  Invalid JSON in extracted file. Assigning score 0.0")
                    score = 0.0
                    
            if 'score' not in locals():
                config = ReportConfig(
                    output_dir=reports_dir, 
                    output_name=extracted_file.stem,
                    save_json=True,
                    save_text=True,
                    save_csv=True,
                    save_markdown=True
                )
                builder = ReportBuilder(config)
                report = await builder.build_async(schema, gold, extracted)
                score = report.overall_score
                builder.save(report)
                
            print(f"  Score: {score}")
        except Exception as e:
            print(f"Error evaluating {filename}: {e}")
            score = "Error"
            
        with open(csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([filename, score])
            
        with open(md_path, "a") as f:
            f.write(f"| {filename} | {score} |\n")
            
        if 'score' in locals():
            del score

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python evaluate_method.py <method_name> [document_type]")
        print("Ejemplo: python evaluate_method.py docling_header")
        print("Ejemplo: python evaluate_method.py docling_header pdf")
        sys.exit(1)
        
    method_name = sys.argv[1]
    document_type = sys.argv[2] if len(sys.argv) > 2 else "pdf"
    asyncio.run(main(method_name, document_type))
