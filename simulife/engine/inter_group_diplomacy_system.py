"""
Inter-Group Diplomacy System for SimuLife
Handles complex diplomatic relations, negotiations, treaties, and international politics
between groups, factions, and emerging civilizations.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import math


class DiplomaticStatus(Enum):
    """Diplomatic relationship status between groups."""
    UNRECOGNIZED = "unrecognized"       # No formal recognition
    ACKNOWLEDGED = "acknowledged"       # Basic awareness
    NEUTRAL = "neutral"                 # Formal neutrality
    FRIENDLY = "friendly"               # Positive relations
    ALLIED = "allied"                   # Military/political alliance
    HOSTILE = "hostile"                 # Antagonistic relations
    WAR = "war"                         # Active conflict
    VASSAL = "vassal"                   # Subordinate relationship
    PROTECTORATE = "protectorate"       # Protection arrangement


class TreatyType(Enum):
    """Types of diplomatic treaties."""
    TRADE_AGREEMENT = "trade_agreement"         # Commercial relations
    MUTUAL_DEFENSE = "mutual_defense"           # Military alliance
    NON_AGGRESSION = "non_aggression"           # Peace agreement
    CULTURAL_EXCHANGE = "cultural_exchange"     # Knowledge/culture sharing
    TERRITORIAL = "territorial"                 # Border/territory agreements
    RESOURCE_SHARING = "resource_sharing"       # Resource agreements
    DIPLOMATIC_IMMUNITY = "diplomatic_immunity" # Diplomatic protection
    PRISONER_EXCHANGE = "prisoner_exchange"     # Conflict resolution
    MARRIAGE_ALLIANCE = "marriage_alliance"     # Dynastic ties
    TRIBUTE = "tribute"                         # Tributary relationship


class NegotiationPhase(Enum):
    """Phases of diplomatic negotiation."""
    PROPOSAL = "proposal"               # Initial proposal made
    DISCUSSION = "discussion"           # Active negotiation
    DEADLOCK = "deadlock"              # Stuck negotiations
    COMPROMISE = "compromise"           # Finding middle ground
    AGREEMENT = "agreement"             # Terms agreed upon
    RATIFICATION = "ratification"       # Formal approval
    IMPLEMENTATION = "implementation"   # Putting into effect
    VIOLATION = "violation"             # Treaty broken
    RENEGOTIATION = "renegotiation"     # Updating terms


class DiplomaticAction(Enum):
    """Types of diplomatic actions."""
    RECOGNITION = "recognition"                 # Formal recognition
    EMBASSY_ESTABLISHMENT = "embassy_establishment"  # Setting up embassy
    TRADE_MISSION = "trade_mission"            # Commercial diplomacy
    CULTURAL_MISSION = "cultural_mission"       # Cultural exchange
    PEACE_NEGOTIATION = "peace_negotiation"     # Conflict resolution
    ALLIANCE_PROPOSAL = "alliance_proposal"     # Military alliance
    TRIBUTE_DEMAND = "tribute_demand"           # Demanding tribute
    DIPLOMATIC_PROTEST = "diplomatic_protest"   # Formal complaint
    AMBASSADOR_RECALL = "ambassador_recall"     # Withdrawing diplomats
    SANCTIONS = "sanctions"                     # Economic pressure


@dataclass
class DiplomaticRelation:
    """Represents the diplomatic relationship between two groups."""
    group1_id: str
    group2_id: str
    status: DiplomaticStatus
    established_day: int
    
    # Relationship metrics
    trust_level: float                  # 0.0-1.0 mutual trust
    trade_volume: float                # Economic ties strength
    cultural_affinity: float           # Cultural compatibility
    power_balance: float               # -1.0 to 1.0 (group1 stronger to group2 stronger)
    
    # Historical tracking
    interaction_history: List[Dict[str, Any]]  # Past diplomatic events
    treaties: List[str]                # Active treaty IDs
    violations: List[Dict[str, Any]]   # Treaty violations
    ambassadors: Dict[str, str]        # Group -> ambassador agent name
    
    # Current dynamics
    pending_negotiations: List[str]     # Negotiation IDs
    recent_incidents: List[Dict[str, Any]]  # Recent diplomatic incidents
    relationship_trends: List[Tuple[int, float]]  # Day, relationship score
    
    # Influence and leverage
    mutual_dependencies: Dict[str, float]  # Areas of dependency
    leverage_points: Dict[str, float]      # Sources of diplomatic leverage
    shared_interests: List[str]            # Common goals and interests
    conflicting_interests: List[str]       # Areas of disagreement


@dataclass
class DiplomaticTreaty:
    """Represents a formal treaty between groups."""
    id: str
    name: str
    treaty_type: TreatyType
    signatory_groups: List[str]
    signed_day: int
    
    # Treaty terms
    terms: Dict[str, Any]              # Specific treaty provisions
    obligations: Dict[str, List[str]]  # Group -> list of obligations
    benefits: Dict[str, List[str]]     # Group -> list of benefits
    duration: Optional[int]            # Treaty duration in days (None = permanent)
    
    # Implementation and compliance
    compliance_score: Dict[str, float] # Group -> compliance rating
    violations: List[Dict[str, Any]]   # Record of violations
    enforcement_mechanisms: List[str]  # How treaty is enforced
    
    # Status and evolution
    status: str                        # active, suspended, terminated
    amendments: List[Dict[str, Any]]   # Changes to original treaty
    renewal_date: Optional[int]        # When treaty needs renewal
    
    # Impact and effectiveness
    economic_impact: Dict[str, float]  # Economic effects per group
    political_impact: Dict[str, float] # Political effects per group
    cultural_impact: Dict[str, float]  # Cultural effects per group


@dataclass
class DiplomaticNegotiation:
    """Represents an ongoing diplomatic negotiation."""
    id: str
    groups: List[str]                  # Participating groups
    proposed_treaty_type: TreatyType
    started_day: int
    
    # Negotiation state
    current_phase: NegotiationPhase
    lead_negotiators: Dict[str, str]   # Group -> agent name
    proposed_terms: Dict[str, Any]     # Current proposal
    
    # Negotiation dynamics
    positions: Dict[str, Dict[str, Any]]  # Each group's position
    concessions_made: Dict[str, List[str]]  # Concessions by group
    deadlock_issues: List[str]         # Sticking points
    
    # External factors
    time_pressure: float               # 0.0-1.0 urgency level
    third_party_influence: Dict[str, float]  # External group influence
    public_pressure: float             # Domestic pressure to agree
    
    # Progress tracking
    agreement_probability: float       # Current chance of success
    negotiation_rounds: int           # Number of rounds conducted
    estimated_completion: Optional[int]  # Estimated completion day


@dataclass
class DiplomaticAgent:
    """Represents an agent serving in diplomatic capacity."""
    agent_name: str
    diplomatic_role: str               # ambassador, envoy, negotiator, etc.
    representing_group: str
    assigned_location: str
    assignment_day: int
    
    # Diplomatic skills and attributes
    negotiation_skill: float          # 0.0-1.0 negotiation ability
    cultural_understanding: float     # Understanding of foreign cultures
    languages_known: List[str]        # Cultural/linguistic knowledge
    reputation: float                  # Diplomatic reputation
    
    # Current assignments
    active_negotiations: List[str]    # Negotiation IDs
    diplomatic_contacts: Dict[str, float]  # Contact -> relationship strength
    cultural_knowledge: Dict[str, float]   # Group -> cultural understanding
    
    # Performance and experience
    successful_negotiations: int      # Number of successful deals
    failed_negotiations: int         # Number of failed deals
    diplomatic_incidents: List[Dict[str, Any]]  # Notable events
    
    # Status and loyalty
    loyalty: float                    # 0.0-1.0 loyalty to home group
    foreign_influence: Dict[str, float]  # Influence from foreign groups
    effectiveness_rating: float      # Current effectiveness


class InterGroupDiplomacySystem:
    """
    Manages complex diplomatic relations, negotiations, and treaties
    between groups, factions, and emerging civilizations.
    """
    
    def __init__(self):
        self.diplomatic_relations: Dict[Tuple[str, str], DiplomaticRelation] = {}
        self.treaties: Dict[str, DiplomaticTreaty] = {}
        self.negotiations: Dict[str, DiplomaticNegotiation] = {}
        self.diplomatic_agents: Dict[str, DiplomaticAgent] = {}
        
        # System tracking
        self.diplomatic_events: List[Dict[str, Any]] = []
        self.international_law: List[Dict[str, Any]] = []
        self.diplomatic_precedents: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        
        # System configuration
        self.diplomacy_triggers = self._initialize_diplomacy_triggers()
        self.treaty_templates = self._initialize_treaty_templates()
        self.negotiation_factors = self._initialize_negotiation_factors()
        
        # World diplomatic state
        self.global_diplomatic_trends: Dict[str, float] = {}
        self.power_balance_shifts: List[Dict[str, Any]] = []
        self.diplomatic_crises: List[Dict[str, Any]] = []
    
    def _initialize_diplomacy_triggers(self) -> Dict[str, Dict[str, Any]]:
        """Initialize conditions that trigger diplomatic activities."""
        return {
            "first_contact": {
                "description": "Groups becoming aware of each other",
                "triggers": ["territorial_proximity", "trade_opportunity", "conflict"],
                "probability": 0.8,
                "outcomes": ["recognition", "initial_contact"]
            },
            "trade_opportunity": {
                "description": "Economic incentives for cooperation",
                "triggers": ["resource_complementarity", "technological_differences", "geographic_access"],
                "probability": 0.6,
                "outcomes": ["trade_agreement", "commercial_embassy"]
            },
            "territorial_dispute": {
                "description": "Conflicts over territory or resources",
                "triggers": ["border_expansion", "resource_competition", "migration_pressure"],
                "probability": 0.7,
                "outcomes": ["territorial_treaty", "conflict", "arbitration"]
            },
            "security_threat": {
                "description": "External threats requiring cooperation",
                "triggers": ["common_enemy", "crisis_response", "mutual_vulnerability"],
                "probability": 0.8,
                "outcomes": ["mutual_defense", "military_alliance", "intelligence_sharing"]
            },
            "cultural_exchange": {
                "description": "Opportunities for cultural sharing",
                "triggers": ["cultural_compatibility", "knowledge_gaps", "artistic_innovation"],
                "probability": 0.4,
                "outcomes": ["cultural_treaty", "educational_exchange", "artistic_collaboration"]
            },
            "power_imbalance": {
                "description": "Significant differences in power",
                "triggers": ["military_superiority", "economic_dominance", "technological_advantage"],
                "probability": 0.6,
                "outcomes": ["tribute_demand", "protectorate", "vassal_relationship"]
            },
            "succession_crisis": {
                "description": "Leadership changes affecting relations",
                "triggers": ["leadership_change", "internal_instability", "regime_change"],
                "probability": 0.5,
                "outcomes": ["renegotiation", "treaty_violation", "relationship_reset"]
            }
        }
    
    def _initialize_treaty_templates(self) -> Dict[TreatyType, Dict[str, Any]]:
        """Initialize templates for different treaty types."""
        return {
            TreatyType.TRADE_AGREEMENT: {
                "typical_terms": ["tariff_reduction", "trade_routes", "currency_exchange", "dispute_resolution"],
                "required_conditions": ["economic_compatibility", "trust_level > 0.4"],
                "typical_duration": 365,  # 1 year
                "renewal_probability": 0.8,
                "compliance_difficulty": 0.3
            },
            TreatyType.MUTUAL_DEFENSE: {
                "typical_terms": ["mutual_military_aid", "shared_intelligence", "coordinated_defense", "non_betrayal"],
                "required_conditions": ["shared_threats", "trust_level > 0.6", "military_compatibility"],
                "typical_duration": 1095,  # 3 years
                "renewal_probability": 0.6,
                "compliance_difficulty": 0.7
            },
            TreatyType.NON_AGGRESSION: {
                "typical_terms": ["no_attacks", "peaceful_coexistence", "border_respect", "conflict_prevention"],
                "required_conditions": ["previous_conflicts", "trust_level > 0.3"],
                "typical_duration": 730,  # 2 years
                "renewal_probability": 0.7,
                "compliance_difficulty": 0.4
            },
            TreatyType.CULTURAL_EXCHANGE: {
                "typical_terms": ["knowledge_sharing", "educational_exchange", "cultural_preservation", "language_learning"],
                "required_conditions": ["cultural_compatibility", "knowledge_differences"],
                "typical_duration": 1825,  # 5 years
                "renewal_probability": 0.9,
                "compliance_difficulty": 0.2
            },
            TreatyType.TERRITORIAL: {
                "typical_terms": ["border_demarcation", "territorial_rights", "resource_access", "migration_rules"],
                "required_conditions": ["territorial_disputes", "geographic_proximity"],
                "typical_duration": None,  # Permanent
                "renewal_probability": 0.3,  # Rarely changed
                "compliance_difficulty": 0.6
            },
            TreatyType.TRIBUTE: {
                "typical_terms": ["regular_payments", "protection_guarantee", "autonomy_limits", "loyalty_oath"],
                "required_conditions": ["power_imbalance > 0.5", "military_superiority"],
                "typical_duration": 1095,  # 3 years
                "renewal_probability": 0.4,
                "compliance_difficulty": 0.8
            }
        }
    
    def _initialize_negotiation_factors(self) -> Dict[str, Dict[str, float]]:
        """Initialize factors affecting negotiation success."""
        return {
            "trust_level": {"high": 1.5, "medium": 1.0, "low": 0.6},
            "power_balance": {"equal": 1.3, "slight_imbalance": 1.0, "major_imbalance": 0.7},
            "cultural_affinity": {"high": 1.4, "medium": 1.0, "low": 0.8},
            "economic_incentive": {"high": 1.6, "medium": 1.0, "low": 0.5},
            "external_pressure": {"high": 1.3, "medium": 1.0, "low": 0.9},
            "negotiator_skill": {"expert": 1.5, "competent": 1.0, "novice": 0.7},
            "time_pressure": {"urgent": 0.8, "moderate": 1.0, "relaxed": 1.2},
            "public_support": {"strong": 1.3, "neutral": 1.0, "opposed": 0.6}
        }
    
    def process_daily_diplomacy(self, agents: List[Any], groups: Dict[str, Any],
                              institutions: Dict[str, Any], world_events: List[Dict[str, Any]],
                              current_day: int) -> List[Dict[str, Any]]:
        """Process daily diplomatic activities."""
        events = []
        
        # Step 1: Check for new diplomatic contacts and recognition
        contact_events = self._check_diplomatic_contacts(agents, groups, current_day)
        events.extend(contact_events)
        
        # Step 2: Update existing diplomatic relations
        relation_events = self._update_diplomatic_relations(groups, world_events, current_day)
        events.extend(relation_events)
        
        # Step 3: Process ongoing negotiations
        negotiation_events = self._process_negotiations(agents, groups, current_day)
        events.extend(negotiation_events)
        
        # Step 4: Check for new negotiation opportunities
        opportunity_events = self._check_negotiation_opportunities(groups, current_day)
        events.extend(opportunity_events)
        
        # Step 5: Monitor treaty compliance and violations
        compliance_events = self._monitor_treaty_compliance(groups, world_events, current_day)
        events.extend(compliance_events)
        
        # Step 6: Manage diplomatic agents and assignments
        agent_events = self._manage_diplomatic_agents(agents, groups, current_day)
        events.extend(agent_events)
        
        # Step 7: Process diplomatic crises and incidents
        crisis_events = self._process_diplomatic_crises(groups, world_events, current_day)
        events.extend(crisis_events)
        
        # Step 8: Update global diplomatic trends
        self._update_global_trends(groups, current_day)
        
        return events
    
    def _check_diplomatic_contacts(self, agents: List[Any], groups: Dict[str, Any],
                                 current_day: int) -> List[Dict[str, Any]]:
        """Check for new diplomatic contacts between groups."""
        events = []
        
        # Get all active groups
        active_groups = {gid: group for gid, group in groups.items() 
                        if self._is_group_diplomatically_active(group)}
        
        # Check for first contact opportunities
        for group1_id, group1 in active_groups.items():
            for group2_id, group2 in active_groups.items():
                if group1_id >= group2_id:  # Avoid duplicates
                    continue
                
                relation_key = self._get_relation_key(group1_id, group2_id)
                
                # Skip if relationship already exists
                if relation_key in self.diplomatic_relations:
                    continue
                
                # Check for contact triggers
                contact_probability = self._calculate_contact_probability(group1, group2, agents)
                
                if random.random() < contact_probability:
                    # Establish first contact
                    relation = self._establish_diplomatic_contact(group1_id, group2_id, group1, group2, current_day)
                    
                    events.append({
                        "type": "diplomatic_first_contact",
                        "group1": group1_id,
                        "group2": group2_id,
                        "initial_status": relation.status.value,
                        "contact_method": self._determine_contact_method(group1, group2),
                        "day": current_day
                    })
                    
                    # Add contact memories to relevant agents
                    self._add_diplomatic_memories(agents, group1_id, group2_id, "first_contact", current_day)
        
        return events
    
    def _is_group_diplomatically_active(self, group: Any) -> bool:
        """Check if a group is active enough for diplomacy."""
        # Check if group has minimum requirements for diplomacy
        if not hasattr(group, 'members') or len(group.members) < 3:
            return False
        
        if hasattr(group, 'status') and group.status == "disbanded":
            return False
        
        # Need some form of organization or leadership
        if hasattr(group, 'leaders') and len(group.leaders) > 0:
            return True
        
        if hasattr(group, 'group_type') and group.group_type in ["faction", "institution", "council"]:
            return True
        
        return False
    
    def _calculate_contact_probability(self, group1: Any, group2: Any, agents: List[Any]) -> float:
        """Calculate probability of diplomatic contact between two groups."""
        base_probability = 0.02  # 2% base chance per day
        
        # Geographic proximity
        group1_locations = self._get_group_locations(group1, agents)
        group2_locations = self._get_group_locations(group2, agents)
        
        if group1_locations & group2_locations:  # Overlapping locations
            base_probability *= 3.0
        elif self._are_locations_adjacent(group1_locations, group2_locations):
            base_probability *= 2.0
        
        # Size factor - larger groups more likely to make contact
        group1_size = len(getattr(group1, 'members', []))
        group2_size = len(getattr(group2, 'members', []))
        size_factor = math.sqrt((group1_size + group2_size) / 10.0)
        base_probability *= min(3.0, size_factor)
        
        # Specialization compatibility
        if self._have_complementary_specializations(group1, group2):
            base_probability *= 1.5
        
        # Existing diplomatic activity
        if self._has_diplomatic_experience(group1) or self._has_diplomatic_experience(group2):
            base_probability *= 1.3
        
        return min(0.3, base_probability)  # Cap at 30% per day
    
    def _get_group_locations(self, group: Any, agents: List[Any]) -> Set[str]:
        """Get locations where group members are present."""
        locations = set()
        
        if hasattr(group, 'members'):
            for member_name in group.members:
                agent = next((a for a in agents if a.name == member_name), None)
                if agent and agent.is_alive:
                    locations.add(agent.location)
        
        return locations
    
    def _are_locations_adjacent(self, locations1: Set[str], locations2: Set[str]) -> bool:
        """Check if two sets of locations are geographically adjacent."""
        # Simplified adjacency check
        adjacency_map = {
            "village_center": {"fields", "forest", "river"},
            "fields": {"village_center", "forest", "plains"},
            "forest": {"village_center", "fields", "mountains", "hills"},
            "mountains": {"forest", "hills"},
            "hills": {"forest", "mountains", "plains"},
            "river": {"village_center", "plains"},
            "plains": {"fields", "hills", "river"}
        }
        
        for loc1 in locations1:
            for loc2 in locations2:
                if loc2 in adjacency_map.get(loc1, set()):
                    return True
        
        return False
    
    def _have_complementary_specializations(self, group1: Any, group2: Any) -> bool:
        """Check if groups have complementary specializations."""
        # This would check if groups have different but compatible specializations
        # For now, assume some groups are complementary
        return random.random() < 0.3
    
    def _has_diplomatic_experience(self, group: Any) -> bool:
        """Check if group has prior diplomatic experience."""
        # This would check group's diplomatic history
        return random.random() < 0.2  # 20% chance
    
    def _establish_diplomatic_contact(self, group1_id: str, group2_id: str, group1: Any, group2: Any,
                                    current_day: int) -> DiplomaticRelation:
        """Establish initial diplomatic contact between two groups."""
        relation_key = self._get_relation_key(group1_id, group2_id)
        
        # Determine initial status
        initial_status = self._determine_initial_status(group1, group2)
        
        # Calculate initial metrics
        trust_level = self._calculate_initial_trust(group1, group2)
        cultural_affinity = self._calculate_cultural_affinity(group1, group2)
        power_balance = self._calculate_power_balance(group1, group2)
        
        relation = DiplomaticRelation(
            group1_id=group1_id,
            group2_id=group2_id,
            status=initial_status,
            established_day=current_day,
            
            trust_level=trust_level,
            trade_volume=0.0,
            cultural_affinity=cultural_affinity,
            power_balance=power_balance,
            
            interaction_history=[],
            treaties=[],
            violations=[],
            ambassadors={},
            
            pending_negotiations=[],
            recent_incidents=[],
            relationship_trends=[(current_day, trust_level)],
            
            mutual_dependencies={},
            leverage_points={},
            shared_interests=[],
            conflicting_interests=[]
        )
        
        self.diplomatic_relations[relation_key] = relation
        return relation
    
    def _get_relation_key(self, group1_id: str, group2_id: str) -> Tuple[str, str]:
        """Get standardized key for diplomatic relation."""
        return tuple(sorted([group1_id, group2_id]))
    
    def _determine_initial_status(self, group1: Any, group2: Any) -> DiplomaticStatus:
        """Determine initial diplomatic status between groups."""
        # Check for existing conflicts or compatibility
        
        # High compatibility leads to friendly status
        if self._are_groups_compatible(group1, group2):
            return DiplomaticStatus.FRIENDLY
        
        # Historical conflicts lead to hostile status
        if self._have_historical_conflicts(group1, group2):
            return DiplomaticStatus.HOSTILE
        
        # Default to neutral for most new contacts
        return DiplomaticStatus.NEUTRAL
    
    def _are_groups_compatible(self, group1: Any, group2: Any) -> bool:
        """Check if groups are naturally compatible."""
        # Check group types, cultures, goals
        compatible_pairs = [
            ("guild", "merchant_group"),
            ("institution", "cultural_group"),
            ("alliance", "political_group")
        ]
        
        group1_type = getattr(group1, 'group_type', 'unknown')
        group2_type = getattr(group2, 'group_type', 'unknown')
        
        return (group1_type, group2_type) in compatible_pairs or (group2_type, group1_type) in compatible_pairs
    
    def _have_historical_conflicts(self, group1: Any, group2: Any) -> bool:
        """Check if groups have historical conflicts."""
        # This would check historical records
        return random.random() < 0.1  # 10% chance of prior conflict
    
    def _calculate_initial_trust(self, group1: Any, group2: Any) -> float:
        """Calculate initial trust level between groups."""
        trust = 0.5  # Neutral starting point
        
        # Adjust based on group characteristics
        if self._are_groups_compatible(group1, group2):
            trust += 0.2
        
        if self._have_historical_conflicts(group1, group2):
            trust -= 0.3
        
        # Random variation
        trust += random.uniform(-0.1, 0.1)
        
        return max(0.0, min(1.0, trust))
    
    def _calculate_cultural_affinity(self, group1: Any, group2: Any) -> float:
        """Calculate cultural affinity between groups."""
        affinity = 0.5  # Base affinity
        
        # Check for shared cultural elements
        if hasattr(group1, 'culture') and hasattr(group2, 'culture'):
            # This would compare actual cultural attributes
            affinity += random.uniform(-0.2, 0.3)
        
        return max(0.0, min(1.0, affinity))
    
    def _calculate_power_balance(self, group1: Any, group2: Any) -> float:
        """Calculate power balance between groups (-1.0 = group1 weaker, +1.0 = group1 stronger)."""
        group1_size = len(getattr(group1, 'members', []))
        group2_size = len(getattr(group2, 'members', []))
        
        if group1_size + group2_size == 0:
            return 0.0
        
        # Simple size-based power calculation
        power_ratio = (group1_size - group2_size) / (group1_size + group2_size)
        
        # Add random factors for other power sources
        power_ratio += random.uniform(-0.2, 0.2)
        
        return max(-1.0, min(1.0, power_ratio))
    
    def _determine_contact_method(self, group1: Any, group2: Any) -> str:
        """Determine how groups made contact."""
        methods = [
            "territorial_encounter",
            "trade_contact", 
            "cultural_exchange",
            "military_encounter",
            "diplomatic_mission",
            "accidental_meeting"
        ]
        return random.choice(methods)
    
    def _add_diplomatic_memories(self, agents: List[Any], group1_id: str, group2_id: str,
                               event_type: str, current_day: int) -> None:
        """Add diplomatic memories to relevant agents."""
        for agent in agents:
            if agent.is_alive and hasattr(agent, 'memory'):
                # Check if agent is involved in either group
                if (hasattr(agent, 'group_memberships') and 
                    (group1_id in agent.group_memberships or group2_id in agent.group_memberships)):
                    
                    memory_text = f"Our group made {event_type} with another group"
                    agent.memory.store_memory(
                        memory_text,
                        importance=0.6,
                        memory_type="diplomacy"
                    )
    
    def _update_diplomatic_relations(self, groups: Dict[str, Any], world_events: List[Dict[str, Any]],
                                   current_day: int) -> List[Dict[str, Any]]:
        """Update existing diplomatic relations."""
        events = []
        
        for relation_key, relation in self.diplomatic_relations.items():
            # Update relationship metrics
            old_trust = relation.trust_level
            
            # Trust evolves based on interactions and events
            trust_change = self._calculate_trust_change(relation, groups, world_events)
            relation.trust_level = max(0.0, min(1.0, relation.trust_level + trust_change))
            
            # Update relationship trends
            relation.relationship_trends.append((current_day, relation.trust_level))
            
            # Keep only recent trends
            if len(relation.relationship_trends) > 100:
                relation.relationship_trends = relation.relationship_trends[-100:]
            
            # Check for status changes
            new_status = self._determine_status_change(relation, groups, world_events)
            if new_status != relation.status:
                old_status = relation.status
                relation.status = new_status
                
                events.append({
                    "type": "diplomatic_status_change",
                    "group1": relation.group1_id,
                    "group2": relation.group2_id,
                    "old_status": old_status.value,
                    "new_status": new_status.value,
                    "trust_level": relation.trust_level,
                    "day": current_day
                })
            
            # Report significant trust changes
            if abs(relation.trust_level - old_trust) > 0.1:
                events.append({
                    "type": "diplomatic_trust_change",
                    "group1": relation.group1_id,
                    "group2": relation.group2_id,
                    "trust_change": relation.trust_level - old_trust,
                    "new_trust": relation.trust_level,
                    "day": current_day
                })
        
        return events
    
    def _calculate_trust_change(self, relation: DiplomaticRelation, groups: Dict[str, Any],
                              world_events: List[Dict[str, Any]]) -> float:
        """Calculate change in trust between groups."""
        trust_change = 0.0
        
        # Gradual decay without interaction
        trust_change -= 0.001
        
        # Positive interactions increase trust
        positive_interactions = len([e for e in world_events if self._is_positive_interaction(e, relation)])
        trust_change += positive_interactions * 0.05
        
        # Negative interactions decrease trust
        negative_interactions = len([e for e in world_events if self._is_negative_interaction(e, relation)])
        trust_change -= negative_interactions * 0.1
        
        # Treaty compliance affects trust
        for treaty_id in relation.treaties:
            if treaty_id in self.treaties:
                treaty = self.treaties[treaty_id]
                compliance_avg = sum(treaty.compliance_score.values()) / len(treaty.compliance_score)
                if compliance_avg > 0.8:
                    trust_change += 0.02
                elif compliance_avg < 0.5:
                    trust_change -= 0.05
        
        return trust_change
    
    def _is_positive_interaction(self, event: Dict[str, Any], relation: DiplomaticRelation) -> bool:
        """Check if event represents positive interaction between groups."""
        event_type = event.get("type", "")
        
        positive_types = ["trade", "cultural_exchange", "cooperation", "aid"]
        return any(pos_type in event_type for pos_type in positive_types)
    
    def _is_negative_interaction(self, event: Dict[str, Any], relation: DiplomaticRelation) -> bool:
        """Check if event represents negative interaction between groups."""
        event_type = event.get("type", "")
        
        negative_types = ["conflict", "violation", "dispute", "aggression"]
        return any(neg_type in event_type for neg_type in negative_types)
    
    def _determine_status_change(self, relation: DiplomaticRelation, groups: Dict[str, Any],
                               world_events: List[Dict[str, Any]]) -> DiplomaticStatus:
        """Determine if diplomatic status should change."""
        current_status = relation.status
        trust = relation.trust_level
        
        # Trust-based status transitions
        if trust > 0.8 and current_status == DiplomaticStatus.FRIENDLY:
            # Check for alliance conditions
            if self._should_form_alliance(relation, groups):
                return DiplomaticStatus.ALLIED
        
        elif trust > 0.6 and current_status == DiplomaticStatus.NEUTRAL:
            return DiplomaticStatus.FRIENDLY
        
        elif trust < 0.3 and current_status in [DiplomaticStatus.NEUTRAL, DiplomaticStatus.FRIENDLY]:
            return DiplomaticStatus.HOSTILE
        
        elif trust < 0.1 and current_status == DiplomaticStatus.HOSTILE:
            # Check for war conditions
            if self._should_declare_war(relation, groups, world_events):
                return DiplomaticStatus.WAR
        
        # War to peace transitions
        elif trust > 0.4 and current_status == DiplomaticStatus.WAR:
            return DiplomaticStatus.HOSTILE
        
        elif trust > 0.6 and current_status == DiplomaticStatus.HOSTILE:
            return DiplomaticStatus.NEUTRAL
        
        return current_status
    
    def _should_form_alliance(self, relation: DiplomaticRelation, groups: Dict[str, Any]) -> bool:
        """Check if groups should form an alliance."""
        # High trust, shared interests, mutual benefits
        if relation.trust_level < 0.8:
            return False
        
        # Check for shared threats or goals
        shared_interests = len(relation.shared_interests) > 0
        mutual_defense_need = random.random() < 0.3  # Simulate external threats
        
        return shared_interests or mutual_defense_need
    
    def _should_declare_war(self, relation: DiplomaticRelation, groups: Dict[str, Any],
                          world_events: List[Dict[str, Any]]) -> bool:
        """Check if groups should declare war."""
        # Very low trust, significant conflicts, power imbalance
        if relation.trust_level > 0.2:
            return False
        
        # Check for recent major incidents
        major_incidents = len([e for e in world_events if self._is_major_incident(e, relation)])
        
        # Check for resource competition or territorial disputes
        resource_conflict = "resource_competition" in relation.conflicting_interests
        territorial_dispute = "territorial_dispute" in relation.conflicting_interests
        
        # War more likely with major incidents and fundamental conflicts
        war_probability = major_incidents * 0.3
        if resource_conflict:
            war_probability += 0.2
        if territorial_dispute:
            war_probability += 0.3
        
        return random.random() < war_probability
    
    def _is_major_incident(self, event: Dict[str, Any], relation: DiplomaticRelation) -> bool:
        """Check if event is a major diplomatic incident."""
        event_type = event.get("type", "")
        major_types = ["treaty_violation", "military_aggression", "resource_theft", "diplomatic_insult"]
        return any(major_type in event_type for major_type in major_types)
    
    def _process_negotiations(self, agents: List[Any], groups: Dict[str, Any],
                            current_day: int) -> List[Dict[str, Any]]:
        """Process ongoing diplomatic negotiations."""
        events = []
        
        for negotiation_id, negotiation in list(self.negotiations.items()):
            # Update negotiation progress
            progress_events = self._update_negotiation_progress(negotiation, agents, groups, current_day)
            events.extend(progress_events)
            
            # Check for negotiation completion
            if negotiation.current_phase == NegotiationPhase.AGREEMENT:
                completion_event = self._complete_negotiation(negotiation, current_day)
                if completion_event:
                    events.append(completion_event)
                    del self.negotiations[negotiation_id]
            
            # Check for negotiation failure
            elif negotiation.current_phase == NegotiationPhase.DEADLOCK:
                if random.random() < 0.1:  # 10% chance of failure per day
                    failure_event = self._fail_negotiation(negotiation, current_day)
                    events.append(failure_event)
                    del self.negotiations[negotiation_id]
        
        return events
    
    def _update_negotiation_progress(self, negotiation: DiplomaticNegotiation, agents: List[Any],
                                   groups: Dict[str, Any], current_day: int) -> List[Dict[str, Any]]:
        """Update progress of a diplomatic negotiation."""
        events = []
        
        # Calculate progress based on various factors
        progress_factors = self._calculate_negotiation_factors(negotiation, agents, groups)
        
        # Update agreement probability
        old_probability = negotiation.agreement_probability
        base_change = 0.05  # 5% base progress per day
        
        # Apply factors
        factor_multiplier = 1.0
        for factor_name, factor_value in progress_factors.items():
            factor_config = self.negotiation_factors.get(factor_name, {})
            
            if factor_value == "high":
                factor_multiplier *= factor_config.get("high", 1.0)
            elif factor_value == "low":
                factor_multiplier *= factor_config.get("low", 1.0)
            else:
                factor_multiplier *= factor_config.get("medium", 1.0)
        
        progress_change = base_change * factor_multiplier
        negotiation.agreement_probability = max(0.0, min(1.0, negotiation.agreement_probability + progress_change))
        
        # Update phase based on progress
        old_phase = negotiation.current_phase
        new_phase = self._determine_negotiation_phase(negotiation)
        
        if new_phase != old_phase:
            negotiation.current_phase = new_phase
            events.append({
                "type": "negotiation_phase_change",
                "negotiation_id": negotiation.id,
                "treaty_type": negotiation.proposed_treaty_type.value,
                "old_phase": old_phase.value,
                "new_phase": new_phase.value,
                "agreement_probability": negotiation.agreement_probability,
                "day": current_day
            })
        
        # Increment negotiation rounds
        negotiation.negotiation_rounds += 1
        
        return events
    
    def _calculate_negotiation_factors(self, negotiation: DiplomaticNegotiation, agents: List[Any],
                                     groups: Dict[str, Any]) -> Dict[str, str]:
        """Calculate factors affecting negotiation progress."""
        factors = {}
        
        # Trust level between groups
        if len(negotiation.groups) >= 2:
            relation_key = self._get_relation_key(negotiation.groups[0], negotiation.groups[1])
            if relation_key in self.diplomatic_relations:
                relation = self.diplomatic_relations[relation_key]
                if relation.trust_level > 0.7:
                    factors["trust_level"] = "high"
                elif relation.trust_level < 0.4:
                    factors["trust_level"] = "low"
                else:
                    factors["trust_level"] = "medium"
        
        # Negotiator skill
        negotiator_skills = []
        for group_id, negotiator_name in negotiation.lead_negotiators.items():
            if negotiator_name in self.diplomatic_agents:
                skill = self.diplomatic_agents[negotiator_name].negotiation_skill
                negotiator_skills.append(skill)
        
        if negotiator_skills:
            avg_skill = sum(negotiator_skills) / len(negotiator_skills)
            if avg_skill > 0.7:
                factors["negotiator_skill"] = "expert"
            elif avg_skill < 0.4:
                factors["negotiator_skill"] = "novice"
            else:
                factors["negotiator_skill"] = "competent"
        
        # Time pressure
        if negotiation.time_pressure > 0.7:
            factors["time_pressure"] = "urgent"
        elif negotiation.time_pressure < 0.3:
            factors["time_pressure"] = "relaxed"
        else:
            factors["time_pressure"] = "moderate"
        
        # Economic incentive (placeholder)
        factors["economic_incentive"] = random.choice(["high", "medium", "low"])
        
        return factors
    
    def _determine_negotiation_phase(self, negotiation: DiplomaticNegotiation) -> NegotiationPhase:
        """Determine current negotiation phase."""
        probability = negotiation.agreement_probability
        rounds = negotiation.negotiation_rounds
        
        if probability > 0.9:
            return NegotiationPhase.AGREEMENT
        elif probability > 0.7:
            return NegotiationPhase.COMPROMISE
        elif probability < 0.2 and rounds > 5:
            return NegotiationPhase.DEADLOCK
        elif rounds > 10:
            return NegotiationPhase.DISCUSSION
        else:
            return NegotiationPhase.PROPOSAL
    
    def _complete_negotiation(self, negotiation: DiplomaticNegotiation, current_day: int) -> Optional[Dict[str, Any]]:
        """Complete a successful negotiation by creating a treaty."""
        # Create treaty from negotiation
        treaty = self._create_treaty_from_negotiation(negotiation, current_day)
        if treaty:
            self.treaties[treaty.id] = treaty
            
            # Update diplomatic relations
            for i, group1_id in enumerate(negotiation.groups):
                for group2_id in negotiation.groups[i+1:]:
                    relation_key = self._get_relation_key(group1_id, group2_id)
                    if relation_key in self.diplomatic_relations:
                        relation = self.diplomatic_relations[relation_key]
                        relation.treaties.append(treaty.id)
                        relation.trust_level = min(1.0, relation.trust_level + 0.1)  # Trust boost
            
            return {
                "type": "treaty_signed",
                "treaty_id": treaty.id,
                "treaty_name": treaty.name,
                "treaty_type": treaty.treaty_type.value,
                "signatory_groups": treaty.signatory_groups,
                "negotiation_duration": negotiation.negotiation_rounds,
                "day": current_day
            }
        
        return None
    
    def _create_treaty_from_negotiation(self, negotiation: DiplomaticNegotiation,
                                      current_day: int) -> Optional[DiplomaticTreaty]:
        """Create a treaty from a completed negotiation."""
        treaty_id = f"treaty_{negotiation.proposed_treaty_type.value}_{current_day}"
        treaty_type = negotiation.proposed_treaty_type
        
        # Get treaty template
        template = self.treaty_templates.get(treaty_type, {})
        
        # Generate treaty name
        treaty_name = self._generate_treaty_name(treaty_type, negotiation.groups)
        
        # Create treaty terms from template and negotiation
        terms = {}
        obligations = {}
        benefits = {}
        
        for group_id in negotiation.groups:
            obligations[group_id] = template.get("typical_terms", [])[:2]  # First 2 terms as obligations
            benefits[group_id] = template.get("typical_terms", [])[2:]     # Rest as benefits
        
        treaty = DiplomaticTreaty(
            id=treaty_id,
            name=treaty_name,
            treaty_type=treaty_type,
            signatory_groups=negotiation.groups.copy(),
            signed_day=current_day,
            
            terms=terms,
            obligations=obligations,
            benefits=benefits,
            duration=template.get("typical_duration"),
            
            compliance_score={group_id: 1.0 for group_id in negotiation.groups},
            violations=[],
            enforcement_mechanisms=["diplomatic_pressure", "economic_sanctions"],
            
            status="active",
            amendments=[],
            renewal_date=None,
            
            economic_impact={group_id: 0.0 for group_id in negotiation.groups},
            political_impact={group_id: 0.0 for group_id in negotiation.groups},
            cultural_impact={group_id: 0.0 for group_id in negotiation.groups}
        )
        
        # Set renewal date if treaty has duration
        if treaty.duration:
            treaty.renewal_date = current_day + treaty.duration
        
        return treaty
    
    def _generate_treaty_name(self, treaty_type: TreatyType, groups: List[str]) -> str:
        """Generate a name for the treaty."""
        type_names = {
            TreatyType.TRADE_AGREEMENT: "Trade Pact",
            TreatyType.MUTUAL_DEFENSE: "Defense Alliance",
            TreatyType.NON_AGGRESSION: "Peace Treaty",
            TreatyType.CULTURAL_EXCHANGE: "Cultural Accord",
            TreatyType.TERRITORIAL: "Border Agreement",
            TreatyType.TRIBUTE: "Tribute Arrangement"
        }
        
        base_name = type_names.get(treaty_type, "Agreement")
        
        if len(groups) == 2:
            return f"{groups[0]}-{groups[1]} {base_name}"
        else:
            return f"Multilateral {base_name}"
    
    def _fail_negotiation(self, negotiation: DiplomaticNegotiation, current_day: int) -> Dict[str, Any]:
        """Handle a failed negotiation."""
        # Decrease trust between negotiating groups
        for i, group1_id in enumerate(negotiation.groups):
            for group2_id in negotiation.groups[i+1:]:
                relation_key = self._get_relation_key(group1_id, group2_id)
                if relation_key in self.diplomatic_relations:
                    relation = self.diplomatic_relations[relation_key]
                    relation.trust_level = max(0.0, relation.trust_level - 0.05)  # Trust penalty
        
        return {
            "type": "negotiation_failed",
            "treaty_type": negotiation.proposed_treaty_type.value,
            "groups": negotiation.groups,
            "failure_reason": "irreconcilable_differences",
            "negotiation_duration": negotiation.negotiation_rounds,
            "day": current_day
        }
    
    def _check_negotiation_opportunities(self, groups: Dict[str, Any], current_day: int) -> List[Dict[str, Any]]:
        """Check for new negotiation opportunities."""
        events = []
        
        # Check each diplomatic relation for negotiation opportunities
        for relation_key, relation in self.diplomatic_relations.items():
            # Skip if already negotiating
            if relation.pending_negotiations:
                continue
            
            # Check for negotiation triggers
            negotiation_opportunity = self._identify_negotiation_opportunity(relation, groups)
            
            if negotiation_opportunity:
                # Start new negotiation
                negotiation = self._start_negotiation(relation, negotiation_opportunity, groups, current_day)
                if negotiation:
                    self.negotiations[negotiation.id] = negotiation
                    relation.pending_negotiations.append(negotiation.id)
                    
                    events.append({
                        "type": "negotiation_started",
                        "negotiation_id": negotiation.id,
                        "groups": negotiation.groups,
                        "treaty_type": negotiation.proposed_treaty_type.value,
                        "trigger": negotiation_opportunity,
                        "day": current_day
                    })
        
        return events
    
    def _identify_negotiation_opportunity(self, relation: DiplomaticRelation, groups: Dict[str, Any]) -> Optional[str]:
        """Identify what type of negotiation opportunity exists."""
        # Check various conditions that might trigger negotiations
        
        # Trade agreement if high economic potential
        if (relation.status in [DiplomaticStatus.NEUTRAL, DiplomaticStatus.FRIENDLY] and
            relation.trust_level > 0.5 and
            self._have_trade_potential(relation, groups)):
            return TreatyType.TRADE_AGREEMENT.value
        
        # Mutual defense if external threats
        if (relation.status == DiplomaticStatus.FRIENDLY and
            relation.trust_level > 0.7 and
            self._have_common_threats(relation, groups)):
            return TreatyType.MUTUAL_DEFENSE.value
        
        # Non-aggression if hostile but not at war
        if (relation.status == DiplomaticStatus.HOSTILE and
            relation.trust_level > 0.3):
            return TreatyType.NON_AGGRESSION.value
        
        # Cultural exchange if high cultural affinity
        if (relation.status in [DiplomaticStatus.FRIENDLY, DiplomaticStatus.ALLIED] and
            relation.cultural_affinity > 0.6):
            return TreatyType.CULTURAL_EXCHANGE.value
        
        # Territorial agreement if border disputes
        if "territorial_dispute" in relation.conflicting_interests:
            return TreatyType.TERRITORIAL.value
        
        return None
    
    def _have_trade_potential(self, relation: DiplomaticRelation, groups: Dict[str, Any]) -> bool:
        """Check if groups have trade potential."""
        # This would check economic compatibility, resource differences, etc.
        return random.random() < 0.4  # 40% chance of trade potential
    
    def _have_common_threats(self, relation: DiplomaticRelation, groups: Dict[str, Any]) -> bool:
        """Check if groups face common external threats."""
        # This would check for hostile relations with third parties
        return random.random() < 0.3  # 30% chance of common threats
    
    def _start_negotiation(self, relation: DiplomaticRelation, opportunity: str, groups: Dict[str, Any],
                         current_day: int) -> Optional[DiplomaticNegotiation]:
        """Start a new diplomatic negotiation."""
        negotiation_id = f"negotiation_{opportunity}_{current_day}"
        treaty_type = TreatyType(opportunity)
        
        # Find negotiators
        negotiators = self._assign_negotiators(relation, groups)
        if not negotiators:
            return None
        
        negotiation = DiplomaticNegotiation(
            id=negotiation_id,
            groups=[relation.group1_id, relation.group2_id],
            proposed_treaty_type=treaty_type,
            started_day=current_day,
            
            current_phase=NegotiationPhase.PROPOSAL,
            lead_negotiators=negotiators,
            proposed_terms={},
            
            positions={},
            concessions_made={},
            deadlock_issues=[],
            
            time_pressure=random.uniform(0.2, 0.8),
            third_party_influence={},
            public_pressure=random.uniform(0.3, 0.7),
            
            agreement_probability=0.5,  # Start at neutral
            negotiation_rounds=0,
            estimated_completion=None
        )
        
        return negotiation
    
    def _assign_negotiators(self, relation: DiplomaticRelation, groups: Dict[str, Any]) -> Dict[str, str]:
        """Assign negotiators for each group."""
        negotiators = {}
        
        for group_id in [relation.group1_id, relation.group2_id]:
            # Find suitable negotiator from diplomatic agents or group leaders
            negotiator = self._find_group_negotiator(group_id, groups)
            if negotiator:
                negotiators[group_id] = negotiator
        
        return negotiators if len(negotiators) == 2 else {}
    
    def _find_group_negotiator(self, group_id: str, groups: Dict[str, Any]) -> Optional[str]:
        """Find a suitable negotiator for a group."""
        # Check existing diplomatic agents
        for agent_name, agent in self.diplomatic_agents.items():
            if agent.representing_group == group_id:
                return agent_name
        
        # Find group leader as fallback
        if group_id in groups:
            group = groups[group_id]
            if hasattr(group, 'leaders') and group.leaders:
                return group.leaders[0]
        
        return None
    
    def _monitor_treaty_compliance(self, groups: Dict[str, Any], world_events: List[Dict[str, Any]],
                                 current_day: int) -> List[Dict[str, Any]]:
        """Monitor compliance with existing treaties."""
        events = []
        
        for treaty_id, treaty in self.treaties.items():
            if treaty.status != "active":
                continue
            
            # Check compliance for each signatory
            for group_id in treaty.signatory_groups:
                compliance_change = self._calculate_compliance_change(treaty, group_id, world_events)
                
                old_compliance = treaty.compliance_score[group_id]
                new_compliance = max(0.0, min(1.0, old_compliance + compliance_change))
                treaty.compliance_score[group_id] = new_compliance
                
                # Detect violations
                if new_compliance < 0.5 and old_compliance >= 0.5:
                    violation_event = self._record_treaty_violation(treaty, group_id, current_day)
                    events.append(violation_event)
                
                # Report significant compliance changes
                elif abs(new_compliance - old_compliance) > 0.2:
                    events.append({
                        "type": "treaty_compliance_change",
                        "treaty_id": treaty_id,
                        "violating_group": group_id,
                        "compliance_change": new_compliance - old_compliance,
                        "new_compliance": new_compliance,
                        "day": current_day
                    })
            
            # Check for treaty renewal
            if treaty.renewal_date and current_day >= treaty.renewal_date:
                renewal_event = self._handle_treaty_renewal(treaty, groups, current_day)
                if renewal_event:
                    events.append(renewal_event)
        
        return events
    
    def _calculate_compliance_change(self, treaty: DiplomaticTreaty, group_id: str,
                                   world_events: List[Dict[str, Any]]) -> float:
        """Calculate change in treaty compliance."""
        compliance_change = 0.0
        
        # Check for events that affect compliance
        for event in world_events:
            if self._affects_treaty_compliance(event, treaty, group_id):
                if self._is_treaty_violation_event(event, treaty):
                    compliance_change -= 0.2
                elif self._is_treaty_compliance_event(event, treaty):
                    compliance_change += 0.1
        
        # Natural decay without positive reinforcement
        compliance_change -= 0.01
        
        return compliance_change
    
    def _affects_treaty_compliance(self, event: Dict[str, Any], treaty: DiplomaticTreaty, group_id: str) -> bool:
        """Check if event affects treaty compliance."""
        # This would check if event involves the group and relates to treaty terms
        event_type = event.get("type", "")
        
        # Check if event involves this group
        participants = event.get("participants", [])
        if group_id not in participants and group_id not in event.get("groups", []):
            return False
        
        # Check if event relates to treaty type
        treaty_related_events = {
            TreatyType.TRADE_AGREEMENT: ["trade", "economic"],
            TreatyType.MUTUAL_DEFENSE: ["military", "conflict", "defense"],
            TreatyType.NON_AGGRESSION: ["conflict", "aggression", "attack"],
            TreatyType.CULTURAL_EXCHANGE: ["cultural", "knowledge", "education"],
            TreatyType.TERRITORIAL: ["territorial", "border", "expansion"]
        }
        
        related_keywords = treaty_related_events.get(treaty.treaty_type, [])
        return any(keyword in event_type for keyword in related_keywords)
    
    def _is_treaty_violation_event(self, event: Dict[str, Any], treaty: DiplomaticTreaty) -> bool:
        """Check if event represents a treaty violation."""
        event_type = event.get("type", "")
        
        violation_patterns = {
            TreatyType.TRADE_AGREEMENT: ["trade_disruption", "embargo", "tariff_increase"],
            TreatyType.MUTUAL_DEFENSE: ["refused_aid", "separate_peace", "betrayal"],
            TreatyType.NON_AGGRESSION: ["attack", "aggression", "invasion"],
            TreatyType.CULTURAL_EXCHANGE: ["cultural_suppression", "knowledge_hoarding"],
            TreatyType.TERRITORIAL: ["border_violation", "territorial_expansion"]
        }
        
        violation_keywords = violation_patterns.get(treaty.treaty_type, [])
        return any(keyword in event_type for keyword in violation_keywords)
    
    def _is_treaty_compliance_event(self, event: Dict[str, Any], treaty: DiplomaticTreaty) -> bool:
        """Check if event represents good treaty compliance."""
        event_type = event.get("type", "")
        
        compliance_patterns = {
            TreatyType.TRADE_AGREEMENT: ["trade_facilitation", "tariff_reduction", "commercial_cooperation"],
            TreatyType.MUTUAL_DEFENSE: ["military_aid", "joint_defense", "intelligence_sharing"],
            TreatyType.NON_AGGRESSION: ["peaceful_resolution", "conflict_avoidance"],
            TreatyType.CULTURAL_EXCHANGE: ["knowledge_sharing", "cultural_mission", "educational_exchange"],
            TreatyType.TERRITORIAL: ["border_respect", "territorial_agreement"]
        }
        
        compliance_keywords = compliance_patterns.get(treaty.treaty_type, [])
        return any(keyword in event_type for keyword in compliance_keywords)
    
    def _record_treaty_violation(self, treaty: DiplomaticTreaty, violating_group: str,
                               current_day: int) -> Dict[str, Any]:
        """Record a treaty violation."""
        violation = {
            "violating_group": violating_group,
            "violation_type": "compliance_failure",
            "day": current_day,
            "severity": "moderate",
            "consequences": []
        }
        
        treaty.violations.append(violation)
        
        # Apply diplomatic consequences
        self._apply_violation_consequences(treaty, violating_group, violation)
        
        return {
            "type": "treaty_violation",
            "treaty_id": treaty.id,
            "treaty_name": treaty.name,
            "violating_group": violating_group,
            "violation_severity": violation["severity"],
            "day": current_day
        }
    
    def _apply_violation_consequences(self, treaty: DiplomaticTreaty, violating_group: str,
                                    violation: Dict[str, Any]) -> None:
        """Apply consequences for treaty violation."""
        # Decrease trust with other signatories
        for group_id in treaty.signatory_groups:
            if group_id != violating_group:
                relation_key = self._get_relation_key(violating_group, group_id)
                if relation_key in self.diplomatic_relations:
                    relation = self.diplomatic_relations[relation_key]
                    relation.trust_level = max(0.0, relation.trust_level - 0.15)
                    violation["consequences"].append(f"trust_decrease_with_{group_id}")
        
        # Possible economic sanctions or diplomatic protests
        if random.random() < 0.6:  # 60% chance
            violation["consequences"].append("diplomatic_protest")
        
        if random.random() < 0.3:  # 30% chance
            violation["consequences"].append("economic_sanctions")
    
    def _handle_treaty_renewal(self, treaty: DiplomaticTreaty, groups: Dict[str, Any],
                             current_day: int) -> Optional[Dict[str, Any]]:
        """Handle treaty renewal process."""
        # Calculate renewal probability based on compliance and satisfaction
        avg_compliance = sum(treaty.compliance_score.values()) / len(treaty.compliance_score)
        
        # Check if all parties want to renew
        renewal_support = 0
        for group_id in treaty.signatory_groups:
            if avg_compliance > 0.7 and self._group_supports_renewal(treaty, group_id, groups):
                renewal_support += 1
        
        renewal_threshold = len(treaty.signatory_groups)  # Need unanimous support
        
        if renewal_support >= renewal_threshold:
            # Renew treaty
            template = self.treaty_templates.get(treaty.treaty_type, {})
            new_duration = template.get("typical_duration", 365)
            treaty.renewal_date = current_day + new_duration
            
            return {
                "type": "treaty_renewed",
                "treaty_id": treaty.id,
                "treaty_name": treaty.name,
                "new_duration": new_duration,
                "compliance_score": avg_compliance,
                "day": current_day
            }
        else:
            # Treaty expires
            treaty.status = "terminated"
            
            # Remove from diplomatic relations
            for i, group1_id in enumerate(treaty.signatory_groups):
                for group2_id in treaty.signatory_groups[i+1:]:
                    relation_key = self._get_relation_key(group1_id, group2_id)
                    if relation_key in self.diplomatic_relations:
                        relation = self.diplomatic_relations[relation_key]
                        if treaty.id in relation.treaties:
                            relation.treaties.remove(treaty.id)
            
            return {
                "type": "treaty_expired",
                "treaty_id": treaty.id,
                "treaty_name": treaty.name,
                "reason": "renewal_failed",
                "final_compliance": avg_compliance,
                "day": current_day
            }
    
    def _group_supports_renewal(self, treaty: DiplomaticTreaty, group_id: str, groups: Dict[str, Any]) -> bool:
        """Check if a group supports treaty renewal."""
        # Check benefits vs costs of treaty
        group_compliance = treaty.compliance_score.get(group_id, 0.5)
        
        # Groups more likely to renew if they're compliant and benefiting
        support_probability = group_compliance * 0.8
        
        # Check if treaty has been beneficial
        economic_benefit = treaty.economic_impact.get(group_id, 0.0)
        if economic_benefit > 0:
            support_probability += 0.2
        
        return random.random() < support_probability
    
    def _manage_diplomatic_agents(self, agents: List[Any], groups: Dict[str, Any],
                                current_day: int) -> List[Dict[str, Any]]:
        """Manage diplomatic agents and their assignments."""
        events = []
        
        # Check for new diplomatic agent appointments
        appointment_events = self._check_agent_appointments(agents, groups, current_day)
        events.extend(appointment_events)
        
        # Update existing diplomatic agents
        for agent_name, diplomatic_agent in self.diplomatic_agents.items():
            # Update agent performance and effectiveness
            self._update_agent_performance(diplomatic_agent, current_day)
            
            # Check for agent reassignment or recall
            if random.random() < 0.02:  # 2% chance per day
                reassignment_event = self._consider_agent_reassignment(diplomatic_agent, groups, current_day)
                if reassignment_event:
                    events.append(reassignment_event)
        
        return events
    
    def _check_agent_appointments(self, agents: List[Any], groups: Dict[str, Any],
                                current_day: int) -> List[Dict[str, Any]]:
        """Check for new diplomatic agent appointments."""
        events = []
        
        # Groups with active diplomatic relations need agents
        active_diplomatic_groups = set()
        for relation in self.diplomatic_relations.values():
            if relation.status in [DiplomaticStatus.FRIENDLY, DiplomaticStatus.ALLIED]:
                active_diplomatic_groups.add(relation.group1_id)
                active_diplomatic_groups.add(relation.group2_id)
        
        for group_id in active_diplomatic_groups:
            # Check if group needs more diplomatic agents
            current_agents = [a for a in self.diplomatic_agents.values() if a.representing_group == group_id]
            
            if len(current_agents) < 2:  # Groups can have up to 2 diplomatic agents
                # Find suitable agent to appoint
                suitable_agent = self._find_suitable_diplomatic_agent(group_id, agents, groups)
                
                if suitable_agent:
                    diplomatic_agent = self._appoint_diplomatic_agent(suitable_agent, group_id, current_day)
                    self.diplomatic_agents[suitable_agent.name] = diplomatic_agent
                    
                    events.append({
                        "type": "diplomatic_agent_appointed",
                        "agent_name": suitable_agent.name,
                        "representing_group": group_id,
                        "diplomatic_role": diplomatic_agent.diplomatic_role,
                        "day": current_day
                    })
        
        return events
    
    def _find_suitable_diplomatic_agent(self, group_id: str, agents: List[Any], groups: Dict[str, Any]) -> Optional[Any]:
        """Find a suitable agent for diplomatic appointment."""
        if group_id not in groups:
            return None
        
        group = groups[group_id]
        
        # Find agents who are members of this group
        group_members = []
        if hasattr(group, 'members'):
            for member_name in group.members:
                agent = next((a for a in agents if a.name == member_name and a.is_alive), None)
                if agent:
                    group_members.append(agent)
        
        if not group_members:
            return None
        
        # Score agents for diplomatic suitability
        best_agent = None
        best_score = 0.0
        
        for agent in group_members:
            # Skip if already a diplomatic agent
            if agent.name in self.diplomatic_agents:
                continue
            
            score = 0.0
            
            # Reputation and social skills
            if hasattr(agent, 'reputation'):
                score += agent.reputation * 0.4
            
            if hasattr(agent, 'relationships'):
                score += min(0.3, len(agent.relationships) / 10.0)
            
            # Relevant specializations
            if hasattr(agent, 'specialization'):
                if agent.specialization in ["leader", "scholar", "merchant"]:
                    score += 0.3
            
            # Age factor - not too young, not too old
            age_factor = 1.0 - abs(agent.age - 40) / 40.0
            score += max(0, age_factor) * 0.2
            
            if score > best_score:
                best_score = score
                best_agent = agent
        
        return best_agent if best_score >= 0.6 else None
    
    def _appoint_diplomatic_agent(self, agent: Any, group_id: str, current_day: int) -> DiplomaticAgent:
        """Appoint an agent to diplomatic service."""
        
        # Determine diplomatic role
        roles = ["ambassador", "envoy", "trade_representative", "cultural_attaché"]
        role = random.choice(roles)
        
        diplomatic_agent = DiplomaticAgent(
            agent_name=agent.name,
            diplomatic_role=role,
            representing_group=group_id,
            assigned_location=agent.location,
            assignment_day=current_day,
            
            negotiation_skill=random.uniform(0.3, 0.8),
            cultural_understanding=random.uniform(0.4, 0.7),
            languages_known=[],
            reputation=getattr(agent, 'reputation', 0.5),
            
            active_negotiations=[],
            diplomatic_contacts={},
            cultural_knowledge={},
            
            successful_negotiations=0,
            failed_negotiations=0,
            diplomatic_incidents=[],
            
            loyalty=0.8,
            foreign_influence={},
            effectiveness_rating=0.5
        )
        
        return diplomatic_agent
    
    def _update_agent_performance(self, diplomatic_agent: DiplomaticAgent, current_day: int) -> None:
        """Update diplomatic agent performance metrics."""
        # Agents improve with experience
        total_negotiations = diplomatic_agent.successful_negotiations + diplomatic_agent.failed_negotiations
        
        if total_negotiations > 0:
            success_rate = diplomatic_agent.successful_negotiations / total_negotiations
            diplomatic_agent.effectiveness_rating = min(1.0, success_rate * 1.2)
            
            # Skills improve with practice
            diplomatic_agent.negotiation_skill = min(1.0, diplomatic_agent.negotiation_skill + 0.01)
    
    def _consider_agent_reassignment(self, diplomatic_agent: DiplomaticAgent, groups: Dict[str, Any],
                                   current_day: int) -> Optional[Dict[str, Any]]:
        """Consider reassigning or recalling a diplomatic agent."""
        # Poor performance might lead to recall
        if diplomatic_agent.effectiveness_rating < 0.3:
            # Recall agent
            del self.diplomatic_agents[diplomatic_agent.agent_name]
            
            return {
                "type": "diplomatic_agent_recalled",
                "agent_name": diplomatic_agent.agent_name,
                "representing_group": diplomatic_agent.representing_group,
                "reason": "poor_performance",
                "effectiveness": diplomatic_agent.effectiveness_rating,
                "day": current_day
            }
        
        return None
    
    def _process_diplomatic_crises(self, groups: Dict[str, Any], world_events: List[Dict[str, Any]],
                                 current_day: int) -> List[Dict[str, Any]]:
        """Process diplomatic crises and incidents."""
        events = []
        
        # Check for new diplomatic crises arising from world events
        for event in world_events:
            if self._creates_diplomatic_crisis(event):
                crisis_event = self._handle_diplomatic_crisis(event, groups, current_day)
                if crisis_event:
                    events.append(crisis_event)
                    self.diplomatic_crises.append(crisis_event)
        
        # Update ongoing diplomatic crises
        for crisis in self.diplomatic_crises[-10:]:  # Only recent crises
            if current_day - crisis["day"] < 30:  # Active for 30 days
                resolution_event = self._attempt_crisis_resolution(crisis, groups, current_day)
                if resolution_event:
                    events.append(resolution_event)
        
        return events
    
    def _creates_diplomatic_crisis(self, event: Dict[str, Any]) -> bool:
        """Check if world event creates a diplomatic crisis."""
        crisis_triggering_events = [
            "treaty_violation", "territorial_dispute", "trade_embargo",
            "diplomatic_insult", "military_incident", "refugee_crisis"
        ]
        
        event_type = event.get("type", "")
        return any(trigger in event_type for trigger in crisis_triggering_events)
    
    def _handle_diplomatic_crisis(self, event: Dict[str, Any], groups: Dict[str, Any],
                                current_day: int) -> Optional[Dict[str, Any]]:
        """Handle a new diplomatic crisis."""
        # Identify affected groups and diplomatic relations
        affected_groups = event.get("groups", event.get("participants", []))
        
        if len(affected_groups) >= 2:
            # Find diplomatic relation
            relation_key = self._get_relation_key(affected_groups[0], affected_groups[1])
            
            if relation_key in self.diplomatic_relations:
                relation = self.diplomatic_relations[relation_key]
                
                # Crisis damages trust and may change status
                relation.trust_level = max(0.0, relation.trust_level - 0.2)
                
                # Record incident
                incident = {
                    "type": event.get("type", "unknown"),
                    "day": current_day,
                    "severity": "high",
                    "resolution_attempts": []
                }
                relation.recent_incidents.append(incident)
                
                return {
                    "type": "diplomatic_crisis",
                    "crisis_trigger": event.get("type", "unknown"),
                    "affected_groups": affected_groups,
                    "trust_impact": -0.2,
                    "day": current_day
                }
        
        return None
    
    def _attempt_crisis_resolution(self, crisis: Dict[str, Any], groups: Dict[str, Any],
                                 current_day: int) -> Optional[Dict[str, Any]]:
        """Attempt to resolve a diplomatic crisis."""
        affected_groups = crisis.get("affected_groups", [])
        
        if len(affected_groups) >= 2:
            relation_key = self._get_relation_key(affected_groups[0], affected_groups[1])
            
            if relation_key in self.diplomatic_relations:
                relation = self.diplomatic_relations[relation_key]
                
                # Higher trust makes resolution more likely
                resolution_probability = relation.trust_level * 0.3
                
                if random.random() < resolution_probability:
                    # Crisis resolved
                    relation.trust_level = min(1.0, relation.trust_level + 0.1)
                    
                    return {
                        "type": "diplomatic_crisis_resolved",
                        "original_crisis": crisis.get("crisis_trigger", "unknown"),
                        "affected_groups": affected_groups,
                        "resolution_method": "diplomatic_negotiation",
                        "trust_recovery": 0.1,
                        "day": current_day
                    }
        
        return None
    
    def _update_global_trends(self, groups: Dict[str, Any], current_day: int) -> None:
        """Update global diplomatic trends."""
        # Calculate overall diplomatic climate
        total_relations = len(self.diplomatic_relations)
        if total_relations == 0:
            return
        
        # Count relations by status
        status_counts = defaultdict(int)
        avg_trust = 0.0
        
        for relation in self.diplomatic_relations.values():
            status_counts[relation.status.value] += 1
            avg_trust += relation.trust_level
        
        avg_trust /= total_relations
        
        # Update trends
        self.global_diplomatic_trends[current_day] = {
            "average_trust": avg_trust,
            "peaceful_relations": (status_counts["friendly"] + status_counts["allied"]) / total_relations,
            "hostile_relations": (status_counts["hostile"] + status_counts["war"]) / total_relations,
            "total_treaties": len([t for t in self.treaties.values() if t.status == "active"]),
            "diplomatic_activity": len(self.negotiations)
        }
        
        # Keep only recent trends
        if len(self.global_diplomatic_trends) > 365:
            old_days = [day for day in self.global_diplomatic_trends.keys() if current_day - day > 365]
            for day in old_days:
                del self.global_diplomatic_trends[day]
    
    def get_diplomacy_summary(self) -> Dict[str, Any]:
        """Get comprehensive diplomatic system summary."""
        summary = {
            "total_diplomatic_relations": len(self.diplomatic_relations),
            "relations_by_status": {},
            "active_treaties": len([t for t in self.treaties.values() if t.status == "active"]),
            "treaties_by_type": {},
            "ongoing_negotiations": len(self.negotiations),
            "diplomatic_agents": len(self.diplomatic_agents),
            "recent_crises": len(self.diplomatic_crises[-10:]),
            "average_trust": 0.0,
            "diplomatic_complexity": 0.0
        }
        
        # Count relations by status
        for relation in self.diplomatic_relations.values():
            status = relation.status.value
            summary["relations_by_status"][status] = summary["relations_by_status"].get(status, 0) + 1
        
        # Count treaties by type
        for treaty in self.treaties.values():
            if treaty.status == "active":
                treaty_type = treaty.treaty_type.value
                summary["treaties_by_type"][treaty_type] = summary["treaties_by_type"].get(treaty_type, 0) + 1
        
        # Calculate average trust
        if self.diplomatic_relations:
            total_trust = sum(r.trust_level for r in self.diplomatic_relations.values())
            summary["average_trust"] = total_trust / len(self.diplomatic_relations)
        
        # Calculate diplomatic complexity
        complexity_factors = [
            len(self.diplomatic_relations) / 10.0,  # Number of relations
            len(self.treaties) / 5.0,               # Number of treaties
            len(self.negotiations) / 3.0,           # Active negotiations
            len(self.diplomatic_agents) / 5.0       # Diplomatic infrastructure
        ]
        
        summary["diplomatic_complexity"] = min(1.0, sum(complexity_factors) / len(complexity_factors))
        
        return summary 