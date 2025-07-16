"""
Technology and Innovation System for SimuLife
Manages research, development, knowledge advancement, and technological progress.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum


class TechnologyCategory(Enum):
    """Categories of technologies that can be researched."""
    SURVIVAL = "survival"           # Basic survival technologies
    CRAFTING = "crafting"          # Tool and item creation
    AGRICULTURE = "agriculture"     # Food production and farming
    MEDICINE = "medicine"          # Health and healing
    SOCIAL = "social"              # Social organization and communication
    SPIRITUAL = "spiritual"        # Religious and philosophical advancement
    MILITARY = "military"          # Warfare and defense
    TRADE = "trade"                # Economic and commercial systems
    CONSTRUCTION = "construction"   # Building and infrastructure
    KNOWLEDGE = "knowledge"        # Information storage and learning


class ResearchStatus(Enum):
    """Status of research projects."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"
    BLOCKED = "blocked"            # Missing prerequisites


class InnovationType(Enum):
    """Types of innovations that can occur."""
    DISCOVERY = "discovery"         # Accidental or observational discovery
    INVENTION = "invention"         # Deliberate creation
    IMPROVEMENT = "improvement"     # Enhancement of existing technology
    COMBINATION = "combination"     # Merging multiple technologies
    ADAPTATION = "adaptation"       # Modifying existing tech for new use


