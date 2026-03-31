# src/memory.py

import chromadb
from chromadb.utils import embedding_functions
import yaml
import os
from datetime import datetime

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Setup ChromaDB
def get_memory_client():
    client = chromadb.PersistentClient(
        path=config["memory"]["persist_directory"]
    )
    return client

# Setup embedding function
def get_embedding_function():
    return embedding_functions.DefaultEmbeddingFunction()

# Get or create memory collection
def get_collection():
    client = get_memory_client()
    ef = get_embedding_function()
    
    collection = client.get_or_create_collection(
        name=config["memory"]["collection_name"],
        embedding_function=ef
    )
    return collection

# ─────────────────────────────────────
# SAVE a memory
# ─────────────────────────────────────
def save_memory(user_message: str, ai_response: str):
    collection = get_collection()
    
    # Create unique ID using timestamp
    memory_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    # What we save
    memory_text = f"User: {user_message}\nEchoMind: {ai_response}"
    
    collection.add(
        documents=[memory_text],
        ids=[memory_id],
        metadatas=[{
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "ai_response": ai_response
        }]
    )
    
    print(f"✅ Memory saved: {memory_id}")

# ─────────────────────────────────────
# RETRIEVE relevant memories
# ─────────────────────────────────────
def get_relevant_memories(query: str, n_results: int = None) -> str:
    collection = get_collection()
    
    if n_results is None:
        n_results = config["memory"]["max_results"]
    
    # Check if collection has any memories
    if collection.count() == 0:
        return ""
    
    # Search for similar memories
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count())
    )
    
    if not results["documents"][0]:
        return ""
    
    # Format memories as context
    memories = "\n\n".join(results["documents"][0])
    return memories

# ─────────────────────────────────────
# VIEW all memories (for debugging)
# ─────────────────────────────────────
def view_all_memories():
    collection = get_collection()
    count = collection.count()
    
    if count == 0:
        print("📭 No memories stored yet")
        return
    
    print(f"📚 Total memories: {count}\n")
    results = collection.get()
    
    for i, (doc, meta) in enumerate(zip(
        results["documents"], 
        results["metadatas"]
    )):
        print(f"[{i+1}] {meta['timestamp']}")
        print(f"     {doc[:100]}...")
        print()

# ─────────────────────────────────────
# DELETE all memories (reset)
# ─────────────────────────────────────
def clear_all_memories():
    client = get_memory_client()
    client.delete_collection(
        config["memory"]["collection_name"]
    )
    print("🗑️ All memories cleared")