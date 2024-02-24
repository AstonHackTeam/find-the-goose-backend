from typing import List

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

client = SpeechClient()

project_id = "find-the-goose"
recognition_config = cloud_speech.RecognitionConfig(
    auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
    language_codes=["en-US"],
    model="long",
)


def transcribe_file(audio: bytes) -> List[str]:
    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        config=recognition_config,
        content=audio,
    )
    response = client.recognize(request=request)
    commands = []
    for result in response.results:
        commands += keyword_spotting(result.alternatives[0].transcript)
    return commands


def keyword_spotting(text: str) -> List[str]:
    keywords = {"up", "down", "left", "right"}
    found_commands = [keyword for keyword in keywords if keyword in text.lower()]
    return found_commands
