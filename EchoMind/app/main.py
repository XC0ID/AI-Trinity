import sys
from pathlib import Path
import os

# Add parent directory to path so src module can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline import chat
from src.memory import view_all_memories, clear_all_memories
from src.utils import setup_logger

os.makedirs("logs", exist_ok=True)
logger = setup_logger()

def main():
    print("=" * 50)
    print("🧠  EchoMind — I remember everything")
    print("=" * 50)
    print("Commands:")
    print("  'quit'      → Exit")
    print("  'memories'  → View all stored memories")
    print("  'clear'     → Clear all memories")
    print("=" * 50 + "\n")
    
    session_history = []
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() == "quit":
                print("\n👋 EchoMind: Goodbye! I'll remember you.")
                break
                
            elif user_input.lower() == "memories":
                view_all_memories()
                continue
                
            elif user_input.lower() == "clear":
                clear_all_memories()
                session_history = []
                print("🔄 All memories and session history cleared.\n")
                continue
            
            response, session_history = chat(
                user_input, 
                session_history
            )
            print(f"\nEchoMind: {response}\n")

        except KeyboardInterrupt:
            print("\n\n👋 EchoMind: Goodbye! I'll remember you.")
            break

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"\n⚠️ Error: {e}\n")


if __name__ == "__main__":
    main()