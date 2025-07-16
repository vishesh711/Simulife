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
        
        # Build technology tree relationships
        self._build_technology_tree()
    
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
        
        # 6. Update agent and group technology knowledge
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
                if hasattr(agent, 'personality'):
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
                            relationship_strength = agent.relationships[student.name].get('strength', 0)
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