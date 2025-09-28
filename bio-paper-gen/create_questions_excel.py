import pandas as pd
from pathlib import Path

# Path to save file
out_path = Path("data/questions.xlsx")
out_path.parent.mkdir(exist_ok=True)

# Sample questions
data = [
    {"id": 1, "chapter": "1", "marks": 1, "question_text": "What is the basic unit of life?"},
    {"id": 2, "chapter": "1", "marks": 2, "question_text": "Explain two differences between prokaryotic and eukaryotic cells."},
    {"id": 3, "chapter": "2", "marks": 3, "question_text": "Describe the structure and function of mitochondria."},
    {"id": 4, "chapter": "2", "marks": 5, "question_text": "Explain the process of photosynthesis in detail."},
    {"id": 5, "chapter": "3", "marks": 1, "question_text": "Define gene."},
    {"id": 6, "chapter": "3", "marks": 2, "question_text": "What is the role of tRNA in protein synthesis?"},
    {"id": 7, "chapter": "4", "marks": 3, "question_text": "Differentiate between mitosis and meiosis."},
    {"id": 8, "chapter": "4", "marks": 5, "question_text": "Explain Mendel’s law of segregation with an example."},
    {"id": 9, "chapter": "5", "marks": 2, "question_text": "What are enzymes? Give an example."},
    {"id": 10, "chapter": "5", "marks": 3, "question_text": "Discuss factors affecting enzyme activity."},
]

# Save to Excel
df = pd.DataFrame(data)
df.to_excel(out_path, index=False)

print(f"Saved: {out_path}  (rows: {len(df)})")

