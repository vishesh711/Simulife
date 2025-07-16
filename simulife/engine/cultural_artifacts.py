"""
Cultural Artifact Creation System for SimuLife
Manages the creation, preservation, and influence of cultural artifacts in the community.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum


class ArtifactType(Enum):
    """Types of cultural artifacts that can be created."""
    STORY = "story"                 # Oral narratives and legends
    ARTWORK = "artwork"             # Visual arts and crafts
    TOOL = "tool"                   # Functional implements with cultural significance
    RITUAL = "ritual"               # Ceremonial practices
    SONG = "song"                   # Musical compositions
    RECIPE = "recipe"               # Culinary traditions
    CUSTOM = "custom"               # Social practices and norms
    MONUMENT = "monument"           # Permanent structures with meaning
    SYMBOL = "symbol"               # Representative objects or designs
    GAME = "game"                   # Entertainment and competitive activities


class ArtifactSignificance(Enum):
    """Levels of cultural significance."""
    PERSONAL = "personal"           # Meaningful to individual/family
    LOCAL = "local"                 # Important to immediate community
    CULTURAL = "cultural"           # Defines community identity
    LEGENDARY = "legendary"         # Transcendent cultural importance


@dataclass
class CulturalArtifact:
    """Represents a cultural artifact created by agents."""
    id: str
    name: str
    type: ArtifactType
    creator: str                    # Agent who created it
    created_day: int
    description: str
    significance: ArtifactSignificance
    preservation_level: float = 1.0  # How well preserved (0.0 to 1.0)
    cultural_influence: float = 0.5  # How much it affects community (0.0 to 1.0)
    associated_agents: Set[str] = None  # Agents who know/value this artifact
    memories_created: List[str] = None  # Important memories this artifact created
    variations: List[str] = None    # Different versions or interpretations
    materials_used: List[str] = None  # What was used to create it
    skills_demonstrated: List[str] = None  # Skills showcased in creation
    
    def __post_init__(self):
        if self.associated_agents is None:
            self.associated_agents = set()
        if self.memories_created is None:
            self.memories_created = []
        if self.variations is None:
            self.variations = []
        if self.materials_used is None:
            self.materials_used = []
        if self.skills_demonstrated is None:
            self.skills_demonstrated = []
    
    def decay(self, decay_rate: float = 0.01):
        """Artifacts gradually decay without maintenance."""
        self.preservation_level = max(0.0, self.preservation_level - decay_rate)
        
        # Significance affects decay rate
        significance_protection = {
            ArtifactSignificance.PERSONAL: 1.0,
            ArtifactSignificance.LOCAL: 0.8,
            ArtifactSignificance.CULTURAL: 0.5,
            ArtifactSignificance.LEGENDARY: 0.2
        }
        
        protection = significance_protection.get(self.significance, 1.0)
        self.preservation_level = max(0.0, self.preservation_level - (decay_rate * protection))
    
    def is_lost(self) -> bool:
        """Check if artifact is effectively lost to the community."""
        return self.preservation_level < 0.1 or len(self.associated_agents) == 0


@dataclass
class ArtifactTemplate:
    """Template for creating specific types of artifacts."""
    type: ArtifactType
    required_skills: Dict[str, float]  # Skills needed to create
    base_names: List[str]             # Possible names for this type
    description_templates: List[str]   # Template descriptions
    materials_options: List[List[str]] # Possible material combinations
    creation_time: int = 1            # Days to create
    base_significance: ArtifactSignificance = ArtifactSignificance.PERSONAL
    
    def can_create(self, agent) -> bool:
        """Check if agent can create this type of artifact."""
        if not hasattr(agent, 'advanced_skills'):
            return False
            
        for skill_name, min_level in self.required_skills.items():
            if skill_name not in agent.advanced_skills:
                return False
            if agent.advanced_skills[skill_name].get_effective_level() < min_level:
                return False
        
        return True


class CulturalArtifactSystem:
    """
    Manages the creation, preservation, and cultural impact of artifacts.
    """
    
    def __init__(self):
        self.artifacts = {}  # id -> CulturalArtifact
        self.artifact_templates = self._initialize_templates()
        self.artifact_counter = 0
        self.community_traditions = []  # Artifacts that have become traditions
        
    def _generate_artifact_id(self) -> str:
        """Generate a unique artifact ID."""
        self.artifact_counter += 1
        return f"artifact_{self.artifact_counter:03d}"
    
    def _initialize_templates(self) -> Dict[ArtifactType, ArtifactTemplate]:
        """Initialize templates for different artifact types."""
        return {
            ArtifactType.STORY: ArtifactTemplate(
                type=ArtifactType.STORY,
                required_skills={"storytelling": 1.5},
                base_names=["The Tale of", "Legend of", "Story of", "Chronicles of", "Saga of"],
                description_templates=[
                    "an inspiring tale about {theme} that teaches important lessons",
                    "a thrilling story of {theme} that captivates listeners",
                    "a wisdom tale about {theme} passed down through generations",
                    "an epic narrative of {theme} that defines community values"
                ],
                materials_options=[["voice", "memory"], ["carved symbols", "voice"]],
                base_significance=ArtifactSignificance.LOCAL
            ),
            
            ArtifactType.ARTWORK: ArtifactTemplate(
                type=ArtifactType.ARTWORK,
                required_skills={"artistry": 2.0},
                base_names=["The", "Sacred", "Beautiful", "Masterful", "Inspired"],
                description_templates=[
                    "a beautiful {art_form} that expresses {emotion} and inspiration",
                    "an intricate {art_form} showing mastery of artistic technique",
                    "a meaningful {art_form} that represents community values",
                    "a stunning {art_form} that brings joy to all who see it"
                ],
                materials_options=[["clay", "pigments"], ["stone", "tools"], ["wood", "carving tools"]],
                base_significance=ArtifactSignificance.LOCAL
            ),
            
            ArtifactType.TOOL: ArtifactTemplate(
                type=ArtifactType.TOOL,
                required_skills={"toolmaking": 2.5, "innovation": 1.0},
                base_names=["The", "Master", "Crafted", "Perfected", "Sacred"],
                description_templates=[
                    "an ingenious {tool_type} that makes {task} much easier",
                    "a masterfully crafted {tool_type} showing exceptional skill",
                    "an innovative {tool_type} that represents a breakthrough in design",
                    "a sacred {tool_type} imbued with cultural significance"
                ],
                materials_options=[["wood", "stone", "fiber"], ["metal", "wood"], ["bone", "sinew"]],
                base_significance=ArtifactSignificance.CULTURAL
            ),
            
            ArtifactType.RITUAL: ArtifactTemplate(
                type=ArtifactType.RITUAL,
                required_skills={"inspiration": 2.0, "leadership": 1.5},
                base_names=["Ceremony of", "Ritual of", "Rite of", "Sacred", "Blessing of"],
                description_templates=[
                    "a meaningful ceremony for {occasion} that brings the community together",
                    "a sacred ritual honoring {concept} and its importance",
                    "a traditional rite marking {milestone} in community life",
                    "a spiritual practice connecting the community to {belief}"
                ],
                materials_options=[["sacred objects", "symbols"], ["natural elements"], ["community gathering"]],
                base_significance=ArtifactSignificance.CULTURAL
            ),
            
            ArtifactType.SONG: ArtifactTemplate(
                type=ArtifactType.SONG,
                required_skills={"storytelling": 1.0, "inspiration": 1.5},
                base_names=["Song of", "Ballad of", "Hymn of", "Melody of", "Chant of"],
                description_templates=[
                    "a stirring song about {theme} that inspires the community",
                    "a melodious ballad telling the story of {story_element}",
                    "a rhythmic chant used during {activity} to build unity",
                    "a beautiful melody that expresses {emotion} and shared feeling"
                ],
                materials_options=[["voice", "rhythm"], ["simple instruments", "voice"]],
                base_significance=ArtifactSignificance.LOCAL
            ),
            
            ArtifactType.RECIPE: ArtifactTemplate(
                type=ArtifactType.RECIPE,
                required_skills={"foraging": 2.0, "innovation": 1.0},
                base_names=["Special", "Traditional", "Celebrated", "Sacred", "Community"],
                description_templates=[
                    "a delicious {food_type} recipe perfect for {occasion}",
                    "a nourishing {food_type} that sustains the community",
                    "a special {food_type} preparation with cultural significance",
                    "an innovative {food_type} recipe that uses local ingredients creatively"
                ],
                materials_options=[["local plants", "preparation tools"], ["seasonal ingredients"]],
                base_significance=ArtifactSignificance.LOCAL
            ),
            
            ArtifactType.CUSTOM: ArtifactTemplate(
                type=ArtifactType.CUSTOM,
                required_skills={"leadership": 2.0, "teaching": 1.5},
                base_names=["Tradition of", "Custom of", "Practice of", "Way of", "Code of"],
                description_templates=[
                    "a meaningful custom regarding {social_aspect} that strengthens community",
                    "a traditional practice for {situation} that shows wisdom",
                    "a social norm about {behavior} that promotes harmony",
                    "a community guideline for {activity} that ensures fairness"
                ],
                materials_options=[["community agreement", "shared understanding"]],
                base_significance=ArtifactSignificance.CULTURAL
            ),
            
            ArtifactType.MONUMENT: ArtifactTemplate(
                type=ArtifactType.MONUMENT,
                required_skills={"construction": 3.0, "leadership": 2.0},
                base_names=["Memorial", "Monument to", "Sacred", "Great", "Community"],
                description_templates=[
                    "a lasting monument commemorating {important_event}",
                    "a sacred structure dedicated to {honored_concept}",
                    "an impressive monument showing community achievement",
                    "a memorial structure honoring {important_figure}"
                ],
                materials_options=[["stone", "earth", "community effort"], ["wood", "stone", "symbols"]],
                creation_time=7,
                base_significance=ArtifactSignificance.LEGENDARY
            ),
            
            ArtifactType.GAME: ArtifactTemplate(
                type=ArtifactType.GAME,
                required_skills={"innovation": 1.5, "athletics": 1.0},
                base_names=["Game of", "Contest of", "Challenge of", "Trial of", "Sport of"],
                description_templates=[
                    "an entertaining game testing {skill_type} and bringing joy",
                    "a competitive activity that builds {community_value}",
                    "a skillful game requiring {attribute} and strategy",
                    "a traditional contest celebrating {cultural_aspect}"
                ],
                materials_options=[["simple tools", "creativity"], ["natural objects", "rules"]],
                base_significance=ArtifactSignificance.LOCAL
            )
        }
    
    def evaluate_creation_potential(self, agent, current_day: int) -> List[Tuple[ArtifactType, float]]:
        """Evaluate which artifacts an agent could potentially create."""
        potentials = []
        
        for artifact_type, template in self.artifact_templates.items():
            if template.can_create(agent):
                # Calculate creation motivation score
                score = 0.0
                
                # Skill level contribution
                total_skill = 0.0
                for skill_name, min_level in template.required_skills.items():
                    if skill_name in agent.advanced_skills:
                        skill_level = agent.advanced_skills[skill_name].get_effective_level()
                        total_skill += skill_level / min_level  # Ratio above minimum
                
                score += total_skill / len(template.required_skills)
                
                # Personality trait contribution
                creation_traits = {
                    ArtifactType.STORY: ["creative", "wise", "charismatic"],
                    ArtifactType.ARTWORK: ["creative", "artistic", "sensitive"],
                    ArtifactType.TOOL: ["innovative", "practical", "patient"],
                    ArtifactType.RITUAL: ["spiritual", "wise", "charismatic"],
                    ArtifactType.SONG: ["creative", "expressive", "inspiring"],
                    ArtifactType.RECIPE: ["nurturing", "innovative", "practical"],
                    ArtifactType.CUSTOM: ["wise", "diplomatic", "thoughtful"],
                    ArtifactType.MONUMENT: ["ambitious", "dedicated", "inspiring"],
                    ArtifactType.GAME: ["playful", "creative", "social"]
                }
                
                relevant_traits = creation_traits.get(artifact_type, [])
                trait_matches = sum(1 for trait in relevant_traits if trait in agent.traits)
                score += trait_matches / len(relevant_traits) if relevant_traits else 0
                
                # Emotional state contribution
                if hasattr(agent, 'emotion'):
                    if agent.emotion in ["inspired", "creative", "joyful", "passionate"]:
                        score += 0.3
                    elif agent.emotion in ["sad", "angry", "frustrated"]:
                        score += 0.1  # Sometimes negative emotions inspire creation
                
                # Specialization bonus
                if hasattr(agent, 'specialization') and agent.specialization:
                    spec_bonuses = {
                        "artisan": [ArtifactType.ARTWORK, ArtifactType.TOOL, ArtifactType.MONUMENT],
                        "scholar": [ArtifactType.STORY, ArtifactType.CUSTOM],
                        "mystic": [ArtifactType.RITUAL, ArtifactType.SONG],
                        "leader": [ArtifactType.CUSTOM, ArtifactType.MONUMENT, ArtifactType.RITUAL]
                    }
                    
                    spec_type = agent.specialization.type.value
                    if spec_type in spec_bonuses and artifact_type in spec_bonuses[spec_type]:
                        score += 0.5
                
                if score > 0.5:  # Only consider if there's meaningful potential
                    potentials.append((artifact_type, score))
        
        return sorted(potentials, key=lambda x: x[1], reverse=True)
    
    def attempt_artifact_creation(self, agent, artifact_type: ArtifactType, 
                                current_day: int) -> Dict[str, Any]:
        """Agent attempts to create a cultural artifact."""
        template = self.artifact_templates[artifact_type]
        
        if not template.can_create(agent):
            return {
                "success": False,
                "reason": "Insufficient skills to create this artifact type",
                "agent": agent.name
            }
        
        # Calculate creation success probability
        success_rate = 0.6  # Base success rate
        
        # Skill bonus
        for skill_name, min_level in template.required_skills.items():
            if skill_name in agent.advanced_skills:
                skill_level = agent.advanced_skills[skill_name].get_effective_level()
                bonus = (skill_level - min_level) * 0.1
                success_rate += bonus
        
        # Specialization bonus
        if hasattr(agent, 'specialization') and agent.specialization:
            if agent.specialization.level >= 2.0:
                success_rate += 0.2
        
        success = random.random() < min(0.95, success_rate)
        
        if not success:
            agent.add_memory(f"Attempted to create a {artifact_type.value} but was not satisfied with the result", importance=0.4)
            return {
                "success": False,
                "reason": "Creation attempt was not successful",
                "agent": agent.name,
                "artifact_type": artifact_type.value
            }
        
        # Generate the artifact
        artifact = self._generate_artifact(agent, template, current_day)
        self.artifacts[artifact.id] = artifact
        
        # Grant experience to relevant skills
        for skill_name in template.required_skills:
            if skill_name in agent.advanced_skills:
                agent.advanced_skills[skill_name].practice(15.0, current_day)
        
        # Create memory
        agent.add_memory(f"Created {artifact.name}, a {artifact_type.value} of {artifact.significance.value} significance", importance=0.8)
        
        # Initially only creator knows about it
        artifact.associated_agents.add(agent.name)
        
        return {
            "success": True,
            "agent": agent.name,
            "artifact": {
                "id": artifact.id,
                "name": artifact.name,
                "type": artifact.type.value,
                "description": artifact.description,
                "significance": artifact.significance.value
            }
        }
    
    def _generate_artifact(self, agent, template: ArtifactTemplate, current_day: int) -> CulturalArtifact:
        """Generate a specific artifact based on template and agent."""
        artifact_id = self._generate_artifact_id()
        
        # Generate name
        name_base = random.choice(template.base_names)
        name_suffix = self._generate_name_suffix(agent, template.type)
        name = f"{name_base} {name_suffix}"
        
        # Generate description
        description_template = random.choice(template.description_templates)
        description = self._fill_description_template(description_template, agent, template.type)
        
        # Determine significance based on agent's skill and reputation
        significance = template.base_significance
        
        # High-skill agents can create more significant artifacts
        if hasattr(agent, 'advanced_skills'):
            avg_skill = sum(agent.advanced_skills[skill].get_effective_level() 
                          for skill in template.required_skills.keys() 
                          if skill in agent.advanced_skills) / len(template.required_skills)
            
            if avg_skill >= 4.0:
                significance = ArtifactSignificance.LEGENDARY
            elif avg_skill >= 3.0:
                significance = ArtifactSignificance.CULTURAL
        
        # Specialization can upgrade significance
        if hasattr(agent, 'specialization') and agent.specialization:
            if agent.specialization.level >= 3.5:
                if significance == ArtifactSignificance.LOCAL:
                    significance = ArtifactSignificance.CULTURAL
                elif significance == ArtifactSignificance.CULTURAL:
                    significance = ArtifactSignificance.LEGENDARY
        
        # Select materials
        materials = random.choice(template.materials_options)
        
        # Determine skills demonstrated
        skills_demonstrated = list(template.required_skills.keys())
        
        return CulturalArtifact(
            id=artifact_id,
            name=name,
            type=template.type,
            creator=agent.name,
            created_day=current_day,
            description=description,
            significance=significance,
            preservation_level=1.0,
            cultural_influence=self._calculate_initial_influence(significance),
            materials_used=materials,
            skills_demonstrated=skills_demonstrated
        )
    
    def _generate_name_suffix(self, agent, artifact_type: ArtifactType) -> str:
        """Generate a meaningful suffix for the artifact name."""
        suffixes = {
            ArtifactType.STORY: ["the Wanderer", "Ancient Wisdom", "the First Days", "the Great Journey", "Unity"],
            ArtifactType.ARTWORK: ["Serenity", "the Dawn", "Community Spirit", "the Seasons", "Harmony"],
            ArtifactType.TOOL: ["Precision", "the Builder", "Craftsmanship", "Innovation", "Mastery"],
            ArtifactType.RITUAL: ["Renewal", "Gratitude", "the Harvest", "Unity", "the Ancestors"],
            ArtifactType.SONG: ["the Heart", "Community", "the Sunrise", "Celebration", "Memory"],
            ArtifactType.RECIPE: ["Feast", "Comfort", "the Harvest", "Celebration", "Sustenance"],
            ArtifactType.CUSTOM: ["Respect", "Cooperation", "Wisdom", "Honor", "Fairness"],
            ArtifactType.MONUMENT: ["Remembrance", "Achievement", "the Founders", "Unity", "Hope"],
            ArtifactType.GAME: ["Skill", "Wisdom", "Speed", "Strategy", "Fun"]
        }
        
        base_suffixes = suffixes.get(artifact_type, ["Creation"])
        
        # Sometimes personalize with creator's name or traits
        if random.random() < 0.3:
            return f"{agent.name}'s {random.choice(['Legacy', 'Gift', 'Vision', 'Dream'])}"
        else:
            return random.choice(base_suffixes)
    
    def _fill_description_template(self, template: str, agent, artifact_type: ArtifactType) -> str:
        """Fill in template placeholders with appropriate content."""
        replacements = {
            "{theme}": ["courage", "wisdom", "love", "sacrifice", "discovery", "community", "growth"],
            "{emotion}": ["joy", "serenity", "strength", "hope", "wonder", "pride", "peace"],
            "{art_form}": ["sculpture", "painting", "carving", "mosaic", "tapestry", "medallion"],
            "{tool_type}": ["hammer", "chisel", "weaving loom", "hunting implement", "farming tool"],
            "{occasion}": ["harvest time", "coming of age", "seasonal change", "community gathering"],
            "{concept}": ["nature", "community", "wisdom", "the ancestors", "the future"],
            "{milestone}": ["important transitions", "achievements", "seasonal changes", "community growth"],
            "{belief}": ["shared values", "natural forces", "community spirit", "ancestral wisdom"],
            "{activity}": ["work", "celebration", "meditation", "community meetings"],
            "{story_element}": ["heroic deeds", "wise decisions", "community founding", "great challenges"],
            "{food_type}": ["bread", "stew", "porridge", "beverage", "preserve", "feast dish"],
            "{social_aspect}": ["cooperation", "conflict resolution", "resource sharing", "decision making"],
            "{situation}": ["disputes", "celebrations", "hardships", "important decisions"],
            "{behavior}": ["generosity", "honesty", "respect", "cooperation", "responsibility"],
            "{important_event}": ["community founding", "great achievements", "difficult times overcome"],
            "{honored_concept}": ["wisdom", "courage", "unity", "perseverance", "creativity"],
            "{important_figure}": ["community founders", "great leaders", "wise teachers", "heroes"],
            "{skill_type}": ["physical prowess", "mental agility", "creative thinking", "cooperation"],
            "{community_value}": ["teamwork", "fairness", "determination", "respect", "friendship"],
            "{attribute}": ["intelligence", "dexterity", "patience", "observation", "coordination"],
            "{cultural_aspect}": ["community bonds", "traditions", "achievements", "shared values"]
        }
        
        result = template
        for placeholder, options in replacements.items():
            if placeholder in result:
                result = result.replace(placeholder, random.choice(options))
        
        return result
    
    def _calculate_initial_influence(self, significance: ArtifactSignificance) -> float:
        """Calculate initial cultural influence based on significance."""
        influence_map = {
            ArtifactSignificance.PERSONAL: 0.1,
            ArtifactSignificance.LOCAL: 0.3,
            ArtifactSignificance.CULTURAL: 0.6,
            ArtifactSignificance.LEGENDARY: 0.9
        }
        return influence_map.get(significance, 0.3)
    
    def spread_artifact_knowledge(self, agents: List, current_day: int) -> List[Dict[str, Any]]:
        """Spread knowledge of artifacts through the community."""
        spread_events = []
        
        for artifact in self.artifacts.values():
            if artifact.is_lost():
                continue
            
            # Artifacts spread knowledge through social interactions
            knowledgeable_agents = [agent for agent in agents 
                                  if agent.name in artifact.associated_agents and agent.is_alive]
            
            if not knowledgeable_agents:
                continue
            
            # 20% chance per day for each knowledgeable agent to share
            for sharing_agent in knowledgeable_agents:
                if random.random() < 0.2:
                    # Find potential recipients
                    potential_recipients = [agent for agent in agents 
                                         if agent.name not in artifact.associated_agents 
                                         and agent.is_alive]
                    
                    if potential_recipients:
                        recipient = random.choice(potential_recipients)
                        
                        # Success depends on relationship and sharing agent's charisma
                        success_rate = 0.5
                        if recipient.name in sharing_agent.relationships:
                            rel_strength = sharing_agent.relationships[recipient.name].get("strength", 0)
                            success_rate += rel_strength * 0.3
                        
                        if "charismatic" in sharing_agent.traits:
                            success_rate += 0.2
                        
                        if random.random() < success_rate:
                            artifact.associated_agents.add(recipient.name)
                            
                            sharing_agent.add_memory(f"Shared knowledge of {artifact.name} with {recipient.name}", importance=0.5)
                            recipient.add_memory(f"Learned about {artifact.name} from {sharing_agent.name}", importance=0.6)
                            
                            spread_events.append({
                                "type": "artifact_knowledge_spread",
                                "artifact": artifact.name,
                                "sharing_agent": sharing_agent.name,
                                "recipient": recipient.name,
                                "artifact_type": artifact.type.value
                            })
        
        return spread_events
    
    def process_daily_artifacts(self, agents: List, current_day: int) -> List[Dict[str, Any]]:
        """Process all artifact-related activities for the day."""
        artifact_events = []
        
        # Attempt artifact creation
        for agent in agents:
            if not agent.is_alive:
                continue
            
            # 15% chance per day to attempt artifact creation
            if random.random() < 0.15:
                potentials = self.evaluate_creation_potential(agent, current_day)
                if potentials:
                    # Choose most suitable artifact type
                    chosen_type = potentials[0][0]
                    creation_result = self.attempt_artifact_creation(agent, chosen_type, current_day)
                    if creation_result["success"]:
                        artifact_events.append({
                            "type": "artifact_created",
                            **creation_result
                        })
        
        # Spread artifact knowledge
        spread_events = self.spread_artifact_knowledge(agents, current_day)
        artifact_events.extend(spread_events)
        
        # Process artifact decay and preservation
        preservation_events = self._process_preservation(agents, current_day)
        artifact_events.extend(preservation_events)
        
        return artifact_events
    
    def _process_preservation(self, agents: List, current_day: int) -> List[Dict[str, Any]]:
        """Process preservation and decay of artifacts."""
        preservation_events = []
        
        # Apply decay to all artifacts
        for artifact in self.artifacts.values():
            if not artifact.is_lost():
                old_preservation = artifact.preservation_level
                artifact.decay()
                
                # Check if artifact became lost
                if artifact.preservation_level < 0.3 and old_preservation >= 0.3:
                    preservation_events.append({
                        "type": "artifact_deteriorating",
                        "artifact": artifact.name,
                        "preservation_level": artifact.preservation_level
                    })
                
                # Chance for preservation efforts
                knowledgeable_agents = [agent for agent in agents 
                                      if agent.name in artifact.associated_agents and agent.is_alive]
                
                for agent in knowledgeable_agents:
                    # 10% chance to attempt preservation
                    if random.random() < 0.1:
                        preservation_attempt = self._attempt_preservation(agent, artifact, current_day)
                        if preservation_attempt:
                            preservation_events.append(preservation_attempt)
        
        return preservation_events
    
    def _attempt_preservation(self, agent, artifact: CulturalArtifact, 
                            current_day: int) -> Optional[Dict[str, Any]]:
        """Agent attempts to preserve an artifact."""
        # Success depends on relevant skills
        success_rate = 0.4
        
        preservation_skills = {
            ArtifactType.STORY: ["storytelling", "teaching"],
            ArtifactType.ARTWORK: ["artistry", "construction"],
            ArtifactType.TOOL: ["toolmaking", "construction"],
            ArtifactType.RITUAL: ["inspiration", "leadership"],
            ArtifactType.SONG: ["storytelling", "inspiration"],
            ArtifactType.RECIPE: ["foraging", "teaching"],
            ArtifactType.CUSTOM: ["leadership", "teaching"],
            ArtifactType.MONUMENT: ["construction", "leadership"],
            ArtifactType.GAME: ["teaching", "innovation"]
        }
        
        relevant_skills = preservation_skills.get(artifact.type, [])
        if hasattr(agent, 'advanced_skills'):
            for skill in relevant_skills:
                if skill in agent.advanced_skills:
                    skill_level = agent.advanced_skills[skill].get_effective_level()
                    success_rate += skill_level * 0.05
        
        if random.random() < success_rate:
            # Successful preservation
            preservation_boost = random.uniform(0.1, 0.3)
            artifact.preservation_level = min(1.0, artifact.preservation_level + preservation_boost)
            
            agent.add_memory(f"Helped preserve {artifact.name} for future generations", importance=0.7)
            
            return {
                "type": "artifact_preserved",
                "agent": agent.name,
                "artifact": artifact.name,
                "new_preservation_level": artifact.preservation_level
            }
        
        return None
    
    def get_cultural_summary(self) -> Dict[str, Any]:
        """Get a summary of all cultural artifacts in the community."""
        active_artifacts = [a for a in self.artifacts.values() if not a.is_lost()]
        
        return {
            "total_artifacts": len(active_artifacts),
            "artifacts_by_type": self._count_by_type(active_artifacts),
            "artifacts_by_significance": self._count_by_significance(active_artifacts),
            "most_influential": self._get_most_influential_artifacts(),
            "most_preserved": self._get_best_preserved_artifacts(),
            "legendary_artifacts": [a.name for a in active_artifacts 
                                  if a.significance == ArtifactSignificance.LEGENDARY]
        }
    
    def _count_by_type(self, artifacts: List[CulturalArtifact]) -> Dict[str, int]:
        """Count artifacts by type."""
        counts = {}
        for artifact in artifacts:
            artifact_type = artifact.type.value
            counts[artifact_type] = counts.get(artifact_type, 0) + 1
        return counts
    
    def _count_by_significance(self, artifacts: List[CulturalArtifact]) -> Dict[str, int]:
        """Count artifacts by significance level."""
        counts = {}
        for artifact in artifacts:
            significance = artifact.significance.value
            counts[significance] = counts.get(significance, 0) + 1
        return counts
    
    def _get_most_influential_artifacts(self) -> List[Dict[str, Any]]:
        """Get the most culturally influential artifacts."""
        active_artifacts = [a for a in self.artifacts.values() if not a.is_lost()]
        top_artifacts = sorted(active_artifacts, key=lambda x: x.cultural_influence, reverse=True)[:3]
        
        return [{
            "name": a.name,
            "type": a.type.value,
            "creator": a.creator,
            "influence": round(a.cultural_influence, 2)
        } for a in top_artifacts]
    
    def _get_best_preserved_artifacts(self) -> List[Dict[str, Any]]:
        """Get the best preserved artifacts."""
        active_artifacts = [a for a in self.artifacts.values() if not a.is_lost()]
        top_artifacts = sorted(active_artifacts, key=lambda x: x.preservation_level, reverse=True)[:3]
        
        return [{
            "name": a.name,
            "type": a.type.value,
            "creator": a.creator,
            "preservation": round(a.preservation_level, 2)
        } for a in top_artifacts] 