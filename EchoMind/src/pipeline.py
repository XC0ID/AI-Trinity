"""
Pipeline module for EchoMind - orchestrates chat interactions with memory
"""

from src.model import chat_with_llm
from src.memory import (
    save_memory, 
    get_relevant_memories, 
    view_all_memories,
    clear_all_memories
)


def chat(user_message: str, history: list = None) -> tuple:
    """
    Main chat pipeline that:
    1. Retrieves relevant memories
    2. Sends message with context to LLM
    3. Saves the interaction to memory
    
    Args:
        user_message: User's input message
        history: Conversation history
        
    Returns:
        tuple: (ai_response, updated_history)
    """
    if history is None:
        history = []
    
    # Retrieve relevant memories based on user message
    relevant_memories = get_relevant_memories(user_message)
    
    # Add memories to history context if available
    if relevant_memories:
        # Optionally prepend to history for LLM context
        pass
    
    # Get response from LLM
    ai_response, updated_history = chat_with_llm(user_message, history)
    
    # Save interaction to memory
    save_memory(user_message, ai_response)
    
    return ai_response, updated_history


__all__ = ['chat']
