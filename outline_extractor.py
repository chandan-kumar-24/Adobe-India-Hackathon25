import fitz  # PyMuPDF
import json
import os

def extract_headings_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    outline = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if block['type'] == 0:
                for line in block["lines"]:
                    text = " ".join(span["text"] for span in line["spans"]).strip()
                    font_size = line["spans"][0]["size"]
                    if len(text) > 5 and font_size > 8:
                        level = "H1" if font_size > 18 else "H2" if font_size > 14 else "H3"
                        outline.append({
                            "level": level,
                            "text": text,
                            "page": page_num + 1
                        })

    return {
        "title": os.path.splitext(os.path.basename(pdf_path))[0],
        "outline": outline
    }

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))

            result = extract_headings_from_pdf(pdf_path)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()
