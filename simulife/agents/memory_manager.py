"""
Memory Manager for SimuLife Agents
Handles vector-based memory storage and retrieval using FAISS.
"""

from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np
import json
import pickle
from datetime import datetime
from typing import List, Dict, Any, Optional


class Memory:
    """Represents a single memory with metadata."""
    
    def __init__(self, content: str, importance: float = 1.0, emotion: str = "neutral", 
                 day: int = 0, memory_type: str = "experience"):
        self.content = content
        self.importance = importance
        self.emotion = emotion
        self.day = day
        self.memory_type = memory_type  # experience, reflection, goal, relationship
        self.timestamp = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "importance": self.importance,
            "emotion": self.emotion,
            "day": self.day,
            "memory_type": self.memory_type,
            "timestamp": self.timestamp.isoformat()
        }


class MemoryManager:
    """Manages vector-based memory storage and retrieval for an agent."""
    
    def __init__(self, agent_name: str, model_name: str = "all-MiniLM-L6-v2", 
                 memory_dir: str = "data/memory_faiss"):
        self.agent_name = agent_name
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = 384  # Dimension for all-MiniLM-L6-v2
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.memories: List[Memory] = []
        self.memory_dir = memory_dir
        self.memory_file = os.path.join(memory_dir, f"{agent_name}_memories.json")
        self.index_file = os.path.join(memory_dir, f"{agent_name}_index.faiss")
        
        # Create memory directory if it doesn't exist
        os.makedirs(memory_dir, exist_ok=True)
        
        # Load existing memories if available
        self.load_memories()

    def store_memory(self, content: str, importance: float = 1.0, 
                    emotion: str = "neutral", day: int = 0, 
                    memory_type: str = "experience") -> None:
        """Store a new memory with vector embedding."""
        memory = Memory(content, importance, emotion, day, memory_type)
        
        # Create embedding
        embedding = self.model.encode([content])[0]
        
        # Add to FAISS index
        self.index.add(np.array([embedding], dtype=np.float32))
        
        # Add to memory list
        self.memories.append(memory)
        
        # Save to disk
        self.save_memories()

    def recall_memories(self, query: str, top_k: int = 5, 
                       memory_type: Optional[str] = None,
                       min_importance: float = 0.0) -> List[Memory]:
        """Retrieve relevant memories based on query."""
        if len(self.memories) == 0:
            return []
        
        # Create query embedding
        query_embedding = self.model.encode([query])[0]
        
        # Search FAISS index
        distances, indices = self.index.search(
            np.array([query_embedding], dtype=np.float32), 
            min(top_k * 2, len(self.memories))  # Get more results to filter
        )
        
        # Filter and rank results
        relevant_memories = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.memories):
                memory = self.memories[idx]
                
                # Apply filters
                if memory_type and memory.memory_type != memory_type:
                    continue
                if memory.importance < min_importance:
                    continue
                
                relevant_memories.append(memory)
                
                if len(relevant_memories) >= top_k:
                    break
        
        return relevant_memories

    def get_recent_memories(self, days: int = 3, limit: int = 10) -> List[Memory]:
        """Get recent memories from the last N days."""
        current_day = max([m.day for m in self.memories]) if self.memories else 0
        cutoff_day = current_day - days
        
        recent = [m for m in self.memories if m.day >= cutoff_day]
        recent.sort(key=lambda x: (x.day, x.importance), reverse=True)
        
        return recent[:limit]

    def get_important_memories(self, threshold: float = 0.7, limit: int = 10) -> List[Memory]:
        """Get the most important memories."""
        important = [m for m in self.memories if m.importance >= threshold]
        important.sort(key=lambda x: x.importance, reverse=True)
        
        return important[:limit]

    def get_memories_by_type(self, memory_type: str, limit: int = 10) -> List[Memory]:
        """Get memories of a specific type."""
        type_memories = [m for m in self.memories if m.memory_type == memory_type]
        type_memories.sort(key=lambda x: (x.day, x.importance), reverse=True)
        
        return type_memories[:limit]

    def reflect_on_memories(self, reflection_prompt: str) -> str:
        """Create a reflection based on stored memories."""
        recent_memories = self.get_recent_memories(days=7)
        important_memories = self.get_important_memories(threshold=0.6)
        
        # Combine unique memories
        all_memories = list({m.content: m for m in recent_memories + important_memories}.values())
        
        if not all_memories:
            return "I have no significant memories to reflect upon."
        
        # Create reflection context
        memory_text = "\n".join([f"- {m.content} (Day {m.day}, {m.emotion})" 
                                for m in all_memories[:10]])
        
        return f"Reflecting on recent experiences:\n{memory_text}"

    def save_memories(self) -> None:
        """Save memories and FAISS index to disk."""
        # Save memories as JSON
        memory_data = [memory.to_dict() for memory in self.memories]
        with open(self.memory_file, 'w') as f:
            json.dump(memory_data, f, indent=2)
        
        # Save FAISS index
        if self.index.ntotal > 0:
            faiss.write_index(self.index, self.index_file)

    def load_memories(self) -> None:
        """Load memories and FAISS index from disk."""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                memory_data = json.load(f)
            
            for data in memory_data:
                memory = Memory(
                    content=data["content"],
                    importance=data["importance"],
                    emotion=data["emotion"],
                    day=data["day"],
                    memory_type=data["memory_type"]
                )
                self.memories.append(memory)
        
        # Load FAISS index
        if os.path.exists(self.index_file) and len(self.memories) > 0:
            self.index = faiss.read_index(self.index_file)

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about stored memories."""
        if not self.memories:
            return {"total_memories": 0}
        
        return {
            "total_memories": len(self.memories),
            "memory_types": {t: len([m for m in self.memories if m.memory_type == t]) 
                           for t in set(m.memory_type for m in self.memories)},
            "avg_importance": sum(m.importance for m in self.memories) / len(self.memories),
            "emotion_distribution": {e: len([m for m in self.memories if m.emotion == e]) 
                                   for e in set(m.emotion for m in self.memories)},
            "day_range": (min(m.day for m in self.memories), max(m.day for m in self.memories))
        } 