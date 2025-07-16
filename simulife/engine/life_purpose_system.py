"""
Life Purpose & Meaning System for SimuLife
Enables agents to discover their unique life calling, develop career aspirations beyond basic specialization,
seek spiritual meaning, and evolve their purpose throughout their lifetime.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict


class PurposeCategory(Enum):
    """Categories of life purpose."""
    CREATOR = "creator"               # Artists, inventors, builders
    PROTECTOR = "protector"           # Guardians, defenders, healers
    TEACHER = "teacher"               # Educators, mentors, guides
    EXPLORER = "explorer"             # Discoverers, pioneers, adventurers
    CAREGIVER = "caregiver"          # Nurturers, supporters, helpers
    LEADER = "leader"                # Organizers, rulers, inspirers
    SCHOLAR = "scholar"              # Researchers, philosophers, thinkers
    CONNECTOR = "connector"          # Diplomats, traders, communicators
    MYSTIC = "mystic"               # Spiritual seekers, visionaries


class PurposeStage(Enum):
    """Stages of purpose development."""
    SEEKING = "seeking"              # Searching for purpose
    EMERGING = "emerging"            # Purpose becoming clear
    COMMITTED = "committed"          # Fully dedicated to purpose
    MASTERY = "mastery"             # Achieving excellence in purpose
    MENTORING = "mentoring"         # Teaching purpose to others
    LEGACY = "legacy"               # Ensuring purpose continues
    TRANSCENDENT = "transcendent"   # Beyond personal purpose


class LifePhase(Enum):
    """Life phases affecting purpose."""
    YOUTH = "youth"                 # 16-25: Exploration
    YOUNG_ADULT = "young_adult"     # 26-35: Establishment  
    ADULT = "adult"                 # 36-50: Achievement
    MIDLIFE = "midlife"            # 51-65: Reflection
    ELDER = "elder"                # 66+: Wisdom


@dataclass
class LifePurpose:
    """Represents an agent's life purpose."""
    agent_name: str
    primary_purpose: PurposeCategory
    purpose_description: str
    discovered_day: int
    
    # Purpose development
    stage: PurposeStage
    commitment_level: float         # 0.0-1.0 how dedicated they are
    fulfillment_level: float        # 0.0-1.0 how fulfilled they feel
    progress: float                 # 0.0-1.0 progress toward mastery
    
    # Supporting elements
    secondary_purposes: List[PurposeCategory]
    career_aspirations: List[str]
    legacy_desires: List[str]
    spiritual_beliefs: Dict[str, Any]
    
    # Evolution tracking
    purpose_evolution: List[Dict[str, Any]]
    major_realizations: List[str]
    obstacles_overcome: List[str]
    mentors: List[str]
    disciples: List[str]


@dataclass
class ExistentialMoment:
    """Represents moments of deep questioning about meaning."""
    agent_name: str
    moment_type: str               # crisis, revelation, questioning, insight
    trigger_event: str
    questions_raised: List[str]
    day: int
    emotional_impact: float
    
    # Resolution
    insights_gained: List[str]
    purpose_change: float          # How much purpose was affected
    spiritual_growth: float        # Spiritual development


@dataclass
class MentorshipRelation:
    """Represents purpose-based mentorship."""
    mentor_name: str
    disciple_name: str
    purpose_area: PurposeCategory
    started_day: int
    
    # Relationship dynamics
    teaching_effectiveness: float
    learning_receptivity: float
    wisdom_transferred: List[str]
    skills_developed: List[str]
    
    # Progress
    sessions_completed: int
    major_breakthroughs: List[str]
    graduation_day: Optional[int]


