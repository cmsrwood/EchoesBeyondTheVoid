import whisper
import pyaudio

class Transcriber:
    def __init__(self, model_size="medium"):
        # Cargar el modelo de Whisper
        self.model = whisper.load_model(model_size)
        self.fs = 16000  # Frecuencia de muestreo
        self.p = pyaudio.PyAudio()  # Instancia de PyAudio

    def transcribe_audio(self, audio_data):
        print("Transcribiendo...")
        result = self.model.transcribe(audio_data, language="es")  # Set the language to Spanish
        print(f"Texto transcrito: {result['text']}")
        return result["text"]
