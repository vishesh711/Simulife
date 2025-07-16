"""
Emotional Complexity System for SimuLife
Enables agents to experience mixed emotions, emotional growth, empathy development,
emotional contagion spreading through communities, and trauma healing processes.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import math


class EmotionType(Enum):
    """Basic emotion types."""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    LOVE = "love"
    CONTEMPT = "contempt"


class ComplexEmotionType(Enum):
    """Complex emotional states."""
    BITTERSWEET = "bittersweet"       # Joy + Sadness
    JEALOUSY = "jealousy"             # Love + Anger + Fear
    NOSTALGIA = "nostalgia"           # Sadness + Love + Joy
    GUILT = "guilt"                   # Fear + Sadness + Anger
    PRIDE = "pride"                   # Joy + Love + Contempt
    SHAME = "shame"                   # Fear + Sadness + Disgust
    AWE = "awe"                       # Surprise + Fear + Joy
    MELANCHOLY = "melancholy"         # Sadness + Love
    RIGHTEOUS_ANGER = "righteous_anger"  # Anger + Love
    ANTICIPATION = "anticipation"     # Joy + Fear + Surprise


class EmotionalGrowthStage(Enum):
    """Stages of emotional development."""
    REACTIVE = "reactive"             # Basic emotional reactions
    AWARE = "aware"                   # Beginning to understand emotions
    PROCESSING = "processing"         # Learning to handle emotions
    INTEGRATED = "integrated"         # Emotions well-managed
    WISE = "wise"                     # Helps others with emotions
    TRANSCENDENT = "transcendent"     # Beyond personal emotions


class TraumaType(Enum):
    """Types of traumatic experiences."""
    LOSS = "loss"                     # Death of loved one
    BETRAYAL = "betrayal"             # Trust broken by someone close
    ABANDONMENT = "abandonment"       # Being left alone
    VIOLENCE = "violence"             # Physical or emotional abuse
    FAILURE = "failure"               # Major life failure
    REJECTION = "rejection"           # Social rejection
    NATURAL_DISASTER = "natural_disaster"  # Environmental trauma
    ILLNESS = "illness"               # Serious health issues


@dataclass
class EmotionalState:
    """Represents an agent's current emotional state."""
    agent_name: str
    day: int
    
    # Basic emotions (0.0-1.0)
    primary_emotions: Dict[EmotionType, float]
    
    # Complex emotional combinations
    complex_emotions: Dict[ComplexEmotionType, float]
    
    # Emotional characteristics
    emotional_intensity: float        # How strongly they feel
    emotional_stability: float        # How stable their emotions are
    emotional_expressiveness: float   # How much they show emotions
    emotional_regulation: float       # How well they control emotions
    
    # Recent influences
    triggering_events: List[str]
    social_influences: List[str]
    internal_factors: List[str]


@dataclass
class EmotionalGrowthEvent:
    """Represents a moment of emotional growth or learning."""
    agent_name: str
    growth_type: str                  # insight, breakthrough, healing, wisdom
    trigger_event: str
    day: int
    
    # Growth details
    emotional_lesson: str
    old_pattern: str
    new_understanding: str
    growth_impact: float              # How much they grew
    
    # Application
    behavioral_changes: List[str]
    improved_relationships: List[str]
    wisdom_gained: str


@dataclass
class EmpathyEvent:
    """Represents an empathetic connection between agents."""
    empathizer: str
    target: str
    emotion_shared: EmotionType
    empathy_strength: float
    day: int
    
    # Context
    situation: str
    empathy_response: str
    emotional_support_given: str
    long_term_impact: float


@dataclass
class EmotionalContagion:
    """Represents emotions spreading through a community."""
    source_agent: str
    emotion_type: EmotionType
    intensity: float
    started_day: int
    
    # Spread pattern
    affected_agents: List[str]
    spread_rate: float
    peak_intensity: float
    duration: int
    
    # Resolution
    natural_decay: bool
    intervention_events: List[str]
    final_impact: Dict[str, float]    # agent -> impact


