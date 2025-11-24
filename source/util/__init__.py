import fitz 

def extract_text_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        text = page.get_text("text")
        pages.append(text)
    doc.close()
    return pages

def chunk_text(text, max_chars=800):
    for i in range(0, len(text), max_chars):
        yield text[i:i+max_chars]
