from fastapi import FastAPI, UploadFile, File, Depends
import os
from service.upload import upload, get_one
from service.chat import chat
import argparse
import uvicorn
import traceback
from dto.chat import ChatDTO
from dto.upload import UploadDTO
from util.extractor import extract_text_by_page
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        # "http://localhost:5173",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INDEX_DIR = "index_data"
os.makedirs(INDEX_DIR, exist_ok=True)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), dto: UploadDTO = Depends()):
    data = await upload(file, dto)

    return data

@app.get("/docs")
async def get_one(_id: str):
    data = get_one(_id)

    return data

@app.post("/index")
async def extract_file(_id: str):
    data = get_one(_id)
    extract_file(data.get("path"))

    return data

@app.post("/chat")
async def ask(dto: ChatDTO):
    try:
        response = await chat(dto.query, collection="default", persist_dir=INDEX_DIR)
    except Exception as e:
        print(e)
        traceback.print_exc()

    return response

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    ) 

    argument_parser.add_argument('-p', '--port', help='Port', metavar='', default=8000, type=int)
    argument_parser.add_argument('-w', '--worker', help='Worker', metavar='', default=1, type=int)
    args = argument_parser.parse_args()

    uvicorn.run("main:app", host="0.0.0.0", port=args.port, workers=args.worker, reload=True)