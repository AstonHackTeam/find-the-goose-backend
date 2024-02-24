from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from speech_to_text import transcribe_streaming_chunk

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    buffer = b""
    buffer_size_threshold = 1024

    try:
        while True:
            data = await websocket.receive_bytes()
            buffer += data
            if len(buffer) >= buffer_size_threshold:
                pass
            else:
                await asyncio.sleep(1)
            response = transcribe_streaming_chunk(buffer)
            for result in response.results:
                commands = keyword_spotting(result.alternatives[0].transcript)
                for command in commands:
                    await websocket.send_text(command)
    except WebSocketDisconnect:
        print("Client disconnected")


def keyword_spotting(text: str) -> List[str]:
    keywords = {"up", "down", "left", "right"}
    found_commands = [keyword for keyword in keywords if keyword in text.lower()]
    return found_commands
