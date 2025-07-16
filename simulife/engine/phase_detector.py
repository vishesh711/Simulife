"""
Phase Detection and Milestone Tracking System for SimuLife Civilization Development

This module implements the core phase detection system that automatically identifies
civilization development milestones and manages transitions between development phases.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
import json
import logging

@dataclass
class Milestone:
    """Represents a significant achievement in civilization development"""
    name: str
    phase: str
    achieved_at: int
    participants: List[str]  # Agent IDs involved
    description: str
    significance_score: float
    prerequisites: List[str]  # Previous milestones required
    details: Dict[str, Any] = None

@dataclass
class PhaseState:
    """Represents the current state of a civilization phase"""
    name: str
    start_time: int
    population_at_start: int
    key_milestones: List[Milestone]
    dominant_behaviors: List[str]
    social_complexity_score: float
    technological_level: int
    cultural_developments: List[str]

@dataclass
class PhaseTransition:
    """Represents a transition between civilization phases"""
    from_phase: str
    to_phase: str
    transition_time: int
    trigger_milestones: List[Milestone]
    population_at_transition: int
    confidence: float
    transition_events: List[str]

class CivilizationMetrics:
    """Calculates and tracks civilization development metrics"""
    
    def __init__(self):
        self.population_growth_rate = 0.0
        self.cooperation_index = 0.0
        self.conflict_frequency = 0.0
        self.knowledge_accumulation_rate = 0.0
        self.social_complexity_score = 0.0
        self.cultural_diversity_index = 0.0
        self.technological_advancement_rate = 0.0
        self.communication_success_rate = 0.0
        self.relationship_formation_rate = 0.0
        
    def calculate_metrics(self, world_state, agents, recent_events):
        """Calculate current civilization health metrics"""
        
        if not agents:
            return self
            
        # Population metrics
        self.population_growth_rate = self._calc_population_growth(world_state)
        
        # Social metrics
        self.cooperation_index = self._calc_cooperation_level(recent_events)
        self.conflict_frequency = self._calc_conflict_rate(recent_events)
        self.communication_success_rate = self._calc_communication_success(recent_events)
        
        # Relationship metrics
        self.relationship_formation_rate = self._calc_relationship_formation(agents)
        
        # Knowledge metrics
        self.knowledge_accumulation_rate = self._calc_knowledge_growth(agents)
        
        # Complexity metrics
        self.social_complexity_score = self._calc_social_complexity(agents)
        
        return self
    
    def _calc_population_growth(self, world_state):
        """Calculate population growth rate"""
        if hasattr(world_state, 'population_history') and len(world_state.population_history) > 1:
            recent_pop = world_state.population_history[-5:]  # Last 5 time periods
            if len(recent_pop) >= 2:
                return (recent_pop[-1] - recent_pop[0]) / len(recent_pop)
        return 0.0
    
    def _calc_cooperation_level(self, recent_events):
        """Calculate cooperation index from recent events"""
        if not recent_events:
            return 0.0
            
        cooperation_events = [e for e in recent_events if 
                             getattr(e, 'event_type', '') in ['cooperation', 'help', 'sharing', 'group_action']]
        return len(cooperation_events) / len(recent_events) if recent_events else 0.0
    
    def _calc_conflict_rate(self, recent_events):
        """Calculate conflict frequency"""
        if not recent_events:
            return 0.0
            
        conflict_events = [e for e in recent_events if 
                          getattr(e, 'event_type', '') in ['conflict', 'fight', 'competition', 'disagreement']]
        return len(conflict_events) / len(recent_events) if recent_events else 0.0
    
    def _calc_communication_success(self, recent_events):
        """Calculate communication success rate"""
        comm_events = [e for e in recent_events if getattr(e, 'event_type', '') == 'communication']
        if not comm_events:
            return 0.0
            
        successful_comms = [e for e in comm_events if getattr(e, 'success', False)]
        return len(successful_comms) / len(comm_events)
    
    def _calc_relationship_formation(self, agents):
        """Calculate rate of new relationship formation"""
        total_relationships = 0
        for agent in agents:
            if hasattr(agent, 'relationships'):
                total_relationships += len(agent.relationships)
        
        return total_relationships / len(agents) if agents else 0.0
    
    def _calc_knowledge_growth(self, agents):
        """Calculate knowledge accumulation rate"""
        total_knowledge = 0
        for agent in agents:
            if hasattr(agent, 'knowledge_base'):
                total_knowledge += len(agent.knowledge_base)
            elif hasattr(agent, 'memory_manager') and hasattr(agent.memory_manager, 'memories'):
                total_knowledge += len(agent.memory_manager.memories)
        
        return total_knowledge / len(agents) if agents else 0.0
    
    def _calc_social_complexity(self, agents):
        """Calculate overall social complexity score"""
        if not agents:
            return 0.0
            
        complexity_factors = []
        
        # Relationship complexity
        avg_relationships = sum(len(getattr(agent, 'relationships', [])) for agent in agents) / len(agents)
        complexity_factors.append(min(avg_relationships / 3.0, 1.0))  # Normalize to 0-1
        
        # Emotional complexity
        avg_emotions = 0
        for agent in agents:
            if hasattr(agent, 'emotional_profile'):
                # Count number of emotions above threshold (handle nested structure)
                emotions_active = 0
                if isinstance(agent.emotional_profile, dict):
                    # Handle Phase 10 nested structure (primary_emotions, complex_emotions)
                    if 'primary_emotions' in agent.emotional_profile:
                        emotions_active += sum(1 for emotion_val in agent.emotional_profile['primary_emotions'].values() 
                                             if emotion_val > 0.3)
                    if 'complex_emotions' in agent.emotional_profile:
                        emotions_active += sum(1 for emotion_val in agent.emotional_profile['complex_emotions'].values() 
                                             if emotion_val > 0.3)
                    # Handle flat structure (backward compatibility)
                    if 'primary_emotions' not in agent.emotional_profile:
                        emotions_active = sum(1 for emotion_val in agent.emotional_profile.values() 
                                            if isinstance(emotion_val, (int, float)) and emotion_val > 0.3)
                avg_emotions += emotions_active
        
        if agents:
            avg_emotions /= len(agents)
            complexity_factors.append(min(avg_emotions / 8.0, 1.0))  # Normalize to 0-1
        
        # Communication complexity
        complexity_factors.append(self.communication_success_rate)
        
        return sum(complexity_factors) / len(complexity_factors) if complexity_factors else 0.0

class MilestoneTracker:
    """Tracks and detects civilization development milestones"""
    
    def __init__(self):
        self.completed_milestones = []
        self.milestone_detectors = {
            # Genesis Phase Milestones
            "first_tool_creation": self._detect_first_tool,
            "first_successful_communication": self._detect_communication,
            "first_emotional_response": self._detect_emotional_response,
            "first_memory_formation": self._detect_memory_formation,
            "first_self_awareness": self._detect_self_awareness,
            
            # Individual Mastery Phase Milestones
            "skill_specialization": self._detect_skill_specialization,
            "complex_tool_creation": self._detect_complex_tools,
            "territory_establishment": self._detect_territory,
            "personality_expression": self._detect_personality,
            
            # Pair Bonding Phase Milestones
            "first_stable_partnership": self._detect_partnership,
            "first_resource_sharing": self._detect_resource_sharing,
            "first_protective_behavior": self._detect_protection,
            "first_romantic_attraction": self._detect_romance,
            
            # Family Formation Phase Milestones
            "first_family_formation": self._detect_family,
            "first_child_teaching": self._detect_teaching,
            "multi_generation_family": self._detect_multi_generation,
            
            # Tribal Formation Phase Milestones
            "first_group_leadership": self._detect_group_leadership,
            "first_group_cooperation": self._detect_group_cooperation,
            "first_group_identity": self._detect_group_identity,
            
            # Inter-Tribal Contact Phase Milestones
            "first_peaceful_contact": self._detect_peaceful_contact,
            "first_trade_exchange": self._detect_trade_exchange,
            "first_inter_tribal_alliance": self._detect_inter_tribal_alliance,
            "first_cultural_adoption": self._detect_cultural_adoption,
            "first_diplomatic_negotiation": self._detect_diplomatic_negotiation,
            "first_conflict_resolution": self._detect_conflict_resolution,
        }
        
    def check_milestones(self, world_state, agents, recent_events):
        """Check for new milestone achievements"""
        new_milestones = []
        
        for milestone_name, detector_func in self.milestone_detectors.items():
            if milestone_name not in [m.name for m in self.completed_milestones]:
                try:
                    detection_result = detector_func(world_state, agents, recent_events)
                    if detection_result:
                        milestone = Milestone(
                            name=milestone_name,
                            phase=self._get_milestone_phase(milestone_name),
                            achieved_at=world_state.day if hasattr(world_state, 'day') else 0,
                            participants=detection_result.get('participants', []),
                            description=self._generate_milestone_description(milestone_name, detection_result),
                            significance_score=self._calculate_significance(milestone_name),
                            prerequisites=self._get_prerequisites(milestone_name),
                            details=detection_result
                        )
                        new_milestones.append(milestone)
                        self.completed_milestones.append(milestone)
                        logging.info(f"🎉 MILESTONE ACHIEVED: {milestone_name} - {milestone.description}")
                except Exception as e:
                    logging.warning(f"Error detecting milestone {milestone_name}: {e}")
        
        return new_milestones
    
    def _detect_first_tool(self, world_state, agents, recent_events):
        """Detect first tool creation event"""
        # Check agent memories for tool creation/use
        for agent in agents:
            if hasattr(agent, 'memory') and hasattr(agent.memory, 'memories'):
                for memory in agent.memory.memories:
                    content = memory.content.lower()
                    if any(word in content for word in ['tool', 'weapon', 'instrument', 'crafted', 'made', 'built']):
                        return {'participants': [agent.name], 'tool_type': 'memory_evidence', 'evidence': memory.content[:100]}
            
            # Check agent skills for tool-making abilities
            if hasattr(agent, 'skills'):
                tool_skills = [skill for skill in agent.skills.keys() 
                              if any(word in skill.lower() for word in ['craft', 'tool', 'build', 'create'])]
                if tool_skills and max(agent.skills[skill] for skill in tool_skills) > 0.3:
                    return {'participants': [agent.name], 'tool_type': 'skill_based', 'skills': tool_skills}
                
        # Check events for tool creation
        for event in recent_events:
            if hasattr(event, 'event_type') and 'tool' in str(event.event_type).lower():
                return {'participants': getattr(event, 'agent_ids', []), 'tool_type': 'event_created'}
            
            # Check event descriptions for tool-related activities
            if hasattr(event, 'description'):
                desc = event.description.lower()
                if any(word in desc for word in ['tool', 'crafted', 'built', 'made', 'weapon']):
                    return {'participants': getattr(event, 'participants', []), 'tool_type': 'event_description'}
        
        return None
    
    def _detect_communication(self, world_state, agents, recent_events):
        """Detect first successful communication between agents"""
        for event in recent_events:
            if (hasattr(event, 'event_type') and 
                event.event_type == 'communication' and
                getattr(event, 'success', False) and
                len(getattr(event, 'participants', [])) >= 2):
                return {
                    'participants': event.participants,
                    'communication_type': getattr(event, 'communication_type', 'unknown')
                }
        
        # Check agent memories for communication
        for agent in agents:
            if hasattr(agent, 'memory') and hasattr(agent.memory, 'memories'):
                for memory in agent.memory.memories[-10:]:  # Check recent memories
                    content = memory.content.lower()
                    if any(word in content for word in ['communicated', 'talked', 'spoke', 'said', 'conversation', 'discussed']):
                        return {'participants': [agent.name], 'memory_based': True, 'evidence': memory.content[:100]}
        
        return None
    
    def _detect_emotional_response(self, world_state, agents, recent_events):
        """Detect first strong emotional response"""
        for agent in agents:
            if hasattr(agent, 'emotional_profile'):
                # Check for any strong emotion (>0.7) - handle nested structure
                if isinstance(agent.emotional_profile, dict):
                    # Check primary emotions
                    if 'primary_emotions' in agent.emotional_profile:
                        for emotion, value in agent.emotional_profile['primary_emotions'].items():
                            if value > 0.7:
                                return {
                                    'participants': [agent.name],
                                    'emotion': emotion,
                                    'intensity': value
                                }
                    # Check complex emotions
                    if 'complex_emotions' in agent.emotional_profile:
                        for emotion, value in agent.emotional_profile['complex_emotions'].items():
                            if value > 0.7:
                                return {
                                    'participants': [agent.name],
                                    'emotion': emotion,
                                    'intensity': value
                                }
                    # Handle flat structure (backward compatibility)
                    if 'primary_emotions' not in agent.emotional_profile:
                        for emotion, value in agent.emotional_profile.items():
                            if isinstance(value, (int, float)) and value > 0.7:
                                return {
                                    'participants': [agent.name],
                                    'emotion': emotion,
                                    'intensity': value
                                }
        
        return None
    
    def _detect_memory_formation(self, world_state, agents, recent_events):
        """Detect formation of significant memories"""
        for agent in agents:
            if hasattr(agent, 'memory') and hasattr(agent.memory, 'memories') and len(agent.memory.memories) > 0:
                return {
                    'participants': [agent.name],
                    'memory_count': len(agent.memory.memories),
                    'recent_memory': agent.memory.memories[-1].content[:100] if agent.memory.memories else None
                }
        
        return None
    
    def _detect_self_awareness(self, world_state, agents, recent_events):
        """Detect self-awareness through agent behavior or memories"""
        for agent in agents:
            # Check memories for self-referential statements
            if hasattr(agent, 'memory') and hasattr(agent.memory, 'memories'):
                for memory in agent.memory.memories:
                    content = memory.content.lower()
                    if any(phrase in content for phrase in ['i am', 'myself', 'i think', 'i feel', 'i exist', 'i want', 'i believe', 'my goal']):
                        return {
                            'participants': [agent.name],
                            'awareness_type': 'memory_based',
                            'evidence': memory.content[:100]
                        }
            
            # Check if agent has personal goals (indicates self-awareness)
            if hasattr(agent, 'current_goal') and agent.current_goal:
                return {
                    'participants': [agent.name],
                    'awareness_type': 'goal_based',
                    'evidence': f'Personal goal: {agent.current_goal}'
                }
            
            # Check if agent has defined personality (indicates self-identity)
            if hasattr(agent, 'traits') and len(agent.traits) > 0:
                return {
                    'participants': [agent.name],
                    'awareness_type': 'personality_based', 
                    'evidence': f'Distinct traits: {agent.traits}'
                }
        
        return None
    
    def _detect_partnership(self, world_state, agents, recent_events):
        """Detect first stable partnership formation"""
        for agent in agents:
            if hasattr(agent, 'relationships'):
                for partner_id, relationship in agent.relationships.items():
                    if (hasattr(relationship, 'strength') and relationship.strength > 0.8 and
                        hasattr(relationship, 'duration') and relationship.duration > 50):
                        return {
                            'participants': [agent.name, partner_id],
                            'relationship_strength': relationship.strength,
                            'duration': relationship.duration
                        }
        
        return None
    
    def _detect_romance(self, world_state, agents, recent_events):
        """Detect first romantic attraction"""
        for agent in agents:
            if hasattr(agent, 'romantic_life') and hasattr(agent.romantic_life, 'relationship_status'):
                if agent.romantic_life.relationship_status != 'single':
                    return {
                        'participants': [agent.name],
                        'relationship_status': agent.romantic_life.relationship_status,
                        'partner': getattr(agent.romantic_life, 'current_partner', None)
                    }
        
        return None
    
    def _detect_skill_specialization(self, world_state, agents, recent_events):
        """Detect when an agent develops specialized skills"""
        for agent in agents:
            if hasattr(agent, 'skills'):
                high_skills = [skill for skill, level in agent.skills.items() if level > 0.7]
                if len(high_skills) > 0:
                    return {
                        'participants': [agent.name],
                        'specialized_skills': high_skills
                    }
        
        return None
    
    def _detect_complex_tools(self, world_state, agents, recent_events):
        """Detect creation of complex/advanced tools"""
        # This would detect multi-component tools or advanced techniques
        return None  # Placeholder for future implementation
    
    def _detect_territory(self, world_state, agents, recent_events):
        """Detect establishment of personal territory"""
        # This would detect when agents establish and defend territories
        return None  # Placeholder for future implementation
    
    def _detect_personality(self, world_state, agents, recent_events):
        """Detect strong personality expression"""
        for agent in agents:
            if hasattr(agent, 'personality'):
                # Check for extreme personality traits
                extreme_traits = {trait: value for trait, value in agent.personality.items() 
                                if value > 0.8 or value < 0.2}
                if len(extreme_traits) > 0:
                    return {
                        'participants': [agent.name],
                        'personality_traits': extreme_traits
                    }
        
        return None
    
    def _detect_resource_sharing(self, world_state, agents, recent_events):
        """Detect first altruistic resource sharing"""
        # Check for events where agents give without immediate benefit
        return None  # Placeholder for future implementation
    
    def _detect_protection(self, world_state, agents, recent_events):
        """Detect protective behavior toward others"""
        # Check for events where agents defend others at personal cost
        return None  # Placeholder for future implementation
    
    def _detect_family(self, world_state, agents, recent_events):
        """Detect first family unit formation"""
        # Check for multi-agent family groups
        return None  # Placeholder for future implementation
    
    def _detect_teaching(self, world_state, agents, recent_events):
        """Detect first teaching/learning events"""
        # Check for knowledge transfer between agents
        return None  # Placeholder for future implementation
    
    def _detect_multi_generation(self, world_state, agents, recent_events):
        """Detect multi-generational family structures"""
        # Check for grandparent-parent-child relationships
        for agent in agents:
            if hasattr(agent, 'family') and agent.family:
                # Look for agents with children who also have children
                if 'children' in agent.family and agent.family['children']:
                    for child_name in agent.family['children']:
                        child_agent = next((a for a in agents if a.name == child_name), None)
                        if (child_agent and hasattr(child_agent, 'family') and 
                            child_agent.family and 'children' in child_agent.family and 
                            child_agent.family['children']):
                            return {
                                'participants': [agent.name, child_name],
                                'generation_depth': 3,
                                'family_line': f'{agent.name} -> {child_name} -> {child_agent.family["children"][0]}'
                            }
        return None
    
    # TRIBAL FORMATION PHASE MILESTONE DETECTORS
    
    def _detect_group_leadership(self, world_state, agents, recent_events):
        """Detect emergence of group leadership"""
        # Check for agents with high influence/reputation
        leaders = []
        for agent in agents:
            if hasattr(agent, 'reputation') and agent.reputation > 0.7:
                leaders.append(agent.name)
            
            # Check if agent has leadership traits
            if hasattr(agent, 'traits') and any(trait in ['ambitious', 'charismatic', 'leader'] for trait in agent.traits):
                if hasattr(agent, 'relationships') and len(agent.relationships) >= 3:
                    leaders.append(agent.name)
        
        # Check for leadership roles in groups
        if hasattr(world_state, 'factions') and world_state.factions:
            for faction in world_state.factions:
                if hasattr(faction, 'leader') and faction.leader:
                    return {
                        'participants': [faction.leader],
                        'leadership_type': 'faction_leader',
                        'group': getattr(faction, 'name', 'Unknown'),
                        'followers': getattr(faction, 'members', [])
                    }
        
        # Check recent events for leadership activities
        for event in recent_events:
            if hasattr(event, 'description') and any(word in event.description.lower() 
                for word in ['led', 'leader', 'command', 'organize', 'direct']):
                return {
                    'participants': getattr(event, 'participants', []),
                    'leadership_type': 'event_based',
                    'evidence': event.description[:100]
                }
        
        if leaders:
            return {
                'participants': leaders[:1],  # First leader found
                'leadership_type': 'reputation_based',
                'influence_level': 'high'
            }
        
        return None
    
    def _detect_group_cooperation(self, world_state, agents, recent_events):
        """Detect first group cooperation activities"""
        # Check recent events for group activities
        cooperation_events = []
        for event in recent_events:
            if hasattr(event, 'participants') and len(getattr(event, 'participants', [])) >= 3:
                if hasattr(event, 'description'):
                    desc = event.description.lower()
                    if any(word in desc for word in ['together', 'group', 'team', 'collective', 'united', 'cooperation']):
                        cooperation_events.append(event)
        
        if cooperation_events:
            event = cooperation_events[0]
            return {
                'participants': event.participants,
                'cooperation_type': 'event_based',
                'activity': event.description[:100],
                'group_size': len(event.participants)
            }
        
        # Check for multiple agents working on similar goals
        goal_groups = {}
        for agent in agents:
            if hasattr(agent, 'current_goal') and agent.current_goal:
                goal = agent.current_goal.lower()
                if goal not in goal_groups:
                    goal_groups[goal] = []
                goal_groups[goal].append(agent.name)
        
        # Find groups with shared goals
        for goal, members in goal_groups.items():
            if len(members) >= 3:
                return {
                    'participants': members,
                    'cooperation_type': 'shared_goals',
                    'common_goal': goal,
                    'group_size': len(members)
                }
        
        return None
    
    def _detect_group_identity(self, world_state, agents, recent_events):
        """Detect formation of group identity and names"""
        # Check for named factions/groups
        if hasattr(world_state, 'factions') and world_state.factions:
            for faction in world_state.factions:
                if hasattr(faction, 'name') and hasattr(faction, 'members') and len(faction.members) >= 2:
                    return {
                        'participants': faction.members,
                        'group_name': faction.name,
                        'identity_type': 'faction_based',
                        'group_size': len(faction.members),
                        'ideology': getattr(faction, 'ideology', 'Unknown')
                    }
        
        # Check for belief systems (indicate group identity)
        if hasattr(world_state, 'beliefs') and world_state.beliefs:
            for belief in world_state.beliefs:
                if hasattr(belief, 'believers') and len(belief.believers) >= 3:
                    return {
                        'participants': belief.believers,
                        'group_name': getattr(belief, 'belief_name', 'Shared Belief'),
                        'identity_type': 'belief_based',
                        'group_size': len(belief.believers)
                    }
        
        # Check for agents with strong shared traits forming groups
        trait_groups = {}
        for agent in agents:
            if hasattr(agent, 'traits'):
                for trait in agent.traits:
                    if trait not in trait_groups:
                        trait_groups[trait] = []
                    trait_groups[trait].append(agent.name)
        
        for trait, members in trait_groups.items():
            if len(members) >= 3:
                return {
                    'participants': members[:3],  # First 3 members
                    'group_name': f'{trait.title()} Group',
                    'identity_type': 'trait_based',
                    'shared_trait': trait
                }
        
        return None
    
    # INTER-TRIBAL CONTACT PHASE MILESTONE DETECTORS
    
    def _detect_peaceful_contact(self, world_state, agents, recent_events):
        """Detect first peaceful contact between different tribes/groups"""
        # Check for diplomatic events in recent events
        for event in recent_events:
            if hasattr(event, 'description'):
                desc = event.description.lower()
                if any(word in desc for word in ['diplomatic', 'peaceful', 'meeting', 'contact', 'encounter', 'ambassador']):
                    if hasattr(event, 'participants') and len(getattr(event, 'participants', [])) >= 2:
                        return {
                            'participants': event.participants,
                            'contact_type': 'diplomatic_event',
                            'evidence': event.description[:100]
                        }
        
        # Check for inter-faction relationships
        if hasattr(world_state, 'factions') and len(world_state.factions) >= 2:
            factions = world_state.factions
            for i, faction1 in enumerate(factions):
                for j, faction2 in enumerate(factions[i+1:], i+1):
                    # Check if members of different factions have positive relationships
                    faction1_members = getattr(faction1, 'members', [])
                    faction2_members = getattr(faction2, 'members', [])
                    
                    for member1_name in faction1_members:
                        member1 = next((a for a in agents if a.name == member1_name), None)
                        if member1 and hasattr(member1, 'relationships'):
                            for member2_name in faction2_members:
                                if member2_name in member1.relationships:
                                    relationship = member1.relationships[member2_name]
                                    if (hasattr(relationship, 'type') and 
                                        relationship.type in ['friend', 'ally', 'partner']):
                                        return {
                                            'participants': [member1_name, member2_name],
                                            'contact_type': 'inter_faction_friendship',
                                            'faction1': getattr(faction1, 'name', 'Unknown'),
                                            'faction2': getattr(faction2, 'name', 'Unknown')
                                        }
        
        return None
    
    def _detect_trade_exchange(self, world_state, agents, recent_events):
        """Detect first trade exchange between groups"""
        # Check recent events for trade activities
        for event in recent_events:
            if hasattr(event, 'description'):
                desc = event.description.lower()
                if any(word in desc for word in ['trade', 'exchange', 'barter', 'commerce', 'goods', 'merchant']):
                    if hasattr(event, 'participants') and len(getattr(event, 'participants', [])) >= 2:
                        return {
                            'participants': event.participants,
                            'trade_type': 'event_based',
                            'evidence': event.description[:100]
                        }
        
        # Check for resource-based interactions between agents
        for agent in agents:
            if hasattr(agent, 'memory') and hasattr(agent.memory, 'memories'):
                for memory in agent.memory.memories[-10:]:  # Recent memories
                    content = memory.content.lower()
                    if any(word in content for word in ['gave', 'traded', 'exchanged', 'shared resources', 'offered']):
                        return {
                            'participants': [agent.name],
                            'trade_type': 'memory_evidence',
                            'evidence': memory.content[:100]
                        }
        
        # Check economic emergence system results
        for event in recent_events:
            if (hasattr(event, 'event_type') and 
                getattr(event, 'event_type', '') in ['economic', 'trade', 'market']):
                return {
                    'participants': getattr(event, 'participants', []),
                    'trade_type': 'economic_system',
                    'activity': str(event)[:100]
                }
        
        return None
    
    def _detect_inter_tribal_alliance(self, world_state, agents, recent_events):
        """Detect formation of alliances between different groups"""
        # Check for formal alliances in world state
        if hasattr(world_state, 'alliances') and world_state.alliances:
            for alliance in world_state.alliances:
                if hasattr(alliance, 'members') and len(alliance.members) >= 2:
                    return {
                        'participants': alliance.members,
                        'alliance_type': 'formal_alliance',
                        'alliance_name': getattr(alliance, 'name', 'Unknown Alliance'),
                        'purpose': getattr(alliance, 'purpose', 'Unknown')
                    }
        
        # Check for cooperative events between different factions
        if hasattr(world_state, 'factions') and len(world_state.factions) >= 2:
            for event in recent_events:
                if hasattr(event, 'participants') and len(getattr(event, 'participants', [])) >= 2:
                    # Check if participants are from different factions
                    faction_representation = {}
                    for participant in event.participants:
                        for faction in world_state.factions:
                            if participant in getattr(faction, 'members', []):
                                faction_name = getattr(faction, 'name', 'Unknown')
                                if faction_name not in faction_representation:
                                    faction_representation[faction_name] = []
                                faction_representation[faction_name].append(participant)
                    
                    if len(faction_representation) >= 2:  # Multi-faction event
                        if hasattr(event, 'description'):
                            desc = event.description.lower()
                            if any(word in desc for word in ['alliance', 'treaty', 'agreement', 'pact', 'united']):
                                return {
                                    'participants': event.participants,
                                    'alliance_type': 'multi_faction_cooperation',
                                    'factions_involved': list(faction_representation.keys()),
                                    'evidence': event.description[:100]
                                }
        
        return None
    
    def _detect_cultural_adoption(self, world_state, agents, recent_events):
        """Detect adoption of another group's customs or practices"""
        # Check for cultural transmission events
        for event in recent_events:
            if hasattr(event, 'description'):
                desc = event.description.lower()
                if any(word in desc for word in ['learned', 'adopted', 'copied', 'cultural', 'custom', 'tradition', 'practice']):
                    if hasattr(event, 'participants') and len(getattr(event, 'participants', [])) >= 2:
                        return {
                            'participants': event.participants,
                            'adoption_type': 'cultural_transmission',
                            'evidence': event.description[:100]
                        }
        
        # Check agent memories for learning about other cultures
        for agent in agents:
            if hasattr(agent, 'memory') and hasattr(agent.memory, 'memories'):
                for memory in agent.memory.memories[-10:]:
                    content = memory.content.lower()
                    if any(phrase in content for phrase in ['learned from', 'observed their', 'adopted their', 'cultural practice', 'different way']):
                        return {
                            'participants': [agent.name],
                            'adoption_type': 'individual_learning',
                            'evidence': memory.content[:100]
                        }
        
        # Check for belief system changes (cultural adoption)
        if hasattr(world_state, 'beliefs') and world_state.beliefs:
            for belief in world_state.beliefs:
                if hasattr(belief, 'believers') and len(belief.believers) >= 2:
                    # If belief has grown recently, it might indicate cultural adoption
                    return {
                        'participants': belief.believers[:2],
                        'adoption_type': 'belief_spreading',
                        'cultural_element': getattr(belief, 'belief_name', 'Unknown Belief')
                    }
        
        return None
    
    def _detect_diplomatic_negotiation(self, world_state, agents, recent_events):
        """Detect first formal diplomatic negotiations"""
        # Check for diplomatic events
        for event in recent_events:
            if hasattr(event, 'description'):
                desc = event.description.lower()
                if any(word in desc for word in ['negotiation', 'diplomacy', 'ambassador', 'treaty', 'talks', 'summit']):
                    return {
                        'participants': getattr(event, 'participants', []),
                        'negotiation_type': 'formal_diplomacy',
                        'evidence': event.description[:100]
                    }
        
        # Check for peaceful resolution activities
        for event in recent_events:
            if hasattr(event, 'event_type') and getattr(event, 'event_type', '') == 'diplomacy':
                return {
                    'participants': getattr(event, 'participants', []),
                    'negotiation_type': 'diplomatic_system',
                    'activity': str(event)[:100]
                }
        
        return None
    
    def _detect_conflict_resolution(self, world_state, agents, recent_events):
        """Detect peaceful resolution of conflicts between groups"""
        # Check for conflict resolution events
        for event in recent_events:
            if hasattr(event, 'description'):
                desc = event.description.lower()
                if any(phrase in desc for phrase in ['resolved conflict', 'peace agreement', 'conflict ended', 'reconciliation', 'mediation']):
                    return {
                        'participants': getattr(event, 'participants', []),
                        'resolution_type': 'peaceful_resolution',
                        'evidence': event.description[:100]
                    }
        
        # Check crisis response system for conflict resolution
        for event in recent_events:
            if (hasattr(event, 'event_type') and 
                getattr(event, 'event_type', '') in ['crisis_response', 'conflict_resolution']):
                return {
                    'participants': getattr(event, 'participants', []),
                    'resolution_type': 'crisis_system',
                    'activity': str(event)[:100]
                }
        
        return None
    
    def _get_milestone_phase(self, milestone_name):
        """Get the phase that a milestone belongs to"""
        phase_mapping = {
            "first_tool_creation": "Genesis",
            "first_successful_communication": "Genesis", 
            "first_emotional_response": "Genesis",
            "first_memory_formation": "Genesis",
            "first_self_awareness": "Genesis",
            "skill_specialization": "Individual Mastery",
            "complex_tool_creation": "Individual Mastery",
            "territory_establishment": "Individual Mastery",
            "personality_expression": "Individual Mastery",
            "first_stable_partnership": "Pair Bonding",
            "first_resource_sharing": "Pair Bonding",
            "first_protective_behavior": "Pair Bonding",
            "first_romantic_attraction": "Pair Bonding",
            "first_family_formation": "Family Formation",
            "first_child_teaching": "Family Formation",
            "multi_generation_family": "Family Formation",
            # Tribal Formation Phase
            "first_group_leadership": "Tribal Formation",
            "first_group_cooperation": "Tribal Formation",
            "first_group_identity": "Tribal Formation",
            # Inter-Tribal Contact Phase
            "first_peaceful_contact": "Inter-Tribal Contact",
            "first_trade_exchange": "Inter-Tribal Contact",
            "first_inter_tribal_alliance": "Inter-Tribal Contact",
            "first_cultural_adoption": "Inter-Tribal Contact",
            "first_diplomatic_negotiation": "Inter-Tribal Contact",
            "first_conflict_resolution": "Inter-Tribal Contact",
        }
        return phase_mapping.get(milestone_name, "Unknown")
    
    def _generate_milestone_description(self, milestone_name, details):
        """Generate human-readable description of milestone achievement"""
        descriptions = {
            "first_tool_creation": "First being successfully created a tool, marking the beginning of technology",
            "first_successful_communication": "First successful communication between beings established",
            "first_emotional_response": "First being demonstrated strong emotional response",
            "first_memory_formation": "First significant memory formation observed",
            "first_self_awareness": "First evidence of self-awareness and consciousness",
            "skill_specialization": "First being developed specialized skills",
            "personality_expression": "Strong personality traits emerged",
            "first_stable_partnership": "First stable partnership formed between beings",
            "first_romantic_attraction": "First romantic relationship developed",
            # Tribal Formation Phase
            "first_group_leadership": "First leader emerged to guide a group",
            "first_group_cooperation": "First coordinated group activity achieved",
            "first_group_identity": "First group formed with shared identity and name",
            # Inter-Tribal Contact Phase
            "first_peaceful_contact": "First peaceful contact established between different groups",
            "first_trade_exchange": "First trade exchange between groups completed",
            "first_inter_tribal_alliance": "First alliance formed between different tribes",
            "first_cultural_adoption": "First adoption of another group's customs or practices",
            "first_diplomatic_negotiation": "First formal diplomatic negotiation conducted",
            "first_conflict_resolution": "First peaceful resolution of inter-group conflict",
        }
        
        base_description = descriptions.get(milestone_name, f"Milestone {milestone_name} achieved")
        
        if details and 'participants' in details:
            participants = details['participants']
            if len(participants) == 1:
                base_description += f" (Agent: {participants[0]})"
            elif len(participants) > 1:
                base_description += f" (Agents: {', '.join(participants)})"
        
        return base_description
    
    def _calculate_significance(self, milestone_name):
        """Calculate significance score for milestone"""
        significance_scores = {
            "first_tool_creation": 0.9,
            "first_successful_communication": 0.8,
            "first_emotional_response": 0.7,
            "first_memory_formation": 0.6,
            "first_self_awareness": 1.0,
            "skill_specialization": 0.6,
            "personality_expression": 0.5,
            "first_stable_partnership": 0.8,
            "first_romantic_attraction": 0.7,
            # Tribal Formation Phase
            "first_group_leadership": 0.8,
            "first_group_cooperation": 0.7,
            "first_group_identity": 0.9,
            # Inter-Tribal Contact Phase
            "first_peaceful_contact": 0.9,
            "first_trade_exchange": 0.8,
            "first_inter_tribal_alliance": 0.9,
            "first_cultural_adoption": 0.7,
            "first_diplomatic_negotiation": 0.8,
            "first_conflict_resolution": 0.8,
        }
        return significance_scores.get(milestone_name, 0.5)
    
    def _get_prerequisites(self, milestone_name):
        """Get prerequisite milestones"""
        prerequisites = {
            "first_successful_communication": ["first_self_awareness"],
            "skill_specialization": ["first_tool_creation"],
            "first_stable_partnership": ["first_successful_communication"],
            "first_romantic_attraction": ["first_emotional_response"],
        }
        return prerequisites.get(milestone_name, [])

