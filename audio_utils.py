import os
import tempfile
from gtts import gTTS

def text_to_audio_file(text: str) -> str:
    """Converts text to an MP3 audio file safely using a temporary file."""
    try:
        fd, temp_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd) 
        
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(temp_path)
        
        return temp_path
    except Exception as e:
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        raise RuntimeError(f"Failed to generate audio: {str(e)}")

def remove_temp_file(path: str):
    """Utility to securely delete the file after sending."""
    if os.path.exists(path):
        os.remove(path)