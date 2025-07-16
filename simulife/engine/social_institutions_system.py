"""
Social Institutions Emergence System for SimuLife
Creates complex organizational structures that emerge naturally from community needs,
building on existing group dynamics to form governments, formal education, and institutions.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict


class InstitutionType(Enum):
    """Types of emergent social institutions."""
    GOVERNMENT = "government"           # Formal governance structures
    FORMAL_SCHOOL = "formal_school"     # Organized education systems
    JUDICIARY = "judiciary"             # Legal and justice systems
    MILITARY = "military"               # Organized defense forces
    RELIGION = "religion"               # Formal religious organizations
    COMMERCE = "commerce"               # Trade and economic institutions
    BUREAUCRACY = "bureaucracy"         # Administrative and record-keeping
    DIPLOMACY = "diplomacy"             # Inter-group relations management
    INFRASTRUCTURE = "infrastructure"   # Public works and maintenance
    CULTURAL_ACADEMY = "cultural_academy" # Advanced arts and knowledge centers


class GovernanceType(Enum):
    """Types of government that can emerge."""
    COUNCIL_DEMOCRACY = "council_democracy"     # Elected council leadership
    MERITOCRACY = "meritocracy"                # Rule by most skilled/wise
    THEOCRACY = "theocracy"                    # Religious leadership
    AUTOCRACY = "autocracy"                    # Single strong leader
    CONFEDERATION = "confederation"             # Alliance of groups
    COLLECTIVE = "collective"                   # Consensus-based decisions
    TECHNOCRACY = "technocracy"                # Rule by technical experts


class InstitutionStatus(Enum):
    """Development status of institutions."""
    FORMING = "forming"                 # Just beginning to organize
    ESTABLISHING = "establishing"       # Building structure and procedures
    FUNCTIONING = "functioning"         # Operating effectively
    EXPANDING = "expanding"             # Growing influence and scope
    DOMINANT = "dominant"               # Major community influence
    DECLINING = "declining"             # Losing effectiveness
    TRANSFORMING = "transforming"       # Evolving into new form


@dataclass
class SocialInstitution:
    """Represents an emergent social institution."""
    id: str
    name: str
    institution_type: InstitutionType
    governance_type: Optional[GovernanceType]
    founding_day: int
    founding_location: str
    
    # Leadership and membership
    leadership_structure: Dict[str, List[str]]  # roles -> agent names
    core_members: Set[str]                      # Essential participants
    affiliated_members: Set[str]                # Associated participants
    citizen_base: Set[str]                      # Broader population served
    
    # Organizational structure
    departments: Dict[str, Dict[str, Any]]      # Specialized divisions
    procedures: List[str]                       # Established processes
    laws_and_rules: List[Dict[str, Any]]        # Formal regulations
    
    # Resources and influence
    controlled_resources: Dict[str, float]      # Resources managed
    budget: Dict[str, float]                    # Resource allocation
    territories: Set[str]                       # Geographic influence
    jurisdiction: Dict[str, Any]                # Areas of authority
    
    # Status and development
    status: InstitutionStatus
    legitimacy: float                           # 0.0-1.0 community acceptance
    effectiveness: float                        # 0.0-1.0 how well it functions
    corruption_level: float                     # 0.0-1.0 institutional decay
    
    # Historical tracking
    founding_crisis: Optional[str]              # Crisis that led to formation
    major_decisions: List[Dict[str, Any]]       # Important institutional decisions
    reforms: List[Dict[str, Any]]               # Changes and adaptations
    conflicts: List[str]                        # Disputes and challenges
    
    # Performance metrics
    services_provided: List[str]                # What the institution does
    success_metrics: Dict[str, float]           # Performance indicators
    public_satisfaction: float                  # 0.0-1.0 citizen satisfaction


@dataclass
class InstitutionalCrisis:
    """Represents a crisis that may drive institutional formation."""
    crisis_type: str
    severity: float                             # 0.0-1.0 impact level
    affected_locations: Set[str]
    affected_population: Set[str]
    resolution_requirements: List[str]          # What's needed to solve it
    time_pressure: int                          # Days until crisis worsens
    
    # Institutional response tracking
    attempted_solutions: List[Dict[str, Any]]
    institutional_responses: Dict[str, Any]     # Which institutions responded
    outcome: Optional[str]                      # Final resolution


class SocialInstitutionsSystem:
    """
    Manages the emergence and evolution of complex social institutions.
    """
    
    def __init__(self):
        self.institutions: Dict[str, SocialInstitution] = {}
        self.active_crises: List[InstitutionalCrisis] = []
        self.institutional_events: List[Dict[str, Any]] = []
        
        # Configuration for institution formation
        self.formation_thresholds = self._initialize_formation_thresholds()
        self.governance_templates = self._initialize_governance_templates()
        self.crisis_types = self._initialize_crisis_types()
        
        # Tracking institutional development
        self.institutional_history: List[Dict[str, Any]] = []
        self.legitimacy_factors = self._initialize_legitimacy_factors()
    
    def _initialize_formation_thresholds(self) -> Dict[str, Dict[str, Any]]:
        """Initialize requirements for different institution types to form."""
        return {
            "government": {
                "min_population": 15,
                "min_groups": 3,
                "required_crises": ["resource_conflict", "inter_group_dispute", "population_pressure"],
                "required_skills": ["leadership", "negotiation", "organization"],
                "min_community_complexity": 0.6
            },
            "formal_school": {
                "min_population": 12,
                "min_groups": 2,
                "required_specialists": ["teacher", "scholar"],
                "required_knowledge_base": 5,  # Number of cultural elements
                "min_community_complexity": 0.4
            },
            "judiciary": {
                "min_population": 18,
                "min_groups": 3,
                "required_crises": ["inter_group_conflict", "resource_dispute"],
                "required_institutions": ["government"],
                "min_community_complexity": 0.7
            },
            "military": {
                "min_population": 20,
                "min_groups": 2,
                "required_crises": ["external_threat", "large_conflict"],
                "required_specialists": ["guardian", "leader"],
                "min_community_complexity": 0.5
            },
            "religion": {
                "min_population": 8,
                "min_groups": 1,
                "required_specialists": ["mystic"],
                "required_cultural_elements": ["rituals", "beliefs"],
                "min_community_complexity": 0.3
            },
            "commerce": {
                "min_population": 15,
                "min_groups": 3,
                "required_specialists": ["merchant"],
                "required_trade_volume": 10,  # Number of trade events
                "min_community_complexity": 0.5
            },
            "bureaucracy": {
                "min_population": 25,
                "min_groups": 4,
                "required_institutions": ["government"],
                "required_complexity": 0.8,
                "min_community_complexity": 0.8
            }
        }
    
    def _initialize_governance_templates(self) -> Dict[GovernanceType, Dict[str, Any]]:
        """Initialize templates for different governance types."""
        return {
            GovernanceType.COUNCIL_DEMOCRACY: {
                "leadership_roles": ["council_leader", "council_member", "representative"],
                "decision_method": "majority_vote",
                "term_limits": True,
                "selection_method": "election",
                "power_distribution": "shared",
                "typical_policies": ["resource_sharing", "conflict_mediation", "community_projects"]
            },
            GovernanceType.MERITOCRACY: {
                "leadership_roles": ["chief_administrator", "department_head", "advisor"],
                "decision_method": "expert_consensus",
                "term_limits": False,
                "selection_method": "skill_assessment",
                "power_distribution": "hierarchical",
                "typical_policies": ["skill_development", "knowledge_preservation", "innovation_support"]
            },
            GovernanceType.THEOCRACY: {
                "leadership_roles": ["high_priest", "spiritual_advisor", "temple_guardian"],
                "decision_method": "spiritual_guidance",
                "term_limits": False,
                "selection_method": "divine_calling",
                "power_distribution": "centralized",
                "typical_policies": ["moral_guidance", "spiritual_practices", "community_rituals"]
            },
            GovernanceType.AUTOCRACY: {
                "leadership_roles": ["supreme_leader", "lieutenant", "enforcer"],
                "decision_method": "leader_decree",
                "term_limits": False,
                "selection_method": "strength_contest",
                "power_distribution": "concentrated",
                "typical_policies": ["order_maintenance", "resource_control", "expansion"]
            },
            GovernanceType.CONFEDERATION: {
                "leadership_roles": ["group_representative", "coordinator", "mediator"],
                "decision_method": "group_consensus",
                "term_limits": True,
                "selection_method": "group_appointment",
                "power_distribution": "federated",
                "typical_policies": ["inter_group_cooperation", "trade_facilitation", "mutual_defense"]
            }
        }
    
    def _initialize_crisis_types(self) -> Dict[str, Dict[str, Any]]:
        """Initialize crisis types that drive institutional formation."""
        return {
            "resource_conflict": {
                "description": "Disputes over scarce resources",
                "triggers": ["resource_scarcity", "population_pressure"],
                "institutional_solutions": ["government", "judiciary", "commerce"],
                "urgency": 0.8
            },
            "inter_group_dispute": {
                "description": "Conflicts between different groups",
                "triggers": ["territorial_disputes", "ideological_differences"],
                "institutional_solutions": ["government", "diplomacy", "judiciary"],
                "urgency": 0.7
            },
            "knowledge_loss": {
                "description": "Important cultural knowledge at risk",
                "triggers": ["elder_deaths", "cultural_decay"],
                "institutional_solutions": ["formal_school", "cultural_academy"],
                "urgency": 0.6
            },
            "external_threat": {
                "description": "Dangers from outside the community",
                "triggers": ["natural_disasters", "hostile_groups"],
                "institutional_solutions": ["military", "government"],
                "urgency": 0.9
            },
            "social_disorder": {
                "description": "Breakdown of social cohesion",
                "triggers": ["high_conflict", "leadership_vacuum"],
                "institutional_solutions": ["government", "religion", "judiciary"],
                "urgency": 0.8
            },
            "economic_instability": {
                "description": "Trade and resource distribution problems",
                "triggers": ["trade_disruption", "resource_hoarding"],
                "institutional_solutions": ["commerce", "government"],
                "urgency": 0.7
            }
        }
    
    def _initialize_legitimacy_factors(self) -> Dict[str, float]:
        """Initialize factors that affect institutional legitimacy."""
        return {
            "founding_consensus": 0.3,      # How widely supported was formation
            "effectiveness": 0.25,          # How well it serves its purpose
            "fairness": 0.2,                # How equitably it treats people
            "tradition": 0.15,              # How well it respects customs
            "success_in_crisis": 0.1        # How well it handles emergencies
        }
    
    def process_daily_institutional_emergence(self, agents: List[Any], groups: Dict[str, Any], 
                                            world_state: Any, current_day: int) -> List[Dict[str, Any]]:
        """Process daily institutional emergence and evolution."""
        events = []
        
        # Step 1: Detect and track institutional crises
        crisis_events = self._detect_institutional_crises(agents, groups, world_state, current_day)
        events.extend(crisis_events)
        
        # Step 2: Check for institution formation opportunities
        formation_events = self._check_institution_formation(agents, groups, current_day)
        events.extend(formation_events)
        
        # Step 3: Process existing institution operations
        operation_events = self._process_institutional_operations(agents, current_day)
        events.extend(operation_events)
        
        # Step 4: Handle institutional evolution and reform
        evolution_events = self._process_institutional_evolution(agents, current_day)
        events.extend(evolution_events)
        
        # Step 5: Manage institutional crises and responses
        response_events = self._handle_institutional_crises(agents, current_day)
        events.extend(response_events)
        
        # Step 6: Update institutional legitimacy and effectiveness
        legitimacy_events = self._update_institutional_metrics(agents, current_day)
        events.extend(legitimacy_events)
        
        return events
    
    def _detect_institutional_crises(self, agents: List[Any], groups: Dict[str, Any], 
                                   world_state: Any, current_day: int) -> List[Dict[str, Any]]:
        """Detect crises that might drive institutional formation."""
        events = []
        
        # Analyze current community state
        community_analysis = self._analyze_community_state(agents, groups, world_state)
        
        # Check for different crisis types
        for crisis_type, crisis_config in self.crisis_types.items():
            crisis_indicators = self._check_crisis_indicators(crisis_type, community_analysis, agents)
            
            if crisis_indicators["severity"] > 0.6:  # Significant crisis
                # Create crisis object
                crisis = InstitutionalCrisis(
                    crisis_type=crisis_type,
                    severity=crisis_indicators["severity"],
                    affected_locations=crisis_indicators["locations"],
                    affected_population=crisis_indicators["population"],
                    resolution_requirements=crisis_config["institutional_solutions"],
                    time_pressure=int(30 * crisis_indicators["severity"]),  # Days to resolve
                    attempted_solutions=[],
                    institutional_responses={},
                    outcome=None
                )
                
                self.active_crises.append(crisis)
                
                events.append({
                    "type": "institutional_crisis_detected",
                    "crisis_type": crisis_type,
                    "severity": crisis_indicators["severity"],
                    "description": crisis_config["description"],
                    "affected_locations": list(crisis_indicators["locations"]),
                    "potential_solutions": crisis_config["institutional_solutions"],
                    "day": current_day
                })
        
        return events
    
    def _analyze_community_state(self, agents: List[Any], groups: Dict[str, Any], 
                                world_state: Any) -> Dict[str, Any]:
        """Analyze current state of the community for institutional needs."""
        analysis = {
            "total_population": len([a for a in agents if a.is_alive]),
            "population_by_location": defaultdict(int),
            "num_groups": len(groups),
            "group_types": defaultdict(int),
            "conflict_level": 0.0,
            "resource_scarcity": 0.0,
            "social_cohesion": 0.0,
            "leadership_vacuum": False,
            "specialist_availability": defaultdict(int),
            "cultural_complexity": 0.0
        }
        
        # Population analysis
        for agent in agents:
            if agent.is_alive:
                analysis["population_by_location"][agent.location] += 1
                
                # Count specialists
                if hasattr(agent, 'specialization') and agent.specialization:
                    analysis["specialist_availability"][agent.specialization] += 1
        
        # Group analysis
        for group_id, group_data in groups.items():
            if group_data.get("status") != "disbanded":
                group_type = group_data.get("type", "unknown")
                analysis["group_types"][group_type] += 1
        
        # Conflict level analysis
        recent_conflicts = 0
        for agent in agents:
            if hasattr(agent, 'memory') and agent.memory:
                # Check for recent conflict memories
                memories = agent.memory.get_memories_by_type("conflict", limit=10)
                recent_conflicts += len(memories)
        
        analysis["conflict_level"] = min(1.0, recent_conflicts / max(1, len(agents) * 2))
        
        # Resource scarcity analysis
        if hasattr(world_state, 'resources'):
            total_resources = len(world_state.resources)
            scarce_resources = len([r for r in world_state.resources.values() if r < 0.5])
            analysis["resource_scarcity"] = scarce_resources / max(1, total_resources)
        
        # Leadership analysis
        leaders = 0
        for agent in agents:
            if hasattr(agent, 'reputation') and agent.reputation > 0.7:
                leaders += 1
            if hasattr(agent, 'specialization') and agent.specialization == "leader":
                leaders += 2
        
        analysis["leadership_vacuum"] = leaders < max(1, len(agents) // 10)
        
        # Social cohesion analysis
        total_relationships = 0
        positive_relationships = 0
        
        for agent in agents:
            if hasattr(agent, 'relationships'):
                total_relationships += len(agent.relationships)
                positive_relationships += len([r for r in agent.relationships.values() 
                                             if r in ["friend", "family", "ally"]])
        
        if total_relationships > 0:
            analysis["social_cohesion"] = positive_relationships / total_relationships
        
        # Cultural complexity
        cultural_elements = 0
        if hasattr(world_state, 'cultural_elements'):
            cultural_elements = len(world_state.cultural_elements)
        
        analysis["cultural_complexity"] = min(1.0, cultural_elements / 20.0)
        
        return analysis
    
    def _check_crisis_indicators(self, crisis_type: str, community_analysis: Dict[str, Any], 
                                agents: List[Any]) -> Dict[str, Any]:
        """Check specific indicators for a crisis type."""
        indicators = {
            "severity": 0.0,
            "locations": set(),
            "population": set()
        }
        
        if crisis_type == "resource_conflict":
            # High resource scarcity + population pressure
            severity = community_analysis["resource_scarcity"]
            if community_analysis["total_population"] > 20:  # Overcrowding
                severity *= 1.5
            indicators["severity"] = min(1.0, severity)
            
            # All locations with significant population affected
            for location, pop in community_analysis["population_by_location"].items():
                if pop >= 3:
                    indicators["locations"].add(location)
                    
        elif crisis_type == "inter_group_dispute":
            # High conflict level + multiple groups
            severity = community_analysis["conflict_level"]
            if community_analysis["num_groups"] >= 3:
                severity *= 1.3
            indicators["severity"] = min(1.0, severity)
            
        elif crisis_type == "social_disorder":
            # Low social cohesion + leadership vacuum
            severity = 1.0 - community_analysis["social_cohesion"]
            if community_analysis["leadership_vacuum"]:
                severity *= 1.5
            indicators["severity"] = min(1.0, severity)
            
        elif crisis_type == "knowledge_loss":
            # Low cultural complexity + elder deaths
            severity = 1.0 - community_analysis["cultural_complexity"]
            elder_deaths = len([a for a in agents if not a.is_alive and a.age > 60])
            if elder_deaths > 0:
                severity *= 1.2
            indicators["severity"] = min(1.0, severity)
        
        # Add affected population
        for agent in agents:
            if agent.is_alive and agent.location in indicators["locations"]:
                indicators["population"].add(agent.name)
        
        return indicators
    
    def _check_institution_formation(self, agents: List[Any], groups: Dict[str, Any], 
                                   current_day: int) -> List[Dict[str, Any]]:
        """Check if conditions are right for new institution formation."""
        events = []
        
        community_analysis = self._analyze_community_state(agents, groups, None)
        
        for institution_type, requirements in self.formation_thresholds.items():
            if self._meets_formation_requirements(institution_type, requirements, 
                                                community_analysis, agents, groups):
                
                # Attempt to form institution
                formation_result = self._attempt_institution_formation(
                    institution_type, agents, groups, community_analysis, current_day
                )
                
                if formation_result:
                    events.append(formation_result)
        
        return events
    
    def _meets_formation_requirements(self, institution_type: str, requirements: Dict[str, Any],
                                    community_analysis: Dict[str, Any], agents: List[Any],
                                    groups: Dict[str, Any]) -> bool:
        """Check if requirements for institution formation are met."""
        
        # Population requirement
        if community_analysis["total_population"] < requirements.get("min_population", 0):
            return False
        
        # Group requirement
        if community_analysis["num_groups"] < requirements.get("min_groups", 0):
            return False
        
        # Community complexity requirement
        if community_analysis["cultural_complexity"] < requirements.get("min_community_complexity", 0):
            return False
        
        # Required skills/specialists
        if "required_specialists" in requirements:
            for specialist_type in requirements["required_specialists"]:
                if community_analysis["specialist_availability"][specialist_type] == 0:
                    return False
        
        # Required institutions (prerequisites)
        if "required_institutions" in requirements:
            existing_types = {inst.institution_type.value for inst in self.institutions.values()}
            for required_type in requirements["required_institutions"]:
                if required_type not in existing_types:
                    return False
        
        # Crisis-driven formation
        if "required_crises" in requirements:
            active_crisis_types = {crisis.crisis_type for crisis in self.active_crises}
            if not any(crisis_type in active_crisis_types 
                      for crisis_type in requirements["required_crises"]):
                return False
        
        return True
    
    def _attempt_institution_formation(self, institution_type: str, agents: List[Any],
                                     groups: Dict[str, Any], community_analysis: Dict[str, Any],
                                     current_day: int) -> Optional[Dict[str, Any]]:
        """Attempt to form a new social institution."""
        
        # Find suitable founding agents
        founders = self._identify_institutional_founders(institution_type, agents)
        if len(founders) < 2:
            return None
        
        # Determine governance type based on founders and community
        governance_type = self._determine_governance_type(founders, community_analysis)
        
        # Create the institution
        institution = self._create_institution(
            institution_type, governance_type, founders, current_day
        )
        
        # Add to system
        self.institutions[institution.id] = institution
        
        # Record founding event
        return {
            "type": "institution_formation",
            "institution_type": institution_type,
            "governance_type": governance_type.value,
            "institution_name": institution.name,
            "founders": [f.name for f in founders],
            "founding_location": institution.founding_location,
            "founding_crisis": institution.founding_crisis,
            "day": current_day
        }
    
    def _identify_institutional_founders(self, institution_type: str, agents: List[Any]) -> List[Any]:
        """Identify agents suitable for founding an institution."""
        suitable_founders = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            founder_score = 0.0
            
            # Leadership and reputation
            if hasattr(agent, 'reputation'):
                founder_score += agent.reputation * 0.3
            
            # Relevant skills
            if hasattr(agent, 'specialization'):
                if institution_type == "government" and agent.specialization == "leader":
                    founder_score += 0.4
                elif institution_type == "formal_school" and agent.specialization == "scholar":
                    founder_score += 0.4
                elif institution_type == "religion" and agent.specialization == "mystic":
                    founder_score += 0.4
                elif institution_type == "military" and agent.specialization == "guardian":
                    founder_score += 0.4
                elif institution_type == "commerce" and agent.specialization == "merchant":
                    founder_score += 0.4
            
            # Social connections
            if hasattr(agent, 'relationships'):
                social_score = len(agent.relationships) / 20.0  # Normalize
                founder_score += social_score * 0.2
            
            # Personality traits
            if hasattr(agent, 'traits'):
                if institution_type == "government" and "ambitious" in agent.traits:
                    founder_score += 0.1
                if institution_type == "formal_school" and "wise" in agent.traits:
                    founder_score += 0.1
                if institution_type == "religion" and "spiritual" in agent.traits:
                    founder_score += 0.1
            
            if founder_score >= 0.5:  # Minimum threshold
                suitable_founders.append(agent)
        
        # Sort by score and return top candidates
        suitable_founders.sort(key=lambda a: self._calculate_founder_score(a, institution_type), reverse=True)
        return suitable_founders[:5]  # Max 5 founders
    
    def _calculate_founder_score(self, agent: Any, institution_type: str) -> float:
        """Calculate how suitable an agent is for founding an institution."""
        score = 0.0
        
        if hasattr(agent, 'reputation'):
            score += agent.reputation * 0.3
        
        if hasattr(agent, 'specialization'):
            relevant_specializations = {
                "government": ["leader"],
                "formal_school": ["scholar", "mystic"],
                "military": ["guardian", "leader"],
                "religion": ["mystic"],
                "commerce": ["merchant"]
            }
            
            if agent.specialization in relevant_specializations.get(institution_type, []):
                score += 0.4
        
        if hasattr(agent, 'relationships'):
            score += min(0.3, len(agent.relationships) / 10.0)
        
        return score
    
    def _determine_governance_type(self, founders: List[Any], 
                                 community_analysis: Dict[str, Any]) -> GovernanceType:
        """Determine what type of governance structure should emerge."""
        
        # Analyze founder characteristics
        leader_count = len([f for f in founders if hasattr(f, 'specialization') and f.specialization == "leader"])
        mystic_count = len([f for f in founders if hasattr(f, 'specialization') and f.specialization == "mystic"])
        scholar_count = len([f for f in founders if hasattr(f, 'specialization') and f.specialization == "scholar"])
        
        # Community characteristics
        high_conflict = community_analysis["conflict_level"] > 0.6
        many_groups = community_analysis["num_groups"] >= 4
        low_cohesion = community_analysis["social_cohesion"] < 0.4
        
        # Decision logic
        if mystic_count >= leader_count and mystic_count > 0:
            return GovernanceType.THEOCRACY
        elif scholar_count >= leader_count and scholar_count > 0:
            return GovernanceType.MERITOCRACY
        elif high_conflict or low_cohesion:
            return GovernanceType.AUTOCRACY  # Strong leadership in crisis
        elif many_groups:
            return GovernanceType.CONFEDERATION  # Represent different groups
        elif len(founders) >= 3:
            return GovernanceType.COUNCIL_DEMOCRACY  # Multiple leaders
        else:
            return GovernanceType.COLLECTIVE  # Default collaborative approach
    
    def _create_institution(self, institution_type: str, governance_type: GovernanceType,
                           founders: List[Any], current_day: int) -> SocialInstitution:
        """Create a new social institution."""
        
        # Generate institution ID and name
        institution_id = f"{institution_type}_{current_day}_{len(self.institutions)}"
        primary_location = founders[0].location
        institution_name = self._generate_institution_name(institution_type, governance_type, primary_location)
        
        # Determine founding crisis
        founding_crisis = None
        if self.active_crises:
            # Find most relevant crisis
            relevant_crises = [c for c in self.active_crises 
                             if institution_type in self.crisis_types[c.crisis_type]["institutional_solutions"]]
            if relevant_crises:
                founding_crisis = relevant_crises[0].crisis_type
        
        # Create leadership structure
        governance_template = self.governance_templates[governance_type]
        leadership_structure = {}
        
        for i, role in enumerate(governance_template["leadership_roles"]):
            if i < len(founders):
                leadership_structure[role] = [founders[i].name]
            else:
                leadership_structure[role] = []
        
        # Initialize institution
        institution = SocialInstitution(
            id=institution_id,
            name=institution_name,
            institution_type=InstitutionType(institution_type),
            governance_type=governance_type,
            founding_day=current_day,
            founding_location=primary_location,
            
            leadership_structure=leadership_structure,
            core_members={f.name for f in founders},
            affiliated_members=set(),
            citizen_base=set(),
            
            departments={},
            procedures=[],
            laws_and_rules=[],
            
            controlled_resources={},
            budget={},
            territories={primary_location},
            jurisdiction={},
            
            status=InstitutionStatus.FORMING,
            legitimacy=0.6,  # Start with moderate legitimacy
            effectiveness=0.4,  # Start with low effectiveness
            corruption_level=0.0,
            
            founding_crisis=founding_crisis,
            major_decisions=[],
            reforms=[],
            conflicts=[],
            
            services_provided=[],
            success_metrics={},
            public_satisfaction=0.5
        )
        
        return institution
    
    def _generate_institution_name(self, institution_type: str, governance_type: GovernanceType,
                                  location: str) -> str:
        """Generate a name for the new institution."""
        location_name = location.replace("_", " ").title()
        
        name_templates = {
            "government": {
                GovernanceType.COUNCIL_DEMOCRACY: f"{location_name} Democratic Council",
                GovernanceType.MERITOCRACY: f"{location_name} Assembly of the Wise",
                GovernanceType.THEOCRACY: f"{location_name} Sacred Authority",
                GovernanceType.AUTOCRACY: f"{location_name} Central Command",
                GovernanceType.CONFEDERATION: f"{location_name} Alliance Government",
                GovernanceType.COLLECTIVE: f"{location_name} Collective Assembly"
            },
            "formal_school": {
                GovernanceType.MERITOCRACY: f"{location_name} Academy of Learning",
                GovernanceType.THEOCRACY: f"{location_name} Sacred School",
                GovernanceType.COUNCIL_DEMOCRACY: f"{location_name} Community Academy"
            },
            "religion": {
                GovernanceType.THEOCRACY: f"{location_name} Sacred Temple",
                GovernanceType.COLLECTIVE: f"{location_name} Spiritual Circle"
            },
            "military": {
                GovernanceType.AUTOCRACY: f"{location_name} Defense Force",
                GovernanceType.CONFEDERATION: f"{location_name} United Guard"
            },
            "commerce": {
                GovernanceType.MERITOCRACY: f"{location_name} Trade Institute",
                GovernanceType.COUNCIL_DEMOCRACY: f"{location_name} Merchants' Guild"
            }
        }
        
        # Get specific name or generate generic one
        if institution_type in name_templates and governance_type in name_templates[institution_type]:
            return name_templates[institution_type][governance_type]
        else:
            return f"{location_name} {institution_type.title().replace('_', ' ')}"
    
    def _process_institutional_operations(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process daily operations of existing institutions."""
        events = []
        
        for institution in self.institutions.values():
            if institution.status in [InstitutionStatus.FUNCTIONING, InstitutionStatus.EXPANDING]:
                operation_events = self._run_institutional_operations(institution, agents, current_day)
                events.extend(operation_events)
        
        return events
    
    def _run_institutional_operations(self, institution: SocialInstitution, agents: List[Any], 
                                    current_day: int) -> List[Dict[str, Any]]:
        """Run daily operations for a specific institution."""
        events = []
        
        # Provide institutional services
        if institution.institution_type == InstitutionType.GOVERNMENT:
            events.extend(self._provide_governance_services(institution, agents, current_day))
        elif institution.institution_type == InstitutionType.FORMAL_SCHOOL:
            events.extend(self._provide_education_services(institution, agents, current_day))
        elif institution.institution_type == InstitutionType.RELIGION:
            events.extend(self._provide_spiritual_services(institution, agents, current_day))
        elif institution.institution_type == InstitutionType.MILITARY:
            events.extend(self._provide_defense_services(institution, agents, current_day))
        elif institution.institution_type == InstitutionType.COMMERCE:
            events.extend(self._provide_trade_services(institution, agents, current_day))
        
        # Update effectiveness based on service provision
        self._update_institutional_effectiveness(institution, len(events))
        
        return events
    
    def _provide_governance_services(self, institution: SocialInstitution, agents: List[Any], 
                                   current_day: int) -> List[Dict[str, Any]]:
        """Provide governance services like conflict resolution and resource allocation."""
        events = []
        
        # Conflict mediation
        if random.random() < 0.3:  # 30% chance per day
            # Find agents in conflict
            conflicted_agents = []
            for agent in agents:
                if hasattr(agent, 'memory') and agent.is_alive:
                    recent_conflicts = agent.memory.get_memories_by_type("conflict", limit=3)
                    if len(recent_conflicts) > 0:
                        conflicted_agents.append(agent)
            
            if len(conflicted_agents) >= 2:
                # Government mediates conflict
                mediator = self._get_institutional_leader(institution, agents)
                if mediator:
                    events.append({
                        "type": "government_mediation",
                        "institution": institution.name,
                        "mediator": mediator.name,
                        "participants": [a.name for a in conflicted_agents[:3]],
                        "day": current_day
                    })
                    
                    # Add positive memories
                    for agent in conflicted_agents[:3]:
                        agent.memory.store_memory(
                            f"Government mediated conflict resolution with {mediator.name}",
                            importance=0.7,
                            memory_type="governance"
                        )
        
        # Resource allocation decisions
        if random.random() < 0.2:  # 20% chance per day
            events.append({
                "type": "resource_allocation",
                "institution": institution.name,
                "decision": "Community resource distribution managed",
                "day": current_day
            })
        
        return events
    
    def _provide_education_services(self, institution: SocialInstitution, agents: List[Any], 
                                  current_day: int) -> List[Dict[str, Any]]:
        """Provide formal education services."""
        events = []
        
        # Formal education sessions
        if random.random() < 0.4:  # 40% chance per day
            teachers = [a for a in agents if a.name in institution.core_members and a.is_alive]
            students = [a for a in agents if a.is_alive and a.age < 25]  # Young agents
            
            if teachers and students:
                teacher = random.choice(teachers)
                student_group = random.sample(students, min(random.randint(1, 4), len(students)))
                
                events.append({
                    "type": "formal_education",
                    "institution": institution.name,
                    "teacher": teacher.name,
                    "students": [s.name for s in student_group],
                    "subject": random.choice(["history", "skills", "wisdom", "culture"]),
                    "day": current_day
                })
                
                # Add learning memories
                for student in student_group:
                    student.memory.store_memory(
                        f"Attended formal education session with {teacher.name}",
                        importance=0.6,
                        memory_type="learning"
                    )
        
        return events
    
    def _provide_spiritual_services(self, institution: SocialInstitution, agents: List[Any], 
                                  current_day: int) -> List[Dict[str, Any]]:
        """Provide spiritual and religious services."""
        events = []
        
        # Religious ceremonies
        if random.random() < 0.25:  # 25% chance per day
            spiritual_leaders = [a for a in agents if a.name in institution.core_members and a.is_alive]
            community = [a for a in agents if a.is_alive]
            
            if spiritual_leaders and community:
                leader = random.choice(spiritual_leaders)
                participants = random.sample(community, min(random.randint(3, 8), len(community)))
                
                events.append({
                    "type": "religious_ceremony",
                    "institution": institution.name,
                    "spiritual_leader": leader.name,
                    "participants": [p.name for p in participants],
                    "ceremony_type": random.choice(["blessing", "meditation", "community_prayer", "seasonal_ritual"]),
                    "day": current_day
                })
                
                # Add spiritual memories
                for participant in participants:
                    participant.memory.store_memory(
                        f"Participated in religious ceremony led by {leader.name}",
                        importance=0.6,
                        memory_type="spiritual"
                    )
        
        return events
    
    def _provide_defense_services(self, institution: SocialInstitution, agents: List[Any], 
                                current_day: int) -> List[Dict[str, Any]]:
        """Provide military and defense services."""
        events = []
        
        # Defense drills and training
        if random.random() < 0.3:  # 30% chance per day
            military_leaders = [a for a in agents if a.name in institution.core_members and a.is_alive]
            
            if military_leaders:
                leader = random.choice(military_leaders)
                
                events.append({
                    "type": "defense_training",
                    "institution": institution.name,
                    "commander": leader.name,
                    "activity": random.choice(["combat_drill", "patrol", "fortification", "strategy_planning"]),
                    "day": current_day
                })
        
        return events
    
    def _provide_trade_services(self, institution: SocialInstitution, agents: List[Any], 
                              current_day: int) -> List[Dict[str, Any]]:
        """Provide trade and commercial services."""
        events = []
        
        # Trade facilitation
        if random.random() < 0.35:  # 35% chance per day
            merchants = [a for a in agents if a.name in institution.core_members and a.is_alive]
            
            if merchants:
                merchant = random.choice(merchants)
                
                events.append({
                    "type": "trade_facilitation",
                    "institution": institution.name,
                    "merchant": merchant.name,
                    "service": random.choice(["market_organization", "trade_mediation", "price_regulation", "quality_assurance"]),
                    "day": current_day
                })
        
        return events
    
    def _get_institutional_leader(self, institution: SocialInstitution, agents: List[Any]) -> Optional[Any]:
        """Get the primary leader of an institution."""
        for role, members in institution.leadership_structure.items():
            if members:
                # Find agent with this name
                leader = next((a for a in agents if a.name == members[0]), None)
                if leader and leader.is_alive:
                    return leader
        return None
    
    def _update_institutional_effectiveness(self, institution: SocialInstitution, services_provided: int):
        """Update institutional effectiveness based on service provision."""
        # Effectiveness increases with successful service provision
        effectiveness_change = min(0.05, services_provided * 0.02)
        institution.effectiveness = min(1.0, institution.effectiveness + effectiveness_change)
        
        # Effectiveness decays slowly if no services provided
        if services_provided == 0:
            institution.effectiveness = max(0.1, institution.effectiveness - 0.01)
    
    def _process_institutional_evolution(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process institutional evolution, reforms, and status changes."""
        events = []
        
        for institution in self.institutions.values():
            # Check for status transitions
            status_change = self._check_status_transition(institution, agents)
            if status_change:
                events.append({
                    "type": "institutional_status_change",
                    "institution": institution.name,
                    "old_status": institution.status.value,
                    "new_status": status_change.value,
                    "reason": self._get_status_change_reason(institution, status_change),
                    "day": current_day
                })
                institution.status = status_change
            
            # Check for reforms
            if random.random() < 0.05:  # 5% chance per day
                reform_event = self._attempt_institutional_reform(institution, agents, current_day)
                if reform_event:
                    events.append(reform_event)
        
        return events
    
    def _check_status_transition(self, institution: SocialInstitution, agents: List[Any]) -> Optional[InstitutionStatus]:
        """Check if an institution should change status."""
        current_status = institution.status
        
        # Factors affecting status
        active_leaders = len([name for role, members in institution.leadership_structure.items() 
                            for name in members if any(a.name == name and a.is_alive for a in agents)])
        
        member_count = len(institution.core_members) + len(institution.affiliated_members)
        
        # Transition logic
        if current_status == InstitutionStatus.FORMING:
            if institution.effectiveness > 0.5 and active_leaders >= 2:
                return InstitutionStatus.ESTABLISHING
        
        elif current_status == InstitutionStatus.ESTABLISHING:
            if institution.effectiveness > 0.7 and institution.legitimacy > 0.6:
                return InstitutionStatus.FUNCTIONING
        
        elif current_status == InstitutionStatus.FUNCTIONING:
            if institution.effectiveness > 0.8 and institution.legitimacy > 0.8:
                return InstitutionStatus.EXPANDING
            elif institution.effectiveness < 0.3 or active_leaders == 0:
                return InstitutionStatus.DECLINING
        
        elif current_status == InstitutionStatus.EXPANDING:
            if institution.effectiveness < 0.6:
                return InstitutionStatus.FUNCTIONING
        
        elif current_status == InstitutionStatus.DECLINING:
            if institution.effectiveness > 0.5 and active_leaders >= 1:
                return InstitutionStatus.FUNCTIONING
            elif institution.effectiveness < 0.1:
                return InstitutionStatus.TRANSFORMING
        
        return None
    
    def _get_status_change_reason(self, institution: SocialInstitution, new_status: InstitutionStatus) -> str:
        """Get a reason for institutional status change."""
        reasons = {
            InstitutionStatus.ESTABLISHING: "Gained organizational structure and leadership",
            InstitutionStatus.FUNCTIONING: "Achieved effective operations and community acceptance",
            InstitutionStatus.EXPANDING: "Demonstrating exceptional effectiveness and influence",
            InstitutionStatus.DECLINING: "Facing leadership challenges and reduced effectiveness",
            InstitutionStatus.TRANSFORMING: "Undergoing fundamental restructuring"
        }
        return reasons.get(new_status, "Natural institutional evolution")
    
    def _attempt_institutional_reform(self, institution: SocialInstitution, agents: List[Any], 
                                    current_day: int) -> Optional[Dict[str, Any]]:
        """Attempt to reform an institution."""
        # Only functioning or declining institutions undergo reforms
        if institution.status not in [InstitutionStatus.FUNCTIONING, InstitutionStatus.DECLINING]:
            return None
        
        # Find reform advocates
        leaders = [a for a in agents if a.name in institution.core_members and a.is_alive]
        if not leaders:
            return None
        
        reformer = random.choice(leaders)
        
        # Types of reforms
        reform_types = [
            "leadership_restructuring",
            "procedural_improvements", 
            "expanded_services",
            "transparency_measures",
            "efficiency_optimization"
        ]
        
        reform_type = random.choice(reform_types)
        
        # Apply reform effects
        if reform_type == "leadership_restructuring":
            institution.legitimacy = min(1.0, institution.legitimacy + 0.1)
        elif reform_type == "procedural_improvements":
            institution.effectiveness = min(1.0, institution.effectiveness + 0.1)
        elif reform_type == "transparency_measures":
            institution.corruption_level = max(0.0, institution.corruption_level - 0.1)
        
        # Record reform
        reform_record = {
            "type": reform_type,
            "reformer": reformer.name,
            "day": current_day,
            "description": f"{reform_type.replace('_', ' ').title()} implemented"
        }
        institution.reforms.append(reform_record)
        
        return {
            "type": "institutional_reform",
            "institution": institution.name,
            "reformer": reformer.name,
            "reform_type": reform_type,
            "day": current_day
        }
    
    def _handle_institutional_crises(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle responses to institutional crises."""
        events = []
        
        for crisis in self.active_crises[:]:  # Copy list to allow modification
            # Check if crisis has been resolved
            if self._is_crisis_resolved(crisis, agents):
                events.append({
                    "type": "crisis_resolved",
                    "crisis_type": crisis.crisis_type,
                    "resolution_method": "institutional_response",
                    "day": current_day
                })
                self.active_crises.remove(crisis)
                continue
            
            # Check if crisis has worsened
            crisis.time_pressure -= 1
            if crisis.time_pressure <= 0:
                # Crisis escalates
                crisis.severity = min(1.0, crisis.severity * 1.2)
                events.append({
                    "type": "crisis_escalation",
                    "crisis_type": crisis.crisis_type,
                    "new_severity": crisis.severity,
                    "day": current_day
                })
        
        return events
    
    def _is_crisis_resolved(self, crisis: InstitutionalCrisis, agents: List[Any]) -> bool:
        """Check if a crisis has been resolved."""
        # Check if appropriate institutions exist to handle the crisis
        crisis_config = self.crisis_types[crisis.crisis_type]
        institutional_solutions = crisis_config["institutional_solutions"]
        
        existing_institution_types = {inst.institution_type.value for inst in self.institutions.values() 
                                    if inst.status in [InstitutionStatus.FUNCTIONING, InstitutionStatus.EXPANDING]}
        
        # Crisis is resolved if at least one appropriate institution exists and is functioning
        return any(solution in existing_institution_types for solution in institutional_solutions)
    
    def _update_institutional_metrics(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Update legitimacy, effectiveness, and other institutional metrics."""
        events = []
        
        for institution in self.institutions.values():
            # Update legitimacy based on performance
            legitimacy_change = self._calculate_legitimacy_change(institution, agents)
            institution.legitimacy = max(0.0, min(1.0, institution.legitimacy + legitimacy_change))
            
            # Update corruption level
            corruption_change = self._calculate_corruption_change(institution, agents)
            institution.corruption_level = max(0.0, min(1.0, institution.corruption_level + corruption_change))
            
            # Update public satisfaction
            satisfaction_change = self._calculate_satisfaction_change(institution, agents)
            institution.public_satisfaction = max(0.0, min(1.0, institution.public_satisfaction + satisfaction_change))
            
            # Report significant changes
            if abs(legitimacy_change) > 0.1 or abs(satisfaction_change) > 0.1:
                events.append({
                    "type": "institutional_metrics_update",
                    "institution": institution.name,
                    "legitimacy_change": legitimacy_change,
                    "satisfaction_change": satisfaction_change,
                    "current_legitimacy": institution.legitimacy,
                    "current_satisfaction": institution.public_satisfaction,
                    "day": current_day
                })
        
        return events
    
    def _calculate_legitimacy_change(self, institution: SocialInstitution, agents: List[Any]) -> float:
        """Calculate change in institutional legitimacy."""
        change = 0.0
        
        # Effectiveness factor
        if institution.effectiveness > 0.7:
            change += 0.02
        elif institution.effectiveness < 0.3:
            change -= 0.02
        
        # Corruption factor
        if institution.corruption_level > 0.5:
            change -= 0.03
        
        # Leadership presence
        active_leaders = len([name for role, members in institution.leadership_structure.items() 
                            for name in members if any(a.name == name and a.is_alive for a in agents)])
        if active_leaders == 0:
            change -= 0.05
        
        return change
    
    def _calculate_corruption_change(self, institution: SocialInstitution, agents: List[Any]) -> float:
        """Calculate change in institutional corruption."""
        change = 0.0
        
        # Corruption naturally increases over time
        change += 0.001
        
        # Strong leadership reduces corruption
        if institution.effectiveness > 0.8:
            change -= 0.002
        
        # Reforms reduce corruption
        recent_reforms = len([r for r in institution.reforms if r.get("type") == "transparency_measures"])
        if recent_reforms > 0:
            change -= 0.01
        
        return change
    
    def _calculate_satisfaction_change(self, institution: SocialInstitution, agents: List[Any]) -> float:
        """Calculate change in public satisfaction."""
        change = 0.0
        
        # Effectiveness improves satisfaction
        if institution.effectiveness > 0.6:
            change += 0.01
        else:
            change -= 0.01
        
        # Legitimacy affects satisfaction
        if institution.legitimacy > 0.7:
            change += 0.005
        elif institution.legitimacy < 0.3:
            change -= 0.01
        
        return change
    
    def get_institutional_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of institutional development."""
        if not self.institutions:
            return {"status": "no_institutions"}
        
        summary = {
            "total_institutions": len(self.institutions),
            "institutions_by_type": {},
            "institutions_by_status": {},
            "governance_distribution": {},
            "average_legitimacy": 0.0,
            "average_effectiveness": 0.0,
            "active_crises": len(self.active_crises),
            "recent_formations": [],
            "institutional_complexity": 0.0
        }
        
        # Calculate distributions
        total_legitimacy = 0.0
        total_effectiveness = 0.0
        
        for institution in self.institutions.values():
            # Type distribution
            inst_type = institution.institution_type.value
            summary["institutions_by_type"][inst_type] = summary["institutions_by_type"].get(inst_type, 0) + 1
            
            # Status distribution
            status = institution.status.value
            summary["institutions_by_status"][status] = summary["institutions_by_status"].get(status, 0) + 1
            
            # Governance distribution
            if institution.governance_type:
                gov_type = institution.governance_type.value
                summary["governance_distribution"][gov_type] = summary["governance_distribution"].get(gov_type, 0) + 1
            
            # Averages
            total_legitimacy += institution.legitimacy
            total_effectiveness += institution.effectiveness
        
        # Calculate averages
        num_institutions = len(self.institutions)
        summary["average_legitimacy"] = total_legitimacy / num_institutions
        summary["average_effectiveness"] = total_effectiveness / num_institutions
        
        # Institutional complexity score
        complexity_factors = [
            len(summary["institutions_by_type"]) / 5.0,  # Variety of types
            len(summary["governance_distribution"]) / 5.0,  # Variety of governance
            summary["average_effectiveness"],  # How well they work
            summary["average_legitimacy"]  # How accepted they are
        ]
        summary["institutional_complexity"] = min(1.0, sum(complexity_factors) / len(complexity_factors))
        
        return summary
    
    def get_institution_details(self, institution_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific institution."""
        if institution_id not in self.institutions:
            return None
        
        institution = self.institutions[institution_id]
        return {
            "basic_info": {
                "name": institution.name,
                "type": institution.institution_type.value,
                "governance": institution.governance_type.value if institution.governance_type else None,
                "founded": institution.founding_day,
                "location": institution.founding_location,
                "status": institution.status.value
            },
            "membership": {
                "leaders": dict(institution.leadership_structure),
                "core_members": list(institution.core_members),
                "affiliated_members": list(institution.affiliated_members),
                "citizen_base": list(institution.citizen_base)
            },
            "performance": {
                "legitimacy": institution.legitimacy,
                "effectiveness": institution.effectiveness,
                "corruption_level": institution.corruption_level,
                "public_satisfaction": institution.public_satisfaction
            },
            "history": {
                "founding_crisis": institution.founding_crisis,
                "major_decisions": institution.major_decisions,
                "reforms": institution.reforms,
                "conflicts": institution.conflicts
            },
            "operations": {
                "services_provided": institution.services_provided,
                "success_metrics": institution.success_metrics,
                "territories": list(institution.territories),
                "controlled_resources": institution.controlled_resources
            }
        } 