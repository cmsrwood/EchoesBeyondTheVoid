import whisper

class Transcriber:
    def __init__(self, model_size="medium"):
        # Cargar el modelo de Whisper
        self.model = whisper.load_model(model_size)

    def transcribe_audio(self, audio_data):
        print("Transcribiendo...")
        result = self.model.transcribe(audio_data, language="es")
        print(f"Texto transcrito: {result['text']}")
        return result["text"]
