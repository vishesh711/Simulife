"""
Professional Specialization System for SimuLife
Manages agent specializations, expertise development, and role-based community functions.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum


class SpecializationType(Enum):
    """Types of specializations agents can develop."""
    ARTISAN = "artisan"         # Crafting and creation specialists
    SCHOLAR = "scholar"         # Knowledge and research specialists  
    HEALER = "healer"           # Medical and wellness specialists
    LEADER = "leader"           # Governance and organization specialists
    GUARDIAN = "guardian"       # Protection and security specialists
    EXPLORER = "explorer"       # Discovery and scouting specialists
    MERCHANT = "merchant"       # Trade and resource specialists
    MYSTIC = "mystic"           # Spiritual and wisdom specialists


@dataclass
class Specialization:
    """Represents an agent's professional specialization."""
    type: SpecializationType
    level: float = 1.0          # 1.0 to 5.0 scale (Novice to Master)
    experience: float = 0.0     # Experience in this specialization
    reputation: float = 0.5     # Community recognition (0.0 to 1.0)
    responsibilities: Set[str] = None  # Specific duties in the community
    apprentices: List[str] = None      # Agents being mentored
    innovations: List[str] = None      # Contributions to the field
    established_day: int = 0    # When specialization was first recognized
    
    def __post_init__(self):
        if self.responsibilities is None:
            self.responsibilities = set()
        if self.apprentices is None:
            self.apprentices = []
        if self.innovations is None:
            self.innovations = []
    
    def get_title(self) -> str:
        """Get the agent's title based on specialization level."""
        level_titles = {
            SpecializationType.ARTISAN: ["Apprentice Crafter", "Skilled Crafter", "Master Artisan", "Grand Artisan", "Legendary Creator"],
            SpecializationType.SCHOLAR: ["Student", "Researcher", "Sage", "Master Scholar", "Grand Philosopher"],
            SpecializationType.HEALER: ["Healer's Aid", "Village Healer", "Master Healer", "Chief Healer", "Legendary Physician"],
            SpecializationType.LEADER: ["Group Leader", "Community Organizer", "Elder", "Chief", "Grand Leader"],
            SpecializationType.GUARDIAN: ["Scout", "Guardian", "Protector", "Captain", "Champion"],
            SpecializationType.EXPLORER: ["Wanderer", "Scout", "Explorer", "Pathfinder", "Master Navigator"],
            SpecializationType.MERCHANT: ["Trader", "Merchant", "Master Trader", "Trade Master", "Commerce Lord"],
            SpecializationType.MYSTIC: ["Seeker", "Mystic", "Wise One", "Spiritual Guide", "Grand Oracle"]
        }
        
        level_index = min(4, max(0, int(self.level) - 1))
        return level_titles[self.type][level_index]
    
    def advance_experience(self, experience_gained: float, current_day: int):
        """Add experience and potentially advance specialization level."""
        self.experience += experience_gained
        
        # Level advancement requires exponentially more experience
        required_exp = (self.level ** 2) * 100
        if self.experience >= required_exp and self.level < 5.0:
            self.level += 0.5
            return True  # Level up occurred
        return False
    
    def gain_reputation(self, amount: float):
        """Increase or decrease reputation within bounds."""
        self.reputation = max(0.0, min(1.0, self.reputation + amount))


