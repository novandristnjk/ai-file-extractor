import os
from fastapi import UploadFile
from util.extractor import extract_text_by_page, chunk_texts
from db.vector_store import VectorStore
from util.embedding import embed_texts
import asyncio
from loguru import logger
from dto.upload import UploadDTO
import srsly
from util.helper import get_md5

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def upload(file: UploadFile, dto: UploadDTO):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    _id = get_md5(file_path)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    if dto.extractFile:
        asyncio.create_task(extract_file(file_path))

    metadata = {
        "fileName": file.filename,
        "path": file_path,
        "id": _id
    }

    srsly.write_json(f"{UPLOAD_DIR}_{_id}.json", metadata)

    return {"status": "uploaded", "path": file_path}

async def get_one(_id):
    try:
        data = srsly.read_json(f"{UPLOAD_DIR}_{_id}.json")
        return data
    except:
        return {"massege": "Document not found"}

async def extract_file(file_path: str):
    logger.info(f"Extracting file {file_path}")
    pages = extract_text_by_page(file_path)

    clean_pages = []
    clean_meta = []

    for i, text in enumerate(pages):
        if text and text.strip():  # skip jika kosong atau hanya whitespace
            clean_pages.append(text)
            clean_meta.append({"page": i + 1})
        else:
            print(f"Skip empty page: {i+1}")

    # embed hanya halaman yang tidak kosong
    vectors = [embed_texts(p) for p in clean_pages]

    vs = VectorStore("default", "index_data")
    vs.upsert(clean_pages, vectors, clean_meta)
    vs.save()
    logger.success(f"Succes extract file {file_path}")
