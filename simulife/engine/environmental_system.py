"""
Environmental Impact System for SimuLife
Makes weather, seasons, and environmental conditions significantly affect agent behavior.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class WeatherSeverity(Enum):
    """Severity levels for weather conditions."""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    EXTREME = "extreme"


@dataclass
class EnvironmentalCondition:
    """Represents current environmental conditions."""
    weather: str
    season: str
    temperature: str
    severity: WeatherSeverity
    effects: Dict[str, float]  # Effects on various aspects
    duration_days: int


@dataclass
class LocationEnvironment:
    """Environmental characteristics of a location."""
    name: str
    base_safety: float  # How safe the location is
    resource_abundance: Dict[str, float]  # Resource availability
    weather_resistance: float  # How well it protects from weather
    seasonal_modifiers: Dict[str, Dict[str, float]]  # Season-specific effects


class EnvironmentalSystem:
    """
    Manages environmental effects on agent behavior and world state.
    """
    
    def __init__(self):
        self.current_conditions = []
        self.location_environments = self._initialize_locations()
        self.environmental_memory = {}  # Track past conditions
        self.adaptation_levels = {}  # How well agents adapt to conditions
        
    def _initialize_locations(self) -> Dict[str, LocationEnvironment]:
        """Initialize environmental characteristics for each location."""
        locations = {
            "village_center": LocationEnvironment(
                name="village_center",
                base_safety=0.8,
                resource_abundance={"food": 0.6, "water": 0.7, "shelter": 0.9, "materials": 0.5},
                weather_resistance=0.7,
                seasonal_modifiers={
                    "spring": {"safety": 0.1, "food": 0.2},
                    "summer": {"food": 0.3, "water": -0.1},
                    "autumn": {"food": 0.1, "materials": 0.2},
                    "winter": {"safety": -0.2, "food": -0.3, "water": -0.1}
                }
            ),
            "forest": LocationEnvironment(
                name="forest",
                base_safety=0.6,
                resource_abundance={"food": 0.8, "water": 0.5, "materials": 0.9, "shelter": 0.4},
                weather_resistance=0.6,
                seasonal_modifiers={
                    "spring": {"food": 0.3, "materials": 0.2},
                    "summer": {"food": 0.2, "safety": -0.1},
                    "autumn": {"food": 0.4, "materials": 0.3},
                    "winter": {"safety": -0.3, "food": -0.4, "materials": -0.2}
                }
            ),
            "river": LocationEnvironment(
                name="river",
                base_safety=0.7,
                resource_abundance={"water": 1.0, "food": 0.7, "materials": 0.3, "shelter": 0.2},
                weather_resistance=0.3,
                seasonal_modifiers={
                    "spring": {"water": 0.2, "food": 0.3, "safety": -0.1},
                    "summer": {"food": 0.2},
                    "autumn": {"food": 0.1},
                    "winter": {"safety": -0.4, "water": -0.3, "food": -0.3}
                }
            ),
            "mountains": LocationEnvironment(
                name="mountains",
                base_safety=0.4,
                resource_abundance={"materials": 1.0, "shelter": 0.8, "food": 0.2, "water": 0.4},
                weather_resistance=0.8,
                seasonal_modifiers={
                    "spring": {"safety": 0.1, "materials": 0.1},
                    "summer": {"safety": 0.2, "food": 0.1},
                    "autumn": {"materials": 0.2},
                    "winter": {"safety": -0.5, "food": -0.4, "water": -0.2}
                }
            ),
            "fields": LocationEnvironment(
                name="fields",
                base_safety=0.8,
                resource_abundance={"food": 1.0, "materials": 0.4, "water": 0.3, "shelter": 0.1},
                weather_resistance=0.2,
                seasonal_modifiers={
                    "spring": {"food": 0.4, "safety": 0.1},
                    "summer": {"food": 0.5},
                    "autumn": {"food": 0.3, "materials": 0.2},
                    "winter": {"safety": -0.4, "food": -0.6}
                }
            )
        }
        return locations

    def assess_environmental_impact(self, agent: Any, world_state: Any) -> Dict[str, float]:
        """Assess how current environmental conditions affect an agent."""
        location_env = self.location_environments.get(agent.location, None)
        if not location_env:
            return {}
        
        impact = {
            "safety_modifier": 0.0,
            "resource_access": 0.0,
            "energy_drain": 0.0,
            "health_effect": 0.0,
            "mood_effect": 0.0,
            "action_restrictions": 0.0
        }
        
        # Base location effects
        impact["safety_modifier"] = location_env.base_safety - 0.5
        
        # Seasonal effects
        season = world_state.season
        seasonal_mods = location_env.seasonal_modifiers.get(season, {})
        for effect, value in seasonal_mods.items():
            if effect == "safety":
                impact["safety_modifier"] += value
            elif effect == "food":
                impact["resource_access"] += value * 0.5
        
        # Weather effects
        weather = world_state.weather
        weather_impact = self._calculate_weather_impact(weather, location_env, agent)
        for key, value in weather_impact.items():
            impact[key] += value
        
        # Agent adaptation effects
        adaptation = self._get_agent_adaptation(agent, world_state)
        impact["energy_drain"] *= (1.0 - adaptation * 0.5)
        impact["health_effect"] *= (1.0 - adaptation * 0.3)
        
        return impact

    def _calculate_weather_impact(self, weather: str, location_env: LocationEnvironment, 
                                agent: Any) -> Dict[str, float]:
        """Calculate weather-specific impacts."""
        impact = {
            "safety_modifier": 0.0,
            "resource_access": 0.0,
            "energy_drain": 0.0,
            "health_effect": 0.0,
            "mood_effect": 0.0,
            "action_restrictions": 0.0
        }
        
        weather_effects = {
            "clear": {"mood_effect": 0.1},
            "sunny": {"mood_effect": 0.2, "energy_drain": 0.05},
            "rainy": {"resource_access": 0.1, "mood_effect": -0.1, "action_restrictions": 0.2},
            "stormy": {"safety_modifier": -0.3, "energy_drain": 0.15, "action_restrictions": 0.4},
            "windy": {"action_restrictions": 0.1, "energy_drain": 0.05},
            "cloudy": {},
            "hot": {"energy_drain": 0.1, "health_effect": -0.05},
            "cold": {"energy_drain": 0.15, "health_effect": -0.1, "resource_access": -0.1},
            "snowy": {"safety_modifier": -0.2, "energy_drain": 0.2, "action_restrictions": 0.3},
            "icy": {"safety_modifier": -0.4, "action_restrictions": 0.5, "health_effect": -0.15}
        }
        
        base_effects = weather_effects.get(weather, {})
        for effect, value in base_effects.items():
            impact[effect] = value
        
        # Modify based on location's weather resistance
        resistance = location_env.weather_resistance
        impact["safety_modifier"] *= (1.0 - resistance * 0.5)
        impact["energy_drain"] *= (1.0 - resistance * 0.3)
        impact["action_restrictions"] *= (1.0 - resistance * 0.4)
        
        # Agent trait modifications
        if "resilient" in agent.traits:
            impact["health_effect"] *= 0.7
            impact["energy_drain"] *= 0.8
        if "adaptive" in agent.traits:
            impact["action_restrictions"] *= 0.8
        if "fragile" in agent.traits:
            impact["health_effect"] *= 1.3
            impact["energy_drain"] *= 1.2
        
        return impact

    def _get_agent_adaptation(self, agent: Any, world_state: Any) -> float:
        """Get how well an agent has adapted to current conditions."""
        adaptation_key = f"{agent.name}_{world_state.season}_{agent.location}"
        
        # Base adaptation starts at 0, improves over time
        if adaptation_key not in self.adaptation_levels:
            self.adaptation_levels[adaptation_key] = 0.0
        
        # Adaptation improves slowly over time spent in conditions
        current_adaptation = self.adaptation_levels[adaptation_key]
        
        # Certain traits help with adaptation
        trait_bonus = 0.0
        if "adaptable" in agent.traits:
            trait_bonus += 0.3
        if "practical" in agent.traits:
            trait_bonus += 0.2
        if "resilient" in agent.traits:
            trait_bonus += 0.2
        
        return min(1.0, current_adaptation + trait_bonus)

    def modify_action_for_environment(self, agent: Any, base_action: str, 
                                   world_state: Any) -> str:
        """Modify an agent's action based on environmental conditions."""
        impact = self.assess_environmental_impact(agent, world_state)
        
        # Severe weather restrictions
        if impact.get("action_restrictions", 0) > 0.4:
            return self._generate_weather_restricted_action(agent, world_state, base_action)
        
        # Moderate environmental pressure
        elif impact.get("energy_drain", 0) > 0.1 or impact.get("health_effect", 0) < -0.05:
            return self._modify_action_for_conditions(agent, base_action, world_state, impact)
        
        # Good conditions might encourage specific activities
        elif impact.get("mood_effect", 0) > 0.1:
            return self._enhance_action_for_good_conditions(agent, base_action, world_state)
        
        return base_action

    def _generate_weather_restricted_action(self, agent: Any, world_state: Any, 
                                          base_action: str) -> str:
        """Generate actions for severe weather conditions."""
        weather = world_state.weather
        location = agent.location
        
        weather_actions = {
            "stormy": [
                f"{agent.name} takes shelter from the storm in {location}",
                f"{agent.name} secures their belongings against the storm",
                f"{agent.name} waits out the storm safely indoors"
            ],
            "snowy": [
                f"{agent.name} focuses on staying warm during the snowfall",
                f"{agent.name} carefully navigates the snowy conditions in {location}",
                f"{agent.name} gathers materials to improve insulation"
            ],
            "icy": [
                f"{agent.name} moves very carefully to avoid slipping on ice",
                f"{agent.name} stays close to safe shelter due to icy conditions",
                f"{agent.name} helps others navigate the dangerous icy terrain"
            ]
        }
        
        actions = weather_actions.get(weather, [
            f"{agent.name} adapts their activities to the harsh {weather} conditions"
        ])
        
        return random.choice(actions)

    def _modify_action_for_conditions(self, agent: Any, base_action: str, 
                                    world_state: Any, impact: Dict[str, float]) -> str:
        """Modify action for moderate environmental pressure."""
        weather = world_state.weather
        season = world_state.season
        
        # If action involves outdoor activities during harsh conditions
        if any(keyword in base_action.lower() for keyword in ["explore", "travel", "venture", "wander"]):
            if impact.get("energy_drain", 0) > 0.1:
                return f"{agent.name} carefully {base_action.split(' ', 1)[1]} despite the {weather} weather"
            
        # If health effects are significant
        if impact.get("health_effect", 0) < -0.05:
            if "rest" not in base_action.lower():
                return f"{agent.name} takes extra care while {base_action.split(' ', 1)[1]} due to the harsh {weather}"
        
        # Winter-specific modifications
        if season == "winter":
            if "socialize" in base_action.lower():
                return f"{agent.name} seeks warm companionship with others during the cold {season}"
            elif "work" in base_action.lower():
                return f"{agent.name} works efficiently to stay warm in the {season} cold"
        
        # Summer-specific modifications  
        elif season == "summer":
            if "active" in base_action.lower() or "work" in base_action.lower():
                return f"{agent.name} {base_action.split(' ', 1)[1]} during cooler parts of the day"
        
        return base_action

    def _enhance_action_for_good_conditions(self, agent: Any, base_action: str, 
                                          world_state: Any) -> str:
        """Enhance actions when environmental conditions are favorable."""
        weather = world_state.weather
        season = world_state.season
        
        if weather in ["clear", "sunny"]:
            if "explore" in base_action.lower():
                return f"{agent.name} enthusiastically explores, enjoying the beautiful {weather} weather"
            elif "socialize" in base_action.lower():
                return f"{agent.name} enjoys socializing in the pleasant {weather} conditions"
            elif "work" in base_action.lower():
                return f"{agent.name} works productively, energized by the {weather} day"
        
        if season == "spring":
            if "goals" in base_action.lower() or "personal" in base_action.lower():
                return f"{agent.name} feels renewed energy for their goals with the arrival of {season}"
        
        return base_action

    def process_environmental_effects(self, agents: List[Any], world_state: Any, 
                                    world_day: int) -> List[Dict[str, Any]]:
        """Process daily environmental effects on all agents."""
        environmental_events = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
                
            impact = self.assess_environmental_impact(agent, world_state)
            
            # Apply health effects
            if impact.get("health_effect", 0) != 0:
                agent.health = max(0.1, min(1.0, agent.health + impact["health_effect"]))
                
                if impact["health_effect"] < -0.1:
                    environmental_events.append({
                        "type": "health_impact",
                        "agent": agent.name,
                        "effect": "negative",
                        "cause": f"{world_state.weather} weather in {agent.location}",
                        "day": world_day
                    })
            
            # Apply mood effects
            if impact.get("mood_effect", 0) != 0:
                if impact["mood_effect"] > 0.15:
                    agent.emotion = "cheerful"
                    agent.emotion_intensity = min(1.0, agent.emotion_intensity + 0.2)
                elif impact["mood_effect"] < -0.15:
                    agent.emotion = "gloomy"
                    agent.emotion_intensity = min(1.0, agent.emotion_intensity + 0.3)
            
            # Apply energy effects
            if impact.get("energy_drain", 0) > 0.1:
                if hasattr(agent, 'energy'):
                    agent.energy = max(0.1, agent.energy - impact["energy_drain"])
            
            # Update adaptation levels
            adaptation_key = f"{agent.name}_{world_state.season}_{agent.location}"
            current_adaptation = self.adaptation_levels.get(adaptation_key, 0.0)
            self.adaptation_levels[adaptation_key] = min(1.0, current_adaptation + 0.01)
            
            # Severe weather events
            if impact.get("safety_modifier", 0) < -0.3:
                environmental_events.append({
                    "type": "weather_hazard",
                    "agent": agent.name,
                    "location": agent.location,
                    "weather": world_state.weather,
                    "severity": "high",
                    "day": world_day
                })
        
        # Location-wide effects
        location_effects = self._process_location_effects(world_state, world_day)
        environmental_events.extend(location_effects)
        
        return environmental_events

    def _process_location_effects(self, world_state: Any, world_day: int) -> List[Dict[str, Any]]:
        """Process location-wide environmental effects."""
        events = []
        
        # Severe weather affecting entire locations
        if world_state.weather in ["stormy", "snowy", "icy"]:
            for location_name, location_env in self.location_environments.items():
                if location_env.weather_resistance < 0.5:  # Vulnerable locations
                    events.append({
                        "type": "location_weather_impact",
                        "location": location_name,
                        "weather": world_state.weather,
                        "effect": "resource_disruption",
                        "day": world_day
                    })
        
        # Seasonal transitions
        if world_day % 90 == 0:  # Season change
            events.append({
                "type": "seasonal_transition",
                "new_season": world_state.season,
                "day": world_day
            })
        
        return events

    def get_location_attractiveness(self, location_name: str, world_state: Any, 
                                  agent: Any = None) -> float:
        """Calculate how attractive a location is given current conditions."""
        location_env = self.location_environments.get(location_name)
        if not location_env:
            return 0.5
        
        attractiveness = location_env.base_safety
        
        # Seasonal modifiers
        seasonal_mods = location_env.seasonal_modifiers.get(world_state.season, {})
        for effect, value in seasonal_mods.items():
            if effect == "safety":
                attractiveness += value
            elif effect in ["food", "water", "materials"]:
                attractiveness += value * 0.3
        
        # Weather resistance bonus during bad weather
        if world_state.weather in ["stormy", "snowy", "icy"]:
            attractiveness += location_env.weather_resistance * 0.4
        
        # Agent-specific attractiveness
        if agent:
            # Resource needs
            if hasattr(agent, 'personal_resources'):
                for resource, abundance in location_env.resource_abundance.items():
                    need_level = 1.0 - agent.personal_resources.get(resource, 0.5)
                    attractiveness += need_level * abundance * 0.2
            
            # Trait preferences
            if "practical" in agent.traits and location_env.resource_abundance.get("materials", 0) > 0.7:
                attractiveness += 0.2
            if "curious" in agent.traits and location_name in ["forest", "mountains"]:
                attractiveness += 0.1
            if "social" in agent.traits and location_name == "village_center":
                attractiveness += 0.2
        
        return min(1.0, max(0.0, attractiveness))

    def to_dict(self) -> Dict[str, Any]:
        """Serialize environmental system state."""
        return {
            "adaptation_levels": self.adaptation_levels,
            "environmental_memory": self.environmental_memory,
            "location_environments": {
                name: {
                    "base_safety": env.base_safety,
                    "resource_abundance": env.resource_abundance,
                    "weather_resistance": env.weather_resistance,
                    "seasonal_modifiers": env.seasonal_modifiers
                } for name, env in self.location_environments.items()
            }
        } 