@dataclass
class TraumaEvent:
    """Represents a traumatic experience and its healing process."""
    agent_name: str
    trauma_type: TraumaType
    trauma_description: str
    occurred_day: int
    
    # Trauma characteristics
    severity: float                   # 0.0-1.0 how severe
    initial_impact: float             # Immediate emotional damage
    triggers: List[str]               # What triggers trauma responses
    
    # Healing process
    healing_stage: str                # denial, anger, bargaining, depression, acceptance
    healing_progress: float           # 0.0-1.0 how much healed
    healing_events: List[Dict[str, Any]]
    support_received: List[str]
    
    # Long-term effects
    permanent_changes: List[str]
    wisdom_gained: List[str]
    post_traumatic_growth: float


class EmotionalComplexitySystem:
    """
    Manages complex emotional experiences including mixed emotions, empathy,
    emotional contagion, trauma, and emotional growth throughout agents' lives.
    """
    
    def __init__(self):
        self.agent_emotional_states: Dict[str, EmotionalState] = {}
        self.emotional_growth_events: List[EmotionalGrowthEvent] = []
        self.empathy_events: List[EmpathyEvent] = []
        self.emotional_contagions: List[EmotionalContagion] = []
        self.trauma_events: Dict[str, List[TraumaEvent]] = defaultdict(list)
        
        # System tracking
        self.emotional_evolution: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.community_emotional_climate: Dict[int, Dict[str, float]] = {}
        
        # Configuration
        self.empathy_base_chance = 0.2            # 20% chance to empathize
        self.emotional_growth_chance = 0.05       # 5% chance for growth moments
        self.contagion_spread_rate = 0.3          # How fast emotions spread
        self.trauma_healing_rate = 0.01           # How fast trauma heals per day
        
        # Emotional patterns and templates
        self.complex_emotion_recipes = self._initialize_complex_emotions()
        self.growth_triggers = self._initialize_growth_triggers()
        self.empathy_responses = self._initialize_empathy_responses()
        self.trauma_healing_stages = self._initialize_trauma_healing()
        
    def _initialize_complex_emotions(self) -> Dict[ComplexEmotionType, Dict]:
        """Initialize complex emotion recipes."""
        return {
            ComplexEmotionType.BITTERSWEET: {
                "components": {EmotionType.JOY: 0.6, EmotionType.SADNESS: 0.7},
                "triggers": ["graduation", "moving_away", "achievement_with_cost"]
            },
            ComplexEmotionType.JEALOUSY: {
                "components": {EmotionType.LOVE: 0.8, EmotionType.ANGER: 0.6, EmotionType.FEAR: 0.5},
                "triggers": ["romantic_rival", "friend_choosing_others", "professional_competition"]
            },
            ComplexEmotionType.NOSTALGIA: {
                "components": {EmotionType.SADNESS: 0.5, EmotionType.LOVE: 0.7, EmotionType.JOY: 0.4},
                "triggers": ["childhood_memories", "old_friends", "past_achievements"]
            },
            ComplexEmotionType.GUILT: {
                "components": {EmotionType.FEAR: 0.6, EmotionType.SADNESS: 0.7, EmotionType.ANGER: 0.3},
                "triggers": ["hurting_someone", "breaking_promise", "selfish_behavior"]
            },
            ComplexEmotionType.PRIDE: {
                "components": {EmotionType.JOY: 0.8, EmotionType.LOVE: 0.5, EmotionType.CONTEMPT: 0.3},
                "triggers": ["achievement", "family_success", "overcoming_challenge"]
            },
            ComplexEmotionType.AWE: {
                "components": {EmotionType.SURPRISE: 0.8, EmotionType.FEAR: 0.4, EmotionType.JOY: 0.6},
                "triggers": ["natural_wonder", "artistic_masterpiece", "profound_realization"]
            }
        }
    
    def _initialize_growth_triggers(self) -> List[str]:
        """Initialize emotional growth trigger events."""
        return [
            "Witnessing someone else's pain and feeling deep empathy",
            "Successfully managing a difficult emotion",
            "Receiving emotional support from others during crisis",
            "Helping someone else through emotional difficulty",
            "Realizing a pattern in emotional reactions",
            "Overcoming a long-held fear",
            "Forgiving someone who hurt them deeply",
            "Learning to express emotions in healthy ways",
            "Understanding the emotions behind someone's behavior",
            "Finding peace after a period of emotional turmoil"
        ]
    
    def _initialize_empathy_responses(self) -> Dict[EmotionType, List[str]]:
        """Initialize empathetic responses by emotion type."""
        return {
            EmotionType.SADNESS: [
                "Offering comfort and presence",
                "Sharing their own similar experience",
                "Providing practical help",
                "Listening without judgment"
            ],
            EmotionType.ANGER: [
                "Validating their feelings",
                "Helping them process the anger safely",
                "Standing up for them if appropriate",
                "Offering perspective on the situation"
            ],
            EmotionType.FEAR: [
                "Providing reassurance and safety",
                "Helping them face the fear gradually",
                "Sharing courage and strength",
                "Staying close during difficult times"
            ],
            EmotionType.JOY: [
                "Celebrating with them",
                "Amplifying their happiness",
                "Sharing in their excitement",
                "Helping them savor the moment"
            ]
        }
    
    def _initialize_trauma_healing(self) -> Dict[str, Dict[str, Any]]:
        """Initialize trauma healing stage information."""
        return {
            "denial": {
                "characteristics": ["Avoiding the reality", "Minimizing impact", "Acting like nothing happened"],
                "duration_range": (7, 30),
                "healing_activities": ["Gentle acknowledgment", "Safe expression", "Patient support"]
            },
            "anger": {
                "characteristics": ["Rage at situation", "Blaming others", "Aggressive outbursts"],
                "duration_range": (14, 60),
                "healing_activities": ["Physical activity", "Venting safely", "Understanding anger"]
            },
            "bargaining": {
                "characteristics": ["What-if thinking", "Trying to undo damage", "Making deals"],
                "duration_range": (7, 30),
                "healing_activities": ["Reality testing", "Acceptance practice", "Mindfulness"]
            },
            "depression": {
                "characteristics": ["Deep sadness", "Withdrawal", "Loss of interest"],
                "duration_range": (30, 180),
                "healing_activities": ["Social support", "Meaning-making", "Small steps forward"]
            },
            "acceptance": {
                "characteristics": ["Realistic view", "Integration", "Moving forward"],
                "duration_range": (60, 365),
                "healing_activities": ["New goals", "Helping others", "Wisdom sharing"]
            }
        }
    
    def process_daily_emotional_complexity(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process daily emotional complexity activities."""
        events = []
        
        # Phase 1: Update emotional states
        state_events = self._update_emotional_states(agents, current_day)
        events.extend(state_events)
        
        # Phase 2: Process complex emotions
        complex_events = self._process_complex_emotions(agents, current_day)
        events.extend(complex_events)
        
        # Phase 3: Handle empathy and emotional connection
        empathy_events = self._process_empathy_events(agents, current_day)
        events.extend(empathy_events)
        
        # Phase 4: Manage emotional contagion
        contagion_events = self._process_emotional_contagion(agents, current_day)
        events.extend(contagion_events)
        
        # Phase 5: Process emotional growth
        growth_events = self._process_emotional_growth(agents, current_day)
        events.extend(growth_events)
        
        # Phase 6: Handle trauma and healing
        trauma_events = self._process_trauma_healing(agents, current_day)
        events.extend(trauma_events)
        
        # Update community emotional climate
        self._update_community_emotional_climate(agents, current_day)
        
        return events
    
    def _update_emotional_states(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Update emotional states for all agents."""
        events = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            # Update or create emotional state
            emotional_state = self._calculate_current_emotional_state(agent, current_day)
            self.agent_emotional_states[agent.name] = emotional_state
            
            # Check for significant emotional changes
            if self._has_significant_emotional_change(agent, emotional_state):
                events.append({
                    "type": "emotional_state_change",
                    "agent": agent.name,
                    "dominant_emotion": self._get_dominant_emotion(emotional_state),
                    "intensity": emotional_state.emotional_intensity,
                    "triggers": emotional_state.triggering_events,
                    "day": current_day
                })
        
        return events
    
    def _process_complex_emotions(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process complex emotional combinations."""
        events = []
        
        for agent in agents:
            if not agent.is_alive or agent.name not in self.agent_emotional_states:
                continue
            
            emotional_state = self.agent_emotional_states[agent.name]
            
            # Check for complex emotion formation
            for complex_emotion, recipe in self.complex_emotion_recipes.items():
                if self._complex_emotion_triggered(emotional_state, recipe):
                    intensity = self._calculate_complex_emotion_intensity(emotional_state, recipe)
                    
                    if intensity > 0.5:  # Significant enough to notice
                        emotional_state.complex_emotions[complex_emotion] = intensity
                        
                        # Create memory of complex emotion
                        agent.memory.store_memory(
                            f"I'm experiencing a complex mix of emotions - {complex_emotion.value}. "
                            f"Life isn't simple; emotions can be contradictory.",
                            importance=0.6,
                            emotion=complex_emotion.value,
                            memory_type="emotional"
                        )
                        
                        events.append({
                            "type": "complex_emotion_experienced",
                            "agent": agent.name,
                            "complex_emotion": complex_emotion.value,
                            "intensity": intensity,
                            "day": current_day
                        })
        
        return events
    
    def _process_empathy_events(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process empathetic connections between agents."""
        events = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            # Check for empathy opportunities with other agents
            for other_agent in agents:
                if (other_agent != agent and other_agent.is_alive and
                    self._should_empathize(agent, other_agent) and
                    random.random() < self.empathy_base_chance):
                    
                    empathy_event = self._create_empathy_event(agent, other_agent, current_day)
                    if empathy_event:
                        self.empathy_events.append(empathy_event)
                        
                        events.append({
                            "type": "empathy_connection",
                            "empathizer": agent.name,
                            "target": other_agent.name,
                            "emotion_shared": empathy_event.emotion_shared.value,
                            "strength": empathy_event.empathy_strength,
                            "day": current_day
                        })
        
        return events
    
    def _process_emotional_contagion(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process emotions spreading through the community."""
        events = []
        
        # Update existing contagions
        for contagion in self.emotional_contagions:
            if current_day - contagion.started_day < contagion.duration:
                spread_events = self._spread_emotional_contagion(contagion, agents, current_day)
                events.extend(spread_events)
        
        # Check for new contagion sources
        for agent in agents:
            if (agent.is_alive and agent.name in self.agent_emotional_states):
                emotional_state = self.agent_emotional_states[agent.name]
                
                # High intensity emotions can start contagions
                for emotion_type, intensity in emotional_state.primary_emotions.items():
                    if (intensity > 0.8 and random.random() < 0.1):  # 10% chance for very intense emotions
                        contagion = self._start_emotional_contagion(agent, emotion_type, intensity, current_day)
                        if contagion:
                            self.emotional_contagions.append(contagion)
                            
                            events.append({
                                "type": "emotional_contagion_started",
                                "source": agent.name,
                                "emotion": emotion_type.value,
                                "intensity": intensity,
                                "day": current_day
                            })
        
        return events
    
    def _process_emotional_growth(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process emotional growth and learning."""
        events = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            # Check for emotional growth opportunities
            if random.random() < self.emotional_growth_chance:
                growth_event = self._create_emotional_growth_event(agent, current_day)
                if growth_event:
                    self.emotional_growth_events.append(growth_event)
                    
                    # Update agent's emotional development
                    self._apply_emotional_growth(agent, growth_event)
                    
                    events.append({
                        "type": "emotional_growth",
                        "agent": agent.name,
                        "growth_type": growth_event.growth_type,
                        "lesson": growth_event.emotional_lesson,
                        "impact": growth_event.growth_impact,
                        "day": current_day
                    })
        
        return events
    
    def _process_trauma_healing(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process trauma healing for affected agents."""
        events = []
        
        for agent in agents:
            if not agent.is_alive or agent.name not in self.trauma_events:
                continue
            
            for trauma in self.trauma_events[agent.name]:
                if trauma.healing_progress < 1.0:  # Still healing
                    healing_event = self._advance_trauma_healing(agent, trauma, current_day)
                    if healing_event:
                        events.append(healing_event)
        
        return events
    
    def _calculate_current_emotional_state(self, agent: Any, current_day: int) -> EmotionalState:
        """Calculate an agent's current emotional state."""
        # Base emotions from personality
        base_emotions = {
            EmotionType.JOY: agent.personality_scores.get("extraversion", 0.5) * 0.6,
            EmotionType.SADNESS: agent.personality_scores.get("neuroticism", 0.5) * 0.4,
            EmotionType.ANGER: (1.0 - agent.personality_scores.get("agreeableness", 0.5)) * 0.3,
            EmotionType.FEAR: agent.personality_scores.get("neuroticism", 0.5) * 0.5,
            EmotionType.SURPRISE: agent.personality_scores.get("openness", 0.5) * 0.4,
            EmotionType.DISGUST: 0.1,  # Base level
            EmotionType.LOVE: agent.personality_scores.get("agreeableness", 0.5) * 0.5,
            EmotionType.CONTEMPT: (1.0 - agent.personality_scores.get("agreeableness", 0.5)) * 0.2
        }
        
        # Modify based on recent experiences
        recent_memories = agent.memory.get_recent_memories(days=7)
        triggering_events = []
        
        for memory in recent_memories:
            if hasattr(memory, 'emotion') and memory.emotion:
                emotion_boost = memory.importance * 0.3
                
                if memory.emotion in ["happy", "joyful", "excited"]:
                    base_emotions[EmotionType.JOY] += emotion_boost
                    triggering_events.append(f"Recent positive experience: {memory.content[:50]}")
                elif memory.emotion in ["sad", "grief", "melancholy"]:
                    base_emotions[EmotionType.SADNESS] += emotion_boost
                    triggering_events.append(f"Recent loss or sadness: {memory.content[:50]}")
                elif memory.emotion in ["angry", "frustrated", "irritated"]:
                    base_emotions[EmotionType.ANGER] += emotion_boost
                    triggering_events.append(f"Recent frustration: {memory.content[:50]}")
                elif memory.emotion in ["afraid", "worried", "anxious"]:
                    base_emotions[EmotionType.FEAR] += emotion_boost
                    triggering_events.append(f"Recent concern: {memory.content[:50]}")
        
        # Normalize emotions
        for emotion in base_emotions:
            base_emotions[emotion] = min(1.0, max(0.0, base_emotions[emotion]))
        
        # Calculate emotional characteristics
        emotional_intensity = sum(base_emotions.values()) / len(base_emotions)
        emotional_stability = 1.0 - agent.personality_scores.get("neuroticism", 0.5)
        emotional_expressiveness = agent.personality_scores.get("extraversion", 0.5)
        emotional_regulation = agent.personality_scores.get("conscientiousness", 0.5)
        
        return EmotionalState(
            agent_name=agent.name,
            day=current_day,
            primary_emotions=base_emotions,
            complex_emotions={},
            emotional_intensity=emotional_intensity,
            emotional_stability=emotional_stability,
            emotional_expressiveness=emotional_expressiveness,
            emotional_regulation=emotional_regulation,
            triggering_events=triggering_events,
            social_influences=[],
            internal_factors=[]
        )
    
    def _create_empathy_event(self, empathizer: Any, target: Any, current_day: int) -> Optional[EmpathyEvent]:
        """Create an empathy event between two agents."""
        if target.name not in self.agent_emotional_states:
            return None
        
        target_state = self.agent_emotional_states[target.name]
        dominant_emotion = self._get_dominant_emotion(target_state)
        
        # Calculate empathy strength
        empathy_strength = self._calculate_empathy_strength(empathizer, target, dominant_emotion)
        
        if empathy_strength >= 0.3:  # Minimum empathy threshold
            # Generate empathetic response
            responses = self.empathy_responses.get(dominant_emotion, ["Offering general support"])
            empathy_response = random.choice(responses)
            
            # Create memories for both agents
            empathizer.memory.store_memory(
                f"I felt {target.name}'s {dominant_emotion.value} deeply. {empathy_response}",
                importance=0.6,
                emotion="empathetic",
                memory_type="social"
            )
            
            target.memory.store_memory(
                f"{empathizer.name} seemed to understand how I was feeling. Their support meant a lot.",
                importance=0.7,
                emotion="grateful",
                memory_type="support"
            )
            
            return EmpathyEvent(
                empathizer=empathizer.name,
                target=target.name,
                emotion_shared=dominant_emotion,
                empathy_strength=empathy_strength,
                day=current_day,
                situation=f"Responding to {target.name}'s {dominant_emotion.value}",
                empathy_response=empathy_response,
                emotional_support_given=empathy_response,
                long_term_impact=empathy_strength * 0.5
            )
        
        return None
    
    def _calculate_empathy_strength(self, empathizer: Any, target: Any, emotion: EmotionType) -> float:
        """Calculate strength of empathetic connection."""
        base_empathy = empathizer.personality_scores.get("agreeableness", 0.5)
        
        # Relationship bonus
        relationship_strength = 0.0
        if hasattr(empathizer, 'relationships') and target.name in empathizer.relationships:
            relationship_type = empathizer.relationships[target.name]
            if relationship_type in ["family", "close_friend"]:
                relationship_strength = 0.4
            elif relationship_type in ["friend"]:
                relationship_strength = 0.2
        
        # Shared experience bonus
        shared_experience = 0.0
        if hasattr(empathizer, 'life_experiences') and hasattr(target, 'life_experiences'):
            # Check for similar emotional experiences
            shared_experience = 0.1  # Simplified for now
        
        # Age and wisdom factor
        age_factor = min(0.2, empathizer.age / 100.0)  # Older agents more empathetic
        
        return min(1.0, base_empathy + relationship_strength + shared_experience + age_factor)
    
    def _get_dominant_emotion(self, emotional_state: EmotionalState) -> EmotionType:
        """Get the strongest emotion in an emotional state."""
        return max(emotional_state.primary_emotions.items(), key=lambda x: x[1])[0]
    
    def _should_empathize(self, agent: Any, other_agent: Any) -> bool:
        """Check if agent should empathize with another."""
        # Must be in same location
        if agent.location != other_agent.location:
            return False
        
        # Higher chance with family and friends
        if hasattr(agent, 'relationships') and other_agent.name in agent.relationships:
            return True
        
        # Random chance with others
        return random.random() < 0.3
    
    def get_agent_emotional_summary(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive emotional summary for an agent."""
        if agent_name not in self.agent_emotional_states:
            return None
        
        emotional_state = self.agent_emotional_states[agent_name]
        growth_events = [e for e in self.emotional_growth_events if e.agent_name == agent_name]
        empathy_given = [e for e in self.empathy_events if e.empathizer == agent_name]
        empathy_received = [e for e in self.empathy_events if e.target == agent_name]
        trauma_history = self.trauma_events.get(agent_name, [])
        
        return {
            "current_emotions": {emotion.value: intensity 
                               for emotion, intensity in emotional_state.primary_emotions.items()},
            "complex_emotions": {emotion.value: intensity 
                               for emotion, intensity in emotional_state.complex_emotions.items()},
            "emotional_regulation": emotional_state.emotional_regulation,
            "empathy_given": len(empathy_given),
            "empathy_received": len(empathy_received),
            "emotional_growth_events": len(growth_events),
            "trauma_events": len(trauma_history),
            "dominant_emotion": self._get_dominant_emotion(emotional_state).value,
            "emotional_intensity": emotional_state.emotional_intensity
        }
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get comprehensive emotional complexity system summary."""
        total_growth_events = len(self.emotional_growth_events)
        total_empathy_events = len(self.empathy_events)
        total_trauma_events = sum(len(traumas) for traumas in self.trauma_events.values())
        
        return {
            "agents_tracked": len(self.agent_emotional_states),
            "total_emotional_growth_events": total_growth_events,
            "total_empathy_connections": total_empathy_events,
            "total_trauma_events": total_trauma_events,
            "active_emotional_contagions": len([c for c in self.emotional_contagions 
                                              if not c.natural_decay]),
            "average_emotional_intensity": sum(state.emotional_intensity 
                                             for state in self.agent_emotional_states.values()) / 
                                         max(1, len(self.agent_emotional_states)),
            "community_empathy_rate": total_empathy_events / max(1, len(self.agent_emotional_states))
        } 

    def _has_significant_emotional_change(self, agent: Any, emotional_state: EmotionalState) -> bool:
        """Check if agent has had a significant emotional change."""
        # For now, always consider changes significant for logging
        # In a full implementation, this would compare with previous state
        return emotional_state.emotional_intensity > 0.7
    
    def _complex_emotion_triggered(self, emotional_state: EmotionalState, recipe: Dict) -> bool:
        """Check if conditions are met for a complex emotion."""
        components = recipe["components"]
        
        # Check if all required emotions are present with sufficient intensity
        for emotion_type, required_intensity in components.items():
            current_intensity = emotional_state.primary_emotions.get(emotion_type, 0.0)
            if current_intensity < required_intensity * 0.7:  # 70% of required intensity
                return False
        
        return True
    
    def _calculate_complex_emotion_intensity(self, emotional_state: EmotionalState, recipe: Dict) -> float:
        """Calculate intensity of a complex emotion."""
        components = recipe["components"]
        total_intensity = 0.0
        
        for emotion_type, required_intensity in components.items():
            current_intensity = emotional_state.primary_emotions.get(emotion_type, 0.0)
            contribution = min(current_intensity, required_intensity)
            total_intensity += contribution
        
        # Average intensity across components
        return total_intensity / len(components)
    
    def _spread_emotional_contagion(self, contagion: EmotionalContagion, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Spread emotional contagion to nearby agents."""
        events = []
        
        source_agent = self._get_agent_by_name(agents, contagion.source_agent)
        if not source_agent:
            return events
        
        # Find agents in same location who could be affected
        nearby_agents = [a for a in agents if (a.is_alive and 
                        a.location == source_agent.location and 
                        a.name != contagion.source_agent and
                        a.name not in contagion.affected_agents)]
        
        for agent in nearby_agents:
            # Check if emotion spreads to this agent
            spread_chance = contagion.spread_rate * (1 - agent.personality_scores.get("emotional_stability", 0.5))
            
            if random.random() < spread_chance:
                contagion.affected_agents.append(agent.name)
                
                # Update agent's emotional state
                if agent.name in self.agent_emotional_states:
                    agent_state = self.agent_emotional_states[agent.name]
                    current_level = agent_state.primary_emotions.get(contagion.emotion_type, 0.0)
                    boost = contagion.intensity * 0.3
                    agent_state.primary_emotions[contagion.emotion_type] = min(1.0, current_level + boost)
                
                events.append({
                    "type": "emotional_contagion_spread",
                    "source": contagion.source_agent,
                    "affected": agent.name,
                    "emotion": contagion.emotion_type.value,
                    "day": current_day
                })
        
        return events
    
    def _start_emotional_contagion(self, agent: Any, emotion_type: EmotionType, intensity: float, current_day: int) -> Optional[EmotionalContagion]:
        """Start a new emotional contagion."""
        return EmotionalContagion(
            source_agent=agent.name,
            emotion_type=emotion_type,
            intensity=intensity,
            started_day=current_day,
            affected_agents=[agent.name],
            spread_rate=self.contagion_spread_rate,
            peak_intensity=intensity,
            duration=random.randint(3, 10),  # 3-10 days
            natural_decay=True,
            intervention_events=[],
            final_impact={}
        )
    
    def _create_emotional_growth_event(self, agent: Any, current_day: int) -> Optional[EmotionalGrowthEvent]:
        """Create an emotional growth event for an agent."""
        growth_types = ["insight", "breakthrough", "healing", "wisdom"]
        growth_type = random.choice(growth_types)
        
        trigger = random.choice(self.growth_triggers)
        
        # Generate lesson based on growth type
        if growth_type == "insight":
            lesson = "Understanding emotions helps me connect better with others"
        elif growth_type == "breakthrough":
            lesson = "I can choose how to respond to my emotions"
        elif growth_type == "healing":
            lesson = "Time and support help heal emotional wounds"
        else:  # wisdom
            lesson = "Everyone struggles with emotions; showing compassion helps"
        
        return EmotionalGrowthEvent(
            agent_name=agent.name,
            growth_type=growth_type,
            trigger_event=trigger,
            day=current_day,
            emotional_lesson=lesson,
            old_pattern="Reacting automatically to emotions",
            new_understanding=lesson,
            growth_impact=random.uniform(0.3, 0.7),
            behavioral_changes=["Better emotional regulation"],
            improved_relationships=[],
            wisdom_gained=lesson
        )
    
    def _apply_emotional_growth(self, agent: Any, growth_event: EmotionalGrowthEvent):
        """Apply emotional growth to an agent."""
        # Create memory of growth
        agent.memory.store_memory(
            f"I learned something important about emotions: {growth_event.emotional_lesson}",
            importance=0.8,
            emotion="growth",
            memory_type="learning"
        )
        
        # Improve emotional regulation if agent has emotional state
        if agent.name in self.agent_emotional_states:
            emotional_state = self.agent_emotional_states[agent.name]
            emotional_state.emotional_regulation = min(1.0, 
                emotional_state.emotional_regulation + growth_event.growth_impact * 0.2)
    
    def _advance_trauma_healing(self, agent: Any, trauma: TraumaEvent, current_day: int) -> Optional[Dict[str, Any]]:
        """Advance trauma healing for an agent."""
        # Simple healing progression
        healing_rate = self.trauma_healing_rate
        
        # Support from others increases healing
        if hasattr(agent, 'relationships'):
            support_bonus = len([rel for rel in agent.relationships.values() 
                               if rel in ["family", "close_friend"]]) * 0.005
            healing_rate += support_bonus
        
        trauma.healing_progress = min(1.0, trauma.healing_progress + healing_rate)
        
        # Check for stage progression
        if trauma.healing_progress > 0.8 and trauma.healing_stage != "acceptance":
            old_stage = trauma.healing_stage
            trauma.healing_stage = "acceptance"
            
            # Create memory of healing progress
            agent.memory.store_memory(
                f"I'm healing from {trauma.trauma_description}. I'm learning to accept what happened.",
                importance=0.7,
                emotion="healing",
                memory_type="recovery"
            )
            
            return {
                "type": "trauma_healing_progress",
                "agent": agent.name,
                "trauma_type": trauma.trauma_type.value,
                "old_stage": old_stage,
                "new_stage": trauma.healing_stage,
                "healing_progress": trauma.healing_progress,
                "day": current_day
            }
        
        return None
    
    def _update_community_emotional_climate(self, agents: List[Any], current_day: int):
        """Update the overall emotional climate of the community."""
        if not self.agent_emotional_states:
            return
        
        # Calculate average emotions across all agents
        emotion_totals = {emotion: 0.0 for emotion in EmotionType}
        agent_count = 0
        
        for agent_name, emotional_state in self.agent_emotional_states.items():
            for emotion, intensity in emotional_state.primary_emotions.items():
                emotion_totals[emotion] += intensity
            agent_count += 1
        
        if agent_count > 0:
            community_climate = {emotion.value: total / agent_count 
                               for emotion, total in emotion_totals.items()}
            
            self.community_emotional_climate[current_day] = community_climate
    
    def _get_agent_by_name(self, agents: List[Any], name: str) -> Optional[Any]:
        """Get agent by name from list."""
        for agent in agents:
            if agent.name == name:
                return agent
        return None 