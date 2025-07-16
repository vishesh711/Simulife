"""
Agent system for SimuLife simulation.
Contains base agent logic, memory management, planning, and reflection.
"""

from .base_agent import BaseAgent
from .memory_manager import MemoryManager
from .llm_integration import LLMAgentBrain, create_llm_provider
from .reproduction import FamilyManager, GeneticSystem 