@dataclass
class SpecializationRequirements:
    """Requirements for establishing a specialization."""
    required_skills: Dict[str, float]  # Minimum skill levels
    required_traits: List[str]         # Personality traits that help
    min_total_skill_level: float = 10.0  # Sum of all relevant skills
    community_need: bool = True        # Whether community needs this role
    
    def check_eligibility(self, agent, skill_system) -> Tuple[bool, List[str]]:
        """Check if agent meets requirements for this specialization."""
        issues = []
        
        if not hasattr(agent, 'advanced_skills'):
            agent.advanced_skills = skill_system.initialize_agent_skills(agent)
        
        # Check individual skill requirements
        for skill_name, min_level in self.required_skills.items():
            if skill_name not in agent.advanced_skills:
                issues.append(f"Missing {skill_name} skill")
            elif agent.advanced_skills[skill_name].get_effective_level() < min_level:
                current = agent.advanced_skills[skill_name].get_effective_level()
                issues.append(f"{skill_name} level {current:.1f} < required {min_level}")
        
        # Check total skill level
        total_skill = sum(agent.advanced_skills[skill].get_effective_level() 
                         for skill in self.required_skills.keys() 
                         if skill in agent.advanced_skills)
        
        if total_skill < self.min_total_skill_level:
            issues.append(f"Total skill level {total_skill:.1f} < required {self.min_total_skill_level}")
        
        # Check trait requirements (at least one matching trait required)
        matching_traits = any(trait in agent.traits for trait in self.required_traits)
        if not matching_traits:
            issues.append(f"Needs one of these traits: {', '.join(self.required_traits)}")
        
        return len(issues) == 0, issues


