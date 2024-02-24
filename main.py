from fastapi import FastAPI, File, UploadFile, HTTPException
from speech_to_text import transcribe_file

app = FastAPI()


@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.wav'):
        raise HTTPException(status_code=400, detail="File format not supported. Please upload a .wav file.")

    try:
        file_data = file.file.read()
        commands = transcribe_file(file_data)
        return {"commands": commands}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    finally:
        file.file.close()
