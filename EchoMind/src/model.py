import os
from groq import Groq
from dotenv import load_dotenv
import yaml

# Fix: Load .env from EchoMind root, not current folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")
ENV_PATH = os.path.join(BASE_DIR, ".env")

# Load .env explicitly with full path
load_dotenv(dotenv_path=ENV_PATH)

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# Debug: confirm key is loaded
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=api_key)

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
                with long-term memory. When given past memories 
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