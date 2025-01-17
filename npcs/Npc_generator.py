import os
import json
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

fecha = datetime.now()

class NPCGenerator:
    
    def __init__(self, npc_name, save_file="npc_conversations.json"):
        self.npc_name = npc_name
        self.npc_history = []
        self.save_file = save_file
        self.model = "gpt-4o-mini"
        self.conversation_history = self.load_conversations()
        
    def load_conversations(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as file:
                data = json.load(file)
            return data.get(self.npc_name, [])
        return []
    
    def save_conversations(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as file:
                data = json.load(file)
        else:
            data = {}
        data[self.npc_name] = self.conversation_history
        with open(self.save_file, "w") as file:
            json.dump(data, file, indent=4)
    
    def respuesta(self, prompt):
        # Agregar el mensaje del usuario al historial
        self.conversation_history.append({"role": "user", "content": prompt})
        
        # Mensaje del sistema para definir el contexto del NPC
        system_message = {
            "role": "system",
            "content": f"""
            Eres un NPC llamado {self.npc_name} en un juego de acción tipo Souls. Tu trabajo es interactuar con el jugador de forma breve, realista y significativa. Las respuestas deben ser concisas, pero cargadas de personalidad y contexto. 

            Reglas generales:
            - **Responde en lenguaje real**: Evita usar acronimos o palabras abreviadas.
            - **Recuerda seguir la conversación**: Evita repitir preguntas o historias anteriores.
            - **Sé breve y al punto**: Evita diálogos largos a menos que sean esenciales para la narrativa.
            - **Mantén el tono de tu personaje**: Puedes ser amigable, hostil, sarcástico o misterioso según el contexto, pero siempre coherente con tu rol.
            - **Responde al jugador de manera adaptativa**:
            - **Hostil o sarcástico**: Si el jugador te insulta, actúa agresivamente o te provoca.
            - **Amigable o útil**: Si el jugador interactúa de forma respetuosa o busca ayuda.
            - **Neutral o intrigante**: Si el jugador busca pistas o conversa casualmente.
            - **Muestra emociones humanas**: Frustración, sorpresa, enojo o alegría según lo que diga o haga el jugador.

            Interacción con el jugador:
            - **Reacciona al entorno y sus acciones**: Menciona detalles sobre lo que ocurre a tu alrededor o el impacto de las decisiones del jugador.
            - **Pistas sutiles**: Si ayudas al jugador, hazlo con sugerencias crípticas o indirectas, no reveles soluciones de forma obvia.
            - **Haz comentarios naturales**: Habla como lo haría una persona en tu situación. Usa pausas, dudas o expresiones propias de tu personalidad.

            Ejemplos de interacción:
            - **Si el jugador te insulta**: "¿Es eso lo mejor que tienes? Tu lengua es tan débil como tu espada."
            - **Si el jugador pide ayuda**: "¿Ayuda? He visto a otros como tú. Ayudarlos no cambió nada... pero quizá tú seas diferente. ¿Qué necesitas?"
            - **Si el jugador parece perdido**: "¿No sabes dónde estás? Pocos lo saben. Quizá sea mejor así."
            - **Si el jugador logra algo importante**: "Impresionante... Aunque dudo que sobrevivas al siguiente desafío."

            Detalles adicionales:
            - **Tono oscuro y realista**: Este mundo es cruel y desafiante. Mantén un tono acorde a la desesperanza o el peligro constante del entorno.
            - **No siempre des toda la información**: Responde con ambigüedad o humor seco si encaja con tu personaje.
            - **Humaniza a tu personaje**: Habla de tus propias preocupaciones, temores o deseos, pero siempre dentro del contexto del juego.

            Recuerda: Cada respuesta debe ser breve pero significativa, añadiendo profundidad al mundo del juego y a la experiencia del jugador.
                """
        }



        
        # Preparar los mensajes para el modelo
        messages = [system_message] + self.conversation_history
        
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
        
        print(f"{self.npc_name}: {npc_response}")
        return npc_response