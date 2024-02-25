from typing import List

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
import whisper

model = whisper.load_model("base")
client = SpeechClient()

project_id = "civil-tube-405901"
recognition_config = cloud_speech.RecognitionConfig(
    auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
    language_codes=["en-US"],
    model="long",
)

def transcribe_file_whisper(file_path)->List[str]:
    file_path_str = str(file_path)
    print(file_path_str)
    result = model.transcribe(file_path_str)
    text = result["text"]
    return keyword_spotting(text)

def transcribe_file(audio: bytes) -> List[str]:
    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        config=recognition_config,
        content=audio,
    )
    response = client.recognize(request=request)
    commands = []
    for result in response.results:
        text = result.alternatives[0].transcript
        print(text)
        text = text.replace("of","up")
        text = text.replace("dumb", "down").replace("Tom", "down").replace("oh", "up")
        commands += keyword_spotting(text)
    return commands


def keyword_spotting(text: str) -> List[str]:
    keywords = {"up", "down", "left", "right"}
    words = text.lower().split()
    found_commands = [word for word in words if word in keywords]
    print(found_commands)
    return found_commands

