import csv

def calculate_mean_score(csv_path):
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            scores = []
            for row in reader:
                val = row.get('Puntuación', '')
                if val != 'Error' and val.strip() != '':
                    try:
                        scores.append(float(val))
                    except ValueError:
                        pass
            
            if not scores:
                print("No hay puntuaciones válidas todavía.")
                return
                
            mean = sum(scores) / len(scores)
            print(f"Archivos evaluados con éxito: {len(scores)}")
            print(f"Puntuación media actual de docling: {mean:.4f}")
    except FileNotFoundError:
        print(f"No se encontró el archivo: {csv_path}")

if __name__ == "__main__":
    calculate_mean_score("evaluations_result/docling/results.csv")
