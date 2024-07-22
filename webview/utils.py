import io
import base64, asyncio
from pydub import AudioSegment

def read_and_encode_audio(file_path: str, input_format: str) -> str:
    """Reads an audio file from the given file path and encodes it into base64 wav"""
    audio = AudioSegment.from_file(file_path, format=input_format)
    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    wav_data = buffer.getvalue()
    base64_wav = base64.b64encode(wav_data).decode('utf-8')
    return f"data:audio/wav;base64,{base64_wav}"

def read_and_encode_mp3(file_path: str) -> str:
    """Reads an mp3 audio from the given file path and encodes it into base64 wav"""
    return read_and_encode_audio(file_path, "mp3")

def read_and_encode_wav(file_path: str) -> str:
    """Reads a wav audio from the given file path and encodes it into base64 wav"""
    return read_and_encode_audio(file_path, "wav")

def read_and_encode_ogg(file_path: str) -> str:
    """Reads an ogg audio from the given file path and encodes it into base64 wav"""
    return read_and_encode_audio(file_path, "ogg")

def read_and_encode_flac(file_path: str) -> str:
    """Reads a flac audio from the given file path and encodes it into base64 wav"""
    return read_and_encode_audio(file_path, "flac")

def read_and_encode_aac(file_path: str) -> str:
    """Reads an aac audio from the given file path and encodes it into base64 wav"""
    return read_and_encode_audio(file_path, "aac")

def read_and_encode_m4a(file_path: str) -> str:
    """Reads an m4a audio from the given file path and encodes it into base64 wav"""
    return read_and_encode_audio(file_path, "m4a")

def ensure_event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop