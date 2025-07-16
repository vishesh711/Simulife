"""
Crisis Response System for SimuLife
Handles how societies collectively adapt to challenges and disasters through
institutional responses, community mobilization, and resilience building.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import math


class CrisisType(Enum):
    """Types of crises that can affect society."""
    NATURAL_DISASTER = "natural_disaster"       # Environmental catastrophes
    RESOURCE_SCARCITY = "resource_scarcity"     # Shortages of essential resources
    EPIDEMIC = "epidemic"                       # Disease outbreaks
    CONFLICT = "conflict"                       # Wars and violent disputes
    ECONOMIC_COLLAPSE = "economic_collapse"     # Economic system failures
    SOCIAL_UNREST = "social_unrest"            # Civil disorder and rebellion
    TECHNOLOGICAL_FAILURE = "technological_failure"  # Tech system breakdowns
    LEADERSHIP_CRISIS = "leadership_crisis"     # Governance failures
    ENVIRONMENTAL_DEGRADATION = "environmental_degradation"  # Ecological damage
    POPULATION_PRESSURE = "population_pressure" # Overpopulation stress


class CrisisSeverity(Enum):
    """Severity levels of crises."""
    MINOR = "minor"                    # Limited local impact
    MODERATE = "moderate"              # Significant community impact
    MAJOR = "major"                    # Widespread regional impact
    CATASTROPHIC = "catastrophic"      # Civilization-threatening impact


class ResponsePhase(Enum):
    """Phases of crisis response."""
    DETECTION = "detection"            # Becoming aware of the crisis
    MOBILIZATION = "mobilization"      # Organizing response efforts
    RESPONSE = "response"              # Active crisis management
    RECOVERY = "recovery"              # Rebuilding and restoration
    ADAPTATION = "adaptation"          # Learning and resilience building


class ResponseStrategy(Enum):
    """Types of response strategies."""
    EVACUATION = "evacuation"                  # Moving people to safety
    RESOURCE_SHARING = "resource_sharing"      # Pooling community resources
    INNOVATION = "innovation"                  # Developing new solutions
    EXTERNAL_AID = "external_aid"              # Seeking help from outside
    COLLECTIVE_ACTION = "collective_action"    # Coordinated community effort
    INSTITUTIONAL_RESPONSE = "institutional_response"  # Government/org action
    ADAPTATION = "adaptation"                  # Changing practices/lifestyle
    RESISTANCE = "resistance"                  # Fighting against the crisis


class ResponseEffectiveness(Enum):
    """Effectiveness levels of responses."""
    FAILED = "failed"                  # Response made things worse
    INEFFECTIVE = "ineffective"        # Response had little impact
    PARTIALLY_EFFECTIVE = "partially_effective"  # Response helped somewhat
    EFFECTIVE = "effective"            # Response successfully addressed crisis
    HIGHLY_EFFECTIVE = "highly_effective"  # Response exceeded expectations


@dataclass
class SocietalCrisis:
    """Represents a crisis affecting society."""
    id: str
    name: str
    crisis_type: CrisisType
    severity: CrisisSeverity
    started_day: int
    
    # Crisis characteristics
    affected_locations: Set[str]       # Geographic impact
    affected_population: Set[str]      # Agents directly affected
    secondary_effects: List[str]       # Indirect consequences
    duration_estimate: int             # Expected duration in days
    
    # Crisis dynamics
    current_phase: ResponsePhase
    intensity_over_time: List[Tuple[int, float]]  # Day, intensity
    peak_intensity: float              # Maximum crisis intensity (0.0-1.0)
    resolution_probability: float      # Chance of natural resolution per day
    
    # Response tracking
    active_responses: Dict[str, Dict[str, Any]]  # Response ID -> details
    coordinating_institutions: Set[str] # Organizations leading response
    community_mobilization: float      # 0.0-1.0 level of community engagement
    
    # Impact and consequences
    casualties: int                     # Agents seriously affected
    resource_losses: Dict[str, float]  # Resources lost or consumed
    social_disruption: float           # Impact on normal activities
    long_term_effects: List[str]       # Lasting consequences
    
    # Resolution
    resolved_day: Optional[int]
    resolution_method: Optional[str]
    lessons_learned: List[str]


@dataclass
class CrisisResponse:
    """Represents a response effort to a crisis."""
    id: str
    crisis_id: str
    response_strategy: ResponseStrategy
    started_day: int
    
    # Response organization
    lead_agents: Set[str]              # Agents coordinating response
    participating_agents: Set[str]     # All agents involved
    coordinating_institutions: Set[str] # Institutions organizing response
    resource_allocation: Dict[str, float]  # Resources dedicated
    
    # Response execution
    implementation_phase: ResponsePhase
    effectiveness: ResponseEffectiveness
    completion_percentage: float       # 0.0-1.0 how complete the response is
    
    # Outcomes and impact
    crisis_impact_reduction: float     # How much it reduced crisis severity
    unintended_consequences: List[str] # Negative side effects
    success_factors: List[str]         # What made it work
    failure_factors: List[str]         # What hindered it
    
    # Learning and adaptation
    innovations_created: List[str]     # New methods/tools developed
    social_bonds_formed: List[Tuple[str, str]]  # New relationships
    institutional_changes: List[str]   # Changes to organizations
    
    # Legacy
    finished_day: Optional[int]
    long_term_impact: Dict[str, float] # Lasting effects on society


@dataclass
class ResilienceCapacity:
    """Represents society's capacity to handle crises."""
    location: str
    
    # Preparedness factors
    early_warning_systems: float      # 0.0-1.0 ability to detect crises early
    resource_reserves: Dict[str, float]  # Stockpiled resources for emergencies
    institutional_capacity: float     # How well institutions can respond
    social_cohesion: float            # Community cooperation levels
    
    # Response capabilities
    leadership_quality: float         # Quality of crisis leadership
    coordination_ability: float       # Ability to organize collective action
    innovation_capacity: float        # Ability to develop new solutions
    external_connections: float       # Access to outside help
    
    # Adaptive capacity
    learning_capability: float        # Ability to learn from past crises
    flexibility: float                # Ability to change practices
    diversity: float                  # Variety of skills and resources
    redundancy: float                 # Backup systems and alternatives
    
    # Historical experience
    crisis_experience: Dict[CrisisType, int]  # Number of past crises handled
    successful_responses: int          # Number of successful past responses
    failed_responses: int             # Number of failed past responses


class CrisisResponseSystem:
    """
    Manages societal responses to crises through collective action,
    institutional coordination, and resilience building.
    """
    
    def __init__(self):
        self.active_crises: Dict[str, SocietalCrisis] = {}
        self.crisis_responses: Dict[str, CrisisResponse] = {}
        self.resilience_capacities: Dict[str, ResilienceCapacity] = {}
        
        # Historical tracking
        self.crisis_history: List[Dict[str, Any]] = []
        self.response_events: List[Dict[str, Any]] = []
        self.lessons_learned: Dict[str, List[str]] = defaultdict(list)
        
        # System configuration
        self.crisis_detection_thresholds = self._initialize_detection_thresholds()
        self.response_strategies = self._initialize_response_strategies()
        self.effectiveness_factors = self._initialize_effectiveness_factors()
        
        # Community resilience tracking
        self.community_preparedness: Dict[str, float] = defaultdict(float)
        self.institutional_memory: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    
    def _initialize_detection_thresholds(self) -> Dict[str, Dict[str, Any]]:
        """Initialize thresholds for detecting different crisis types."""
        return {
            "natural_disaster": {
                "environmental_indicators": 0.7,
                "resource_disruption": 0.5,
                "population_displacement": 0.3,
                "detection_delay": 1  # Days to detect after onset
            },
            "resource_scarcity": {
                "resource_levels": 0.3,  # Below 30% of normal
                "demand_pressure": 0.8,
                "price_volatility": 0.6,
                "detection_delay": 3
            },
            "epidemic": {
                "illness_rate": 0.2,    # 20% of population affected
                "spread_rate": 0.1,     # 10% increase per day
                "mortality_rate": 0.05, # 5% death rate
                "detection_delay": 5
            },
            "conflict": {
                "violence_level": 0.4,
                "social_tension": 0.7,
                "institutional_breakdown": 0.5,
                "detection_delay": 2
            },
            "economic_collapse": {
                "trade_disruption": 0.6,
                "currency_instability": 0.8,
                "unemployment": 0.4,
                "detection_delay": 7
            },
            "social_unrest": {
                "dissatisfaction": 0.7,
                "protest_activity": 0.5,
                "authority_legitimacy": 0.3,
                "detection_delay": 3
            },
            "leadership_crisis": {
                "governance_effectiveness": 0.2,
                "public_confidence": 0.3,
                "institutional_dysfunction": 0.6,
                "detection_delay": 10
            },
            "population_pressure": {
                "carrying_capacity_ratio": 1.2,  # 120% of capacity
                "resource_competition": 0.8,
                "migration_pressure": 0.6,
                "detection_delay": 14
            }
        }
    
    def _initialize_response_strategies(self) -> Dict[ResponseStrategy, Dict[str, Any]]:
        """Initialize response strategy templates."""
        return {
            ResponseStrategy.EVACUATION: {
                "applicable_crises": [CrisisType.NATURAL_DISASTER, CrisisType.EPIDEMIC, CrisisType.CONFLICT],
                "resource_requirements": {"organization": 0.7, "transportation": 0.8, "communication": 0.6},
                "effectiveness_factors": ["early_warning", "coordination", "destination_capacity"],
                "typical_duration": 7,
                "population_impact": 0.9
            },
            ResponseStrategy.RESOURCE_SHARING: {
                "applicable_crises": [CrisisType.RESOURCE_SCARCITY, CrisisType.NATURAL_DISASTER, CrisisType.ECONOMIC_COLLAPSE],
                "resource_requirements": {"social_cohesion": 0.6, "communication": 0.5, "leadership": 0.4},
                "effectiveness_factors": ["community_trust", "resource_availability", "fair_distribution"],
                "typical_duration": 30,
                "population_impact": 0.7
            },
            ResponseStrategy.INNOVATION: {
                "applicable_crises": [CrisisType.TECHNOLOGICAL_FAILURE, CrisisType.ENVIRONMENTAL_DEGRADATION, CrisisType.RESOURCE_SCARCITY],
                "resource_requirements": {"knowledge": 0.8, "creativity": 0.7, "experimentation": 0.6},
                "effectiveness_factors": ["expertise", "resources_for_research", "trial_and_error"],
                "typical_duration": 60,
                "population_impact": 0.4
            },
            ResponseStrategy.EXTERNAL_AID: {
                "applicable_crises": [CrisisType.NATURAL_DISASTER, CrisisType.EPIDEMIC, CrisisType.ECONOMIC_COLLAPSE],
                "resource_requirements": {"communication": 0.8, "diplomacy": 0.6, "transportation": 0.5},
                "effectiveness_factors": ["external_relationships", "communication_ability", "aid_availability"],
                "typical_duration": 14,
                "population_impact": 0.6
            },
            ResponseStrategy.COLLECTIVE_ACTION: {
                "applicable_crises": [CrisisType.SOCIAL_UNREST, CrisisType.RESOURCE_SCARCITY, CrisisType.ENVIRONMENTAL_DEGRADATION],
                "resource_requirements": {"social_cohesion": 0.8, "leadership": 0.7, "communication": 0.6},
                "effectiveness_factors": ["unity", "clear_goals", "sustained_participation"],
                "typical_duration": 45,
                "population_impact": 0.8
            },
            ResponseStrategy.INSTITUTIONAL_RESPONSE: {
                "applicable_crises": [CrisisType.LEADERSHIP_CRISIS, CrisisType.ECONOMIC_COLLAPSE, CrisisType.SOCIAL_UNREST],
                "resource_requirements": {"institutional_capacity": 0.8, "legitimacy": 0.6, "resources": 0.7},
                "effectiveness_factors": ["institutional_strength", "public_support", "resource_access"],
                "typical_duration": 90,
                "population_impact": 0.5
            },
            ResponseStrategy.ADAPTATION: {
                "applicable_crises": [CrisisType.ENVIRONMENTAL_DEGRADATION, CrisisType.POPULATION_PRESSURE, CrisisType.TECHNOLOGICAL_FAILURE],
                "resource_requirements": {"flexibility": 0.7, "learning_capacity": 0.8, "innovation": 0.6},
                "effectiveness_factors": ["adaptability", "long_term_thinking", "cultural_flexibility"],
                "typical_duration": 180,
                "population_impact": 0.3
            },
            ResponseStrategy.RESISTANCE: {
                "applicable_crises": [CrisisType.CONFLICT, CrisisType.SOCIAL_UNREST, CrisisType.LEADERSHIP_CRISIS],
                "resource_requirements": {"organization": 0.8, "commitment": 0.9, "resources": 0.6},
                "effectiveness_factors": ["unity", "determination", "strategic_planning"],
                "typical_duration": 120,
                "population_impact": 0.9
            }
        }
    
    def _initialize_effectiveness_factors(self) -> Dict[str, Dict[str, float]]:
        """Initialize factors that affect response effectiveness."""
        return {
            "early_detection": {"effectiveness_multiplier": 1.5, "resource_efficiency": 1.3},
            "strong_leadership": {"effectiveness_multiplier": 1.4, "coordination_bonus": 1.5},
            "high_social_cohesion": {"effectiveness_multiplier": 1.3, "participation_bonus": 1.4},
            "adequate_resources": {"effectiveness_multiplier": 1.6, "sustainability_bonus": 1.2},
            "past_experience": {"effectiveness_multiplier": 1.2, "learning_bonus": 1.3},
            "institutional_capacity": {"effectiveness_multiplier": 1.3, "coordination_bonus": 1.2},
            "external_support": {"effectiveness_multiplier": 1.2, "resource_bonus": 1.4},
            "innovation_capability": {"effectiveness_multiplier": 1.4, "adaptation_bonus": 1.5}
        }
    
    def process_daily_crisis_response(self, agents: List[Any], institutions: Dict[str, Any],
                                    groups: Dict[str, Any], world_events: List[Dict[str, Any]],
                                    world_state: Any, current_day: int) -> List[Dict[str, Any]]:
        """Process daily crisis response activities."""
        events = []
        
        # Step 1: Detect new crises
        detection_events = self._detect_new_crises(agents, institutions, world_events, world_state, current_day)
        events.extend(detection_events)
        
        # Step 2: Update existing crisis progression
        progression_events = self._update_crisis_progression(agents, current_day)
        events.extend(progression_events)
        
        # Step 3: Initiate and coordinate responses
        response_events = self._coordinate_crisis_responses(agents, institutions, groups, current_day)
        events.extend(response_events)
        
        # Step 4: Update response effectiveness
        effectiveness_events = self._update_response_effectiveness(agents, current_day)
        events.extend(effectiveness_events)
        
        # Step 5: Process recovery and adaptation
        recovery_events = self._process_recovery_and_adaptation(agents, institutions, current_day)
        events.extend(recovery_events)
        
        # Step 6: Update resilience capacities
        resilience_events = self._update_resilience_capacities(agents, institutions, current_day)
        events.extend(resilience_events)
        
        # Step 7: Learn from completed crises
        learning_events = self._process_crisis_learning(current_day)
        events.extend(learning_events)
        
        return events
    
    def _detect_new_crises(self, agents: List[Any], institutions: Dict[str, Any],
                          world_events: List[Dict[str, Any]], world_state: Any,
                          current_day: int) -> List[Dict[str, Any]]:
        """Detect new crises based on current conditions."""
        events = []
        
        # Analyze current conditions for crisis indicators
        crisis_indicators = self._analyze_crisis_indicators(agents, institutions, world_events, world_state)
        
        for crisis_type, indicators in crisis_indicators.items():
            threshold_config = self.crisis_detection_thresholds.get(crisis_type, {})
            
            # Check if indicators exceed thresholds
            if self._crisis_threshold_exceeded(indicators, threshold_config):
                # Detect new crisis
                crisis = self._create_new_crisis(crisis_type, indicators, agents, current_day)
                if crisis:
                    self.active_crises[crisis.id] = crisis
                    
                    events.append({
                        "type": "crisis_detected",
                        "crisis_id": crisis.id,
                        "crisis_name": crisis.name,
                        "crisis_type": crisis_type,
                        "severity": crisis.severity.value,
                        "affected_locations": list(crisis.affected_locations),
                        "affected_population": len(crisis.affected_population),
                        "day": current_day
                    })
                    
                    # Add crisis awareness to affected agents
                    self._add_crisis_awareness(crisis, agents)
        
        return events
    
    def _analyze_crisis_indicators(self, agents: List[Any], institutions: Dict[str, Any],
                                 world_events: List[Dict[str, Any]], world_state: Any) -> Dict[str, Dict[str, float]]:
        """Analyze current conditions for crisis indicators."""
        indicators = {}
        
        # Natural disaster indicators
        indicators["natural_disaster"] = {
            "environmental_indicators": self._analyze_environmental_stress(world_events, world_state),
            "resource_disruption": self._analyze_resource_disruption(agents, world_state),
            "population_displacement": self._analyze_population_displacement(agents)
        }
        
        # Resource scarcity indicators
        indicators["resource_scarcity"] = {
            "resource_levels": self._analyze_resource_levels(world_state),
            "demand_pressure": self._analyze_resource_demand(agents),
            "price_volatility": self._analyze_economic_volatility(world_events)
        }
        
        # Epidemic indicators
        indicators["epidemic"] = {
            "illness_rate": self._analyze_illness_rate(agents),
            "spread_rate": self._analyze_disease_spread(agents),
            "mortality_rate": self._analyze_mortality_rate(agents)
        }
        
        # Conflict indicators
        indicators["conflict"] = {
            "violence_level": self._analyze_violence_level(agents, world_events),
            "social_tension": self._analyze_social_tension(agents),
            "institutional_breakdown": self._analyze_institutional_breakdown(institutions)
        }
        
        # Economic collapse indicators
        indicators["economic_collapse"] = {
            "trade_disruption": self._analyze_trade_disruption(world_events),
            "currency_instability": self._analyze_currency_instability(world_events),
            "unemployment": self._analyze_economic_distress(agents)
        }
        
        # Social unrest indicators
        indicators["social_unrest"] = {
            "dissatisfaction": self._analyze_public_dissatisfaction(agents),
            "protest_activity": self._analyze_protest_activity(world_events),
            "authority_legitimacy": self._analyze_authority_legitimacy(institutions)
        }
        
        # Leadership crisis indicators
        indicators["leadership_crisis"] = {
            "governance_effectiveness": self._analyze_governance_effectiveness(institutions),
            "public_confidence": self._analyze_public_confidence(agents, institutions),
            "institutional_dysfunction": self._analyze_institutional_dysfunction(institutions)
        }
        
        # Population pressure indicators
        indicators["population_pressure"] = {
            "carrying_capacity_ratio": self._analyze_carrying_capacity_ratio(agents, world_state),
            "resource_competition": self._analyze_resource_competition(agents),
            "migration_pressure": self._analyze_migration_pressure(agents)
        }
        
        return indicators
    
    def _analyze_environmental_stress(self, world_events: List[Dict[str, Any]], world_state: Any) -> float:
        """Analyze environmental stress indicators."""
        # Count recent environmental events
        environmental_events = [e for e in world_events if 
                               e.get("type", "") in ["natural_disaster", "climate_change", "environmental_degradation"]]
        
        return min(1.0, len(environmental_events) / 5.0)  # Scale to 0-1
    
    def _analyze_resource_disruption(self, agents: List[Any], world_state: Any) -> float:
        """Analyze resource availability disruption."""
        # This would integrate with resource system to check scarcity
        # For now, simulate based on agent needs vs availability
        total_needs = len([a for a in agents if a.is_alive])
        # Simplified resource availability check
        return max(0.0, min(1.0, (total_needs - 20) / 20.0))  # Crisis if >20 agents
    
    def _analyze_population_displacement(self, agents: List[Any]) -> float:
        """Analyze population displacement levels."""
        # Count agents who have moved recently (would integrate with migration system)
        recent_movers = len([a for a in agents if a.is_alive and random.random() < 0.1])  # Simulate 10% mobility
        total_population = len([a for a in agents if a.is_alive])
        
        return recent_movers / max(1, total_population)
    
    def _analyze_resource_levels(self, world_state: Any) -> float:
        """Analyze overall resource availability."""
        # This would integrate with resource system
        # Simulate resource scarcity
        return random.uniform(0.2, 0.8)  # Placeholder
    
    def _analyze_resource_demand(self, agents: List[Any]) -> float:
        """Analyze resource demand pressure."""
        population_pressure = len([a for a in agents if a.is_alive]) / 30.0  # Pressure above 30 agents
        return min(1.0, population_pressure)
    
    def _analyze_economic_volatility(self, world_events: List[Dict[str, Any]]) -> float:
        """Analyze economic volatility indicators."""
        economic_events = [e for e in world_events if "economic" in e.get("type", "").lower()]
        return min(1.0, len(economic_events) / 3.0)
    
    def _analyze_illness_rate(self, agents: List[Any]) -> float:
        """Analyze illness rates in population."""
        # Count agents with health issues
        sick_agents = len([a for a in agents if a.is_alive and hasattr(a, 'health') and a.health < 0.7])
        total_population = len([a for a in agents if a.is_alive])
        
        return sick_agents / max(1, total_population)
    
    def _analyze_disease_spread(self, agents: List[Any]) -> float:
        """Analyze disease spread rate."""
        # Simulate disease spread based on population density and health
        return random.uniform(0.0, 0.3)  # Placeholder
    
    def _analyze_mortality_rate(self, agents: List[Any]) -> float:
        """Analyze mortality rate."""
        dead_agents = len([a for a in agents if not a.is_alive])
        total_agents = len(agents)
        
        return dead_agents / max(1, total_agents)
    
    def _analyze_violence_level(self, agents: List[Any], world_events: List[Dict[str, Any]]) -> float:
        """Analyze violence and conflict levels."""
        violence_events = [e for e in world_events if "conflict" in e.get("type", "").lower()]
        return min(1.0, len(violence_events) / 5.0)
    
    def _analyze_social_tension(self, agents: List[Any]) -> float:
        """Analyze social tension levels."""
        # Count recent conflicts in agent memories
        conflict_count = 0
        for agent in agents:
            if hasattr(agent, 'memory') and agent.is_alive:
                conflicts = agent.memory.get_memories_by_type("conflict", limit=3)
                conflict_count += len(conflicts)
        
        return min(1.0, conflict_count / max(1, len([a for a in agents if a.is_alive]) * 2))
    
    def _analyze_institutional_breakdown(self, institutions: Dict[str, Any]) -> float:
        """Analyze institutional effectiveness breakdown."""
        if not institutions:
            return 1.0  # Complete breakdown if no institutions
        
        # Check institution effectiveness
        total_effectiveness = 0.0
        for institution in institutions.values():
            if hasattr(institution, 'effectiveness'):
                total_effectiveness += institution.effectiveness
        
        avg_effectiveness = total_effectiveness / len(institutions)
        return 1.0 - avg_effectiveness  # Higher breakdown = lower effectiveness
    
    def _analyze_trade_disruption(self, world_events: List[Dict[str, Any]]) -> float:
        """Analyze trade and economic disruption."""
        trade_events = [e for e in world_events if "trade" in e.get("type", "").lower()]
        disruption_events = [e for e in trade_events if "disruption" in e.get("type", "").lower()]
        
        return len(disruption_events) / max(1, len(trade_events))
    
    def _analyze_currency_instability(self, world_events: List[Dict[str, Any]]) -> float:
        """Analyze currency and financial instability."""
        financial_events = [e for e in world_events if "currency" in e.get("type", "").lower() or 
                           "financial" in e.get("type", "").lower()]
        return min(1.0, len(financial_events) / 3.0)
    
    def _analyze_economic_distress(self, agents: List[Any]) -> float:
        """Analyze economic distress levels."""
        # Count agents with low resources/wealth
        distressed_agents = len([a for a in agents if a.is_alive and 
                               hasattr(a, 'resources') and 
                               sum(a.resources.values()) < 2.0])  # Low resource threshold
        total_population = len([a for a in agents if a.is_alive])
        
        return distressed_agents / max(1, total_population)
    
    def _analyze_public_dissatisfaction(self, agents: List[Any]) -> float:
        """Analyze public dissatisfaction levels."""
        # Count agents with low satisfaction/happiness
        dissatisfied_agents = len([a for a in agents if a.is_alive and 
                                 hasattr(a, 'happiness') and a.happiness < 0.4])
        total_population = len([a for a in agents if a.is_alive])
        
        return dissatisfied_agents / max(1, total_population)
    
    def _analyze_protest_activity(self, world_events: List[Dict[str, Any]]) -> float:
        """Analyze protest and demonstration activity."""
        protest_events = [e for e in world_events if "protest" in e.get("type", "").lower() or
                         "demonstration" in e.get("type", "").lower()]
        return min(1.0, len(protest_events) / 3.0)
    
    def _analyze_authority_legitimacy(self, institutions: Dict[str, Any]) -> float:
        """Analyze legitimacy of governing authorities."""
        if not institutions:
            return 0.0  # No authority = no legitimacy
        
        # Check government institution legitimacy
        gov_institutions = [i for i in institutions.values() if 
                           hasattr(i, 'institution_type') and "government" in i.institution_type]
        
        if not gov_institutions:
            return 0.5  # Moderate legitimacy without formal government
        
        total_legitimacy = sum(getattr(i, 'legitimacy', 0.5) for i in gov_institutions)
        return total_legitimacy / len(gov_institutions)
    
    def _analyze_governance_effectiveness(self, institutions: Dict[str, Any]) -> float:
        """Analyze governance effectiveness."""
        gov_institutions = [i for i in institutions.values() if 
                           hasattr(i, 'institution_type') and "government" in i.institution_type]
        
        if not gov_institutions:
            return 0.2  # Low effectiveness without formal government
        
        total_effectiveness = sum(getattr(i, 'effectiveness', 0.3) for i in gov_institutions)
        return total_effectiveness / len(gov_institutions)
    
    def _analyze_public_confidence(self, agents: List[Any], institutions: Dict[str, Any]) -> float:
        """Analyze public confidence in institutions."""
        # This would check agent attitudes toward institutions
        # For now, simulate based on institution legitimacy
        if not institutions:
            return 0.3
        
        avg_legitimacy = sum(getattr(i, 'legitimacy', 0.5) for i in institutions.values()) / len(institutions)
        return avg_legitimacy
    
    def _analyze_institutional_dysfunction(self, institutions: Dict[str, Any]) -> float:
        """Analyze institutional dysfunction levels."""
        if not institutions:
            return 1.0  # Complete dysfunction
        
        total_effectiveness = sum(getattr(i, 'effectiveness', 0.3) for i in institutions.values())
        avg_effectiveness = total_effectiveness / len(institutions)
        
        return 1.0 - avg_effectiveness  # Higher dysfunction = lower effectiveness
    
    def _analyze_carrying_capacity_ratio(self, agents: List[Any], world_state: Any) -> float:
        """Analyze population vs carrying capacity ratio."""
        current_population = len([a for a in agents if a.is_alive])
        # Estimated carrying capacity based on available resources
        estimated_capacity = 25  # Placeholder capacity
        
        return current_population / estimated_capacity
    
    def _analyze_resource_competition(self, agents: List[Any]) -> float:
        """Analyze competition for resources."""
        # Count recent resource conflicts
        return random.uniform(0.0, 0.8)  # Placeholder
    
    def _analyze_migration_pressure(self, agents: List[Any]) -> float:
        """Analyze pressure for migration/movement."""
        # This would integrate with migration system
        return random.uniform(0.0, 0.6)  # Placeholder
    
    def _crisis_threshold_exceeded(self, indicators: Dict[str, float], 
                                 threshold_config: Dict[str, Any]) -> bool:
        """Check if crisis indicators exceed detection thresholds."""
        for indicator_name, threshold in threshold_config.items():
            if indicator_name == "detection_delay":
                continue
            
            current_value = indicators.get(indicator_name, 0.0)
            if isinstance(threshold, (int, float)):
                if current_value < threshold:
                    return False
            
        return True  # All thresholds exceeded
    
    def _create_new_crisis(self, crisis_type: str, indicators: Dict[str, float], 
                         agents: List[Any], current_day: int) -> Optional[SocietalCrisis]:
        """Create a new crisis object."""
        crisis_id = f"crisis_{crisis_type}_{current_day}"
        
        # Determine severity based on indicator strength
        avg_indicator = sum(indicators.values()) / len(indicators) if indicators else 0.5
        if avg_indicator > 0.8:
            severity = CrisisSeverity.CATASTROPHIC
        elif avg_indicator > 0.6:
            severity = CrisisSeverity.MAJOR
        elif avg_indicator > 0.4:
            severity = CrisisSeverity.MODERATE
        else:
            severity = CrisisSeverity.MINOR
        
        # Generate crisis name
        crisis_names = {
            "natural_disaster": "Environmental Catastrophe",
            "resource_scarcity": "Resource Crisis",
            "epidemic": "Disease Outbreak",
            "conflict": "Social Conflict",
            "economic_collapse": "Economic Crisis",
            "social_unrest": "Civil Unrest",
            "leadership_crisis": "Governance Crisis",
            "population_pressure": "Population Crisis"
        }
        
        crisis_name = crisis_names.get(crisis_type, "Unknown Crisis")
        
        # Determine affected areas and population
        affected_locations = set()
        affected_population = set()
        
        # All locations affected for major crises
        if severity in [CrisisSeverity.MAJOR, CrisisSeverity.CATASTROPHIC]:
            for agent in agents:
                if agent.is_alive:
                    affected_locations.add(agent.location)
                    affected_population.add(agent.name)
        else:
            # Select random subset for minor/moderate crises
            alive_agents = [a for a in agents if a.is_alive]
            num_affected = min(len(alive_agents), max(1, int(len(alive_agents) * avg_indicator)))
            affected_agents = random.sample(alive_agents, num_affected)
            
            for agent in affected_agents:
                affected_locations.add(agent.location)
                affected_population.add(agent.name)
        
        # Estimate duration based on crisis type and severity
        base_durations = {
            CrisisType.NATURAL_DISASTER: 7,
            CrisisType.RESOURCE_SCARCITY: 30,
            CrisisType.EPIDEMIC: 60,
            CrisisType.CONFLICT: 90,
            CrisisType.ECONOMIC_COLLAPSE: 120,
            CrisisType.SOCIAL_UNREST: 45,
            CrisisType.LEADERSHIP_CRISIS: 180,
            CrisisType.POPULATION_PRESSURE: 365
        }
        
        base_duration = base_durations.get(CrisisType(crisis_type), 30)
        severity_multiplier = {
            CrisisSeverity.MINOR: 0.5,
            CrisisSeverity.MODERATE: 1.0,
            CrisisSeverity.MAJOR: 1.5,
            CrisisSeverity.CATASTROPHIC: 2.0
        }
        
        duration = int(base_duration * severity_multiplier[severity])
        
        crisis = SocietalCrisis(
            id=crisis_id,
            name=crisis_name,
            crisis_type=CrisisType(crisis_type),
            severity=severity,
            started_day=current_day,
            
            affected_locations=affected_locations,
            affected_population=affected_population,
            secondary_effects=[],
            duration_estimate=duration,
            
            current_phase=ResponsePhase.DETECTION,
            intensity_over_time=[(current_day, avg_indicator)],
            peak_intensity=avg_indicator,
            resolution_probability=1.0 / duration,  # Daily resolution chance
            
            active_responses={},
            coordinating_institutions=set(),
            community_mobilization=0.0,
            
            casualties=0,
            resource_losses={},
            social_disruption=avg_indicator * 0.7,
            long_term_effects=[],
            
            resolved_day=None,
            resolution_method=None,
            lessons_learned=[]
        )
        
        return crisis
    
    def _add_crisis_awareness(self, crisis: SocietalCrisis, agents: List[Any]) -> None:
        """Add crisis awareness to affected agents."""
        for agent in agents:
            if agent.name in crisis.affected_population and agent.is_alive:
                agent.memory.store_memory(
                    f"Crisis detected: {crisis.name} affecting our community",
                    importance=0.8,
                    memory_type="crisis"
                )
    
    def _update_crisis_progression(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Update progression of existing crises."""
        events = []
        
        for crisis_id, crisis in list(self.active_crises.items()):
            # Update crisis intensity
            days_elapsed = current_day - crisis.started_day
            intensity_change = self._calculate_intensity_change(crisis, days_elapsed)
            
            # Update phase progression - only report every 3 days to reduce spam
            if current_day % 3 == 0:
                old_phase = crisis.current_phase
                new_phase = self._determine_crisis_phase(crisis, days_elapsed)
                
                if new_phase != old_phase:
                    crisis.current_phase = new_phase
                    events.append({
                        "type": "crisis_phase_change",
                        "crisis_id": crisis_id,
                        "crisis_name": crisis.name,
                        "old_phase": old_phase.value,
                        "new_phase": new_phase.value,
                        "day": current_day
                    })
            
            # Check for natural resolution
            if random.random() < crisis.resolution_probability:
                resolution_event = self._resolve_crisis(crisis, "natural_resolution", current_day)
                events.append(resolution_event)
                del self.active_crises[crisis_id]
            
            # Check for crisis escalation - reduce frequency and increase threshold
            elif intensity_change > 0.4 and current_day % 5 == 0:  # Major escalation only, check every 5 days
                events.append({
                    "type": "crisis_escalation",
                    "crisis_id": crisis_id,
                    "crisis_name": crisis.name,
                    "intensity_increase": intensity_change,
                    "day": current_day
                })
                
                # Update peak intensity
                crisis.peak_intensity = max(crisis.peak_intensity, 
                                          crisis.intensity_over_time[-1][1] + intensity_change)
        
        return events
    
    def _calculate_intensity_change(self, crisis: SocietalCrisis, days_elapsed: int) -> float:
        """Calculate change in crisis intensity."""
        # Most crises follow a pattern: rapid rise, peak, gradual decline
        duration_ratio = days_elapsed / max(1, crisis.duration_estimate)
        
        if duration_ratio < 0.2:  # Rising phase
            return random.uniform(0.0, 0.3)
        elif duration_ratio < 0.5:  # Peak phase
            return random.uniform(-0.1, 0.1)
        else:  # Declining phase
            return random.uniform(-0.3, 0.0)
    
    def _determine_crisis_phase(self, crisis: SocietalCrisis, days_elapsed: int) -> ResponsePhase:
        """Determine current phase of crisis response."""
        duration_ratio = days_elapsed / max(1, crisis.duration_estimate)
        
        if duration_ratio < 0.1:
            return ResponsePhase.DETECTION
        elif duration_ratio < 0.3:
            return ResponsePhase.MOBILIZATION
        elif duration_ratio < 0.7:
            return ResponsePhase.RESPONSE
        elif duration_ratio < 0.9:
            return ResponsePhase.RECOVERY
        else:
            return ResponsePhase.ADAPTATION
    
    def _coordinate_crisis_responses(self, agents: List[Any], institutions: Dict[str, Any],
                                   groups: Dict[str, Any], current_day: int) -> List[Dict[str, Any]]:
        """Coordinate response efforts to active crises."""
        events = []
        
        for crisis_id, crisis in self.active_crises.items():
            # Check if new responses should be initiated
            if crisis.current_phase in [ResponsePhase.DETECTION, ResponsePhase.MOBILIZATION]:
                response_events = self._initiate_crisis_responses(crisis, agents, institutions, groups, current_day)
                events.extend(response_events)
            
            # Update existing response coordination
            coordination_events = self._update_response_coordination(crisis, agents, institutions, current_day)
            events.extend(coordination_events)
        
        return events
    
    def _initiate_crisis_responses(self, crisis: SocietalCrisis, agents: List[Any],
                                 institutions: Dict[str, Any], groups: Dict[str, Any],
                                 current_day: int) -> List[Dict[str, Any]]:
        """Initiate new response efforts for a crisis."""
        events = []
        
        # Determine appropriate response strategies
        applicable_strategies = self._get_applicable_strategies(crisis)
        
        # Check community capacity for each strategy
        for strategy in applicable_strategies:
            if self._can_implement_strategy(strategy, crisis, agents, institutions):
                response = self._create_crisis_response(strategy, crisis, agents, institutions, current_day)
                if response:
                    self.crisis_responses[response.id] = response
                    crisis.active_responses[response.id] = {
                        "strategy": strategy.value,
                        "started_day": current_day,
                        "lead_agents": list(response.lead_agents)
                    }
                    
                    events.append({
                        "type": "crisis_response_initiated",
                        "crisis_id": crisis.id,
                        "response_id": response.id,
                        "strategy": strategy.value,
                        "lead_agents": list(response.lead_agents),
                        "participating_agents": len(response.participating_agents),
                        "day": current_day
                    })
                    
                    # Add response memories to participants
                    self._add_response_memories(response, agents, crisis)
        
        return events
    
    def _get_applicable_strategies(self, crisis: SocietalCrisis) -> List[ResponseStrategy]:
        """Get response strategies applicable to a crisis type."""
        applicable = []
        
        for strategy, config in self.response_strategies.items():
            if crisis.crisis_type in config["applicable_crises"]:
                applicable.append(strategy)
        
        return applicable
    
    def _can_implement_strategy(self, strategy: ResponseStrategy, crisis: SocietalCrisis,
                              agents: List[Any], institutions: Dict[str, Any]) -> bool:
        """Check if community can implement a response strategy."""
        strategy_config = self.response_strategies[strategy]
        requirements = strategy_config["resource_requirements"]
        
        # Check each requirement
        for requirement, threshold in requirements.items():
            current_capacity = self._assess_community_capacity(requirement, agents, institutions)
            if current_capacity < threshold:
                return False
        
        return True
    
    def _assess_community_capacity(self, capacity_type: str, agents: List[Any], 
                                 institutions: Dict[str, Any]) -> float:
        """Assess community capacity for a specific requirement."""
        if capacity_type == "organization":
            # Based on institutional strength and leadership
            leader_count = len([a for a in agents if a.is_alive and 
                              hasattr(a, 'specialization') and a.specialization == "leader"])
            institution_strength = len(institutions) / 5.0  # Normalize
            return min(1.0, (leader_count / 10.0) + institution_strength)
        
        elif capacity_type == "social_cohesion":
            # Based on relationships and group membership
            total_relationships = sum(len(getattr(a, 'relationships', {})) for a in agents if a.is_alive)
            population = len([a for a in agents if a.is_alive])
            return min(1.0, total_relationships / max(1, population * 3))
        
        elif capacity_type == "communication":
            # Based on cultural development and knowledge systems
            cultural_institutions = len([i for i in institutions.values() if 
                                       hasattr(i, 'institution_type') and "cultural" in i.institution_type])
            return min(1.0, cultural_institutions / 3.0)
        
        elif capacity_type == "leadership":
            # Based on leadership roles and reputation
            leaders = [a for a in agents if a.is_alive and 
                      hasattr(a, 'reputation') and a.reputation > 0.7]
            return min(1.0, len(leaders) / 5.0)
        
        elif capacity_type == "resources":
            # Based on available resources and wealth
            # This would integrate with resource/economic systems
            return random.uniform(0.3, 0.8)  # Placeholder
        
        else:
            return 0.5  # Default moderate capacity
    
    def _create_crisis_response(self, strategy: ResponseStrategy, crisis: SocietalCrisis,
                              agents: List[Any], institutions: Dict[str, Any],
                              current_day: int) -> Optional[CrisisResponse]:
        """Create a new crisis response effort."""
        response_id = f"response_{strategy.value}_{crisis.id}_{current_day}"
        
        # Select lead agents
        lead_agents = self._select_response_leaders(strategy, crisis, agents)
        if not lead_agents:
            return None
        
        # Select participating agents
        participating_agents = self._select_response_participants(strategy, crisis, agents, lead_agents)
        
        # Identify coordinating institutions
        coordinating_institutions = self._identify_coordinating_institutions(strategy, institutions)
        
        # Allocate resources
        resource_allocation = self._calculate_resource_allocation(strategy, crisis, agents, institutions)
        
        response = CrisisResponse(
            id=response_id,
            crisis_id=crisis.id,
            response_strategy=strategy,
            started_day=current_day,
            
            lead_agents=set(a.name for a in lead_agents),
            participating_agents=set(a.name for a in participating_agents),
            coordinating_institutions=coordinating_institutions,
            resource_allocation=resource_allocation,
            
            implementation_phase=ResponsePhase.MOBILIZATION,
            effectiveness=ResponseEffectiveness.PARTIALLY_EFFECTIVE,  # Start optimistic
            completion_percentage=0.0,
            
            crisis_impact_reduction=0.0,
            unintended_consequences=[],
            success_factors=[],
            failure_factors=[],
            
            innovations_created=[],
            social_bonds_formed=[],
            institutional_changes=[],
            
            finished_day=None,
            long_term_impact={}
        )
        
        return response
    
    def _select_response_leaders(self, strategy: ResponseStrategy, crisis: SocietalCrisis,
                               agents: List[Any]) -> List[Any]:
        """Select agents to lead response efforts."""
        suitable_leaders = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            leadership_score = 0.0
            
            # Reputation and social connections
            if hasattr(agent, 'reputation'):
                leadership_score += agent.reputation * 0.4
            
            if hasattr(agent, 'relationships'):
                leadership_score += min(0.3, len(agent.relationships) / 10.0)
            
            # Relevant specialization
            if hasattr(agent, 'specialization'):
                if strategy in [ResponseStrategy.INSTITUTIONAL_RESPONSE] and agent.specialization == "leader":
                    leadership_score += 0.3
                elif strategy in [ResponseStrategy.INNOVATION] and agent.specialization == "scholar":
                    leadership_score += 0.3
                elif strategy in [ResponseStrategy.RESOURCE_SHARING] and agent.specialization == "merchant":
                    leadership_score += 0.2
            
            # Being affected by the crisis
            if agent.name in crisis.affected_population:
                leadership_score += 0.1
            
            if leadership_score >= 0.6:  # Leadership threshold
                suitable_leaders.append(agent)
        
        # Sort by leadership score and select top candidates
        suitable_leaders.sort(key=lambda a: self._calculate_leadership_score(a, strategy), reverse=True)
        return suitable_leaders[:random.randint(1, 3)]  # 1-3 leaders
    
    def _calculate_leadership_score(self, agent: Any, strategy: ResponseStrategy) -> float:
        """Calculate leadership score for an agent."""
        score = 0.0
        
        if hasattr(agent, 'reputation'):
            score += agent.reputation * 0.5
        
        if hasattr(agent, 'relationships'):
            score += min(0.3, len(agent.relationships) / 10.0)
        
        if hasattr(agent, 'specialization'):
            # Strategy-specific bonuses
            if strategy == ResponseStrategy.INNOVATION and agent.specialization in ["scholar", "mystic"]:
                score += 0.2
            elif strategy == ResponseStrategy.COLLECTIVE_ACTION and agent.specialization == "leader":
                score += 0.2
        
        return score
    
    def _select_response_participants(self, strategy: ResponseStrategy, crisis: SocietalCrisis,
                                    agents: List[Any], leaders: List[Any]) -> List[Any]:
        """Select agents to participate in response efforts."""
        participants = leaders.copy()  # Leaders are always participants
        
        # Select additional participants based on strategy requirements
        strategy_config = self.response_strategies[strategy]
        population_impact = strategy_config.get("population_impact", 0.5)
        
        # Calculate how many participants needed
        affected_population = len(crisis.affected_population)
        target_participants = int(affected_population * population_impact)
        target_participants = min(target_participants, len([a for a in agents if a.is_alive]))
        
        # Select participants from affected population first
        affected_agents = [a for a in agents if a.name in crisis.affected_population and a not in participants]
        available_agents = [a for a in agents if a.is_alive and a not in participants]
        
        # Prioritize affected agents, then others
        candidate_pool = affected_agents + [a for a in available_agents if a not in affected_agents]
        
        additional_needed = max(0, target_participants - len(participants))
        if additional_needed > 0:
            additional_participants = random.sample(
                candidate_pool, 
                min(additional_needed, len(candidate_pool))
            )
            participants.extend(additional_participants)
        
        return participants
    
    def _identify_coordinating_institutions(self, strategy: ResponseStrategy, 
                                         institutions: Dict[str, Any]) -> Set[str]:
        """Identify institutions that would coordinate this response strategy."""
        coordinating = set()
        
        for institution_id, institution in institutions.items():
            if hasattr(institution, 'institution_type'):
                institution_type = institution.institution_type
                
                # Match institutions to strategies
                if (strategy == ResponseStrategy.INSTITUTIONAL_RESPONSE and 
                    "government" in institution_type):
                    coordinating.add(institution_id)
                elif (strategy == ResponseStrategy.INNOVATION and 
                      ("school" in institution_type or "academy" in institution_type)):
                    coordinating.add(institution_id)
                elif (strategy == ResponseStrategy.RESOURCE_SHARING and 
                      "commerce" in institution_type):
                    coordinating.add(institution_id)
                elif (strategy in [ResponseStrategy.COLLECTIVE_ACTION, ResponseStrategy.EVACUATION] and
                      "government" in institution_type):
                    coordinating.add(institution_id)
        
        return coordinating
    
    def _calculate_resource_allocation(self, strategy: ResponseStrategy, crisis: SocietalCrisis,
                                     agents: List[Any], institutions: Dict[str, Any]) -> Dict[str, float]:
        """Calculate resource allocation for response effort."""
        # This would integrate with resource/economic systems
        # For now, simulate based on strategy requirements and available capacity
        
        strategy_config = self.response_strategies[strategy]
        requirements = strategy_config["resource_requirements"]
        
        allocation = {}
        for resource_type, requirement_level in requirements.items():
            # Estimate available resources for this type
            available = self._estimate_available_resources(resource_type, agents, institutions)
            
            # Allocate portion of available resources
            allocated = min(available * 0.5, requirement_level)  # Up to 50% of available
            allocation[resource_type] = allocated
        
        return allocation
    
    def _estimate_available_resources(self, resource_type: str, agents: List[Any], 
                                    institutions: Dict[str, Any]) -> float:
        """Estimate available resources of a specific type."""
        # This would integrate with actual resource systems
        if resource_type == "organization":
            return len(institutions) / 5.0
        elif resource_type == "social_cohesion":
            total_relationships = sum(len(getattr(a, 'relationships', {})) for a in agents if a.is_alive)
            return min(1.0, total_relationships / 50.0)
        elif resource_type == "communication":
            return random.uniform(0.3, 0.8)
        else:
            return random.uniform(0.2, 0.7)  # Generic resource availability
    
    def _add_response_memories(self, response: CrisisResponse, agents: List[Any], 
                             crisis: SocietalCrisis) -> None:
        """Add response participation memories to agents."""
        for agent in agents:
            if agent.name in response.participating_agents and agent.is_alive:
                memory_text = f"Participating in {response.response_strategy.value} response to {crisis.name}"
                agent.memory.store_memory(
                    memory_text,
                    importance=0.7,
                    memory_type="crisis_response"
                )
    
    def _update_response_coordination(self, crisis: SocietalCrisis, agents: List[Any],
                                    institutions: Dict[str, Any], current_day: int) -> List[Dict[str, Any]]:
        """Update coordination of existing crisis responses."""
        events = []
        
        for response_id in crisis.active_responses:
            if response_id in self.crisis_responses:
                response = self.crisis_responses[response_id]
                
                # Update response progress
                progress_change = self._calculate_response_progress(response, crisis, agents, current_day)
                response.completion_percentage = min(1.0, response.completion_percentage + progress_change)
                
                # Update community mobilization
                mobilization_change = self._calculate_mobilization_change(response, crisis, agents)
                crisis.community_mobilization = min(1.0, crisis.community_mobilization + mobilization_change)
                
                # Check for response completion
                if response.completion_percentage >= 1.0 and not response.finished_day:
                    response.finished_day = current_day
                    response.implementation_phase = ResponsePhase.RECOVERY
                    
                    events.append({
                        "type": "crisis_response_completed",
                        "crisis_id": crisis.id,
                        "response_id": response_id,
                        "strategy": response.response_strategy.value,
                        "effectiveness": response.effectiveness.value,
                        "day": current_day
                    })
        
        return events
    
    def _calculate_response_progress(self, response: CrisisResponse, crisis: SocietalCrisis,
                                   agents: List[Any], current_day: int) -> float:
        """Calculate progress made on a response effort."""
        # Base progress rate
        base_progress = 1.0 / self.response_strategies[response.response_strategy]["typical_duration"]
        
        # Modifiers based on capacity and effectiveness
        modifiers = []
        
        # Leadership effectiveness
        leaders = [a for a in agents if a.name in response.lead_agents and a.is_alive]
        if leaders:
            avg_leader_reputation = sum(getattr(a, 'reputation', 0.5) for a in leaders) / len(leaders)
            modifiers.append(avg_leader_reputation)
        
        # Participation level
        active_participants = len([a for a in agents if a.name in response.participating_agents and a.is_alive])
        target_participants = len(response.participating_agents)
        if target_participants > 0:
            participation_ratio = active_participants / target_participants
            modifiers.append(participation_ratio)
        
        # Resource availability
        if response.resource_allocation:
            avg_resource_level = sum(response.resource_allocation.values()) / len(response.resource_allocation)
            modifiers.append(avg_resource_level)
        
        # Apply modifiers
        modifier_effect = sum(modifiers) / len(modifiers) if modifiers else 0.5
        adjusted_progress = base_progress * modifier_effect
        
        return max(0.01, adjusted_progress)  # Minimum progress to prevent stalling
    
    def _calculate_mobilization_change(self, response: CrisisResponse, crisis: SocietalCrisis,
                                     agents: List[Any]) -> float:
        """Calculate change in community mobilization."""
        # Mobilization increases with successful responses and decreases with failures
        
        if response.effectiveness in [ResponseEffectiveness.EFFECTIVE, ResponseEffectiveness.HIGHLY_EFFECTIVE]:
            return 0.05  # Positive mobilization
        elif response.effectiveness == ResponseEffectiveness.PARTIALLY_EFFECTIVE:
            return 0.02
        elif response.effectiveness == ResponseEffectiveness.INEFFECTIVE:
            return -0.02
        else:  # FAILED
            return -0.05
    
    def _update_response_effectiveness(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Update effectiveness of ongoing responses."""
        events = []
        
        for response_id, response in self.crisis_responses.items():
            if response.finished_day:  # Only update ongoing responses
                continue
            
            # Calculate new effectiveness
            old_effectiveness = response.effectiveness
            new_effectiveness = self._calculate_response_effectiveness(response, agents, current_day)
            
            if new_effectiveness != old_effectiveness:
                response.effectiveness = new_effectiveness
                
                events.append({
                    "type": "response_effectiveness_change",
                    "response_id": response_id,
                    "old_effectiveness": old_effectiveness.value,
                    "new_effectiveness": new_effectiveness.value,
                    "strategy": response.response_strategy.value,
                    "day": current_day
                })
        
        return events
    
    def _calculate_response_effectiveness(self, response: CrisisResponse, agents: List[Any],
                                        current_day: int) -> ResponseEffectiveness:
        """Calculate effectiveness of a response effort."""
        effectiveness_factors = []
        
        # Check success and failure factors
        success_score = len(response.success_factors) * 0.2
        failure_score = len(response.failure_factors) * 0.3  # Failures weigh more
        
        # Leadership quality
        leaders = [a for a in agents if a.name in response.lead_agents and a.is_alive]
        if leaders:
            avg_leader_quality = sum(getattr(a, 'reputation', 0.5) for a in leaders) / len(leaders)
            effectiveness_factors.append(avg_leader_quality)
        
        # Resource adequacy
        if response.resource_allocation:
            resource_adequacy = sum(response.resource_allocation.values()) / len(response.resource_allocation)
            effectiveness_factors.append(resource_adequacy)
        
        # Community participation
        active_participants = len([a for a in agents if a.name in response.participating_agents and a.is_alive])
        if len(response.participating_agents) > 0:
            participation_ratio = active_participants / len(response.participating_agents)
            effectiveness_factors.append(participation_ratio)
        
        # Progress rate
        days_active = current_day - response.started_day + 1
        expected_progress = days_active / self.response_strategies[response.response_strategy]["typical_duration"]
        progress_ratio = response.completion_percentage / max(0.01, expected_progress)
        effectiveness_factors.append(min(1.0, progress_ratio))
        
        # Calculate overall effectiveness
        base_effectiveness = sum(effectiveness_factors) / len(effectiveness_factors) if effectiveness_factors else 0.5
        final_effectiveness = base_effectiveness + success_score - failure_score
        
        # Convert to enum
        if final_effectiveness > 0.8:
            return ResponseEffectiveness.HIGHLY_EFFECTIVE
        elif final_effectiveness > 0.6:
            return ResponseEffectiveness.EFFECTIVE
        elif final_effectiveness > 0.4:
            return ResponseEffectiveness.PARTIALLY_EFFECTIVE
        elif final_effectiveness > 0.2:
            return ResponseEffectiveness.INEFFECTIVE
        else:
            return ResponseEffectiveness.FAILED
    
    def _process_recovery_and_adaptation(self, agents: List[Any], institutions: Dict[str, Any],
                                       current_day: int) -> List[Dict[str, Any]]:
        """Process recovery and adaptation phases of crisis response."""
        events = []
        
        for crisis_id, crisis in self.active_crises.items():
            if crisis.current_phase in [ResponsePhase.RECOVERY, ResponsePhase.ADAPTATION]:
                # Process recovery activities
                recovery_events = self._process_crisis_recovery(crisis, agents, institutions, current_day)
                events.extend(recovery_events)
                
                # Process adaptation and learning
                adaptation_events = self._process_crisis_adaptation(crisis, agents, institutions, current_day)
                events.extend(adaptation_events)
        
        return events
    
    def _process_crisis_recovery(self, crisis: SocietalCrisis, agents: List[Any],
                               institutions: Dict[str, Any], current_day: int) -> List[Dict[str, Any]]:
        """Process recovery activities for a crisis."""
        events = []
        
        # Recovery activities: rebuilding, resource restoration, social healing
        if random.random() < 0.1:  # 10% chance per day
            recovery_activities = [
                "resource_restoration",
                "infrastructure_rebuilding", 
                "social_healing",
                "community_reorganization"
            ]
            
            activity = random.choice(recovery_activities)
            
            events.append({
                "type": "crisis_recovery_activity",
                "crisis_id": crisis.id,
                "activity": activity,
                "description": f"Community engaging in {activity.replace('_', ' ')} efforts",
                "day": current_day
            })
            
            # Add recovery memories to affected agents
            for agent in agents:
                if agent.name in crisis.affected_population and agent.is_alive:
                    agent.memory.store_memory(
                        f"Participating in {activity.replace('_', ' ')} after {crisis.name}",
                        importance=0.6,
                        memory_type="recovery"
                    )
        
        return events
    
    def _process_crisis_adaptation(self, crisis: SocietalCrisis, agents: List[Any],
                                 institutions: Dict[str, Any], current_day: int) -> List[Dict[str, Any]]:
        """Process adaptation and learning from crisis."""
        events = []
        
        # Adaptation involves changing practices to prevent future crises
        if random.random() < 0.05:  # 5% chance per day
            adaptations = [
                "improved_early_warning",
                "resource_stockpiling",
                "emergency_procedures",
                "community_preparedness_training",
                "institutional_reforms"
            ]
            
            adaptation = random.choice(adaptations)
            crisis.lessons_learned.append(adaptation)
            
            events.append({
                "type": "crisis_adaptation",
                "crisis_id": crisis.id,
                "adaptation": adaptation,
                "description": f"Community implementing {adaptation.replace('_', ' ')} based on crisis experience",
                "day": current_day
            })
            
            # Update community resilience
            for location in crisis.affected_locations:
                if location not in self.resilience_capacities:
                    self.resilience_capacities[location] = self._create_initial_resilience_capacity(location)
                
                resilience = self.resilience_capacities[location]
                
                # Improve relevant capacity based on adaptation type
                if adaptation == "improved_early_warning":
                    resilience.early_warning_systems = min(1.0, resilience.early_warning_systems + 0.1)
                elif adaptation == "resource_stockpiling":
                    for resource in ["food", "water", "materials"]:
                        resilience.resource_reserves[resource] = resilience.resource_reserves.get(resource, 0) + 0.2
                elif adaptation == "emergency_procedures":
                    resilience.coordination_ability = min(1.0, resilience.coordination_ability + 0.1)
                elif adaptation == "institutional_reforms":
                    resilience.institutional_capacity = min(1.0, resilience.institutional_capacity + 0.1)
        
        return events
    
    def _create_initial_resilience_capacity(self, location: str) -> ResilienceCapacity:
        """Create initial resilience capacity for a location."""
        return ResilienceCapacity(
            location=location,
            early_warning_systems=0.3,
            resource_reserves={"food": 0.2, "water": 0.2, "materials": 0.1},
            institutional_capacity=0.4,
            social_cohesion=0.5,
            leadership_quality=0.4,
            coordination_ability=0.3,
            innovation_capacity=0.3,
            external_connections=0.2,
            learning_capability=0.4,
            flexibility=0.5,
            diversity=0.4,
            redundancy=0.3,
            crisis_experience={},
            successful_responses=0,
            failed_responses=0
        )
    
    def _update_resilience_capacities(self, agents: List[Any], institutions: Dict[str, Any],
                                    current_day: int) -> List[Dict[str, Any]]:
        """Update resilience capacities based on recent experiences."""
        events = []
        
        # Update resilience based on completed responses
        for response_id, response in self.crisis_responses.items():
            if response.finished_day == current_day:  # Just completed
                # Update experience for affected locations
                crisis = self.active_crises.get(response.crisis_id) or self._get_historical_crisis(response.crisis_id)
                
                if crisis:
                    for location in crisis.affected_locations:
                        if location not in self.resilience_capacities:
                            self.resilience_capacities[location] = self._create_initial_resilience_capacity(location)
                        
                        resilience = self.resilience_capacities[location]
                        
                        # Update crisis experience
                        crisis_type = crisis.crisis_type
                        resilience.crisis_experience[crisis_type] = resilience.crisis_experience.get(crisis_type, 0) + 1
                        
                        # Update success/failure counts
                        if response.effectiveness in [ResponseEffectiveness.EFFECTIVE, ResponseEffectiveness.HIGHLY_EFFECTIVE]:
                            resilience.successful_responses += 1
                            # Improve capacities based on successful response
                            resilience.learning_capability = min(1.0, resilience.learning_capability + 0.05)
                            resilience.coordination_ability = min(1.0, resilience.coordination_ability + 0.03)
                        else:
                            resilience.failed_responses += 1
                            # Still learn from failures, but less
                            resilience.learning_capability = min(1.0, resilience.learning_capability + 0.02)
                        
                        events.append({
                            "type": "resilience_capacity_update",
                            "location": location,
                            "crisis_type": crisis_type.value,
                            "response_effectiveness": response.effectiveness.value,
                            "new_experience_count": resilience.crisis_experience[crisis_type],
                            "day": current_day
                        })
        
        return events
    
    def _get_historical_crisis(self, crisis_id: str) -> Optional[SocietalCrisis]:
        """Get crisis from historical records."""
        for crisis_record in self.crisis_history:
            if crisis_record.get("crisis_id") == crisis_id:
                # Reconstruct crisis object from historical record
                # This is a simplified version
                return SocietalCrisis(
                    id=crisis_id,
                    name=crisis_record.get("name", "Unknown Crisis"),
                    crisis_type=CrisisType(crisis_record.get("crisis_type", "natural_disaster")),
                    severity=CrisisSeverity(crisis_record.get("severity", "moderate")),
                    started_day=crisis_record.get("started_day", 0),
                    affected_locations=set(crisis_record.get("affected_locations", [])),
                    affected_population=set(crisis_record.get("affected_population", [])),
                    secondary_effects=[],
                    duration_estimate=30,
                    current_phase=ResponsePhase.ADAPTATION,
                    intensity_over_time=[],
                    peak_intensity=0.5,
                    resolution_probability=0.0,
                    active_responses={},
                    coordinating_institutions=set(),
                    community_mobilization=0.0,
                    casualties=0,
                    resource_losses={},
                    social_disruption=0.0,
                    long_term_effects=[],
                    resolved_day=crisis_record.get("resolved_day"),
                    resolution_method=crisis_record.get("resolution_method"),
                    lessons_learned=crisis_record.get("lessons_learned", [])
                )
        return None
    
    def _process_crisis_learning(self, current_day: int) -> List[Dict[str, Any]]:
        """Process learning from completed crises."""
        events = []
        
        # Check for crises that just resolved
        newly_resolved = []
        for crisis_id, crisis in list(self.active_crises.items()):
            if crisis.resolved_day == current_day:
                newly_resolved.append(crisis)
                
                # Move to historical records
                self.crisis_history.append({
                    "crisis_id": crisis.id,
                    "name": crisis.name,
                    "crisis_type": crisis.crisis_type.value,
                    "severity": crisis.severity.value,
                    "started_day": crisis.started_day,
                    "resolved_day": crisis.resolved_day,
                    "resolution_method": crisis.resolution_method,
                    "affected_locations": list(crisis.affected_locations),
                    "affected_population": list(crisis.affected_population),
                    "lessons_learned": crisis.lessons_learned,
                    "peak_intensity": crisis.peak_intensity,
                    "total_responses": len(crisis.active_responses),
                    "community_mobilization": crisis.community_mobilization
                })
                
                del self.active_crises[crisis_id]
        
        # Generate learning events
        for crisis in newly_resolved:
            if crisis.lessons_learned:
                events.append({
                    "type": "crisis_lessons_learned",
                    "crisis_name": crisis.name,
                    "lessons": crisis.lessons_learned,
                    "community_mobilization": crisis.community_mobilization,
                    "responses_count": len(crisis.active_responses),
                    "description": f"Community learned from {crisis.name}: {', '.join(crisis.lessons_learned[:3])}",
                    "day": current_day
                })
                
                # Add lessons to system-wide knowledge
                for lesson in crisis.lessons_learned:
                    self.lessons_learned[crisis.crisis_type.value].append(lesson)
        
        return events
    
    def _resolve_crisis(self, crisis: SocietalCrisis, resolution_method: str, current_day: int) -> Dict[str, Any]:
        """Resolve a crisis and record the resolution."""
        crisis.resolved_day = current_day
        crisis.resolution_method = resolution_method
        crisis.current_phase = ResponsePhase.ADAPTATION
        
        return {
            "type": "crisis_resolved",
            "crisis_id": crisis.id,
            "crisis_name": crisis.name,
            "resolution_method": resolution_method,
            "duration": current_day - crisis.started_day,
            "peak_intensity": crisis.peak_intensity,
            "responses_used": len(crisis.active_responses),
            "community_mobilization": crisis.community_mobilization,
            "day": current_day
        }
    
    def get_crisis_response_summary(self) -> Dict[str, Any]:
        """Get comprehensive crisis response system summary."""
        summary = {
            "active_crises": len(self.active_crises),
            "historical_crises": len(self.crisis_history),
            "active_responses": len([r for r in self.crisis_responses.values() if not r.finished_day]),
            "completed_responses": len([r for r in self.crisis_responses.values() if r.finished_day]),
            "crisis_types_experienced": {},
            "response_effectiveness": {},
            "community_resilience": {},
            "lessons_learned_count": sum(len(lessons) for lessons in self.lessons_learned.values())
        }
        
        # Count crisis types from history
        for crisis_record in self.crisis_history:
            crisis_type = crisis_record["crisis_type"]
            summary["crisis_types_experienced"][crisis_type] = summary["crisis_types_experienced"].get(crisis_type, 0) + 1
        
        # Count response effectiveness
        for response in self.crisis_responses.values():
            effectiveness = response.effectiveness.value
            summary["response_effectiveness"][effectiveness] = summary["response_effectiveness"].get(effectiveness, 0) + 1
        
        # Summarize community resilience
        if self.resilience_capacities:
            avg_resilience = {
                "early_warning": sum(r.early_warning_systems for r in self.resilience_capacities.values()) / len(self.resilience_capacities),
                "social_cohesion": sum(r.social_cohesion for r in self.resilience_capacities.values()) / len(self.resilience_capacities),
                "institutional_capacity": sum(r.institutional_capacity for r in self.resilience_capacities.values()) / len(self.resilience_capacities),
                "learning_capability": sum(r.learning_capability for r in self.resilience_capacities.values()) / len(self.resilience_capacities)
            }
            summary["community_resilience"] = avg_resilience
        
        return summary 