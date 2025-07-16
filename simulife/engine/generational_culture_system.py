"""
Generational Cultural Transmission System for SimuLife
Handles how culture, knowledge, values, and traditions pass between generations and evolve.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict


class CultureType(Enum):
    """Types of cultural elements."""
    VALUES = "values"                    # Core beliefs and principles
    TRADITIONS = "traditions"           # Recurring practices and ceremonies
    KNOWLEDGE = "knowledge"             # Skills, technologies, and information
    STORIES = "stories"                 # Narratives, myths, and histories
    CUSTOMS = "customs"                 # Social norms and behaviors
    LANGUAGE = "language"               # Communication patterns and expressions
    ARTS = "arts"                       # Creative expressions and aesthetics
    RITUALS = "rituals"                 # Spiritual and ceremonial practices


class TransmissionType(Enum):
    """Methods of cultural transmission."""
    PARENT_TO_CHILD = "parent_to_child"         # Direct family transmission
    ELDER_TO_YOUTH = "elder_to_youth"           # Community elder teaching
    PEER_TO_PEER = "peer_to_peer"               # Same generation sharing
    FORMAL_EDUCATION = "formal_education"       # Institutional learning
    STORYTELLING = "storytelling"               # Narrative transmission
    APPRENTICESHIP = "apprenticeship"           # Skill-based learning
    RITUAL_PARTICIPATION = "ritual_participation" # Learning through practice
    OBSERVATION = "observation"                 # Learning by watching


class CulturalEvolution(Enum):
    """Types of cultural evolution."""
    PRESERVATION = "preservation"        # Maintaining traditions unchanged
    ADAPTATION = "adaptation"           # Modifying traditions for new circumstances
    INNOVATION = "innovation"           # Creating new cultural elements
    FUSION = "fusion"                   # Combining different cultural elements
    ABANDONMENT = "abandonment"         # Letting traditions fade away
    REVIVAL = "revival"                 # Bringing back old traditions


@dataclass
class CulturalElement:
    """Represents a cultural element that can be transmitted."""
    id: str
    name: str
    culture_type: CultureType
    description: str
    origin_generation: int              # Generation when it started
    current_generation: int             # Latest generation that knows it
    knowledge_bearers: Set[str]         # Agents who carry this culture
    transmission_methods: List[TransmissionType]
    complexity: float                   # How difficult it is to learn (0.0-1.0)
    importance: float                   # How important it is to the community (0.0-1.0)
    adaptability: float                 # How easily it can be modified (0.0-1.0)
    preservation_rate: float            # How likely it is to be passed on (0.0-1.0)
    evolution_history: List[Dict[str, Any]]  # Record of changes over time
    associated_skills: List[str]        # Skills related to this culture
    prerequisites: List[str]            # Other cultural elements needed first


@dataclass
class GenerationData:
    """Data about a specific generation."""
    generation_number: int
    birth_year_range: Tuple[int, int]   # (earliest_birth, latest_birth)
    agents: Set[str]                    # Agent names in this generation
    cultural_innovations: List[str]     # New cultural elements created
    cultural_losses: List[str]          # Cultural elements lost
    dominant_values: Dict[str, float]   # Prevalent values and their strengths
    generational_identity: str          # Unique characteristics of this generation
    life_experiences: List[str]         # Major events this generation lived through


@dataclass
class CulturalTransmissionEvent:
    """Records a cultural transmission event."""
    transmitter: str                    # Agent passing on culture
    receiver: str                       # Agent receiving culture
    cultural_element: str               # What was transmitted
    transmission_type: TransmissionType
    success: bool                       # Whether transmission was successful
    fidelity: float                     # How accurately it was transmitted (0.0-1.0)
    day: int
    generation_gap: int                 # Number of generations between transmitter and receiver


class GenerationalCultureSystem:
    """
    Manages cultural transmission between generations and cultural evolution.
    """
    
    def __init__(self):
        self.cultural_elements: Dict[str, CulturalElement] = {}
        self.generations: Dict[int, GenerationData] = {}
        self.transmission_events: List[CulturalTransmissionEvent] = []
        self.cultural_lineages: Dict[str, List[str]] = {}  # cultural_element -> lineage of bearers
        
        # Initialize base cultural elements
        self._initialize_base_culture()
        
        # Transmission effectiveness factors
        self.transmission_factors = {
            "family_bonus": 0.3,           # Bonus for family transmission
            "age_gap_penalty": 0.05,       # Penalty per 10-year age gap
            "relationship_bonus": 0.2,     # Bonus for good relationships
            "skill_match_bonus": 0.25,     # Bonus when skills match culture
            "formal_education_bonus": 0.4, # Bonus for institutional learning
            "repeated_exposure_bonus": 0.1 # Bonus for multiple exposures
        }
    
    def _initialize_base_culture(self):
        """Initialize fundamental cultural elements."""
        base_elements = [
            # Values
            CulturalElement(
                id="respect_for_elders",
                name="Respect for Elders",
                culture_type=CultureType.VALUES,
                description="Valuing the wisdom and experience of older community members",
                origin_generation=0,
                current_generation=0,
                knowledge_bearers=set(),
                transmission_methods=[TransmissionType.PARENT_TO_CHILD, TransmissionType.ELDER_TO_YOUTH],
                complexity=0.3,
                importance=0.8,
                adaptability=0.4,
                preservation_rate=0.9,
                evolution_history=[],
                associated_skills=["social", "wisdom"],
                prerequisites=[]
            ),
            
            # Traditions
            CulturalElement(
                id="birth_celebration",
                name="Birth Celebration Ceremony",
                culture_type=CultureType.TRADITIONS,
                description="Ceremonial celebration when a new child is born",
                origin_generation=0,
                current_generation=0,
                knowledge_bearers=set(),
                transmission_methods=[TransmissionType.RITUAL_PARTICIPATION, TransmissionType.OBSERVATION],
                complexity=0.5,
                importance=0.7,
                adaptability=0.6,
                preservation_rate=0.8,
                evolution_history=[],
                associated_skills=["social", "organization"],
                prerequisites=[]
            ),
            
            # Knowledge
            CulturalElement(
                id="fire_wisdom",
                name="Fire-Making Wisdom",
                culture_type=CultureType.KNOWLEDGE,
                description="Traditional knowledge about making and maintaining fire",
                origin_generation=0,
                current_generation=0,
                knowledge_bearers=set(),
                transmission_methods=[TransmissionType.APPRENTICESHIP, TransmissionType.PARENT_TO_CHILD],
                complexity=0.4,
                importance=0.9,
                adaptability=0.5,
                preservation_rate=0.95,
                evolution_history=[],
                associated_skills=["survival", "crafting"],
                prerequisites=[]
            ),
            
            # Stories
            CulturalElement(
                id="origin_story",
                name="Origin Story of the People",
                culture_type=CultureType.STORIES,
                description="Narrative explaining how the community came to be",
                origin_generation=0,
                current_generation=0,
                knowledge_bearers=set(),
                transmission_methods=[TransmissionType.STORYTELLING, TransmissionType.ELDER_TO_YOUTH],
                complexity=0.6,
                importance=0.8,
                adaptability=0.8,
                preservation_rate=0.7,
                evolution_history=[],
                associated_skills=["memory", "social"],
                prerequisites=[]
            ),
            
            # Customs
            CulturalElement(
                id="greeting_customs",
                name="Traditional Greetings",
                culture_type=CultureType.CUSTOMS,
                description="Customary ways of greeting and acknowledging others",
                origin_generation=0,
                current_generation=0,
                knowledge_bearers=set(),
                transmission_methods=[TransmissionType.OBSERVATION, TransmissionType.PEER_TO_PEER],
                complexity=0.2,
                importance=0.6,
                adaptability=0.7,
                preservation_rate=0.8,
                evolution_history=[],
                associated_skills=["social"],
                prerequisites=[]
            ),
            
            # Arts
            CulturalElement(
                id="ancestral_songs",
                name="Songs of the Ancestors",
                culture_type=CultureType.ARTS,
                description="Traditional songs passed down through generations",
                origin_generation=0,
                current_generation=0,
                knowledge_bearers=set(),
                transmission_methods=[TransmissionType.STORYTELLING, TransmissionType.RITUAL_PARTICIPATION],
                complexity=0.7,
                importance=0.6,
                adaptability=0.5,
                preservation_rate=0.6,
                evolution_history=[],
                associated_skills=["memory", "artistry"],
                prerequisites=[]
            )
        ]
        
        for element in base_elements:
            self.cultural_elements[element.id] = element
    
    def initialize_agent_culture(self, agent: Any, current_day: int) -> Dict[str, float]:
        """Initialize cultural knowledge for a new agent based on family and community."""
        agent_culture = {}
        
        # Determine agent's generation
        generation = self._determine_agent_generation(agent, current_day)
        
        # Family cultural transmission (if agent has parents)
        if hasattr(agent, 'family') and agent.family.get('parents'):
            for parent_name in agent.family['parents']:
                parent_culture = self._get_agent_culture(parent_name)
                for culture_id, knowledge_level in parent_culture.items():
                    element = self.cultural_elements[culture_id]
                    # Family transmission has high success rate
                    transmission_success = random.random() < (element.preservation_rate + 0.2)
                    if transmission_success:
                        fidelity = random.uniform(0.7, 1.0)  # High fidelity for family transmission
                        agent_culture[culture_id] = knowledge_level * fidelity
        
        # Community cultural transmission (baseline cultural elements everyone learns)
        for culture_id, element in self.cultural_elements.items():
            if culture_id not in agent_culture:
                # Check if this is a foundational cultural element
                if element.importance > 0.7 and len(element.prerequisites) == 0:
                    community_transmission_chance = element.preservation_rate * 0.8
                    if random.random() < community_transmission_chance:
                        agent_culture[culture_id] = random.uniform(0.3, 0.8)
        
        # Update cultural element knowledge bearers
        for culture_id, knowledge_level in agent_culture.items():
            if knowledge_level > 0.5:  # Sufficient knowledge to be considered a bearer
                self.cultural_elements[culture_id].knowledge_bearers.add(agent.name)
        
        return agent_culture
    
    def _determine_agent_generation(self, agent: Any, current_day: int) -> int:
        """Determine which generation an agent belongs to."""
        # Simple generation calculation based on birth year
        birth_year = agent.birth_day // 365
        generation = max(0, birth_year // 25)  # 25-year generations
        
        # Update generation data
        if generation not in self.generations:
            self.generations[generation] = GenerationData(
                generation_number=generation,
                birth_year_range=(birth_year, birth_year),
                agents=set(),
                cultural_innovations=[],
                cultural_losses=[],
                dominant_values={},
                generational_identity="",
                life_experiences=[]
            )
        else:
            # Update birth year range
            min_year, max_year = self.generations[generation].birth_year_range
            self.generations[generation].birth_year_range = (
                min(min_year, birth_year),
                max(max_year, birth_year)
            )
        
        self.generations[generation].agents.add(agent.name)
        return generation
    
    def _get_agent_culture(self, agent_name: str) -> Dict[str, float]:
        """Get cultural knowledge for an agent."""
        # This would be stored on the agent or in a separate system
        # For now, return empty dict as placeholder
        return {}
    
    def process_daily_cultural_transmission(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process daily cultural transmission events."""
        transmission_events = []
        
        # Process various types of cultural transmission
        transmission_events.extend(self._process_family_transmission(agents, current_day))
        transmission_events.extend(self._process_elder_teaching(agents, current_day))
        transmission_events.extend(self._process_peer_sharing(agents, current_day))
        transmission_events.extend(self._process_storytelling_events(agents, current_day))
        transmission_events.extend(self._process_ritual_transmission(agents, current_day))
        
        # Process cultural evolution
        evolution_events = self._process_cultural_evolution(agents, current_day)
        transmission_events.extend(evolution_events)
        
        # Update cultural preservation and loss
        preservation_events = self._process_cultural_preservation(agents, current_day)
        transmission_events.extend(preservation_events)
        
        return transmission_events
    
    def _process_family_transmission(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process cultural transmission within families."""
        events = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            # Parents teaching children
            if hasattr(agent, 'family') and agent.family.get('children'):
                for child_name in agent.family['children']:
                    child = next((a for a in agents if a.name == child_name), None)
                    if child and child.is_alive and random.random() < 0.1:  # 10% chance per day
                        transmission_event = self._attempt_cultural_transmission(
                            agent, child, TransmissionType.PARENT_TO_CHILD, current_day
                        )
                        if transmission_event:
                            events.append(transmission_event)
        
        return events
    
    def _process_elder_teaching(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process elders teaching younger community members."""
        events = []
        
        # Find elders (agents over 60)
        elders = [a for a in agents if a.is_alive and a.age >= 60]
        youths = [a for a in agents if a.is_alive and a.age < 30]
        
        for elder in elders:
            if random.random() < 0.05:  # 5% chance per day
                if youths:
                    student = random.choice(youths)
                    transmission_event = self._attempt_cultural_transmission(
                        elder, student, TransmissionType.ELDER_TO_YOUTH, current_day
                    )
                    if transmission_event:
                        events.append(transmission_event)
        
        return events
    
    def _process_peer_sharing(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process cultural sharing between peers."""
        events = []
        
        # Group agents by similar age
        age_groups = defaultdict(list)
        for agent in agents:
            if agent.is_alive:
                age_group = agent.age // 10 * 10  # Group by decades
                age_groups[age_group].append(agent)
        
        for age_group, group_agents in age_groups.items():
            if len(group_agents) >= 2:
                # Random peer interactions
                for _ in range(max(1, len(group_agents) // 3)):
                    if random.random() < 0.08:  # 8% chance
                        agent1, agent2 = random.sample(group_agents, 2)
                        transmission_event = self._attempt_cultural_transmission(
                            agent1, agent2, TransmissionType.PEER_TO_PEER, current_day
                        )
                        if transmission_event:
                            events.append(transmission_event)
        
        return events
    
    def _process_storytelling_events(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process storytelling events that transmit cultural narratives."""
        events = []
        
        # Community storytelling events
        if random.random() < 0.03:  # 3% chance per day
            # Find a storyteller (someone with high social skills or memory)
            storytellers = []
            for agent in agents:
                if agent.is_alive:
                    storytelling_ability = 0.5  # Base ability
                    if hasattr(agent, 'skills'):
                        if 'social' in agent.skills:
                            social_skill = agent.skills['social']
                            if isinstance(social_skill, float):
                                storytelling_ability += social_skill * 0.3
                        if 'memory' in agent.skills:
                            memory_skill = agent.skills['memory']
                            if isinstance(memory_skill, float):
                                storytelling_ability += memory_skill * 0.3
                    
                    storytellers.append((agent, storytelling_ability))
            
            if storytellers:
                # Choose storyteller based on ability
                storytellers.sort(key=lambda x: x[1], reverse=True)
                storyteller = storytellers[0][0]
                
                # Find audience
                potential_audience = [a for a in agents if a.is_alive and a.name != storyteller.name]
                audience = random.sample(potential_audience, min(random.randint(2, 8), len(potential_audience)))
                
                # Transmit story-based cultural elements
                story_elements = [e for e in self.cultural_elements.values() 
                                if e.culture_type in [CultureType.STORIES, CultureType.VALUES]]
                
                if story_elements:
                    element = random.choice(story_elements)
                    successful_transmissions = 0
                    
                    for listener in audience:
                        if self._transmit_cultural_element(storyteller, listener, element, 
                                                         TransmissionType.STORYTELLING, current_day):
                            successful_transmissions += 1
                    
                    events.append({
                        "type": "storytelling_event",
                        "storyteller": storyteller.name,
                        "audience": [a.name for a in audience],
                        "cultural_element": element.name,
                        "successful_transmissions": successful_transmissions,
                        "day": current_day
                    })
        
        return events
    
    def _process_ritual_transmission(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process cultural transmission through ritual participation."""
        events = []
        
        # Community rituals
        if random.random() < 0.02:  # 2% chance per day
            # Find ritual elements
            ritual_elements = [e for e in self.cultural_elements.values() 
                             if e.culture_type in [CultureType.RITUALS, CultureType.TRADITIONS]]
            
            if ritual_elements:
                element = random.choice(ritual_elements)
                
                # Find participants
                participants = random.sample(
                    [a for a in agents if a.is_alive], 
                    min(random.randint(3, 10), len([a for a in agents if a.is_alive]))
                )
                
                # Ritual transmission has moderate success but high fidelity
                successful_transmissions = 0
                for participant in participants:
                    if random.random() < 0.6:  # 60% success rate for ritual transmission
                        element.knowledge_bearers.add(participant.name)
                        successful_transmissions += 1
                        
                        # Add cultural memory
                        participant.memory.store_memory(
                            f"Participated in {element.name} ritual ceremony",
                            importance=0.7,
                            memory_type="cultural"
                        )
                
                events.append({
                    "type": "ritual_transmission",
                    "ritual": element.name,
                    "participants": [p.name for p in participants],
                    "successful_transmissions": successful_transmissions,
                    "day": current_day
                })
        
        return events
    
    def _attempt_cultural_transmission(self, transmitter: Any, receiver: Any, 
                                     transmission_type: TransmissionType, 
                                     current_day: int) -> Optional[Dict[str, Any]]:
        """Attempt to transmit cultural knowledge between two agents."""
        # Find cultural elements the transmitter knows but receiver doesn't
        transmitter_culture = self._get_agent_cultural_knowledge(transmitter)
        receiver_culture = self._get_agent_cultural_knowledge(receiver)
        
        transmittable_elements = []
        for culture_id, knowledge_level in transmitter_culture.items():
            if knowledge_level > 0.5:  # Sufficient knowledge to transmit
                receiver_knowledge = receiver_culture.get(culture_id, 0.0)
                if receiver_knowledge < knowledge_level - 0.2:  # Significant knowledge gap
                    transmittable_elements.append(culture_id)
        
        if not transmittable_elements:
            return None
        
        # Choose a cultural element to transmit
        culture_id = random.choice(transmittable_elements)
        element = self.cultural_elements[culture_id]
        
        # Attempt transmission
        success = self._transmit_cultural_element(transmitter, receiver, element, 
                                                transmission_type, current_day)
        
        if success:
            return {
                "type": "cultural_transmission",
                "transmitter": transmitter.name,
                "receiver": receiver.name,
                "cultural_element": element.name,
                "transmission_type": transmission_type.value,
                "success": True,
                "day": current_day
            }
        
        return None
    
    def _transmit_cultural_element(self, transmitter: Any, receiver: Any, 
                                  element: CulturalElement, transmission_type: TransmissionType,
                                  current_day: int) -> bool:
        """Attempt to transmit a specific cultural element."""
        # Calculate transmission success probability
        base_success = 0.5
        
        # Transmission type modifiers
        type_modifiers = {
            TransmissionType.PARENT_TO_CHILD: 0.3,
            TransmissionType.ELDER_TO_YOUTH: 0.2,
            TransmissionType.APPRENTICESHIP: 0.4,
            TransmissionType.FORMAL_EDUCATION: 0.4,
            TransmissionType.RITUAL_PARTICIPATION: 0.2,
            TransmissionType.STORYTELLING: 0.1,
            TransmissionType.PEER_TO_PEER: 0.0,
            TransmissionType.OBSERVATION: -0.1
        }
        
        success_probability = base_success + type_modifiers.get(transmission_type, 0.0)
        
        # Element complexity affects success
        success_probability -= element.complexity * 0.3
        
        # Relationship bonus
        if hasattr(transmitter, 'relationships') and receiver.name in transmitter.relationships:
            relationship = transmitter.relationships[receiver.name]
            if relationship in ["family", "friend", "mentor"]:
                success_probability += self.transmission_factors["relationship_bonus"]
        
        # Family bonus
        if (hasattr(transmitter, 'family') and hasattr(receiver, 'family') and
            any(name in receiver.family.get('parents', []) for name in [transmitter.name]) or
            any(name in transmitter.family.get('children', []) for name in [receiver.name])):
            success_probability += self.transmission_factors["family_bonus"]
        
        # Age gap penalty
        age_gap = abs(transmitter.age - receiver.age)
        success_probability -= (age_gap // 10) * self.transmission_factors["age_gap_penalty"]
        
        # Skill matching bonus
        if element.associated_skills:
            for skill in element.associated_skills:
                if (hasattr(transmitter, 'skills') and hasattr(receiver, 'skills') and
                    skill in transmitter.skills and skill in receiver.skills):
                    success_probability += self.transmission_factors["skill_match_bonus"] / len(element.associated_skills)
        
        # Final success check
        success = random.random() < max(0.1, min(0.9, success_probability))
        
        if success:
            # Calculate fidelity (how accurately the culture is transmitted)
            fidelity = random.uniform(0.6, 1.0)
            
            # Update receiver's cultural knowledge
            element.knowledge_bearers.add(receiver.name)
            
            # Record transmission event
            self.transmission_events.append(CulturalTransmissionEvent(
                transmitter=transmitter.name,
                receiver=receiver.name,
                cultural_element=element.id,
                transmission_type=transmission_type,
                success=True,
                fidelity=fidelity,
                day=current_day,
                generation_gap=abs(self._determine_agent_generation(transmitter, current_day) - 
                                 self._determine_agent_generation(receiver, current_day))
            ))
            
            # Add memory to receiver
            receiver.memory.store_memory(
                f"Learned {element.name} from {transmitter.name}",
                importance=element.importance * 0.7,
                memory_type="cultural"
            )
        
        return success
    
    def _get_agent_cultural_knowledge(self, agent: Any) -> Dict[str, float]:
        """Get an agent's cultural knowledge levels."""
        # This would be stored on the agent or in a separate system
        # For now, check if agent is in knowledge bearers
        culture_levels = {}
        for culture_id, element in self.cultural_elements.items():
            if agent.name in element.knowledge_bearers:
                culture_levels[culture_id] = random.uniform(0.6, 1.0)  # Assume good knowledge
        return culture_levels
    
    def _process_cultural_evolution(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process evolution of cultural elements."""
        evolution_events = []
        
        # Innovation: Creating new cultural elements
        if random.random() < 0.01:  # 1% chance per day
            innovator = random.choice([a for a in agents if a.is_alive])
            new_element = self._create_cultural_innovation(innovator, current_day)
            if new_element:
                evolution_events.append({
                    "type": "cultural_innovation",
                    "innovator": innovator.name,
                    "new_element": new_element.name,
                    "culture_type": new_element.culture_type.value,
                    "day": current_day
                })
        
        # Adaptation: Modifying existing cultural elements
        for element in list(self.cultural_elements.values()):
            if element.adaptability > 0.5 and random.random() < 0.005:  # 0.5% chance
                adaptation_event = self._adapt_cultural_element(element, agents, current_day)
                if adaptation_event:
                    evolution_events.append(adaptation_event)
        
        return evolution_events
    
    def _create_cultural_innovation(self, innovator: Any, current_day: int) -> Optional[CulturalElement]:
        """Create a new cultural element through innovation."""
        # Choose type of innovation based on innovator's traits and skills
        innovation_types = list(CultureType)
        
        # Weight based on agent characteristics
        if hasattr(innovator, 'skills'):
            if innovator.skills.get('artistry', 0) > 0.7:
                innovation_types.extend([CultureType.ARTS, CultureType.STORIES])
            if innovator.skills.get('social', 0) > 0.7:
                innovation_types.extend([CultureType.CUSTOMS, CultureType.TRADITIONS])
            if innovator.skills.get('spiritual', 0) > 0.7:
                innovation_types.extend([CultureType.RITUALS, CultureType.VALUES])
        
        culture_type = random.choice(innovation_types)
        
        # Generate new cultural element
        element_id = f"innovation_{current_day}_{innovator.name.lower()}"
        
        innovation_names = {
            CultureType.VALUES: ["New Life Philosophy", "Community Principle", "Moral Teaching"],
            CultureType.TRADITIONS: ["Seasonal Festival", "Coming of Age Ceremony", "Harvest Ritual"],
            CultureType.KNOWLEDGE: ["Craft Technique", "Survival Method", "Healing Practice"],
            CultureType.STORIES: ["Hero Tale", "Creation Myth", "Moral Fable"],
            CultureType.CUSTOMS: ["Social Greeting", "Dining Etiquette", "Work Practice"],
            CultureType.ARTS: ["Dance Form", "Song Style", "Craft Pattern"],
            CultureType.RITUALS: ["Blessing Ceremony", "Purification Rite", "Memory Honoring"]
        }
        
        name = random.choice(innovation_names.get(culture_type, ["New Cultural Practice"]))
        
        new_element = CulturalElement(
            id=element_id,
            name=f"{innovator.name}'s {name}",
            culture_type=culture_type,
            description=f"A new {culture_type.value} created by {innovator.name}",
            origin_generation=self._determine_agent_generation(innovator, current_day),
            current_generation=self._determine_agent_generation(innovator, current_day),
            knowledge_bearers={innovator.name},
            transmission_methods=[TransmissionType.PEER_TO_PEER, TransmissionType.OBSERVATION],
            complexity=random.uniform(0.3, 0.8),
            importance=random.uniform(0.2, 0.6),  # Starts with lower importance
            adaptability=random.uniform(0.6, 0.9),  # New elements are more adaptable
            preservation_rate=random.uniform(0.4, 0.7),  # Lower initial preservation
            evolution_history=[{
                "type": "creation",
                "day": current_day,
                "agent": innovator.name,
                "description": "Initial creation"
            }],
            associated_skills=[],
            prerequisites=[]
        )
        
        self.cultural_elements[element_id] = new_element
        
        # Add memory to innovator
        innovator.memory.store_memory(
            f"Created new cultural practice: {new_element.name}",
            importance=0.8,
            memory_type="achievement"
        )
        
        return new_element
    
    def _adapt_cultural_element(self, element: CulturalElement, agents: List[Any], 
                              current_day: int) -> Optional[Dict[str, Any]]:
        """Adapt an existing cultural element to current circumstances."""
        if not element.knowledge_bearers:
            return None
        
        # Find an agent who knows this culture to lead the adaptation
        adapters = [a for a in agents if a.is_alive and a.name in element.knowledge_bearers]
        if not adapters:
            return None
        
        adapter = random.choice(adapters)
        
        # Types of adaptation
        adaptation_types = ["simplification", "elaboration", "modernization", "localization"]
        adaptation_type = random.choice(adaptation_types)
        
        # Apply adaptation
        old_complexity = element.complexity
        old_importance = element.importance
        
        if adaptation_type == "simplification":
            element.complexity = max(0.1, element.complexity - random.uniform(0.1, 0.3))
            element.preservation_rate += 0.1
        elif adaptation_type == "elaboration":
            element.complexity = min(1.0, element.complexity + random.uniform(0.1, 0.2))
            element.importance += 0.1
        elif adaptation_type == "modernization":
            element.adaptability = min(1.0, element.adaptability + 0.1)
            element.preservation_rate = max(0.3, element.preservation_rate - 0.05)
        elif adaptation_type == "localization":
            element.preservation_rate += 0.05
            element.importance += 0.05
        
        # Record evolution
        element.evolution_history.append({
            "type": adaptation_type,
            "day": current_day,
            "adapter": adapter.name,
            "changes": f"Complexity: {old_complexity:.2f} -> {element.complexity:.2f}, "
                      f"Importance: {old_importance:.2f} -> {element.importance:.2f}"
        })
        
        return {
            "type": "cultural_adaptation",
            "adapter": adapter.name,
            "cultural_element": element.name,
            "adaptation_type": adaptation_type,
            "day": current_day
        }
    
    def _process_cultural_preservation(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process cultural preservation and potential loss."""
        preservation_events = []
        
        for element in list(self.cultural_elements.values()):
            # Check if element has enough active bearers
            active_bearers = [name for name in element.knowledge_bearers 
                            if any(a.name == name and a.is_alive for a in agents)]
            
            # Update active bearers
            element.knowledge_bearers = set(active_bearers)
            
            # Risk of cultural loss
            if len(active_bearers) <= 1:  # Critical preservation risk
                loss_probability = 0.1 if len(active_bearers) == 1 else 0.3
                
                if random.random() < loss_probability:
                    # Cultural element is in danger or lost
                    if len(active_bearers) == 0:
                        preservation_events.append({
                            "type": "cultural_loss",
                            "cultural_element": element.name,
                            "reason": "no_remaining_bearers",
                            "day": current_day
                        })
                        # Mark for removal (don't remove during iteration)
                        element.preservation_rate = 0.0
                    else:
                        preservation_events.append({
                            "type": "cultural_endangerment",
                            "cultural_element": element.name,
                            "remaining_bearers": active_bearers,
                            "day": current_day
                        })
            
            # Preservation efforts
            elif len(active_bearers) >= 3 and element.importance > 0.7:
                # Strong cultural elements with multiple bearers may gain preservation strength
                if random.random() < 0.05:  # 5% chance
                    element.preservation_rate = min(1.0, element.preservation_rate + 0.05)
                    preservation_events.append({
                        "type": "cultural_strengthening",
                        "cultural_element": element.name,
                        "bearers": len(active_bearers),
                        "day": current_day
                    })
        
        # Remove lost cultural elements
        lost_elements = [eid for eid, element in self.cultural_elements.items() 
                        if element.preservation_rate <= 0.0]
        for eid in lost_elements:
            del self.cultural_elements[eid]
        
        return preservation_events
    
    def get_cultural_summary(self) -> Dict[str, Any]:
        """Get comprehensive cultural transmission summary."""
        total_elements = len(self.cultural_elements)
        elements_by_type = {}
        for culture_type in CultureType:
            count = len([e for e in self.cultural_elements.values() if e.culture_type == culture_type])
            elements_by_type[culture_type.value] = count
        
        active_bearers = set()
        for element in self.cultural_elements.values():
            active_bearers.update(element.knowledge_bearers)
        
        return {
            "total_cultural_elements": total_elements,
            "elements_by_type": elements_by_type,
            "total_transmission_events": len(self.transmission_events),
            "active_cultural_bearers": len(active_bearers),
            "generations_tracked": len(self.generations),
            "cultural_diversity": self._calculate_cultural_diversity(),
            "preservation_status": self._assess_preservation_status()
        }
    
    def _calculate_cultural_diversity(self) -> float:
        """Calculate cultural diversity score."""
        if not self.cultural_elements:
            return 0.0
        
        # Diversity based on number of different types and their distribution
        type_counts = {}
        for element in self.cultural_elements.values():
            type_counts[element.culture_type] = type_counts.get(element.culture_type, 0) + 1
        
        # Shannon diversity index
        total = len(self.cultural_elements)
        diversity = 0.0
        for count in type_counts.values():
            if count > 0:
                proportion = count / total
                diversity -= proportion * (proportion ** 0.5)  # Simplified Shannon index
        
        return min(1.0, diversity)
    
    def _assess_preservation_status(self) -> str:
        """Assess overall cultural preservation status."""
        if not self.cultural_elements:
            return "no_culture"
        
        endangered_count = len([e for e in self.cultural_elements.values() 
                              if len(e.knowledge_bearers) <= 1])
        total_count = len(self.cultural_elements)
        
        if endangered_count == 0:
            return "well_preserved"
        elif endangered_count < total_count * 0.2:
            return "mostly_preserved"
        elif endangered_count < total_count * 0.5:
            return "at_risk"
        else:
            return "critically_endangered" 