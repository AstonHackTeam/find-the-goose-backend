from fastapi import FastAPI, HTTPException
from pathlib import Path

from speech_to_text import transcribe_file

app = FastAPI()

BASE_DIR = ""  # 修改为你的文件存储目录的绝对路径

@app.get("/upload")
def upload_file(file_name: str):
    if not file_name.endswith('.wav'):
        raise HTTPException(status_code=400, detail="File format not supported. Please upload a .wav file.")

    file_path = Path(BASE_DIR) / file_name
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found.")

    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
            commands = transcribe_file(file_data)
            return {"commands": commands}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
