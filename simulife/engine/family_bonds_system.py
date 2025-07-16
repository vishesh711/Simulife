"""
Deep Family Bonds System for SimuLife
Enables intense family relationships including parental love, sibling dynamics, 
grandparent wisdom transmission, and unique family traditions that develop over generations.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict


class FamilyRole(Enum):
    """Roles within a family structure."""
    PARENT = "parent"
    CHILD = "child"
    SIBLING = "sibling"
    GRANDPARENT = "grandparent"
    GRANDCHILD = "grandchild"
    UNCLE_AUNT = "uncle_aunt"
    NEPHEW_NIECE = "nephew_niece"
    COUSIN = "cousin"


class BondType(Enum):
    """Types of family bonds."""
    PARENTAL_LOVE = "parental_love"         # Parent to child
    FILIAL_DEVOTION = "filial_devotion"     # Child to parent
    SIBLING_LOYALTY = "sibling_loyalty"     # Between siblings
    SIBLING_RIVALRY = "sibling_rivalry"     # Competitive siblings
    GRANDPARENT_WISDOM = "grandparent_wisdom"  # Elder to grandchild
    PROTECTIVE_INSTINCT = "protective_instinct"  # Protective family member
    FAMILY_PRIDE = "family_pride"           # Pride in family achievements
    GENERATIONAL_TENSION = "generational_tension"  # Cross-generation conflict


class TraditionType(Enum):
    """Types of family traditions."""
    COMING_OF_AGE = "coming_of_age"         # Rituals for adulthood
    SEASONAL_CELEBRATION = "seasonal_celebration"  # Holiday traditions
    STORYTELLING = "storytelling"           # Family story traditions
    SKILL_PASSING = "skill_passing"         # Teaching family skills
    MEMORIAL = "memorial"                   # Honoring deceased family
    BLESSING = "blessing"                   # Family blessing rituals
    REUNION = "reunion"                     # Family gathering traditions
    NAMING = "naming"                       # Naming traditions


@dataclass
class FamilyBond:
    """Represents a deep emotional bond between family members."""
    person1: str
    person2: str
    bond_type: BondType
    strength: float                         # 0.0-1.0 intensity of bond
    formed_day: int
    
    # Bond characteristics
    trust_level: float
    emotional_intimacy: float
    shared_experiences: List[str]
    protective_intensity: float             # How protective they are
    conflict_history: List[Dict[str, Any]]
    
    # Development tracking
    bond_milestones: List[str]
    challenges_overcome: List[str]
    growth_events: List[Dict[str, Any]]


@dataclass
class FamilyTradition:
    """Represents a unique family tradition."""
    family_id: str
    tradition_type: TraditionType
    name: str
    description: str
    started_day: int
    founder: str
    
    # Tradition details
    participants: List[str]
    frequency: str                          # daily, weekly, monthly, yearly, life_event
    significance_level: float               # 0.0-1.0 importance to family
    preservation_status: str                # thriving, declining, extinct
    
    # Cultural elements
    rituals: List[str]
    symbols: List[str]
    special_objects: List[str]
    stories_told: List[str]
    
    # Evolution
    variations: List[str]                   # How tradition has changed
    next_generation_carriers: List[str]     # Who will continue it


@dataclass
class WisdomTransmission:
    """Represents wisdom passed from elder to younger family member."""
    elder: str
    younger: str
    wisdom_type: str                        # life_advice, practical_skills, cultural_knowledge
    transmission_day: int
    
    # Content
    wisdom_content: str
    practical_applications: List[str]
    life_lessons: List[str]
    warnings_given: List[str]
    
    # Effectiveness
    receptivity: float                      # How well it was received
    application_success: float              # How well it was applied
    impact_on_decisions: List[str]


@dataclass
class GenerationalConflict:
    """Represents tension between different generations in a family."""
    elder_generation: List[str]
    younger_generation: List[str]
    conflict_source: str
    started_day: int
    
    # Conflict details
    disagreement_areas: List[str]
    values_in_conflict: List[str]
    resolution_attempts: List[str]
    mediation_events: List[Dict[str, Any]]
    
    # Resolution
    resolved: bool
    resolution_day: Optional[int]
    compromise_reached: Optional[str]
    long_term_impact: List[str]


class DeepFamilyBondsSystem:
    """
    Manages deep family emotional bonds, traditions, wisdom transmission,
    and generational dynamics within families.
    """
    
    def __init__(self):
        self.family_bonds: Dict[str, List[FamilyBond]] = defaultdict(list)
        self.family_traditions: Dict[str, List[FamilyTradition]] = defaultdict(list)
        self.wisdom_transmissions: List[WisdomTransmission] = []
        self.generational_conflicts: List[GenerationalConflict] = []
        
        # System tracking
        self.bond_formation_events: List[Dict[str, Any]] = []
        self.tradition_creation_events: List[Dict[str, Any]] = []
        self.wisdom_sharing_events: List[Dict[str, Any]] = []
        
        # Configuration
        self.bond_formation_chance = 0.8       # High chance for family bonds
        self.tradition_creation_chance = 0.1   # 10% chance when conditions met
        self.wisdom_transmission_chance = 0.3  # 30% chance for elder-youth interactions
        self.generational_conflict_chance = 0.05  # 5% chance per generation gap
        
        # Templates
        self.wisdom_templates = self._initialize_wisdom_templates()
        self.tradition_templates = self._initialize_tradition_templates()
        self.bond_milestone_templates = self._initialize_bond_milestones()
        
    def _initialize_wisdom_templates(self) -> Dict[str, List[str]]:
        """Initialize wisdom templates by category."""
        return {
            "life_advice": [
                "Trust your instincts, but verify with your mind",
                "Kindness costs nothing but is worth everything",
                "Hard work pays off, but remember to rest",
                "Listen more than you speak",
                "Family comes first, but don't lose yourself",
                "Every failure teaches something valuable",
                "Patience is the key to most problems"
            ],
            "practical_skills": [
                "How to read the weather patterns",
                "The best way to preserve food for winter",
                "How to negotiate fairly in trade",
                "The art of making things with your hands",
                "How to heal common ailments with herbs",
                "The importance of maintaining tools",
                "How to lead others without dominating them"
            ],
            "cultural_knowledge": [
                "The old stories of our people",
                "Why we celebrate certain seasons",
                "The meaning behind our family symbols",
                "How our ancestors survived difficult times",
                "The proper way to honor the dead",
                "The significance of our naming traditions",
                "The values that have kept our family strong"
            ],
            "warnings": [
                "Beware of those who promise easy solutions",
                "Don't trust someone who speaks ill of everyone",
                "Avoid making permanent decisions when emotional",
                "Be careful not to lose sight of what matters",
                "Don't let pride prevent you from asking for help",
                "Remember that power corrupts if not checked",
                "Don't sacrifice your principles for temporary gain"
            ]
        }
    
    def _initialize_tradition_templates(self) -> Dict[TraditionType, Dict[str, List[str]]]:
        """Initialize tradition templates by type."""
        return {
            TraditionType.COMING_OF_AGE: {
                "names": ["The First Hunt", "The Wisdom Walk", "The Skill Trial", "The Vision Quest"],
                "descriptions": [
                    "Young family members must demonstrate courage and skill",
                    "A journey of self-discovery guided by elders",
                    "Testing practical abilities needed for adulthood",
                    "A spiritual journey to find one's path in life"
                ]
            },
            TraditionType.SEASONAL_CELEBRATION: {
                "names": ["Harvest Gathering", "Winter Stories", "Spring Renewal", "Summer Festival"],
                "descriptions": [
                    "Family gathers to celebrate the year's bounty",
                    "Long winter nights filled with family stories",
                    "Welcoming new growth and fresh beginnings",
                    "Celebrating life and community in the warm season"
                ]
            },
            TraditionType.STORYTELLING: {
                "names": ["The Elder's Tales", "Ancestor Stories", "Heroic Chronicles", "Wisdom Legends"],
                "descriptions": [
                    "Ancient family stories passed down through generations",
                    "Tales of ancestors who shaped the family's destiny",
                    "Stories of family members who overcame great challenges",
                    "Legends that teach important life lessons"
                ]
            },
            TraditionType.SKILL_PASSING: {
                "names": ["The Craft Teaching", "Master's Legacy", "Family Art", "Sacred Knowledge"],
                "descriptions": [
                    "Essential skills passed from parent to child",
                    "Master craftspeople training the next generation",
                    "Artistic traditions unique to the family",
                    "Special knowledge kept within the family"
                ]
            }
        }
    
    def _initialize_bond_milestones(self) -> Dict[BondType, List[str]]:
        """Initialize bond milestone templates."""
        return {
            BondType.PARENTAL_LOVE: [
                "First time holding their child",
                "Teaching their child to walk",
                "Protecting their child from danger",
                "Seeing their child achieve something important",
                "Giving their child life advice"
            ],
            BondType.SIBLING_LOYALTY: [
                "Standing up for each other in conflict",
                "Sharing a secret that bonds them forever",
                "Helping each other through a crisis",
                "Celebrating each other's successes",
                "Forgiving a major disagreement"
            ],
            BondType.GRANDPARENT_WISDOM: [
                "First time sharing family stories",
                "Teaching a traditional skill",
                "Offering guidance during a difficult time",
                "Recognizing their grandchild's special talent",
                "Passing down a family heirloom"
            ]
        }
    
    def process_daily_family_bonds(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process daily family bond development and activities."""
        events = []
        
        # Phase 1: Form new family bonds
        bond_events = self._process_bond_formation(agents, current_day)
        events.extend(bond_events)
        
        # Phase 2: Strengthen existing bonds
        strengthening_events = self._process_bond_strengthening(agents, current_day)
        events.extend(strengthening_events)
        
        # Phase 3: Create and maintain family traditions
        tradition_events = self._process_family_traditions(agents, current_day)
        events.extend(tradition_events)
        
        # Phase 4: Wisdom transmission from elders
        wisdom_events = self._process_wisdom_transmission(agents, current_day)
        events.extend(wisdom_events)
        
        # Phase 5: Handle generational conflicts
        conflict_events = self._process_generational_dynamics(agents, current_day)
        events.extend(conflict_events)
        
        # Phase 6: Protective instincts and family defense
        protection_events = self._process_protective_behaviors(agents, current_day)
        events.extend(protection_events)
        
        return events
    
    def _process_bond_formation(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle formation of new family bonds."""
        events = []
        
        # Group agents by family
        families = self._group_agents_by_family(agents)
        
        for family_id, family_members in families.items():
            # Check each pair of family members for potential bonds
            for i, agent1 in enumerate(family_members):
                for agent2 in family_members[i+1:]:
                    if not self._have_established_bond(agent1, agent2):
                        bond = self._attempt_bond_formation(agent1, agent2, current_day)
                        if bond:
                            self.family_bonds[family_id].append(bond)
                            
                            events.append({
                                "type": "family_bond_formed",
                                "participants": [agent1.name, agent2.name],
                                "bond_type": bond.bond_type.value,
                                "strength": bond.strength,
                                "day": current_day
                            })
        
        return events
    
    def _process_bond_strengthening(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle strengthening of existing family bonds."""
        events = []
        
        for family_id, bonds in self.family_bonds.items():
            for bond in bonds:
                agent1 = self._get_agent_by_name(agents, bond.person1)
                agent2 = self._get_agent_by_name(agents, bond.person2)
                
                if agent1 and agent2 and agent1.is_alive and agent2.is_alive:
                    strengthening_event = self._strengthen_bond(bond, agent1, agent2, current_day)
                    if strengthening_event:
                        events.append(strengthening_event)
        
        return events
    
    def _process_family_traditions(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle creation and maintenance of family traditions."""
        events = []
        
        families = self._group_agents_by_family(agents)
        
        for family_id, family_members in families.items():
            # Check for new tradition creation
            if random.random() < self.tradition_creation_chance:
                tradition = self._create_family_tradition(family_id, family_members, current_day)
                if tradition:
                    self.family_traditions[family_id].append(tradition)
                    
                    events.append({
                        "type": "family_tradition_created",
                        "family": family_id,
                        "tradition": tradition.name,
                        "type": tradition.tradition_type.value,
                        "founder": tradition.founder,
                        "day": current_day
                    })
            
            # Practice existing traditions
            for tradition in self.family_traditions[family_id]:
                practice_event = self._practice_tradition(tradition, family_members, current_day)
                if practice_event:
                    events.append(practice_event)
        
        return events
    
    def _process_wisdom_transmission(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle wisdom transmission from elders to younger family members."""
        events = []
        
        families = self._group_agents_by_family(agents)
        
        for family_id, family_members in families.items():
            # Find elder-youth pairs
            elders = [a for a in family_members if a.age >= 50]
            youth = [a for a in family_members if a.age <= 30]
            
            for elder in elders:
                for young_member in youth:
                    if (self._are_related(elder, young_member) and 
                        random.random() < self.wisdom_transmission_chance):
                        
                        transmission = self._transmit_wisdom(elder, young_member, current_day)
                        if transmission:
                            self.wisdom_transmissions.append(transmission)
                            
                            events.append({
                                "type": "wisdom_transmitted",
                                "elder": elder.name,
                                "recipient": young_member.name,
                                "wisdom_type": transmission.wisdom_type,
                                "content": transmission.wisdom_content[:100] + "...",
                                "day": current_day
                            })
        
        return events
    
    def _process_generational_dynamics(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle generational conflicts and resolutions."""
        events = []
        
        families = self._group_agents_by_family(agents)
        
        for family_id, family_members in families.items():
            # Find different generations
            elders = [a for a in family_members if a.age >= 50]
            youth = [a for a in family_members if a.age <= 30]
            
            if elders and youth:
                # Check for generational conflicts
                if random.random() < self.generational_conflict_chance:
                    conflict = self._create_generational_conflict(elders, youth, current_day)
                    if conflict:
                        self.generational_conflicts.append(conflict)
                        
                        events.append({
                            "type": "generational_conflict",
                            "family": family_id,
                            "elders": [e.name for e in elders],
                            "youth": [y.name for y in youth],
                            "source": conflict.conflict_source,
                            "day": current_day
                        })
        
        return events
    
    def _process_protective_behaviors(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle protective family behaviors."""
        events = []
        
        # Check for threats to family members and protective responses
        for agent in agents:
            if not agent.is_alive:
                continue
            
            # Check recent traumatic experiences of family members
            family_members = self._get_family_members(agent, agents)
            for family_member in family_members:
                if self._family_member_in_danger(family_member):
                    protective_event = self._trigger_protective_behavior(agent, family_member, current_day)
                    if protective_event:
                        events.append(protective_event)
        
        return events
    
    def _strengthen_bond(self, bond: FamilyBond, agent1: Any, agent2: Any, current_day: int) -> Optional[Dict[str, Any]]:
        """Strengthen an existing family bond."""
        # Chance for bond strengthening based on positive interactions
        if random.random() < 0.1:  # 10% chance per day
            strength_increase = random.uniform(0.05, 0.15)
            bond.strength = min(1.0, bond.strength + strength_increase)
            
            # Add shared experience
            shared_experiences = [
                "Spending quality time together",
                "Supporting each other through difficulty", 
                "Celebrating together",
                "Working on a project together",
                "Having deep conversation"
            ]
            experience = random.choice(shared_experiences)
            bond.shared_experiences.append(experience)
            
            # Create memories
            agent1.memory.store_memory(
                f"I had a meaningful moment with {agent2.name}: {experience}",
                importance=0.6,
                emotion="bonding",
                memory_type="family"
            )
            
            agent2.memory.store_memory(
                f"I felt closer to {agent1.name} when we shared {experience}",
                importance=0.6,
                emotion="bonding", 
                memory_type="family"
            )
            
            return {
                "type": "family_bond_strengthened",
                "participants": [agent1.name, agent2.name],
                "bond_type": bond.bond_type.value,
                "new_strength": bond.strength,
                "shared_experience": experience,
                "day": current_day
            }
        
        return None
    
    def _create_family_tradition(self, family_id: str, family_members: List[Any], current_day: int) -> Optional[FamilyTradition]:
        """Create a new family tradition."""
        if len(family_members) < 2:
            return None
        
        # Choose tradition type based on family characteristics
        tradition_type = self._select_tradition_type(family_members)
        tradition_templates = self.tradition_templates.get(tradition_type, {})
        
        if not tradition_templates:
            return None
        
        name = random.choice(tradition_templates.get("names", ["Family Custom"]))
        description = random.choice(tradition_templates.get("descriptions", ["A meaningful family practice"]))
        founder = random.choice(family_members).name
        
        return FamilyTradition(
            family_id=family_id,
            tradition_type=tradition_type,
            name=name,
            description=description,
            started_day=current_day,
            founder=founder,
            participants=[member.name for member in family_members],
            frequency="yearly",
            significance_level=random.uniform(0.6, 0.9),
            preservation_status="thriving",
            rituals=[],
            symbols=[],
            special_objects=[],
            stories_told=[],
            variations=[],
            next_generation_carriers=[]
        )
    
    def _practice_tradition(self, tradition: FamilyTradition, family_members: List[Any], current_day: int) -> Optional[Dict[str, Any]]:
        """Practice an existing family tradition."""
        # Check if it's time to practice this tradition
        should_practice = False
        
        if tradition.frequency == "daily" and random.random() < 0.3:
            should_practice = True
        elif tradition.frequency == "weekly" and current_day % 7 == 0 and random.random() < 0.4:
            should_practice = True
        elif tradition.frequency == "monthly" and current_day % 30 == 0 and random.random() < 0.6:
            should_practice = True
        elif tradition.frequency == "yearly" and current_day % 365 == 0:
            should_practice = True
        
        if should_practice:
            # Update tradition vitality
            tradition.significance_level = min(1.0, tradition.significance_level + 0.05)
            
            # Create memories for participants
            for member in family_members:
                if member.name in tradition.participants:
                    member.memory.store_memory(
                        f"We practiced our family tradition '{tradition.name}': {tradition.description}",
                        importance=0.7,
                        emotion="belonging",
                        memory_type="tradition"
                    )
            
            return {
                "type": "family_tradition_practiced",
                "tradition": tradition.name,
                "family": tradition.family_id,
                "participants": [m.name for m in family_members if m.name in tradition.participants],
                "day": current_day
            }
        
        return None
    
    def _create_generational_conflict(self, elders: List[Any], youth: List[Any], current_day: int) -> Optional[GenerationalConflict]:
        """Create a generational conflict."""
        conflict_sources = [
            "Different values about tradition vs. innovation",
            "Disagreement about proper behavior",
            "Conflict over family resources",
            "Different views on relationships",
            "Disagreement about work and responsibility"
        ]
        
        source = random.choice(conflict_sources)
        
        return GenerationalConflict(
            elder_generation=[e.name for e in elders],
            younger_generation=[y.name for y in youth],
            conflict_source=source,
            started_day=current_day,
            disagreement_areas=[source],
            values_in_conflict=["tradition vs change"],
            resolution_attempts=[],
            mediation_events=[],
            resolved=False,
            resolution_day=None,
            compromise_reached=None,
            long_term_impact=[]
        )
    
    def _have_established_bond(self, agent1: Any, agent2: Any) -> bool:
        """Check if two agents already have an established bond."""
        for bonds in self.family_bonds.values():
            for bond in bonds:
                if ((bond.person1 == agent1.name and bond.person2 == agent2.name) or
                    (bond.person1 == agent2.name and bond.person2 == agent1.name)):
                    return True
        return False
    
    def _select_tradition_type(self, family_members: List[Any]) -> TraditionType:
        """Select appropriate tradition type for family."""
        # Simple selection for now
        tradition_types = list(TraditionType)
        return random.choice(tradition_types)
    
    def _get_family_members(self, agent: Any, all_agents: List[Any]) -> List[Any]:
        """Get all family members of an agent."""
        family_members = []
        if hasattr(agent, 'family'):
            family_id = agent.family.get('family_id')
            for other_agent in all_agents:
                if (other_agent.is_alive and hasattr(other_agent, 'family') and
                    other_agent.family.get('family_id') == family_id):
                    family_members.append(other_agent)
        return family_members
    
    def _family_member_in_danger(self, agent: Any) -> bool:
        """Check if family member is in danger or distress."""
        # Simple check - could be expanded
        return agent.health < 0.3 or random.random() < 0.05
    
    def _trigger_protective_behavior(self, protector: Any, protected: Any, current_day: int) -> Optional[Dict[str, Any]]:
        """Trigger protective behavior from one family member to another."""
        if random.random() < 0.7:  # 70% chance to act protectively
            protective_actions = [
                "Staying close to provide comfort",
                "Seeking help for their family member",
                "Offering resources and support",
                "Defending them from threats"
            ]
            
            action = random.choice(protective_actions)
            
            # Create memories
            protector.memory.store_memory(
                f"I feel protective of {protected.name} and am {action.lower()}",
                importance=0.8,
                emotion="protective",
                memory_type="family"
            )
            
            return {
                "type": "protective_behavior",
                "protector": protector.name,
                "protected": protected.name,
                "action": action,
                "day": current_day
            }
        
        return None
    
    def _group_agents_by_family(self, agents: List[Any]) -> Dict[str, List[Any]]:
        """Group agents by their family ID."""
        families = defaultdict(list)
        
        for agent in agents:
            if agent.is_alive and hasattr(agent, 'family'):
                family_id = agent.family.get('family_id', f"family_{agent.name}")
                families[family_id].append(agent)
        
        return families
    
    def _attempt_bond_formation(self, agent1: Any, agent2: Any, current_day: int) -> Optional[FamilyBond]:
        """Attempt to form a family bond between two agents."""
        relationship = self._determine_family_relationship(agent1, agent2)
        if not relationship:
            return None
        
        # Determine bond type based on relationship
        bond_type = self._get_bond_type_for_relationship(relationship, agent1, agent2)
        if not bond_type:
            return None
        
        # Calculate bond strength
        strength = self._calculate_bond_strength(agent1, agent2, bond_type)
        
        if strength >= 0.3:  # Minimum threshold for bond formation
            return FamilyBond(
                person1=agent1.name,
                person2=agent2.name,
                bond_type=bond_type,
                strength=strength,
                formed_day=current_day,
                trust_level=strength * 0.8,
                emotional_intimacy=strength * 0.6,
                shared_experiences=[],
                protective_intensity=strength if bond_type == BondType.PARENTAL_LOVE else strength * 0.5,
                conflict_history=[],
                bond_milestones=[],
                challenges_overcome=[],
                growth_events=[]
            )
        
        return None
    
    def _determine_family_relationship(self, agent1: Any, agent2: Any) -> Optional[str]:
        """Determine the family relationship between two agents."""
        if not (hasattr(agent1, 'family') and hasattr(agent2, 'family')):
            return None
        
        # Check parent-child relationships
        if agent2.name in agent1.family.get('children', []):
            return "parent_child"
        if agent1.name in agent2.family.get('children', []):
            return "child_parent"
        
        # Check sibling relationships
        if agent2.name in agent1.family.get('siblings', []):
            return "sibling"
        
        # Check grandparent-grandchild
        if agent2.name in agent1.family.get('grandchildren', []):
            return "grandparent_grandchild"
        if agent1.name in agent2.family.get('grandchildren', []):
            return "grandchild_grandparent"
        
        return None
    
    def _get_bond_type_for_relationship(self, relationship: str, agent1: Any, agent2: Any) -> Optional[BondType]:
        """Get appropriate bond type for family relationship."""
        if relationship == "parent_child":
            return BondType.PARENTAL_LOVE
        elif relationship == "child_parent":
            return BondType.FILIAL_DEVOTION
        elif relationship == "sibling":
            # Determine if it's loyalty or rivalry based on personalities
            if self._siblings_have_rivalry(agent1, agent2):
                return BondType.SIBLING_RIVALRY
            else:
                return BondType.SIBLING_LOYALTY
        elif relationship == "grandparent_grandchild":
            return BondType.GRANDPARENT_WISDOM
        elif relationship == "grandchild_grandparent":
            return BondType.FILIAL_DEVOTION
        
        return None
    
    def _calculate_bond_strength(self, agent1: Any, agent2: Any, bond_type: BondType) -> float:
        """Calculate the strength of a family bond."""
        base_strength = 0.6  # Family bonds start strong
        
        # Personality compatibility
        compatibility = self._calculate_family_compatibility(agent1, agent2)
        
        # Bond type modifiers
        if bond_type == BondType.PARENTAL_LOVE:
            base_strength = 0.9  # Parental love is very strong
        elif bond_type == BondType.SIBLING_RIVALRY:
            base_strength = 0.4  # Rivalry is weaker
        elif bond_type == BondType.GRANDPARENT_WISDOM:
            base_strength = 0.7  # Strong wisdom bonds
        
        # Age factor (closer ages often bond better for siblings)
        if bond_type in [BondType.SIBLING_LOYALTY, BondType.SIBLING_RIVALRY]:
            age_diff = abs(agent1.age - agent2.age)
            age_factor = max(0.5, 1.0 - (age_diff / 20.0))
            base_strength *= age_factor
        
        return min(1.0, base_strength + compatibility * 0.3)
    
    def _calculate_family_compatibility(self, agent1: Any, agent2: Any) -> float:
        """Calculate personality compatibility between family members."""
        # Use personality scores if available
        if hasattr(agent1, 'personality_scores') and hasattr(agent2, 'personality_scores'):
            score1 = agent1.personality_scores
            score2 = agent2.personality_scores
            
            # Calculate similarity in key traits
            agreeableness_sim = 1.0 - abs(score1.get("agreeableness", 0.5) - score2.get("agreeableness", 0.5))
            conscientiousness_sim = 1.0 - abs(score1.get("conscientiousness", 0.5) - score2.get("conscientiousness", 0.5))
            
            return (agreeableness_sim + conscientiousness_sim) / 2
        
        return 0.5  # Neutral compatibility
    
    def _siblings_have_rivalry(self, agent1: Any, agent2: Any) -> bool:
        """Determine if siblings are likely to have rivalry."""
        # Close age gaps often create rivalry
        age_diff = abs(agent1.age - agent2.age)
        if age_diff <= 3:
            return random.random() < 0.4  # 40% chance
        
        # Similar personalities might compete
        if hasattr(agent1, 'personality_scores') and hasattr(agent2, 'personality_scores'):
            competitiveness1 = agent1.personality_scores.get("extraversion", 0.5)
            competitiveness2 = agent2.personality_scores.get("extraversion", 0.5)
            
            if competitiveness1 > 0.7 and competitiveness2 > 0.7:
                return random.random() < 0.6  # 60% chance
        
        return random.random() < 0.2  # 20% base chance
    
    def _are_related(self, agent1: Any, agent2: Any) -> bool:
        """Check if two agents are family members."""
        if not (hasattr(agent1, 'family') and hasattr(agent2, 'family')):
            return False
        
        # Check various family relationships
        family1 = agent1.family
        family2 = agent2.family
        
        # Same family ID
        if family1.get('family_id') == family2.get('family_id'):
            return True
        
        # Direct relationships
        if (agent2.name in family1.get('children', []) or
            agent2.name in family1.get('parents', []) or
            agent2.name in family1.get('siblings', []) or
            agent2.name in family1.get('grandchildren', []) or
            agent2.name in family1.get('grandparents', [])):
            return True
        
        return False
    
    def _transmit_wisdom(self, elder: Any, younger: Any, current_day: int) -> Optional[WisdomTransmission]:
        """Create a wisdom transmission event."""
        # Choose type of wisdom to transmit
        wisdom_types = ["life_advice", "practical_skills", "cultural_knowledge", "warnings"]
        wisdom_type = random.choice(wisdom_types)
        
        # Select appropriate wisdom content
        wisdom_options = self.wisdom_templates[wisdom_type]
        wisdom_content = random.choice(wisdom_options)
        
        # Generate practical applications
        applications = self._generate_practical_applications(wisdom_type)
        
        # Calculate receptivity
        receptivity = self._calculate_wisdom_receptivity(elder, younger)
        
        if receptivity >= 0.3:  # Minimum receptivity threshold
            transmission = WisdomTransmission(
                elder=elder.name,
                younger=younger.name,
                wisdom_type=wisdom_type,
                transmission_day=current_day,
                wisdom_content=wisdom_content,
                practical_applications=applications,
                life_lessons=[wisdom_content],
                warnings_given=[] if wisdom_type != "warnings" else [wisdom_content],
                receptivity=receptivity,
                application_success=0.0,  # Will be updated over time
                impact_on_decisions=[]
            )
            
            # Create memories for both
            elder.memory.store_memory(
                f"I shared important wisdom with {younger.name}: {wisdom_content}",
                importance=0.7,
                emotion="wise",
                memory_type="teaching"
            )
            
            younger.memory.store_memory(
                f"{elder.name} shared wisdom with me: {wisdom_content}. I should remember this.",
                importance=0.8,
                emotion="grateful",
                memory_type="learning"
            )
            
            return transmission
        
        return None
    
    def _calculate_wisdom_receptivity(self, elder: Any, younger: Any) -> float:
        """Calculate how receptive the younger person is to wisdom."""
        base_receptivity = 0.5
        
        # Age factor (very young are more receptive)
        if younger.age < 20:
            base_receptivity += 0.3
        elif younger.age < 30:
            base_receptivity += 0.1
        
        # Personality factors
        if hasattr(younger, 'personality_scores'):
            openness = younger.personality_scores.get("openness", 0.5)
            conscientiousness = younger.personality_scores.get("conscientiousness", 0.5)
            base_receptivity += (openness + conscientiousness) * 0.2
        
        # Relationship strength
        bond_strength = self._get_bond_strength(elder.name, younger.name)
        base_receptivity += bond_strength * 0.3
        
        return min(1.0, base_receptivity)
    
    def _get_bond_strength(self, person1: str, person2: str) -> float:
        """Get bond strength between two family members."""
        for bonds in self.family_bonds.values():
            for bond in bonds:
                if ((bond.person1 == person1 and bond.person2 == person2) or
                    (bond.person1 == person2 and bond.person2 == person1)):
                    return bond.strength
        return 0.5  # Default neutral strength
    
    def _generate_practical_applications(self, wisdom_type: str) -> List[str]:
        """Generate practical applications for wisdom."""
        applications = {
            "life_advice": ["Make better decisions", "Improve relationships", "Handle stress better"],
            "practical_skills": ["Apply in daily work", "Teach others", "Improve efficiency"],
            "cultural_knowledge": ["Understand traditions", "Participate in ceremonies", "Share stories"],
            "warnings": ["Avoid dangerous situations", "Recognize warning signs", "Make safer choices"]
        }
        
        return applications.get(wisdom_type, ["Apply in daily life"])
    
    def _get_agent_by_name(self, agents: List[Any], name: str) -> Optional[Any]:
        """Get agent by name from list."""
        for agent in agents:
            if agent.name == name:
                return agent
        return None
    
    def get_family_summary(self, family_id: str) -> Dict[str, Any]:
        """Get comprehensive summary of a family."""
        bonds = self.family_bonds.get(family_id, [])
        traditions = self.family_traditions.get(family_id, [])
        
        return {
            "family_id": family_id,
            "total_bonds": len(bonds),
            "bond_types": [bond.bond_type.value for bond in bonds],
            "average_bond_strength": sum(bond.strength for bond in bonds) / max(1, len(bonds)),
            "traditions": [tradition.name for tradition in traditions],
            "active_traditions": len([t for t in traditions if t.preservation_status == "thriving"]),
            "wisdom_transmissions": len([w for w in self.wisdom_transmissions 
                                       if any(bond.person1 == w.elder or bond.person1 == w.younger 
                                             for bond in bonds)])
        }
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get comprehensive family bonds system summary."""
        total_bonds = sum(len(bonds) for bonds in self.family_bonds.values())
        total_traditions = sum(len(traditions) for traditions in self.family_traditions.values())
        
        bond_type_distribution = {}
        for bonds in self.family_bonds.values():
            for bond in bonds:
                bond_type = bond.bond_type.value
                bond_type_distribution[bond_type] = bond_type_distribution.get(bond_type, 0) + 1
        
        return {
            "total_family_bonds": total_bonds,
            "total_family_traditions": total_traditions,
            "total_wisdom_transmissions": len(self.wisdom_transmissions),
            "active_families": len(self.family_bonds),
            "bond_type_distribution": bond_type_distribution,
            "average_bond_strength": sum(bond.strength for bonds in self.family_bonds.values() 
                                       for bond in bonds) / max(1, total_bonds),
            "tradition_preservation_rate": len([t for traditions in self.family_traditions.values() 
                                              for t in traditions if t.preservation_status == "thriving"]) / 
                                         max(1, total_traditions)
        } 