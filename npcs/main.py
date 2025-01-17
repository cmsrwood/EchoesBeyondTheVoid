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
        content_type = request.headers.get('Content-Type')
        
        # Si el cliente envía un archivo de audio (multipart/form-data)
        if content_type and 'multipart/form-data' in content_type:
            if 'audio' not in request.files:
                return jsonify({"error": "No se encontró un archivo de audio."}), 400
            
            # Guardar el archivo temporalmente
            audio_file = request.files['audio']
            audio_path = os.path.join("temp_audio.wav")
            audio_file.save(audio_path)
            
            # Transcribir el audio
            audio_text = transcriber.transcribe_audio(audio_path)
            os.remove(audio_path)  # Limpiar archivo temporal
            
            # Crear un NPC (opcional: nombre desde JSON si se incluye)
            npc_name = request.form.get("name_npc", "NPC")
            npc = NPCGenerator(npc_name)
            
            # Generar respuesta del NPC basado en la transcripción
            npc_response = npc.respuesta(audio_text)
            
            return jsonify({
                "transcription": audio_text,
                "npc_name": npc_name,  # Nombre del NPC
                "npc_response": npc_response  # Respuesta generada por el NPC
            })


        # Si el cliente envía datos JSON (application/json)
        elif content_type and 'application/json' in content_type:
            data = request.json
            user_message = data.get("message", "")
            
            if not user_message:
                return jsonify({"error": "El mensaje no puede estar vacío."}), 400
            
            # Crear un NPC (opcional: nombre desde JSON si se incluye)
            npc_name = data.get("npc_name", "NPC")
            npc = NPCGenerator(npc_name)
            
            # Generar respuesta del NPC
            npc_response = npc.respuesta(user_message)
            
            return jsonify({
                "text": npc_response
            })

        else:
            return jsonify({"error": "Tipo de contenido no soportado. Usa 'application/json' o 'multipart/form-data'."}), 415

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
