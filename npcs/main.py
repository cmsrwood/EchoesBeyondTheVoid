from Transcriber import Transcriber
from Npc_generator import NPCGenerator
import flask
from flask import request, jsonify
import os

app = flask.Flask(__name__)

# Crear instancias de las clases
transcriber = Transcriber()

@app.route('/npc', methods=['POST'])
def process_request():
    try:
        # Ruta predefinida del archivo de audio
        audio_file_path = os.path.join("../Saved/BouncedWavFiles/Record.wav")
        
        # Verificar si el archivo existe
        if not os.path.exists(audio_file_path):
            return jsonify({"error": f"El archivo de audio no se encontró en la ruta: {audio_file_path}"}), 404
        
        # Transcribir el audio
        audio_text = transcriber.transcribe_audio(audio_file_path)
        
        # Obtener nombre del NPC desde el formulario o JSON
        data = request.get_json() or {}
        npc_name = data.get("npc_name", "NPC")
        
        # Crear un NPC y generar una respuesta
        npc = NPCGenerator(npc_name)
        npc_response = npc.respuesta(audio_text)
        
        return jsonify({
            "npc_name": npc_name,
            "transcription": audio_text,
            "npc_response": npc_response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
