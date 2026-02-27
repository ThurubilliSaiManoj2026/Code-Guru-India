# core/speech_input.py
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

# Language codes for Whisper
WHISPER_LANG_CODES = {
    "తెలుగు (Telugu)": "te-IN",
    "தமிழ் (Tamil)":   "ta-IN",
    "हिंदी (Hindi)":   "hi-IN",
}

class VoiceInput:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        print("✅ Google Speech Recognition ready!")

    def record_until_silence(
        self,
        sample_rate=16000,
        silence_threshold=0.008,
        min_duration=2,
        max_duration=20,
        silence_duration=1.5
    ):
        """Auto stops when user stops speaking"""
        print("🎙️ Listening... speak now!")
        chunk_size = int(sample_rate * 0.1)
        audio_chunks = []
        silent_chunks = 0
        speaking_started = False
        total_chunks = 0
        max_chunks = int(max_duration / 0.1)
        silence_chunks_needed = int(silence_duration / 0.1)

        with sd.InputStream(
            samplerate=sample_rate,
            channels=1,
            dtype='float32',
            blocksize=chunk_size
        ) as stream:
            while total_chunks < max_chunks:
                chunk, _ = stream.read(chunk_size)
                audio_chunks.append(chunk.copy())
                total_chunks += 1
                volume = np.abs(chunk).mean()
                if volume > silence_threshold:
                    speaking_started = True
                    silent_chunks = 0
                elif speaking_started:
                    silent_chunks += 1
                if (
                    speaking_started
                    and silent_chunks >= silence_chunks_needed
                    and total_chunks >= int(min_duration / 0.1)
                ):
                    print("✅ Speech ended!")
                    break

        audio = np.concatenate(audio_chunks, axis=0)
        return audio, sample_rate

    def transcribe(self, audio, sample_rate, selected_language):
        """Transcribe using Groq Whisper API — most accurate"""
        tmp_path = None
        try:
            # Convert float32 to int16
            audio_int16 = (audio * 32767).astype(np.int16)

            # Save to temp WAV file
            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False
            ) as f:
                tmp_path = f.name
                wav.write(tmp_path, sample_rate, audio_int16)

            # Get language code
            lang_code = WHISPER_LANG_CODES.get(selected_language, "te")

            # Use Groq Whisper API
            with open(tmp_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    file=("audio.wav", audio_file.read()),
                    model="whisper-large-v3",
                    language=lang_code,
                    response_format="text",
                    temperature=0.0
                )

            text = transcription.strip() if isinstance(transcription, str) else transcription.text.strip()

            # Filter garbage outputs
            garbage = [
                "thank you", "thanks for watching", "subscribe",
                ".", ",", "!", "?", "...", "okay", "the", "",
                "you", "bye", "hi", "hello"
            ]
            if not text or text.lower() in garbage or len(text) < 3:
                return "❌ Could not understand. Please speak clearly and try again."

            return text

        except Exception as e:
            return f"❌ Error: {str(e)}"
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)