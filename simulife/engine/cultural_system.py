"""
Cultural Evolution System for SimuLife
Manages knowledge transfer, skill development, tradition formation, and cultural artifacts.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class KnowledgeType(Enum):
    """Types of knowledge that can be learned and transmitted."""
    PRACTICAL = "practical"      # Farming, building, healing
    SOCIAL = "social"           # Leadership, diplomacy, trade  
    CREATIVE = "creative"       # Art, music, storytelling
    SPIRITUAL = "spiritual"     # Beliefs, rituals, wisdom
    TECHNICAL = "technical"     # Tools, innovation, crafts


@dataclass
class CulturalArtifact:
    """Represents a cultural artifact or creation."""
    name: str
    type: str  # story, tradition, tool, ritual, etc.
    creator: str
    description: str
    cultural_value: float
    knowledge_content: Dict[str, float]  # Knowledge it contains
    creation_day: int
    preservation_level: float  # How well it's preserved


@dataclass 
class Tradition:
    """Represents an established cultural tradition."""
    name: str
    description: str
    participants: List[str]
    knowledge_preserved: Dict[str, float]
    establishment_day: int
    strength: float  # How strongly established (0-1)
    frequency: str  # daily, weekly, seasonal, annual


class CulturalSystem:
    """
    Manages cultural evolution, knowledge transfer, and artifact creation.
    """
    
    def __init__(self):
        self.artifacts: List[CulturalArtifact] = []
        self.traditions: List[Tradition] = []
        self.knowledge_network = {}  # Track who knows what
        self.cultural_memory = {}  # Community knowledge storage
        self.innovation_history = []  # Track innovations and their spread
        
    def update_agent_knowledge(self, agent: Any, knowledge_type: str, 
                             skill_area: str, amount: float) -> None:
        """Update an agent's knowledge in a specific area."""
        if not hasattr(agent, 'cultural_knowledge'):
            agent.cultural_knowledge = {}
        
        if knowledge_type not in agent.cultural_knowledge:
            agent.cultural_knowledge[knowledge_type] = {}
            
        current = agent.cultural_knowledge[knowledge_type].get(skill_area, 0.0)
        agent.cultural_knowledge[knowledge_type][skill_area] = min(1.0, current + amount)
        
        # Also update skills dictionary for consistency
        if skill_area not in agent.skills:
            agent.skills[skill_area] = 0.0
        agent.skills[skill_area] = min(1.0, agent.skills[skill_area] + amount)

    def attempt_knowledge_transfer(self, teacher: Any, student: Any, 
                                 world_day: int) -> Optional[Dict[str, Any]]:
        """
        Attempt to transfer knowledge between two agents.
        
        Returns:
            Dictionary describing the transfer if successful, None otherwise
        """
        # Check if transfer conditions are met
        relationship = teacher.relationships.get(student.name, "stranger")
        if relationship in ["stranger", "enemy"]:
            return None
            
        # Teacher must have knowledge to share
        teacher_knowledge = getattr(teacher, 'cultural_knowledge', {})
        if not teacher_knowledge:
            return None
            
        # Find knowledge areas where teacher exceeds student
        teachable_areas = []
        student_knowledge = getattr(student, 'cultural_knowledge', {})
        
        for knowledge_type, skills in teacher_knowledge.items():
            for skill_area, teacher_level in skills.items():
                student_level = student_knowledge.get(knowledge_type, {}).get(skill_area, 0.0)
                if teacher_level > student_level + 0.2:  # Minimum gap required
                    teachable_areas.append((knowledge_type, skill_area, teacher_level - student_level))
        
        if not teachable_areas:
            return None
            
        # Select knowledge to transfer based on teacher's traits and expertise
        knowledge_type, skill_area, gap = random.choice(teachable_areas)
        
        # Calculate transfer effectiveness
        base_transfer = 0.1  # Base 10% knowledge transfer
        
        # Modifiers based on relationship and traits
        relationship_bonus = {
            "friend": 0.3, "family": 0.4, "mentor": 0.5, 
            "partner": 0.2, "faction_member": 0.3
        }.get(relationship, 0.1)
        
        teacher_effectiveness = 1.0
        if "wise" in teacher.traits:
            teacher_effectiveness += 0.3
        if "patient" in teacher.traits:
            teacher_effectiveness += 0.2
        if "kind" in teacher.traits:
            teacher_effectiveness += 0.1
            
        student_receptiveness = 1.0
        if "curious" in student.traits:
            student_receptiveness += 0.3
        if "ambitious" in student.traits:
            student_receptiveness += 0.2
            
        # Final transfer amount
        transfer_amount = min(0.3, base_transfer * relationship_bonus * 
                            teacher_effectiveness * student_receptiveness)
        
        # Apply the knowledge transfer
        self.update_agent_knowledge(student, knowledge_type, skill_area, transfer_amount)
        
        # Create memory for both agents
        teaching_memory = f"Taught {student.name} about {skill_area} ({knowledge_type} knowledge)"
        learning_memory = f"Learned about {skill_area} from {teacher.name}"
        
        teacher.memory.store_memory(teaching_memory, importance=0.4, 
                                  emotion="proud", memory_type="experience")
        student.memory.store_memory(learning_memory, importance=0.6,
                                  emotion="grateful", memory_type="experience")
        
        return {
            "type": "knowledge_transfer",
            "teacher": teacher.name,
            "student": student.name,
            "knowledge_type": knowledge_type,
            "skill_area": skill_area,
            "amount_transferred": transfer_amount,
            "day": world_day
        }

    def attempt_innovation(self, agent: Any, world_day: int, 
                         world_state: Any = None) -> Optional[Dict[str, Any]]:
        """
        Agent attempts to innovate or create something new.
        
        Returns:
            Dictionary describing the innovation if successful
        """
        # Innovation chance based on traits and knowledge
        base_chance = 0.02  # 2% base chance per day
        
        if "creative" in agent.traits:
            base_chance *= 2.0
        if "curious" in agent.traits:
            base_chance *= 1.5
        if "ambitious" in agent.traits:
            base_chance *= 1.3
            
        # Knowledge level affects innovation ability
        agent_knowledge = getattr(agent, 'cultural_knowledge', {})
        total_knowledge = 0
        for knowledge_type, skills in agent_knowledge.items():
            total_knowledge += sum(skills.values())
            
        knowledge_modifier = 1.0 + (total_knowledge * 0.1)
        final_chance = base_chance * knowledge_modifier
        
        if random.random() > final_chance:
            return None
            
        # Determine type of innovation
        innovation_types = []
        
        if "creative" in agent.traits:
            innovation_types.extend(["story", "song", "art", "dance"])
        if "practical" in agent.traits:
            innovation_types.extend(["tool", "technique", "method"])
        if "spiritual" in agent.traits:
            innovation_types.extend(["ritual", "belief", "wisdom"])
        if "social" in agent.traits:
            innovation_types.extend(["custom", "game", "celebration"])
            
        if not innovation_types:
            innovation_types = ["story", "technique", "custom"]
            
        innovation_type = random.choice(innovation_types)
        
        # Create the innovation
        innovation_names = {
            "story": ["The Tale of the Ancient Ones", "The Story of the Great Journey", 
                     "Legends of the Mystic Forest", "The Chronicle of Heroes"],
            "song": ["Song of the Seasons", "Melody of the Heart", "Chant of Unity", 
                    "Harmony of the Winds"],
            "art": ["Sacred Symbols", "Cave Paintings", "Ceremonial Masks", "Stone Carvings"],
            "tool": ["Improved Fishing Net", "Better Shelter Design", "New Farming Method", 
                    "Enhanced Water Collection"],
            "ritual": ["Blessing of the Harvest", "Ceremony of Remembrance", 
                      "Rite of Passage", "Ritual of Healing"],
            "custom": ["Community Gathering", "Sharing Circle", "Skills Exchange", 
                      "Storytelling Night"],
            "technique": ["Advanced Crafting", "Improved Healing", "Better Building", 
                         "Enhanced Preservation"]
        }
        
        innovation_name = random.choice(innovation_names.get(innovation_type, ["New Creation"]))
        
        # Create cultural artifact
        artifact = CulturalArtifact(
            name=innovation_name,
            type=innovation_type,
            creator=agent.name,
            description=f"A {innovation_type} created by {agent.name}",
            cultural_value=random.uniform(0.3, 0.8),
            knowledge_content=self._generate_knowledge_content(innovation_type, agent),
            creation_day=world_day,
            preservation_level=1.0
        )
        
        self.artifacts.append(artifact)
        
        # Store memory of creation
        creation_memory = f"Created {innovation_name}, a {innovation_type} that represents my vision"
        agent.memory.store_memory(creation_memory, importance=0.8, 
                                emotion="proud", memory_type="experience")
        
        # Increase agent's reputation
        agent.reputation = min(1.0, agent.reputation + 0.1)
        
        return {
            "type": "innovation",
            "creator": agent.name,
            "innovation_name": innovation_name,
            "innovation_type": innovation_type,
            "cultural_value": artifact.cultural_value,
            "day": world_day
        }

    def _generate_knowledge_content(self, innovation_type: str, 
                                  creator: Any) -> Dict[str, float]:
        """Generate knowledge content for an innovation."""
        content = {}
        
        type_knowledge_map = {
            "story": {"creative": 0.3, "social": 0.2, "spiritual": 0.1},
            "song": {"creative": 0.4, "spiritual": 0.2},
            "art": {"creative": 0.5, "technical": 0.1},
            "tool": {"practical": 0.4, "technical": 0.3},
            "ritual": {"spiritual": 0.4, "social": 0.3},
            "custom": {"social": 0.4, "practical": 0.2},
            "technique": {"practical": 0.4, "technical": 0.2}
        }
        
        base_content = type_knowledge_map.get(innovation_type, {"creative": 0.3})
        
        # Add creator's knowledge influence
        creator_knowledge = getattr(creator, 'cultural_knowledge', {})
        for knowledge_type, value in base_content.items():
            creator_bonus = 0
            if knowledge_type in creator_knowledge:
                creator_bonus = sum(creator_knowledge[knowledge_type].values()) * 0.1
            content[knowledge_type] = min(0.8, value + creator_bonus)
            
        return content

    def attempt_tradition_formation(self, agents: List[Any], world_day: int) -> Optional[Dict[str, Any]]:
        """
        Attempt to form a new tradition from repeated behaviors or events.
        
        Returns:
            Dictionary describing the new tradition if formed
        """
        # Need minimum community size
        if len([a for a in agents if a.is_alive]) < 3:
            return None
            
        # Look for patterns in agent behaviors or shared experiences
        shared_experiences = {}
        for agent in agents:
            if not agent.is_alive:
                continue
                
            # Look at recent memories for shared experiences
            recent_memories = agent.memory.get_recent_memories(days=30, limit=20)
            for memory in recent_memories:
                if any(keyword in memory.content.lower() for keyword in 
                      ["together", "community", "celebration", "ritual", "gathering"]):
                    key = memory.content[:30]  # Use first 30 chars as key
                    if key not in shared_experiences:
                        shared_experiences[key] = []
                    shared_experiences[key].append(agent.name)
        
        # Find experiences shared by multiple agents
        potential_traditions = []
        for experience, participants in shared_experiences.items():
            if len(participants) >= 3:  # Need at least 3 participants
                potential_traditions.append((experience, participants))
        
        if not potential_traditions:
            return None
            
        # Small chance to form tradition
        if random.random() > 0.15:  # 15% chance when conditions met
            return None
            
        experience, participants = random.choice(potential_traditions)
        
        # Create tradition
        tradition_types = ["storytelling", "celebration", "gathering", "ceremony", "sharing"]
        tradition_type = random.choice(tradition_types)
        
        tradition_names = {
            "storytelling": "Evening Tales",
            "celebration": "Seasonal Festival", 
            "gathering": "Community Circle",
            "ceremony": "Blessing Ritual",
            "sharing": "Knowledge Exchange"
        }
        
        tradition_name = tradition_names.get(tradition_type, "Community Custom")
        
        tradition = Tradition(
            name=tradition_name,
            description=f"A {tradition_type} tradition that brings the community together",
            participants=participants,
            knowledge_preserved={"social": 0.3, "spiritual": 0.2},
            establishment_day=world_day,
            strength=0.3,  # Initial strength
            frequency="weekly"
        )
        
        self.traditions.append(tradition)
        
        # Notify participants
        for agent in agents:
            if agent.name in participants:
                memory_text = f"Helped establish the {tradition_name} tradition"
                agent.memory.store_memory(memory_text, importance=0.7,
                                        emotion="proud", memory_type="experience")
        
        return {
            "type": "tradition_formation",
            "tradition_name": tradition_name,
            "participants": participants,
            "day": world_day
        }

    def process_cultural_evolution(self, agents: List[Any], world_day: int,
                                 world_state: Any = None) -> List[Dict[str, Any]]:
        """
        Process daily cultural evolution - knowledge transfer, innovations, traditions.
        
        Returns:
            List of cultural events that occurred
        """
        cultural_events = []
        alive_agents = [a for a in agents if a.is_alive]
        
        if len(alive_agents) < 2:
            return cultural_events
            
        # 1. Attempt knowledge transfers between agents
        for i, agent1 in enumerate(alive_agents):
            for agent2 in alive_agents[i+1:]:
                # Check if they're in the same location
                if agent1.location == agent2.location:
                    # Chance for knowledge transfer in either direction
                    if random.random() < 0.1:  # 10% chance per interaction
                        transfer = self.attempt_knowledge_transfer(agent1, agent2, world_day)
                        if transfer:
                            cultural_events.append(transfer)
                    
                    if random.random() < 0.1:  # 10% chance reverse direction
                        transfer = self.attempt_knowledge_transfer(agent2, agent1, world_day)
                        if transfer:
                            cultural_events.append(transfer)
        
        # 2. Attempt innovations by individual agents
        for agent in alive_agents:
            innovation = self.attempt_innovation(agent, world_day, world_state)
            if innovation:
                cultural_events.append(innovation)
        
        # 3. Attempt tradition formation
        tradition = self.attempt_tradition_formation(alive_agents, world_day)
        if tradition:
            cultural_events.append(tradition)
            
        # 4. Decay old artifacts and strengthen traditions
        self._process_cultural_preservation(world_day)
        
        return cultural_events

    def _process_cultural_preservation(self, world_day: int) -> None:
        """Process preservation and decay of cultural elements."""
        # Decay artifacts over time
        for artifact in self.artifacts:
            age_days = world_day - artifact.creation_day
            if age_days > 365:  # Start decaying after 1 year
                decay_rate = 0.001 * (age_days - 365)  # Gradual decay
                artifact.preservation_level = max(0.1, artifact.preservation_level - decay_rate)
        
        # Strengthen traditions with active participants
        for tradition in self.traditions:
            active_participants = 0  # Would need to check agent memories/behaviors
            if active_participants >= len(tradition.participants) * 0.5:
                tradition.strength = min(1.0, tradition.strength + 0.01)
            else:
                tradition.strength = max(0.1, tradition.strength - 0.005)

    def get_cultural_summary(self) -> Dict[str, Any]:
        """Get a summary of current cultural state."""
        return {
            "total_artifacts": len(self.artifacts),
            "active_traditions": len([t for t in self.traditions if t.strength > 0.3]),
            "recent_artifacts": [a.name for a in self.artifacts[-5:]],
            "strongest_traditions": sorted(self.traditions, key=lambda t: t.strength, reverse=True)[:3]
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize cultural system state."""
        return {
            "artifacts": [
                {
                    "name": a.name,
                    "type": a.type,
                    "creator": a.creator,
                    "description": a.description,
                    "cultural_value": a.cultural_value,
                    "knowledge_content": a.knowledge_content,
                    "creation_day": a.creation_day,
                    "preservation_level": a.preservation_level
                } for a in self.artifacts
            ],
            "traditions": [
                {
                    "name": t.name,
                    "description": t.description,
                    "participants": t.participants,
                    "knowledge_preserved": t.knowledge_preserved,
                    "establishment_day": t.establishment_day,
                    "strength": t.strength,
                    "frequency": t.frequency
                } for t in self.traditions
            ]
        } 