class TechnologyGoalPriority(Enum):
    """Priority levels for technology goals."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CompetitionType(Enum):
    """Types of technology competition."""
    RESEARCH_RACE = "research_race"     # Race to discover same technology
    INNOVATION_WAR = "innovation_war"   # Competitive innovation development
    KNOWLEDGE_THEFT = "knowledge_theft" # Attempting to steal technology
    EMBARGO = "embargo"                 # Blocking technology transfer


class ResearchFailureType(Enum):
    """Types of research failures."""
    RESOURCE_DEPLETION = "resource_depletion"   # Ran out of resources
    SKILL_INADEQUACY = "skill_inadequacy"       # Insufficient skills
    COLLABORATION_BREAKDOWN = "collaboration_breakdown"  # Team conflicts
    ACCIDENTAL_DESTRUCTION = "accidental_destruction"   # Destroyed research
    EXTERNAL_INTERFERENCE = "external_interference"     # Sabotage or theft


@dataclass
class Technology:
    """Represents a technology that can be researched and developed."""
    id: str
    name: str
    category: TechnologyCategory
    description: str
    prerequisites: List[str]        # Required technologies
    required_skills: Dict[str, float]  # Skills needed with minimum levels
    research_complexity: float      # 0.1 (simple) to 1.0 (very complex)
    discovery_chance: float         # Base chance for accidental discovery
    benefits: Dict[str, Any]        # Effects when technology is acquired
    unlock_actions: List[str]       # New actions this technology enables
    is_discovered: bool = False
    discovery_day: Optional[int] = None
    discovered_by: Optional[str] = None  # Agent or group who discovered it


@dataclass
class ResearchProject:
    """Represents an active research project."""
    id: str
    technology_id: str
    lead_researcher: str            # Primary agent leading the project
    collaborators: List[str]        # Additional agents working on it
    group_id: Optional[str]         # Group sponsoring the research
    status: ResearchStatus
    progress: float                 # 0.0 to 1.0
    required_progress: float        # Total progress needed
    start_day: int
    estimated_completion: Optional[int]
    daily_progress_rate: float
    last_progress_day: int
    resources_invested: Dict[str, float]
    breakthrough_chances: List[float]  # Chances for breakthrough at different stages


@dataclass
class Innovation:
    """Represents a technological innovation or discovery."""
    id: str
    name: str
    innovation_type: InnovationType
    technology_affected: str
    innovator: str                  # Agent who made the innovation
    day_discovered: int
    description: str
    impact_level: float             # 0.1 (minor) to 1.0 (revolutionary)
    adoption_rate: float            # How quickly others adopt it
    knowledge_requirements: Dict[str, float]


@dataclass
class TechnologyGoal:
    """Represents a technology research goal for an agent or group."""
    id: str
    target_technology: str
    goal_setter: str                # Agent or group who set the goal
    priority: TechnologyGoalPriority
    set_day: int
    target_completion_day: Optional[int]
    resources_allocated: Dict[str, float]
    motivation: str                 # Why this goal was set
    completion_reward: Dict[str, Any]
    is_completed: bool = False
    completion_day: Optional[int] = None


@dataclass
class TechnologyCompetition:
    """Represents competitive technology development between groups."""
    id: str
    competition_type: CompetitionType
    target_technology: str
    participants: List[str]         # Groups or agents competing
    start_day: int
    current_leader: Optional[str]
    leader_progress: float
    stakes: Dict[str, Any]          # What's at stake
    sabotage_attempts: List[str]    # Record of interference attempts
    is_active: bool = True
    winner: Optional[str] = None
    end_day: Optional[int] = None


@dataclass
class ResearchFailure:
    """Represents a failed research attempt."""
    id: str
    project_id: str
    failure_type: ResearchFailureType
    failure_day: int
    lead_researcher: str
    resources_lost: Dict[str, float]
    skill_penalties: Dict[str, float]
    description: str
    consequences: List[str]         # Long-term effects
    lessons_learned: Dict[str, float]  # Skill bonuses from failure


@dataclass
class TechnologyConflict:
    """Represents conflicts arising from technology disparities."""
    id: str
    conflict_type: str
    advantaged_side: str            # Group with tech advantage
    disadvantaged_side: str         # Group without tech advantage
    technology_gap: List[str]       # Technologies creating the advantage
    conflict_intensity: float       # 0.1 to 1.0
    start_day: int
    resolution_attempts: List[str]
    is_resolved: bool = False
    resolution_day: Optional[int] = None
    outcome: Optional[str] = None


class TechnologySystem:
    """
    Manages technological research, development, and innovation in SimuLife.
    """
    
    def __init__(self):
        self.technologies: Dict[str, Technology] = {}
        self.research_projects: Dict[str, ResearchProject] = {}
        self.innovations: Dict[str, Innovation] = {}
        self.agent_knowledge: Dict[str, Dict[str, float]] = {}  # agent -> tech -> knowledge_level
        self.group_technologies: Dict[str, Set[str]] = {}  # group -> set of known technologies
        self.technology_tree = {}
        
        # Phase 6 Enhancements
        self.technology_goals: Dict[str, TechnologyGoal] = {}
        self.technology_competitions: Dict[str, TechnologyCompetition] = {}
        self.research_failures: Dict[str, ResearchFailure] = {}
        self.technology_conflicts: Dict[str, TechnologyConflict] = {}
        self.technology_advantages: Dict[str, Dict[str, float]] = {}  # tech -> advantage_type -> bonus
        
        # Initialize the technology tree
        self._initialize_technology_tree()
        
        # Track system events
        self.technology_events: List[Dict[str, Any]] = []
    
    def _initialize_technology_tree(self):
        """Initialize the comprehensive technology tree."""
        
        # Survival Technologies
        self.technologies.update({
            "fire_making": Technology(
                id="fire_making",
                name="Fire Making",
                category=TechnologyCategory.SURVIVAL,
                description="The ability to create and control fire",
                prerequisites=[],
                required_skills={"survival": 0.3},
                research_complexity=0.2,
                discovery_chance=0.3,
                benefits={"warmth": 1.0, "cooking": 1.0, "light": 1.0},
                unlock_actions=["make_fire", "cook_food"]
            ),
            "shelter_construction": Technology(
                id="shelter_construction",
                name="Shelter Construction",
                category=TechnologyCategory.SURVIVAL,
                description="Building basic protective structures",
                prerequisites=[],
                required_skills={"crafting": 0.4, "survival": 0.3},
                research_complexity=0.3,
                discovery_chance=0.2,
                benefits={"protection": 1.0, "comfort": 0.5},
                unlock_actions=["build_shelter", "repair_shelter"]
            ),
            "water_purification": Technology(
                id="water_purification",
                name="Water Purification",
                category=TechnologyCategory.SURVIVAL,
                description="Methods to clean and purify water",
                prerequisites=["fire_making"],
                required_skills={"survival": 0.5, "medicine": 0.3},
                research_complexity=0.4,
                discovery_chance=0.15,
                benefits={"health": 1.0, "disease_resistance": 0.7},
                unlock_actions=["purify_water", "boil_water"]
            )
        })
        
        # Crafting Technologies
        self.technologies.update({
            "stone_tools": Technology(
                id="stone_tools",
                name="Stone Tools",
                category=TechnologyCategory.CRAFTING,
                description="Creating tools from stone and rock",
                prerequisites=[],
                required_skills={"crafting": 0.4},
                research_complexity=0.3,
                discovery_chance=0.25,
                benefits={"tool_efficiency": 1.5, "hunting": 1.2},
                unlock_actions=["craft_stone_tools", "sharpen_tools"]
            ),
            "rope_making": Technology(
                id="rope_making",
                name="Rope Making",
                category=TechnologyCategory.CRAFTING,
                description="Creating rope from natural fibers",
                prerequisites=[],
                required_skills={"crafting": 0.5, "foraging": 0.3},
                research_complexity=0.4,
                discovery_chance=0.2,
                benefits={"construction": 1.0, "hunting": 1.1},
                unlock_actions=["make_rope", "weave_fibers"]
            ),
            "pottery": Technology(
                id="pottery",
                name="Pottery",
                category=TechnologyCategory.CRAFTING,
                description="Creating containers from clay",
                prerequisites=["fire_making"],
                required_skills={"crafting": 0.6, "artistry": 0.4},
                research_complexity=0.5,
                discovery_chance=0.1,
                benefits={"storage": 1.5, "cooking": 1.3},
                unlock_actions=["make_pottery", "fire_clay"]
            ),
            "metalworking": Technology(
                id="metalworking",
                name="Metalworking",
                category=TechnologyCategory.CRAFTING,
                description="Shaping and working with metals",
                prerequisites=["fire_making", "stone_tools"],
                required_skills={"crafting": 0.8, "foraging": 0.5},
                research_complexity=0.8,
                discovery_chance=0.05,
                benefits={"tool_efficiency": 2.0, "construction": 1.5},
                unlock_actions=["forge_metal", "craft_metal_tools"]
            )
        })
        
        # Agriculture Technologies
        self.technologies.update({
            "plant_cultivation": Technology(
                id="plant_cultivation",
                name="Plant Cultivation",
                category=TechnologyCategory.AGRICULTURE,
                description="Deliberately growing plants for food",
                prerequisites=[],
                required_skills={"foraging": 0.6, "survival": 0.4},
                research_complexity=0.5,
                discovery_chance=0.15,
                benefits={"food_security": 2.0, "nutrition": 1.3},
                unlock_actions=["plant_seeds", "tend_crops"]
            ),
            "animal_domestication": Technology(
                id="animal_domestication",
                name="Animal Domestication",
                category=TechnologyCategory.AGRICULTURE,
                description="Taming and raising animals",
                prerequisites=["plant_cultivation"],
                required_skills={"survival": 0.7, "social": 0.4},
                research_complexity=0.7,
                discovery_chance=0.1,
                benefits={"food_security": 1.5, "materials": 1.8},
                unlock_actions=["tame_animals", "raise_livestock"]
            ),
            "irrigation": Technology(
                id="irrigation",
                name="Irrigation",
                category=TechnologyCategory.AGRICULTURE,
                description="Directing water to crops",
                prerequisites=["plant_cultivation", "construction_basic"],
                required_skills={"engineering": 0.6, "organization": 0.5},
                research_complexity=0.8,
                discovery_chance=0.05,
                benefits={"crop_yield": 2.5, "consistency": 2.0},
                unlock_actions=["build_irrigation", "manage_water_flow"]
            )
        })
        
        # Medicine Technologies
        self.technologies.update({
            "herbal_medicine": Technology(
                id="herbal_medicine",
                name="Herbal Medicine",
                category=TechnologyCategory.MEDICINE,
                description="Using plants for healing",
                prerequisites=[],
                required_skills={"medicine": 0.5, "foraging": 0.6},
                research_complexity=0.4,
                discovery_chance=0.2,
                benefits={"healing": 1.5, "disease_resistance": 1.2},
                unlock_actions=["gather_medicinal_plants", "prepare_medicine"]
            ),
            "surgical_techniques": Technology(
                id="surgical_techniques",
                name="Surgical Techniques",
                category=TechnologyCategory.MEDICINE,
                description="Basic surgical procedures",
                prerequisites=["herbal_medicine", "stone_tools"],
                required_skills={"medicine": 0.8, "precision": 0.7},
                research_complexity=0.9,
                discovery_chance=0.03,
                benefits={"trauma_treatment": 2.0, "survival_rate": 1.8},
                unlock_actions=["perform_surgery", "treat_wounds"]
            )
        })
        
        # Social Technologies
        self.technologies.update({
            "written_language": Technology(
                id="written_language",
                name="Written Language",
                category=TechnologyCategory.SOCIAL,
                description="Recording information through symbols",
                prerequisites=[],
                required_skills={"intellectual": 0.7, "artistry": 0.4},
                research_complexity=0.8,
                discovery_chance=0.05,
                benefits={"knowledge_preservation": 3.0, "communication": 2.0},
                unlock_actions=["write_records", "teach_writing"]
            ),
            "currency_system": Technology(
                id="currency_system",
                name="Currency System",
                category=TechnologyCategory.SOCIAL,
                description="Standardized medium of exchange",
                prerequisites=["written_language"],
                required_skills={"negotiation": 0.6, "organization": 0.7},
                research_complexity=0.7,
                discovery_chance=0.08,
                benefits={"trade_efficiency": 2.5, "wealth_accumulation": 2.0},
                unlock_actions=["mint_currency", "establish_prices"]
            ),
            "legal_system": Technology(
                id="legal_system",
                name="Legal System",
                category=TechnologyCategory.SOCIAL,
                description="Formal rules and justice procedures",
                prerequisites=["written_language"],
                required_skills={"leadership": 0.7, "wisdom": 0.6},
                research_complexity=0.9,
                discovery_chance=0.03,
                benefits={"social_order": 2.0, "conflict_resolution": 2.5},
                unlock_actions=["establish_laws", "hold_trials"]
            )
        })
        
        # Construction Technologies  
        self.technologies.update({
            "construction_basic": Technology(
                id="construction_basic",
                name="Basic Construction",
                category=TechnologyCategory.CONSTRUCTION,
                description="Fundamental building techniques",
                prerequisites=["stone_tools", "rope_making"],
                required_skills={"crafting": 0.6, "engineering": 0.4},
                research_complexity=0.5,
                discovery_chance=0.1,
                benefits={"building_quality": 1.5, "durability": 1.3},
                unlock_actions=["construct_buildings", "plan_structures"]
            ),
            "advanced_architecture": Technology(
                id="advanced_architecture",
                name="Advanced Architecture",
                category=TechnologyCategory.CONSTRUCTION,
                description="Complex structural design and engineering",
                prerequisites=["construction_basic", "written_language"],
                required_skills={"engineering": 0.8, "artistry": 0.6},
                research_complexity=0.9,
                discovery_chance=0.02,
                benefits={"building_complexity": 3.0, "city_planning": 2.5},
                unlock_actions=["design_monuments", "plan_cities"]
            )
        })
        
        # Advanced Technologies (Phase 6 Enhancement)
        self.technologies.update({
            # Advanced Knowledge Technologies
            "astronomy": Technology(
                id="astronomy",
                name="Astronomy", 
                category=TechnologyCategory.KNOWLEDGE,
                description="Study of celestial bodies and their movements",
                prerequisites=["written_language", "advanced_mathematics"],
                required_skills={"intellectual": 0.9, "observation": 0.8},
                research_complexity=0.95,
                discovery_chance=0.01,
                benefits={"navigation": 2.5, "calendar_precision": 3.0, "wisdom": 1.5},
                unlock_actions=["observe_stars", "predict_eclipses", "create_calendar"]
            ),
            "advanced_mathematics": Technology(
                id="advanced_mathematics",
                name="Advanced Mathematics",
                category=TechnologyCategory.KNOWLEDGE,
                description="Complex mathematical concepts and calculations",
                prerequisites=["written_language"],
                required_skills={"intellectual": 0.85, "logic": 0.8},
                research_complexity=0.9,
                discovery_chance=0.02,
                benefits={"engineering_precision": 2.0, "trade_calculations": 2.5},
                unlock_actions=["perform_calculations", "solve_complex_problems"]
            ),
            "philosophy": Technology(
                id="philosophy",
                name="Philosophy",
                category=TechnologyCategory.KNOWLEDGE,
                description="Deep thinking about existence, ethics, and knowledge",
                prerequisites=["written_language"],
                required_skills={"wisdom": 0.8, "intellectual": 0.7},
                research_complexity=0.8,
                discovery_chance=0.05,
                benefits={"wisdom": 2.0, "decision_making": 1.8, "social_harmony": 1.5},
                unlock_actions=["contemplate_existence", "teach_ethics", "resolve_moral_dilemmas"]
            ),
            
            # Advanced Medicine Technologies
            "advanced_surgery": Technology(
                id="advanced_surgery",
                name="Advanced Surgery",
                category=TechnologyCategory.MEDICINE,
                description="Complex surgical procedures and techniques",
                prerequisites=["surgical_techniques", "metalworking"],
                required_skills={"medicine": 0.95, "precision": 0.9},
                research_complexity=0.95,
                discovery_chance=0.01,
                benefits={"complex_treatment": 3.0, "survival_rate": 2.5},
                unlock_actions=["perform_advanced_surgery", "train_surgeons"]
            ),
            "disease_theory": Technology(
                id="disease_theory",
                name="Disease Theory",
                category=TechnologyCategory.MEDICINE,
                description="Understanding of how diseases spread and can be prevented",
                prerequisites=["herbal_medicine", "written_language"],
                required_skills={"medicine": 0.8, "observation": 0.7},
                research_complexity=0.85,
                discovery_chance=0.03,
                benefits={"epidemic_prevention": 3.0, "public_health": 2.5},
                unlock_actions=["quarantine_disease", "prevent_epidemics"]
            ),
            
            # Advanced Military Technologies
            "metallurgy": Technology(
                id="metallurgy",
                name="Metallurgy",
                category=TechnologyCategory.MILITARY,
                description="Advanced metal working and alloy creation",
                prerequisites=["metalworking", "fire_advanced"],
                required_skills={"crafting": 0.9, "chemistry": 0.7},
                research_complexity=0.9,
                discovery_chance=0.02,
                benefits={"weapon_quality": 3.0, "tool_durability": 2.5, "armor_protection": 2.0},
                unlock_actions=["forge_advanced_weapons", "create_alloys"]
            ),
            "fire_advanced": Technology(
                id="fire_advanced",
                name="Advanced Fire Control",
                category=TechnologyCategory.CRAFTING,
                description="High-temperature fires and advanced combustion",
                prerequisites=["fire_making", "construction_basic"],
                required_skills={"crafting": 0.7, "engineering": 0.6},
                research_complexity=0.7,
                discovery_chance=0.05,
                benefits={"smelting": 2.0, "metalworking": 1.8},
                unlock_actions=["build_furnaces", "smelt_metals"]
            ),
            "tactical_warfare": Technology(
                id="tactical_warfare",
                name="Tactical Warfare",
                category=TechnologyCategory.MILITARY,
                description="Advanced military strategy and battlefield tactics",
                prerequisites=["written_language", "metallurgy"],
                required_skills={"strategy": 0.8, "leadership": 0.7},
                research_complexity=0.8,
                discovery_chance=0.03,
                benefits={"military_effectiveness": 3.0, "conquest_ability": 2.5},
                unlock_actions=["plan_military_campaigns", "train_armies"]
            ),
            
            # Advanced Social Technologies
            "diplomacy": Technology(
                id="diplomacy",
                name="Diplomacy",
                category=TechnologyCategory.SOCIAL,
                description="Formal diplomatic relations and treaty making",
                prerequisites=["legal_system", "currency_system"],
                required_skills={"negotiation": 0.8, "persuasion": 0.7},
                research_complexity=0.8,
                discovery_chance=0.04,
                benefits={"peace_agreements": 2.5, "trade_relations": 2.0},
                unlock_actions=["negotiate_treaties", "establish_embassies"]
            ),
            "complex_governance": Technology(
                id="complex_governance",
                name="Complex Governance",
                category=TechnologyCategory.SOCIAL,
                description="Advanced governmental structures and administration",
                prerequisites=["legal_system", "written_language"],
                required_skills={"leadership": 0.85, "organization": 0.8},
                research_complexity=0.9,
                discovery_chance=0.02,
                benefits={"administrative_efficiency": 3.0, "large_scale_coordination": 2.5},
                unlock_actions=["establish_bureaucracy", "coordinate_large_projects"]
            ),
            
            # Advanced Spiritual Technologies
            "organized_religion": Technology(
                id="organized_religion",
                name="Organized Religion",
                category=TechnologyCategory.SPIRITUAL,
                description="Formal religious institutions and practices",
                prerequisites=["written_language", "construction_basic"],
                required_skills={"spiritual": 0.8, "leadership": 0.6},
                research_complexity=0.7,
                discovery_chance=0.05,
                benefits={"social_cohesion": 2.0, "moral_guidance": 2.5},
                unlock_actions=["build_temples", "conduct_ceremonies", "train_priests"]
            ),
            "mysticism": Technology(
                id="mysticism",
                name="Mysticism",
                category=TechnologyCategory.SPIRITUAL,
                description="Deep spiritual practices and esoteric knowledge",
                prerequisites=["organized_religion", "philosophy"],
                required_skills={"spiritual": 0.9, "wisdom": 0.8},
                research_complexity=0.85,
                discovery_chance=0.02,
                benefits={"spiritual_insight": 3.0, "inner_peace": 2.0},
                unlock_actions=["practice_mysticism", "achieve_enlightenment"]
            )
        })
        
        # Initialize technology advantages
        self._initialize_technology_advantages()
        
        # Build technology tree relationships
        self._build_technology_tree()
    
    def _initialize_technology_advantages(self):
        """Initialize technology advantages for various activities."""
        self.technology_advantages = {
            # Military advantages
            "metallurgy": {"combat_effectiveness": 2.0, "weapon_damage": 3.0, "armor_defense": 2.5},
            "tactical_warfare": {"military_strategy": 3.0, "battlefield_coordination": 2.5, "victory_chance": 2.0},
            
            # Economic advantages  
            "currency_system": {"trade_efficiency": 2.5, "wealth_accumulation": 2.0, "market_development": 1.8},
            "advanced_mathematics": {"trade_calculations": 2.0, "construction_precision": 1.8, "resource_efficiency": 1.5},
            
            # Social advantages
            "diplomacy": {"negotiation_success": 2.5, "peace_treaty_duration": 2.0, "alliance_stability": 1.8},
            "complex_governance": {"organization_efficiency": 3.0, "large_project_success": 2.5, "social_stability": 2.0},
            "legal_system": {"conflict_resolution": 2.5, "social_order": 2.0, "crime_prevention": 1.8},
            
            # Knowledge advantages
            "written_language": {"knowledge_preservation": 3.0, "learning_speed": 2.0, "cultural_transmission": 2.5},
            "philosophy": {"wisdom_development": 2.0, "ethical_decision_making": 2.5, "moral_leadership": 1.8},
            "astronomy": {"navigation_accuracy": 2.5, "calendar_precision": 3.0, "prediction_ability": 2.0},
            
            # Medical advantages
            "advanced_surgery": {"healing_effectiveness": 3.0, "trauma_survival": 2.5, "medical_reputation": 2.0},
            "disease_theory": {"epidemic_prevention": 3.0, "public_health": 2.5, "population_health": 2.0},
            
            # Construction advantages
            "advanced_architecture": {"building_quality": 3.0, "monument_construction": 2.5, "city_planning": 2.0},
            "construction_basic": {"shelter_quality": 1.5, "infrastructure_development": 1.8, "durability": 1.3},
            
            # Spiritual advantages
            "organized_religion": {"social_cohesion": 2.0, "moral_authority": 2.5, "cultural_unity": 1.8},
            "mysticism": {"spiritual_insight": 3.0, "inner_peace": 2.0, "wisdom_teaching": 2.5}
        }
    
    def _build_technology_tree(self):
        """Build the technology dependency tree."""
        self.technology_tree = {}
        
        for tech_id, technology in self.technologies.items():
            self.technology_tree[tech_id] = {
                "prerequisites": technology.prerequisites,
                "unlocks": []
            }
        
        # Build unlock relationships
        for tech_id, technology in self.technologies.items():
            for prereq in technology.prerequisites:
                if prereq in self.technology_tree:
                    self.technology_tree[prereq]["unlocks"].append(tech_id)
    
    def process_daily_technology_activities(self, agents: List[Any], groups: Dict[str, Any], 
                                         current_day: int) -> List[Dict[str, Any]]:
        """Process all technology-related activities for a day."""
        events = []
        
        # 1. Process active research projects
        research_events = self._process_research_projects(agents, current_day)
        events.extend(research_events)
        
        # 2. Check for spontaneous discoveries
        discovery_events = self._check_spontaneous_discoveries(agents, current_day)
        events.extend(discovery_events)
        
        # 3. Process innovation attempts
        innovation_events = self._process_innovations(agents, current_day)
        events.extend(innovation_events)
        
        # 4. Handle knowledge sharing and technology transfer
        transfer_events = self._process_knowledge_transfer(agents, groups, current_day)
        events.extend(transfer_events)
        
        # 5. Check for new research project initiation
        initiation_events = self._check_research_initiation(agents, groups, current_day)
        events.extend(initiation_events)
        
        # Phase 6 Enhancements
        # 6. Process technology goals
        goal_events = self._process_technology_goals(agents, groups, current_day)
        events.extend(goal_events)
        
        # 7. Process technology competitions
        competition_events = self._process_technology_competitions(agents, groups, current_day)
        events.extend(competition_events)
        
        # 8. Process research failures
        failure_events = self._process_research_failures(agents, current_day)
        events.extend(failure_events)
        
        # 9. Process technology-based conflicts
        conflict_events = self._process_technology_conflicts(agents, groups, current_day)
        events.extend(conflict_events)
        
        # 10. Update agent and group technology knowledge
        self._update_technology_knowledge(agents, groups, current_day)
        
        return events
    
    def _process_research_projects(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process progress on active research projects."""
        events = []
        
        for project_id, project in list(self.research_projects.items()):
            if project.status != ResearchStatus.IN_PROGRESS:
                continue
            
            # Get lead researcher
            lead_agent = next((a for a in agents if a.name == project.lead_researcher), None)
            if not lead_agent or not lead_agent.is_alive:
                # Project leader is unavailable, slow progress or abandon
                if random.random() < 0.3:  # 30% chance to abandon
                    project.status = ResearchStatus.ABANDONED
                    events.append({
                        "type": "research_abandoned",
                        "project": project_id,
                        "reason": "lead_researcher_unavailable",
                        "day": current_day
                    })
                continue
            
            # Calculate daily progress
            base_progress = project.daily_progress_rate
            
            # Factor in lead researcher's relevant skills
            technology = self.technologies[project.technology_id]
            skill_bonus = 0.0
            for skill_name, min_level in technology.required_skills.items():
                if hasattr(lead_agent, 'skills') and skill_name in lead_agent.skills:
                    # Handle both simple float skills and Skill objects
                    skill_value = lead_agent.skills[skill_name]
                    if hasattr(skill_value, 'get_effective_level'):
                        skill_level = skill_value.get_effective_level()
                    else:
                        skill_level = float(skill_value)
                    skill_bonus += max(0, skill_level - min_level) * 0.5
            
            # Factor in collaborators
            collaboration_bonus = 0.0
            active_collaborators = 0
            for collaborator_name in project.collaborators:
                collaborator = next((a for a in agents if a.name == collaborator_name), None)
                if collaborator and collaborator.is_alive:
                    active_collaborators += 1
                    # Each collaborator adds based on their relevant skills
                    for skill_name in technology.required_skills:
                        if hasattr(collaborator, 'skills') and skill_name in collaborator.skills:
                            skill_value = collaborator.skills[skill_name]
                            if hasattr(skill_value, 'get_effective_level'):
                                skill_level = skill_value.get_effective_level()
                            else:
                                skill_level = float(skill_value)
                            collaboration_bonus += skill_level * 0.2
            
            # Calculate total progress for the day
            total_progress = base_progress + skill_bonus + collaboration_bonus
            total_progress *= random.uniform(0.7, 1.3)  # Daily variation
            
            project.progress += total_progress
            project.last_progress_day = current_day
            
            # Check for breakthrough
            progress_ratio = project.progress / project.required_progress
            if len(project.breakthrough_chances) > 0:
                stage = min(int(progress_ratio * len(project.breakthrough_chances)), 
                           len(project.breakthrough_chances) - 1)
                if random.random() < project.breakthrough_chances[stage]:
                    # Breakthrough! Accelerate progress
                    project.progress += project.required_progress * 0.3
                    events.append({
                        "type": "research_breakthrough",
                        "project": project_id,
                        "researcher": project.lead_researcher,
                        "day": current_day,
                        "technology": project.technology_id
                    })
            
            # Check for completion
            if project.progress >= project.required_progress:
                project.status = ResearchStatus.COMPLETED
                technology = self.technologies[project.technology_id]
                technology.is_discovered = True
                technology.discovery_day = current_day
                technology.discovered_by = project.lead_researcher
                
                events.append({
                    "type": "technology_discovered",
                    "project": project_id,
                    "technology": project.technology_id,
                    "researcher": project.lead_researcher,
                    "collaborators": project.collaborators,
                    "day": current_day,
                    "research_duration": current_day - project.start_day
                })
                
                # Add knowledge to all participants
                self._add_technology_knowledge(project.lead_researcher, project.technology_id, 1.0)
                for collaborator in project.collaborators:
                    self._add_technology_knowledge(collaborator, project.technology_id, 0.8)
                
                # Add memories to participants
                memory_text = f"Successfully completed research on {technology.name}"
                lead_agent.memory.store_memory(memory_text, importance=0.8, memory_type="achievement")
                
                for collaborator_name in project.collaborators:
                    collaborator = next((a for a in agents if a.name == collaborator_name), None)
                    if collaborator:
                        collaborator.memory.store_memory(
                            f"Helped research {technology.name} with {project.lead_researcher}",
                            importance=0.6, memory_type="collaboration"
                        )
        
        return events
    
    def _check_spontaneous_discoveries(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Check for accidental or observational discoveries."""
        events = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            # Check each undiscovered technology for potential discovery
            for tech_id, technology in self.technologies.items():
                if technology.is_discovered:
                    continue
                
                # Check if agent meets prerequisites
                if not self._agent_has_prerequisites(agent.name, technology):
                    continue
                
                # Check discovery chance based on agent's activities and skills
                base_chance = technology.discovery_chance / 365  # Daily chance
                
                # Skill-based multiplier
                skill_multiplier = 1.0
                for skill_name, min_level in technology.required_skills.items():
                    if hasattr(agent, 'skills') and skill_name in agent.skills:
                        skill_value = agent.skills[skill_name]
                        if hasattr(skill_value, 'get_effective_level'):
                            skill_level = skill_value.get_effective_level()
                        else:
                            skill_level = float(skill_value)
                        if skill_level >= min_level:
                            skill_multiplier *= (1 + skill_level)
                
                # Personality-based multiplier
                discovery_chance = base_chance * skill_multiplier
                if hasattr(agent, 'personality') and isinstance(agent.personality, dict):
                    if 'openness' in agent.personality:
                        discovery_chance *= (1 + agent.personality['openness'])
                    if 'curiosity' in agent.personality:
                        discovery_chance *= (1 + agent.personality.get('curiosity', 0))
                
                if random.random() < discovery_chance:
                    # Spontaneous discovery!
                    technology.is_discovered = True
                    technology.discovery_day = current_day
                    technology.discovered_by = agent.name
                    
                    events.append({
                        "type": "spontaneous_discovery",
                        "technology": tech_id,
                        "discoverer": agent.name,
                        "day": current_day,
                        "discovery_type": "observation"
                    })
                    
                    # Add knowledge to discoverer
                    self._add_technology_knowledge(agent.name, tech_id, 1.0)
                    
                    # Add memory
                    agent.memory.store_memory(
                        f"Discovered {technology.name} through observation and experimentation",
                        importance=0.9, memory_type="discovery"
                    )
                    
                    break  # One discovery per agent per day
        
        return events
    
    def _process_innovations(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process attempts at technological innovation and improvement."""
        events = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            # Check for innovation attempt (low chance)
            innovation_chance = 0.01  # 1% base chance per day
            
            # Skill-based modifiers
            if hasattr(agent, 'skills'):
                if 'intellectual' in agent.skills:
                    skill_value = agent.skills['intellectual']
                    if hasattr(skill_value, 'get_effective_level'):
                        skill_level = skill_value.get_effective_level()
                    else:
                        skill_level = float(skill_value)
                    innovation_chance *= (1 + skill_level)
                if 'crafting' in agent.skills:
                    skill_value = agent.skills['crafting']
                    if hasattr(skill_value, 'get_effective_level'):
                        skill_level = skill_value.get_effective_level()
                    else:
                        skill_level = float(skill_value)
                    innovation_chance *= (1 + skill_level * 0.5)
            
            # Personality modifiers
            if hasattr(agent, 'personality'):
                if 'openness' in agent.personality:
                    innovation_chance *= (1 + agent.personality['openness'])
            
            if random.random() < innovation_chance:
                # Attempt innovation
                known_techs = self._get_agent_technologies(agent.name)
                if len(known_techs) < 2:
                    continue  # Need at least 2 technologies to innovate
                
                innovation_type = random.choice(list(InnovationType))
                
                if innovation_type == InnovationType.IMPROVEMENT:
                    # Improve existing technology
                    tech_to_improve = random.choice(list(known_techs))
                    innovation = self._create_improvement_innovation(agent, tech_to_improve, current_day)
                    
                elif innovation_type == InnovationType.COMBINATION:
                    # Combine two technologies
                    if len(known_techs) >= 2:
                        techs_to_combine = random.sample(list(known_techs), 2)
                        innovation = self._create_combination_innovation(agent, techs_to_combine, current_day)
                    else:
                        continue
                
                elif innovation_type == InnovationType.ADAPTATION:
                    # Adapt existing technology for new use
                    tech_to_adapt = random.choice(list(known_techs))
                    innovation = self._create_adaptation_innovation(agent, tech_to_adapt, current_day)
                
                else:
                    continue  # Skip other types for now
                
                if innovation:
                    self.innovations[innovation.id] = innovation
                    events.append({
                        "type": "innovation_created",
                        "innovation": innovation.id,
                        "innovator": agent.name,
                        "innovation_type": innovation.innovation_type.value,
                        "day": current_day
                    })
                    
                    # Add memory
                    agent.memory.store_memory(
                        f"Created innovation: {innovation.name}",
                        importance=0.8, memory_type="achievement"
                    )
        
        return events
    
    def _process_knowledge_transfer(self, agents: List[Any], groups: Dict[str, Any], 
                                  current_day: int) -> List[Dict[str, Any]]:
        """Process sharing of technological knowledge between agents and groups."""
        events = []
        
        # Agent-to-agent knowledge sharing
        for agent in agents:
            if not agent.is_alive:
                continue
            
            agent_techs = self._get_agent_technologies(agent.name)
            if len(agent_techs) == 0:
                continue
            
            # Check for teaching opportunities
            if random.random() < 0.1:  # 10% chance to teach each day
                # Find potential students
                potential_students = [
                    other for other in agents 
                    if other.is_alive and other.name != agent.name
                    and len(self._get_agent_technologies(other.name)) < len(agent_techs)
                ]
                
                if potential_students:
                    student = random.choice(potential_students)
                    tech_to_teach = random.choice(list(agent_techs))
                    
                    # Check if student already knows this technology
                    if not self._agent_knows_technology(student.name, tech_to_teach):
                        # Attempt knowledge transfer
                        success_chance = 0.6  # Base 60% success rate
                        
                        # Factor in teacher's teaching ability
                        if hasattr(agent, 'skills') and 'social' in agent.skills:
                            skill_value = agent.skills['social']
                            if hasattr(skill_value, 'get_effective_level'):
                                skill_level = skill_value.get_effective_level()
                            else:
                                skill_level = float(skill_value)
                            success_chance += skill_level * 0.3
                        
                        # Factor in student's learning ability
                        if hasattr(student, 'skills') and 'intellectual' in student.skills:
                            skill_value = student.skills['intellectual']
                            if hasattr(skill_value, 'get_effective_level'):
                                skill_level = skill_value.get_effective_level()
                            else:
                                skill_level = float(skill_value)
                            success_chance += skill_level * 0.2
                        
                        # Factor in relationship
                        if hasattr(agent, 'relationships') and student.name in agent.relationships:
                            relationship = agent.relationships[student.name]
                            # Convert relationship string to numeric strength
                            if isinstance(relationship, dict):
                                relationship_strength = relationship.get('strength', 0)
                            else:
                                # Map relationship strings to numeric values
                                relationship_mapping = {
                                    "family": 0.8,
                                    "friend": 0.6,
                                    "mentor": 0.7,
                                    "student": 0.7,
                                    "acquaintance": 0.3,
                                    "stranger": 0.1
                                }
                                relationship_strength = relationship_mapping.get(relationship, 0.1)
                            success_chance += relationship_strength * 0.2
                        
                        if random.random() < success_chance:
                            # Successful knowledge transfer
                            knowledge_level = random.uniform(0.5, 0.8)  # Partial knowledge from teaching
                            self._add_technology_knowledge(student.name, tech_to_teach, knowledge_level)
                            
                            events.append({
                                "type": "knowledge_transfer",
                                "teacher": agent.name,
                                "student": student.name,
                                "technology": tech_to_teach,
                                "day": current_day
                            })
                            
                            # Add memories
                            technology = self.technologies[tech_to_teach]
                            agent.memory.store_memory(
                                f"Taught {technology.name} to {student.name}",
                                importance=0.5, memory_type="social"
                            )
                            student.memory.store_memory(
                                f"Learned {technology.name} from {agent.name}",
                                importance=0.7, memory_type="learning"
                            )
        
        # Group-based knowledge sharing
        for group_name, group_data in groups.items():
            if group_data.get("type") == "institution":
                # Institutions facilitate knowledge sharing
                events.extend(self._process_institutional_knowledge_sharing(
                    group_name, group_data, agents, current_day))
        
        return events
    
    def _check_research_initiation(self, agents: List[Any], groups: Dict[str, Any], 
                                 current_day: int) -> List[Dict[str, Any]]:
        """Check for new research projects being initiated."""
        events = []
        
        # Individual research initiation
        for agent in agents:
            if not agent.is_alive:
                continue
            
            # Check if agent is already leading a research project
            if any(project.lead_researcher == agent.name and project.status == ResearchStatus.IN_PROGRESS
                   for project in self.research_projects.values()):
                continue
            
            # Check for research interest
            if random.random() < 0.05:  # 5% chance per day
                available_techs = self._get_available_research_technologies(agent.name)
                if available_techs:
                    tech_to_research = random.choice(available_techs)
                    project = self._initiate_research_project(agent.name, tech_to_research, None, current_day)
                    
                    if project:
                        events.append({
                            "type": "research_initiated",
                            "project": project.id,
                            "researcher": agent.name,
                            "technology": tech_to_research,
                            "day": current_day
                        })
                        
                        # Add memory
                        technology = self.technologies[tech_to_research]
                        agent.memory.store_memory(
                            f"Started researching {technology.name}",
                            importance=0.6, memory_type="goal"
                        )
        
        # Group research initiation
        for group_name, group_data in groups.items():
            if group_data.get("type") in ["institution", "guild"]:
                # These group types can sponsor research
                if random.random() < 0.08:  # 8% chance per day for groups
                    available_techs = self._get_group_research_opportunities(group_name, group_data, agents)
                    if available_techs:
                        tech_to_research = random.choice(available_techs)
                        
                        # Find suitable lead researcher from group members
                        potential_leaders = [
                            agent for agent in agents
                            if agent.name in group_data.get("members", [])
                            and agent.is_alive
                            and self._agent_can_research(agent.name, tech_to_research)
                        ]
                        
                        if potential_leaders:
                            leader = max(potential_leaders, 
                                       key=lambda a: self._calculate_research_aptitude(a.name, tech_to_research))
                            
                            project = self._initiate_research_project(
                                leader.name, tech_to_research, group_name, current_day)
                            
                            if project:
                                events.append({
                                    "type": "group_research_initiated",
                                    "project": project.id,
                                    "group": group_name,
                                    "lead_researcher": leader.name,
                                    "technology": tech_to_research,
                                    "day": current_day
                                })
        
        return events
    
    def _agent_has_prerequisites(self, agent_name: str, technology: Technology) -> bool:
        """Check if an agent has the prerequisite technologies."""
        agent_techs = self._get_agent_technologies(agent_name)
        return all(prereq in agent_techs for prereq in technology.prerequisites)
    
    def _get_agent_technologies(self, agent_name: str) -> Set[str]:
        """Get set of technologies known by an agent."""
        return set(self.agent_knowledge.get(agent_name, {}).keys())
    
    def _agent_knows_technology(self, agent_name: str, tech_id: str) -> bool:
        """Check if an agent knows a specific technology."""
        return tech_id in self.agent_knowledge.get(agent_name, {})
    
    def _add_technology_knowledge(self, agent_name: str, tech_id: str, knowledge_level: float):
        """Add technology knowledge to an agent."""
        if agent_name not in self.agent_knowledge:
            self.agent_knowledge[agent_name] = {}
        self.agent_knowledge[agent_name][tech_id] = min(1.0, knowledge_level)
    
    def _get_available_research_technologies(self, agent_name: str) -> List[str]:
        """Get list of technologies available for research by an agent."""
        available = []
        agent_techs = self._get_agent_technologies(agent_name)
        
        for tech_id, technology in self.technologies.items():
            if technology.is_discovered:
                continue
            if not self._agent_has_prerequisites(agent_name, technology):
                continue
            if tech_id in [p.technology_id for p in self.research_projects.values() 
                          if p.status == ResearchStatus.IN_PROGRESS]:
                continue
            
            available.append(tech_id)
        
        return available
    
    def _initiate_research_project(self, lead_researcher: str, tech_id: str, 
                                 group_id: Optional[str], current_day: int) -> Optional[ResearchProject]:
        """Initiate a new research project."""
        technology = self.technologies[tech_id]
        
        # Calculate research requirements
        base_progress_needed = technology.research_complexity * 100
        complexity_modifier = random.uniform(0.8, 1.2)
        required_progress = base_progress_needed * complexity_modifier
        
        # Calculate daily progress rate
        base_rate = 1.0
        daily_rate = base_rate * random.uniform(0.8, 1.2)
        
        # Estimate completion time
        estimated_days = int(required_progress / daily_rate)
        
        # Create project
        project_id = f"research_{tech_id}_{current_day}"
        project = ResearchProject(
            id=project_id,
            technology_id=tech_id,
            lead_researcher=lead_researcher,
            collaborators=[],
            group_id=group_id,
            status=ResearchStatus.IN_PROGRESS,
            progress=0.0,
            required_progress=required_progress,
            start_day=current_day,
            estimated_completion=current_day + estimated_days,
            daily_progress_rate=daily_rate,
            last_progress_day=current_day,
            resources_invested={},
            breakthrough_chances=[0.1, 0.15, 0.2, 0.25]  # Increasing chances as research progresses
        )
        
        self.research_projects[project_id] = project
        return project
    
    def _calculate_research_aptitude(self, agent_name: str, tech_id: str) -> float:
        """Calculate an agent's aptitude for researching a specific technology."""
        # This would need to access agent skills - simplified for now
        return random.uniform(0.3, 1.0)
    
    def _agent_can_research(self, agent_name: str, tech_id: str) -> bool:
        """Check if an agent can research a specific technology."""
        technology = self.technologies[tech_id]
        return self._agent_has_prerequisites(agent_name, technology)
    
    def _get_group_research_opportunities(self, group_name: str, group_data: Dict[str, Any], 
                                        agents: List[Any]) -> List[str]:
        """Get research opportunities for a group."""
        # Simplified - would normally consider group capabilities and needs
        available = []
        for tech_id, technology in self.technologies.items():
            if not technology.is_discovered:
                available.append(tech_id)
        return available[:3]  # Limit to 3 opportunities
    
    def _create_improvement_innovation(self, agent: Any, tech_id: str, current_day: int) -> Optional[Innovation]:
        """Create an improvement innovation for existing technology."""
        technology = self.technologies[tech_id]
        innovation_id = f"improve_{tech_id}_{current_day}_{agent.name}"
        
        innovation = Innovation(
            id=innovation_id,
            name=f"Improved {technology.name}",
            innovation_type=InnovationType.IMPROVEMENT,
            technology_affected=tech_id,
            innovator=agent.name,
            day_discovered=current_day,
            description=f"An enhancement to {technology.name} that makes it more effective",
            impact_level=random.uniform(0.3, 0.7),
            adoption_rate=random.uniform(0.1, 0.4),
            knowledge_requirements={tech_id: 0.8}
        )
        
        return innovation
    
    def _create_combination_innovation(self, agent: Any, tech_ids: List[str], current_day: int) -> Optional[Innovation]:
        """Create a combination innovation from multiple technologies."""
        tech_names = [self.technologies[tid].name for tid in tech_ids]
        innovation_id = f"combine_{'_'.join(tech_ids)}_{current_day}_{agent.name}"
        
        innovation = Innovation(
            id=innovation_id,
            name=f"Combined {' and '.join(tech_names)}",
            innovation_type=InnovationType.COMBINATION,
            technology_affected=tech_ids[0],  # Primary technology affected
            innovator=agent.name,
            day_discovered=current_day,
            description=f"A novel combination of {' and '.join(tech_names)}",
            impact_level=random.uniform(0.5, 0.9),
            adoption_rate=random.uniform(0.05, 0.3),
            knowledge_requirements={tid: 0.6 for tid in tech_ids}
        )
        
        return innovation
    
    def _create_adaptation_innovation(self, agent: Any, tech_id: str, current_day: int) -> Optional[Innovation]:
        """Create an adaptation innovation for new use of existing technology."""
        technology = self.technologies[tech_id]
        innovation_id = f"adapt_{tech_id}_{current_day}_{agent.name}"
        
        innovation = Innovation(
            id=innovation_id,
            name=f"Adapted {technology.name}",
            innovation_type=InnovationType.ADAPTATION,
            technology_affected=tech_id,
            innovator=agent.name,
            day_discovered=current_day,
            description=f"A new application of {technology.name} for different purposes",
            impact_level=random.uniform(0.2, 0.6),
            adoption_rate=random.uniform(0.2, 0.5),
            knowledge_requirements={tech_id: 0.7}
        )
        
        return innovation
    
    def _process_institutional_knowledge_sharing(self, group_name: str, group_data: Dict[str, Any],
                                               agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process knowledge sharing within institutions."""
        events = []
        
        # Simplified institutional knowledge sharing
        if random.random() < 0.2:  # 20% chance for institutional knowledge event
            # Find members with different knowledge levels
            members = [agent for agent in agents if agent.name in group_data.get("members", [])]
            if len(members) >= 2:
                teacher = random.choice(members)
                student = random.choice([m for m in members if m.name != teacher.name])
                
                teacher_techs = self._get_agent_technologies(teacher.name)
                student_techs = self._get_agent_technologies(student.name)
                
                teachable_techs = teacher_techs - student_techs
                if teachable_techs:
                    tech_to_teach = random.choice(list(teachable_techs))
                    self._add_technology_knowledge(student.name, tech_to_teach, 0.6)
                    
                    events.append({
                        "type": "institutional_knowledge_sharing",
                        "institution": group_name,
                        "teacher": teacher.name,
                        "student": student.name,
                        "technology": tech_to_teach,
                        "day": current_day
                    })
        
        return events
    
    def _update_technology_knowledge(self, agents: List[Any], groups: Dict[str, Any], current_day: int):
        """Update technology knowledge levels and group technology access."""
        
        # Update group technology repositories
        for group_name, group_data in groups.items():
            group_techs = set()
            for member_name in group_data.get("members", []):
                member_techs = self._get_agent_technologies(member_name)
                group_techs.update(member_techs)
            self.group_technologies[group_name] = group_techs
    
    def get_agent_technology_summary(self, agent_name: str) -> Dict[str, Any]:
        """Get comprehensive technology summary for an agent."""
        agent_techs = self.agent_knowledge.get(agent_name, {})
        
        summary = {
            "total_technologies": len(agent_techs),
            "technologies_by_category": {},
            "research_projects": [],
            "innovations_created": [],
            "knowledge_levels": agent_techs
        }
        
        # Group by category
        for tech_id, knowledge_level in agent_techs.items():
            if tech_id in self.technologies:
                category = self.technologies[tech_id].category.value
                if category not in summary["technologies_by_category"]:
                    summary["technologies_by_category"][category] = []
                summary["technologies_by_category"][category].append({
                    "id": tech_id,
                    "name": self.technologies[tech_id].name,
                    "knowledge_level": knowledge_level
                })
        
        # Find research projects
        for project in self.research_projects.values():
            if project.lead_researcher == agent_name or agent_name in project.collaborators:
                summary["research_projects"].append({
                    "id": project.id,
                    "technology": project.technology_id,
                    "status": project.status.value,
                    "role": "lead" if project.lead_researcher == agent_name else "collaborator"
                })
        
        # Find innovations
        for innovation in self.innovations.values():
            if innovation.innovator == agent_name:
                summary["innovations_created"].append({
                    "id": innovation.id,
                    "name": innovation.name,
                    "type": innovation.innovation_type.value,
                    "impact": innovation.impact_level
                })
        
        return summary
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall technology system status."""
        discovered_techs = sum(1 for tech in self.technologies.values() if tech.is_discovered)
        active_projects = sum(1 for project in self.research_projects.values() 
                            if project.status == ResearchStatus.IN_PROGRESS)
        
        return {
            "total_technologies": len(self.technologies),
            "discovered_technologies": discovered_techs,
            "undiscovered_technologies": len(self.technologies) - discovered_techs,
            "active_research_projects": active_projects,
            "completed_projects": sum(1 for project in self.research_projects.values() 
                                    if project.status == ResearchStatus.COMPLETED),
            "total_innovations": len(self.innovations),
            "technologies_by_category": {
                category.value: sum(1 for tech in self.technologies.values() 
                                  if tech.category == category)
                for category in TechnologyCategory
            },
            "discovery_rate": f"{(discovered_techs / len(self.technologies)) * 100:.1f}%"
        }

    def get_technology_summary(self) -> Dict[str, Any]:
        """Get technology system summary for other systems."""
        discovered_techs = sum(1 for tech in self.technologies.values() if tech.is_discovered)
        active_projects = sum(1 for project in self.research_projects.values() 
                            if project.status == ResearchStatus.IN_PROGRESS)
        
        # Calculate average advancement level
        total_knowledge = 0.0
        knowledge_count = 0
        for agent_knowledge in self.agent_knowledge.values():
            for knowledge_level in agent_knowledge.values():
                total_knowledge += knowledge_level
                knowledge_count += 1
        
        avg_advancement = total_knowledge / knowledge_count if knowledge_count > 0 else 0.0
        
        # Count recent innovations
        recent_innovations = len([i for i in self.innovations.values() 
                                if hasattr(i, 'creation_day') and 
                                i.creation_day >= max(0, len(self.innovations) - 30)])
        
        return {
            "total_technologies": len(self.technologies),
            "discovered_technologies": discovered_techs,
            "active_research_projects": active_projects,
            "average_advancement": avg_advancement,
            "recent_innovations": recent_innovations,
            "technology_complexity": min(1.0, discovered_techs / len(self.technologies))
        }
    
    # ===== PHASE 6 ENHANCEMENTS =====
    
    def _process_technology_goals(self, agents: List[Any], groups: Dict[str, Any], 
                                current_day: int) -> List[Dict[str, Any]]:
        """Process technology goals and their progress."""
        events = []
        
        # Check for new technology goal creation
        if random.random() < 0.1:  # 10% chance per day
            goal_event = self._create_technology_goal(agents, groups, current_day)
            if goal_event:
                events.append(goal_event)
        
        # Process existing goals
        for goal_id, goal in list(self.technology_goals.items()):
            if goal.is_completed:
                continue
                
            # Check if target technology has been discovered
            target_tech = self.technologies.get(goal.target_technology)
            if target_tech and target_tech.is_discovered:
                goal.is_completed = True
                goal.completion_day = current_day
                
                events.append({
                    "type": "technology_goal_completed",
                    "goal_id": goal_id,
                    "goal_setter": goal.goal_setter,
                    "target_technology": goal.target_technology,
                    "completion_day": current_day,
                    "days_taken": current_day - goal.set_day,
                    "priority": goal.priority.value,
                    "reward": goal.completion_reward
                })
            
            # Check for goal deadline
            elif goal.target_completion_day and current_day >= goal.target_completion_day:
                events.append({
                    "type": "technology_goal_failed",
                    "goal_id": goal_id,
                    "goal_setter": goal.goal_setter,
                    "target_technology": goal.target_technology,
                    "failure_day": current_day,
                    "priority": goal.priority.value
                })
        
        return events
    
    def _create_technology_goal(self, agents: List[Any], groups: Dict[str, Any], 
                              current_day: int) -> Optional[Dict[str, Any]]:
        """Create a new technology goal."""
        # Select goal setter (agent or group)
        all_entities = [agent.name for agent in agents if agent.is_alive]
        all_entities.extend(groups.keys())
        
        if not all_entities:
            return None
        
        goal_setter = random.choice(all_entities)
        
        # Select target technology
        available_techs = [tech_id for tech_id, tech in self.technologies.items() 
                          if not tech.is_discovered]
        
        if not available_techs:
            return None
        
        target_tech = random.choice(available_techs)
        technology = self.technologies[target_tech]
        
        # Determine priority based on technology complexity
        if technology.research_complexity > 0.8:
            priority = TechnologyGoalPriority.HIGH
        elif technology.research_complexity > 0.5:
            priority = TechnologyGoalPriority.MEDIUM  
        else:
            priority = TechnologyGoalPriority.LOW
        
        # Set target completion time
        base_days = int(technology.research_complexity * 200)
        target_days = current_day + random.randint(base_days, base_days * 2)
        
        # Create goal
        goal_id = f"goal_{target_tech}_{current_day}"
        goal = TechnologyGoal(
            id=goal_id,
            target_technology=target_tech,
            goal_setter=goal_setter,
            priority=priority,
            set_day=current_day,
            target_completion_day=target_days,
            resources_allocated={"research_focus": 2.0, "time": 1.5},
            motivation=f"Seeking to discover {technology.name} for {goal_setter}",
            completion_reward={"reputation": 2.0, "knowledge": 1.5}
        )
        
        self.technology_goals[goal_id] = goal
        
        return {
            "type": "technology_goal_created",
            "goal_id": goal_id,
            "goal_setter": goal_setter,
            "target_technology": target_tech,
            "priority": priority.value,
            "target_completion": target_days,
            "motivation": goal.motivation
        }
    
    def _process_technology_competitions(self, agents: List[Any], groups: Dict[str, Any], 
                                       current_day: int) -> List[Dict[str, Any]]:
        """Process technology competitions between groups."""
        events = []
        
        # Check for new competition creation
        if random.random() < 0.05:  # 5% chance per day
            competition_event = self._create_technology_competition(agents, groups, current_day)
            if competition_event:
                events.append(competition_event)
        
        # Process existing competitions
        for comp_id, competition in list(self.technology_competitions.items()):
            if not competition.is_active:
                continue
            
            target_tech = self.technologies.get(competition.target_technology)
            if target_tech and target_tech.is_discovered:
                # Competition ends - someone won
                winner = target_tech.discovered_by or "unknown"
                competition.is_active = False
                competition.winner = winner
                competition.end_day = current_day
                
                events.append({
                    "type": "technology_competition_ended",
                    "competition_id": comp_id,
                    "winner": winner,
                    "target_technology": competition.target_technology,
                    "competition_type": competition.competition_type.value,
                    "participants": competition.participants,
                    "duration": current_day - competition.start_day
                })
            
            # Check for sabotage attempts
            elif random.random() < 0.02:  # 2% chance for sabotage
                sabotage_event = self._attempt_sabotage(competition, current_day)
                if sabotage_event:
                    events.append(sabotage_event)
        
        return events
    
    def _create_technology_competition(self, agents: List[Any], groups: Dict[str, Any], 
                                     current_day: int) -> Optional[Dict[str, Any]]:
        """Create a new technology competition."""
        # Find groups with research capabilities
        research_groups = [group_name for group_name, group_data in groups.items()
                          if group_data.get("type") in ["institution", "guild"] and
                          len(group_data.get("members", [])) >= 2]
        
        if len(research_groups) < 2:
            return None
        
        # Select competing groups
        participants = random.sample(research_groups, min(3, len(research_groups)))
        
        # Select target technology
        available_techs = [tech_id for tech_id, tech in self.technologies.items() 
                          if not tech.is_discovered and tech.research_complexity > 0.6]
        
        if not available_techs:
            return None
        
        target_tech = random.choice(available_techs)
        
        # Determine competition type
        comp_type = random.choice([CompetitionType.RESEARCH_RACE, CompetitionType.INNOVATION_WAR])
        
        # Create competition
        comp_id = f"competition_{target_tech}_{current_day}"
        competition = TechnologyCompetition(
            id=comp_id,
            competition_type=comp_type,
            target_technology=target_tech,
            participants=participants,
            start_day=current_day,
            current_leader=None,
            leader_progress=0.0,
            stakes={"reputation": 3.0, "resources": 2.0, "knowledge": 2.5},
            sabotage_attempts=[]
        )
        
        self.technology_competitions[comp_id] = competition
        
        return {
            "type": "technology_competition_started",
            "competition_id": comp_id,
            "competition_type": comp_type.value,
            "target_technology": target_tech,
            "participants": participants,
            "stakes": competition.stakes
        }
    
    def _attempt_sabotage(self, competition: TechnologyCompetition, current_day: int) -> Optional[Dict[str, Any]]:
        """Attempt sabotage in a technology competition."""
        if len(competition.participants) < 2:
            return None
        
        saboteur = random.choice(competition.participants)
        target = random.choice([p for p in competition.participants if p != saboteur])
        
        # Record sabotage attempt
        sabotage_record = f"{saboteur} vs {target} on day {current_day}"
        competition.sabotage_attempts.append(sabotage_record)
        
        return {
            "type": "technology_sabotage_attempt",
            "competition_id": competition.id,
            "saboteur": saboteur,
            "target": target,
            "target_technology": competition.target_technology,
            "success": random.random() < 0.3  # 30% success rate
        }
    
    def _process_research_failures(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process research project failures and their consequences."""
        events = []
        
        for project_id, project in list(self.research_projects.items()):
            if project.status != ResearchStatus.IN_PROGRESS:
                continue
            
            # Check for various failure conditions
            failure_chance = 0.02  # 2% base failure chance per day
            
            # Increase failure chance based on project complexity
            technology = self.technologies[project.technology_id]
            failure_chance += technology.research_complexity * 0.01
            
            # Check for failure
            if random.random() < failure_chance:
                failure_event = self._handle_research_failure(project, current_day)
                if failure_event:
                    events.append(failure_event)
        
        return events
    
    def _handle_research_failure(self, project: ResearchProject, current_day: int) -> Optional[Dict[str, Any]]:
        """Handle a research project failure."""
        # Determine failure type
        failure_types = [
            ResearchFailureType.RESOURCE_DEPLETION,
            ResearchFailureType.SKILL_INADEQUACY,
            ResearchFailureType.COLLABORATION_BREAKDOWN,
            ResearchFailureType.ACCIDENTAL_DESTRUCTION
        ]
        
        failure_type = random.choice(failure_types)
        
        # Calculate consequences
        resources_lost = {
            "time": project.progress * 0.5,
            "materials": random.uniform(0.2, 0.8),
            "reputation": random.uniform(0.1, 0.3)
        }
        
        skill_penalties = {
            "research_confidence": -0.1,
            "collaboration": -0.05 if failure_type == ResearchFailureType.COLLABORATION_BREAKDOWN else 0.0
        }
        
        lessons_learned = {
            "failure_recovery": 0.1,
            "risk_assessment": 0.05
        }
        
        # Create failure record
        failure_id = f"failure_{project.id}_{current_day}"
        failure = ResearchFailure(
            id=failure_id,
            project_id=project.id,
            failure_type=failure_type,
            failure_day=current_day,
            lead_researcher=project.lead_researcher,
            resources_lost=resources_lost,
            skill_penalties=skill_penalties,
            description=f"{failure_type.value} caused research failure",
            consequences=[f"Lost {resources_lost['materials']:.1f} materials", 
                         f"Reputation decreased by {resources_lost['reputation']:.1f}"],
            lessons_learned=lessons_learned
        )
        
        self.research_failures[failure_id] = failure
        
        # Update project status
        project.status = ResearchStatus.ABANDONED
        
        return {
            "type": "research_failure",
            "failure_id": failure_id,
            "project_id": project.id,
            "failure_type": failure_type.value,
            "lead_researcher": project.lead_researcher,
            "technology": project.technology_id,
            "resources_lost": resources_lost,
            "lessons_learned": lessons_learned
        }
    
    def _process_technology_conflicts(self, agents: List[Any], groups: Dict[str, Any], 
                                    current_day: int) -> List[Dict[str, Any]]:
        """Process conflicts arising from technology disparities."""
        events = []
        
        # Check for new technology conflicts
        if random.random() < 0.03:  # 3% chance per day
            conflict_event = self._create_technology_conflict(groups, current_day)
            if conflict_event:
                events.append(conflict_event)
        
        # Process existing conflicts
        for conflict_id, conflict in list(self.technology_conflicts.items()):
            if conflict.is_resolved:
                continue
            
            # Check for conflict escalation
            if random.random() < 0.1:  # 10% chance for escalation
                conflict.conflict_intensity = min(1.0, conflict.conflict_intensity + 0.1)
                
                events.append({
                    "type": "technology_conflict_escalation",
                    "conflict_id": conflict_id,
                    "advantaged_side": conflict.advantaged_side,
                    "disadvantaged_side": conflict.disadvantaged_side,
                    "new_intensity": conflict.conflict_intensity
                })
            
            # Check for conflict resolution
            elif random.random() < 0.05:  # 5% chance for resolution
                resolution_event = self._resolve_technology_conflict(conflict, current_day)
                if resolution_event:
                    events.append(resolution_event)
        
        return events
    
    def _create_technology_conflict(self, groups: Dict[str, Any], current_day: int) -> Optional[Dict[str, Any]]:
        """Create a new technology-based conflict."""
        group_names = list(groups.keys())
        if len(group_names) < 2:
            return None
        
        # Find groups with significant technology disparities
        group_a, group_b = random.sample(group_names, 2)
        
        techs_a = self.group_technologies.get(group_a, set())
        techs_b = self.group_technologies.get(group_b, set())
        
        # Calculate technology gap
        tech_gap = list(techs_a - techs_b) if len(techs_a) > len(techs_b) else list(techs_b - techs_a)
        
        if len(tech_gap) < 2:  # Need significant gap
            return None
        
        advantaged_side = group_a if len(techs_a) > len(techs_b) else group_b
        disadvantaged_side = group_b if advantaged_side == group_a else group_a
        
        # Create conflict
        conflict_id = f"tech_conflict_{advantaged_side}_{disadvantaged_side}_{current_day}"
        conflict = TechnologyConflict(
            id=conflict_id,
            conflict_type="technology_disparity",
            advantaged_side=advantaged_side,
            disadvantaged_side=disadvantaged_side,
            technology_gap=tech_gap,
            conflict_intensity=random.uniform(0.3, 0.7),
            start_day=current_day,
            resolution_attempts=[]
        )
        
        self.technology_conflicts[conflict_id] = conflict
        
        return {
            "type": "technology_conflict_started",
            "conflict_id": conflict_id,
            "advantaged_side": advantaged_side,
            "disadvantaged_side": disadvantaged_side,
            "technology_gap": tech_gap,
            "conflict_intensity": conflict.conflict_intensity
        }
    
    def _resolve_technology_conflict(self, conflict: TechnologyConflict, current_day: int) -> Optional[Dict[str, Any]]:
        """Resolve a technology conflict."""
        resolution_methods = [
            "technology_sharing", "peaceful_negotiation", "technology_trade", 
            "research_collaboration", "diplomatic_solution"
        ]
        
        resolution = random.choice(resolution_methods)
        conflict.resolution_attempts.append(f"{resolution} on day {current_day}")
        
        # Mark as resolved
        conflict.is_resolved = True
        conflict.resolution_day = current_day
        conflict.outcome = resolution
        
        return {
            "type": "technology_conflict_resolved",
            "conflict_id": conflict.id,
            "resolution_method": resolution,
            "advantaged_side": conflict.advantaged_side,
            "disadvantaged_side": conflict.disadvantaged_side,
            "duration": current_day - conflict.start_day
        }
    
    def get_technology_advantage(self, entity_name: str, advantage_type: str) -> float:
        """Get technology advantage bonus for an entity in a specific area."""
        entity_techs = self.group_technologies.get(entity_name, set())
        if not entity_techs:
            # Try agent knowledge
            entity_techs = set(self.agent_knowledge.get(entity_name, {}).keys())
        
        total_bonus = 1.0
        
        for tech_id in entity_techs:
            if tech_id in self.technology_advantages:
                tech_advantages = self.technology_advantages[tech_id]
                if advantage_type in tech_advantages:
                    total_bonus *= tech_advantages[advantage_type]
        
        return total_bonus
    
    def get_enhanced_technology_summary(self) -> Dict[str, Any]:
        """Get comprehensive technology system summary including Phase 6 enhancements."""
        base_summary = self.get_technology_summary()
        
        # Add Phase 6 metrics
        active_goals = len([g for g in self.technology_goals.values() if not g.is_completed])
        active_competitions = len([c for c in self.technology_competitions.values() if c.is_active])
        total_failures = len(self.research_failures)
        active_conflicts = len([c for c in self.technology_conflicts.values() if not c.is_resolved])
        
        enhanced_summary = base_summary.copy()
        enhanced_summary.update({
            "active_technology_goals": active_goals,
            "active_competitions": active_competitions,
            "research_failures": total_failures,
            "technology_conflicts": active_conflicts,
            "advanced_technologies": len([t for t in self.technologies.values() 
                                        if t.research_complexity > 0.8 and t.is_discovered]),
            "competition_intensity": sum(c.conflict_intensity for c in self.technology_conflicts.values() 
                                       if not c.is_resolved) / max(1, active_conflicts)
        })
        
        return enhanced_summary 