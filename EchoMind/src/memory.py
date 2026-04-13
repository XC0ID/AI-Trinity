import chromadb
from chromadb.utils import embedding_functions
import yaml
import os
from datetime import datetime

# ✅ FIX — Find config.yaml no matter where you run from
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

# Load config
with open(CONFIG_PATH, "r") as f:       # ← changed this line
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
    
    memory_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
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
    
    if collection.count() == 0:
        return ""
    
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count())
    )
    
    if not results["documents"][0]:
        return ""
    
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


# ═════════════════════════════════════
# EchoMindMemory Class (OOP interface)
# ═════════════════════════════════════
class EchoMindMemory:
    """Object-oriented wrapper for ChromaDB memory operations."""
    
    def __init__(self, config_dict=None):
        """Initialize memory with custom config or default."""
        self.config = config_dict if config_dict else config
        self.collection = None
        self._init_collection()
    
    def _init_collection(self):
        """Initialize or get existing collection."""
        client = chromadb.PersistentClient(
            path=self.config["memory"]["persist_directory"]
        )
        ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection = client.get_or_create_collection(
            name=self.config["memory"]["collection_name"],
            embedding_function=ef
        )
    
    def save(self, text: str, metadata: dict = None):
        """Save a single memory (text only)."""
        memory_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        meta = metadata or {"timestamp": datetime.now().isoformat()}
        
        self.collection.add(
            documents=[text],
            ids=[memory_id],
            metadatas=[meta]
        )
    
    def retrieve(self, query: str, n_results: int = None) -> list:
        """Retrieve relevant memories via semantic search."""
        if self.collection.count() == 0:
            return []
        
        if n_results is None:
            n_results = self.config["memory"]["max_results"]
        
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, self.collection.count())
        )
        
        return results.get("documents", [[]])[0] if results else []
    
    def count(self) -> int:
        """Return total number of stored memories."""
        return self.collection.count()
    
    def view_all(self):
        """View all stored memories."""
        count = self.collection.count()
        
        if count == 0:
            print("📭 No memories stored yet")
            return
        
        print(f"📚 Total memories: {count}\n")
        results = self.collection.get()
        
        for i, (doc, meta) in enumerate(zip(
            results.get("documents", []), 
            results.get("metadatas", [])
        )):
            timestamp = meta.get("timestamp", "N/A")
            print(f"[{i+1}] {timestamp}")
            print(f"     {doc[:100]}...")
            print()
    
    def delete_all(self):
        """Clear all memories in this collection."""
        client = chromadb.PersistentClient(
            path=self.config["memory"]["persist_directory"]
        )
        try:
            client.delete_collection(
                self.config["memory"]["collection_name"]
            )
            print(f"✅ Deleted collection: {self.config['memory']['collection_name']}")
            # Reinitialize to get fresh collection
            self._init_collection()
        except Exception as e:
            print(f"⚠️ Could not delete collection: {e}")
    
    def format_for_prompt(self, memories: list) -> str:
        """Format retrieved memories for injection into LLM prompt."""
        if not memories:
            return ""
        
        formatted = "## Relevant Past Memories:\n"
        for i, memory in enumerate(memories, 1):
            formatted += f"\n{i}. {memory}"
        
        return formatted