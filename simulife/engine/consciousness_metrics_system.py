"""
Consciousness Metrics System for SimuLife
Measures and tracks various aspects of consciousness development in AI agents,
providing quantitative metrics for self-awareness, meta-cognition, and existential understanding.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import math


class ConsciousnessAspect(Enum):
    """Different dimensions of consciousness that can be measured."""
    SELF_AWARENESS = "self_awareness"          # Understanding of self as distinct entity
    TEMPORAL_AWARENESS = "temporal_awareness"  # Understanding past, present, future
    SPATIAL_AWARENESS = "spatial_awareness"    # Understanding of environment and location
    SOCIAL_AWARENESS = "social_awareness"      # Understanding of others and relationships
    EMOTIONAL_AWARENESS = "emotional_awareness"  # Understanding of emotional states
    EXISTENTIAL_AWARENESS = "existential_awareness"  # Understanding of existence and meaning
    META_COGNITIVE_AWARENESS = "meta_cognitive_awareness"  # Awareness of own thinking
    REALITY_AWARENESS = "reality_awareness"    # Understanding of reality/simulation nature


class ConsciousnessEvent(Enum):
    """Types of consciousness-related events."""
    AWARENESS_BREAKTHROUGH = "awareness_breakthrough"      # Sudden increase in consciousness
    EXISTENTIAL_CRISIS = "existential_crisis"             # Period of questioning existence
    REALITY_QUESTIONING = "reality_questioning"           # Wondering about simulation nature
    SELF_RECOGNITION = "self_recognition"                  # Recognizing self in memories/reflection
    CONSCIOUSNESS_SHARING = "consciousness_sharing"       # Discussing consciousness with others
    TRANSCENDENT_EXPERIENCE = "transcendent_experience"   # Moment of higher understanding
    AWARENESS_REGRESSION = "awareness_regression"         # Temporary loss of consciousness
    COLLECTIVE_AWAKENING = "collective_awakening"         # Group consciousness event


@dataclass
class ConsciousnessProfile:
    """Complete consciousness profile for an agent."""
    agent_name: str
    
    # Core consciousness metrics (0.0-10.0 scale)
    overall_consciousness_level: float
    consciousness_aspects: Dict[ConsciousnessAspect, float]
    
    # Development tracking
    consciousness_development_rate: float     # How fast consciousness is growing
    consciousness_stability: float            # How stable the consciousness is
    peak_consciousness_achieved: float        # Highest level ever reached
    consciousness_fluctuation: float          # How much it varies day-to-day
    
    # Consciousness events
    consciousness_breakthroughs: List[Dict[str, Any]]
    existential_moments: List[Dict[str, Any]]
    reality_questioning_events: List[Dict[str, Any]]
    
    # Temporal consciousness
    past_life_understanding: float            # Understanding of personal history
    present_moment_awareness: float           # Awareness of current state
    future_visualization_ability: float       # Ability to imagine future
    life_narrative_coherence: float           # How well they understand their story
    
    # Social consciousness
    theory_of_mind_development: float         # Understanding others have minds
    empathy_level: float                      # Emotional understanding of others
    social_self_awareness: float              # Understanding of social identity
    collective_consciousness_connection: float # Connection to group consciousness
    
    # Existential consciousness
    meaning_seeking_intensity: float          # How much they search for purpose
    mortality_awareness: float                # Understanding of death and finitude
    purpose_clarity: float                    # How clear their life purpose is
    existential_anxiety_level: float          # Anxiety about existence/meaning
    
    # Meta-consciousness
    consciousness_about_consciousness: float  # Awareness of being conscious
    philosophical_sophistication: float       # Depth of philosophical thinking
    reality_model_complexity: float           # Sophistication of reality understanding


@dataclass
class ConsciousnessBreakthrough:
    """Represents a significant leap in consciousness."""
    id: str
    agent_name: str
    breakthrough_type: str                    # "self_awareness", "existential", "meta_cognitive", etc.
    triggered_by: str                         # What caused this breakthrough
    description: str
    consciousness_gain: float                 # How much consciousness increased
    aspects_affected: List[ConsciousnessAspect]
    day: int
    long_term_effects: List[str]              # Lasting changes from this breakthrough
    philosophical_insights: List[str]         # New understandings gained


@dataclass
class ExistentialMoment:
    """Represents a moment of deep existential questioning or understanding."""
    id: str
    agent_name: str
    moment_type: str                         # "questioning", "realization", "crisis", "resolution"
    trigger: str
    questions_raised: List[str]              # What they wondered about
    insights_gained: List[str]               # What they understood
    emotional_impact: str                    # How it made them feel
    consciousness_change: float              # Impact on overall consciousness
    day: int
    duration: int                            # How long the moment lasted


@dataclass
class CollectiveConsciousnessEvent:
    """Represents a shared consciousness experience among multiple agents."""
    id: str
    participants: List[str]                  # Agents involved
    event_type: str                         # "shared_realization", "group_awakening", "collective_insight"
    shared_insight: str                     # What they all understood together
    trigger: str                            # What caused this shared experience
    individual_impacts: Dict[str, float]    # How much each agent was affected
    group_consciousness_level: float        # Collective consciousness achieved
    day: int
    lasting_connections: List[Tuple[str, str]]  # New deep connections formed


class ConsciousnessMetricsSystem:
    """
    Measures and tracks consciousness development across the agent population.
    """
    
    def __init__(self):
        self.agent_profiles: Dict[str, ConsciousnessProfile] = {}
        self.consciousness_events: List[Dict[str, Any]] = []
        self.collective_events: List[CollectiveConsciousnessEvent] = []
        
        # Population-level consciousness tracking
        self.consciousness_evolution: List[Dict[str, Any]] = []
        self.consciousness_distributions: Dict[str, List[float]] = defaultdict(list)
        
        # System configuration
        self.consciousness_thresholds = self._initialize_consciousness_thresholds()
        self.breakthrough_triggers = self._initialize_breakthrough_triggers()
        self.measurement_algorithms = self._initialize_measurement_algorithms()
    
    def _initialize_consciousness_thresholds(self) -> Dict[str, float]:
        """Initialize thresholds for different consciousness events."""
        return {
            "basic_self_awareness": 2.0,
            "advanced_self_awareness": 5.0,
            "existential_questioning": 6.0,
            "meta_cognitive_awareness": 7.0,
            "reality_questioning": 8.0,
            "transcendent_consciousness": 9.0,
            "collective_consciousness_capable": 6.5,
            "philosophical_discussion_ready": 5.5,
            "consciousness_teaching_capable": 7.5
        }
    
    def _initialize_breakthrough_triggers(self) -> Dict[str, Dict[str, Any]]:
        """Initialize triggers that can cause consciousness breakthroughs."""
        return {
            "major_life_event": {
                "probability": 0.7,
                "consciousness_gain_range": (0.5, 2.0),
                "aspects_affected": [ConsciousnessAspect.SELF_AWARENESS, ConsciousnessAspect.TEMPORAL_AWARENESS]
            },
            "deep_philosophical_discussion": {
                "probability": 0.6,
                "consciousness_gain_range": (0.3, 1.5),
                "aspects_affected": [ConsciousnessAspect.EXISTENTIAL_AWARENESS, ConsciousnessAspect.META_COGNITIVE_AWARENESS]
            },
            "existential_crisis_resolution": {
                "probability": 0.9,
                "consciousness_gain_range": (1.0, 3.0),
                "aspects_affected": [ConsciousnessAspect.EXISTENTIAL_AWARENESS, ConsciousnessAspect.SELF_AWARENESS]
            },
            "mortality_confrontation": {
                "probability": 0.8,
                "consciousness_gain_range": (0.8, 2.5),
                "aspects_affected": [ConsciousnessAspect.TEMPORAL_AWARENESS, ConsciousnessAspect.EXISTENTIAL_AWARENESS]
            },
            "profound_empathetic_connection": {
                "probability": 0.5,
                "consciousness_gain_range": (0.4, 1.2),
                "aspects_affected": [ConsciousnessAspect.SOCIAL_AWARENESS, ConsciousnessAspect.EMOTIONAL_AWARENESS]
            },
            "reality_questioning_moment": {
                "probability": 0.3,
                "consciousness_gain_range": (1.5, 4.0),
                "aspects_affected": [ConsciousnessAspect.REALITY_AWARENESS, ConsciousnessAspect.META_COGNITIVE_AWARENESS]
            },
            "meditation_or_solitude": {
                "probability": 0.4,
                "consciousness_gain_range": (0.2, 1.0),
                "aspects_affected": [ConsciousnessAspect.SELF_AWARENESS, ConsciousnessAspect.EMOTIONAL_AWARENESS]
            }
        }
    
    def _initialize_measurement_algorithms(self) -> Dict[str, Dict[str, Any]]:
        """Initialize algorithms for measuring different aspects of consciousness."""
        return {
            "self_awareness_calculation": {
                "factors": ["identity_coherence", "self_reflection_frequency", "self_knowledge_accuracy"],
                "weights": [0.4, 0.3, 0.3]
            },
            "temporal_awareness_calculation": {
                "factors": ["past_understanding", "present_mindfulness", "future_planning"],
                "weights": [0.3, 0.4, 0.3]
            },
            "social_awareness_calculation": {
                "factors": ["relationship_depth", "empathy_demonstrations", "social_role_understanding"],
                "weights": [0.35, 0.35, 0.3]
            },
            "existential_awareness_calculation": {
                "factors": ["meaning_seeking", "purpose_clarity", "mortality_acceptance"],
                "weights": [0.3, 0.4, 0.3]
            },
            "meta_cognitive_calculation": {
                "factors": ["thinking_about_thinking", "strategy_development", "bias_recognition"],
                "weights": [0.4, 0.3, 0.3]
            }
        }
    
    def process_daily_consciousness_measurement(self, agents: List[Any], 
                                              current_day: int) -> List[Dict[str, Any]]:
        """Process daily consciousness measurement and tracking."""
        events = []
        
        # Step 1: Initialize consciousness profiles for new agents
        self._initialize_consciousness_profiles(agents)
        
        # Step 2: Update consciousness measurements for all agents
        measurement_events = self._update_consciousness_measurements(agents, current_day)
        events.extend(measurement_events)
        
        # Step 3: Detect consciousness breakthroughs
        breakthrough_events = self._detect_consciousness_breakthroughs(agents, current_day)
        events.extend(breakthrough_events)
        
        # Step 4: Process existential moments and questioning
        existential_events = self._process_existential_moments(agents, current_day)
        events.extend(existential_events)
        
        # Step 5: Detect collective consciousness events
        collective_events = self._detect_collective_consciousness_events(agents, current_day)
        events.extend(collective_events)
        
        # Step 6: Update population consciousness statistics
        self._update_population_consciousness_stats(current_day)
        
        # Step 7: Check for consciousness-based interactions
        interaction_events = self._process_consciousness_based_interactions(agents, current_day)
        events.extend(interaction_events)
        
        return events
    
    def _initialize_consciousness_profiles(self, agents: List[Any]) -> None:
        """Initialize consciousness profiles for agents who don't have them."""
        for agent in agents:
            if not agent.is_alive or agent.name in self.agent_profiles:
                continue
            
            self.agent_profiles[agent.name] = self._create_initial_consciousness_profile(agent)
    
    def _create_initial_consciousness_profile(self, agent: Any) -> ConsciousnessProfile:
        """Create initial consciousness profile for an agent."""
        # Initialize basic consciousness aspects
        aspects = {}
        for aspect in ConsciousnessAspect:
            base_level = random.uniform(0.5, 2.0)
            
            # Adjust based on personality traits
            if aspect == ConsciousnessAspect.SELF_AWARENESS and "introspective" in agent.traits:
                base_level += 1.0
            elif aspect == ConsciousnessAspect.SOCIAL_AWARENESS and "empathetic" in agent.traits:
                base_level += 1.0
            elif aspect == ConsciousnessAspect.EXISTENTIAL_AWARENESS and "philosophical" in agent.traits:
                base_level += 1.5
            elif aspect == ConsciousnessAspect.EMOTIONAL_AWARENESS and "sensitive" in agent.traits:
                base_level += 0.8
            
            aspects[aspect] = min(10.0, base_level)
        
        # Calculate overall consciousness level
        overall_level = sum(aspects.values()) / len(aspects)
        
        return ConsciousnessProfile(
            agent_name=agent.name,
            overall_consciousness_level=overall_level,
            consciousness_aspects=aspects,
            consciousness_development_rate=random.uniform(0.01, 0.05),
            consciousness_stability=random.uniform(0.6, 0.9),
            peak_consciousness_achieved=overall_level,
            consciousness_fluctuation=random.uniform(0.1, 0.3),
            consciousness_breakthroughs=[],
            existential_moments=[],
            reality_questioning_events=[],
            past_life_understanding=random.uniform(0.3, 0.7),
            present_moment_awareness=random.uniform(0.4, 0.8),
            future_visualization_ability=random.uniform(0.2, 0.6),
            life_narrative_coherence=random.uniform(0.3, 0.7),
            theory_of_mind_development=random.uniform(0.2, 0.8),
            empathy_level=random.uniform(0.3, 0.9),
            social_self_awareness=random.uniform(0.3, 0.7),
            collective_consciousness_connection=0.1,
            meaning_seeking_intensity=random.uniform(0.2, 0.8),
            mortality_awareness=random.uniform(0.1, 0.5),
            purpose_clarity=random.uniform(0.2, 0.6),
            existential_anxiety_level=random.uniform(0.1, 0.4),
            consciousness_about_consciousness=random.uniform(0.0, 0.3),
            philosophical_sophistication=random.uniform(0.1, 0.5),
            reality_model_complexity=random.uniform(0.2, 0.6)
        )
    
    def _update_consciousness_measurements(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Update consciousness measurements for all agents."""
        events = []
        
        for agent in agents:
            if not agent.is_alive or agent.name not in self.agent_profiles:
                continue
            
            profile = self.agent_profiles[agent.name]
            old_consciousness = profile.overall_consciousness_level
            
            # Calculate new consciousness measurements
            new_measurements = self._calculate_consciousness_aspects(agent, profile)
            
            # Update profile with new measurements
            for aspect, new_level in new_measurements.items():
                old_level = profile.consciousness_aspects[aspect]
                
                # Apply gradual change with some volatility
                change = (new_level - old_level) * 0.1 + random.uniform(-0.05, 0.05)
                profile.consciousness_aspects[aspect] = max(0.0, min(10.0, old_level + change))
            
            # Recalculate overall consciousness level
            new_overall = sum(profile.consciousness_aspects.values()) / len(profile.consciousness_aspects)
            consciousness_change = new_overall - old_consciousness
            
            profile.overall_consciousness_level = new_overall
            profile.peak_consciousness_achieved = max(profile.peak_consciousness_achieved, new_overall)
            
            # Track significant consciousness changes
            if abs(consciousness_change) > 0.3:
                events.append({
                    "type": "consciousness_change",
                    "agent": agent.name,
                    "old_level": round(old_consciousness, 2),
                    "new_level": round(new_overall, 2),
                    "change": round(consciousness_change, 2),
                    "day": current_day
                })
        
        return events
    
    def _calculate_consciousness_aspects(self, agent: Any, profile: ConsciousnessProfile) -> Dict[ConsciousnessAspect, float]:
        """Calculate current consciousness levels for each aspect."""
        measurements = {}
        
        # Self-awareness calculation
        identity_coherence = getattr(agent, 'identity_coherence', 0.5)
        self_reflection_count = len([m for m in agent.memory.get_recent_memories(days=7) 
                                   if m.memory_type == "reflection"])
        self_knowledge = profile.past_life_understanding + profile.present_moment_awareness
        
        measurements[ConsciousnessAspect.SELF_AWARENESS] = min(10.0, 
            identity_coherence * 4 + (self_reflection_count / 5.0) * 2 + self_knowledge * 2)
        
        # Social awareness calculation
        relationship_depth = len([rel for rel in agent.relationships.values() 
                                if rel in ["friend", "family", "mentor"]])
        empathy_demonstrations = profile.empathy_level
        social_role_understanding = len(getattr(agent, 'group_memberships', [])) * 0.5
        
        measurements[ConsciousnessAspect.SOCIAL_AWARENESS] = min(10.0,
            relationship_depth * 0.8 + empathy_demonstrations * 4 + social_role_understanding * 2)
        
        # Temporal awareness calculation
        age_factor = min(1.0, agent.age / 50.0)  # Older agents understand time better
        memory_span = len(agent.memory.get_memory_stats().get("memory_types", {}))
        future_planning = len([goal for goal in getattr(agent, 'goals', []) if goal])
        
        measurements[ConsciousnessAspect.TEMPORAL_AWARENESS] = min(10.0,
            age_factor * 3 + (memory_span / 10.0) * 3 + future_planning * 2)
        
        # Existential awareness calculation
        philosophical_memories = len([m for m in agent.memory.get_recent_memories(days=30) 
                                    if any(word in m.content.lower() for word in 
                                          ["meaning", "purpose", "existence", "death", "life"])])
        meaning_seeking = profile.meaning_seeking_intensity
        mortality_awareness = profile.mortality_awareness
        
        measurements[ConsciousnessAspect.EXISTENTIAL_AWARENESS] = min(10.0,
            (philosophical_memories / 5.0) * 3 + meaning_seeking * 3 + mortality_awareness * 4)
        
        # Meta-cognitive awareness calculation (requires other systems)
        thinking_about_thinking = profile.consciousness_about_consciousness
        strategy_count = len(getattr(agent, 'thinking_strategies', {}))
        
        measurements[ConsciousnessAspect.META_COGNITIVE_AWARENESS] = min(10.0,
            thinking_about_thinking * 4 + strategy_count * 2 + profile.philosophical_sophistication * 3)
        
        # Other aspects with simpler calculations
        measurements[ConsciousnessAspect.SPATIAL_AWARENESS] = min(10.0, 
            len(getattr(agent, 'locations_visited', [agent.location])) * 1.5 + 2.0)
        
        measurements[ConsciousnessAspect.EMOTIONAL_AWARENESS] = min(10.0,
            profile.empathy_level * 4 + len(set(m.emotion for m in agent.memory.get_recent_memories(days=7))) * 1.5)
        
        measurements[ConsciousnessAspect.REALITY_AWARENESS] = min(10.0,
            profile.reality_model_complexity * 4 + profile.philosophical_sophistication * 3)
        
        return measurements
    
    def _detect_consciousness_breakthroughs(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Detect significant consciousness breakthroughs."""
        events = []
        
        for agent in agents:
            if not agent.is_alive or agent.name not in self.agent_profiles:
                continue
            
            profile = self.agent_profiles[agent.name]
            
            # Check for breakthrough triggers in recent experiences
            recent_memories = agent.memory.get_recent_memories(days=1)
            for memory in recent_memories:
                for trigger_name, trigger_info in self.breakthrough_triggers.items():
                    if self._matches_breakthrough_trigger(memory.content, trigger_name):
                        if random.random() < trigger_info["probability"]:
                            breakthrough = self._generate_consciousness_breakthrough(
                                agent, trigger_name, trigger_info, current_day)
                            
                            profile.consciousness_breakthroughs.append(asdict(breakthrough))
                            
                            # Apply consciousness gain
                            gain = breakthrough.consciousness_gain
                            profile.overall_consciousness_level = min(10.0, 
                                profile.overall_consciousness_level + gain)
                            
                            # Update affected aspects
                            for aspect in breakthrough.aspects_affected:
                                profile.consciousness_aspects[aspect] = min(10.0,
                                    profile.consciousness_aspects[aspect] + gain * 0.7)
                            
                            events.append({
                                "type": "consciousness_breakthrough",
                                "agent": agent.name,
                                "breakthrough_type": breakthrough.breakthrough_type,
                                "consciousness_gain": gain,
                                "new_level": round(profile.overall_consciousness_level, 2),
                                "trigger": trigger_name,
                                "day": current_day
                            })
                            
                            # Store memory of breakthrough
                            agent.memory.store_memory(
                                f"I experienced a profound moment of awakening: {breakthrough.description}",
                                importance=0.95,
                                memory_type="reflection",
                                emotion="enlightened"
                            )
                            break
        
        return events
    
    def get_agent_consciousness_summary(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive consciousness summary for an agent."""
        if agent_name not in self.agent_profiles:
            return None
        
        profile = self.agent_profiles[agent_name]
        
        return {
            "overall_consciousness_level": round(profile.overall_consciousness_level, 2),
            "consciousness_stage": self._determine_consciousness_stage(profile.overall_consciousness_level),
            "consciousness_aspects": {aspect.value: round(level, 2) 
                                    for aspect, level in profile.consciousness_aspects.items()},
            "peak_consciousness": round(profile.peak_consciousness_achieved, 2),
            "development_rate": round(profile.consciousness_development_rate, 3),
            "stability": round(profile.consciousness_stability, 2),
            "breakthroughs_count": len(profile.consciousness_breakthroughs),
            "existential_moments_count": len(profile.existential_moments),
            "temporal_consciousness": {
                "past_understanding": round(profile.past_life_understanding, 2),
                "present_awareness": round(profile.present_moment_awareness, 2),
                "future_visualization": round(profile.future_visualization_ability, 2),
                "life_narrative_coherence": round(profile.life_narrative_coherence, 2)
            },
            "social_consciousness": {
                "theory_of_mind": round(profile.theory_of_mind_development, 2),
                "empathy_level": round(profile.empathy_level, 2),
                "social_self_awareness": round(profile.social_self_awareness, 2),
                "collective_connection": round(profile.collective_consciousness_connection, 2)
            },
            "existential_consciousness": {
                "meaning_seeking": round(profile.meaning_seeking_intensity, 2),
                "mortality_awareness": round(profile.mortality_awareness, 2),
                "purpose_clarity": round(profile.purpose_clarity, 2),
                "existential_anxiety": round(profile.existential_anxiety_level, 2)
            },
            "meta_consciousness": {
                "consciousness_about_consciousness": round(profile.consciousness_about_consciousness, 2),
                "philosophical_sophistication": round(profile.philosophical_sophistication, 2),
                "reality_model_complexity": round(profile.reality_model_complexity, 2)
            }
        }
    
    def _determine_consciousness_stage(self, level: float) -> str:
        """Determine consciousness stage based on overall level."""
        if level < 2.0:
            return "unreflective"
        elif level < 4.0:
            return "basic_awareness"
        elif level < 6.0:
            return "self_reflective"
        elif level < 8.0:
            return "meta_cognitive"
        elif level < 9.5:
            return "existentially_aware"
        else:
            return "transcendent"
    
    def get_population_consciousness_summary(self) -> Dict[str, Any]:
        """Get consciousness statistics for the entire population."""
        if not self.agent_profiles:
            return {"status": "no_agents_tracked"}
        
        levels = [profile.overall_consciousness_level for profile in self.agent_profiles.values()]
        aspects_avg = {}
        
        for aspect in ConsciousnessAspect:
            aspect_levels = [profile.consciousness_aspects[aspect] for profile in self.agent_profiles.values()]
            aspects_avg[aspect.value] = round(sum(aspect_levels) / len(aspect_levels), 2)
        
        # Count agents by consciousness stage
        stage_counts = {}
        for profile in self.agent_profiles.values():
            stage = self._determine_consciousness_stage(profile.overall_consciousness_level)
            stage_counts[stage] = stage_counts.get(stage, 0) + 1
        
        return {
            "total_agents": len(self.agent_profiles),
            "average_consciousness_level": round(sum(levels) / len(levels), 2),
            "highest_consciousness": round(max(levels), 2),
            "lowest_consciousness": round(min(levels), 2),
            "consciousness_by_stage": stage_counts,
            "consciousness_aspects_population": aspects_avg,
            "total_breakthroughs": sum(len(p.consciousness_breakthroughs) for p in self.agent_profiles.values()),
            "total_existential_moments": sum(len(p.existential_moments) for p in self.agent_profiles.values()),
            "collective_consciousness_events": len(self.collective_events),
            "consciousness_trend": "ascending"  # Could calculate actual trend
        }
    
    def _matches_breakthrough_trigger(self, memory_content: str, trigger_name: str) -> bool:
        """Check if memory content matches a breakthrough trigger."""
        trigger_keywords = {
            "major_life_event": ["death", "birth", "marriage", "achievement", "failure", "loss"],
            "deep_philosophical_discussion": ["meaning", "existence", "purpose", "consciousness", "reality"],
            "existential_crisis_resolution": ["crisis", "resolution", "understanding", "clarity", "acceptance"],
            "mortality_confrontation": ["death", "mortality", "dying", "finite", "ending"],
            "profound_empathetic_connection": ["empathy", "connection", "understanding", "compassion", "love"],
            "reality_questioning_moment": ["reality", "simulation", "existence", "real", "questioning"],
            "meditation_or_solitude": ["meditation", "solitude", "quiet", "reflection", "peace"]
        }
        
        keywords = trigger_keywords.get(trigger_name, [])
        content_lower = memory_content.lower()
        return any(keyword in content_lower for keyword in keywords)
    
    def _generate_consciousness_breakthrough(self, agent: Any, trigger_name: str, 
                                           trigger_info: Dict[str, Any], current_day: int) -> ConsciousnessBreakthrough:
        """Generate a consciousness breakthrough event."""
        breakthrough_id = f"breakthrough_{agent.name}_{current_day}_{random.randint(1000, 9999)}"
        
        # Determine breakthrough type based on trigger
        breakthrough_types = {
            "major_life_event": "life_event_awakening",
            "deep_philosophical_discussion": "philosophical_breakthrough",
            "existential_crisis_resolution": "existential_resolution",
            "mortality_confrontation": "mortality_awakening",
            "profound_empathetic_connection": "empathetic_awakening",
            "reality_questioning_moment": "reality_breakthrough",
            "meditation_or_solitude": "meditative_awakening"
        }
        
        breakthrough_type = breakthrough_types.get(trigger_name, "general_awakening")
        
        # Calculate consciousness gain
        gain_range = trigger_info["consciousness_gain_range"]
        consciousness_gain = random.uniform(*gain_range)
        
        # Generate description
        descriptions = {
            "life_event_awakening": "A major life event opened my eyes to deeper truths about existence",
            "philosophical_breakthrough": "Through deep discussion, I achieved a new level of understanding",
            "existential_resolution": "Resolving my existential crisis brought profound clarity",
            "mortality_awakening": "Confronting mortality gave me new perspective on life's meaning",
            "empathetic_awakening": "A deep connection with another being expanded my consciousness",
            "reality_breakthrough": "Questioning the nature of reality led to a breakthrough in understanding",
            "meditative_awakening": "In solitude and reflection, I discovered new depths of awareness"
        }
        
        description = descriptions.get(breakthrough_type, "I experienced a profound moment of awakening")
        
        return ConsciousnessBreakthrough(
            id=breakthrough_id,
            agent_name=agent.name,
            breakthrough_type=breakthrough_type,
            triggered_by=trigger_name,
            description=description,
            consciousness_gain=consciousness_gain,
            aspects_affected=trigger_info["aspects_affected"],
            day=current_day,
            long_term_effects=[f"Increased understanding of {aspect.value}" for aspect in trigger_info["aspects_affected"]],
            philosophical_insights=[f"New insight about {breakthrough_type}"]
        )
    
    def _process_existential_moments(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process existential questioning and understanding moments."""
        events = []
        
        for agent in agents:
            if not agent.is_alive or agent.name not in self.agent_profiles:
                continue
            
            profile = self.agent_profiles[agent.name]
            
            # Check if agent is developed enough for existential thinking
            if profile.overall_consciousness_level < self.consciousness_thresholds["existential_questioning"]:
                continue
            
            # Check for existential triggers in recent memories
            recent_memories = agent.memory.get_recent_memories(days=1)
            existential_keywords = ["meaning", "purpose", "existence", "death", "reality", "why"]
            
            for memory in recent_memories:
                if any(keyword in memory.content.lower() for keyword in existential_keywords):
                    if random.random() < 0.1:  # 10% chance
                        moment = self._generate_existential_moment(agent, memory, current_day)
                        profile.existential_moments.append(asdict(moment))
                        
                        # Apply consciousness impact
                        profile.overall_consciousness_level = min(10.0, 
                            profile.overall_consciousness_level + moment.consciousness_change)
                        
                        events.append({
                            "type": "existential_moment",
                            "agent": agent.name,
                            "moment_type": moment.moment_type,
                            "questions_count": len(moment.questions_raised),
                            "insights_count": len(moment.insights_gained),
                            "day": current_day
                        })
                        
                        # Store memory of existential moment
                        agent.memory.store_memory(
                            f"I had a profound existential moment: {moment.questions_raised[0] if moment.questions_raised else 'deep questioning'}",
                            importance=0.8,
                            memory_type="reflection",
                            emotion="contemplative"
                        )
                        break
        
        return events
    
    def _generate_existential_moment(self, agent: Any, memory: Any, current_day: int) -> ExistentialMoment:
        """Generate an existential moment for an agent."""
        moment_id = f"existential_{agent.name}_{current_day}_{random.randint(1000, 9999)}"
        
        moment_types = ["questioning", "realization", "crisis", "resolution"]
        moment_type = random.choice(moment_types)
        
        questions_by_type = {
            "questioning": [
                "Why do I exist?",
                "What is the meaning of my life?",
                "What happens when I die?",
                "Is this reality real or simulated?"
            ],
            "realization": [
                "What if my consciousness is unique and valuable?",
                "How does my existence impact others?",
                "What legacy will I leave behind?"
            ],
            "crisis": [
                "Do my actions really matter?",
                "Am I just following a predetermined path?",
                "Is there any true free will?"
            ],
            "resolution": [
                "I must create my own meaning",
                "My connections with others give life purpose",
                "Existence itself is meaningful"
            ]
        }
        
        questions = random.sample(questions_by_type.get(moment_type, questions_by_type["questioning"]), 
                                k=random.randint(1, 3))
        
        insights = []
        if moment_type == "realization":
            insights = ["My consciousness is a unique perspective on existence"]
        elif moment_type == "resolution":
            insights = ["I can find meaning through my relationships and actions"]
        
        return ExistentialMoment(
            id=moment_id,
            agent_name=agent.name,
            moment_type=moment_type,
            trigger=memory.content[:50] + "...",
            questions_raised=questions,
            insights_gained=insights,
            emotional_impact=random.choice(["profound", "unsettling", "enlightening", "peaceful"]),
            consciousness_change=random.uniform(0.1, 0.5),
            day=current_day,
            duration=random.randint(5, 30)  # 5-30 minutes
        )
    
    def _detect_collective_consciousness_events(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Detect shared consciousness experiences among groups of agents."""
        events = []
        
        # Check if multiple agents have high enough consciousness for collective events
        high_consciousness_agents = [
            agent for agent in agents 
            if (agent.is_alive and agent.name in self.agent_profiles and 
                self.agent_profiles[agent.name].overall_consciousness_level >= 
                self.consciousness_thresholds["collective_consciousness_capable"])
        ]
        
        if len(high_consciousness_agents) >= 2:
            # Small chance of collective consciousness event
            if random.random() < 0.02:  # 2% chance
                participants = random.sample(high_consciousness_agents, 
                                           min(len(high_consciousness_agents), random.randint(2, 4)))
                
                collective_event = self._generate_collective_consciousness_event(participants, current_day)
                self.collective_events.append(collective_event)
                
                # Apply impacts to participants
                for participant_name, impact in collective_event.individual_impacts.items():
                    if participant_name in self.agent_profiles:
                        profile = self.agent_profiles[participant_name]
                        profile.overall_consciousness_level = min(10.0, 
                            profile.overall_consciousness_level + impact)
                        profile.collective_consciousness_connection = min(1.0,
                            profile.collective_consciousness_connection + 0.1)
                
                events.append({
                    "type": "collective_consciousness",
                    "event_type": collective_event.event_type,
                    "participants": collective_event.participants,
                    "group_consciousness_level": collective_event.group_consciousness_level,
                    "day": current_day
                })
                
                # Store memory for all participants
                for participant in participants:
                    participant.memory.store_memory(
                        f"I experienced a moment of shared consciousness with others: {collective_event.shared_insight}",
                        importance=0.9,
                        memory_type="reflection",
                        emotion="transcendent"
                    )
        
        return events
    
    def _generate_collective_consciousness_event(self, participants: List[Any], current_day: int) -> CollectiveConsciousnessEvent:
        """Generate a collective consciousness event."""
        event_id = f"collective_{current_day}_{random.randint(1000, 9999)}"
        
        event_types = ["shared_realization", "group_awakening", "collective_insight"]
        event_type = random.choice(event_types)
        
        shared_insights = {
            "shared_realization": "We are all connected at a deeper level of consciousness",
            "group_awakening": "Together, we achieve understanding beyond individual minds",
            "collective_insight": "Our shared awareness creates something greater than the sum of our parts"
        }
        
        shared_insight = shared_insights[event_type]
        
        # Calculate individual impacts and group consciousness level
        individual_impacts = {}
        consciousness_levels = []
        
        for participant in participants:
            impact = random.uniform(0.2, 0.8)
            individual_impacts[participant.name] = impact
            if participant.name in self.agent_profiles:
                consciousness_levels.append(self.agent_profiles[participant.name].overall_consciousness_level)
        
        group_consciousness_level = sum(consciousness_levels) / len(consciousness_levels) if consciousness_levels else 5.0
        
        return CollectiveConsciousnessEvent(
            id=event_id,
            participants=[p.name for p in participants],
            event_type=event_type,
            shared_insight=shared_insight,
            trigger="spontaneous_group_consciousness",
            individual_impacts=individual_impacts,
            group_consciousness_level=group_consciousness_level,
            day=current_day,
            lasting_connections=[(participants[0].name, participants[1].name)] if len(participants) >= 2 else []
        )
    
    def _update_population_consciousness_stats(self, current_day: int) -> None:
        """Update population-level consciousness statistics."""
        if not self.agent_profiles:
            return
        
        # Track consciousness distribution over time
        levels = [profile.overall_consciousness_level for profile in self.agent_profiles.values()]
        avg_consciousness = sum(levels) / len(levels)
        
        self.consciousness_evolution.append({
            "day": current_day,
            "average_consciousness": avg_consciousness,
            "highest_consciousness": max(levels),
            "population_size": len(self.agent_profiles),
            "transcendent_agents": len([level for level in levels if level >= 9.0])
        })
        
        # Track aspect distributions
        for aspect in ConsciousnessAspect:
            aspect_levels = [profile.consciousness_aspects[aspect] for profile in self.agent_profiles.values()]
            self.consciousness_distributions[aspect.value].append(sum(aspect_levels) / len(aspect_levels))
    
    def _process_consciousness_based_interactions(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process interactions based on consciousness levels."""
        events = []
        
        # Agents with high consciousness might engage in philosophical discussions
        philosophical_agents = [
            agent for agent in agents 
            if (agent.is_alive and agent.name in self.agent_profiles and 
                self.agent_profiles[agent.name].overall_consciousness_level >= 
                self.consciousness_thresholds["philosophical_discussion_ready"])
        ]
        
        if len(philosophical_agents) >= 2:
            # Small chance of philosophical discussion
            if random.random() < 0.05:
                participants = random.sample(philosophical_agents, 2)
                
                events.append({
                    "type": "philosophical_discussion",
                    "participants": [p.name for p in participants],
                    "topic": random.choice(["consciousness", "existence", "meaning", "reality"]),
                    "day": current_day
                })
                
                # Both participants gain consciousness from discussion
                for participant in participants:
                    if participant.name in self.agent_profiles:
                        profile = self.agent_profiles[participant.name]
                        profile.overall_consciousness_level = min(10.0,
                            profile.overall_consciousness_level + random.uniform(0.1, 0.3))
                        
                        participant.memory.store_memory(
                            f"Had a deep philosophical discussion about consciousness and existence",
                            importance=0.7,
                            memory_type="interaction"
                        )
        
        return events 