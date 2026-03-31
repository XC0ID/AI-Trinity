from groq import Groq
from dotenv import load_dotenv
import yaml
import os

load_dotenv()

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat_with_llm(message: str, history: list = []) -> tuple:
    
    history.append({
        "role": "user",
        "content": message
    })
    
    response = client.chat.completions.create(
        model=config["model"]["name"],
        temperature=config["model"]["temperature"],
        max_tokens=config["model"]["max_tokens"],
        messages=[
            {
                "role": "system",
                "content": """You are EchoMind, an AI assistant 
                with a long-term memory. When given past memories 
                as context, use them naturally in conversation. 
                Never say you can't remember — use the memories 
                provided to you."""
            },
            *history
        ]
    )
    
    reply = response.choices[0].message.content
    
    history.append({
        "role": "assistant",
        "content": reply
    })
    
    return reply, history