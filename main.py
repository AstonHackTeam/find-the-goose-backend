from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from pathlib import Path
import os

from speech_to_text import transcribe_file, transcribe_file_whisper

app = FastAPI()

BASE_DIR = "C:/Users/yuxin/Documents/GitHub/godot-frontend"  # 修改为你的文件存储目录的绝对路径
# BASE_DIR = "C:/Users/yuxin/Downloads/audio_mic_record/mic_record"  # 修改为你的文件存储目录的绝对路径

class UploadFileSchema(BaseModel):
    file_name: str

@app.post("/upload")
async def upload_file(request: UploadFileSchema):
    file_name = request.file_name

    if not file_name.endswith('.wav'):
        raise HTTPException(status_code=400, detail="File format not supported. Please upload a .wav file.")

    file_path = Path(BASE_DIR) / file_name
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found.")

    # try:
    with open(file_path, "rb") as file:
        file_data = file.read()
        commands = transcribe_file(file_data)
        return {"commands": commands}
        # commands = transcribe_file_whisper(file_path)
        # return {"commands": commands}
    # except Exception as e:
        # raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    # finally:
        # 在finally块中确保文件关闭，并且在处理后删除文件
        # file.close()
        # os.remove(file_path)
