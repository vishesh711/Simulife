"""
Skill Development System for SimuLife
Manages agent skill progression, specialization, and skill-based activities.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class SkillCategory(Enum):
    """Categories of skills that agents can develop."""
    SOCIAL = "social"           # Communication, leadership, negotiation
    CRAFTING = "crafting"       # Building, tool-making, artistry
    SURVIVAL = "survival"       # Hunting, foraging, medicine
    INTELLECTUAL = "intellectual"  # Research, teaching, innovation
    PHYSICAL = "physical"       # Athletics, combat, endurance
    SPIRITUAL = "spiritual"     # Meditation, healing, wisdom


@dataclass
class Skill:
    """Represents a specific skill with progression tracking."""
    name: str
    category: SkillCategory
    level: float = 0.0          # 0.0 to 10.0 scale
    experience: float = 0.0     # Total experience points
    last_practiced: int = 0     # Day last practiced
    natural_aptitude: float = 1.0  # Multiplier based on personality
    specialization_bonus: float = 0.0  # Bonus from specialization
    
    def get_effective_level(self) -> float:
        """Get skill level with all bonuses applied."""
        return min(10.0, self.level * self.natural_aptitude + self.specialization_bonus)
    
    def practice(self, experience_gained: float, current_day: int):
        """Add experience and potentially level up the skill."""
        self.experience += experience_gained * self.natural_aptitude
        self.last_practiced = current_day
        
        # Level progression follows diminishing returns
        new_level = (self.experience / 100.0) ** 0.7
        if new_level > self.level:
            self.level = min(10.0, new_level)
    
    def decay(self, current_day: int, decay_rate: float = 0.001):
        """Skills decay slowly if not practiced."""
        days_since_practice = current_day - self.last_practiced
        if days_since_practice > 30:  # Only decay after a month of no practice
            decay_amount = (days_since_practice - 30) * decay_rate
            self.level = max(0.0, self.level - decay_amount)


@dataclass 
class SkillTemplate:
    """Template for skill activities and requirements."""
    name: str
    category: SkillCategory
    required_skills: Dict[str, float]  # Minimum skill levels needed
    experience_reward: float
    success_rate_base: float = 0.5
    description: str = ""
    
    def can_attempt(self, agent_skills: Dict[str, Skill]) -> bool:
        """Check if agent has required skills to attempt this activity."""
        for skill_name, min_level in self.required_skills.items():
            if skill_name not in agent_skills:
                return False
            if agent_skills[skill_name].get_effective_level() < min_level:
                return False
        return True
    
    def calculate_success_rate(self, agent_skills: Dict[str, Skill]) -> float:
        """Calculate success probability based on agent's skill levels."""
        if not self.can_attempt(agent_skills):
            return 0.0
        
        # Base success rate plus bonuses from skill levels
        success_rate = self.success_rate_base
        for skill_name, min_level in self.required_skills.items():
            skill_level = agent_skills[skill_name].get_effective_level()
            bonus = (skill_level - min_level) * 0.05  # 5% per level above minimum
            success_rate += bonus
            
        return min(0.95, max(0.05, success_rate))


