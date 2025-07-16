"""
World State Management for SimuLife
Tracks global environment, weather, events, and world history.
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class WorldEvent:
    """Represents a significant event in the world."""
    event_id: str
    day: int
    event_type: str  # conflict, celebration, disaster, discovery, etc.
    description: str
    participants: List[str]  # Agent names involved
    location: str
    importance: float
    consequences: List[str]


class WorldState:
    """
    Manages the global state of the SimuLife world.
    Tracks environment, events, factions, and world progression.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        # Time and progression
        self.current_day = config.get("current_day", 0) if config else 0
        self.season = config.get("season", "spring") if config else "spring"
        self.year = config.get("year", 1) if config else 1
        
        # Environment
        self.weather = config.get("weather", "clear") if config else "clear"
        self.temperature = config.get("temperature", "mild") if config else "mild"
        self.resources = config.get("resources", {
            "food": 1.0,
            "water": 1.0,
            "shelter": 1.0,
            "knowledge": 0.5
        }) if config else {
            "food": 1.0,
            "water": 1.0,
            "shelter": 1.0,
            "knowledge": 0.5
        }
        
        # World events and history
        self.events: List[WorldEvent] = []
        self.event_counter = 0
        
        # Locations and geography
        self.locations = config.get("locations", {
            "village_center": "The heart of the community where people gather",
            "forest": "A mysterious woodland area rich with resources",
            "river": "A flowing source of water and life",
            "mountains": "Tall peaks that offer perspective and challenge",
            "fields": "Open areas for farming and contemplation"
        }) if config else {
            "village_center": "The heart of the community where people gather",
            "forest": "A mysterious woodland area rich with resources",
            "river": "A flowing source of water and life",
            "mountains": "Tall peaks that offer perspective and challenge",
            "fields": "Open areas for farming and contemplation"
        }
        
        # Factions and groups (will grow organically)
        self.factions: Dict[str, Dict] = config.get("factions", {}) if config else {}
        
        # World beliefs and customs (emergent culture)
        self.beliefs: Dict[str, Any] = config.get("beliefs", {}) if config else {}
        self.customs: List[str] = config.get("customs", []) if config else []
        
        # Population stats
        self.population_stats = {
            "total_agents": 0,
            "births": 0,
            "deaths": 0,
            "average_age": 0
        }

    def advance_day(self) -> None:
        """Advance the world by one day and update environmental factors."""
        self.current_day += 1
        
        # Update season and year
        days_per_season = 90
        if self.current_day % (days_per_season * 4) == 0:
            self.year += 1
        
        season_day = self.current_day % (days_per_season * 4)
        if season_day < days_per_season:
            self.season = "spring"
        elif season_day < days_per_season * 2:
            self.season = "summer"
        elif season_day < days_per_season * 3:
            self.season = "autumn"
        else:
            self.season = "winter"
        
        # Random weather changes
        self._update_weather()
        
        # Random resource fluctuations
        self._update_resources()
        
        # Chance for random world events
        if random.random() < 0.1:  # 10% chance per day
            self._generate_random_event()

    def _update_weather(self) -> None:
        """Update weather based on season and randomness."""
        weather_options = {
            "spring": ["clear", "rainy", "cloudy", "windy"],
            "summer": ["clear", "hot", "sunny", "stormy"],
            "autumn": ["cloudy", "windy", "rainy", "cool"],
            "winter": ["cold", "snowy", "cloudy", "icy"]
        }
        
        # 70% chance to keep current weather, 30% to change
        if random.random() < 0.3:
            self.weather = random.choice(weather_options.get(self.season, ["clear"]))

    def _update_resources(self) -> None:
        """Update resource availability based on season and events."""
        # Seasonal effects on resources
        resource_modifiers = {
            "spring": {"food": 0.02, "water": 0.01},
            "summer": {"food": 0.03, "water": -0.01},
            "autumn": {"food": 0.01, "water": 0.0},
            "winter": {"food": -0.02, "water": -0.01}
        }
        
        modifiers = resource_modifiers.get(self.season, {})
        for resource, change in modifiers.items():
            if resource in self.resources:
                self.resources[resource] = max(0.0, min(2.0, 
                    self.resources[resource] + change + random.uniform(-0.01, 0.01)))

    def _generate_random_event(self) -> None:
        """Generate a random world event."""
        event_types = [
            "weather_change",
            "resource_discovery", 
            "natural_phenomenon",
            "mysterious_occurrence"
        ]
        
        event_type = random.choice(event_types)
        event_descriptions = {
            "weather_change": "A sudden change in weather patterns affects the region",
            "resource_discovery": "New resources have been discovered in the area",
            "natural_phenomenon": "Strange lights appear in the sky, puzzling everyone",
            "mysterious_occurrence": "Unexplained events occur that spark curiosity and debate"
        }
        
        event = WorldEvent(
            event_id=f"world_event_{self.event_counter}",
            day=self.current_day,
            event_type=event_type,
            description=event_descriptions.get(event_type, "Something interesting happened"),
            participants=[],
            location=random.choice(list(self.locations.keys())),
            importance=random.uniform(0.3, 0.8),
            consequences=[]
        )
        
        self.events.append(event)
        self.event_counter += 1

    def add_agent_event(self, agent_names: List[str], event_type: str, 
                       description: str, location: str, importance: float = 0.5) -> WorldEvent:
        """Add an event involving specific agents."""
        event = WorldEvent(
            event_id=f"agent_event_{self.event_counter}",
            day=self.current_day,
            event_type=event_type,
            description=description,
            participants=agent_names,
            location=location,
            importance=importance,
            consequences=[]
        )
        
        self.events.append(event)
        self.event_counter += 1
        return event

    def get_recent_events(self, days: int = 7) -> List[WorldEvent]:
        """Get events from the last N days."""
        cutoff_day = self.current_day - days
        return [event for event in self.events if event.day >= cutoff_day]

    def get_important_events(self, threshold: float = 0.7) -> List[WorldEvent]:
        """Get events above importance threshold."""
        return [event for event in self.events if event.importance >= threshold]

    def add_faction(self, name: str, leader: str, members: List[str], 
                   ideology: str, location: str) -> None:
        """Add a new faction to the world."""
        self.factions[name] = {
            "leader": leader,
            "members": members,
            "ideology": ideology,
            "location": location,
            "founded_day": self.current_day,
            "reputation": 0.5,
            "territory": [location]
        }

    def add_belief(self, belief_name: str, description: str, 
                  believers: List[str], origin_day: int = None) -> None:
        """Add a new belief system to the world."""
        self.beliefs[belief_name] = {
            "description": description,
            "believers": believers,
            "origin_day": origin_day or self.current_day,
            "strength": len(believers) / max(1, self.population_stats["total_agents"])
        }

    def add_custom(self, custom_name: str, description: str, 
                  participants: List[str]) -> None:
        """Add a new custom or tradition."""
        self.customs.append({
            "name": custom_name,
            "description": description,
            "participants": participants,
            "established_day": self.current_day
        })

    def get_world_description(self) -> str:
        """Get a narrative description of the current world state."""
        desc_parts = [
            f"Day {self.current_day} of Year {self.year}, {self.season} season.",
            f"The weather is {self.weather}."
        ]
        
        # Resource status
        resource_status = []
        for resource, level in self.resources.items():
            if level > 1.2:
                status = "abundant"
            elif level > 0.8:
                status = "adequate"
            elif level > 0.4:
                status = "scarce"
            else:
                status = "critically low"
            resource_status.append(f"{resource} is {status}")
        
        if resource_status:
            desc_parts.append("Resources: " + ", ".join(resource_status) + ".")
        
        # Recent events
        recent_events = self.get_recent_events(days=3)
        if recent_events:
            desc_parts.append(f"Recent events include: {recent_events[-1].description}")
        
        # Factions
        if self.factions:
            faction_names = list(self.factions.keys())
            desc_parts.append(f"Active factions: {', '.join(faction_names[:3])}")
        
        return " ".join(desc_parts)

    def update_population_stats(self, total_agents: int, births: int = 0, deaths: int = 0, 
                              average_age: float = 0) -> None:
        """Update population statistics."""
        self.population_stats = {
            "total_agents": total_agents,
            "births": births,
            "deaths": deaths,
            "average_age": average_age
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize world state to dictionary."""
        return {
            "current_day": self.current_day,
            "season": self.season,
            "year": self.year,
            "weather": self.weather,
            "temperature": self.temperature,
            "resources": self.resources,
            "events": [asdict(event) for event in self.events[-50:]],  # Keep recent events
            "locations": self.locations,
            "factions": self.factions,
            "beliefs": self.beliefs,
            "customs": self.customs,
            "population_stats": self.population_stats
        }

    def save_to_file(self, filepath: str) -> None:
        """Save world state to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_from_file(cls, filepath: str) -> 'WorldState':
        """Load world state from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Reconstruct events
        world = cls(data)
        world.events = []
        for event_data in data.get("events", []):
            event = WorldEvent(**event_data)
            world.events.append(event)
        
        return world 