from typing import List
import whisper

model = whisper.load_model("base")

def transcribe_file_whisper(file_path)->List[str]:
    file_path_str = str(file_path)
    print(file_path_str)
    result = model.transcribe(file_path_str)
    text = result["text"]
    return keyword_spotting(text)


def keyword_spotting(text: str) -> List[str]:
    keywords = {"up", "down", "left", "right"}
    found_commands = [keyword for keyword in keywords if keyword in text.lower()]
    return found_commands
