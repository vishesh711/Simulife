"""
Advanced Event System for SimuLife
Generates complex, cascading events that create emergent storytelling and social dynamics.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    """Types of events that can occur in SimuLife."""
    NATURAL = "natural"           # Weather, disasters, resource changes
    SOCIAL = "social"             # Conflicts, celebrations, meetings
    DISCOVERY = "discovery"       # New knowledge, artifacts, places
    CRISIS = "crisis"             # Challenges requiring community response
    CULTURAL = "cultural"         # Festivals, traditions, beliefs
    POLITICAL = "political"       # Leadership changes, laws, alliances
    ECONOMIC = "economic"         # Trade, resource scarcity, prosperity
    TECHNOLOGICAL = "technological"  # Innovations, improvements


@dataclass
class EventTemplate:
    """Template for generating specific types of events."""
    event_type: EventType
    name: str
    description_template: str
    conditions: Dict[str, Any]    # Requirements for this event to trigger
    effects: Dict[str, Any]       # What happens when event occurs
    follow_up_events: List[str]   # Possible cascading events
    probability: float            # Base probability per day
    cooldown_days: int = 30       # Min days before event can repeat


class AdvancedEventSystem:
    """
    Advanced event generation system that creates emergent narratives.
    """
    
    def __init__(self):
        self.event_templates = self._initialize_event_templates()
        self.recent_events = []  # Track recent events for cascading effects
        self.event_cooldowns = {}  # Track when events last occurred
        self.cultural_memory = {}  # Track what the community remembers
        
    def _initialize_event_templates(self) -> Dict[str, EventTemplate]:
        """Initialize the library of possible events."""
        templates = {}
        
        # Natural Events
        templates["great_storm"] = EventTemplate(
            event_type=EventType.NATURAL,
            name="Great Storm",
            description_template="A powerful storm sweeps through {location}, affecting everyone",
            conditions={"season": ["autumn", "winter"], "min_agents": 2},
            effects={
                "world_resources": {"water": +0.3, "shelter": -0.2},
                "agent_emotions": {"emotion": "concerned", "intensity": 0.7},
                "relationship_bonds": +0.1  # Shared hardship brings people together
            },
            follow_up_events=["community_rebuilding", "resource_scarcity"],
            probability=0.08,
            cooldown_days=90
        )
        
        templates["abundant_harvest"] = EventTemplate(
            event_type=EventType.NATURAL,
            name="Abundant Harvest",
            description_template="The land provides an exceptional harvest in {location}",
            conditions={"season": ["summer", "autumn"], "world_resources.food": "> 0.8"},
            effects={
                "world_resources": {"food": +0.4},
                "agent_emotions": {"emotion": "joyful", "intensity": 0.8},
                "community_satisfaction": +0.3
            },
            follow_up_events=["harvest_celebration", "population_growth"],
            probability=0.06,
            cooldown_days=365
        )
        
        # Social Events
        templates["love_triangle"] = EventTemplate(
            event_type=EventType.SOCIAL,
            name="Love Triangle",
            description_template="{agent1} and {agent2} both pursue {agent3}, creating tension",
            conditions={"min_agents": 3, "has_romantic_relationships": True},
            effects={
                "relationship_drama": True,
                "faction_formation_chance": +0.2,
                "agent_emotions": {"emotion": "conflicted", "intensity": 0.6}
            },
            follow_up_events=["rivalry_formation", "community_division", "romantic_resolution"],
            probability=0.03,
            cooldown_days=180
        )
        
        templates["mentor_student"] = EventTemplate(
            event_type=EventType.SOCIAL,
            name="Mentorship Forms",
            description_template="{elder} begins teaching {student} valuable skills",
            conditions={"age_gap": 15, "skill_difference": 0.3},
            effects={
                "skill_transfer": True,
                "relationship_strength": +0.4,
                "knowledge_preservation": +0.2
            },
            follow_up_events=["knowledge_school", "tradition_formation"],
            probability=0.12,
            cooldown_days=60
        )
        
        # Discovery Events
        templates["ancient_artifact"] = EventTemplate(
            event_type=EventType.DISCOVERY,
            name="Ancient Artifact",
            description_template="{discoverer} finds a mysterious artifact while exploring {location}",
            conditions={"has_explorers": True, "location": ["forest", "mountains"]},
            effects={
                "world_mystery": +1,
                "discoverer_reputation": +0.3,
                "knowledge_gain": {"history": 0.2, "magic": 0.1}
            },
            follow_up_events=["belief_formation", "scholar_rivalry", "artifact_study"],
            probability=0.04,
            cooldown_days=120
        )
        
        templates["new_location"] = EventTemplate(
            event_type=EventType.DISCOVERY,
            name="New Territory",
            description_template="Explorers discover a new area: {new_location_name}",
            conditions={"has_explorers": True, "population": "> 5"},
            effects={
                "world_expansion": True,
                "new_location": True,
                "explorer_fame": +0.4
            },
            follow_up_events=["settlement_formation", "resource_competition", "territorial_conflict"],
            probability=0.03,
            cooldown_days=200
        )
        
        # Crisis Events
        templates["resource_crisis"] = EventTemplate(
            event_type=EventType.CRISIS,
            name="Resource Scarcity",
            description_template="Essential resources become scarce, testing the community",
            conditions={"world_resources.food": "< 0.4", "population": "> 3"},
            effects={
                "world_resources": {"food": -0.2},
                "community_stress": +0.5,
                "cooperation_test": True
            },
            follow_up_events=["rationing_system", "resource_conflict", "innovation_drive"],
            probability=0.1,
            cooldown_days=150
        )
        
        templates["disease_outbreak"] = EventTemplate(
            event_type=EventType.CRISIS,
            name="Disease Outbreak",
            description_template="A mysterious illness spreads among the community",
            conditions={"population": "> 4", "has_healers": False},
            effects={
                "health_crisis": True,
                "agent_health": -0.3,
                "isolation_behaviors": +0.4
            },
            follow_up_events=["healer_emergence", "quarantine_measures", "community_support"],
            probability=0.02,
            cooldown_days=300
        )
        
        # Cultural Events
        templates["storytelling_tradition"] = EventTemplate(
            event_type=EventType.CULTURAL,
            name="Storytelling Tradition",
            description_template="The community begins sharing stories and creating oral traditions",
            conditions={"population": "> 3, ", "has_elders": True},
            effects={
                "cultural_development": +0.3,
                "memory_preservation": +0.4,
                "community_bonding": +0.2
            },
            follow_up_events=["mythology_creation", "cultural_festival", "wisdom_keepers"],
            probability=0.07,
            cooldown_days=180
        )
        
        # Political Events
        templates["leadership_challenge"] = EventTemplate(
            event_type=EventType.POLITICAL,
            name="Leadership Challenge",
            description_template="{challenger} questions {leader}'s authority",
            conditions={"has_leader": True, "has_ambitious_agents": True},
            effects={
                "political_tension": +0.4,
                "faction_formation": +0.3,
                "leadership_instability": True
            },
            follow_up_events=["election_system", "political_exile", "power_struggle"],
            probability=0.05,
            cooldown_days=120
        )
        
        return templates
    
    def evaluate_event_conditions(self, template: EventTemplate, 
                                 world_state: Any, agents: List[Any]) -> bool:
        """Check if conditions are met for an event to occur."""
        conditions = template.conditions
        
        # Check population requirements
        if "min_agents" in conditions:
            if len([a for a in agents if a.is_alive]) < conditions["min_agents"]:
                return False
        
        # Check season requirements
        if "season" in conditions:
            if world_state.season not in conditions["season"]:
                return False
        
        # Check resource levels
        for key, value in conditions.items():
            if key.startswith("world_resources."):
                resource = key.split(".")[1]
                resource_level = world_state.resources.get(resource, 0)
                
                if isinstance(value, str):
                    # Handle comparison operators
                    if value.startswith("> "):
                        threshold = float(value[2:])
                        if resource_level <= threshold:
                            return False
                    elif value.startswith("< "):
                        threshold = float(value[2:])
                        if resource_level >= threshold:
                            return False
        
        # Check for specific agent types
        if "has_explorers" in conditions and conditions["has_explorers"]:
            has_explorer = any("adventurous" in a.traits or "curious" in a.traits 
                             for a in agents if a.is_alive)
            if not has_explorer:
                return False
        
        if "has_healers" in conditions and conditions["has_healers"]:
            has_healer = any("empathetic" in a.traits or "wise" in a.traits 
                           for a in agents if a.is_alive)
            if not has_healer:
                return False
        
        if "has_ambitious_agents" in conditions and conditions["has_ambitious_agents"]:
            has_ambitious = any("ambitious" in a.traits for a in agents if a.is_alive)
            if not has_ambitious:
                return False
        
        # Check cooldown
        if template.name in self.event_cooldowns:
            days_since = world_state.current_day - self.event_cooldowns[template.name]
            if days_since < template.cooldown_days:
                return False
        
        return True
    
    def generate_daily_events(self, world_state: Any, agents: List[Any]) -> List[Dict[str, Any]]:
        """Generate events for the current day."""
        generated_events = []
        
        for template_name, template in self.event_templates.items():
            # Check if conditions are met
            if not self.evaluate_event_conditions(template, world_state, agents):
                continue
            
            # Check probability
            if random.random() > template.probability:
                continue
            
            # Generate the event
            event_data = self._instantiate_event(template, world_state, agents)
            if event_data:
                generated_events.append(event_data)
                self.event_cooldowns[template.name] = world_state.current_day
                
                # Apply event effects
                self._apply_event_effects(event_data, template, world_state, agents)
                
                # Track for cascading events
                self.recent_events.append({
                    "template": template_name,
                    "day": world_state.current_day,
                    "data": event_data
                })
        
        # Generate follow-up events
        follow_up_events = self._generate_follow_up_events(world_state, agents)
        generated_events.extend(follow_up_events)
        
        return generated_events
    
    def _instantiate_event(self, template: EventTemplate, 
                          world_state: Any, agents: List[Any]) -> Optional[Dict[str, Any]]:
        """Create a specific instance of an event from a template."""
        alive_agents = [a for a in agents if a.is_alive]
        
        if not alive_agents:
            return None
        
        event_data = {
            "type": template.event_type.value,
            "name": template.name,
            "day": world_state.current_day,
            "participants": [],
            "location": "village_center",  # Default location
            "importance": 0.5
        }
        
        # Fill in template variables
        description = template.description_template
        
        # Select participants based on event type
        if "{agent1}" in description or "{discoverer}" in description or "{challenger}" in description:
            # Select appropriate agent
            suitable_agents = alive_agents
            
            if template.event_type == EventType.DISCOVERY:
                # Prefer explorers for discovery events
                explorers = [a for a in alive_agents if "adventurous" in a.traits or "curious" in a.traits]
                suitable_agents = explorers if explorers else alive_agents
            elif template.event_type == EventType.POLITICAL:
                # Prefer ambitious agents for political events
                ambitious = [a for a in alive_agents if "ambitious" in a.traits]
                suitable_agents = ambitious if ambitious else alive_agents
            
            main_agent = random.choice(suitable_agents)
            event_data["participants"].append(main_agent.name)
            event_data["location"] = main_agent.location
            
            # Replace placeholders
            description = description.replace("{agent1}", main_agent.name)
            description = description.replace("{discoverer}", main_agent.name)
            description = description.replace("{challenger}", main_agent.name)
        
        # Add additional participants if needed
        if "{agent2}" in description or "{student}" in description:
            remaining_agents = [a for a in alive_agents if a.name not in event_data["participants"]]
            if remaining_agents:
                second_agent = random.choice(remaining_agents)
                event_data["participants"].append(second_agent.name)
                
                description = description.replace("{agent2}", second_agent.name)
                description = description.replace("{student}", second_agent.name)
        
        if "{agent3}" in description:
            remaining_agents = [a for a in alive_agents if a.name not in event_data["participants"]]
            if remaining_agents:
                third_agent = random.choice(remaining_agents)
                event_data["participants"].append(third_agent.name)
                description = description.replace("{agent3}", third_agent.name)
        
        # Replace location placeholders
        if "{location}" in description:
            locations = list(world_state.locations.keys())
            location = random.choice(locations)
            description = description.replace("{location}", location)
            event_data["location"] = location
        
        # Replace other placeholders
        if "{new_location_name}" in description:
            new_names = ["Crystal Caves", "Whispering Grove", "Golden Plains", 
                        "Misty Peaks", "Sacred Springs", "Shadow Valley"]
            new_location = random.choice(new_names)
            description = description.replace("{new_location_name}", new_location)
        
        event_data["description"] = description
        event_data["importance"] = self._calculate_event_importance(template, event_data, agents)
        
        return event_data
    
    def _calculate_event_importance(self, template: EventTemplate, 
                                  event_data: Dict[str, Any], agents: List[Any]) -> float:
        """Calculate the importance/impact of an event."""
        base_importance = 0.5
        
        # Crisis events are generally more important
        if template.event_type == EventType.CRISIS:
            base_importance += 0.3
        
        # Events affecting more people are more important
        population = len([a for a in agents if a.is_alive])
        if len(event_data["participants"]) >= population * 0.5:
            base_importance += 0.2
        
        # Discovery and cultural events can be very important
        if template.event_type in [EventType.DISCOVERY, EventType.CULTURAL]:
            base_importance += 0.1
        
        return min(1.0, base_importance)
    
    def _apply_event_effects(self, event_data: Dict[str, Any], template: EventTemplate,
                           world_state: Any, agents: List[Any]) -> None:
        """Apply the effects of an event to the world and agents."""
        effects = template.effects
        
        # Apply world resource changes
        if "world_resources" in effects:
            for resource, change in effects["world_resources"].items():
                current = world_state.resources.get(resource, 0)
                world_state.resources[resource] = max(0, min(2.0, current + change))
        
        # Apply agent emotion changes
        if "agent_emotions" in effects:
            emotion_data = effects["agent_emotions"]
            
            for agent in agents:
                if agent.is_alive and (not event_data["participants"] or 
                                     agent.name in event_data["participants"]):
                    agent.emotion = emotion_data.get("emotion", agent.emotion)
                    agent.emotion_intensity = emotion_data.get("intensity", agent.emotion_intensity)
        
        # Apply relationship changes
        if "relationship_bonds" in effects:
            bond_change = effects["relationship_bonds"]
            participants = event_data["participants"]
            
            if len(participants) >= 2:
                # Strengthen relationships between participants
                for i, agent1_name in enumerate(participants):
                    for agent2_name in participants[i+1:]:
                        agent1 = next((a for a in agents if a.name == agent1_name), None)
                        agent2 = next((a for a in agents if a.name == agent2_name), None)
                        
                        if agent1 and agent2:
                            # Strengthen their relationship
                            current_rel = agent1.relationships.get(agent2_name, "stranger")
                            if current_rel == "stranger" and bond_change > 0:
                                agent1.relationships[agent2_name] = "acquaintance"
                                agent2.relationships[agent1_name] = "acquaintance"
                            elif current_rel == "acquaintance" and bond_change > 0.3:
                                agent1.relationships[agent2_name] = "friend"
                                agent2.relationships[agent1_name] = "friend"
    
    def _generate_follow_up_events(self, world_state: Any, agents: List[Any]) -> List[Dict[str, Any]]:
        """Generate events that follow from recent events."""
        follow_up_events = []
        
        # Look at recent events for potential follow-ups
        for recent_event in self.recent_events[-7:]:  # Last week's events
            template = self.event_templates.get(recent_event["template"])
            if not template or not template.follow_up_events:
                continue
            
            # Small chance for follow-up
            if random.random() < 0.2:  # 20% chance for follow-up
                follow_up_name = random.choice(template.follow_up_events)
                
                # Generate a simple follow-up event
                follow_up = {
                    "type": "follow_up",
                    "name": f"Aftermath: {follow_up_name.replace('_', ' ').title()}",
                    "description": f"The community deals with the aftermath of {template.name}",
                    "day": world_state.current_day,
                    "participants": recent_event["data"]["participants"],
                    "location": recent_event["data"]["location"],
                    "importance": recent_event["data"]["importance"] * 0.7,
                    "parent_event": recent_event["template"]
                }
                
                follow_up_events.append(follow_up)
        
        return follow_up_events
    
    def get_event_history_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get a summary of recent events for analysis."""
        recent = [e for e in self.recent_events if e["day"] >= (max([e["day"] for e in self.recent_events]) - days)]
        
        event_types = {}
        participants = {}
        
        for event in recent:
            event_type = event.get("data", {}).get("type", "unknown")
            event_types[event_type] = event_types.get(event_type, 0) + 1
            
            for participant in event.get("data", {}).get("participants", []):
                participants[participant] = participants.get(participant, 0) + 1
        
        return {
            "total_events": len(recent),
            "event_types": event_types,
            "most_active_agents": sorted(participants.items(), key=lambda x: x[1], reverse=True)[:5],
            "timeline": [{"day": e["day"], "name": e["data"]["name"]} for e in recent]
        } 