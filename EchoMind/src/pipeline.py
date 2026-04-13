"""
Pipeline module for EchoMind - orchestrates chat interactions with memory
"""

import os
import yaml
from datetime import datetime
from src.model import chat_with_llm
from src.memory import (
    save_memory, 
    get_relevant_memories, 
    view_all_memories,
    clear_all_memories,
    EchoMindMemory
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


# ═════════════════════════════════════
# EchoMindPipeline Class
# ═════════════════════════════════════
class EchoMindPipeline:
    """Full pipeline orchestrating chat, memory, and LLM interactions."""
    
    def __init__(self, config_path: str):
        """
        Initialize EchoMind pipeline.
        
        Args:
            config_path: Path to config.yaml file
        """
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize memory
        self.memory = EchoMindMemory(self.config)
        
        # Session state
        self.history = []
        self.messages_count = 0
        self.session_start = datetime.now()
    
    def chat(self, user_message: str) -> str:
        """
        Send a message and get response with memory context.
        
        Args:
            user_message: User's input
            
        Returns:
            str: AI response
        """
        # Retrieve relevant memories
        relevant_memories = self.memory.retrieve(user_message)
        
        # Format memories for context
        memory_context = self.memory.format_for_prompt(relevant_memories)
        
        # Build messages with memory context
        messages = [
            {
                'role': 'system',
                'content': f"""You are EchoMind, an AI assistant with long-term memory.
                
{memory_context}

Use these memories naturally in conversation. Never say you can't remember — use the memories provided."""
            }
        ]
        
        # Add conversation history
        messages.extend(self.history)
        
        # Add current user message
        messages.append({'role': 'user', 'content': user_message})
        
        # Get response from LLM
        response = self._get_llm_response(messages)
        
        # Update conversation history
        self.history.append({'role': 'user', 'content': user_message})
        self.history.append({'role': 'assistant', 'content': response})
        
        # Save to memory for future sessions
        self.memory.save(
            f"User: {user_message}\n\nEchoMind: {response}",
            metadata={'timestamp': datetime.now().isoformat()}
        )
        
        # Update counters
        self.messages_count += 1
        
        return response
    
    def _get_llm_response(self, messages: list) -> str:
        """Get response from Groq LLM."""
        from groq import Groq
        from dotenv import load_dotenv
        
        # Ensure API key is loaded
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY not found")
        
        client = Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            model=self.config['model']['name'],
            temperature=self.config['model']['temperature'],
            max_tokens=self.config['model']['max_tokens'],
            messages=messages
        )
        
        return response.choices[0].message.content
    
    def get_memory_count(self) -> int:
        """Get total number of stored memories."""
        return self.memory.count()
    
    def get_stats(self) -> dict:
        """Get session statistics."""
        elapsed = (datetime.now() - self.session_start).total_seconds()
        
        return {
            'messages_in_session': self.messages_count,
            'total_memories': self.memory.count(),
            'session_duration_seconds': round(elapsed, 2),
            'session_start': self.session_start.isoformat()
        }
    
    def clear_memory(self):
        """Clear all stored memories."""
        self.memory.delete_all()
        print("✅ Memory cleared")


__all__ = ['chat', 'EchoMindPipeline']