class SpecializationSystem:
    """
    Manages professional specializations and community roles.
    """
    
    def __init__(self):
        self.specialization_requirements = self._initialize_requirements()
        self.community_roles = {}  # Track who holds what roles
        self.specialization_events = []  # Track major specialization events
        
    def _initialize_requirements(self) -> Dict[SpecializationType, SpecializationRequirements]:
        """Initialize requirements for each specialization type."""
        return {
            SpecializationType.ARTISAN: SpecializationRequirements(
                required_skills={"toolmaking": 2.5, "construction": 2.0, "artistry": 2.0},
                required_traits=["creative", "patient", "precise", "artistic"],
                min_total_skill_level=8.0
            ),
            
            SpecializationType.SCHOLAR: SpecializationRequirements(
                required_skills={"research": 2.5, "teaching": 2.0, "storytelling": 1.5},
                required_traits=["curious", "intelligent", "wise", "patient"],
                min_total_skill_level=7.5
            ),
            
            SpecializationType.HEALER: SpecializationRequirements(
                required_skills={"medicine": 3.0, "foraging": 2.0},
                required_traits=["empathetic", "careful", "wise", "nurturing"],
                min_total_skill_level=6.5
            ),
            
            SpecializationType.LEADER: SpecializationRequirements(
                required_skills={"leadership": 3.0, "negotiation": 2.0, "teaching": 1.5},
                required_traits=["charismatic", "ambitious", "confident", "diplomatic"],
                min_total_skill_level=8.0
            ),
            
            SpecializationType.GUARDIAN: SpecializationRequirements(
                required_skills={"athletics": 2.5, "stealth": 2.0, "leadership": 1.5},
                required_traits=["brave", "strong", "protective", "loyal"],
                min_total_skill_level=7.0
            ),
            
            SpecializationType.EXPLORER: SpecializationRequirements(
                required_skills={"athletics": 2.0, "foraging": 2.0, "stealth": 1.5},
                required_traits=["adventurous", "curious", "brave", "independent"],
                min_total_skill_level=6.5
            ),
            
            SpecializationType.MERCHANT: SpecializationRequirements(
                required_skills={"negotiation": 2.5, "leadership": 1.5, "research": 1.5},
                required_traits=["charismatic", "ambitious", "clever", "social"],
                min_total_skill_level=6.5
            ),
            
            SpecializationType.MYSTIC: SpecializationRequirements(
                required_skills={"meditation": 2.5, "inspiration": 2.0, "storytelling": 1.5},
                required_traits=["wise", "spiritual", "empathetic", "intuitive"],
                min_total_skill_level=7.0
            )
        }
    
    def evaluate_specialization_potential(self, agent, skill_system) -> List[Tuple[SpecializationType, float]]:
        """Evaluate which specializations an agent could potentially develop."""
        potentials = []
        
        for spec_type, requirements in self.specialization_requirements.items():
            eligible, issues = requirements.check_eligibility(agent, skill_system)
            
            if eligible:
                # Calculate suitability score
                score = 0.0
                
                # Skill level contribution
                total_skill = sum(agent.advanced_skills[skill].get_effective_level() 
                                for skill in requirements.required_skills.keys() 
                                if skill in agent.advanced_skills)
                score += total_skill / requirements.min_total_skill_level
                
                # Trait match contribution
                matching_traits = sum(1 for trait in requirements.required_traits 
                                    if trait in agent.traits)
                score += matching_traits / len(requirements.required_traits)
                
                # Personality alignment
                score *= random.uniform(0.8, 1.2)  # Add some variability
                
                potentials.append((spec_type, score))
        
        return sorted(potentials, key=lambda x: x[1], reverse=True)
    
    def attempt_specialization(self, agent, spec_type: SpecializationType, 
                             skill_system, current_day: int) -> Dict[str, Any]:
        """Attempt to establish a specialization for an agent."""
        requirements = self.specialization_requirements[spec_type]
        eligible, issues = requirements.check_eligibility(agent, skill_system)
        
        result = {
            "agent": agent.name,
            "specialization_type": spec_type.value,
            "success": False,
            "issues": issues
        }
        
        if not eligible:
            result["message"] = f"{agent.name} does not meet requirements for {spec_type.value}"
            return result
        
        # Check if agent already has a specialization
        if hasattr(agent, 'specialization') and agent.specialization:
            result["message"] = f"{agent.name} already specialized as {agent.specialization.type.value}"
            return result
        
        # Success! Establish the specialization
        specialization = Specialization(
            type=spec_type,
            level=1.0,
            experience=0.0,
            reputation=0.5,
            established_day=current_day
        )
        
        agent.specialization = specialization
        
        # Assign initial responsibilities
        self._assign_initial_responsibilities(agent, specialization)
        
        # Add to community tracking
        if spec_type not in self.community_roles:
            self.community_roles[spec_type] = []
        self.community_roles[spec_type].append(agent.name)
        
        # Create memory
        title = specialization.get_title()
        agent.add_memory(
            f"Became a {title}, taking on the role of {spec_type.value} in the community",
            importance=0.9
        )
        
        result.update({
            "success": True,
            "title": title,
            "message": f"{agent.name} became a {title}!",
            "responsibilities": list(specialization.responsibilities)
        })
        
        return result
    
    def _assign_initial_responsibilities(self, agent, specialization: Specialization):
        """Assign initial responsibilities based on specialization type."""
        responsibilities_map = {
            SpecializationType.ARTISAN: ["craft_tools", "build_structures", "create_art"],
            SpecializationType.SCHOLAR: ["research_topics", "teach_others", "preserve_knowledge"],
            SpecializationType.HEALER: ["treat_illness", "prepare_medicines", "health_advice"],
            SpecializationType.LEADER: ["organize_community", "resolve_disputes", "make_decisions"],
            SpecializationType.GUARDIAN: ["protect_community", "scout_threats", "train_defense"],
            SpecializationType.EXPLORER: ["scout_territory", "find_resources", "map_areas"],
            SpecializationType.MERCHANT: ["organize_trade", "manage_resources", "negotiate_deals"],
            SpecializationType.MYSTIC: ["spiritual_guidance", "interpret_signs", "perform_rituals"]
        }
        
        specialization.responsibilities.update(responsibilities_map[specialization.type])
    
    def process_specialization_activities(self, agents: List, current_day: int) -> List[Dict[str, Any]]:
        """Process daily activities for specialized agents."""
        specialization_events = []
        
        for agent in agents:
            if not agent.is_alive or not hasattr(agent, 'specialization') or not agent.specialization:
                continue
            
            spec = agent.specialization
            
            # 40% chance per day for specialized activity
            if random.random() < 0.4:
                activity = self._perform_specialized_activity(agent, spec, current_day)
                if activity:
                    specialization_events.append(activity)
            
            # Check for advancement opportunities (10% chance)
            if random.random() < 0.1:
                advancement = self._check_advancement(agent, spec, current_day)
                if advancement:
                    specialization_events.append(advancement)
            
            # Check for mentorship opportunities (15% chance)
            if random.random() < 0.15:
                mentorship = self._check_mentorship_opportunity(agent, spec, agents, current_day)
                if mentorship:
                    specialization_events.append(mentorship)
        
        return specialization_events
    
    def _perform_specialized_activity(self, agent, specialization: Specialization, 
                                    current_day: int) -> Optional[Dict[str, Any]]:
        """Perform a specialized activity based on agent's role."""
        activities_map = {
            SpecializationType.ARTISAN: [
                "crafted an intricate tool for the community",
                "improved the construction of a community building",
                "created a beautiful artwork that inspires others"
            ],
            SpecializationType.SCHOLAR: [
                "conducted research on local phenomena",
                "taught important skills to community members",
                "preserved important cultural knowledge"
            ],
            SpecializationType.HEALER: [
                "treated several community members for ailments",
                "discovered new medicinal properties of local plants",
                "provided wellness guidance to maintain health"
            ],
            SpecializationType.LEADER: [
                "organized a successful community project",
                "mediated a complex dispute between residents",
                "made important decisions for community welfare"
            ],
            SpecializationType.GUARDIAN: [
                "patrolled the community perimeter for threats",
                "trained others in defensive techniques",
                "ensured the safety of community gatherings"
            ],
            SpecializationType.EXPLORER: [
                "discovered new territory with valuable resources",
                "mapped previously unknown areas",
                "found a safe route to distant locations"
            ],
            SpecializationType.MERCHANT: [
                "organized beneficial trades with neighboring groups",
                "efficiently distributed community resources",
                "negotiated advantageous deals for everyone"
            ],
            SpecializationType.MYSTIC: [
                "provided spiritual guidance during difficult times",
                "interpreted signs and omens for the community",
                "led meaningful rituals that brought people together"
            ]
        }
        
        activity_descriptions = activities_map[specialization.type]
        description = random.choice(activity_descriptions)
        
        # Calculate success based on specialization level
        success_rate = 0.5 + (specialization.level / 10.0) + (specialization.reputation / 5.0)
        success = random.random() < success_rate
        
        if success:
            # Grant experience and possibly reputation
            exp_gain = random.uniform(10, 25)
            rep_gain = random.uniform(0.01, 0.05)
            
            leveled_up = specialization.advance_experience(exp_gain, current_day)
            specialization.gain_reputation(rep_gain)
            
            # Add to agent's memory
            agent.add_memory(f"Successfully {description}", importance=0.7)
            
            result = {
                "agent": agent.name,
                "activity": "specialized_activity",
                "description": f"{agent.name} {description}",
                "success": True,
                "experience_gained": exp_gain,
                "reputation_gained": rep_gain,
                "specialization_type": specialization.type.value
            }
            
            if leveled_up:
                new_title = specialization.get_title()
                result["level_up"] = {
                    "new_level": specialization.level,
                    "new_title": new_title
                }
                agent.add_memory(f"Advanced to {new_title}!", importance=0.9)
            
            return result
        else:
            # Minor failure
            agent.add_memory(f"Attempted to {description} but encountered difficulties", importance=0.3)
            return {
                "agent": agent.name,
                "activity": "specialized_activity",
                "description": f"{agent.name} attempted to {description} but encountered difficulties",
                "success": False,
                "specialization_type": specialization.type.value
            }
    
    def _check_advancement(self, agent, specialization: Specialization, 
                          current_day: int) -> Optional[Dict[str, Any]]:
        """Check for major advancement opportunities."""
        if specialization.level >= 4.5:  # Already at highest practical level
            return None
        
        # Major advancement requires high reputation and experience
        if specialization.reputation < 0.7 or specialization.experience < specialization.level * 150:
            return None
        
        advancement_opportunities = {
            SpecializationType.ARTISAN: "master a revolutionary crafting technique",
            SpecializationType.SCHOLAR: "make a significant intellectual discovery",
            SpecializationType.HEALER: "develop a powerful new treatment method",
            SpecializationType.LEADER: "successfully guide the community through a major challenge",
            SpecializationType.GUARDIAN: "demonstrate exceptional protective abilities",
            SpecializationType.EXPLORER: "discover something truly remarkable",
            SpecializationType.MERCHANT: "establish transformative trade relationships",
            SpecializationType.MYSTIC: "achieve a profound spiritual breakthrough"
        }
        
        opportunity = advancement_opportunities[specialization.type]
        success_rate = specialization.reputation * 0.8  # High reputation needed
        
        if random.random() < success_rate:
            # Major advancement
            old_level = specialization.level
            specialization.level = min(5.0, specialization.level + 0.5)
            specialization.gain_reputation(0.1)
            
            if specialization.type.value not in specialization.innovations:
                specialization.innovations.append(opportunity)
            
            new_title = specialization.get_title()
            agent.add_memory(f"Achieved a major breakthrough and became a {new_title}!", importance=1.0)
            
            return {
                "agent": agent.name,
                "activity": "major_advancement",
                "description": f"{agent.name} achieved a breakthrough: {opportunity}",
                "success": True,
                "old_level": old_level,
                "new_level": specialization.level,
                "new_title": new_title,
                "specialization_type": specialization.type.value
            }
        
        return None
    
    def _check_mentorship_opportunity(self, agent, specialization: Specialization, 
                                    all_agents: List, current_day: int) -> Optional[Dict[str, Any]]:
        """Check for opportunities to mentor other agents."""
        if specialization.level < 2.0:  # Need to be experienced enough to mentor
            return None
        
        # Find potential apprentices
        potential_apprentices = []
        for other_agent in all_agents:
            if (other_agent.is_alive and other_agent != agent and 
                (not hasattr(other_agent, 'specialization') or not other_agent.specialization)):
                
                # Check if they have potential for this specialization
                requirements = self.specialization_requirements[specialization.type]
                if hasattr(other_agent, 'advanced_skills'):
                    skill_match = any(other_agent.advanced_skills.get(skill, type('', (), {'get_effective_level': lambda: 0})).get_effective_level() > 1.0 
                                    for skill in requirements.required_skills)
                    trait_match = any(trait in other_agent.traits for trait in requirements.required_traits)
                    
                    if skill_match or trait_match:
                        potential_apprentices.append(other_agent)
        
        if not potential_apprentices:
            return None
        
        apprentice = random.choice(potential_apprentices)
        
        # Attempt mentorship
        success_rate = 0.6 + (specialization.level / 10.0)
        if random.random() < success_rate:
            specialization.apprentices.append(apprentice.name)
            specialization.gain_reputation(0.03)
            
            agent.add_memory(f"Began mentoring {apprentice.name} in {specialization.type.value}", importance=0.6)
            apprentice.add_memory(f"Began learning {specialization.type.value} from master {agent.name}", importance=0.7)
            
            return {
                "agent": agent.name,
                "activity": "mentorship",
                "description": f"{agent.name} began mentoring {apprentice.name} in {specialization.type.value}",
                "success": True,
                "apprentice": apprentice.name,
                "specialization_type": specialization.type.value
            }
        
        return None
    
    def get_community_specialization_summary(self, agents: List) -> Dict[str, Any]:
        """Get a summary of all specializations in the community."""
        summary = {
            "total_specialists": 0,
            "specializations_by_type": {},
            "masters": [],
            "recent_advancements": []
        }
        
        for agent in agents:
            if (agent.is_alive and hasattr(agent, 'specialization') and agent.specialization):
                spec = agent.specialization
                summary["total_specialists"] += 1
                
                spec_type = spec.type.value
                if spec_type not in summary["specializations_by_type"]:
                    summary["specializations_by_type"][spec_type] = []
                
                summary["specializations_by_type"][spec_type].append({
                    "name": agent.name,
                    "level": spec.level,
                    "title": spec.get_title(),
                    "reputation": round(spec.reputation, 2)
                })
                
                # Track masters (level 4+)
                if spec.level >= 4.0:
                    summary["masters"].append({
                        "name": agent.name,
                        "specialization": spec_type,
                        "title": spec.get_title(),
                        "innovations": spec.innovations
                    })
        
        return summary 