class LifePurposeSystem:
    """
    Manages life purpose discovery, career aspirations, spiritual development,
    and meaning-making throughout agents' lifetimes.
    """
    
    def __init__(self):
        self.agent_purposes: Dict[str, LifePurpose] = {}
        self.existential_moments: List[ExistentialMoment] = []
        self.mentorship_relations: Dict[str, MentorshipRelation] = {}
        
        # System tracking
        self.purpose_discoveries: List[Dict[str, Any]] = []
        self.spiritual_awakenings: List[Dict[str, Any]] = []
        self.legacy_achievements: List[Dict[str, Any]] = []
        
        # Configuration
        self.purpose_discovery_age_range = (18, 30)  # Most discover purpose in this range
        self.midlife_crisis_chance = 0.3            # 30% chance of midlife crisis
        self.spiritual_awakening_chance = 0.05      # 5% base chance per year
        self.mentorship_formation_chance = 0.2      # 20% chance when conditions met
        
        # Purpose archetypes and descriptions
        self.purpose_descriptions = self._initialize_purpose_descriptions()
        self.career_paths = self._initialize_career_paths()
        self.spiritual_questions = self._initialize_spiritual_questions()
        
    def _initialize_purpose_descriptions(self) -> Dict[PurposeCategory, List[str]]:
        """Initialize purpose descriptions for each category."""
        return {
            PurposeCategory.CREATOR: [
                "To bring new beauty into the world through art and creation",
                "To build lasting structures that serve future generations",
                "To invent solutions that improve life for everyone",
                "To express the divine through creative works"
            ],
            PurposeCategory.PROTECTOR: [
                "To shield the innocent from harm and injustice",
                "To heal the sick and comfort the suffering",
                "To defend my community against all threats",
                "To preserve what is sacred and valuable"
            ],
            PurposeCategory.TEACHER: [
                "To guide others toward wisdom and understanding",
                "To ensure knowledge passes to future generations",
                "To help each person discover their own potential",
                "To illuminate truth through patient instruction"
            ],
            PurposeCategory.EXPLORER: [
                "To discover new lands and possibilities",
                "To push the boundaries of what is known",
                "To venture where others fear to go",
                "To map the unknown territories of existence"
            ],
            PurposeCategory.CAREGIVER: [
                "To nurture and support those who need help",
                "To ease suffering wherever I find it",
                "To create a world where everyone feels valued",
                "To be a source of comfort and strength"
            ],
            PurposeCategory.LEADER: [
                "To guide my people toward a better future",
                "To organize society for the common good",
                "To inspire others to achieve their greatest potential",
                "To bear responsibility for collective decisions"
            ],
            PurposeCategory.SCHOLAR: [
                "To understand the deep truths of existence",
                "To uncover the patterns that govern reality",
                "To preserve and expand human knowledge",
                "To think the thoughts that advance civilization"
            ],
            PurposeCategory.CONNECTOR: [
                "To bridge differences and bring people together",
                "To facilitate understanding between diverse groups",
                "To create networks that strengthen community",
                "To ensure information and resources flow freely"
            ],
            PurposeCategory.MYSTIC: [
                "To commune with the divine and transcendent",
                "To explore the spiritual dimensions of existence",
                "To help others find their connection to the sacred",
                "To be a bridge between the material and spiritual worlds"
            ]
        }
    
    def _initialize_career_paths(self) -> Dict[PurposeCategory, List[str]]:
        """Initialize career aspirations for each purpose category."""
        return {
            PurposeCategory.CREATOR: ["master_artisan", "architect", "inventor", "storyteller", "musician"],
            PurposeCategory.PROTECTOR: ["healer", "guardian", "warrior", "defender", "peacekeeper"],
            PurposeCategory.TEACHER: ["educator", "mentor", "guide", "counselor", "trainer"],
            PurposeCategory.EXPLORER: ["scout", "navigator", "adventurer", "researcher", "pioneer"],
            PurposeCategory.CAREGIVER: ["caretaker", "supporter", "helper", "comforter", "nurturer"],
            PurposeCategory.LEADER: ["chief", "organizer", "ruler", "coordinator", "director"],
            PurposeCategory.SCHOLAR: ["philosopher", "researcher", "thinker", "analyst", "theorist"],
            PurposeCategory.CONNECTOR: ["diplomat", "trader", "messenger", "facilitator", "negotiator"],
            PurposeCategory.MYSTIC: ["spiritual_guide", "visionary", "oracle", "priest", "sage"]
        }
    
    def _initialize_spiritual_questions(self) -> List[str]:
        """Initialize existential questions agents might contemplate."""
        return [
            "What is the meaning of existence?",
            "Why was I born into this world?",
            "What happens after death?",
            "Is there a divine purpose to life?",
            "How should I treat others?",
            "What legacy will I leave behind?",
            "Am I fulfilling my true potential?",
            "What is my responsibility to future generations?",
            "How can I find inner peace?",
            "What is the nature of consciousness?",
            "Are we alone in the universe?",
            "What is the source of moral truth?"
        ]
    
    def process_daily_purpose_development(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process daily purpose development activities."""
        events = []
        
        # Phase 1: Purpose discovery for young agents
        discovery_events = self._process_purpose_discovery(agents, current_day)
        events.extend(discovery_events)
        
        # Phase 2: Purpose development and progression
        development_events = self._process_purpose_development(agents, current_day)
        events.extend(development_events)
        
        # Phase 3: Existential questioning and spiritual moments
        spiritual_events = self._process_existential_moments(agents, current_day)
        events.extend(spiritual_events)
        
        # Phase 4: Mentorship formation and teaching
        mentorship_events = self._process_mentorship_activities(agents, current_day)
        events.extend(mentorship_events)
        
        # Phase 5: Midlife crises and purpose evolution
        crisis_events = self._process_midlife_transformations(agents, current_day)
        events.extend(crisis_events)
        
        # Phase 6: Legacy building and transcendence
        legacy_events = self._process_legacy_building(agents, current_day)
        events.extend(legacy_events)
        
        return events
    
    def _process_purpose_discovery(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle agents discovering their life purpose."""
        events = []
        
        for agent in agents:
            if (not agent.is_alive or 
                agent.name in self.agent_purposes or
                not self._is_ready_for_purpose_discovery(agent)):
                continue
            
            # Check if agent has a purpose-triggering experience
            if self._should_discover_purpose(agent, current_day):
                purpose = self._discover_life_purpose(agent, current_day)
                
                if purpose:
                    self.agent_purposes[agent.name] = purpose
                    
                    # Add purpose to agent
                    agent.life_purpose = purpose.primary_purpose.value
                    agent.purpose_description = purpose.purpose_description
                    agent.purpose_fulfillment = purpose.fulfillment_level
                    
                    # Create memory
                    agent.memory.store_memory(
                        f"I've discovered my life's purpose: {purpose.purpose_description}. Everything makes sense now!",
                        importance=1.0,
                        emotion="enlightenment",
                        memory_type="life_milestone"
                    )
                    
                    events.append({
                        "type": "purpose_discovery",
                        "agent": agent.name,
                        "purpose": purpose.primary_purpose.value,
                        "description": purpose.purpose_description,
                        "day": current_day
                    })
        
        return events
    
    def _process_purpose_development(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle development and progression of existing purposes."""
        events = []
        
        for agent in agents:
            if not agent.is_alive or agent.name not in self.agent_purposes:
                continue
            
            purpose = self.agent_purposes[agent.name]
            
            # Progress purpose development
            progress_event = self._advance_purpose_progress(agent, purpose, current_day)
            if progress_event:
                events.append(progress_event)
            
            # Check for stage transitions
            stage_event = self._check_purpose_stage_transition(agent, purpose, current_day)
            if stage_event:
                events.append(stage_event)
        
        return events
    
    def _process_existential_moments(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle moments of deep questioning and spiritual experiences."""
        events = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            # Check for existential moments
            if random.random() < self._calculate_existential_moment_chance(agent):
                moment = self._create_existential_moment(agent, current_day)
                self.existential_moments.append(moment)
                
                # Process the impact
                self._process_existential_impact(agent, moment)
                
                events.append({
                    "type": "existential_moment",
                    "agent": agent.name,
                    "moment_type": moment.moment_type,
                    "trigger": moment.trigger_event,
                    "questions": moment.questions_raised[:2],  # First 2 questions
                    "day": current_day
                })
        
        return events
    
    def _process_mentorship_activities(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle mentorship formation and activities."""
        events = []
        
        # Find potential mentor-student pairs
        mentors = [a for a in agents if a.is_alive and a.age >= 40 and a.name in self.agent_purposes]
        students = [a for a in agents if a.is_alive and a.age <= 35]
        
        for mentor in mentors:
            mentor_purpose = self.agent_purposes[mentor.name]
            if mentor_purpose.stage in [PurposeStage.MASTERY, PurposeStage.MENTORING]:
                for student in students:
                    if (random.random() < self.mentorship_formation_chance and
                        self._should_mentor_relationship_form(mentor, student)):
                        
                        mentorship = self._create_mentorship_relation(mentor, student, current_day)
                        if mentorship:
                            self.mentorship_relations[f"{mentor.name}_{student.name}"] = mentorship
                            
                            events.append({
                                "type": "mentorship_formed",
                                "mentor": mentor.name,
                                "student": student.name,
                                "purpose_area": mentorship.purpose_area.value,
                                "day": current_day
                            })
        
        return events
    
    def _process_midlife_transformations(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle midlife crises and purpose evolution."""
        events = []
        
        for agent in agents:
            if (agent.is_alive and 45 <= agent.age <= 55 and 
                random.random() < self.midlife_crisis_chance):
                
                crisis_event = self._trigger_midlife_crisis(agent, current_day)
                if crisis_event:
                    events.append(crisis_event)
        
        return events
    
    def _process_legacy_building(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle legacy building activities for elder agents."""
        events = []
        
        for agent in agents:
            if (agent.is_alive and agent.age >= 60 and 
                agent.name in self.agent_purposes):
                
                purpose = self.agent_purposes[agent.name]
                if purpose.stage != PurposeStage.LEGACY:
                    purpose.stage = PurposeStage.LEGACY
                    
                    events.append({
                        "type": "legacy_stage_reached",
                        "agent": agent.name,
                        "purpose": purpose.primary_purpose.value,
                        "legacy_desires": purpose.legacy_desires,
                        "day": current_day
                    })
        
        return events
    
    def _is_ready_for_purpose_discovery(self, agent: Any) -> bool:
        """Check if agent is ready to discover their purpose."""
        min_age, max_age = self.purpose_discovery_age_range
        
        # Age requirement
        if not (min_age <= agent.age <= max_age):
            return False
        
        # Must have some life experience (memories)
        if len(agent.memory.get_recent_memories(days=365)) < 50:
            return False
        
        # Must have developed some skills
        if hasattr(agent, 'advanced_skills'):
            skilled_areas = sum(1 for skill in agent.advanced_skills.values() if skill.level > 0.3)
            if skilled_areas < 2:
                return False
        
        return True
    
    def _should_discover_purpose(self, agent: Any, current_day: int) -> bool:
        """Determine if agent should discover purpose today."""
        # Base chance increases with age within discovery range
        min_age, max_age = self.purpose_discovery_age_range
        age_factor = (agent.age - min_age) / (max_age - min_age)
        base_chance = 0.01 + (age_factor * 0.05)  # 1% to 6% chance
        
        # Increase chance based on recent significant experiences
        recent_memories = agent.memory.get_recent_memories(days=30)
        significant_experiences = len([m for m in recent_memories if m.importance > 0.7])
        experience_bonus = min(0.05, significant_experiences * 0.01)
        
        # Personality factors
        openness_bonus = agent.personality_scores.get("openness", 0.5) * 0.02
        conscientiousness_bonus = agent.personality_scores.get("conscientiousness", 0.5) * 0.01
        
        total_chance = base_chance + experience_bonus + openness_bonus + conscientiousness_bonus
        
        return random.random() < total_chance
    
    def _discover_life_purpose(self, agent: Any, current_day: int) -> LifePurpose:
        """Generate a life purpose for an agent."""
        # Determine purpose category based on personality and experiences
        purpose_category = self._determine_purpose_category(agent)
        
        # Select specific purpose description
        descriptions = self.purpose_descriptions[purpose_category]
        purpose_description = random.choice(descriptions)
        
        # Generate secondary purposes
        secondary_purposes = []
        for _ in range(random.randint(1, 3)):
            secondary = random.choice(list(PurposeCategory))
            if secondary != purpose_category and secondary not in secondary_purposes:
                secondary_purposes.append(secondary)
        
        # Generate career aspirations
        career_paths = self.career_paths[purpose_category]
        career_aspirations = random.sample(career_paths, min(3, len(career_paths)))
        
        # Generate legacy desires
        legacy_desires = self._generate_legacy_desires(purpose_category)
        
        # Generate initial spiritual beliefs
        spiritual_beliefs = self._generate_spiritual_beliefs(agent)
        
        return LifePurpose(
            agent_name=agent.name,
            primary_purpose=purpose_category,
            purpose_description=purpose_description,
            discovered_day=current_day,
            stage=PurposeStage.EMERGING,
            commitment_level=random.uniform(0.6, 0.8),
            fulfillment_level=random.uniform(0.3, 0.6),
            progress=0.1,
            secondary_purposes=secondary_purposes,
            career_aspirations=career_aspirations,
            legacy_desires=legacy_desires,
            spiritual_beliefs=spiritual_beliefs,
            purpose_evolution=[],
            major_realizations=[],
            obstacles_overcome=[],
            mentors=[],
            disciples=[]
        )
    
    def _determine_purpose_category(self, agent: Any) -> PurposeCategory:
        """Determine purpose category based on agent traits and personality."""
        # Personality-based weights
        weights = {}
        
        # Map personality traits to purposes
        openness = agent.personality_scores.get("openness", 0.5)
        conscientiousness = agent.personality_scores.get("conscientiousness", 0.5)
        extraversion = agent.personality_scores.get("extraversion", 0.5)
        agreeableness = agent.personality_scores.get("agreeableness", 0.5)
        neuroticism = agent.personality_scores.get("neuroticism", 0.5)
        
        weights[PurposeCategory.CREATOR] = openness * 2 + (1 - neuroticism)
        weights[PurposeCategory.PROTECTOR] = agreeableness + conscientiousness + (1 - neuroticism)
        weights[PurposeCategory.TEACHER] = agreeableness + conscientiousness + extraversion * 0.5
        weights[PurposeCategory.EXPLORER] = openness + extraversion + (1 - neuroticism)
        weights[PurposeCategory.CAREGIVER] = agreeableness * 2 + conscientiousness
        weights[PurposeCategory.LEADER] = extraversion * 2 + conscientiousness + (1 - neuroticism)
        weights[PurposeCategory.SCHOLAR] = openness + conscientiousness + (1 - extraversion) * 0.5
        weights[PurposeCategory.CONNECTOR] = extraversion + agreeableness + openness
        weights[PurposeCategory.MYSTIC] = openness + (1 - extraversion) + neuroticism * 0.5
        
        # Add trait-based bonuses
        traits = getattr(agent, 'traits', [])
        if 'creative' in traits:
            weights[PurposeCategory.CREATOR] += 1.0
        if 'protective' in traits:
            weights[PurposeCategory.PROTECTOR] += 1.0
        if 'wise' in traits:
            weights[PurposeCategory.TEACHER] += 1.0
        if 'curious' in traits:
            weights[PurposeCategory.EXPLORER] += 1.0
        if 'caring' in traits:
            weights[PurposeCategory.CAREGIVER] += 1.0
        if 'ambitious' in traits:
            weights[PurposeCategory.LEADER] += 1.0
        if 'analytical' in traits:
            weights[PurposeCategory.SCHOLAR] += 1.0
        if 'social' in traits:
            weights[PurposeCategory.CONNECTOR] += 1.0
        if 'spiritual' in traits:
            weights[PurposeCategory.MYSTIC] += 1.0
        
        # Weighted random selection
        total_weight = sum(weights.values())
        if total_weight == 0:
            return random.choice(list(PurposeCategory))
        
        rand_val = random.uniform(0, total_weight)
        current_weight = 0
        
        for purpose, weight in weights.items():
            current_weight += weight
            if rand_val <= current_weight:
                return purpose
        
        return list(PurposeCategory)[0]  # Fallback
    
    def _generate_legacy_desires(self, purpose_category: PurposeCategory) -> List[str]:
        """Generate what the agent wants to be remembered for."""
        legacy_templates = {
            PurposeCategory.CREATOR: [
                "Creating beautiful works that inspire future generations",
                "Building structures that last for centuries",
                "Inventing tools that make life better"
            ],
            PurposeCategory.PROTECTOR: [
                "Defending the innocent from harm",
                "Healing those who suffered",
                "Making the world a safer place"
            ],
            PurposeCategory.TEACHER: [
                "Educating countless students",
                "Passing down wisdom to future generations",
                "Helping others discover their potential"
            ],
            PurposeCategory.EXPLORER: [
                "Discovering new lands and possibilities",
                "Pushing the boundaries of the known world",
                "Inspiring others to venture forth"
            ],
            PurposeCategory.CAREGIVER: [
                "Helping those in need",
                "Creating a more compassionate world",
                "Being there for people when they needed me most"
            ],
            PurposeCategory.LEADER: [
                "Leading my people to prosperity",
                "Making decisions that benefited everyone",
                "Uniting people around common causes"
            ],
            PurposeCategory.SCHOLAR: [
                "Advancing human knowledge",
                "Solving important mysteries",
                "Thinking thoughts that changed everything"
            ],
            PurposeCategory.CONNECTOR: [
                "Bringing people together",
                "Building bridges between different groups",
                "Creating lasting friendships and alliances"
            ],
            PurposeCategory.MYSTIC: [
                "Connecting people to the divine",
                "Exploring the mysteries of existence",
                "Helping others find inner peace"
            ]
        }
        
        templates = legacy_templates.get(purpose_category, ["Making a positive difference"])
        return random.sample(templates, min(2, len(templates)))
    
    def _generate_spiritual_beliefs(self, agent: Any) -> Dict[str, Any]:
        """Generate spiritual beliefs for an agent."""
        beliefs = {}
        
        # Basic spiritual orientation
        spirituality_level = random.uniform(0.2, 1.0)
        beliefs["spirituality_level"] = spirituality_level
        
        if spirituality_level > 0.7:
            beliefs["believes_in_afterlife"] = True
            beliefs["believes_in_divine"] = True
            beliefs["practices_meditation"] = random.choice([True, False])
        elif spirituality_level > 0.4:
            beliefs["believes_in_afterlife"] = random.choice([True, False])
            beliefs["believes_in_divine"] = random.choice([True, False])
            beliefs["practices_meditation"] = False
        else:
            beliefs["believes_in_afterlife"] = False
            beliefs["believes_in_divine"] = False
            beliefs["practices_meditation"] = False
        
        # Personal spiritual questions
        questions = random.sample(self.spiritual_questions, random.randint(2, 5))
        beliefs["contemplated_questions"] = questions
        
        return beliefs
    
    def _calculate_existential_moment_chance(self, agent: Any) -> float:
        """Calculate chance of existential moment occurring."""
        base_chance = 0.001  # 0.1% per day
        
        # Age factor (more common in youth and midlife)
        if 16 <= agent.age <= 25:
            age_factor = 2.0  # Youth questioning
        elif 45 <= agent.age <= 55:
            age_factor = 2.5  # Midlife crisis
        elif agent.age >= 65:
            age_factor = 1.5  # Elder contemplation
        else:
            age_factor = 1.0
        
        # Personality factors
        openness_factor = 1 + agent.personality_scores.get("openness", 0.5)
        neuroticism_factor = 1 + agent.personality_scores.get("neuroticism", 0.5) * 0.5
        
        # Recent trauma or significant events
        recent_memories = agent.memory.get_recent_memories(days=30)
        trauma_factor = 1.0
        for memory in recent_memories:
            if memory.emotion in ["grief", "fear", "awe"]:
                trauma_factor += 0.5
        
        return base_chance * age_factor * openness_factor * neuroticism_factor * trauma_factor
    
    def _create_existential_moment(self, agent: Any, current_day: int) -> ExistentialMoment:
        """Create an existential questioning moment."""
        moment_types = ["crisis", "revelation", "questioning", "insight"]
        moment_type = random.choice(moment_types)
        
        # Determine trigger based on recent experiences
        recent_memories = agent.memory.get_recent_memories(days=7)
        if recent_memories:
            trigger = f"Reflecting on recent experience: {recent_memories[0].content[:50]}"
        else:
            triggers = [
                "Watching the stars at night",
                "Witnessing a birth or death",
                "Experiencing a moment of profound beauty",
                "Feeling deeply alone",
                "Achieving a long-sought goal"
            ]
            trigger = random.choice(triggers)
        
        # Generate questions based on moment type
        if moment_type == "crisis":
            questions = [
                "Am I wasting my life?",
                "What have I really accomplished?",
                "Is this all there is?"
            ]
        elif moment_type == "revelation":
            questions = [
                "What if everything is connected?",
                "What is my true calling?",
                "How can I make a real difference?"
            ]
        elif moment_type == "questioning":
            questions = random.sample(self.spiritual_questions, 3)
        else:  # insight
            questions = [
                "How can I live more authentically?",
                "What really matters in life?",
                "How should I treat others?"
            ]
        
        insights = []
        if random.random() < 0.6:  # 60% chance of gaining insights
            insight_templates = [
                "Life is precious and should not be wasted",
                "Connection with others gives life meaning",
                "I have more potential than I realized",
                "Small acts of kindness matter greatly",
                "Everyone is struggling in their own way"
            ]
            insights = [random.choice(insight_templates)]
        
        return ExistentialMoment(
            agent_name=agent.name,
            moment_type=moment_type,
            trigger_event=trigger,
            questions_raised=questions,
            day=current_day,
            emotional_impact=random.uniform(0.5, 1.0),
            insights_gained=insights,
            purpose_change=random.uniform(-0.1, 0.3),
            spiritual_growth=random.uniform(0.0, 0.2)
        )
    
    def _process_existential_impact(self, agent: Any, moment: ExistentialMoment):
        """Process the impact of an existential moment on the agent."""
        # Create memory
        agent.memory.store_memory(
            f"I had a profound moment of {moment.moment_type}: {moment.trigger_event}. "
            f"I found myself questioning: {moment.questions_raised[0]}",
            importance=0.8,
            emotion="contemplative",
            memory_type="philosophical"
        )
        
        # Update purpose if agent has one
        if agent.name in self.agent_purposes:
            purpose = self.agent_purposes[agent.name]
            purpose.fulfillment_level = max(0, min(1, purpose.fulfillment_level + moment.purpose_change))
            
            if moment.insights_gained:
                purpose.major_realizations.extend(moment.insights_gained)
        
        # Update spiritual beliefs
        if hasattr(agent, 'spiritual_growth'):
            agent.spiritual_growth += moment.spiritual_growth
        else:
            agent.spiritual_growth = moment.spiritual_growth
    
    def _should_mentor_relationship_form(self, mentor: Any, student: Any) -> bool:
        """Check if mentorship should form between two agents."""
        # Check if they're in same location
        if mentor.location != student.location:
            return False
        
        # Check if they have compatible purposes or interests
        mentor_purpose = self.agent_purposes[mentor.name]
        
        # Students without purpose are good candidates
        if student.name not in self.agent_purposes:
            return True
        
        # Students with related purposes
        student_purpose = self.agent_purposes[student.name]
        if (student_purpose.primary_purpose == mentor_purpose.primary_purpose or
            mentor_purpose.primary_purpose in student_purpose.secondary_purposes):
            return True
        
        return False
    
    def _create_mentorship_relation(self, mentor: Any, student: Any, current_day: int) -> Optional[MentorshipRelation]:
        """Create a mentorship relationship."""
        mentor_purpose = self.agent_purposes[mentor.name]
        
        return MentorshipRelation(
            mentor_name=mentor.name,
            disciple_name=student.name,
            purpose_area=mentor_purpose.primary_purpose,
            started_day=current_day,
            teaching_effectiveness=random.uniform(0.6, 0.9),
            learning_receptivity=random.uniform(0.5, 0.8),
            wisdom_transferred=[],
            skills_developed=[],
            sessions_completed=0,
            major_breakthroughs=[],
            graduation_day=None
        )
    
    def _trigger_midlife_crisis(self, agent: Any, current_day: int) -> Optional[Dict[str, Any]]:
        """Trigger a midlife crisis for an agent."""
        if agent.name not in self.agent_purposes:
            return None
        
        purpose = self.agent_purposes[agent.name]
        
        # Create existential moment
        crisis_questions = [
            "Have I wasted half my life?",
            "Is this really my true calling?",
            "What have I actually accomplished?",
            "How much time do I have left?",
            "Should I change everything?"
        ]
        
        moment = ExistentialMoment(
            agent_name=agent.name,
            moment_type="crisis",
            trigger_event="Reaching middle age and questioning life choices",
            questions_raised=random.sample(crisis_questions, 3),
            day=current_day,
            emotional_impact=random.uniform(0.7, 1.0),
            insights_gained=[],
            purpose_change=random.uniform(-0.3, 0.4),
            spiritual_growth=random.uniform(0.1, 0.3)
        )
        
        self.existential_moments.append(moment)
        
        # Possibly evolve purpose
        if random.random() < 0.3:  # 30% chance to change purpose
            self._evolve_agent_purpose(agent, purpose, current_day)
        
        return {
            "type": "midlife_crisis",
            "agent": agent.name,
            "questions": moment.questions_raised,
            "impact": moment.emotional_impact,
            "day": current_day
        }
    
    def get_agent_purpose_summary(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive purpose summary for an agent."""
        if agent_name not in self.agent_purposes:
            return None
        
        purpose = self.agent_purposes[agent_name]
        existential_moments = [m for m in self.existential_moments if m.agent_name == agent_name]
        
        return {
            "primary_purpose": purpose.primary_purpose.value,
            "description": purpose.purpose_description,
            "stage": purpose.stage.value,
            "commitment": purpose.commitment_level,
            "fulfillment": purpose.fulfillment_level,
            "progress": purpose.progress,
            "career_aspirations": purpose.career_aspirations,
            "legacy_desires": purpose.legacy_desires,
            "spiritual_beliefs": purpose.spiritual_beliefs,
            "major_realizations": purpose.major_realizations,
            "existential_moments": len(existential_moments),
            "mentors": purpose.mentors,
            "disciples": purpose.disciples
        }
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get comprehensive purpose system summary."""
        purpose_distribution = {}
        for purpose in self.agent_purposes.values():
            category = purpose.primary_purpose.value
            purpose_distribution[category] = purpose_distribution.get(category, 0) + 1
        
        return {
            "agents_with_purpose": len(self.agent_purposes),
            "purpose_distribution": purpose_distribution,
            "existential_moments": len(self.existential_moments),
            "mentorship_relations": len(self.mentorship_relations),
            "average_fulfillment": sum(p.fulfillment_level for p in self.agent_purposes.values()) / 
                                 max(1, len(self.agent_purposes)),
            "spiritual_awakenings": len(self.spiritual_awakenings)
        } 