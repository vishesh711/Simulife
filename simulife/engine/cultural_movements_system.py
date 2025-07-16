"""
Cultural Movements System for SimuLife
Generates ideologies, belief systems, religious movements, and social changes
that emerge naturally from agent interactions and shared cultural experiences.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import math


class MovementType(Enum):
    """Types of cultural movements."""
    RELIGIOUS = "religious"                 # Spiritual beliefs and practices
    POLITICAL = "political"                 # Governance and social organization
    PHILOSOPHICAL = "philosophical"         # Ways of thinking and understanding
    SOCIAL_REFORM = "social_reform"         # Changes to social norms and practices
    CULTURAL_REVIVAL = "cultural_revival"   # Restoration of traditional practices
    REVOLUTIONARY = "revolutionary"         # Radical social transformation
    ARTISTIC = "artistic"                   # Creative expression movements
    INTELLECTUAL = "intellectual"           # Knowledge and learning focused


class MovementStage(Enum):
    """Stages of movement development."""
    EMERGING = "emerging"                   # Initial formation
    GROWING = "growing"                     # Gaining followers
    ESTABLISHED = "established"             # Stable and influential
    DOMINANT = "dominant"                   # Major cultural force
    DECLINING = "declining"                 # Losing influence
    TRANSFORMING = "transforming"           # Evolving into new form
    FRAGMENTING = "fragmenting"             # Breaking into sub-movements


class BeliefIntensity(Enum):
    """Intensity of belief in a movement."""
    CURIOUS = "curious"                     # Mild interest
    SYMPATHETIC = "sympathetic"             # Agrees with ideas
    COMMITTED = "committed"                 # Active supporter
    DEVOTED = "devoted"                     # Strong believer
    ZEALOUS = "zealous"                     # Extreme dedication


class PropagationMethod(Enum):
    """Methods of spreading cultural movements."""
    TEACHING = "teaching"                   # Formal education
    PREACHING = "preaching"                 # Religious/ideological proclamation
    STORYTELLING = "storytelling"           # Narrative transmission
    DEMONSTRATION = "demonstration"         # Leading by example
    ARTISTIC_EXPRESSION = "artistic_expression"  # Through art and creativity
    SOCIAL_PRESSURE = "social_pressure"     # Peer influence
    INSTITUTIONAL = "institutional"         # Through organizations
    CRISIS_RESPONSE = "crisis_response"     # Emergence during difficult times


@dataclass
class CulturalBelief:
    """Represents a cultural belief or value."""
    id: str
    name: str
    description: str
    core_principles: List[str]              # Key tenets of the belief
    origin_source: str                      # What led to this belief
    evidence_support: float                 # How well-supported it seems (0.0-1.0)
    emotional_appeal: float                 # How emotionally compelling (0.0-1.0)
    practical_utility: float               # How useful in daily life (0.0-1.0)
    complexity: float                       # How easy to understand (0.0-1.0)
    exclusivity: float                      # How much it conflicts with others (0.0-1.0)
    
    # Social aspects
    social_cohesion: float                  # How much it brings people together
    authority_structure: Optional[str]      # Who has authority in this belief
    ritual_practices: List[str]             # Associated practices
    moral_codes: List[str]                  # Ethical guidelines
    
    # Propagation characteristics
    preferred_methods: List[PropagationMethod]
    target_demographics: List[str]          # Who is most receptive
    resistance_factors: List[str]           # What opposes this belief


@dataclass
class CulturalMovement:
    """Represents a cultural movement or ideology."""
    id: str
    name: str
    movement_type: MovementType
    founding_day: int
    founding_location: str
    
    # Core beliefs and values
    core_beliefs: Set[str]                  # Belief IDs
    central_narrative: str                  # Main story/explanation
    key_symbols: List[str]                  # Important symbols/artifacts
    sacred_texts: List[str]                 # Important written works
    
    # Leadership and organization
    founders: Set[str]                      # Original creators
    current_leaders: Set[str]               # Current authorities
    organizational_structure: str           # How it's organized
    leadership_selection: str               # How leaders are chosen
    
    # Membership and influence
    believers: Dict[str, BeliefIntensity]   # Agent name -> belief intensity
    sympathizers: Set[str]                  # Agents who are interested
    opponents: Set[str]                     # Agents who oppose it
    
    # Movement characteristics
    stage: MovementStage
    influence_radius: float                 # Geographic spread (0.0-1.0)
    cultural_influence: float               # Impact on culture (0.0-1.0)
    political_influence: float              # Impact on governance (0.0-1.0)
    economic_influence: float               # Impact on economy (0.0-1.0)
    
    # Development and change
    schisms: List[Dict[str, Any]]           # Splits in the movement
    reforms: List[Dict[str, Any]]           # Changes and adaptations
    conflicts: List[Dict[str, Any]]         # Disputes with other movements
    achievements: List[Dict[str, Any]]      # Major accomplishments
    
    # Propagation and growth
    growth_rate: float                      # How quickly it's spreading
    propagation_methods: List[PropagationMethod]
    recruitment_success: float             # How good at gaining followers
    retention_rate: float                  # How well it keeps followers


@dataclass
class CulturalConflict:
    """Represents conflict between cultural movements or beliefs."""
    id: str
    conflicting_movements: List[str]        # Movement IDs in conflict
    conflict_type: str                      # Type of disagreement
    intensity: float                        # How severe the conflict (0.0-1.0)
    started_day: int
    
    # Conflict characteristics
    core_disagreements: List[str]           # What they disagree about
    contested_resources: List[str]          # What they're competing for
    territorial_disputes: List[str]         # Geographic areas of conflict
    
    # Resolution attempts
    mediation_attempts: List[Dict[str, Any]]
    compromises_offered: List[Dict[str, Any]]
    resolution_status: str                  # Current status
    
    # Impact
    affected_population: Set[str]           # Agents caught in conflict
    social_disruption: float                # Impact on community (0.0-1.0)
    violence_level: float                   # Physical conflict level (0.0-1.0)


class CulturalMovementsSystem:
    """
    Manages the emergence and evolution of cultural movements, ideologies, and belief systems.
    """
    
    def __init__(self):
        self.cultural_beliefs: Dict[str, CulturalBelief] = {}
        self.movements: Dict[str, CulturalMovement] = {}
        self.cultural_conflicts: Dict[str, CulturalConflict] = {}
        
        # Tracking and history
        self.movement_events: List[Dict[str, Any]] = []
        self.belief_evolution: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.cultural_zeitgeist: Dict[int, Dict[str, Any]] = {}  # Day -> cultural snapshot
        
        # System configuration
        self.movement_formation_triggers = self._initialize_formation_triggers()
        self.belief_archetypes = self._initialize_belief_archetypes()
        self.propagation_effectiveness = self._initialize_propagation_effectiveness()
        
        # Initialize fundamental beliefs
        self._initialize_fundamental_beliefs()
    
    def _initialize_formation_triggers(self) -> Dict[str, Dict[str, Any]]:
        """Initialize triggers that can cause movement formation."""
        return {
            "crisis_response": {
                "description": "Major crisis requiring explanation or solution",
                "trigger_events": ["natural_disaster", "epidemic", "resource_scarcity", "conflict"],
                "movement_types": [MovementType.RELIGIOUS, MovementType.POLITICAL, MovementType.SOCIAL_REFORM],
                "formation_probability": 0.3
            },
            "cultural_innovation": {
                "description": "New ideas or discoveries changing worldview",
                "trigger_events": ["technological_breakthrough", "knowledge_discovery", "artistic_innovation"],
                "movement_types": [MovementType.PHILOSOPHICAL, MovementType.INTELLECTUAL, MovementType.ARTISTIC],
                "formation_probability": 0.2
            },
            "social_tension": {
                "description": "Growing dissatisfaction with current social order",
                "trigger_events": ["inequality", "leadership_failure", "cultural_oppression"],
                "movement_types": [MovementType.REVOLUTIONARY, MovementType.SOCIAL_REFORM, MovementType.POLITICAL],
                "formation_probability": 0.25
            },
            "spiritual_seeking": {
                "description": "Questions about meaning and purpose in life",
                "trigger_events": ["elder_wisdom", "mystical_experience", "death_contemplation"],
                "movement_types": [MovementType.RELIGIOUS, MovementType.PHILOSOPHICAL],
                "formation_probability": 0.15
            },
            "cultural_nostalgia": {
                "description": "Desire to return to perceived better past",
                "trigger_events": ["cultural_loss", "tradition_erosion", "generational_change"],
                "movement_types": [MovementType.CULTURAL_REVIVAL, MovementType.SOCIAL_REFORM],
                "formation_probability": 0.2
            },
            "visionary_leadership": {
                "description": "Charismatic individual with compelling vision",
                "trigger_events": ["exceptional_individual", "spiritual_revelation", "intellectual_breakthrough"],
                "movement_types": [MovementType.RELIGIOUS, MovementType.POLITICAL, MovementType.PHILOSOPHICAL],
                "formation_probability": 0.1
            }
        }
    
    def _initialize_belief_archetypes(self) -> Dict[str, Dict[str, Any]]:
        """Initialize archetypal beliefs that can form."""
        return {
            "cosmological": {
                "themes": ["creation_myths", "afterlife_beliefs", "cosmic_purpose"],
                "principles": ["universal_order", "divine_plan", "cosmic_balance"],
                "appeal": "existential_questions"
            },
            "moral_ethical": {
                "themes": ["right_and_wrong", "virtue_and_vice", "justice"],
                "principles": ["golden_rule", "karma", "moral_duty"],
                "appeal": "social_harmony"
            },
            "social_organization": {
                "themes": ["leadership", "cooperation", "hierarchy"],
                "principles": ["collective_good", "individual_rights", "social_contract"],
                "appeal": "practical_governance"
            },
            "nature_relationship": {
                "themes": ["environmental_stewardship", "natural_harmony", "resource_use"],
                "principles": ["sustainability", "respect_for_nature", "human_dominion"],
                "appeal": "survival_and_prosperity"
            },
            "knowledge_wisdom": {
                "themes": ["learning", "understanding", "truth_seeking"],
                "principles": ["empirical_observation", "revealed_truth", "rational_inquiry"],
                "appeal": "intellectual_satisfaction"
            },
            "artistic_expression": {
                "themes": ["beauty", "creativity", "cultural_identity"],
                "principles": ["aesthetic_values", "creative_freedom", "cultural_preservation"],
                "appeal": "emotional_fulfillment"
            }
        }
    
    def _initialize_propagation_effectiveness(self) -> Dict[PropagationMethod, Dict[str, float]]:
        """Initialize effectiveness of different propagation methods."""
        return {
            PropagationMethod.TEACHING: {
                "educated_receptivity": 0.8,
                "young_receptivity": 0.9,
                "retention_rate": 0.7,
                "depth_of_conversion": 0.6
            },
            PropagationMethod.PREACHING: {
                "emotional_receptivity": 0.8,
                "crisis_effectiveness": 0.9,
                "retention_rate": 0.5,
                "depth_of_conversion": 0.8
            },
            PropagationMethod.STORYTELLING: {
                "universal_appeal": 0.7,
                "cultural_resonance": 0.8,
                "retention_rate": 0.6,
                "depth_of_conversion": 0.5
            },
            PropagationMethod.DEMONSTRATION: {
                "practical_appeal": 0.6,
                "credibility_boost": 0.8,
                "retention_rate": 0.8,
                "depth_of_conversion": 0.7
            },
            PropagationMethod.ARTISTIC_EXPRESSION: {
                "emotional_impact": 0.9,
                "cultural_penetration": 0.7,
                "retention_rate": 0.6,
                "depth_of_conversion": 0.6
            },
            PropagationMethod.SOCIAL_PRESSURE: {
                "conformity_drive": 0.8,
                "social_integration": 0.9,
                "retention_rate": 0.4,
                "depth_of_conversion": 0.3
            }
        }
    
    def _initialize_fundamental_beliefs(self) -> None:
        """Initialize some fundamental beliefs that exist in the culture."""
        fundamental_beliefs = [
            CulturalBelief(
                id="ancestor_veneration",
                name="Ancestor Veneration",
                description="Belief that deceased ancestors watch over and guide the living",
                core_principles=["respect_for_elders", "continuity_of_family", "wisdom_of_ancestors"],
                origin_source="death_and_memory",
                evidence_support=0.3,
                emotional_appeal=0.8,
                practical_utility=0.6,
                complexity=0.2,
                exclusivity=0.1,
                social_cohesion=0.7,
                authority_structure="family_elders",
                ritual_practices=["memorial_ceremonies", "ancestor_prayers", "family_gatherings"],
                moral_codes=["honor_family_name", "preserve_traditions", "care_for_elders"],
                preferred_methods=[PropagationMethod.STORYTELLING, PropagationMethod.DEMONSTRATION],
                target_demographics=["family_oriented", "tradition_minded"],
                resistance_factors=["individualistic_values", "youth_rebellion"]
            ),
            
            CulturalBelief(
                id="natural_harmony",
                name="Natural Harmony",
                description="Belief that humans should live in balance with nature",
                core_principles=["environmental_respect", "sustainable_living", "natural_wisdom"],
                origin_source="environmental_observation",
                evidence_support=0.7,
                emotional_appeal=0.6,
                practical_utility=0.8,
                complexity=0.4,
                exclusivity=0.2,
                social_cohesion=0.6,
                authority_structure="nature_wise",
                ritual_practices=["seasonal_celebrations", "nature_meditation", "conservation_practices"],
                moral_codes=["do_no_harm_to_nature", "take_only_what_is_needed", "preserve_for_future"],
                preferred_methods=[PropagationMethod.DEMONSTRATION, PropagationMethod.TEACHING],
                target_demographics=["rural_dwellers", "resource_dependent"],
                resistance_factors=["urban_development", "resource_exploitation"]
            ),
            
            CulturalBelief(
                id="collective_cooperation",
                name="Collective Cooperation",
                description="Belief that community welfare is more important than individual gain",
                core_principles=["shared_responsibility", "mutual_aid", "collective_decision_making"],
                origin_source="survival_necessity",
                evidence_support=0.6,
                emotional_appeal=0.7,
                practical_utility=0.8,
                complexity=0.3,
                exclusivity=0.4,
                social_cohesion=0.9,
                authority_structure="community_council",
                ritual_practices=["community_meetings", "shared_labor", "resource_sharing"],
                moral_codes=["help_others_in_need", "contribute_to_community", "consensus_decision_making"],
                preferred_methods=[PropagationMethod.DEMONSTRATION, PropagationMethod.SOCIAL_PRESSURE],
                target_demographics=["community_minded", "resource_scarce"],
                resistance_factors=["individualistic_tendencies", "competitive_personalities"]
            ),
            
            CulturalBelief(
                id="knowledge_pursuit",
                name="Knowledge Pursuit",
                description="Belief that seeking knowledge and understanding is a fundamental virtue",
                core_principles=["intellectual_curiosity", "truth_seeking", "wisdom_accumulation"],
                origin_source="problem_solving_success",
                evidence_support=0.8,
                emotional_appeal=0.5,
                practical_utility=0.9,
                complexity=0.6,
                exclusivity=0.1,
                social_cohesion=0.5,
                authority_structure="learned_scholars",
                ritual_practices=["knowledge_sharing", "research_activities", "teaching_sessions"],
                moral_codes=["seek_truth", "share_knowledge", "question_assumptions"],
                preferred_methods=[PropagationMethod.TEACHING, PropagationMethod.DEMONSTRATION],
                target_demographics=["intellectually_curious", "skill_oriented"],
                resistance_factors=["anti_intellectualism", "tradition_rigid"]
            )
        ]
        
        for belief in fundamental_beliefs:
            self.cultural_beliefs[belief.id] = belief
    
    def process_daily_cultural_movements(self, agents: List[Any], groups: Dict[str, Any],
                                       world_events: List[Dict[str, Any]], 
                                       current_day: int) -> List[Dict[str, Any]]:
        """Process daily cultural movement activities."""
        events = []
        
        # Step 1: Check for movement formation triggers
        formation_events = self._check_movement_formation(agents, groups, world_events, current_day)
        events.extend(formation_events)
        
        # Step 2: Process belief propagation and recruitment
        propagation_events = self._process_belief_propagation(agents, current_day)
        events.extend(propagation_events)
        
        # Step 3: Evolve existing movements
        evolution_events = self._evolve_movements(agents, current_day)
        events.extend(evolution_events)
        
        # Step 4: Handle cultural conflicts
        conflict_events = self._process_cultural_conflicts(agents, current_day)
        events.extend(conflict_events)
        
        # Step 5: Track cultural zeitgeist
        self._update_cultural_zeitgeist(agents, current_day)
        
        # Step 6: Process movement interactions with institutions
        institutional_events = self._process_institutional_interactions(agents, groups, current_day)
        events.extend(institutional_events)
        
        return events
    
    def _check_movement_formation(self, agents: List[Any], groups: Dict[str, Any],
                                world_events: List[Dict[str, Any]], 
                                current_day: int) -> List[Dict[str, Any]]:
        """Check for conditions that might trigger new movement formation."""
        events = []
        
        # Analyze current conditions for movement triggers
        current_conditions = self._analyze_cultural_conditions(agents, groups, world_events)
        
        for trigger_name, trigger_config in self.movement_formation_triggers.items():
            trigger_strength = self._calculate_trigger_strength(trigger_name, current_conditions, world_events)
            
            if trigger_strength > 0.5:  # Sufficient conditions for movement formation
                formation_chance = trigger_config["formation_probability"] * trigger_strength
                
                if random.random() < formation_chance:
                    # Attempt to form a new movement
                    movement = self._create_cultural_movement(trigger_name, trigger_config, agents, current_day)
                    if movement:
                        events.append({
                            "type": "cultural_movement_formation",
                            "movement_name": movement.name,
                            "movement_type": movement.movement_type.value,
                            "trigger": trigger_name,
                            "founders": list(movement.founders),
                            "core_beliefs": list(movement.core_beliefs),
                            "day": current_day
                        })
        
        return events
    
    def _analyze_cultural_conditions(self, agents: List[Any], groups: Dict[str, Any],
                                   world_events: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze current conditions that might trigger cultural movements."""
        conditions = {
            "crisis_level": 0.0,
            "innovation_level": 0.0,
            "social_tension": 0.0,
            "spiritual_seeking": 0.0,
            "cultural_nostalgia": 0.0,
            "visionary_potential": 0.0
        }
        
        # Crisis level from recent events
        crisis_events = ["natural_disaster", "epidemic", "resource_scarcity", "conflict", "death"]
        recent_crises = [e for e in world_events if any(crisis in e.get("type", "") for crisis in crisis_events)]
        conditions["crisis_level"] = min(1.0, len(recent_crises) / 5.0)
        
        # Innovation level from technological/knowledge advancement
        innovation_events = ["technological_breakthrough", "knowledge_discovery", "cultural_innovation"]
        recent_innovations = [e for e in world_events if any(innov in e.get("type", "") for innov in innovation_events)]
        conditions["innovation_level"] = min(1.0, len(recent_innovations) / 3.0)
        
        # Social tension from conflicts and inequality
        conflict_count = 0
        leadership_issues = 0
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            # Count recent conflicts
            if hasattr(agent, 'memory'):
                recent_conflicts = agent.memory.get_memories_by_type("conflict", limit=5)
                conflict_count += len(recent_conflicts)
            
            # Check for leadership dissatisfaction
            if hasattr(agent, 'reputation') and agent.reputation < 0.3:
                leadership_issues += 1
        
        conditions["social_tension"] = min(1.0, (conflict_count / max(1, len(agents))) + 
                                         (leadership_issues / max(1, len(agents))))
        
        # Spiritual seeking from mortality awareness and meaning-seeking
        elder_count = len([a for a in agents if a.is_alive and a.age > 60])
        death_awareness = len([a for a in agents if not a.is_alive]) / max(1, len(agents))
        conditions["spiritual_seeking"] = min(1.0, (elder_count / max(1, len(agents))) + death_awareness)
        
        # Cultural nostalgia from tradition loss
        young_count = len([a for a in agents if a.is_alive and a.age < 25])
        generational_gap = young_count / max(1, len([a for a in agents if a.is_alive]))
        conditions["cultural_nostalgia"] = min(1.0, generational_gap * 0.5)
        
        # Visionary potential from high-reputation, skilled individuals
        visionaries = len([a for a in agents if a.is_alive and 
                          hasattr(a, 'reputation') and a.reputation > 0.8])
        conditions["visionary_potential"] = min(1.0, visionaries / max(1, len(agents) / 10))
        
        return conditions
    
    def _calculate_trigger_strength(self, trigger_name: str, conditions: Dict[str, float],
                                  world_events: List[Dict[str, Any]]) -> float:
        """Calculate strength of a movement formation trigger."""
        trigger_mapping = {
            "crisis_response": conditions["crisis_level"],
            "cultural_innovation": conditions["innovation_level"],
            "social_tension": conditions["social_tension"],
            "spiritual_seeking": conditions["spiritual_seeking"],
            "cultural_nostalgia": conditions["cultural_nostalgia"],
            "visionary_leadership": conditions["visionary_potential"]
        }
        
        base_strength = trigger_mapping.get(trigger_name, 0.0)
        
        # Boost from relevant recent events
        trigger_config = self.movement_formation_triggers[trigger_name]
        relevant_events = [e for e in world_events if any(trigger_event in e.get("type", "") 
                          for trigger_event in trigger_config["trigger_events"])]
        
        event_boost = min(0.5, len(relevant_events) * 0.1)
        
        return min(1.0, base_strength + event_boost)
    
    def _create_cultural_movement(self, trigger_name: str, trigger_config: Dict[str, Any],
                                agents: List[Any], current_day: int) -> Optional[CulturalMovement]:
        """Create a new cultural movement."""
        # Find suitable founders
        founders = self._identify_movement_founders(trigger_name, agents)
        if not founders:
            return None
        
        # Choose movement type
        movement_type = random.choice(trigger_config["movement_types"])
        
        # Generate movement characteristics
        movement_id = f"movement_{movement_type.value}_{current_day}"
        movement_name = self._generate_movement_name(movement_type, trigger_name, founders[0])
        
        # Create core beliefs for this movement
        core_beliefs = self._generate_movement_beliefs(movement_type, trigger_name, current_day)
        
        # Generate central narrative
        central_narrative = self._generate_movement_narrative(movement_type, trigger_name, founders)
        
        movement = CulturalMovement(
            id=movement_id,
            name=movement_name,
            movement_type=movement_type,
            founding_day=current_day,
            founding_location=founders[0].location,
            
            core_beliefs=set(core_beliefs),
            central_narrative=central_narrative,
            key_symbols=[],
            sacred_texts=[],
            
            founders={f.name for f in founders},
            current_leaders={f.name for f in founders},
            organizational_structure="informal",
            leadership_selection="charismatic",
            
            believers={f.name: BeliefIntensity.DEVOTED for f in founders},
            sympathizers=set(),
            opponents=set(),
            
            stage=MovementStage.EMERGING,
            influence_radius=0.1,
            cultural_influence=0.1,
            political_influence=0.0,
            economic_influence=0.0,
            
            schisms=[],
            reforms=[],
            conflicts=[],
            achievements=[],
            
            growth_rate=0.1,
            propagation_methods=self._determine_propagation_methods(movement_type),
            recruitment_success=0.3,
            retention_rate=0.6
        )
        
        self.movements[movement_id] = movement
        
        # Add founding memory to founders
        for founder in founders:
            founder.memory.store_memory(
                f"Founded {movement_name} movement with core belief in {central_narrative}",
                importance=0.9,
                memory_type="cultural"
            )
        
        return movement
    
    def _identify_movement_founders(self, trigger_name: str, agents: List[Any]) -> List[Any]:
        """Identify agents suitable for founding a movement."""
        potential_founders = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            founder_score = 0.0
            
            # Leadership and reputation
            if hasattr(agent, 'reputation'):
                founder_score += agent.reputation * 0.4
            
            # Relevant specializations
            if hasattr(agent, 'specialization'):
                if trigger_name in ["spiritual_seeking", "crisis_response"] and agent.specialization == "mystic":
                    founder_score += 0.3
                elif trigger_name == "cultural_innovation" and agent.specialization == "scholar":
                    founder_score += 0.3
                elif trigger_name == "social_tension" and agent.specialization == "leader":
                    founder_score += 0.3
            
            # Personality traits
            if hasattr(agent, 'traits'):
                if "charismatic" in agent.traits or "ambitious" in agent.traits:
                    founder_score += 0.2
                if trigger_name == "cultural_innovation" and "creative" in agent.traits:
                    founder_score += 0.1
                if trigger_name == "spiritual_seeking" and "spiritual" in agent.traits:
                    founder_score += 0.1
            
            # Social connections
            if hasattr(agent, 'relationships'):
                social_network = len(agent.relationships)
                founder_score += min(0.2, social_network / 10.0)
            
            if founder_score >= 0.6:  # Threshold for founding capability
                potential_founders.append(agent)
        
        # Sort by score and return top candidates
        potential_founders.sort(
            key=lambda a: self._calculate_founder_score(a, trigger_name), 
            reverse=True
        )
        
        return potential_founders[:random.randint(1, 3)]  # 1-3 founders
    
    def _calculate_founder_score(self, agent: Any, trigger_name: str) -> float:
        """Calculate an agent's suitability for founding a movement."""
        score = 0.0
        
        if hasattr(agent, 'reputation'):
            score += agent.reputation * 0.4
        
        if hasattr(agent, 'relationships'):
            score += min(0.3, len(agent.relationships) / 10.0)
        
        # Age factor - not too young, not too old
        age_factor = 1.0 - abs(agent.age - 40) / 40.0  # Peak at age 40
        score += max(0, age_factor) * 0.3
        
        return score
    
    def _generate_movement_name(self, movement_type: MovementType, trigger_name: str, 
                              founder: Any) -> str:
        """Generate a name for the cultural movement."""
        name_templates = {
            MovementType.RELIGIOUS: [
                f"The {founder.name} Teachings",
                f"The Sacred Way of {founder.location.title()}",
                "The Divine Harmony",
                "The Eternal Light"
            ],
            MovementType.POLITICAL: [
                f"The {founder.location.title()} Council",
                "The People's Alliance",
                "The New Order",
                "The Unity Movement"
            ],
            MovementType.PHILOSOPHICAL: [
                f"The {founder.name} School",
                "The Wisdom Seekers",
                "The Truth Path",
                "The Enlightened Way"
            ],
            MovementType.SOCIAL_REFORM: [
                "The Change Makers",
                "The Progressive Alliance",
                "The Reform Movement",
                "The New Society"
            ],
            MovementType.CULTURAL_REVIVAL: [
                "The Ancient Ways",
                "The Tradition Keepers",
                "The Heritage Circle",
                "The Old Path"
            ],
            MovementType.REVOLUTIONARY: [
                "The Liberation Front",
                "The Revolutionary Guard",
                "The Freedom Movement",
                "The New Dawn"
            ]
        }
        
        templates = name_templates.get(movement_type, ["The New Movement"])
        return random.choice(templates)
    
    def _generate_movement_beliefs(self, movement_type: MovementType, trigger_name: str,
                                 current_day: int) -> List[str]:
        """Generate core beliefs for a movement."""
        beliefs = []
        
        # Select relevant archetypal beliefs
        if movement_type == MovementType.RELIGIOUS:
            archetype = "cosmological"
            belief_themes = ["afterlife", "divine_purpose", "spiritual_practices"]
        elif movement_type == MovementType.POLITICAL:
            archetype = "social_organization"
            belief_themes = ["governance", "justice", "collective_action"]
        elif movement_type == MovementType.PHILOSOPHICAL:
            archetype = "knowledge_wisdom"
            belief_themes = ["truth_seeking", "rational_inquiry", "understanding"]
        elif movement_type == MovementType.SOCIAL_REFORM:
            archetype = "moral_ethical"
            belief_themes = ["social_justice", "equality", "progress"]
        else:
            archetype = "nature_relationship"
            belief_themes = ["balance", "harmony", "sustainability"]
        
        # Create new beliefs or reference existing ones
        for theme in belief_themes[:2]:  # Maximum 2 core beliefs
            belief_id = f"belief_{theme}_{current_day}"
            
            if belief_id not in self.cultural_beliefs:
                # Create new belief
                new_belief = self._create_belief_from_theme(belief_id, theme, archetype)
                self.cultural_beliefs[belief_id] = new_belief
            
            beliefs.append(belief_id)
        
        # Also include some existing fundamental beliefs if compatible
        compatible_beliefs = self._find_compatible_beliefs(movement_type, trigger_name)
        beliefs.extend(compatible_beliefs[:1])  # Add up to 1 existing belief
        
        return beliefs
    
    def _create_belief_from_theme(self, belief_id: str, theme: str, archetype: str) -> CulturalBelief:
        """Create a new cultural belief from a theme."""
        archetype_config = self.belief_archetypes[archetype]
        
        return CulturalBelief(
            id=belief_id,
            name=theme.replace("_", " ").title(),
            description=f"Belief system centered on {theme.replace('_', ' ')}",
            core_principles=archetype_config["principles"][:2],
            origin_source=theme,
            evidence_support=random.uniform(0.3, 0.7),
            emotional_appeal=random.uniform(0.5, 0.9),
            practical_utility=random.uniform(0.4, 0.8),
            complexity=random.uniform(0.3, 0.7),
            exclusivity=random.uniform(0.1, 0.6),
            social_cohesion=random.uniform(0.5, 0.8),
            authority_structure="movement_leaders",
            ritual_practices=[f"{theme}_ceremony", f"{theme}_practice"],
            moral_codes=[f"uphold_{theme}", f"spread_{theme}"],
            preferred_methods=[PropagationMethod.TEACHING, PropagationMethod.PREACHING],
            target_demographics=["movement_sympathizers"],
            resistance_factors=["conflicting_beliefs", "established_traditions"]
        )
    
    def _find_compatible_beliefs(self, movement_type: MovementType, trigger_name: str) -> List[str]:
        """Find existing beliefs compatible with a movement."""
        compatible = []
        
        for belief_id, belief in self.cultural_beliefs.items():
            compatibility_score = 0.0
            
            # Religious movements compatible with spiritual beliefs
            if movement_type == MovementType.RELIGIOUS and "spiritual" in belief.description.lower():
                compatibility_score += 0.8
            
            # Political movements compatible with social organization beliefs
            if movement_type == MovementType.POLITICAL and "collective" in belief.core_principles:
                compatibility_score += 0.7
            
            # Reform movements compatible with progressive beliefs
            if movement_type == MovementType.SOCIAL_REFORM and belief.social_cohesion > 0.7:
                compatibility_score += 0.6
            
            if compatibility_score > 0.5:
                compatible.append(belief_id)
        
        return compatible
    
    def _generate_movement_narrative(self, movement_type: MovementType, trigger_name: str,
                                   founders: List[Any]) -> str:
        """Generate the central narrative/story of a movement."""
        founder_name = founders[0].name
        location = founders[0].location
        
        narratives = {
            MovementType.RELIGIOUS: [
                f"{founder_name} received divine revelation about the true nature of existence",
                f"The sacred spirits of {location} spoke through {founder_name} to guide the people",
                "The ancient wisdom has been rediscovered and must be shared with all"
            ],
            MovementType.POLITICAL: [
                f"The people of {location} deserve better leadership and {founder_name} will provide it",
                "A new form of governance based on justice and equality must be established",
                "The old ways of leadership have failed, and a new order must emerge"
            ],
            MovementType.PHILOSOPHICAL: [
                f"{founder_name} has discovered fundamental truths about how we should live",
                "Through careful thought and observation, the path to wisdom has been found",
                "The mysteries of existence can be understood through rational inquiry"
            ],
            MovementType.SOCIAL_REFORM: [
                "Society can be improved through collective action and progressive change",
                f"The injustices witnessed in {location} demand immediate reform",
                "A better world is possible if we work together to create it"
            ],
            MovementType.CULTURAL_REVIVAL: [
                "The ancient ways of our ancestors were superior and must be restored",
                f"The traditions of {location} are being lost and must be preserved",
                "Modern changes have led us astray from the true path of our people"
            ],
            MovementType.REVOLUTIONARY: [
                "The current system is fundamentally corrupt and must be completely overthrown",
                f"The oppressed people of {location} must rise up and claim their freedom",
                "Only through radical change can true justice be achieved"
            ]
        }
        
        movement_narratives = narratives.get(movement_type, ["A new way of thinking has emerged"])
        return random.choice(movement_narratives)
    
    def _determine_propagation_methods(self, movement_type: MovementType) -> List[PropagationMethod]:
        """Determine the primary propagation methods for a movement type."""
        method_preferences = {
            MovementType.RELIGIOUS: [
                PropagationMethod.PREACHING, 
                PropagationMethod.STORYTELLING, 
                PropagationMethod.ARTISTIC_EXPRESSION
            ],
            MovementType.POLITICAL: [
                PropagationMethod.DEMONSTRATION, 
                PropagationMethod.SOCIAL_PRESSURE, 
                PropagationMethod.INSTITUTIONAL
            ],
            MovementType.PHILOSOPHICAL: [
                PropagationMethod.TEACHING, 
                PropagationMethod.DEMONSTRATION, 
                PropagationMethod.STORYTELLING
            ],
            MovementType.SOCIAL_REFORM: [
                PropagationMethod.DEMONSTRATION, 
                PropagationMethod.SOCIAL_PRESSURE, 
                PropagationMethod.CRISIS_RESPONSE
            ],
            MovementType.CULTURAL_REVIVAL: [
                PropagationMethod.STORYTELLING, 
                PropagationMethod.ARTISTIC_EXPRESSION, 
                PropagationMethod.DEMONSTRATION
            ],
            MovementType.REVOLUTIONARY: [
                PropagationMethod.CRISIS_RESPONSE, 
                PropagationMethod.SOCIAL_PRESSURE, 
                PropagationMethod.DEMONSTRATION
            ]
        }
        
        return method_preferences.get(movement_type, [PropagationMethod.TEACHING])
    
    def _process_belief_propagation(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process propagation of beliefs and recruitment to movements."""
        events = []
        
        for movement_id, movement in self.movements.items():
            if movement.stage in [MovementStage.DECLINING, MovementStage.FRAGMENTING]:
                continue
            
            # Find active propagators (believers with high intensity)
            propagators = [agent for agent in agents 
                          if agent.is_alive and agent.name in movement.believers and
                          movement.believers[agent.name] in [BeliefIntensity.DEVOTED, BeliefIntensity.ZEALOUS]]
            
            if not propagators:
                continue
            
            # Each propagator attempts to spread beliefs
            for propagator in propagators:
                propagation_events = self._attempt_belief_propagation(
                    propagator, movement, agents, current_day
                )
                events.extend(propagation_events)
        
        return events
    
    def _attempt_belief_propagation(self, propagator: Any, movement: CulturalMovement,
                                  agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Attempt to propagate beliefs from one agent to others."""
        events = []
        
        # Find potential converts in same location
        potential_converts = [agent for agent in agents 
                            if (agent.is_alive and 
                                agent.location == propagator.location and 
                                agent.name != propagator.name and
                                agent.name not in movement.believers and
                                agent.name not in movement.opponents)]
        
        if not potential_converts:
            return events
        
        # Select propagation method
        method = random.choice(movement.propagation_methods)
        
        # Choose target(s) for propagation
        num_targets = min(random.randint(1, 3), len(potential_converts))
        targets = random.sample(potential_converts, num_targets)
        
        for target in targets:
            # Calculate conversion probability
            conversion_probability = self._calculate_conversion_probability(
                propagator, target, movement, method
            )
            
            if random.random() < conversion_probability:
                # Successful conversion
                belief_intensity = self._determine_initial_belief_intensity(target, movement)
                movement.believers[target.name] = belief_intensity
                
                # Remove from sympathizers if present
                movement.sympathizers.discard(target.name)
                
                events.append({
                    "type": "belief_conversion",
                    "convert": target.name,
                    "propagator": propagator.name,
                    "movement": movement.name,
                    "method": method.value,
                    "belief_intensity": belief_intensity.value,
                    "day": current_day
                })
                
                # Add memory to both agents
                propagator.memory.store_memory(
                    f"Successfully shared {movement.name} beliefs with {target.name}",
                    importance=0.6,
                    memory_type="cultural"
                )
                
                target.memory.store_memory(
                    f"Learned about {movement.name} from {propagator.name} and found it compelling",
                    importance=0.7,
                    memory_type="cultural"
                )
                
            elif random.random() < conversion_probability * 2:  # Sympathizer creation
                movement.sympathizers.add(target.name)
                
                events.append({
                    "type": "belief_sympathy",
                    "sympathizer": target.name,
                    "propagator": propagator.name,
                    "movement": movement.name,
                    "method": method.value,
                    "day": current_day
                })
        
        return events
    
    def _calculate_conversion_probability(self, propagator: Any, target: Any, 
                                        movement: CulturalMovement, 
                                        method: PropagationMethod) -> float:
        """Calculate probability of successful belief conversion."""
        base_probability = 0.1  # 10% base chance
        
        # Propagator effectiveness
        if hasattr(propagator, 'reputation'):
            base_probability += propagator.reputation * 0.2
        
        if hasattr(propagator, 'specialization'):
            if propagator.specialization in ["mystic", "scholar", "leader"]:
                base_probability += 0.1
        
        # Relationship bonus
        if hasattr(propagator, 'relationships') and target.name in propagator.relationships:
            relationship = propagator.relationships[target.name]
            if relationship in ["friend", "family"]:
                base_probability += 0.3
            elif relationship in ["ally", "mentor"]:
                base_probability += 0.2
        
        # Target receptivity
        if hasattr(target, 'traits'):
            if "open_minded" in target.traits or "curious" in target.traits:
                base_probability += 0.2
            elif "skeptical" in target.traits or "stubborn" in target.traits:
                base_probability -= 0.2
        
        # Method effectiveness
        method_config = self.propagation_effectiveness.get(method, {})
        method_bonus = method_config.get("universal_appeal", 0.5) * 0.2
        base_probability += method_bonus
        
        # Movement appeal factors
        appeal_factors = []
        for belief_id in movement.core_beliefs:
            if belief_id in self.cultural_beliefs:
                belief = self.cultural_beliefs[belief_id]
                appeal_factors.extend([
                    belief.emotional_appeal * 0.1,
                    belief.practical_utility * 0.1,
                    (1.0 - belief.complexity) * 0.05  # Simpler beliefs spread easier
                ])
        
        if appeal_factors:
            base_probability += sum(appeal_factors) / len(appeal_factors)
        
        # Competition from existing beliefs
        existing_belief_resistance = len([bid for bid in movement.core_beliefs 
                                        if bid in self.cultural_beliefs]) * 0.05
        base_probability -= existing_belief_resistance
        
        return max(0.01, min(0.8, base_probability))  # Clamp between 1% and 80%
    
    def _determine_initial_belief_intensity(self, agent: Any, movement: CulturalMovement) -> BeliefIntensity:
        """Determine initial belief intensity for a new convert."""
        # Base on agent personality and conversion circumstances
        intensity_factors = []
        
        if hasattr(agent, 'traits'):
            if "passionate" in agent.traits or "devoted" in agent.traits:
                intensity_factors.append(0.8)
            elif "cautious" in agent.traits or "skeptical" in agent.traits:
                intensity_factors.append(0.3)
            else:
                intensity_factors.append(0.5)
        
        # Young agents more likely to be zealous
        if agent.age < 30:
            intensity_factors.append(0.7)
        elif agent.age > 60:
            intensity_factors.append(0.4)
        
        avg_intensity = sum(intensity_factors) / len(intensity_factors) if intensity_factors else 0.5
        
        if avg_intensity > 0.8:
            return BeliefIntensity.ZEALOUS
        elif avg_intensity > 0.6:
            return BeliefIntensity.DEVOTED
        elif avg_intensity > 0.4:
            return BeliefIntensity.COMMITTED
        elif avg_intensity > 0.2:
            return BeliefIntensity.SYMPATHETIC
        else:
            return BeliefIntensity.CURIOUS
    
    def _evolve_movements(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process evolution and development of existing movements."""
        events = []
        
        for movement_id, movement in self.movements.items():
            # Update movement metrics
            self._update_movement_metrics(movement, agents)
            
            # Check for stage transitions
            stage_change = self._check_stage_transition(movement, agents)
            if stage_change:
                old_stage = movement.stage
                movement.stage = stage_change
                events.append({
                    "type": "movement_stage_change",
                    "movement": movement.name,
                    "old_stage": old_stage.value,
                    "new_stage": stage_change.value,
                    "believer_count": len(movement.believers),
                    "day": current_day
                })
            
            # Check for reforms or schisms - reduce frequency to weekly
            if current_day % 7 == 0:  # Only check once per week
                reform_events = self._check_movement_reforms(movement, agents, current_day)
                events.extend(reform_events)
            
            # Check for achievements - reduce frequency to monthly
            if current_day % 30 == 0:  # Only check once per month
                achievement_events = self._check_movement_achievements(movement, agents, current_day)
                events.extend(achievement_events)
        
        return events
    
    def _update_movement_metrics(self, movement: CulturalMovement, agents: List[Any]) -> None:
        """Update movement metrics based on current state."""
        # Count active believers
        active_believers = len([name for name in movement.believers 
                              if any(a.name == name and a.is_alive for a in agents)])
        
        # Calculate growth rate
        total_population = len([a for a in agents if a.is_alive])
        if total_population > 0:
            believer_ratio = active_believers / total_population
            movement.growth_rate = min(1.0, believer_ratio * 2.0)  # Growth correlated with size
        
        # Update influence metrics
        if active_believers > 0:
            # Cultural influence based on believer ratio and intensity
            high_intensity_believers = len([name for name, intensity in movement.believers.items()
                                          if intensity in [BeliefIntensity.DEVOTED, BeliefIntensity.ZEALOUS]])
            movement.cultural_influence = min(1.0, (active_believers / max(1, total_population)) + 
                                           (high_intensity_believers * 0.1))
            
            # Political influence based on leadership and governance interaction
            leaders_in_govt = 0  # Would check against government institutions
            movement.political_influence = min(1.0, leaders_in_govt * 0.2)
            
            # Economic influence based on merchant/trader participation
            economic_participants = len([name for name in movement.believers
                                       if any(a.name == name and 
                                             hasattr(a, 'specialization') and 
                                             a.specialization == "merchant" for a in agents)])
            movement.economic_influence = min(1.0, economic_participants / max(1, active_believers))
            
            # Geographic influence based on spread
            locations = set(a.location for a in agents if a.name in movement.believers and a.is_alive)
            total_locations = len(set(a.location for a in agents if a.is_alive))
            movement.influence_radius = len(locations) / max(1, total_locations)
        
        # Update retention rate based on recent conversions vs departures
        # This would track actual retention over time
    
    def _check_stage_transition(self, movement: CulturalMovement, agents: List[Any]) -> Optional[MovementStage]:
        """Check if a movement should transition to a new stage."""
        active_believers = len([name for name in movement.believers 
                              if any(a.name == name and a.is_alive for a in agents)])
        total_population = len([a for a in agents if a.is_alive])
        
        current_stage = movement.stage
        
        if current_stage == MovementStage.EMERGING:
            if active_believers >= 5 and movement.cultural_influence > 0.1:
                return MovementStage.GROWING
        
        elif current_stage == MovementStage.GROWING:
            if active_believers >= 10 and movement.cultural_influence > 0.3:
                return MovementStage.ESTABLISHED
            elif active_believers < 3:
                return MovementStage.DECLINING
        
        elif current_stage == MovementStage.ESTABLISHED:
            if movement.cultural_influence > 0.6 and active_believers > total_population * 0.4:
                return MovementStage.DOMINANT
            elif active_believers < 5:
                return MovementStage.DECLINING
        
        elif current_stage == MovementStage.DOMINANT:
            if movement.cultural_influence < 0.4:
                return MovementStage.ESTABLISHED
            elif active_believers < total_population * 0.3:
                return MovementStage.DECLINING
        
        elif current_stage == MovementStage.DECLINING:
            if active_believers < 2:
                return MovementStage.FRAGMENTING
            elif active_believers >= 8 and movement.cultural_influence > 0.2:
                return MovementStage.ESTABLISHED
        
        return None
    
    def _check_movement_reforms(self, movement: CulturalMovement, agents: List[Any], 
                              current_day: int) -> List[Dict[str, Any]]:
        """Check for reforms or schisms within a movement."""
        events = []
        
        # Only established movements can have significant reforms
        if movement.stage not in [MovementStage.ESTABLISHED, MovementStage.DOMINANT]:
            return events
        
        # Check for schism probability
        if len(movement.believers) >= 8 and random.random() < 0.05:  # 5% chance
            schism_event = self._create_movement_schism(movement, agents, current_day)
            if schism_event:
                events.append(schism_event)
        
        # Check for reform probability
        elif random.random() < 0.08:  # 8% chance
            reform_event = self._create_movement_reform(movement, agents, current_day)
            if reform_event:
                events.append(reform_event)
        
        return events
    
    def _create_movement_schism(self, movement: CulturalMovement, agents: List[Any], 
                              current_day: int) -> Optional[Dict[str, Any]]:
        """Create a schism within a movement."""
        # Find potential schism leaders
        potential_leaders = [agent for agent in agents 
                           if (agent.is_alive and 
                               agent.name in movement.believers and
                               movement.believers[agent.name] in [BeliefIntensity.DEVOTED, BeliefIntensity.ZEALOUS] and
                               agent.name not in movement.current_leaders)]
        
        if not potential_leaders:
            return None
        
        schism_leader = random.choice(potential_leaders)
        
        # Create new breakaway movement
        new_movement_id = f"schism_{movement.id}_{current_day}"
        new_movement_name = f"{movement.name} Reformed"
        
        # Split believers
        breakaway_believers = {}
        for believer_name, intensity in list(movement.believers.items()):
            if random.random() < 0.3:  # 30% chance to join schism
                breakaway_believers[believer_name] = intensity
                del movement.believers[believer_name]
        
        # Ensure schism leader is in breakaway group
        if schism_leader.name not in breakaway_believers:
            breakaway_believers[schism_leader.name] = movement.believers.pop(schism_leader.name, BeliefIntensity.DEVOTED)
        
        # Create new movement
        new_movement = CulturalMovement(
            id=new_movement_id,
            name=new_movement_name,
            movement_type=movement.movement_type,
            founding_day=current_day,
            founding_location=schism_leader.location,
            
            core_beliefs=movement.core_beliefs.copy(),
            central_narrative=f"Reformed interpretation of {movement.central_narrative}",
            key_symbols=[],
            sacred_texts=[],
            
            founders={schism_leader.name},
            current_leaders={schism_leader.name},
            organizational_structure="reformed",
            leadership_selection="merit_based",
            
            believers=breakaway_believers,
            sympathizers=set(),
            opponents=set(),
            
            stage=MovementStage.EMERGING,
            influence_radius=0.1,
            cultural_influence=0.1,
            political_influence=0.0,
            economic_influence=0.0,
            
            schisms=[],
            reforms=[],
            conflicts=[],
            achievements=[],
            
            growth_rate=0.1,
            propagation_methods=movement.propagation_methods.copy(),
            recruitment_success=0.3,
            retention_rate=0.6
        )
        
        self.movements[new_movement_id] = new_movement
        
        # Record schism in original movement
        schism_record = {
            "type": "schism",
            "leader": schism_leader.name,
            "new_movement": new_movement_name,
            "followers_lost": len(breakaway_believers),
            "day": current_day,
            "reason": "doctrinal_differences"
        }
        movement.schisms.append(schism_record)
        
        return {
            "type": "movement_schism",
            "original_movement": movement.name,
            "new_movement": new_movement_name,
            "schism_leader": schism_leader.name,
            "followers_split": len(breakaway_believers),
            "day": current_day
        }
    
    def _create_movement_reform(self, movement: CulturalMovement, agents: List[Any], 
                              current_day: int) -> Optional[Dict[str, Any]]:
        """Create a reform within a movement."""
        # Find reform leader
        reform_leaders = [agent for agent in agents 
                         if (agent.is_alive and agent.name in movement.current_leaders)]
        
        if not reform_leaders:
            return None
        
        reform_leader = random.choice(reform_leaders)
        
        # Types of reforms
        reform_types = [
            "organizational_restructuring",
            "doctrinal_clarification", 
            "leadership_changes",
            "ritual_modifications",
            "outreach_expansion"
        ]
        
        reform_type = random.choice(reform_types)
        
        # Apply reform effects
        if reform_type == "organizational_restructuring":
            movement.organizational_structure = "hierarchical" if movement.organizational_structure == "informal" else "democratic"
        elif reform_type == "leadership_changes":
            movement.leadership_selection = "elected" if movement.leadership_selection == "charismatic" else "hereditary"
        elif reform_type == "outreach_expansion":
            movement.recruitment_success = min(1.0, movement.recruitment_success + 0.1)
        
        # Record reform
        reform_record = {
            "type": reform_type,
            "leader": reform_leader.name,
            "day": current_day,
            "description": f"{reform_type.replace('_', ' ').title()} implemented"
        }
        movement.reforms.append(reform_record)
        
        return {
            "type": "movement_reform",
            "movement": movement.name,
            "reform_type": reform_type,
            "reform_leader": reform_leader.name,
            "day": current_day
        }
    
    def _check_movement_achievements(self, movement: CulturalMovement, agents: List[Any], 
                                   current_day: int) -> List[Dict[str, Any]]:
        """Check for movement achievements."""
        events = []
        
        # Achievement: Reach certain membership milestones
        member_count = len(movement.believers)
        milestone_achievements = [10, 25, 50, 100]
        
        for milestone in milestone_achievements:
            if (member_count >= milestone and 
                not any(ach.get("type") == "membership_milestone" and ach.get("milestone") == milestone 
                       for ach in movement.achievements)):
                
                achievement = {
                    "type": "membership_milestone",
                    "milestone": milestone,
                    "day": current_day,
                    "description": f"Reached {milestone} believers"
                }
                movement.achievements.append(achievement)
                
                events.append({
                    "type": "movement_achievement",
                    "movement": movement.name,
                    "achievement": "membership_milestone",
                    "milestone": milestone,
                    "day": current_day
                })
        
        # Achievement: Geographic spread
        if (movement.influence_radius > 0.5 and 
            not any(ach.get("type") == "geographic_spread" for ach in movement.achievements)):
            
            achievement = {
                "type": "geographic_spread",
                "day": current_day,
                "description": "Spread across multiple regions"
            }
            movement.achievements.append(achievement)
            
            events.append({
                "type": "movement_achievement",
                "movement": movement.name,
                "achievement": "geographic_spread",
                "day": current_day
            })
        
        return events
    
    def _process_cultural_conflicts(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process conflicts between different cultural movements."""
        events = []
        
        # Check for conflicts between movements
        movement_pairs = []
        movement_list = list(self.movements.values())
        
        for i, movement1 in enumerate(movement_list):
            for movement2 in movement_list[i+1:]:
                conflict_probability = self._calculate_conflict_probability(movement1, movement2)
                
                if conflict_probability > 0.3 and random.random() < conflict_probability * 0.1:
                    conflict_event = self._create_cultural_conflict(movement1, movement2, agents, current_day)
                    if conflict_event:
                        events.append(conflict_event)
        
        # Process existing conflicts
        for conflict_id, conflict in list(self.cultural_conflicts.items()):
            conflict_events = self._process_existing_conflict(conflict, agents, current_day)
            events.extend(conflict_events)
        
        return events
    
    def _calculate_conflict_probability(self, movement1: CulturalMovement, 
                                      movement2: CulturalMovement) -> float:
        """Calculate probability of conflict between two movements."""
        conflict_factors = []
        
        # Same type movements more likely to conflict
        if movement1.movement_type == movement2.movement_type:
            conflict_factors.append(0.4)
        
        # Overlapping influence areas
        if movement1.founding_location == movement2.founding_location:
            conflict_factors.append(0.3)
        
        # Competing belief systems
        belief_overlap = len(movement1.core_beliefs & movement2.core_beliefs)
        if belief_overlap > 0:
            conflict_factors.append(0.2 * belief_overlap)
        
        # High intensity believers more likely to create conflict
        zealous_count = (len([i for i in movement1.believers.values() if i == BeliefIntensity.ZEALOUS]) +
                        len([i for i in movement2.believers.values() if i == BeliefIntensity.ZEALOUS]))
        if zealous_count > 0:
            conflict_factors.append(0.1 * zealous_count)
        
        return min(1.0, sum(conflict_factors)) if conflict_factors else 0.0
    
    def _create_cultural_conflict(self, movement1: CulturalMovement, movement2: CulturalMovement,
                                agents: List[Any], current_day: int) -> Optional[Dict[str, Any]]:
        """Create a new cultural conflict between movements."""
        conflict_id = f"conflict_{movement1.id}_{movement2.id}_{current_day}"
        
        # Determine type of conflict
        conflict_types = ["ideological_dispute", "territorial_competition", "resource_conflict", 
                         "authority_challenge", "doctrinal_disagreement"]
        conflict_type = random.choice(conflict_types)
        
        # Find affected population
        affected_agents = set()
        for agent in agents:
            if (agent.is_alive and 
                (agent.name in movement1.believers or agent.name in movement2.believers or
                 agent.name in movement1.sympathizers or agent.name in movement2.sympathizers)):
                affected_agents.add(agent.name)
        
        # Create conflict
        conflict = CulturalConflict(
            id=conflict_id,
            conflicting_movements=[movement1.id, movement2.id],
            conflict_type=conflict_type,
            intensity=random.uniform(0.3, 0.8),
            started_day=current_day,
            
            core_disagreements=[f"{conflict_type.replace('_', ' ')}", "fundamental_beliefs"],
            contested_resources=["followers", "influence", "territory"],
            territorial_disputes=[movement1.founding_location, movement2.founding_location],
            
            mediation_attempts=[],
            compromises_offered=[],
            resolution_status="ongoing",
            
            affected_population=affected_agents,
            social_disruption=random.uniform(0.2, 0.6),
            violence_level=random.uniform(0.0, 0.3)
        )
        
        self.cultural_conflicts[conflict_id] = conflict
        
        # Record conflict in movements
        conflict_record = {
            "opponent": movement2.name,
            "type": conflict_type,
            "started": current_day,
            "status": "ongoing"
        }
        movement1.conflicts.append(conflict_record)
        
        conflict_record2 = {
            "opponent": movement1.name,
            "type": conflict_type,
            "started": current_day,
            "status": "ongoing"
        }
        movement2.conflicts.append(conflict_record2)
        
        return {
            "type": "cultural_conflict_start",
            "movements": [movement1.name, movement2.name],
            "conflict_type": conflict_type,
            "intensity": conflict.intensity,
            "affected_population": len(affected_agents),
            "day": current_day
        }
    
    def _process_existing_conflict(self, conflict: CulturalConflict, agents: List[Any], 
                                 current_day: int) -> List[Dict[str, Any]]:
        """Process an ongoing cultural conflict."""
        events = []
        
        # Conflict may escalate or de-escalate
        escalation_chance = 0.05 if conflict.intensity < 0.8 else 0.0
        deescalation_chance = 0.1 if conflict.intensity > 0.3 else 0.0
        
        if random.random() < escalation_chance:
            conflict.intensity = min(1.0, conflict.intensity + random.uniform(0.1, 0.3))
            events.append({
                "type": "conflict_escalation",
                "conflict_id": conflict.id,
                "new_intensity": conflict.intensity,
                "day": current_day
            })
        
        elif random.random() < deescalation_chance:
            conflict.intensity = max(0.1, conflict.intensity - random.uniform(0.1, 0.2))
            events.append({
                "type": "conflict_deescalation",
                "conflict_id": conflict.id,
                "new_intensity": conflict.intensity,
                "day": current_day
            })
        
        # Check for resolution
        if conflict.intensity < 0.2 or random.random() < 0.02:  # 2% chance of resolution
            conflict.resolution_status = "resolved"
            events.append({
                "type": "conflict_resolution",
                "conflict_id": conflict.id,
                "resolution_method": "natural_cooling",
                "day": current_day
            })
        
        return events
    
    def _update_cultural_zeitgeist(self, agents: List[Any], current_day: int) -> None:
        """Update the overall cultural zeitgeist/mood of the time."""
        zeitgeist = {
            "dominant_movements": [],
            "emerging_ideas": [],
            "cultural_tensions": [],
            "popular_beliefs": [],
            "generational_differences": {},
            "day": current_day
        }
        
        # Find dominant movements
        for movement in self.movements.values():
            if movement.stage in [MovementStage.DOMINANT, MovementStage.ESTABLISHED]:
                zeitgeist["dominant_movements"].append({
                    "name": movement.name,
                    "type": movement.movement_type.value,
                    "influence": movement.cultural_influence
                })
        
        # Find emerging movements
        for movement in self.movements.values():
            if movement.stage == MovementStage.EMERGING:
                zeitgeist["emerging_ideas"].append({
                    "name": movement.name,
                    "type": movement.movement_type.value,
                    "narrative": movement.central_narrative
                })
        
        # Identify cultural tensions from conflicts
        for conflict in self.cultural_conflicts.values():
            if conflict.resolution_status == "ongoing":
                zeitgeist["cultural_tensions"].append({
                    "type": conflict.conflict_type,
                    "intensity": conflict.intensity,
                    "affected_population": len(conflict.affected_population)
                })
        
        # Most popular beliefs
        belief_popularity = defaultdict(int)
        for movement in self.movements.values():
            for belief_id in movement.core_beliefs:
                belief_popularity[belief_id] += len(movement.believers)
        
        top_beliefs = sorted(belief_popularity.items(), key=lambda x: x[1], reverse=True)[:3]
        for belief_id, popularity in top_beliefs:
            if belief_id in self.cultural_beliefs:
                zeitgeist["popular_beliefs"].append({
                    "name": self.cultural_beliefs[belief_id].name,
                    "popularity": popularity
                })
        
        self.cultural_zeitgeist[current_day] = zeitgeist
    
    def _process_institutional_interactions(self, agents: List[Any], groups: Dict[str, Any], 
                                          current_day: int) -> List[Dict[str, Any]]:
        """Process interactions between cultural movements and institutions."""
        events = []
        
        # This would integrate with the social institutions system
        # For now, simulate basic interactions
        
        for movement in self.movements.values():
            if movement.stage in [MovementStage.ESTABLISHED, MovementStage.DOMINANT]:
                # Check for institutional adoption
                if random.random() < 0.05:  # 5% chance
                    events.append({
                        "type": "institutional_adoption",
                        "movement": movement.name,
                        "institution_type": "cultural_institution",
                        "description": f"{movement.name} principles adopted by local institution",
                        "day": current_day
                    })
                    
                    movement.political_influence = min(1.0, movement.political_influence + 0.1)
        
        return events
    
    def get_cultural_movements_summary(self) -> Dict[str, Any]:
        """Get comprehensive cultural movements summary."""
        summary = {
            "total_movements": len(self.movements),
            "movements_by_type": {},
            "movements_by_stage": {},
            "total_believers": 0,
            "cultural_beliefs": len(self.cultural_beliefs),
            "active_conflicts": len([c for c in self.cultural_conflicts.values() 
                                   if c.resolution_status == "ongoing"]),
            "dominant_movements": [],
            "cultural_diversity": 0.0
        }
        
        # Count by type and stage
        for movement in self.movements.values():
            mov_type = movement.movement_type.value
            summary["movements_by_type"][mov_type] = summary["movements_by_type"].get(mov_type, 0) + 1
            
            stage = movement.stage.value
            summary["movements_by_stage"][stage] = summary["movements_by_stage"].get(stage, 0) + 1
            
            summary["total_believers"] += len(movement.believers)
            
            if movement.stage in [MovementStage.DOMINANT, MovementStage.ESTABLISHED]:
                summary["dominant_movements"].append({
                    "name": movement.name,
                    "type": mov_type,
                    "believers": len(movement.believers),
                    "influence": movement.cultural_influence
                })
        
        # Cultural diversity based on number of different movement types and belief systems
        diversity_factors = [
            len(summary["movements_by_type"]) / 6.0,  # Movement type variety
            len(self.cultural_beliefs) / 20.0,        # Belief variety
            min(1.0, len(self.movements) / 10.0)      # Total movements
        ]
        summary["cultural_diversity"] = sum(diversity_factors) / len(diversity_factors)
        
        return summary 