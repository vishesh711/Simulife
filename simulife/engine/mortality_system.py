"""
Mortality and Aging System for SimuLife
Handles death, aging, natural lifecycle progression, and mortality statistics.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class DeathCause(Enum):
    """Possible causes of death in SimuLife."""
    OLD_AGE = "old_age"
    DISEASE = "disease"
    ACCIDENT = "accident"
    VIOLENCE = "violence"
    STARVATION = "starvation"
    EXPOSURE = "exposure"
    CHILDBIRTH = "childbirth"
    GENETIC_CONDITION = "genetic_condition"


class LifeStage(Enum):
    """Life stages for agents."""
    INFANT = "infant"          # 0-2 years
    CHILD = "child"            # 3-12 years
    ADOLESCENT = "adolescent"  # 13-17 years
    YOUNG_ADULT = "young_adult" # 18-30 years
    ADULT = "adult"            # 31-50 years
    MIDDLE_AGED = "middle_aged" # 51-65 years
    ELDER = "elder"            # 66-80 years
    ANCIENT = "ancient"        # 81+ years


@dataclass
class DeathRecord:
    """Record of an agent's death."""
    agent_id: str
    agent_name: str
    age_at_death: int
    death_day: int
    cause_of_death: DeathCause
    circumstances: str
    family_members: List[str]
    achievements: List[str]
    legacy_score: float


@dataclass
class AgingEffect:
    """Effects of aging on agent capabilities."""
    age_threshold: int
    health_impact: float       # Negative impact on health
    energy_impact: float       # Impact on energy levels
    skill_decay_rate: float    # Rate of skill decay
    memory_impact: float       # Impact on memory formation
    social_impact: float       # Impact on social interactions
    reproduction_impact: float # Impact on reproduction capability