class PhaseDetector:
    """Main phase detection and transition management system"""
    
    def __init__(self):
        self.phase_definitions = self._load_phase_definitions()
        self.transition_rules = self._load_transition_rules()
        self.milestone_tracker = MilestoneTracker()
        self.civilization_metrics = CivilizationMetrics()
        self.current_phase = "Genesis"
        self.phase_history = []
        
    def check_transition(self, world_state, agents, recent_events):
        """Determine if civilization should advance to next phase"""
        
        # Update civilization metrics
        self.civilization_metrics.calculate_metrics(world_state, agents, recent_events)
        
        # Check for new milestones
        new_milestones = self.milestone_tracker.check_milestones(world_state, agents, recent_events)
        
        # Evaluate phase transition
        next_phase_candidates = self._get_possible_transitions(self.current_phase)
        
        for candidate_phase in next_phase_candidates:
            if self._evaluate_phase_readiness(candidate_phase, world_state, agents):
                confidence = self._calculate_confidence(candidate_phase, world_state, agents)
                
                if confidence > 0.7:  # High confidence threshold
                    return PhaseTransition(
                        from_phase=self.current_phase,
                        to_phase=candidate_phase,
                        transition_time=world_state.day if hasattr(world_state, 'day') else 0,
                        trigger_milestones=new_milestones,
                        population_at_transition=len(agents),
                        confidence=confidence,
                        transition_events=self._identify_transition_events(recent_events)
                    )
        
        return None
    
    def _load_phase_definitions(self):
        """Load phase definitions and requirements"""
        return {
            "Genesis": {
                "min_population": 1,
                "min_complexity": 0.0,
                "required_milestones": [],
                "description": "The Spark of Consciousness"
            },
            "Individual Mastery": {
                "min_population": 3,
                "min_complexity": 0.2,
                "required_milestones": ["first_self_awareness", "first_tool_creation"],
                "description": "Learning to Survive"
            },
            "Pair Bonding": {
                "min_population": 5,
                "min_complexity": 0.4,
                "required_milestones": ["first_successful_communication", "personality_expression"],
                "description": "The First Connections"
            },
            "Family Formation": {
                "min_population": 8,
                "min_complexity": 0.6,
                "required_milestones": ["first_stable_partnership", "first_romantic_attraction"],
                "description": "Beyond the Pair"
            },
            "Tribal Formation": {
                "min_population": 15,
                "min_complexity": 0.8,
                "required_milestones": ["first_family_formation", "first_child_teaching"],
                "description": "The First Groups"
            },
            "Inter-Tribal Contact": {
                "min_population": 25,
                "min_complexity": 1.0,
                "required_milestones": ["first_group_leadership", "first_group_identity"],
                "description": "Meeting Others"
            }
        }
    
    def _load_transition_rules(self):
        """Load phase transition rules"""
        return {
            "Genesis": ["Individual Mastery"],
            "Individual Mastery": ["Pair Bonding"],
            "Pair Bonding": ["Family Formation"],
            "Family Formation": ["Tribal Formation"],
            "Tribal Formation": ["Inter-Tribal Contact"]
        }
    
    def _get_possible_transitions(self, current_phase):
        """Get possible next phases from current phase"""
        return self.transition_rules.get(current_phase, [])
    
    def _evaluate_phase_readiness(self, phase, world_state, agents):
        """Check if specific phase requirements are met"""
        
        phase_config = self.phase_definitions.get(phase, {})
        
        # Population requirements
        if len(agents) < phase_config.get("min_population", 0):
            return False
            
        # Required milestones
        required_milestones = set(phase_config.get("required_milestones", []))
        achieved_milestones = set(milestone.name for milestone in self.milestone_tracker.completed_milestones)
        
        if not required_milestones.issubset(achieved_milestones):
            return False
            
        # Behavioral complexity requirements
        if self.civilization_metrics.social_complexity_score < phase_config.get("min_complexity", 0.0):
            return False
        
        # Phase-specific requirements
        if phase == "Individual Mastery":
            return self._check_individual_mastery_requirements(world_state, agents)
        elif phase == "Pair Bonding":
            return self._check_pair_bonding_requirements(world_state, agents)
        elif phase == "Family Formation":
            return self._check_family_formation_requirements(world_state, agents)
        elif phase == "Tribal Formation":
            return self._check_tribal_formation_requirements(world_state, agents)
        elif phase == "Inter-Tribal Contact":
            return self._check_inter_tribal_contact_requirements(world_state, agents)
        
        return True
    
    def _check_individual_mastery_requirements(self, world_state, agents):
        """Specific requirements for individual mastery phase"""
        # Check if agents have developed individual skills and personalities
        skilled_agents = 0
        for agent in agents:
            # Check personality_scores (new structure)
            if hasattr(agent, 'personality_scores') and any(abs(trait - 0.5) > 0.3 for trait in agent.personality_scores.values()):
                skilled_agents += 1
            # Check personality (legacy structure)
            elif hasattr(agent, 'personality') and any(abs(trait - 0.5) > 0.3 for trait in agent.personality.values()):
                skilled_agents += 1
            # Check if agent has distinct traits (alternative indicator)
            elif hasattr(agent, 'traits') and len(agent.traits) > 0:
                skilled_agents += 1
        
        return skilled_agents >= 2  # At least 2 agents with distinct personalities
    
    def _check_pair_bonding_requirements(self, world_state, agents):
        """Specific requirements for pair bonding phase"""
        # Check if agents are attempting communication and forming bonds
        return self.civilization_metrics.communication_success_rate > 0.3
    
    def _check_family_formation_requirements(self, world_state, agents):
        """Specific requirements for family formation"""
        # Check if stable partnerships exist
        partnerships = 0
        for agent in agents:
            if (hasattr(agent, 'romantic_life') and 
                hasattr(agent.romantic_life, 'relationship_status') and
                agent.romantic_life.relationship_status in ['dating', 'engaged', 'married']):
                partnerships += 1
        
        return partnerships >= 2  # At least 2 agents in partnerships
    
    def _check_tribal_formation_requirements(self, world_state, agents):
        """Specific requirements for tribal formation phase"""
        # Check if groups/factions have formed
        if hasattr(world_state, 'factions') and len(world_state.factions) >= 1:
            # Check if factions have adequate membership
            for faction in world_state.factions:
                if hasattr(faction, 'members') and len(faction.members) >= 3:
                    return True
        
        # Check if agents show group cooperation behavior
        cooperation_events = 0
        for agent in agents:
            if hasattr(agent, 'relationships') and len(agent.relationships) >= 2:
                cooperation_events += 1
        
        return cooperation_events >= 3  # At least 3 agents with multiple relationships
    
    def _check_inter_tribal_contact_requirements(self, world_state, agents):
        """Specific requirements for inter-tribal contact phase"""
        # Check if multiple distinct groups exist
        if hasattr(world_state, 'factions') and len(world_state.factions) >= 2:
            # Check if groups have enough members to be considered separate tribes
            viable_factions = 0
            for faction in world_state.factions:
                if hasattr(faction, 'members') and len(faction.members) >= 3:
                    viable_factions += 1
            
            if viable_factions >= 2:
                return True
        
        # Alternative check: high cooperation index indicating group interactions
        return self.civilization_metrics.cooperation_index > 0.5
    
    def _calculate_confidence(self, phase, world_state, agents):
        """Calculate confidence score for phase transition"""
        confidence_factors = []
        
        # Population factor
        phase_config = self.phase_definitions.get(phase, {})
        min_pop = phase_config.get("min_population", 1)
        pop_factor = min(len(agents) / min_pop, 1.0)
        confidence_factors.append(pop_factor)
        
        # Complexity factor
        min_complexity = phase_config.get("min_complexity", 0.0)
        complexity_factor = min(self.civilization_metrics.social_complexity_score / min_complexity, 1.0) if min_complexity > 0 else 1.0
        confidence_factors.append(complexity_factor)
        
        # Milestone completion factor
        required_milestones = set(phase_config.get("required_milestones", []))
        achieved_milestones = set(milestone.name for milestone in self.milestone_tracker.completed_milestones)
        
        if required_milestones:
            milestone_factor = len(achieved_milestones.intersection(required_milestones)) / len(required_milestones)
        else:
            milestone_factor = 1.0
        confidence_factors.append(milestone_factor)
        
        return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.0
    
    def _identify_transition_events(self, recent_events):
        """Identify events that contributed to phase transition"""
        return [str(event) for event in recent_events[-5:]]  # Last 5 events
    
    def transition_to_phase(self, new_phase, transition_details=None):
        """Execute transition to new phase"""
        old_phase = self.current_phase
        
        # Record phase history
        if transition_details:
            self.phase_history.append(transition_details)
        
        # Update current phase
        self.current_phase = new_phase
        
        logging.info(f"🌟 PHASE TRANSITION: {old_phase} → {new_phase}")
        
        return True
    
    def get_current_status(self, world_state, agents):
        """Get current phase status and progress"""
        return {
            "current_phase": self.current_phase,
            "phase_description": self.phase_definitions.get(self.current_phase, {}).get("description", ""),
            "population": len(agents),
            "milestones_achieved": len(self.milestone_tracker.completed_milestones),
            "social_complexity": self.civilization_metrics.social_complexity_score,
            "cooperation_index": self.civilization_metrics.cooperation_index,
            "recent_milestones": [m.name for m in self.milestone_tracker.completed_milestones[-3:]],
            "next_possible_phases": self._get_possible_transitions(self.current_phase)
        }
    
    def get_milestone_progress(self, target_phase=None):
        """Get progress toward next phase milestones"""
        if not target_phase:
            possible_phases = self._get_possible_transitions(self.current_phase)
            target_phase = possible_phases[0] if possible_phases else None
        
        if not target_phase:
            return {}
        
        phase_config = self.phase_definitions.get(target_phase, {})
        required_milestones = phase_config.get("required_milestones", [])
        achieved_milestones = set(milestone.name for milestone in self.milestone_tracker.completed_milestones)
        
        return {
            "target_phase": target_phase,
            "required_milestones": required_milestones,
            "achieved_milestones": list(achieved_milestones.intersection(required_milestones)),
            "remaining_milestones": list(set(required_milestones) - achieved_milestones),
            "progress_percentage": len(achieved_milestones.intersection(required_milestones)) / len(required_milestones) * 100 if required_milestones else 100
        }
    
    def display_phase_dashboard(self, world_state, agents, detailed=True):
        """Display comprehensive civilization phase dashboard"""
        print(f"\n{'='*60}")
        print(f"🌟 SIMULIFE CIVILIZATION PHASE DASHBOARD")
        print(f"{'='*60}")
        
        # Current Phase Status
        phase_status = self.get_current_status(world_state, agents)
        print(f"\n🏛️  CURRENT CIVILIZATION PHASE")
        print(f"   Phase: {phase_status['current_phase']}")
        print(f"   Description: {phase_status['phase_description']}")
        print(f"   Population: {phase_status['population']} beings")
        print(f"   Day: {getattr(world_state, 'day', 'Unknown')}")
        
        # Civilization Metrics
        metrics = self.civilization_metrics
        print(f"\n📊 CIVILIZATION METRICS")
        print(f"   Social Complexity: {metrics.social_complexity_score:.3f}")
        print(f"   Cooperation Index: {metrics.cooperation_index:.3f}")
        print(f"   Communication Success: {metrics.communication_success_rate:.3f}")
        print(f"   Relationship Formation: {metrics.relationship_formation_rate:.3f}")
        print(f"   Knowledge Growth: {metrics.knowledge_accumulation_rate:.1f}")
        
        # Milestone Progress  
        milestone_progress = self.get_milestone_progress()
        if milestone_progress:
            print(f"\n🎯 PHASE PROGRESSION")
            print(f"   Target Phase: {milestone_progress['target_phase']}")
            print(f"   Progress: {milestone_progress['progress_percentage']:.1f}%")
            
            if milestone_progress['achieved_milestones']:
                print(f"   ✅ Achieved: {', '.join(milestone_progress['achieved_milestones'])}")
            
            if milestone_progress['remaining_milestones']:
                print(f"   🎯 Remaining: {', '.join(milestone_progress['remaining_milestones'])}")
        
        # Recent Milestones
        recent_milestones = self.milestone_tracker.completed_milestones[-5:]  # Last 5
        if recent_milestones:
            print(f"\n🏆 RECENT MILESTONES ACHIEVED")
            for milestone in recent_milestones:
                participants_str = ', '.join(milestone.participants) if milestone.participants else 'Unknown'
                print(f"   • {milestone.name} (Day {milestone.achieved_at})")
                print(f"     {milestone.description}")
                print(f"     Participants: {participants_str}")
                if detailed and milestone.details:
                    for key, value in milestone.details.items():
                        if key != 'participants':
                            print(f"     {key.title()}: {value}")
                print()
        
        # Phase History
        if self.phase_history:
            print(f"\n📜 CIVILIZATION HISTORY")
            for i, transition in enumerate(self.phase_history):
                print(f"   {i+1}. {transition.from_phase} → {transition.to_phase}")
                print(f"      Day: {transition.transition_time}, Population: {transition.population_at_transition}")
                print(f"      Confidence: {transition.confidence:.1%}")
        
        # Next Phase Requirements
        if milestone_progress and milestone_progress.get('target_phase'):
            target_phase = milestone_progress['target_phase']
            phase_config = self.phase_definitions.get(target_phase, {})
            
            print(f"\n🔮 NEXT PHASE REQUIREMENTS: {target_phase}")
            print(f"   Description: {phase_config.get('description', 'Unknown')}")
            print(f"   Min Population: {phase_config.get('min_population', 0)}")
            print(f"   Min Complexity: {phase_config.get('min_complexity', 0.0):.2f}")
            
            required_milestones = phase_config.get('required_milestones', [])
            if required_milestones:
                achieved = set(m.name for m in self.milestone_tracker.completed_milestones)
                print(f"   Required Milestones:")
                for milestone in required_milestones:
                    status = "✅" if milestone in achieved else "❌"
                    print(f"     {status} {milestone}")
        
        # All Available Milestones Status
        if detailed:
            print(f"\n📋 ALL MILESTONE STATUS")
            achieved_names = set(m.name for m in self.milestone_tracker.completed_milestones)
            
            phases = ["Genesis", "Individual Mastery", "Pair Bonding", "Family Formation", "Tribal Formation", "Inter-Tribal Contact"]
            for phase in phases:
                phase_milestones = [name for name, detector in self.milestone_tracker.milestone_detectors.items() 
                                   if self.milestone_tracker._get_milestone_phase(name) == phase]
                
                if phase_milestones:
                    print(f"\n   {phase} Phase:")
                    for milestone in phase_milestones:
                        status = "✅" if milestone in achieved_names else "⭕"
                        print(f"     {status} {milestone}")
        
        print(f"\n{'='*60}")
        print(f"End of Civilization Dashboard")
        print(f"{'='*60}\n")

def create_phase_detector():
    """Factory function to create a new PhaseDetector instance"""
    return PhaseDetector() 