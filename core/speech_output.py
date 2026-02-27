# core/speech_output.py
from gtts import gTTS
from config.languages import LANGUAGE_CONFIG

class VoiceOutput:
    def speak(self, text, language):
        gtts_code = LANGUAGE_CONFIG[language]["gtts_code"]
        tts = gTTS(text=text, lang=gtts_code, slow=False)
        audio_path = "response.mp3"
        tts.save(audio_path)
        return audio_path