class SkillSystem:
    """
    Manages skill development, practice activities, and specialization.
    """
    
    def __init__(self):
        self.skill_templates = self._initialize_skill_templates()
        self.skill_activities = self._initialize_skill_activities()
        
    def _initialize_skill_templates(self) -> Dict[str, Dict]:
        """Initialize base skill definitions."""
        return {
            # Social Skills
            "leadership": {
                "category": SkillCategory.SOCIAL,
                "description": "Ability to guide and inspire others",
                "base_traits": ["ambitious", "charismatic", "confident"]
            },
            "negotiation": {
                "category": SkillCategory.SOCIAL,
                "description": "Skill in resolving conflicts and making deals",
                "base_traits": ["diplomatic", "empathetic", "patient"]
            },
            "teaching": {
                "category": SkillCategory.SOCIAL,
                "description": "Ability to share knowledge effectively",
                "base_traits": ["patient", "wise", "empathetic"]
            },
            
            # Crafting Skills
            "toolmaking": {
                "category": SkillCategory.CRAFTING,
                "description": "Creating and improving tools and equipment",
                "base_traits": ["creative", "patient", "precise"]
            },
            "construction": {
                "category": SkillCategory.CRAFTING,
                "description": "Building shelters and structures",
                "base_traits": ["strong", "patient", "organized"]
            },
            "artistry": {
                "category": SkillCategory.CRAFTING,
                "description": "Creating beautiful and meaningful objects",
                "base_traits": ["creative", "sensitive", "expressive"]
            },
            
            # Survival Skills
            "foraging": {
                "category": SkillCategory.SURVIVAL,
                "description": "Finding food and useful materials in nature",
                "base_traits": ["observant", "patient", "wise"]
            },
            "medicine": {
                "category": SkillCategory.SURVIVAL,
                "description": "Healing and treating injuries and illness",
                "base_traits": ["empathetic", "careful", "wise"]
            },
            "hunting": {
                "category": SkillCategory.SURVIVAL,
                "description": "Tracking and hunting animals for food",
                "base_traits": ["patient", "strong", "focused"]
            },
            
            # Intellectual Skills
            "research": {
                "category": SkillCategory.INTELLECTUAL,
                "description": "Investigating and discovering new knowledge",
                "base_traits": ["curious", "patient", "methodical"]
            },
            "innovation": {
                "category": SkillCategory.INTELLECTUAL,
                "description": "Creating new ideas and solutions",
                "base_traits": ["creative", "intelligent", "bold"]
            },
            "storytelling": {
                "category": SkillCategory.INTELLECTUAL,
                "description": "Preserving and sharing cultural knowledge",
                "base_traits": ["creative", "charismatic", "wise"]
            },
            
            # Physical Skills
            "athletics": {
                "category": SkillCategory.PHYSICAL,
                "description": "Physical strength, speed, and coordination",
                "base_traits": ["strong", "energetic", "competitive"]
            },
            "stealth": {
                "category": SkillCategory.PHYSICAL,
                "description": "Moving quietly and remaining undetected",
                "base_traits": ["careful", "patient", "observant"]
            },
            
            # Spiritual Skills
            "meditation": {
                "category": SkillCategory.SPIRITUAL,
                "description": "Inner peace and mental discipline",
                "base_traits": ["patient", "wise", "calm"]
            },
            "inspiration": {
                "category": SkillCategory.SPIRITUAL,
                "description": "Motivating and uplifting others",
                "base_traits": ["charismatic", "empathetic", "optimistic"]
            }
        }
    
    def _initialize_skill_activities(self) -> List[SkillTemplate]:
        """Initialize activities that can develop skills."""
        return [
            # Social Activities
            SkillTemplate(
                name="organize_community_meeting",
                category=SkillCategory.SOCIAL,
                required_skills={"leadership": 2.0},
                experience_reward=15.0,
                success_rate_base=0.6,
                description="Organize and lead a community gathering"
            ),
            SkillTemplate(
                name="mediate_dispute",
                category=SkillCategory.SOCIAL,
                required_skills={"negotiation": 1.5},
                experience_reward=12.0,
                success_rate_base=0.4,
                description="Help resolve conflicts between others"
            ),
            SkillTemplate(
                name="mentor_younger_agent",
                category=SkillCategory.SOCIAL,
                required_skills={"teaching": 2.0},
                experience_reward=10.0,
                success_rate_base=0.7,
                description="Share knowledge and guide a less experienced agent"
            ),
            
            # Crafting Activities
            SkillTemplate(
                name="craft_advanced_tool",
                category=SkillCategory.CRAFTING,
                required_skills={"toolmaking": 3.0},
                experience_reward=20.0,
                success_rate_base=0.3,
                description="Create a sophisticated tool or implement"
            ),
            SkillTemplate(
                name="build_community_structure",
                category=SkillCategory.CRAFTING,
                required_skills={"construction": 2.5, "leadership": 1.0},
                experience_reward=25.0,
                success_rate_base=0.4,
                description="Lead construction of a building for community use"
            ),
            SkillTemplate(
                name="create_artwork",
                category=SkillCategory.CRAFTING,
                required_skills={"artistry": 1.5},
                experience_reward=8.0,
                success_rate_base=0.8,
                description="Create a beautiful or meaningful artistic piece"
            ),
            
            # Survival Activities
            SkillTemplate(
                name="discover_new_food_source",
                category=SkillCategory.SURVIVAL,
                required_skills={"foraging": 2.0},
                experience_reward=15.0,
                success_rate_base=0.5,
                description="Find new sources of food in the environment"
            ),
            SkillTemplate(
                name="develop_herbal_remedy",
                category=SkillCategory.SURVIVAL,
                required_skills={"medicine": 2.5, "foraging": 1.0},
                experience_reward=18.0,
                success_rate_base=0.3,
                description="Create a new treatment using natural ingredients"
            ),
            
            # Intellectual Activities
            SkillTemplate(
                name="conduct_research_project",
                category=SkillCategory.INTELLECTUAL,
                required_skills={"research": 2.0},
                experience_reward=20.0,
                success_rate_base=0.6,
                description="Investigate a specific topic or phenomenon"
            ),
            SkillTemplate(
                name="invent_new_technique",
                category=SkillCategory.INTELLECTUAL,
                required_skills={"innovation": 3.0},
                experience_reward=25.0,
                success_rate_base=0.2,
                description="Develop a completely new way of doing something"
            ),
            
            # Physical Activities
            SkillTemplate(
                name="athletic_competition",
                category=SkillCategory.PHYSICAL,
                required_skills={"athletics": 1.5},
                experience_reward=8.0,
                success_rate_base=0.7,
                description="Compete in physical challenges with others"
            ),
            
            # Spiritual Activities
            SkillTemplate(
                name="spiritual_guidance_session",
                category=SkillCategory.SPIRITUAL,
                required_skills={"meditation": 2.0, "inspiration": 1.5},
                experience_reward=12.0,
                success_rate_base=0.5,
                description="Guide others in spiritual or mental practices"
            )
        ]
    
    def initialize_agent_skills(self, agent) -> Dict[str, Skill]:
        """Initialize skills for a new agent based on personality."""
        skills = {}
        
        for skill_name, skill_info in self.skill_templates.items():
            # Calculate natural aptitude based on personality traits
            aptitude = 1.0
            matching_traits = 0
            for trait in skill_info["base_traits"]:
                if trait in agent.traits:
                    aptitude += 0.3
                    matching_traits += 1
            
            # Add some randomness
            aptitude += random.uniform(-0.2, 0.2)
            aptitude = max(0.5, min(2.0, aptitude))
            
            # Initialize skill with some base experience if agent has matching traits
            base_experience = matching_traits * 20 + random.uniform(0, 30)
            
            skill = Skill(
                name=skill_name,
                category=skill_info["category"],
                natural_aptitude=aptitude,
                experience=base_experience
            )
            skill.practice(0, 0)  # Calculate initial level
            skills[skill_name] = skill
            
        return skills
    
    def find_suitable_activity(self, agent, current_day: int) -> Optional[SkillTemplate]:
        """Find a skill activity the agent can attempt and would want to do."""
        if not hasattr(agent, 'advanced_skills'):
            return None
            
        available_activities = []
        
        for activity in self.skill_activities:
            if activity.can_attempt(agent.advanced_skills):
                success_rate = activity.calculate_success_rate(agent.advanced_skills)
                # Agents prefer activities they're likely to succeed at
                if success_rate >= 0.2:  # At least 20% chance
                    available_activities.append((activity, success_rate))
        
        if not available_activities:
            return None
        
        # Weighted selection favoring higher success rates
        weights = [rate ** 2 for _, rate in available_activities]  # Square to emphasize higher rates
        total_weight = sum(weights)
        
        if total_weight == 0:
            return None
            
        r = random.uniform(0, total_weight)
        current_weight = 0
        
        for (activity, rate), weight in zip(available_activities, weights):
            current_weight += weight
            if r <= current_weight:
                return activity
        
        return available_activities[0][0]  # Fallback
    
    def attempt_skill_activity(self, agent, activity: SkillTemplate, current_day: int) -> Dict[str, Any]:
        """Agent attempts a skill-based activity."""
        success_rate = activity.calculate_success_rate(agent.advanced_skills)
        success = random.random() < success_rate
        
        result = {
            "activity": activity.name,
            "description": activity.description,
            "success": success,
            "success_rate": success_rate,
            "experience_gained": {},
            "skill_improvements": []
        }
        
        # Grant experience to relevant skills
        experience_multiplier = 1.5 if success else 0.7
        for skill_name in activity.required_skills:
            if skill_name in agent.advanced_skills:
                exp_gained = activity.experience_reward * experience_multiplier
                old_level = agent.advanced_skills[skill_name].level
                
                agent.advanced_skills[skill_name].practice(exp_gained, current_day)
                new_level = agent.advanced_skills[skill_name].level
                
                result["experience_gained"][skill_name] = exp_gained
                
                if new_level > old_level + 0.1:  # Significant improvement
                    result["skill_improvements"].append({
                        "skill": skill_name,
                        "old_level": round(old_level, 1),
                        "new_level": round(new_level, 1)
                    })
        
        # Add to agent's memory
        memory_text = f"Attempted {activity.description}"
        if success:
            memory_text += " and succeeded"
        else:
            memory_text += " but did not succeed as hoped"
            
        if result["skill_improvements"]:
            improvements = ", ".join([f"{imp['skill']} improved to {imp['new_level']}" 
                                    for imp in result["skill_improvements"]])
            memory_text += f". Skills improved: {improvements}"
        
        agent.add_memory(memory_text, importance=0.6 if success else 0.4)
        
        return result
    
    def process_daily_skill_activities(self, agents: List, current_day: int) -> List[Dict[str, Any]]:
        """Process skill development activities for all agents."""
        skill_events = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
                
            # Initialize advanced skills if not present
            if not hasattr(agent, 'advanced_skills'):
                agent.advanced_skills = self.initialize_agent_skills(agent)
            
            # Apply skill decay
            for skill in agent.advanced_skills.values():
                skill.decay(current_day)
            
            # 30% chance per day to attempt a skill activity
            if random.random() < 0.3:
                activity = self.find_suitable_activity(agent, current_day)
                if activity:
                    result = self.attempt_skill_activity(agent, activity, current_day)
                    result["agent"] = agent.name
                    skill_events.append(result)
        
        return skill_events
    
    def get_agent_skill_summary(self, agent) -> Dict[str, Any]:
        """Get a summary of an agent's skills."""
        if not hasattr(agent, 'advanced_skills'):
            return {"total_skills": 0, "specializations": [], "top_skills": []}
        
        skills_by_level = sorted(agent.advanced_skills.items(), 
                               key=lambda x: x[1].get_effective_level(), 
                               reverse=True)
        
        top_skills = [(name, round(skill.get_effective_level(), 1)) 
                     for name, skill in skills_by_level[:5]]
        
        # Identify specializations (skills significantly above average)
        all_levels = [skill.get_effective_level() for skill in agent.advanced_skills.values()]
        avg_level = sum(all_levels) / len(all_levels) if all_levels else 0
        
        specializations = []
        for name, skill in agent.advanced_skills.items():
            if skill.get_effective_level() > avg_level + 1.5:
                specializations.append((name, round(skill.get_effective_level(), 1)))
        
        return {
            "total_skills": len(agent.advanced_skills),
            "average_level": round(avg_level, 1),
            "specializations": specializations,
            "top_skills": top_skills
        } 