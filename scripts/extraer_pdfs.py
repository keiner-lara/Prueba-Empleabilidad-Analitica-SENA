"""
Extrae texto de los 3 PDFs usando índice para evitar problemas de encoding.
"""
import pdfplumber, os

base = os.path.dirname(os.path.abspath(__file__))
todo = sorted([f for f in os.listdir(base) if f.endswith('.pdf')])

labels = {
    0: 'assessment',
    1: 'insights',   # Insights & Storytelling — lo ignoramos si aparece
    2: 'norma95',
    3: 'norma96',
}

print("PDFs encontrados:")
for i, f in enumerate(todo):
    print(f"  [{i}] {f}")

print()

for i, fname in enumerate(todo):
    path = os.path.join(base, fname)
    with pdfplumber.open(path) as pdf:
        text = ""
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n--- PAGINA ---\n"
    label = labels.get(i, f'pdf_{i}')
    out = os.path.join(base, f'_extracted_{label}.txt')
    with open(out, 'w', encoding='utf-8') as f_out:
        f_out.write(text)
    print(f"OK [{label}] -> {len(text)} chars -> {out}")
