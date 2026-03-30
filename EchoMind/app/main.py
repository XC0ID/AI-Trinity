import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model import chat

def main():
    print("🧠 EchoMind is running... (type 'quit' to exit)\n")
    history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        response, history = chat(user_input, history)
        print(f"\nEchoMind: {response}\n")

if __name__ == "__main__":
    main()