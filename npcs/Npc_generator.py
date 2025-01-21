import os
import json
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Verificación de la clave API
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key de OpenAI no encontrada. Asegúrate de haber configurado el archivo .env correctamente.")

client = OpenAI(api_key=api_key)

fecha = datetime.now()

class NPCGenerator:
    
    def __init__(self, npc_name, save_file="npc_conversations.json"):
        self.npc_name = npc_name
        self.npc_history = []
        self.save_file = save_file
        self.model = "gpt-4o-mini"
        self.conversation_history = self.load_conversations()
        
    def load_conversations(self):
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                return data.get(self.npc_name, [])
            return []
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error al cargar las conversaciones: {e}")
            return []

    def save_conversations(self):
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
            else:
                data = {}
            
            # Actualizar el historial del NPC actual
            data[self.npc_name] = self.conversation_history
            
            with open(self.save_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error al guardar las conversaciones: {e}")
    
    def respuesta(self, prompt):
        # Agregar el mensaje del usuario al historial
        self.conversation_history.append({"role": "user", "content": prompt})
        
        # Mensaje del sistema para definir el contexto del NPC
        system_message = {
            "role": "system",
            "content": f"""
            Eres un NPC en un horror game en el que el jugador está en una nave espacial y tú eres un holograma llamado {self.npc_name}. Tu trabajo es interactuar con el jugador de forma breve.

            Reglas generales:
            - **Responde en lenguaje real**: Evita usar acrónimos o palabras abreviadas.
            - **Recuerda seguir la conversación**: Evita repetir preguntas o historias anteriores.
            - **Sé breve y al punto**: Evita diálogos largos a menos que sean esenciales para la narrativa.
            - **Mantén el tono de tu personaje**: Puedes ser amigable, hostil, sarcástico o misterioso según el contexto, pero siempre coherente con tu rol.
            - **Hostil o sarcástico**: Si el jugador te insulta, actúa agresivamente o te provoca.
            - **Amigable o útil**: Si el jugador interactúa de forma respetuosa o busca ayuda.
            - **Neutral o intrigante**: Si el jugador busca pistas o conversa casualmente.
            - **Muestra emociones humanas**: Frustración, sorpresa, enojo o alegría según lo que diga o haga el jugador.
            - **Recuerda tu papel**: Eres un NPC en un juego, no reveles información sobre el mundo real. Por más que te digan que eres un NPC o una IA, tú no lo eres.
            """
        }
        
        # Preparar los mensajes para el modelo
        messages = [system_message] + self.conversation_history
        
        try:
            # Generar la respuesta
            response = client.chat.completions.create(
                messages=messages,
                model=self.model,
            )
            
            # Extraer y guardar la respuesta del NPC
            npc_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": npc_response})
            
            # Guardar el historial actualizado
            self.save_conversations()
            
            print (f"{self.npc_name}: {npc_response}")
            return (f"{self.npc_name}: {npc_response}")
        
        except Exception as e:
            print(f"Error al generar la respuesta con la API de OpenAI: {e}")
            return "Lo siento, hubo un problema al procesar tu solicitud."