class MortalitySystem:
    """
    Manages aging, death, and natural lifecycle progression for agents.
    """
    
    def __init__(self):
        self.death_records: List[DeathRecord] = []
        self.aging_effects = self._initialize_aging_effects()
        self.mortality_stats = {
            "total_deaths": 0,
            "deaths_by_cause": {cause.value: 0 for cause in DeathCause},
            "deaths_by_age_group": {},
            "average_lifespan": 0,
            "infant_mortality": 0,
            "elder_survival": 0
        }
        
        # Mortality configuration
        self.base_mortality_rates = self._initialize_mortality_rates()
        self.aging_progression = self._initialize_aging_progression()
    
    def _initialize_aging_effects(self) -> Dict[LifeStage, AgingEffect]:
        """Initialize aging effects for different life stages."""
        return {
            LifeStage.INFANT: AgingEffect(
                age_threshold=0,
                health_impact=0.0,
                energy_impact=0.1,
                skill_decay_rate=0.0,
                memory_impact=0.2,
                social_impact=0.3,
                reproduction_impact=1.0  # Cannot reproduce
            ),
            LifeStage.CHILD: AgingEffect(
                age_threshold=3,
                health_impact=0.0,
                energy_impact=-0.1,    # Higher energy
                skill_decay_rate=0.0,
                memory_impact=0.0,     # Good memory formation
                social_impact=0.1,
                reproduction_impact=1.0  # Cannot reproduce
            ),
            LifeStage.ADOLESCENT: AgingEffect(
                age_threshold=13,
                health_impact=0.0,
                energy_impact=-0.05,
                skill_decay_rate=0.0,
                memory_impact=0.0,
                social_impact=0.0,
                reproduction_impact=0.3  # Limited reproduction
            ),
            LifeStage.YOUNG_ADULT: AgingEffect(
                age_threshold=18,
                health_impact=0.0,
                energy_impact=0.0,
                skill_decay_rate=0.0,
                memory_impact=0.0,
                social_impact=0.0,
                reproduction_impact=0.0  # Peak reproduction
            ),
            LifeStage.ADULT: AgingEffect(
                age_threshold=31,
                health_impact=0.01,
                energy_impact=0.01,
                skill_decay_rate=0.001,
                memory_impact=0.01,
                social_impact=0.0,
                reproduction_impact=0.1
            ),
            LifeStage.MIDDLE_AGED: AgingEffect(
                age_threshold=51,
                health_impact=0.02,
                energy_impact=0.02,
                skill_decay_rate=0.002,
                memory_impact=0.02,
                social_impact=0.01,
                reproduction_impact=0.5
            ),
            LifeStage.ELDER: AgingEffect(
                age_threshold=66,
                health_impact=0.04,
                energy_impact=0.03,
                skill_decay_rate=0.004,
                memory_impact=0.03,
                social_impact=0.02,
                reproduction_impact=0.9
            ),
            LifeStage.ANCIENT: AgingEffect(
                age_threshold=81,
                health_impact=0.08,
                energy_impact=0.06,
                skill_decay_rate=0.008,
                memory_impact=0.05,
                social_impact=0.03,
                reproduction_impact=1.0  # Cannot reproduce
            )
        }
    
    def _initialize_mortality_rates(self) -> Dict[LifeStage, float]:
        """Initialize base mortality rates for different life stages (per day)."""
        return {
            LifeStage.INFANT: 0.001,      # High infant mortality
            LifeStage.CHILD: 0.0001,      # Very low child mortality
            LifeStage.ADOLESCENT: 0.0002, # Low adolescent mortality
            LifeStage.YOUNG_ADULT: 0.0003, # Low young adult mortality
            LifeStage.ADULT: 0.0005,      # Moderate adult mortality
            LifeStage.MIDDLE_AGED: 0.001, # Increasing mortality
            LifeStage.ELDER: 0.003,       # Higher elder mortality
            LifeStage.ANCIENT: 0.008      # High ancient mortality
        }
    
    def _initialize_aging_progression(self) -> Dict[str, Dict[str, Any]]:
        """Initialize aging progression effects."""
        return {
            "health_decline": {
                "start_age": 40,
                "rate": 0.001,  # Health decline per day after start_age
                "acceleration": 1.1  # Acceleration factor with age
            },
            "energy_decline": {
                "start_age": 35,
                "rate": 0.0008,
                "acceleration": 1.05
            },
            "skill_decay": {
                "start_age": 60,
                "rate": 0.0001,
                "acceleration": 1.2
            },
            "memory_decline": {
                "start_age": 55,
                "rate": 0.0005,
                "acceleration": 1.15
            }
        }
    
    def get_life_stage(self, age: int) -> LifeStage:
        """Determine life stage based on age."""
        if age < 3:
            return LifeStage.INFANT
        elif age < 13:
            return LifeStage.CHILD
        elif age < 18:
            return LifeStage.ADOLESCENT
        elif age < 31:
            return LifeStage.YOUNG_ADULT
        elif age < 51:
            return LifeStage.ADULT
        elif age < 66:
            return LifeStage.MIDDLE_AGED
        elif age < 81:
            return LifeStage.ELDER
        else:
            return LifeStage.ANCIENT
    
    def process_daily_aging(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process aging effects and mortality for all agents."""
        aging_events = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            # Age the agent
            agent.age = (current_day - agent.birth_day) // 365
            life_stage = self.get_life_stage(agent.age)
            
            # Apply aging effects
            aging_applied = self._apply_aging_effects(agent, life_stage, current_day)
            if aging_applied:
                aging_events.append(aging_applied)
            
            # Check for death
            death_event = self._check_mortality(agent, life_stage, current_day)
            if death_event:
                aging_events.append(death_event)
                self._process_death(agent, death_event, current_day)
        
        return aging_events
    
    def _apply_aging_effects(self, agent: Any, life_stage: LifeStage, current_day: int) -> Optional[Dict[str, Any]]:
        """Apply aging effects to an agent."""
        aging_effect = self.aging_effects[life_stage]
        effects_applied = []
        
        # Health effects
        if aging_effect.health_impact > 0:
            health_decline = aging_effect.health_impact * random.uniform(0.5, 1.5)
            agent.health = max(0.0, agent.health - health_decline)
            if health_decline > 0.01:  # Significant decline
                effects_applied.append(f"health decline (-{health_decline:.3f})")
        
        # Energy effects
        if aging_effect.energy_impact != 0:
            energy_change = aging_effect.energy_impact * random.uniform(0.5, 1.5)
            agent.energy = max(0.0, min(1.0, agent.energy - energy_change))
            if abs(energy_change) > 0.01:
                effects_applied.append(f"energy change ({energy_change:+.3f})")
        
        # Skill decay for older agents
        if aging_effect.skill_decay_rate > 0 and hasattr(agent, 'skills'):
            for skill_name, skill_value in agent.skills.items():
                if isinstance(skill_value, float):
                    decay = aging_effect.skill_decay_rate * random.uniform(0.5, 1.5)
                    agent.skills[skill_name] = max(0.0, skill_value - decay)
                    if decay > 0.002:
                        effects_applied.append(f"{skill_name} skill decay")
        
        # Memory impact (affects memory importance threshold)
        if aging_effect.memory_impact > 0:
            # This would affect how memories are stored/retrieved
            # Implementation depends on memory system details
            pass
        
        # Check for life stage transitions
        previous_stage = getattr(agent, '_life_stage', None)
        if previous_stage != life_stage:
            agent._life_stage = life_stage
            effects_applied.append(f"life stage transition to {life_stage.value}")
        
        if effects_applied:
            return {
                "type": "aging_effects",
                "agent": agent.name,
                "age": agent.age,
                "life_stage": life_stage.value,
                "effects": effects_applied,
                "day": current_day
            }
        
        return None
    
    def _check_mortality(self, agent: Any, life_stage: LifeStage, current_day: int) -> Optional[Dict[str, Any]]:
        """Check if an agent dies this day."""
        base_mortality = self.base_mortality_rates[life_stage]
        
        # Modify mortality based on health
        health_modifier = 1.0
        if agent.health < 0.3:
            health_modifier = 3.0  # Higher chance of death when unhealthy
        elif agent.health < 0.5:
            health_modifier = 2.0
        elif agent.health > 0.8:
            health_modifier = 0.7  # Lower chance when very healthy
        
        # Modify based on life satisfaction and social connections
        satisfaction_modifier = 1.0
        if hasattr(agent, 'life_satisfaction'):
            if agent.life_satisfaction < 0.3:
                satisfaction_modifier = 1.5  # Depression increases mortality
            elif agent.life_satisfaction > 0.8:
                satisfaction_modifier = 0.8  # Happiness decreases mortality
        
        # Social connections protect against mortality
        social_modifier = 1.0
        if hasattr(agent, 'relationships'):
            num_relationships = len([r for r in agent.relationships.values() 
                                   if r in ["friend", "family", "spouse", "partner"]])
            if num_relationships == 0:
                social_modifier = 1.4  # Loneliness increases mortality
            elif num_relationships >= 3:
                social_modifier = 0.8  # Social connections decrease mortality
        
        # Calculate final mortality chance
        final_mortality = base_mortality * health_modifier * satisfaction_modifier * social_modifier
        
        # Add random events
        if random.random() < 0.001:  # 0.1% chance of random death events
            final_mortality *= 10  # Accidents, disasters, etc.
        
        if random.random() < final_mortality:
            # Agent dies - determine cause
            cause = self._determine_death_cause(agent, life_stage)
            circumstances = self._generate_death_circumstances(agent, cause, life_stage)
            
            return {
                "type": "death",
                "agent": agent.name,
                "age": agent.age,
                "cause": cause.value,
                "circumstances": circumstances,
                "day": current_day,
                "life_stage": life_stage.value
            }
        
        return None
    
    def _determine_death_cause(self, agent: Any, life_stage: LifeStage) -> DeathCause:
        """Determine the cause of death based on agent and life stage."""
        # Age-based death cause probabilities
        if life_stage == LifeStage.INFANT:
            return random.choices([DeathCause.DISEASE, DeathCause.GENETIC_CONDITION, DeathCause.ACCIDENT],
                                weights=[0.5, 0.3, 0.2])[0]
        elif life_stage in [LifeStage.CHILD, LifeStage.ADOLESCENT]:
            return random.choices([DeathCause.ACCIDENT, DeathCause.DISEASE, DeathCause.VIOLENCE],
                                weights=[0.5, 0.3, 0.2])[0]
        elif life_stage in [LifeStage.YOUNG_ADULT, LifeStage.ADULT]:
            # Check for childbirth deaths (if recently gave birth)
            if hasattr(agent, 'family') and random.random() < 0.1:
                return DeathCause.CHILDBIRTH
            return random.choices([DeathCause.ACCIDENT, DeathCause.DISEASE, DeathCause.VIOLENCE],
                                weights=[0.4, 0.4, 0.2])[0]
        elif life_stage == LifeStage.MIDDLE_AGED:
            return random.choices([DeathCause.DISEASE, DeathCause.ACCIDENT, DeathCause.OLD_AGE],
                                weights=[0.6, 0.3, 0.1])[0]
        else:  # Elder, Ancient
            return random.choices([DeathCause.OLD_AGE, DeathCause.DISEASE, DeathCause.ACCIDENT],
                                weights=[0.7, 0.2, 0.1])[0]
    
    def _generate_death_circumstances(self, agent: Any, cause: DeathCause, life_stage: LifeStage) -> str:
        """Generate narrative description of death circumstances."""
        circumstances_by_cause = {
            DeathCause.OLD_AGE: [
                "passed away peacefully in their sleep",
                "died surrounded by family after a long life",
                "succumbed to the natural effects of advanced age",
                "passed away quietly after growing weak with age"
            ],
            DeathCause.DISEASE: [
                "fell ill with a mysterious illness and did not recover",
                "was struck down by a sudden sickness",
                "died after a prolonged battle with illness",
                "succumbed to a disease that spread through the community"
            ],
            DeathCause.ACCIDENT: [
                "died in an unfortunate accident",
                "was killed in a tragic mishap while working",
                "fell and sustained fatal injuries",
                "died from injuries sustained during travel"
            ],
            DeathCause.VIOLENCE: [
                "was killed during a conflict",
                "died defending others from danger",
                "was murdered by an unknown assailant",
                "died in violence that erupted in the community"
            ],
            DeathCause.STARVATION: [
                "died from lack of food during times of scarcity",
                "starved when resources became critically low",
                "perished due to malnutrition and hunger"
            ],
            DeathCause.EXPOSURE: [
                "died from exposure to harsh weather conditions",
                "perished in the cold without adequate shelter",
                "was caught in a storm and did not survive"
            ],
            DeathCause.CHILDBIRTH: [
                "died during childbirth complications",
                "passed away giving life to their child",
                "died from complications following the birth of their child"
            ],
            DeathCause.GENETIC_CONDITION: [
                "died from a hereditary condition that manifested early",
                "succumbed to a genetic illness that ran in the family",
                "was born with a condition that proved fatal"
            ]
        }
        
        possible_circumstances = circumstances_by_cause.get(cause, ["died under unknown circumstances"])
        return random.choice(possible_circumstances)
    
    def _process_death(self, agent: Any, death_event: Dict[str, Any], current_day: int):
        """Process the death of an agent and create death record."""
        # Mark agent as dead
        agent.is_alive = False
        
        # Create death record
        death_record = DeathRecord(
            agent_id=agent.id,
            agent_name=agent.name,
            age_at_death=agent.age,
            death_day=current_day,
            cause_of_death=DeathCause(death_event["cause"]),
            circumstances=death_event["circumstances"],
            family_members=list(agent.family.get("children", [])) + list(agent.family.get("parents", [])),
            achievements=self._compile_agent_achievements(agent),
            legacy_score=self._calculate_legacy_score(agent)
        )
        
        self.death_records.append(death_record)
        
        # Update mortality statistics
        self._update_mortality_stats(death_record)
        
        # Notify family and friends
        self._notify_death_to_relationships(agent, death_event, current_day)
    
    def _compile_agent_achievements(self, agent: Any) -> List[str]:
        """Compile list of significant achievements for deceased agent."""
        achievements = []
        
        # Family achievements
        if hasattr(agent, 'family'):
            children = agent.family.get("children", [])
            if children:
                achievements.append(f"Parent to {len(children)} children")
        
        # Social achievements
        if hasattr(agent, 'relationships'):
            num_friends = len([r for r in agent.relationships.values() if r == "friend"])
            if num_friends >= 5:
                achievements.append("Had many friends in the community")
        
        # Skill achievements
        if hasattr(agent, 'skills'):
            high_skills = [name for name, value in agent.skills.items() 
                          if (isinstance(value, float) and value > 0.8)]
            if high_skills:
                achievements.append(f"Master of {', '.join(high_skills[:3])}")
        
        # Leadership achievements
        if hasattr(agent, 'reputation') and agent.reputation > 0.8:
            achievements.append("Respected leader in the community")
        
        # Longevity achievement
        if agent.age >= 80:
            achievements.append("Lived to an advanced age")
        
        return achievements[:5]  # Limit to 5 achievements
    
    def _calculate_legacy_score(self, agent: Any) -> float:
        """Calculate legacy score for deceased agent."""
        score = 0.0
        
        # Age factor (living longer = higher legacy)
        score += min(agent.age / 80.0, 1.0) * 0.3
        
        # Family factor
        if hasattr(agent, 'family'):
            children = len(agent.family.get("children", []))
            score += min(children / 5.0, 1.0) * 0.2
        
        # Social factor
        if hasattr(agent, 'relationships'):
            relationships = len(agent.relationships)
            score += min(relationships / 10.0, 1.0) * 0.2
        
        # Achievement factor
        if hasattr(agent, 'reputation'):
            score += agent.reputation * 0.2
        
        # Skills factor
        if hasattr(agent, 'skills'):
            avg_skill = sum(v for v in agent.skills.values() if isinstance(v, float)) / max(len(agent.skills), 1)
            score += avg_skill * 0.1
        
        return min(score, 1.0)
    
    def _update_mortality_stats(self, death_record: DeathRecord):
        """Update mortality statistics with new death."""
        self.mortality_stats["total_deaths"] += 1
        self.mortality_stats["deaths_by_cause"][death_record.cause_of_death.value] += 1
        
        # Age group statistics
        age_group = "child" if death_record.age_at_death < 18 else "adult" if death_record.age_at_death < 65 else "elder"
        if age_group not in self.mortality_stats["deaths_by_age_group"]:
            self.mortality_stats["deaths_by_age_group"][age_group] = 0
        self.mortality_stats["deaths_by_age_group"][age_group] += 1
        
        # Update average lifespan
        total_lifespan = sum(record.age_at_death for record in self.death_records)
        self.mortality_stats["average_lifespan"] = total_lifespan / len(self.death_records)
        
        # Infant mortality rate
        infant_deaths = len([r for r in self.death_records if r.age_at_death < 1])
        total_births = len(self.death_records)  # Simplified - would need birth tracking
        if total_births > 0:
            self.mortality_stats["infant_mortality"] = infant_deaths / total_births
    
    def _notify_death_to_relationships(self, deceased_agent: Any, death_event: Dict[str, Any], current_day: int):
        """Notify family and friends about the death."""
        # This would integrate with the memory system to add grief memories
        # and potentially trigger grief reactions in related agents
        pass
    
    def get_mortality_statistics(self) -> Dict[str, Any]:
        """Get comprehensive mortality statistics."""
        return {
            "total_deaths": len(self.death_records),
            "deaths_by_cause": self.mortality_stats["deaths_by_cause"],
            "deaths_by_age_group": self.mortality_stats["deaths_by_age_group"],
            "average_lifespan": self.mortality_stats["average_lifespan"],
            "recent_deaths": [asdict(record) for record in self.death_records[-5:]],
            "notable_deaths": [asdict(record) for record in self.death_records 
                             if record.legacy_score > 0.7],
            "population_health": self._analyze_population_health()
        }
    
    def _analyze_population_health(self) -> Dict[str, Any]:
        """Analyze overall population health trends."""
        if not self.death_records:
            return {"status": "insufficient_data"}
        
        recent_deaths = [r for r in self.death_records if r.death_day > (max(r.death_day for r in self.death_records) - 365)]
        
        analysis = {
            "recent_mortality_trend": len(recent_deaths),
            "leading_cause_of_death": max(self.mortality_stats["deaths_by_cause"], 
                                        key=self.mortality_stats["deaths_by_cause"].get),
            "demographic_risk": "high" if len([r for r in recent_deaths if r.age_at_death < 50]) > len(recent_deaths) * 0.5 else "normal"
        }
        
        return analysis
    
    def generate_memorial_events(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Generate memorial events for recently deceased agents."""
        memorial_events = []
        
        # Check for recent deaths that warrant memorials
        recent_deaths = [r for r in self.death_records 
                        if current_day - r.death_day <= 7 and r.legacy_score > 0.5]
        
        for death_record in recent_deaths:
            if random.random() < 0.6:  # 60% chance of memorial
                memorial_events.append({
                    "type": "memorial",
                    "deceased": death_record.agent_name,
                    "age_at_death": death_record.age_at_death,
                    "legacy_score": death_record.legacy_score,
                    "achievements": death_record.achievements,
                    "attendees": death_record.family_members,
                    "day": current_day
                })
        
        return memorial_events 