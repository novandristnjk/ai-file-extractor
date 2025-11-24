import fitz # pymupdf
from typing import List, Iterable

def extract_text_by_page(pdf_path: str) -> List[str]:
    """Return list of page texts."""
    pages = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text = page.get_text("text")
            pages.append(text)
    return pages

def chunk_texts(text: str, max_chars: int = 1000) -> Iterable[str]:
    """Yield text chunks of approx `max_chars` length. Tries to split on paragraph/newline boundaries."""
    text = (text or "").strip()
    if not text:
        return

    paras = [p.strip() for p in text.split('\n\n') if p.strip()]

    cur = ""
    for p in paras:
        if len(cur) + len(p) + 2 <= max_chars:
            cur = (cur + "\n\n" + p).strip() if cur else p
        else:
            if cur:
                yield cur
            if len(p) <= max_chars:
                cur = p
            else:
                for i in range(0, len(p), max_chars):
                    yield p[i:i+max_chars]
            cur = ""
    if cur:
        yield cur