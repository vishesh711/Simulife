"""
Love & Romance System for SimuLife
Enables agents to experience romantic attraction, courtship, marriage, and family formation
with authentic human-like emotional depth and cultural variation.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import math


class RelationshipStatus(Enum):
    """Stages of romantic relationships."""
    SINGLE = "single"
    ATTRACTED = "attracted"           # One-sided attraction
    MUTUAL_ATTRACTION = "mutual_attraction"  # Both interested
    COURTING = "courting"            # Active courtship phase
    DATING = "dating"                # Established romantic relationship
    ENGAGED = "engaged"              # Committed to marriage
    MARRIED = "married"              # Formal partnership
    SEPARATED = "separated"          # Relationship troubles
    DIVORCED = "divorced"            # Former marriage ended
    WIDOWED = "widowed"              # Partner deceased


class CourtshipStyle(Enum):
    """Different approaches to romantic courtship."""
    ARTISTIC_EXPRESSION = "artistic_expression"      # Through art, music, poetry
    INTELLECTUAL_CONNECTION = "intellectual_connection"  # Deep conversations
    PHYSICAL_PROWESS = "physical_prowess"            # Athletic displays
    SPIRITUAL_BONDING = "spiritual_bonding"          # Shared spiritual experiences
    PRACTICAL_PARTNERSHIP = "practical_partnership"  # Demonstrating usefulness
    GIFT_GIVING = "gift_giving"                      # Presents and tokens
    PROTECTIVE_DISPLAY = "protective_display"        # Showing protective abilities
    HUMOR_AND_CHARM = "humor_and_charm"             # Making partner laugh


class LoveLanguage(Enum):
    """How agents express and receive love."""
    WORDS_OF_AFFIRMATION = "words_of_affirmation"
    ACTS_OF_SERVICE = "acts_of_service"
    RECEIVING_GIFTS = "receiving_gifts"
    QUALITY_TIME = "quality_time"
    PHYSICAL_TOUCH = "physical_touch"


@dataclass
class RomanticAttraction:
    """Represents romantic feelings between two agents."""
    agent_name: str
    target_name: str
    attraction_strength: float         # 0.0-1.0 intensity of feelings
    started_day: int
    attraction_type: str               # physical, emotional, intellectual, spiritual
    compatibility_score: float        # How well matched they are
    reciprocated: bool                 # Is the feeling mutual?
    status: RelationshipStatus
    
    # Attraction factors
    physical_attraction: float
    personality_attraction: float
    intellectual_attraction: float
    spiritual_attraction: float
    social_attraction: float
    
    # Relationship progression
    courtship_attempts: int
    successful_interactions: int
    failed_interactions: int
    relationship_milestones: List[str]


@dataclass
class RomanticRelationship:
    """Represents an active romantic relationship."""
    id: str
    partner1: str
    partner2: str
    started_day: int
    
    # Relationship dynamics
    status: RelationshipStatus
    love_intensity: float              # 0.0-1.0 depth of love
    compatibility: float               # How well they work together
    passion: float                     # Physical/romantic attraction
    intimacy: float                    # Emotional closeness
    commitment: float                  # Dedication to relationship
    
    # Relationship health
    satisfaction: float                # Overall happiness
    conflict_level: float              # Amount of disagreement
    trust_level: float                 # Faith in each other
    communication_quality: float      # How well they communicate
    
    # Shared experiences
    shared_activities: List[str]
    shared_memories: List[Dict[str, Any]]
    relationship_traditions: List[str]
    future_plans: List[str]
    
    # Cultural elements
    courtship_style: CourtshipStyle
    cultural_traditions: List[str]
    family_approval: Dict[str, float]  # family_member -> approval_level
    
    # Marriage planning
    engagement_day: Optional[int]
    wedding_planned: bool
    wedding_style: Optional[str]
    wedding_day: Optional[int]


@dataclass
class MarriageEvent:
    """Represents a marriage ceremony and its cultural significance."""
    couple: Tuple[str, str]
    wedding_day: int
    ceremony_location: str
    ceremony_style: str                # Cultural variation
    
    # Ceremony details
    officiant: Optional[str]           # Who performed ceremony
    witnesses: List[str]               # Family and friends present
    vows_exchanged: List[str]          # Personal promises made
    cultural_rituals: List[str]        # Traditional ceremony elements
    
    # Social impact
    community_celebration: bool
    gifts_received: List[Dict[str, Any]]
    family_traditions_merged: List[str]
    new_household_established: bool
    
    # Aftermath
    honeymoon_activities: List[str]
    marriage_satisfaction_initial: float
    social_status_change: Dict[str, float]


class LoveRomanceSystem:
    """
    Manages romantic relationships, love, courtship, and marriage across the agent population.
    """
    
    def __init__(self):
        self.romantic_attractions: Dict[str, List[RomanticAttraction]] = defaultdict(list)
        self.active_relationships: Dict[str, RomanticRelationship] = {}
        self.marriage_history: List[MarriageEvent] = []
        self.courtship_traditions: Dict[str, List[CourtshipStyle]] = {}
        
        # System tracking
        self.love_stories: List[Dict[str, Any]] = []
        self.heartbreak_events: List[Dict[str, Any]] = []
        self.romance_statistics: Dict[str, Any] = {}
        
        # Cultural variation
        self.cultural_courtship_styles: Dict[str, List[CourtshipStyle]] = {}
        self.marriage_traditions: Dict[str, Dict[str, Any]] = {}
        self.relationship_values: Dict[str, List[str]] = {}
        
        # Configuration
        self.attraction_base_chance = 0.1          # Base chance per day of attraction
        self.compatibility_threshold = 0.6        # Minimum for romantic interest
        self.courtship_success_rate = 0.3         # Base courtship success chance
        self.marriage_readiness_age = 18          # Minimum age for marriage
        self.relationship_decay_rate = 0.05       # How fast relationships can deteriorate
        
        # Initialize cultural defaults
        self._initialize_cultural_defaults()
    
    def _initialize_cultural_defaults(self):
        """Set up default cultural approaches to romance and marriage."""
        # Default courtship styles - different cultures will develop preferences
        self.cultural_courtship_styles["default"] = [
            CourtshipStyle.ARTISTIC_EXPRESSION,
            CourtshipStyle.INTELLECTUAL_CONNECTION,
            CourtshipStyle.GIFT_GIVING,
            CourtshipStyle.HUMOR_AND_CHARM
        ]
        
        # Default marriage traditions
        self.marriage_traditions["default"] = {
            "ceremony_style": "community_gathering",
            "vow_requirements": True,
            "witness_count_min": 2,
            "celebration_duration": 3,  # days
            "gift_giving_expected": True,
            "family_approval_required": False,
            "honeymoon_tradition": True
        }
    
    def process_daily_romantic_development(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process all romantic developments for a single day."""
        events = []
        
        # Phase 1: New romantic attractions
        attraction_events = self._process_new_attractions(agents, current_day)
        events.extend(attraction_events)
        
        # Phase 2: Courtship activities
        courtship_events = self._process_courtship_activities(agents, current_day)
        events.extend(courtship_events)
        
        # Phase 3: Relationship progression
        progression_events = self._process_relationship_progression(agents, current_day)
        events.extend(progression_events)
        
        # Phase 4: Marriage proposals and ceremonies
        marriage_events = self._process_marriage_activities(agents, current_day)
        events.extend(marriage_events)
        
        # Phase 5: Relationship maintenance and challenges
        maintenance_events = self._process_relationship_maintenance(agents, current_day)
        events.extend(maintenance_events)
        
        # Phase 6: Family planning and reproduction
        reproduction_events = self._process_family_planning(agents, current_day)
        events.extend(reproduction_events)
        
        # Update statistics
        self._update_romance_statistics(agents, current_day)
        
        return events
    
    def _process_new_attractions(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle formation of new romantic attractions."""
        events = []
        
        eligible_agents = [a for a in agents if a.is_alive and a.age >= 16]
        
        for agent in eligible_agents:
            # Skip if already in committed relationship
            if hasattr(agent, 'relationship_status') and agent.relationship_status in [
                RelationshipStatus.MARRIED, RelationshipStatus.ENGAGED, RelationshipStatus.DATING
            ]:
                continue
            
            # Daily chance for romantic attraction
            if random.random() < self.attraction_base_chance:
                potential_partners = self._find_potential_romantic_partners(agent, eligible_agents)
                
                if potential_partners:
                    # Select most compatible potential partner
                    target_agent, compatibility = potential_partners[0]
                    
                    # Create attraction
                    attraction = self._create_romantic_attraction(agent, target_agent, compatibility, current_day)
                    self.romantic_attractions[agent.name].append(attraction)
                    
                    # Update agent emotional state
                    if hasattr(agent, 'emotional_profile'):
                        agent.emotional_profile["complex_emotions"]["romantic_love"] += attraction.attraction_strength * 0.3
                        agent.emotional_profile["primary_emotions"]["anticipation"] += 0.2
                    
                    # Create memory
                    agent.memory.store_memory(
                        f"I'm developing feelings for {target_agent.name}. There's something special about them that draws me in.",
                        importance=0.8,
                        emotion="romantic_attraction",
                        memory_type="romantic"
                    )
                    
                    events.append({
                        "type": "romantic_attraction_formed",
                        "agent": agent.name,
                        "target": target_agent.name,
                        "attraction_strength": attraction.attraction_strength,
                        "compatibility": compatibility,
                        "attraction_type": attraction.attraction_type,
                        "day": current_day
                    })
        
        return events
    
    def _find_potential_romantic_partners(self, agent: Any, all_agents: List[Any]) -> List[Tuple[Any, float]]:
        """Find agents that could be romantic partners."""
        potential_partners = []
        
        for other_agent in all_agents:
            if (other_agent != agent and 
                other_agent.is_alive and
                not self._are_closely_related(agent, other_agent) and
                self._age_compatible(agent, other_agent)):
                
                try:
                    compatibility = self._calculate_romantic_compatibility(agent, other_agent)
                    
                    if compatibility >= self.compatibility_threshold:
                        potential_partners.append((other_agent, compatibility))
                except Exception as e:
                    # Skip this agent if compatibility calculation fails
                    print(f"Warning: Could not calculate compatibility between {agent.name} and {other_agent.name}: {e}")
                    continue
        
        # Sort by compatibility
        potential_partners.sort(key=lambda x: x[1], reverse=True)
        return potential_partners[:3]  # Top 3 most compatible
    
    def _calculate_romantic_compatibility(self, agent1: Any, agent2: Any) -> float:
        """Calculate comprehensive romantic compatibility between two agents."""
        compatibility = 0.0
        
        # Personality compatibility
        personality_compat = self._calculate_personality_compatibility(agent1, agent2)
        compatibility += personality_compat * 0.3
        
        # Age compatibility (prefer similar ages)
        age_diff = abs(agent1.age - agent2.age)
        age_compat = max(0, 1.0 - (age_diff / 20.0))  # Decreases with age difference
        compatibility += age_compat * 0.2
        
        # Shared interests and values
        shared_interests = self._calculate_shared_interests(agent1, agent2)
        compatibility += shared_interests * 0.2
        
        # Physical attraction (based on traits and preferences)
        physical_compat = self._calculate_physical_attraction(agent1, agent2)
        compatibility += physical_compat * 0.15
        
        # Social status compatibility
        social_compat = self._calculate_social_compatibility(agent1, agent2)
        compatibility += social_compat * 0.1
        
        # Random chemistry factor
        chemistry = random.uniform(0.0, 0.05)
        compatibility += chemistry
        
        return min(1.0, compatibility)
    
    def _create_romantic_attraction(self, agent: Any, target: Any, compatibility: float, current_day: int) -> RomanticAttraction:
        """Create a romantic attraction between two agents."""
        attraction_strength = compatibility * random.uniform(0.7, 1.0)
        
        # Determine attraction type based on agent personalities
        attraction_types = []
        if agent.personality_scores.get("openness", 0.5) > 0.7:
            attraction_types.append("intellectual")
        if agent.personality_scores.get("extraversion", 0.5) > 0.6:
            attraction_types.append("social")
        if "spiritual" in agent.traits:
            attraction_types.append("spiritual")
        attraction_types.append("physical")  # Always present
        
        primary_attraction_type = random.choice(attraction_types)
        
        return RomanticAttraction(
            agent_name=agent.name,
            target_name=target.name,
            attraction_strength=attraction_strength,
            started_day=current_day,
            attraction_type=primary_attraction_type,
            compatibility_score=compatibility,
            reciprocated=False,  # Will be determined later
            status=RelationshipStatus.ATTRACTED,
            physical_attraction=random.uniform(0.4, 1.0),
            personality_attraction=compatibility,
            intellectual_attraction=self._calculate_intellectual_attraction(agent, target),
            spiritual_attraction=self._calculate_spiritual_attraction(agent, target),
            social_attraction=self._calculate_social_attraction(agent, target),
            courtship_attempts=0,
            successful_interactions=0,
            failed_interactions=0,
            relationship_milestones=[]
        )
    
    def _process_courtship_activities(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle courtship attempts and romantic interactions."""
        events = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
                
            # Check if agent has romantic attractions to pursue
            agent_attractions = self.romantic_attractions.get(agent.name, [])
            
            for attraction in agent_attractions:
                if attraction.status == RelationshipStatus.ATTRACTED:
                    # Attempt courtship activity
                    target_agent = self._get_agent_by_name(agents, attraction.target_name)
                    if target_agent and target_agent.is_alive:
                        
                        courtship_event = self._attempt_courtship_activity(
                            agent, target_agent, attraction, current_day
                        )
                        
                        if courtship_event:
                            events.append(courtship_event)
        
        return events
    
    def _attempt_courtship_activity(self, courting_agent: Any, target_agent: Any, 
                                  attraction: RomanticAttraction, current_day: int) -> Optional[Dict[str, Any]]:
        """Agent attempts to court their romantic interest."""
        # Determine courtship style based on agent personality and culture
        courtship_style = self._select_courtship_style(courting_agent)
        
        # Calculate success chance based on compatibility and approach
        base_success_chance = self.courtship_success_rate
        compatibility_bonus = attraction.compatibility_score * 0.3
        personality_bonus = self._calculate_courtship_personality_bonus(courting_agent, courtship_style)
        
        success_chance = base_success_chance + compatibility_bonus + personality_bonus
        
        # Attempt courtship
        if random.random() < success_chance:
            # Successful courtship activity
            attraction.successful_interactions += 1
            attraction.courtship_attempts += 1
            
            # Create positive memory for both agents
            courting_agent.memory.store_memory(
                f"I had a wonderful time with {target_agent.name} today. Our connection grows stronger.",
                importance=0.7,
                emotion="joy",
                memory_type="romantic"
            )
            
            target_agent.memory.store_memory(
                f"{courting_agent.name} made me feel special today. I'm starting to see them differently.",
                importance=0.6,
                emotion="happiness",
                memory_type="romantic"
            )
            
            # Check if target becomes interested
            if not attraction.reciprocated and attraction.successful_interactions >= 2:
                if random.random() < attraction.compatibility_score:
                    attraction.reciprocated = True
                    attraction.status = RelationshipStatus.MUTUAL_ATTRACTION
                    
                    # Create mutual romantic relationship
                    relationship = self._create_romantic_relationship(
                        courting_agent, target_agent, attraction, current_day
                    )
                    self.active_relationships[relationship.id] = relationship
            
            return {
                "type": "successful_courtship",
                "courting_agent": courting_agent.name,
                "target_agent": target_agent.name,
                "courtship_style": courtship_style.value,
                "interaction_count": attraction.successful_interactions,
                "reciprocated": attraction.reciprocated,
                "day": current_day
            }
        else:
            # Failed courtship attempt
            attraction.failed_interactions += 1
            attraction.courtship_attempts += 1
            
            # Create disappointed memory
            courting_agent.memory.store_memory(
                f"My attempt to connect with {target_agent.name} didn't go as hoped. Perhaps I need a different approach.",
                importance=0.5,
                emotion="disappointment",
                memory_type="romantic"
            )
            
            return {
                "type": "failed_courtship",
                "courting_agent": courting_agent.name,
                "target_agent": target_agent.name,
                "courtship_style": courtship_style.value,
                "attempt_count": attraction.courtship_attempts,
                "day": current_day
            }
    
    def _create_romantic_relationship(self, agent1: Any, agent2: Any, 
                                    attraction: RomanticAttraction, current_day: int) -> RomanticRelationship:
        """Create a formal romantic relationship between two agents."""
        relationship_id = f"{agent1.name}_{agent2.name}_{current_day}"
        
        # Determine courtship style for the relationship
        courtship_style = self._select_courtship_style(agent1)
        
        relationship = RomanticRelationship(
            id=relationship_id,
            partner1=agent1.name,
            partner2=agent2.name,
            started_day=current_day,
            status=RelationshipStatus.DATING,
            love_intensity=attraction.attraction_strength * 0.6,  # Starts moderate
            compatibility=attraction.compatibility_score,
            passion=attraction.physical_attraction,
            intimacy=0.4,  # Builds over time
            commitment=0.3,  # Low initially
            satisfaction=0.7,  # Generally happy at start
            conflict_level=0.1,  # Minimal conflict early
            trust_level=0.6,  # Moderate trust
            communication_quality=0.5,  # Average initially
            shared_activities=[],
            shared_memories=[],
            relationship_traditions=[],
            future_plans=[],
            courtship_style=courtship_style,
            cultural_traditions=[],
            family_approval={},
            engagement_day=None,
            wedding_planned=False,
            wedding_style=None,
            wedding_day=None
        )
        
        # Update agent relationship statuses
        agent1.relationship_status = RelationshipStatus.DATING
        agent2.relationship_status = RelationshipStatus.DATING
        agent1.romantic_partner = agent2.name
        agent2.romantic_partner = agent1.name
        
        return relationship
    
    def _process_family_planning(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle family planning and reproduction for married couples."""
        events = []
        
        # Find married couples
        married_couples = self._get_married_couples(agents)
        
        for couple in married_couples:
            agent1, agent2 = couple
            
            # Check if couple wants children
            if (self._couple_wants_children(agent1, agent2) and
                self._couple_can_have_children(agent1, agent2)):
                
                # Attempt conception based on various factors
                conception_chance = self._calculate_conception_chance(agent1, agent2)
                
                if random.random() < conception_chance:
                    # Successful conception
                    pregnancy_event = self._create_pregnancy(agent1, agent2, current_day)
                    events.append(pregnancy_event)
        
        return events
    
    def _create_pregnancy(self, parent1: Any, parent2: Any, current_day: int) -> Dict[str, Any]:
        """Create pregnancy and schedule birth."""
        # Determine which parent carries the pregnancy (in this simulation, could be either)
        carrying_parent = random.choice([parent1, parent2])
        other_parent = parent2 if carrying_parent == parent1 else parent1
        
        # Schedule birth for 9 months (270 days) later
        expected_birth_day = current_day + 270
        
        # Create pregnancy record
        pregnancy = {
            "parents": [parent1.name, parent2.name],
            "carrying_parent": carrying_parent.name,
            "conception_day": current_day,
            "expected_birth_day": expected_birth_day,
            "pregnancy_id": f"{parent1.name}_{parent2.name}_{current_day}"
        }
        
        # Add pregnancy to world state for tracking
        if not hasattr(carrying_parent, 'pregnancies'):
            carrying_parent.pregnancies = []
        carrying_parent.pregnancies.append(pregnancy)
        
        # Create memories for both parents
        carrying_parent.memory.store_memory(
            f"I'm going to have a child with {other_parent.name}! This changes everything - we're going to be parents.",
            importance=1.0,
            emotion="joy",
            memory_type="life_milestone"
        )
        
        other_parent.memory.store_memory(
            f"{carrying_parent.name} and I are expecting a child! I feel a mix of excitement and responsibility.",
            importance=1.0,
            emotion="anticipation",
            memory_type="life_milestone"
        )
        
        return {
            "type": "pregnancy_announcement",
            "parents": [parent1.name, parent2.name],
            "carrying_parent": carrying_parent.name,
            "expected_birth": expected_birth_day,
            "conception_day": current_day
        }
    
    # Helper methods for compatibility calculations
    def _calculate_personality_compatibility(self, agent1: Any, agent2: Any) -> float:
        """Calculate personality-based compatibility."""
        compatibility = 0.0
        
        # Some personality traits work well together
        extraversion_diff = abs(agent1.personality_scores.get("extraversion", 0.5) - 
                              agent2.personality_scores.get("extraversion", 0.5))
        
        # Similar extraversion levels work well
        if extraversion_diff < 0.3:
            compatibility += 0.3
        
        # Complementary traits (one organized, one flexible can work)
        conscientiousness_diff = abs(agent1.personality_scores.get("conscientiousness", 0.5) - 
                                   agent2.personality_scores.get("conscientiousness", 0.5))
        if 0.3 < conscientiousness_diff < 0.7:  # Some difference but not extreme
            compatibility += 0.2
        
        # Shared agreeableness helps
        agreeableness_avg = (agent1.personality_scores.get("agreeableness", 0.5) + 
                           agent2.personality_scores.get("agreeableness", 0.5)) / 2
        compatibility += agreeableness_avg * 0.3
        
        return min(1.0, compatibility)
    
    def _calculate_shared_interests(self, agent1: Any, agent2: Any) -> float:
        """Calculate compatibility based on shared interests and goals."""
        try:
            # Compare traits
            agent1_traits = set(getattr(agent1, 'traits', []))
            agent2_traits = set(getattr(agent2, 'traits', []))
            shared_traits = len(agent1_traits & agent2_traits)
            total_traits = len(agent1_traits | agent2_traits)
            
            if total_traits > 0:
                trait_similarity = shared_traits / total_traits
            else:
                trait_similarity = 0.5
            
            # Compare goals if available
            goal_similarity = 0.5  # Default
            if hasattr(agent1, 'goals') and hasattr(agent2, 'goals'):
                agent1_goals = set(getattr(agent1, 'goals', []))
                agent2_goals = set(getattr(agent2, 'goals', []))
                shared_goals = len(agent1_goals & agent2_goals)
                total_goals = len(agent1_goals | agent2_goals)
                
                if total_goals > 0:
                    goal_similarity = shared_goals / total_goals
            
            return (trait_similarity + goal_similarity) / 2
        except Exception as e:
            # Return neutral compatibility if calculation fails
            return 0.5
    
    def _calculate_physical_attraction(self, agent1: Any, agent2: Any) -> float:
        """Calculate physical attraction (simplified for this simulation)."""
        # In a more complex simulation, this could factor in physical traits
        # For now, use personality and random factors
        base_attraction = random.uniform(0.3, 0.8)
        
        # Agents with higher openness might be more physically attracted to diverse partners
        openness_factor = agent1.personality_scores.get("openness", 0.5) * 0.2
        
        return min(1.0, base_attraction + openness_factor)
    
    def _calculate_social_compatibility(self, agent1: Any, agent2: Any) -> float:
        """Calculate social status and background compatibility."""
        # For now, simplified - could include reputation, social group membership, etc.
        
        rep_diff = abs(agent1.reputation - agent2.reputation)
        rep_compatibility = max(0, 1.0 - rep_diff)
        
        # Location compatibility (same location = higher compatibility)
        location_compatibility = 1.0 if agent1.location == agent2.location else 0.7
        
        return (rep_compatibility + location_compatibility) / 2
    
    def _are_closely_related(self, agent1: Any, agent2: Any) -> bool:
        """Check if two agents are too closely related for romance."""
        # Check if they're siblings
        if (hasattr(agent1, 'family') and hasattr(agent2, 'family')):
            if agent2.name in agent1.family.get('siblings', []):
                return True
            if agent1.name in agent2.family.get('siblings', []):
                return True
            
            # Check if they're parent-child
            if agent2.name in agent1.family.get('parents', []):
                return True
            if agent1.name in agent2.family.get('parents', []):
                return True
            if agent2.name in agent1.family.get('children', []):
                return True
            if agent1.name in agent2.family.get('children', []):
                return True
        
        return False
    
    def _age_compatible(self, agent1: Any, agent2: Any) -> bool:
        """Check if agents are age-compatible for romance."""
        age_diff = abs(agent1.age - agent2.age)
        
        # Both must be adults
        if agent1.age < 16 or agent2.age < 16:
            return False
        
        # Maximum age difference of 15 years
        if age_diff > 15:
            return False
        
        return True
    
    def _get_agent_by_name(self, agents: List[Any], name: str) -> Optional[Any]:
        """Find agent by name in list."""
        for agent in agents:
            if agent.name == name:
                return agent
        return None
    
    def _select_courtship_style(self, agent: Any) -> CourtshipStyle:
        """Select appropriate courtship style based on agent personality."""
        # Base selection on personality traits
        if "creative" in agent.traits or "artistic" in agent.traits:
            return CourtshipStyle.ARTISTIC_EXPRESSION
        elif "intelligent" in agent.traits or agent.personality_scores.get("openness", 0.5) > 0.7:
            return CourtshipStyle.INTELLECTUAL_CONNECTION
        elif "strong" in agent.traits or "athletic" in agent.traits:
            return CourtshipStyle.PHYSICAL_PROWESS
        elif "spiritual" in agent.traits or "wise" in agent.traits:
            return CourtshipStyle.SPIRITUAL_BONDING
        elif agent.personality_scores.get("conscientiousness", 0.5) > 0.7:
            return CourtshipStyle.PRACTICAL_PARTNERSHIP
        elif agent.personality_scores.get("extraversion", 0.5) > 0.7:
            return CourtshipStyle.HUMOR_AND_CHARM
        else:
            return CourtshipStyle.GIFT_GIVING  # Default
    
    def _calculate_courtship_personality_bonus(self, agent: Any, style: CourtshipStyle) -> float:
        """Calculate bonus based on how well courtship style matches personality."""
        bonus = 0.0
        
        if style == CourtshipStyle.ARTISTIC_EXPRESSION and "creative" in agent.traits:
            bonus += 0.2
        elif style == CourtshipStyle.INTELLECTUAL_CONNECTION and agent.personality_scores.get("openness", 0.5) > 0.7:
            bonus += 0.2
        elif style == CourtshipStyle.HUMOR_AND_CHARM and agent.personality_scores.get("extraversion", 0.5) > 0.7:
            bonus += 0.2
        # Add more style-personality matches as needed
        
        return bonus
    
    def _calculate_intellectual_attraction(self, agent1: Any, agent2: Any) -> float:
        """Calculate intellectual compatibility."""
        # Compare intelligence levels and openness
        if hasattr(agent1, 'intelligence') and hasattr(agent2, 'intelligence'):
            intelligence_diff = abs(agent1.intelligence - agent2.intelligence)
            intellectual_compat = max(0, 1.0 - intelligence_diff)
        else:
            intellectual_compat = 0.5
        
        # Factor in openness to experience
        openness_avg = (agent1.personality_scores.get("openness", 0.5) + 
                       agent2.personality_scores.get("openness", 0.5)) / 2
        
        return (intellectual_compat + openness_avg) / 2
    
    def _calculate_spiritual_attraction(self, agent1: Any, agent2: Any) -> float:
        """Calculate spiritual compatibility."""
        spiritual_traits1 = [t for t in agent1.traits if t in ["spiritual", "wise", "philosophical"]]
        spiritual_traits2 = [t for t in agent2.traits if t in ["spiritual", "wise", "philosophical"]]
        
        if spiritual_traits1 and spiritual_traits2:
            return 0.8  # High spiritual attraction
        elif spiritual_traits1 or spiritual_traits2:
            return 0.4  # One spiritual, one not
        else:
            return 0.2  # Neither particularly spiritual
    
    def _calculate_social_attraction(self, agent1: Any, agent2: Any) -> float:
        """Calculate social compatibility and attraction."""
        extraversion_avg = (agent1.personality_scores.get("extraversion", 0.5) + 
                          agent2.personality_scores.get("extraversion", 0.5)) / 2
        
        agreeableness_avg = (agent1.personality_scores.get("agreeableness", 0.5) + 
                           agent2.personality_scores.get("agreeableness", 0.5)) / 2
        
        return (extraversion_avg + agreeableness_avg) / 2
    
    def _get_married_couples(self, agents: List[Any]) -> List[Tuple[Any, Any]]:
        """Get list of married couples from agent population."""
        couples = []
        processed_agents = set()
        
        for agent in agents:
            if (agent.is_alive and 
                agent.name not in processed_agents and
                hasattr(agent, 'relationship_status') and 
                agent.relationship_status == RelationshipStatus.MARRIED and
                hasattr(agent, 'romantic_partner')):
                
                partner_name = agent.romantic_partner
                partner = self._get_agent_by_name(agents, partner_name)
                
                if partner and partner.is_alive:
                    couples.append((agent, partner))
                    processed_agents.add(agent.name)
                    processed_agents.add(partner.name)
        
        return couples
    
    def _couple_wants_children(self, agent1: Any, agent2: Any) -> bool:
        """Determine if a couple wants to have children."""
        # Base chance on age, relationship satisfaction, and personality
        base_desire = 0.3  # 30% base chance
        
        # Age factors
        if 20 <= agent1.age <= 35 and 20 <= agent2.age <= 35:
            base_desire += 0.4  # Prime childbearing years
        elif agent1.age > 40 or agent2.age > 40:
            base_desire -= 0.2  # Older, less likely
        
        # Personality factors
        conscientiousness_avg = (agent1.personality_scores.get("conscientiousness", 0.5) + 
                               agent2.personality_scores.get("conscientiousness", 0.5)) / 2
        base_desire += conscientiousness_avg * 0.2  # Responsible people more likely
        
        # Random factor
        return random.random() < base_desire
    
    def _couple_can_have_children(self, agent1: Any, agent2: Any) -> bool:
        """Check if couple is physically capable of having children."""
        # Both must be alive and of appropriate age
        if not (agent1.is_alive and agent2.is_alive):
            return False
        
        if agent1.age < 16 or agent2.age < 16 or agent1.age > 50 or agent2.age > 50:
            return False
        
        # Check if already pregnant
        if hasattr(agent1, 'pregnancies') and agent1.pregnancies:
            return False
        if hasattr(agent2, 'pregnancies') and agent2.pregnancies:
            return False
        
        return True
    
    def _calculate_conception_chance(self, agent1: Any, agent2: Any) -> float:
        """Calculate chance of conception per day."""
        base_chance = 0.005  # 0.5% per day base chance
        
        # Age factors
        age_avg = (agent1.age + agent2.age) / 2
        if 20 <= age_avg <= 30:
            age_factor = 1.0  # Peak fertility
        elif age_avg < 20:
            age_factor = 0.7  # Young but less fertile
        elif age_avg > 30:
            age_factor = max(0.3, 1.0 - ((age_avg - 30) * 0.05))  # Declining fertility
        else:
            age_factor = 0.5
        
        # Health factors
        health_avg = (agent1.health + agent2.health) / 2
        health_factor = health_avg
        
        # Relationship satisfaction (from active relationship record)
        satisfaction_factor = 1.0  # Default
        for relationship in self.active_relationships.values():
            if ((relationship.partner1 == agent1.name and relationship.partner2 == agent2.name) or
                (relationship.partner1 == agent2.name and relationship.partner2 == agent1.name)):
                satisfaction_factor = relationship.satisfaction
                break
        
        return base_chance * age_factor * health_factor * satisfaction_factor
    
    def _process_relationship_progression(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle progression of existing relationships."""
        events = []
        
        for relationship in list(self.active_relationships.values()):
            agent1 = self._get_agent_by_name(agents, relationship.partner1)
            agent2 = self._get_agent_by_name(agents, relationship.partner2)
            
            if not (agent1 and agent2 and agent1.is_alive and agent2.is_alive):
                continue
            
            # Update relationship over time
            progression_event = self._update_relationship_progression(relationship, agent1, agent2, current_day)
            if progression_event:
                events.append(progression_event)
        
        return events
    
    def _update_relationship_progression(self, relationship: RomanticRelationship, 
                                       agent1: Any, agent2: Any, current_day: int) -> Optional[Dict[str, Any]]:
        """Update a relationship's progression and status."""
        days_together = current_day - relationship.started_day
        
        # Natural relationship progression
        if relationship.status == RelationshipStatus.DATING and days_together > 365:  # 1 year
            if relationship.satisfaction > 0.7 and relationship.commitment > 0.6:
                # Consider engagement
                if random.random() < 0.1:  # 10% chance per check
                    relationship.status = RelationshipStatus.ENGAGED
                    relationship.engagement_day = current_day
                    relationship.commitment += 0.2
                    
                    return {
                        "type": "engagement",
                        "couple": [agent1.name, agent2.name],
                        "engagement_day": current_day,
                        "relationship_duration": days_together
                    }
        
        elif relationship.status == RelationshipStatus.ENGAGED and days_together > 500:  # ~1.5 years
            if relationship.satisfaction > 0.6:
                # Plan wedding
                if not relationship.wedding_planned:
                    relationship.wedding_planned = True
                    relationship.wedding_day = current_day + random.randint(30, 180)  # 1-6 months
                    
                    return {
                        "type": "wedding_planned",
                        "couple": [agent1.name, agent2.name],
                        "wedding_day": relationship.wedding_day
                    }
        
        return None
    
    def _process_marriage_activities(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle marriage ceremonies and wedding events."""
        events = []
        
        for relationship in list(self.active_relationships.values()):
            if (relationship.wedding_planned and 
                relationship.wedding_day and 
                relationship.wedding_day <= current_day):
                
                agent1 = self._get_agent_by_name(agents, relationship.partner1)
                agent2 = self._get_agent_by_name(agents, relationship.partner2)
                
                if agent1 and agent2 and agent1.is_alive and agent2.is_alive:
                    marriage_event = self._conduct_marriage_ceremony(relationship, agent1, agent2, current_day)
                    events.append(marriage_event)
        
        return events
    
    def _conduct_marriage_ceremony(self, relationship: RomanticRelationship, 
                                 agent1: Any, agent2: Any, current_day: int) -> Dict[str, Any]:
        """Conduct a marriage ceremony."""
        # Create marriage event
        marriage = MarriageEvent(
            couple=(agent1.name, agent2.name),
            wedding_day=current_day,
            ceremony_location=agent1.location,  # Default to agent1's location
            ceremony_style="traditional_gathering",
            officiant=None,  # Could select a respected community member
            witnesses=[],  # Would include family and friends
            vows_exchanged=[],
            cultural_rituals=[],
            community_celebration=True,
            gifts_received=[],
            family_traditions_merged=[],
            new_household_established=True,
            honeymoon_activities=[],
            marriage_satisfaction_initial=relationship.satisfaction,
            social_status_change={}
        )
        
        # Update relationship status
        relationship.status = RelationshipStatus.MARRIED
        relationship.commitment = min(1.0, relationship.commitment + 0.3)
        relationship.satisfaction = min(1.0, relationship.satisfaction + 0.2)
        
        # Update agent statuses
        agent1.relationship_status = RelationshipStatus.MARRIED
        agent2.relationship_status = RelationshipStatus.MARRIED
        
        # Create memories
        agent1.memory.store_memory(
            f"Today I married {agent2.name}! This is the beginning of our life together as partners.",
            importance=1.0,
            emotion="joy",
            memory_type="life_milestone"
        )
        
        agent2.memory.store_memory(
            f"{agent1.name} and I are now married! I feel so happy and committed to our future together.",
            importance=1.0,
            emotion="love",
            memory_type="life_milestone"
        )
        
        # Store marriage in history
        self.marriage_history.append(marriage)
        
        return {
            "type": "marriage_ceremony",
            "couple": [agent1.name, agent2.name],
            "wedding_day": current_day,
            "ceremony_location": marriage.ceremony_location,
            "ceremony_style": marriage.ceremony_style,
            "community_celebration": marriage.community_celebration
        }
    
    def _process_relationship_maintenance(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle ongoing relationship maintenance and potential issues."""
        events = []
        
        for relationship in list(self.active_relationships.values()):
            agent1 = self._get_agent_by_name(agents, relationship.partner1)
            agent2 = self._get_agent_by_name(agents, relationship.partner2)
            
            if not (agent1 and agent2 and agent1.is_alive and agent2.is_alive):
                continue
            
            # Random relationship events
            if random.random() < 0.05:  # 5% chance of relationship event per day
                event = self._generate_relationship_event(relationship, agent1, agent2, current_day)
                if event:
                    events.append(event)
        
        return events
    
    def _generate_relationship_event(self, relationship: RomanticRelationship, 
                                   agent1: Any, agent2: Any, current_day: int) -> Optional[Dict[str, Any]]:
        """Generate random relationship events."""
        event_types = ["romantic_gesture", "minor_conflict", "shared_activity", "relationship_milestone"]
        event_type = random.choice(event_types)
        
        if event_type == "romantic_gesture":
            # One partner does something romantic
            giving_partner = random.choice([agent1, agent2])
            receiving_partner = agent2 if giving_partner == agent1 else agent1
            
            relationship.satisfaction = min(1.0, relationship.satisfaction + 0.1)
            relationship.intimacy = min(1.0, relationship.intimacy + 0.05)
            
            return {
                "type": "romantic_gesture",
                "giving_partner": giving_partner.name,
                "receiving_partner": receiving_partner.name,
                "day": current_day
            }
        
        elif event_type == "minor_conflict":
            # Small disagreement
            relationship.conflict_level = min(1.0, relationship.conflict_level + 0.1)
            relationship.satisfaction = max(0.0, relationship.satisfaction - 0.05)
            
            return {
                "type": "relationship_conflict",
                "couple": [agent1.name, agent2.name],
                "severity": "minor",
                "day": current_day
            }
        
        return None
    
    def _update_romance_statistics(self, agents: List[Any], current_day: int):
        """Update system-wide romance statistics."""
        total_agents = len([a for a in agents if a.is_alive])
        single_agents = len([a for a in agents if a.is_alive and 
                           getattr(a, 'relationship_status', RelationshipStatus.SINGLE) == RelationshipStatus.SINGLE])
        dating_agents = len([a for a in agents if a.is_alive and 
                           getattr(a, 'relationship_status', RelationshipStatus.SINGLE) == RelationshipStatus.DATING])
        married_agents = len([a for a in agents if a.is_alive and 
                            getattr(a, 'relationship_status', RelationshipStatus.SINGLE) == RelationshipStatus.MARRIED])
        
        self.romance_statistics = {
            "total_population": total_agents,
            "single_agents": single_agents,
            "dating_agents": dating_agents,
            "married_agents": married_agents,
            "active_relationships": len(self.active_relationships),
            "total_marriages": len(self.marriage_history),
            "single_percentage": (single_agents / total_agents * 100) if total_agents > 0 else 0,
            "married_percentage": (married_agents / total_agents * 100) if total_agents > 0 else 0,
            "last_updated": current_day
        }
    
    def get_agent_romantic_summary(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive romantic summary for an agent."""
        attractions = self.romantic_attractions.get(agent_name, [])
        
        # Find active relationship
        active_relationship = None
        for rel in self.active_relationships.values():
            if rel.partner1 == agent_name or rel.partner2 == agent_name:
                active_relationship = rel
                break
        
        return {
            "current_attractions": [asdict(attr) for attr in attractions],
            "active_relationship": asdict(active_relationship) if active_relationship else None,
            "marriage_history": [asdict(marriage) for marriage in self.marriage_history 
                               if agent_name in marriage.couple],
            "romantic_events_count": len([event for event in self.love_stories 
                                        if event.get("agent") == agent_name])
        }
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get comprehensive romance system summary."""
        return {
            "total_attractions": sum(len(attrs) for attrs in self.romantic_attractions.values()),
            "active_relationships": len(self.active_relationships),
            "total_marriages": len(self.marriage_history),
            "relationship_status_distribution": self.romance_statistics,
            "love_stories_count": len(self.love_stories),
            "heartbreak_events_count": len(self.heartbreak_events)
        } 