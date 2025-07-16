"""
Civilizational Milestones System for SimuLife
Detects and celebrates major achievements that represent civilizational progress,
building on all existing systems to identify critical developmental thresholds.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import math


class MilestoneCategory(Enum):
    """Categories of civilizational milestones."""
    TECHNOLOGICAL = "technological"         # Tools, techniques, and innovations
    SOCIAL = "social"                      # Organization and governance
    CULTURAL = "cultural"                  # Arts, beliefs, and knowledge
    ECONOMIC = "economic"                  # Trade, currency, and resource management
    DEMOGRAPHIC = "demographic"            # Population and settlement patterns
    INTELLECTUAL = "intellectual"          # Knowledge systems and learning
    ORGANIZATIONAL = "organizational"      # Institutions and specialization
    ENVIRONMENTAL = "environmental"        # Human-nature relationships


class MilestoneSignificance(Enum):
    """Significance levels of milestones."""
    LOCAL = "local"                        # Village/community level achievement
    REGIONAL = "regional"                  # Multi-community achievement
    CIVILIZATIONAL = "civilizational"     # Major societal transformation
    EPOCHAL = "epochal"                    # Fundamental change in human organization


class MilestoneStatus(Enum):
    """Status of milestone achievement."""
    EMERGING = "emerging"                  # Prerequisites developing
    ACHIEVED = "achieved"                  # Milestone reached
    ESTABLISHED = "established"            # Milestone integrated into culture
    TRANSCENDED = "transcended"            # Milestone surpassed by new developments


@dataclass
class CivilizationalMilestone:
    """Represents a major civilizational achievement."""
    id: str
    name: str
    description: str
    category: MilestoneCategory
    significance: MilestoneSignificance
    
    # Achievement criteria
    prerequisites: List[str]               # Required prior milestones
    system_requirements: Dict[str, Any]    # Required system states
    threshold_conditions: Dict[str, float] # Numerical thresholds to meet
    
    # Achievement details
    achieved_day: Optional[int]
    achieving_agents: Set[str]             # Agents who contributed
    achieving_location: Optional[str]      # Where it was achieved
    achievement_context: Dict[str, Any]    # Circumstances of achievement
    
    # Impact and legacy
    status: MilestoneStatus
    cultural_impact: float                 # 0.0-1.0 impact on culture
    technological_impact: float           # 0.0-1.0 impact on technology
    social_impact: float                  # 0.0-1.0 impact on society
    
    # Follow-up effects
    unlocked_possibilities: List[str]      # What this enables
    subsequent_developments: List[str]     # What followed from this
    commemoration_events: List[Dict[str, Any]]  # How it's remembered
    
    # Decline and obsolescence
    obsolescence_factors: List[str]        # What might make it obsolete
    replacement_milestones: List[str]      # What might replace it


@dataclass
class MilestoneProgression:
    """Tracks progress toward a milestone."""
    milestone_id: str
    current_progress: float                # 0.0-1.0 progress toward achievement
    prerequisite_status: Dict[str, bool]   # Which prerequisites are met
    system_readiness: Dict[str, float]     # How ready each system is
    blocking_factors: List[str]            # What's preventing achievement
    accelerating_factors: List[str]        # What's helping achievement
    estimated_days_to_achievement: Optional[int]


class CivilizationalMilestonesSystem:
    """
    Detects and celebrates major civilizational achievements by analyzing
    the state of all systems and identifying when critical thresholds are reached.
    """
    
    def __init__(self):
        self.milestone_definitions: Dict[str, CivilizationalMilestone] = {}
        self.achieved_milestones: Dict[str, CivilizationalMilestone] = {}
        self.milestone_progression: Dict[str, MilestoneProgression] = {}
        
        # Tracking and analysis
        self.achievement_events: List[Dict[str, Any]] = []
        self.civilizational_timeline: List[Dict[str, Any]] = []
        self.cultural_memory: Dict[str, Any] = {}  # How milestones are remembered
        
        # System state tracking
        self.system_analysis_cache: Dict[int, Dict[str, Any]] = {}  # Day -> analysis
        self.progression_history: Dict[str, List[Tuple[int, float]]] = defaultdict(list)
        
        # Initialize milestone definitions
        self._initialize_milestone_definitions()
    
    def _initialize_milestone_definitions(self) -> None:
        """Initialize the catalog of possible civilizational milestones."""
        
        # Technological Milestones
        self.milestone_definitions["agriculture"] = CivilizationalMilestone(
            id="agriculture",
            name="Agricultural Revolution",
            description="Development of systematic food production and cultivation",
            category=MilestoneCategory.TECHNOLOGICAL,
            significance=MilestoneSignificance.CIVILIZATIONAL,
            
            prerequisites=[],
            system_requirements={
                "population_size": 10,
                "food_specialization": 0.3,
                "environmental_knowledge": 0.4,
                "tool_availability": 0.2
            },
            threshold_conditions={
                "food_production_agents": 3,
                "sustained_food_surplus": 0.2,
                "settlement_stability": 0.6
            },
            
            achieved_day=None,
            achieving_agents=set(),
            achieving_location=None,
            achievement_context={},
            
            status=MilestoneStatus.EMERGING,
            cultural_impact=0.8,
            technological_impact=0.9,
            social_impact=0.7,
            
            unlocked_possibilities=[
                "permanent_settlements", "population_growth", "labor_specialization",
                "food_storage", "seasonal_planning"
            ],
            subsequent_developments=[],
            commemoration_events=[],
            
            obsolescence_factors=["industrial_agriculture", "post_scarcity"],
            replacement_milestones=["industrial_revolution"]
        )
        
        self.milestone_definitions["writing"] = CivilizationalMilestone(
            id="writing",
            name="Written Language",
            description="Development of symbolic systems for recording information",
            category=MilestoneCategory.INTELLECTUAL,
            significance=MilestoneSignificance.CIVILIZATIONAL,
            
            prerequisites=["complex_language"],
            system_requirements={
                "population_size": 15,
                "knowledge_specialists": 2,
                "cultural_complexity": 0.5,
                "information_needs": 0.4
            },
            threshold_conditions={
                "symbol_use": 0.6,
                "information_storage": 0.3,
                "teaching_systems": 0.4
            },
            
            achieved_day=None,
            achieving_agents=set(),
            achieving_location=None,
            achievement_context={},
            
            status=MilestoneStatus.EMERGING,
            cultural_impact=0.9,
            technological_impact=0.6,
            social_impact=0.8,
            
            unlocked_possibilities=[
                "historical_records", "complex_laws", "long_distance_communication",
                "knowledge_accumulation", "abstract_thought"
            ],
            subsequent_developments=[],
            commemoration_events=[],
            
            obsolescence_factors=["digital_technology"],
            replacement_milestones=["printing", "digital_communication"]
        )
        
        self.milestone_definitions["formal_government"] = CivilizationalMilestone(
            id="formal_government",
            name="Formal Government",
            description="Establishment of organized, legitimate governmental authority",
            category=MilestoneCategory.SOCIAL,
            significance=MilestoneSignificance.CIVILIZATIONAL,
            
            prerequisites=["leadership_roles"],
            system_requirements={
                "population_size": 20,
                "social_complexity": 0.6,
                "institutional_development": 0.4,
                "conflict_resolution_needs": 0.5
            },
            threshold_conditions={
                "governance_institutions": 1,
                "legal_systems": 0.3,
                "public_legitimacy": 0.6
            },
            
            achieved_day=None,
            achieving_agents=set(),
            achieving_location=None,
            achievement_context={},
            
            status=MilestoneStatus.EMERGING,
            cultural_impact=0.7,
            technological_impact=0.3,
            social_impact=0.9,
            
            unlocked_possibilities=[
                "complex_laws", "taxation", "public_works", "military_organization",
                "inter_community_relations"
            ],
            subsequent_developments=[],
            commemoration_events=[],
            
            obsolescence_factors=["anarchism", "post_state_organization"],
            replacement_milestones=["democratic_government", "world_government"]
        )
        
        self.milestone_definitions["currency"] = CivilizationalMilestone(
            id="currency",
            name="Monetary System",
            description="Development of standardized medium of exchange",
            category=MilestoneCategory.ECONOMIC,
            significance=MilestoneSignificance.REGIONAL,
            
            prerequisites=["trade_networks"],
            system_requirements={
                "population_size": 15,
                "trade_volume": 30,
                "market_complexity": 0.4,
                "trust_systems": 0.5
            },
            threshold_conditions={
                "standardized_exchange": 0.6,
                "value_storage": 0.4,
                "economic_institutions": 1
            },
            
            achieved_day=None,
            achieving_agents=set(),
            achieving_location=None,
            achievement_context={},
            
            status=MilestoneStatus.EMERGING,
            cultural_impact=0.5,
            technological_impact=0.4,
            social_impact=0.6,
            
            unlocked_possibilities=[
                "complex_trade", "wealth_accumulation", "credit_systems",
                "economic_planning", "price_mechanisms"
            ],
            subsequent_developments=[],
            commemoration_events=[],
            
            obsolescence_factors=["digital_currency", "post_monetary_society"],
            replacement_milestones=["banking_system", "global_currency"]
        )
        
        self.milestone_definitions["urbanization"] = CivilizationalMilestone(
            id="urbanization",
            name="Urban Centers",
            description="Development of concentrated urban settlements",
            category=MilestoneCategory.DEMOGRAPHIC,
            significance=MilestoneSignificance.CIVILIZATIONAL,
            
            prerequisites=["agriculture", "trade_networks"],
            system_requirements={
                "population_size": 30,
                "resource_surplus": 0.5,
                "transportation": 0.3,
                "specialization": 0.6
            },
            threshold_conditions={
                "population_density": 0.7,
                "urban_services": 0.4,
                "non_food_production": 0.5
            },
            
            achieved_day=None,
            achieving_agents=set(),
            achieving_location=None,
            achievement_context={},
            
            status=MilestoneStatus.EMERGING,
            cultural_impact=0.8,
            technological_impact=0.6,
            social_impact=0.9,
            
            unlocked_possibilities=[
                "complex_architecture", "urban_planning", "public_services",
                "cultural_centers", "administrative_efficiency"
            ],
            subsequent_developments=[],
            commemoration_events=[],
            
            obsolescence_factors=["rural_renaissance", "virtual_communities"],
            replacement_milestones=["megalopolis", "smart_cities"]
        )
        
        self.milestone_definitions["organized_religion"] = CivilizationalMilestone(
            id="organized_religion",
            name="Organized Religion",
            description="Formal religious institutions with established doctrines",
            category=MilestoneCategory.CULTURAL,
            significance=MilestoneSignificance.REGIONAL,
            
            prerequisites=["spiritual_beliefs"],
            system_requirements={
                "population_size": 12,
                "cultural_movements": 1,
                "spiritual_specialists": 2,
                "ritual_systems": 0.4
            },
            threshold_conditions={
                "religious_institutions": 1,
                "doctrine_systematization": 0.5,
                "community_participation": 0.6
            },
            
            achieved_day=None,
            achieving_agents=set(),
            achieving_location=None,
            achievement_context={},
            
            status=MilestoneStatus.EMERGING,
            cultural_impact=0.9,
            technological_impact=0.2,
            social_impact=0.7,
            
            unlocked_possibilities=[
                "moral_codes", "community_identity", "social_cohesion",
                "artistic_expression", "philosophical_thought"
            ],
            subsequent_developments=[],
            commemoration_events=[],
            
            obsolescence_factors=["secularization", "spiritual_pluralism"],
            replacement_milestones=["world_religion", "secular_philosophy"]
        )
        
        self.milestone_definitions["formal_education"] = CivilizationalMilestone(
            id="formal_education",
            name="Educational System",
            description="Systematic institutions for knowledge transmission",
            category=MilestoneCategory.INTELLECTUAL,
            significance=MilestoneSignificance.REGIONAL,
            
            prerequisites=["knowledge_specialists"],
            system_requirements={
                "population_size": 18,
                "educational_institutions": 1,
                "knowledge_base": 0.6,
                "teaching_specialists": 2
            },
            threshold_conditions={
                "systematic_instruction": 0.6,
                "curriculum_development": 0.4,
                "student_populations": 0.3
            },
            
            achieved_day=None,
            achieving_agents=set(),
            achieving_location=None,
            achievement_context={},
            
            status=MilestoneStatus.EMERGING,
            cultural_impact=0.8,
            technological_impact=0.7,
            social_impact=0.6,
            
            unlocked_possibilities=[
                "knowledge_preservation", "skill_development", "social_mobility",
                "intellectual_advancement", "cultural_continuity"
            ],
            subsequent_developments=[],
            commemoration_events=[],
            
            obsolescence_factors=["self_directed_learning", "ai_tutors"],
            replacement_milestones=["universal_education", "virtual_learning"]
        )
        
        self.milestone_definitions["legal_system"] = CivilizationalMilestone(
            id="legal_system",
            name="Codified Laws",
            description="Formal legal codes and judicial procedures",
            category=MilestoneCategory.SOCIAL,
            significance=MilestoneSignificance.REGIONAL,
            
            prerequisites=["formal_government", "writing"],
            system_requirements={
                "population_size": 25,
                "governance_complexity": 0.7,
                "conflict_resolution": 0.6,
                "social_institutions": 2
            },
            threshold_conditions={
                "written_laws": 0.8,
                "judicial_procedures": 0.6,
                "legal_enforcement": 0.5
            },
            
            achieved_day=None,
            achieving_agents=set(),
            achieving_location=None,
            achievement_context={},
            
            status=MilestoneStatus.EMERGING,
            cultural_impact=0.6,
            technological_impact=0.3,
            social_impact=0.9,
            
            unlocked_possibilities=[
                "property_rights", "contract_enforcement", "civil_order",
                "justice_systems", "social_contracts"
            ],
            subsequent_developments=[],
            commemoration_events=[],
            
            obsolescence_factors=["algorithmic_justice", "restorative_justice"],
            replacement_milestones=["constitutional_law", "international_law"]
        )
        
        # Initialize progression tracking for all milestones
        for milestone_id in self.milestone_definitions:
            self.milestone_progression[milestone_id] = MilestoneProgression(
                milestone_id=milestone_id,
                current_progress=0.0,
                prerequisite_status={},
                system_readiness={},
                blocking_factors=[],
                accelerating_factors=[],
                estimated_days_to_achievement=None
            )
    
    def process_daily_milestone_analysis(self, agents: List[Any], groups: Dict[str, Any],
                                       institutions: Dict[str, Any], movements: Dict[str, Any],
                                       economic_state: Dict[str, Any], technology_state: Dict[str, Any],
                                       world_state: Any, current_day: int) -> List[Dict[str, Any]]:
        """Process daily analysis of civilizational milestone progress."""
        events = []
        
        # Step 1: Analyze current system states
        system_analysis = self._analyze_system_states(
            agents, groups, institutions, movements, economic_state, technology_state, world_state
        )
        self.system_analysis_cache[current_day] = system_analysis
        
        # Step 2: Update milestone progression
        progression_events = self._update_milestone_progression(system_analysis, current_day)
        events.extend(progression_events)
        
        # Step 3: Check for milestone achievements
        achievement_events = self._check_milestone_achievements(system_analysis, current_day)
        events.extend(achievement_events)
        
        # Step 4: Process milestone impacts and consequences
        impact_events = self._process_milestone_impacts(current_day)
        events.extend(impact_events)
        
        # Step 5: Update cultural memory and commemoration
        memory_events = self._update_cultural_memory(agents, current_day)
        events.extend(memory_events)
        
        # Step 6: Clean up old analysis cache
        self._cleanup_analysis_cache(current_day)
        
        return events
    
    def _analyze_system_states(self, agents: List[Any], groups: Dict[str, Any],
                             institutions: Dict[str, Any], movements: Dict[str, Any],
                             economic_state: Dict[str, Any], technology_state: Dict[str, Any],
                             world_state: Any) -> Dict[str, Any]:
        """Analyze current state of all systems for milestone evaluation."""
        analysis = {
            # Population and demographics
            "population_size": len([a for a in agents if a.is_alive]),
            "population_by_location": defaultdict(int),
            "age_distribution": {"young": 0, "adult": 0, "elder": 0},
            
            # Social organization
            "social_groups": len(groups),
            "institutions_count": len(institutions),
            "governance_institutions": 0,
            "cultural_institutions": 0,
            "economic_institutions": 0,
            
            # Cultural and intellectual
            "cultural_movements": len(movements),
            "knowledge_specialists": 0,
            "cultural_complexity": 0.0,
            "belief_systems": 0,
            
            # Economic
            "trade_volume": economic_state.get("recent_trade_volume", 0),
            "market_complexity": economic_state.get("economic_complexity", 0),
            "currency_systems": len(economic_state.get("currency_systems", set())),
            "economic_specialization": 0.0,
            
            # Technological
            "technology_level": technology_state.get("average_advancement", 0),
            "innovation_rate": technology_state.get("recent_innovations", 0),
            "tool_sophistication": 0.0,
            
            # Environmental and resource
            "resource_surplus": 0.0,
            "environmental_adaptation": 0.0,
            "settlement_stability": 0.0
        }
        
        # Detailed population analysis
        for agent in agents:
            if agent.is_alive:
                analysis["population_by_location"][agent.location] += 1
                
                if agent.age < 25:
                    analysis["age_distribution"]["young"] += 1
                elif agent.age < 60:
                    analysis["age_distribution"]["adult"] += 1
                else:
                    analysis["age_distribution"]["elder"] += 1
                
                # Count specialists
                if hasattr(agent, 'specialization'):
                    if agent.specialization in ["scholar", "mystic", "leader"]:
                        analysis["knowledge_specialists"] += 1
        
        # Institution analysis
        for institution_id, institution in institutions.items():
            if hasattr(institution, 'institution_type'):
                if "government" in institution.institution_type:
                    analysis["governance_institutions"] += 1
                elif "school" in institution.institution_type or "academy" in institution.institution_type:
                    analysis["cultural_institutions"] += 1
                elif "commerce" in institution.institution_type or "market" in institution.institution_type:
                    analysis["economic_institutions"] += 1
        
        # Cultural movement analysis
        belief_systems = set()
        for movement_id, movement in movements.items():
            if hasattr(movement, 'core_beliefs'):
                belief_systems.update(movement.core_beliefs)
        analysis["belief_systems"] = len(belief_systems)
        
        # Calculate complexity metrics
        if analysis["population_size"] > 0:
            analysis["cultural_complexity"] = min(1.0, (
                analysis["cultural_movements"] / 5.0 +
                analysis["belief_systems"] / 10.0 +
                analysis["cultural_institutions"] / 3.0
            ) / 3.0)
            
            analysis["economic_specialization"] = min(1.0, (
                analysis["economic_institutions"] / 2.0 +
                analysis["currency_systems"] / 3.0 +
                min(1.0, analysis["trade_volume"] / 100.0)
            ) / 3.0)
        
        # Settlement stability (how long-established communities are)
        location_counts = analysis["population_by_location"]
        if location_counts:
            max_population = max(location_counts.values())
            stable_locations = len([pop for pop in location_counts.values() if pop >= 5])
            analysis["settlement_stability"] = min(1.0, stable_locations / max(1, len(location_counts)))
        
        return analysis
    
    def _update_milestone_progression(self, system_analysis: Dict[str, Any], 
                                    current_day: int) -> List[Dict[str, Any]]:
        """Update progression toward all milestones."""
        events = []
        
        for milestone_id, milestone in self.milestone_definitions.items():
            if milestone_id in self.achieved_milestones:
                continue  # Already achieved
            
            progression = self.milestone_progression[milestone_id]
            
            # Calculate new progress
            new_progress = self._calculate_milestone_progress(milestone, system_analysis)
            old_progress = progression.current_progress
            
            progression.current_progress = new_progress
            self.progression_history[milestone_id].append((current_day, new_progress))
            
            # Update prerequisite status
            progression.prerequisite_status = self._check_prerequisites(milestone)
            
            # Update system readiness
            progression.system_readiness = self._calculate_system_readiness(milestone, system_analysis)
            
            # Identify blocking and accelerating factors
            progression.blocking_factors = self._identify_blocking_factors(milestone, system_analysis)
            progression.accelerating_factors = self._identify_accelerating_factors(milestone, system_analysis)
            
            # Estimate time to achievement
            progression.estimated_days_to_achievement = self._estimate_achievement_time(
                milestone, progression, current_day
            )
            
            # Report significant progress changes
            progress_change = new_progress - old_progress
            if abs(progress_change) > 0.1:  # 10% change
                events.append({
                    "type": "milestone_progress_change",
                    "milestone": milestone.name,
                    "milestone_id": milestone_id,
                    "old_progress": old_progress,
                    "new_progress": new_progress,
                    "change": progress_change,
                    "estimated_days": progression.estimated_days_to_achievement,
                    "day": current_day
                })
        
        return events
    
    def _calculate_milestone_progress(self, milestone: CivilizationalMilestone, 
                                    system_analysis: Dict[str, Any]) -> float:
        """Calculate progress toward a specific milestone."""
        progress_factors = []
        
        # Check system requirements
        for req_name, req_value in milestone.system_requirements.items():
            current_value = system_analysis.get(req_name, 0)
            if isinstance(req_value, (int, float)) and isinstance(current_value, (int, float)):
                if req_value > 0:
                    progress_factors.append(min(1.0, current_value / req_value))
                else:
                    progress_factors.append(1.0 if current_value > 0 else 0.0)
        
        # Check threshold conditions
        for condition_name, threshold in milestone.threshold_conditions.items():
            current_value = self._get_condition_value(condition_name, system_analysis)
            if threshold > 0:
                progress_factors.append(min(1.0, current_value / threshold))
            else:
                progress_factors.append(1.0 if current_value > 0 else 0.0)
        
        # Check prerequisites
        prerequisites_met = self._check_prerequisites(milestone)
        if milestone.prerequisites:
            prereq_progress = sum(prerequisites_met.values()) / len(prerequisites_met)
            progress_factors.append(prereq_progress)
        
        return sum(progress_factors) / len(progress_factors) if progress_factors else 0.0
    
    def _get_condition_value(self, condition_name: str, system_analysis: Dict[str, Any]) -> float:
        """Get the current value for a threshold condition."""
        # Map condition names to analysis values
        condition_mapping = {
            "food_production_agents": system_analysis.get("knowledge_specialists", 0) * 0.5,
            "sustained_food_surplus": system_analysis.get("resource_surplus", 0),
            "settlement_stability": system_analysis.get("settlement_stability", 0),
            "symbol_use": system_analysis.get("cultural_complexity", 0) * 0.8,
            "information_storage": system_analysis.get("cultural_institutions", 0) / 3.0,
            "teaching_systems": system_analysis.get("knowledge_specialists", 0) / 5.0,
            "governance_institutions": system_analysis.get("governance_institutions", 0),
            "legal_systems": system_analysis.get("governance_institutions", 0) * 0.5,
            "public_legitimacy": min(1.0, system_analysis.get("governance_institutions", 0) / 2.0),
            "standardized_exchange": system_analysis.get("currency_systems", 0) / 3.0,
            "value_storage": system_analysis.get("economic_specialization", 0),
            "economic_institutions": system_analysis.get("economic_institutions", 0),
            "population_density": self._calculate_population_density(system_analysis),
            "urban_services": system_analysis.get("cultural_institutions", 0) / 3.0,
            "non_food_production": system_analysis.get("economic_specialization", 0),
            "religious_institutions": len([m for m in system_analysis.get("movements", []) 
                                         if "religious" in str(m)]) / 2.0,
            "doctrine_systematization": system_analysis.get("belief_systems", 0) / 5.0,
            "community_participation": system_analysis.get("cultural_complexity", 0),
            "systematic_instruction": system_analysis.get("cultural_institutions", 0) / 2.0,
            "curriculum_development": system_analysis.get("knowledge_specialists", 0) / 3.0,
            "student_populations": system_analysis.get("age_distribution", {}).get("young", 0) / 10.0,
            "written_laws": system_analysis.get("governance_institutions", 0) * 0.8,
            "judicial_procedures": system_analysis.get("governance_institutions", 0) * 0.6,
            "legal_enforcement": system_analysis.get("governance_institutions", 0) * 0.5
        }
        
        return condition_mapping.get(condition_name, 0.0)
    
    def _calculate_population_density(self, system_analysis: Dict[str, Any]) -> float:
        """Calculate population density metric."""
        location_pops = system_analysis.get("population_by_location", {})
        if not location_pops:
            return 0.0
        
        max_pop = max(location_pops.values()) if location_pops else 0
        total_locations = len(location_pops)
        
        # High density if most people concentrated in few locations
        if total_locations > 0:
            concentration = max_pop / sum(location_pops.values())
            return min(1.0, concentration * 2.0)  # Scale to 0-1
        return 0.0
    
    def _check_prerequisites(self, milestone: CivilizationalMilestone) -> Dict[str, bool]:
        """Check which prerequisites are met for a milestone."""
        prereq_status = {}
        
        for prereq_id in milestone.prerequisites:
            # Check if prerequisite milestone is achieved
            prereq_status[prereq_id] = prereq_id in self.achieved_milestones
        
        return prereq_status
    
    def _calculate_system_readiness(self, milestone: CivilizationalMilestone, 
                                  system_analysis: Dict[str, Any]) -> Dict[str, float]:
        """Calculate how ready each system is for the milestone."""
        readiness = {}
        
        for system_name, requirement in milestone.system_requirements.items():
            current_value = system_analysis.get(system_name, 0)
            if isinstance(requirement, (int, float)) and requirement > 0:
                readiness[system_name] = min(1.0, current_value / requirement)
            else:
                readiness[system_name] = 1.0 if current_value > 0 else 0.0
        
        return readiness
    
    def _identify_blocking_factors(self, milestone: CivilizationalMilestone, 
                                 system_analysis: Dict[str, Any]) -> List[str]:
        """Identify factors blocking milestone achievement."""
        blocking_factors = []
        
        # Check unmet prerequisites
        prereq_status = self._check_prerequisites(milestone)
        for prereq_id, is_met in prereq_status.items():
            if not is_met:
                blocking_factors.append(f"prerequisite_{prereq_id}_not_met")
        
        # Check insufficient system requirements
        system_readiness = self._calculate_system_readiness(milestone, system_analysis)
        for system_name, readiness in system_readiness.items():
            if readiness < 0.5:  # Less than 50% ready
                blocking_factors.append(f"insufficient_{system_name}")
        
        # Specific blocking factors by milestone type
        if milestone.id == "agriculture":
            if system_analysis.get("population_size", 0) < 8:
                blocking_factors.append("population_too_small")
            if system_analysis.get("settlement_stability", 0) < 0.3:
                blocking_factors.append("nomadic_lifestyle")
        
        elif milestone.id == "writing":
            if system_analysis.get("knowledge_specialists", 0) < 1:
                blocking_factors.append("no_knowledge_specialists")
            if system_analysis.get("cultural_complexity", 0) < 0.3:
                blocking_factors.append("insufficient_cultural_development")
        
        elif milestone.id == "formal_government":
            if system_analysis.get("social_groups", 0) < 2:
                blocking_factors.append("insufficient_social_organization")
            if system_analysis.get("population_size", 0) < 15:
                blocking_factors.append("population_too_small_for_government")
        
        return blocking_factors
    
    def _identify_accelerating_factors(self, milestone: CivilizationalMilestone, 
                                     system_analysis: Dict[str, Any]) -> List[str]:
        """Identify factors accelerating milestone achievement."""
        accelerating_factors = []
        
        # Check strong system readiness
        system_readiness = self._calculate_system_readiness(milestone, system_analysis)
        for system_name, readiness in system_readiness.items():
            if readiness > 0.8:  # Very ready
                accelerating_factors.append(f"strong_{system_name}")
        
        # General accelerating factors
        if system_analysis.get("population_size", 0) > 30:
            accelerating_factors.append("large_population")
        
        if system_analysis.get("cultural_complexity", 0) > 0.7:
            accelerating_factors.append("advanced_culture")
        
        if system_analysis.get("economic_specialization", 0) > 0.6:
            accelerating_factors.append("economic_development")
        
        # Specific accelerating factors
        if milestone.id == "agriculture":
            if system_analysis.get("knowledge_specialists", 0) >= 3:
                accelerating_factors.append("knowledge_specialists_available")
        
        elif milestone.id == "urbanization":
            if system_analysis.get("trade_volume", 0) > 50:
                accelerating_factors.append("active_trade_networks")
        
        return accelerating_factors
    
    def _estimate_achievement_time(self, milestone: CivilizationalMilestone, 
                                 progression: MilestoneProgression, 
                                 current_day: int) -> Optional[int]:
        """Estimate days until milestone achievement."""
        current_progress = progression.current_progress
        
        if current_progress >= 1.0:
            return 0  # Ready for achievement
        
        if current_progress < 0.1:
            return None  # Too early to estimate
        
        # Look at recent progress rate
        recent_history = [p for d, p in self.progression_history[milestone.id] if current_day - d <= 30]
        
        if len(recent_history) < 2:
            return None
        
        # Calculate progress rate
        progress_rate = (recent_history[-1] - recent_history[0]) / len(recent_history)
        
        if progress_rate <= 0:
            return None  # No progress being made
        
        # Estimate time based on current rate
        remaining_progress = 1.0 - current_progress
        estimated_days = int(remaining_progress / progress_rate)
        
        # Apply modifiers based on blocking/accelerating factors
        if len(progression.blocking_factors) > len(progression.accelerating_factors):
            estimated_days = int(estimated_days * 1.5)  # Slower due to blocks
        elif len(progression.accelerating_factors) > len(progression.blocking_factors):
            estimated_days = int(estimated_days * 0.7)  # Faster due to acceleration
        
        return max(1, estimated_days)
    
    def _check_milestone_achievements(self, system_analysis: Dict[str, Any], 
                                    current_day: int) -> List[Dict[str, Any]]:
        """Check if any milestones should be achieved."""
        events = []
        
        for milestone_id, milestone in self.milestone_definitions.items():
            if milestone_id in self.achieved_milestones:
                continue
            
            progression = self.milestone_progression[milestone_id]
            
            # Check if milestone should be achieved
            if self._should_achieve_milestone(milestone, progression, system_analysis):
                achievement_event = self._achieve_milestone(milestone, system_analysis, current_day)
                events.append(achievement_event)
        
        return events
    
    def _should_achieve_milestone(self, milestone: CivilizationalMilestone, 
                                progression: MilestoneProgression, 
                                system_analysis: Dict[str, Any]) -> bool:
        """Determine if a milestone should be achieved."""
        # Must have high progress
        if progression.current_progress < 0.9:
            return False
        
        # All prerequisites must be met
        if not all(progression.prerequisite_status.values()):
            return False
        
        # No critical blocking factors
        critical_blocks = [f for f in progression.blocking_factors 
                          if "prerequisite" in f or "insufficient" in f]
        if critical_blocks:
            return False
        
        # System requirements must be mostly met
        avg_readiness = sum(progression.system_readiness.values()) / len(progression.system_readiness) if progression.system_readiness else 0
        if avg_readiness < 0.8:
            return False
        
        return True
    
    def _achieve_milestone(self, milestone: CivilizationalMilestone, 
                         system_analysis: Dict[str, Any], current_day: int) -> Dict[str, Any]:
        """Achieve a milestone and process its effects."""
        # Update milestone status
        milestone.achieved_day = current_day
        milestone.status = MilestoneStatus.ACHIEVED
        
        # Identify achieving agents and location
        achieving_agents = self._identify_achieving_agents(milestone, system_analysis)
        achieving_location = self._identify_achieving_location(milestone, system_analysis)
        
        milestone.achieving_agents = set(achieving_agents)
        milestone.achieving_location = achieving_location
        milestone.achievement_context = {
            "system_state": system_analysis.copy(),
            "circumstances": f"Achieved through {', '.join(milestone.unlocked_possibilities[:3])}"
        }
        
        # Move to achieved milestones
        self.achieved_milestones[milestone.id] = milestone
        
        # Record achievement
        achievement_event = {
            "type": "milestone_achievement",
            "milestone_id": milestone.id,
            "milestone_name": milestone.name,
            "category": milestone.category.value,
            "significance": milestone.significance.value,
            "achieving_agents": achieving_agents,
            "achieving_location": achieving_location,
            "cultural_impact": milestone.cultural_impact,
            "technological_impact": milestone.technological_impact,
            "social_impact": milestone.social_impact,
            "unlocked_possibilities": milestone.unlocked_possibilities,
            "day": current_day
        }
        
        self.achievement_events.append(achievement_event)
        self.civilizational_timeline.append(achievement_event)
        
        # Process immediate impacts
        self._process_immediate_milestone_impacts(milestone, current_day)
        
        return achievement_event
    
    def _identify_achieving_agents(self, milestone: CivilizationalMilestone, 
                                 system_analysis: Dict[str, Any]) -> List[str]:
        """Identify agents who contributed to milestone achievement."""
        # This would integrate with actual agent analysis
        # For now, return placeholder based on milestone type
        
        if milestone.category == MilestoneCategory.TECHNOLOGICAL:
            return ["innovator_agents"]
        elif milestone.category == MilestoneCategory.SOCIAL:
            return ["leader_agents"]
        elif milestone.category == MilestoneCategory.INTELLECTUAL:
            return ["scholar_agents"]
        else:
            return ["community_members"]
    
    def _identify_achieving_location(self, milestone: CivilizationalMilestone, 
                                   system_analysis: Dict[str, Any]) -> str:
        """Identify location where milestone was achieved."""
        # Find location with highest population or most relevant activity
        location_pops = system_analysis.get("population_by_location", {})
        
        if location_pops:
            return max(location_pops.keys(), key=lambda k: location_pops[k])
        else:
            return "unknown_location"
    
    def _process_immediate_milestone_impacts(self, milestone: CivilizationalMilestone, 
                                           current_day: int) -> None:
        """Process immediate impacts of milestone achievement."""
        # This would integrate with other systems to apply milestone effects
        # For example, agriculture might boost resource production
        # Writing might improve cultural transmission
        # Government might improve conflict resolution
        
        # For now, just record that impacts should be applied
        impact_record = {
            "milestone_id": milestone.id,
            "impacts_to_apply": milestone.unlocked_possibilities,
            "day": current_day
        }
        
        # Store for integration with other systems
        # Other systems would check this to see what new capabilities are available
    
    def _process_milestone_impacts(self, current_day: int) -> List[Dict[str, Any]]:
        """Process ongoing impacts and consequences of achieved milestones."""
        events = []
        
        for milestone_id, milestone in self.achieved_milestones.items():
            # Check for establishment (milestone becoming integrated)
            if (milestone.status == MilestoneStatus.ACHIEVED and 
                current_day - milestone.achieved_day > 30):  # 30 days to establish
                
                milestone.status = MilestoneStatus.ESTABLISHED
                events.append({
                    "type": "milestone_establishment",
                    "milestone": milestone.name,
                    "description": f"{milestone.name} has become integrated into civilization",
                    "day": current_day
                })
            
            # Check for subsequent developments
            if (milestone.status == MilestoneStatus.ESTABLISHED and 
                random.random() < 0.02):  # 2% chance per day
                
                subsequent_development = self._generate_subsequent_development(milestone, current_day)
                if subsequent_development:
                    milestone.subsequent_developments.append(subsequent_development)
                    events.append({
                        "type": "milestone_development",
                        "milestone": milestone.name,
                        "development": subsequent_development,
                        "day": current_day
                    })
        
        return events
    
    def _generate_subsequent_development(self, milestone: CivilizationalMilestone, 
                                       current_day: int) -> Optional[str]:
        """Generate a subsequent development from a milestone."""
        development_templates = {
            "agriculture": [
                "crop_rotation_techniques", "irrigation_systems", "agricultural_festivals",
                "farming_tools_improvement", "seed_selection_methods"
            ],
            "writing": [
                "historical_chronicles", "legal_documents", "literary_works",
                "administrative_records", "educational_texts"
            ],
            "formal_government": [
                "tax_collection_systems", "public_works_projects", "diplomatic_relations",
                "military_organization", "civil_service"
            ],
            "currency": [
                "banking_systems", "credit_mechanisms", "international_trade",
                "economic_regulations", "wealth_management"
            ]
        }
        
        developments = development_templates.get(milestone.id, [])
        if developments:
            return random.choice(developments)
        return None
    
    def _update_cultural_memory(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Update how milestones are remembered and commemorated."""
        events = []
        
        for milestone_id, milestone in self.achieved_milestones.items():
            # Check for commemoration events
            if (milestone.status == MilestoneStatus.ESTABLISHED and 
                len(milestone.commemoration_events) == 0 and
                random.random() < 0.1):  # 10% chance of commemoration
                
                commemoration = self._create_milestone_commemoration(milestone, agents, current_day)
                if commemoration:
                    milestone.commemoration_events.append(commemoration)
                    events.append({
                        "type": "milestone_commemoration",
                        "milestone": milestone.name,
                        "commemoration_type": commemoration["type"],
                        "description": commemoration["description"],
                        "day": current_day
                    })
        
        return events
    
    def _create_milestone_commemoration(self, milestone: CivilizationalMilestone, 
                                      agents: List[Any], current_day: int) -> Optional[Dict[str, Any]]:
        """Create a commemoration event for a milestone."""
        commemoration_types = {
            MilestoneCategory.TECHNOLOGICAL: "innovation_celebration",
            MilestoneCategory.SOCIAL: "founding_ceremony",
            MilestoneCategory.CULTURAL: "cultural_festival",
            MilestoneCategory.ECONOMIC: "prosperity_celebration",
            MilestoneCategory.INTELLECTUAL: "wisdom_gathering"
        }
        
        commemoration_type = commemoration_types.get(milestone.category, "general_celebration")
        
        return {
            "type": commemoration_type,
            "description": f"Community celebration of {milestone.name} achievement",
            "participants": [a.name for a in agents[:5] if a.is_alive],  # First 5 agents
            "location": milestone.achieving_location,
            "cultural_significance": milestone.cultural_impact,
            "day": current_day
        }
    
    def _cleanup_analysis_cache(self, current_day: int) -> None:
        """Clean up old analysis cache entries."""
        cutoff_day = current_day - 100  # Keep 100 days of history
        
        for day in list(self.system_analysis_cache.keys()):
            if day < cutoff_day:
                del self.system_analysis_cache[day]
        
        # Clean up progression history
        for milestone_id in self.progression_history:
            self.progression_history[milestone_id] = [
                (day, progress) for day, progress in self.progression_history[milestone_id]
                if day >= cutoff_day
            ]
    
    def get_civilizational_status(self) -> Dict[str, Any]:
        """Get comprehensive civilizational development status."""
        status = {
            "total_milestones": len(self.milestone_definitions),
            "achieved_milestones": len(self.achieved_milestones),
            "achievement_rate": len(self.achieved_milestones) / len(self.milestone_definitions),
            "milestones_by_category": {},
            "milestones_by_significance": {},
            "recent_achievements": [],
            "nearest_milestones": [],
            "civilizational_age": self._determine_civilizational_age(),
            "development_trajectory": self._analyze_development_trajectory()
        }
        
        # Categorize achieved milestones
        for milestone in self.achieved_milestones.values():
            category = milestone.category.value
            significance = milestone.significance.value
            
            if category not in status["milestones_by_category"]:
                status["milestones_by_category"][category] = {"achieved": 0, "total": 0}
            if significance not in status["milestones_by_significance"]:
                status["milestones_by_significance"][significance] = {"achieved": 0, "total": 0}
            
            status["milestones_by_category"][category]["achieved"] += 1
            status["milestones_by_significance"][significance]["achieved"] += 1
        
        # Count totals
        for milestone in self.milestone_definitions.values():
            category = milestone.category.value
            significance = milestone.significance.value
            
            if category not in status["milestones_by_category"]:
                status["milestones_by_category"][category] = {"achieved": 0, "total": 0}
            if significance not in status["milestones_by_significance"]:
                status["milestones_by_significance"][significance] = {"achieved": 0, "total": 0}
            
            status["milestones_by_category"][category]["total"] += 1
            status["milestones_by_significance"][significance]["total"] += 1
        
        # Recent achievements (last 100 days)
        current_day = max([m.achieved_day for m in self.achieved_milestones.values()], default=0)
        status["recent_achievements"] = [
            {
                "name": m.name,
                "day": m.achieved_day,
                "significance": m.significance.value
            }
            for m in self.achieved_milestones.values()
            if m.achieved_day and current_day - m.achieved_day <= 100
        ]
        
        # Nearest milestones (highest progress)
        nearest = sorted([
            {
                "name": self.milestone_definitions[mid].name,
                "progress": prog.current_progress,
                "estimated_days": prog.estimated_days_to_achievement
            }
            for mid, prog in self.milestone_progression.items()
            if mid not in self.achieved_milestones
        ], key=lambda x: x["progress"], reverse=True)[:5]
        
        status["nearest_milestones"] = nearest
        
        return status
    
    def _determine_civilizational_age(self) -> str:
        """Determine the current civilizational age based on achievements."""
        achieved_categories = set(m.category for m in self.achieved_milestones.values())
        
        if MilestoneCategory.TECHNOLOGICAL in achieved_categories and "agriculture" in self.achieved_milestones:
            if "writing" in self.achieved_milestones and "formal_government" in self.achieved_milestones:
                return "Classical Age"
            else:
                return "Agricultural Age"
        elif len(self.achieved_milestones) > 0:
            return "Tribal Age"
        else:
            return "Prehistoric Age"
    
    def _analyze_development_trajectory(self) -> Dict[str, Any]:
        """Analyze the trajectory of civilizational development."""
        if len(self.achievement_events) < 2:
            return {"trajectory": "insufficient_data"}
        
        # Calculate achievement rate over time
        events_by_day = sorted(self.achievement_events, key=lambda x: x["day"])
        first_day = events_by_day[0]["day"]
        last_day = events_by_day[-1]["day"]
        
        if last_day - first_day <= 0:
            return {"trajectory": "single_achievement"}
        
        achievement_rate = len(events_by_day) / (last_day - first_day)
        
        # Analyze recent vs early achievement rates
        midpoint = first_day + (last_day - first_day) // 2
        early_achievements = len([e for e in events_by_day if e["day"] <= midpoint])
        late_achievements = len([e for e in events_by_day if e["day"] > midpoint])
        
        trajectory = "steady"
        if late_achievements > early_achievements * 1.5:
            trajectory = "accelerating"
        elif late_achievements < early_achievements * 0.7:
            trajectory = "slowing"
        
        return {
            "trajectory": trajectory,
            "achievement_rate": achievement_rate,
            "total_span": last_day - first_day,
            "recent_acceleration": late_achievements > early_achievements
        } 