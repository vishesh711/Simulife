"""
Base Agent for SimuLife Simulation
Each agent has personality, memory, emotions, and can make decisions.
"""

import json
import random
from typing import Dict, List, Any, Optional
from .memory_manager import MemoryManager
from .llm_integration import LLMAgentBrain, create_llm_provider


class BaseAgent:
    """
    Core agent class representing an AI entity in the SimuLife simulation.
    Each agent has personality traits, emotions, goals, relationships, and memory.
    """
    
    def __init__(self, config: Dict[str, Any], world_day: int = 0):
        # Basic identity
        self.id = config.get("id", f"agent_{random.randint(1000, 9999)}")
        self.name = config["name"]
        self.age = config.get("age", 25)
        self.birth_day = config.get("birth_day", world_day - self.age * 365)
        
        # Personality and traits
        self.traits = config.get("traits", [])
        self.personality_scores = config.get("personality_scores", {
            "openness": 0.5,
            "conscientiousness": 0.5,
            "extraversion": 0.5,
            "agreeableness": 0.5,
            "neuroticism": 0.5
        })
        
        # Goals and motivations
        self.goals = config.get("goals", [])
        self.current_goal = config.get("current_goal", "")
        self.life_satisfaction = config.get("life_satisfaction", 0.5)
        
        # Emotional state
        self.emotion = config.get("emotion", "neutral")
        self.emotion_intensity = config.get("emotion_intensity", 0.5)
        self.mood = config.get("mood", "stable")
        
        # Relationships and social
        self.relationships = config.get("relationships", {})
        self.family = config.get("family", {})
        self.faction = config.get("faction", None)
        self.reputation = config.get("reputation", 0.5)
        
        # Physical and location
        self.location = config.get("location", "village_center")
        self.health = config.get("health", 1.0)
        self.energy = config.get("energy", 1.0)
        
        # Skills and knowledge
        self.skills = config.get("skills", {})
        self.beliefs = config.get("beliefs", {})
        self.values = config.get("values", [])
        
        # Memory system
        self.memory = MemoryManager(self.name)
        
        # Phase 10: Deep Human Emotions & Life Purpose
        self.emotional_profile = config.get("emotional_profile", {
            "primary_emotions": {
                "love": 0.0,           # Capacity for deep love
                "joy": 0.5,            # General happiness
                "fear": 0.3,           # Anxiety and worry
                "anger": 0.2,          # Frustration and rage
                "sadness": 0.1,        # Depression and grief
                "surprise": 0.4,       # Wonder and shock
                "trust": 0.6,          # Faith in others
                "anticipation": 0.5    # Hope and excitement
            },
            "complex_emotions": {
                "romantic_love": 0.0,      # Passionate attachment
                "parental_love": 0.0,      # Protective nurturing
                "jealousy": 0.0,           # Romantic/social jealousy
                "nostalgia": 0.0,          # Longing for past
                "ambition": 0.3,           # Drive for achievement
                "contentment": 0.4,        # Life satisfaction
                "loneliness": 0.2,         # Social isolation pain
                "pride": 0.3,              # Self-worth and dignity
                "shame": 0.1,              # Self-criticism
                "compassion": 0.5          # Care for others' suffering
            }
        })
        
        # Life Purpose & Meaning
        self.life_purpose = config.get("life_purpose", {
            "core_calling": None,              # Primary life mission
            "secondary_purposes": [],          # Supporting goals
            "spiritual_beliefs": {},           # Religious/philosophical views
            "legacy_desires": [],              # How they want to be remembered
            "meaning_sources": [],             # What gives life meaning
            "existential_questions": [],       # Deep questions they ponder
            "purpose_evolution": []            # How purpose changes over time
        })
        
        # Romance & Love Life
        self.romantic_life = config.get("romantic_life", {
            "attraction_preferences": {},       # What they find attractive
            "romantic_history": [],            # Past relationships
            "current_partner": None,           # Active romantic relationship
            "courtship_style": None,           # How they pursue romance
            "love_languages": [],              # How they express/receive love
            "relationship_values": [],         # What they value in partnerships
            "heartbreak_history": [],          # Past emotional wounds
            "romantic_ideals": {}              # Dreams about perfect love
        })
        
        # Deep Family Connections
        self.family_bonds = config.get("family_bonds", {
            "parental_attachment": {},         # Strength of parent bonds
            "sibling_relationships": {},       # Complex sibling dynamics
            "protective_instincts": {},        # Who they'd protect
            "family_loyalty": 0.7,             # Commitment to family
            "generational_values": {},         # Family traditions they hold
            "family_role": None,               # Their position in family
            "inherited_traits": {},            # Family characteristics
            "family_secrets": []               # Hidden family knowledge
        })
        
        # Romantic relationship status (Phase 10)
        self.relationship_status = config.get("relationship_status", "single")
        self.romantic_partner = config.get("romantic_partner", None)
        
        # Pregnancy tracking (for reproduction system)
        self.pregnancies = config.get("pregnancies", [])
        
        # LLM brain for intelligent decision-making
        llm_config = config.get("llm_config", {"provider_type": "mock"})
        provider = create_llm_provider(**llm_config)
        self.brain = LLMAgentBrain(provider)
        
        # Status tracking
        self.is_alive = config.get("is_alive", True)
        self.last_action = config.get("last_action", "")
        self.action_history = config.get("action_history", [])
        
        # Store initial config for reference
        self.initial_config = config.copy()

    def reflect(self, world_context: Optional[str] = None) -> str:
        """
        Agent reflects on recent experiences and creates self-awareness.
        """
        # Get recent memories
        recent_memories = self.memory.get_recent_memories(days=3, limit=5)
        important_memories = self.memory.get_important_memories(threshold=0.6, limit=3)
        
        # Create reflection context
        reflection_parts = [
            f"I am {self.name}, feeling {self.emotion} with {self.emotion_intensity:.1f} intensity.",
            f"My current goal is: {self.current_goal or 'undecided'}."
        ]
        
        if recent_memories:
            memory_text = "; ".join([m.content for m in recent_memories])
            reflection_parts.append(f"Recent experiences: {memory_text}")
        
        if important_memories:
            important_text = "; ".join([m.content for m in important_memories])
            reflection_parts.append(f"Important memories: {important_text}")
        
        if self.relationships:
            rel_text = ", ".join([f"{name}({rel})" for name, rel in self.relationships.items()])
            reflection_parts.append(f"My relationships: {rel_text}")
        
        if world_context:
            reflection_parts.append(f"World situation: {world_context}")
        
        reflection = " ".join(reflection_parts)
        
        # Store this reflection as a memory
        self.memory.store_memory(
            f"Reflected on my situation: {reflection[:100]}...",
            importance=0.4,
            emotion=self.emotion,
            memory_type="reflection"
        )
        
        return reflection

    def decide_action(self, available_actions: List[str] = None, world_state: Dict = None) -> str:
        """
        Agent decides what action to take based on personality, goals, and memories.
        """
        if available_actions is None:
            available_actions = [
                "rest_and_think",
                "socialize_with_others", 
                "work_on_skills",
                "explore_area",
                "help_someone",
                "pursue_personal_goal",
                "observe_surroundings"
            ]
        
        # Get context for decision making
        reflection = self.reflect(world_state.get("description", "") if world_state else None)
        
        # Build rich context for LLM decision making
        recent_memories = self.memory.get_recent_memories(days=2, limit=3)
        recent_memories_text = "; ".join([m.content for m in recent_memories]) if recent_memories else "None"
        
        relationships_summary = ", ".join([f"{name}({rel})" for name, rel in self.relationships.items()]) if self.relationships else "None"
        
        agent_context = {
            "name": self.name,
            "age": self.age,
            "traits": self.traits,
            "emotion": self.emotion,
            "emotion_intensity": self.emotion_intensity,
            "current_goal": self.current_goal,
            "location": self.location,
            "recent_memories": recent_memories_text,
            "relationships_summary": relationships_summary
        }
        
        world_context = world_state.get("description", "") if world_state else ""
        
        # Use LLM brain for intelligent decision making
        try:
            llm_action = self.brain.decide_action(agent_context, available_actions, world_context)
            action_description = f"{self.name} {llm_action}"
        except Exception as e:
            # Fallback to simple logic if LLM fails
            print(f"LLM decision failed for {self.name}: {e}, using fallback")
            action_description = self._fallback_decide_action(available_actions)
        
        # Store action in memory and history
        self.last_action = action_description
        self.action_history.append(action_description)
        if len(self.action_history) > 50:  # Keep history manageable
            self.action_history = self.action_history[-50:]
        
        self.memory.store_memory(
            f"I decided to {action_description}",
            importance=0.3,
            emotion=self.emotion,
            memory_type="experience"
        )
        
        return action_description

    def _fallback_decide_action(self, available_actions: List[str]) -> str:
        """Fallback decision logic when LLM is unavailable."""
        # Simple decision logic based on personality and state
        decision_factors = []
        
        # Energy-based decisions
        if self.energy < 0.3:
            decision_factors.append(("rest_and_think", 0.8))
        
        # Personality-based preferences
        if "curious" in self.traits:
            decision_factors.extend([
                ("explore_area", 0.6),
                ("observe_surroundings", 0.5)
            ])
        
        if "kind" in self.traits:
            decision_factors.append(("help_someone", 0.7))
        
        if "ambitious" in self.traits:
            decision_factors.extend([
                ("pursue_personal_goal", 0.8),
                ("work_on_skills", 0.6)
            ])
        
        if self.personality_scores.get("extraversion", 0.5) > 0.6:
            decision_factors.append(("socialize_with_others", 0.7))
        
        # Goal-based decisions
        if self.current_goal:
            if "learn" in self.current_goal.lower():
                decision_factors.append(("work_on_skills", 0.8))
            if "friend" in self.current_goal.lower() or "social" in self.current_goal.lower():
                decision_factors.append(("socialize_with_others", 0.9))
        
        # Select action with some randomness
        if decision_factors:
            action_weights = {}
            for action, weight in decision_factors:
                if action in available_actions:
                    action_weights[action] = action_weights.get(action, 0) + weight
            
            if action_weights:
                # Add some randomness
                actions = list(action_weights.keys())
                weights = [action_weights[a] + random.random() * 0.3 for a in actions]
                chosen_action = random.choices(actions, weights=weights)[0]
            else:
                chosen_action = random.choice(available_actions)
        else:
            chosen_action = random.choice(available_actions)
        
        # Create action description
        return self._describe_action(chosen_action)

    def _describe_action(self, action: str) -> str:
        """Create a natural language description of the action."""
        action_descriptions = {
            "rest_and_think": f"{self.name} finds a quiet spot to rest and contemplate life",
            "socialize_with_others": f"{self.name} seeks out others to chat and build relationships",
            "work_on_skills": f"{self.name} practices skills to improve and learn new things",
            "explore_area": f"{self.name} ventures out to explore and discover new places",
            "help_someone": f"{self.name} looks for someone who needs assistance",
            "pursue_personal_goal": f"{self.name} works toward their personal goal: {self.current_goal}",
            "observe_surroundings": f"{self.name} carefully observes the environment and people around"
        }
        
        return action_descriptions.get(action, f"{self.name} {action}")

    def interact_with(self, other_agent: 'BaseAgent', interaction_type: str = "conversation") -> str:
        """
        Handle interaction between this agent and another agent.
        """
        # Determine relationship context
        relationship = self.relationships.get(other_agent.name, "stranger")
        
        # Create interaction based on personalities and relationship
        if interaction_type == "conversation":
            if relationship == "friend":
                interaction = f"{self.name} has a warm conversation with {other_agent.name}"
            elif relationship == "rival":
                interaction = f"{self.name} has a tense exchange with {other_agent.name}"
            elif relationship == "family":
                interaction = f"{self.name} shares family news with {other_agent.name}"
            else:
                interaction = f"{self.name} introduces themselves to {other_agent.name}"
        else:
            interaction = f"{self.name} {interaction_type} with {other_agent.name}"
        
        # Store memory of interaction
        self.memory.store_memory(
            interaction,
            importance=0.5 if relationship in ["friend", "family"] else 0.3,
            emotion=self.emotion,
            memory_type="relationship"
        )
        
        # Update relationship if needed
        self._update_relationship(other_agent, interaction_type)
        
        return interaction

    def _update_relationship(self, other_agent: 'BaseAgent', interaction_type: str):
        """Update relationship status based on interaction."""
        current_rel = self.relationships.get(other_agent.name, "stranger")
        
        # Simple relationship evolution logic
        if interaction_type == "conversation" and current_rel == "stranger":
            if random.random() < 0.3:  # 30% chance to become acquaintance
                self.relationships[other_agent.name] = "acquaintance"
        elif interaction_type == "help" and current_rel in ["stranger", "acquaintance"]:
            if random.random() < 0.4:  # 40% chance to become friend
                self.relationships[other_agent.name] = "friend"

    def observe_event(self, event_description: str, importance: float = 0.5, 
                     emotion_trigger: str = None) -> None:
        """
        Agent observes and reacts to an event in the world.
        """
        # Store event in memory
        self.memory.store_memory(
            event_description,
            importance=importance,
            emotion=emotion_trigger or self.emotion,
            memory_type="experience"
        )
        
        # Event might affect emotional state
        if emotion_trigger and importance > 0.6:
            self.emotion = emotion_trigger
            self.emotion_intensity = min(1.0, self.emotion_intensity + importance * 0.5)

    def age_one_day(self, world_day: int) -> None:
        """
        Age the agent by one day and update states.
        """
        # Update age if needed (simplified - could be more complex)
        days_lived = world_day - self.birth_day
        self.age = days_lived // 365
        
        # Gradual changes over time
        self.energy = min(1.0, self.energy + random.uniform(-0.1, 0.2))
        
        # Emotional state tends to return to neutral over time
        if self.emotion != "neutral":
            self.emotion_intensity *= 0.9
            if self.emotion_intensity < 0.2:
                self.emotion = "neutral"
                self.emotion_intensity = 0.1

    def experience_romantic_attraction(self, target_agent) -> bool:
        """Experience romantic feelings for another agent."""
        # This method is called by the LoveRomanceSystem
        return True  # Basic implementation - system handles the complexity
    
    def calculate_romantic_compatibility(self, other_agent) -> float:
        """Calculate romantic compatibility with another agent."""
        # Basic compatibility calculation - full logic is in LoveRomanceSystem
        compatibility = 0.0
        
        # Personality compatibility
        for trait in ["extraversion", "agreeableness", "openness"]:
            if trait in self.personality_scores and trait in other_agent.personality_scores:
                diff = abs(self.personality_scores[trait] - other_agent.personality_scores[trait])
                compatibility += max(0, 1.0 - diff) * 0.2
        
        # Shared traits
        shared_traits = len(set(self.traits) & set(other_agent.traits))
        compatibility += shared_traits * 0.1
        
        # Age compatibility
        age_diff = abs(self.age - other_agent.age)
        age_compat = max(0, 1.0 - (age_diff / 20.0))
        compatibility += age_compat * 0.2
        
        return min(1.0, compatibility)
    
    def discover_life_purpose(self):
        """Agent discovers or evolves their life purpose."""
        # Life purpose emerges from personality, experiences, and age
        if self.age >= 18 and not self.life_purpose["core_calling"]:
            # Generate purpose based on personality and experiences
            possible_purposes = self._generate_possible_purposes()
            if possible_purposes:
                chosen_purpose = possible_purposes[0]  # Take the most fitting one
                self.life_purpose["core_calling"] = chosen_purpose
                
                # Create important memory
                self.memory.store_memory(
                    f"I've discovered my life's calling: {chosen_purpose}. This gives my existence meaning.",
                    importance=1.0,
                    emotion="enlightenment",
                    memory_type="life_milestone"
                )
    
    def _generate_possible_purposes(self) -> List[str]:
        """Generate possible life purposes based on personality and traits."""
        purposes = []
        
        if "creative" in self.traits or "artistic" in self.traits:
            purposes.append("create beautiful art that inspires others")
        if "wise" in self.traits or self.personality_scores.get("openness", 0.5) > 0.7:
            purposes.append("seek knowledge and teach wisdom")
        if "social" in self.traits or self.personality_scores.get("extraversion", 0.5) > 0.7:
            purposes.append("build strong communities and help others")
        if "strong" in self.traits or "protective" in self.traits:
            purposes.append("protect those who cannot protect themselves")
        if "spiritual" in self.traits:
            purposes.append("understand the deeper meaning of existence")
        if self.personality_scores.get("conscientiousness", 0.5) > 0.7:
            purposes.append("create lasting institutions that benefit society")
        
        # Default purposes if none match
        if not purposes:
            purposes = [
                "live a meaningful life and be remembered kindly",
                "make the world a better place for future generations",
                "find happiness and help others find theirs"
            ]
        
        return purposes
    
    def form_deep_family_bond(self, family_member, bond_type: str):
        """Create intense family emotional bonds."""
        import random
        
        if bond_type == "parent_child":
            # Incredibly strong protective and nurturing bond
            bond_strength = random.uniform(0.8, 1.0)
            self.family_bonds["parental_attachment"][family_member.name] = bond_strength
            
            # Parental love is one of the strongest emotions
            self.emotional_profile["complex_emotions"]["parental_love"] = max(
                self.emotional_profile["complex_emotions"]["parental_love"],
                bond_strength
            )
            
        elif bond_type == "siblings":
            # Complex mix of competition and loyalty
            bond_strength = random.uniform(0.4, 0.9)
            rivalry_level = random.uniform(0.1, 0.6)
            
            self.family_bonds["sibling_relationships"][family_member.name] = {
                "bond_strength": bond_strength,
                "rivalry_level": rivalry_level,
                "shared_memories": [],
                "loyalty": random.uniform(0.6, 1.0)
            }
    
    def update_emotional_state(self, emotion_changes: Dict[str, float]):
        """Update agent's emotional state with new influences."""
        # Update primary emotions
        for emotion, change in emotion_changes.get("primary_emotions", {}).items():
            if emotion in self.emotional_profile["primary_emotions"]:
                current_value = self.emotional_profile["primary_emotions"][emotion]
                new_value = max(0.0, min(1.0, current_value + change))
                self.emotional_profile["primary_emotions"][emotion] = new_value
        
        # Update complex emotions
        for emotion, change in emotion_changes.get("complex_emotions", {}).items():
            if emotion in self.emotional_profile["complex_emotions"]:
                current_value = self.emotional_profile["complex_emotions"][emotion]
                new_value = max(0.0, min(1.0, current_value + change))
                self.emotional_profile["complex_emotions"][emotion] = new_value
    
    def get_dominant_emotion(self) -> str:
        """Get the currently strongest emotion."""
        all_emotions = {}
        all_emotions.update(self.emotional_profile["primary_emotions"])
        all_emotions.update(self.emotional_profile["complex_emotions"])
        
        return max(all_emotions, key=all_emotions.get)
    
    def get_life_stage(self) -> str:
        """Determine current life stage based on age."""
        if self.age < 16:
            return "child"
        elif self.age < 25:
            return "young_adult"
        elif self.age < 40:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        else:
            return "elder"

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize agent state to dictionary for saving.
        """
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "birth_day": self.birth_day,
            "traits": self.traits,
            "personality_scores": self.personality_scores,
            "goals": self.goals,
            "current_goal": self.current_goal,
            "life_satisfaction": self.life_satisfaction,
            "emotion": self.emotion,
            "emotion_intensity": self.emotion_intensity,
            "mood": self.mood,
            "relationships": self.relationships,
            "family": self.family,
            "faction": self.faction,
            "reputation": self.reputation,
            "location": self.location,
            "health": self.health,
            "energy": self.energy,
            "skills": self.skills,
            "beliefs": self.beliefs,
            "values": self.values,
            "is_alive": self.is_alive,
            "last_action": self.last_action,
            "action_history": self.action_history[-10:],  # Keep only recent history
            # Phase 10 additions
            "emotional_profile": self.emotional_profile,
            "life_purpose": self.life_purpose,
            "romantic_life": self.romantic_life,
            "family_bonds": self.family_bonds,
            "relationship_status": self.relationship_status,
            "romantic_partner": self.romantic_partner,
            "pregnancies": self.pregnancies
        }

    def get_status_summary(self) -> str:
        """
        Get a brief summary of the agent's current status.
        """
        status_parts = [
            f"{self.name} (Age {self.age})",
            f"Emotion: {self.emotion} ({self.emotion_intensity:.1f})",
            f"Energy: {self.energy:.1f}",
            f"Goal: {self.current_goal or 'None'}",
            f"Location: {self.location}"
        ]
        
        if self.relationships:
            rel_count = len(self.relationships)
            status_parts.append(f"Relationships: {rel_count}")
        
        memory_stats = self.memory.get_memory_stats()
        if memory_stats.get("total_memories", 0) > 0:
            status_parts.append(f"Memories: {memory_stats['total_memories']}")
        
        return " | ".join(status_parts) 