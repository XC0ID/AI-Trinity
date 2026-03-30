from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat(message: str, history: list = []) -> str:
    history.append({
        "role": "user",
        "content": message
    })

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": "You are EchoMind, a helpful AI assistant."},
            *history
        ]
    )

    reply = response.choices[0].message.content
    history.append({
        "role": "assistant", 
        "content": reply
    })

    return reply, history