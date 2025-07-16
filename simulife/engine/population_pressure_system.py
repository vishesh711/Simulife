"""
Population Pressure System for SimuLife
Handles population-driven resource scarcity, migration, conflicts, and carrying capacity.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum


class PopulationPressureLevel(Enum):
    """Levels of population pressure."""
    UNDERPOPULATED = "underpopulated"
    SUSTAINABLE = "sustainable"
    APPROACHING_LIMIT = "approaching_limit"
    OVERPOPULATED = "overpopulated"
    CRITICALLY_OVERPOPULATED = "critically_overpopulated"


class MigrationCause(Enum):
    """Reasons for population migration."""
    OVERPOPULATION = "overpopulation"
    RESOURCE_SCARCITY = "resource_scarcity"
    CONFLICT_DISPLACEMENT = "conflict_displacement"
    EXPLORATION = "exploration"
    FAMILY_FOLLOWING = "family_following"
    ENVIRONMENTAL_PRESSURE = "environmental_pressure"
    OPPORTUNITY_SEEKING = "opportunity_seeking"


class ResourceScarcityType(Enum):
    """Types of resource scarcity."""
    FOOD_SHORTAGE = "food_shortage"
    WATER_SHORTAGE = "water_shortage"
    SHELTER_SHORTAGE = "shelter_shortage"
    MATERIALS_SHORTAGE = "materials_shortage"
    SPACE_SHORTAGE = "space_shortage"
    EMPLOYMENT_SHORTAGE = "employment_shortage"


@dataclass
class CarryingCapacity:
    """Carrying capacity for a location."""
    location: str
    base_capacity: int              # Base number of agents supportable
    current_capacity: int           # Current capacity with improvements
    technology_modifier: float     # Technology improvements to capacity
    resource_modifier: float       # Resource availability modifier
    environmental_modifier: float  # Environmental condition modifier
    infrastructure_level: int      # Level of built infrastructure
    last_updated: int              # Day when capacity was last calculated


@dataclass
class MigrationEvent:
    """Represents a migration event."""
    migrants: List[str]            # Agent names migrating
    origin_location: str
    destination_location: str
    migration_cause: MigrationCause
    day: int
    group_migration: bool          # Whether families/groups migrate together
    success_probability: float    # Chance of successful migration
    resources_taken: Dict[str, float]  # Resources migrants take with them


@dataclass
class PopulationPressureData:
    """Data about population pressure in a location."""
    location: str
    current_population: int
    carrying_capacity: int
    pressure_level: PopulationPressureLevel
    pressure_score: float          # 0.0 = no pressure, 2.0+ = extreme pressure
    resource_shortage: Dict[str, float]  # Resource availability ratios
    growth_rate: float             # Recent population growth rate
    sustainability_trend: str      # improving, stable, declining


class PopulationPressureSystem:
    """
    Manages population pressure, carrying capacity, migration, and resource conflicts.
    """
    
    def __init__(self):
        self.carrying_capacities: Dict[str, CarryingCapacity] = {}
        self.population_data: Dict[str, PopulationPressureData] = {}
        self.migration_history: List[MigrationEvent] = []
        self.resource_conflicts: List[Dict[str, Any]] = []
        
        # Configuration
        self.base_carrying_capacities = self._initialize_base_capacities()
        self.migration_patterns = {
            "family_cohesion": 0.7,    # Chance families migrate together
            "group_migration": 0.4,    # Chance of group migration
            "return_migration": 0.2,   # Chance of returning to origin
            "exploration_rate": 0.1    # Chance of exploring new locations
        }
        
        # Population thresholds
        self.pressure_thresholds = {
            "sustainable_max": 0.8,      # 80% of capacity = sustainable
            "approaching_limit": 0.9,    # 90% of capacity = approaching limit
            "overpopulated": 1.1,        # 110% of capacity = overpopulated
            "critical": 1.3              # 130% of capacity = critical
        }
    
    def _initialize_base_capacities(self) -> Dict[str, int]:
        """Initialize base carrying capacities for different locations."""
        return {
            "village_center": 15,    # Central area with good infrastructure
            "forest": 8,             # Rich resources but limited space
            "river": 12,             # Good water access
            "mountains": 6,          # Harsh conditions, limited capacity
            "fields": 20,            # Large area, good for agriculture
            "coastal": 18,           # Access to ocean resources
            "desert": 3,             # Very harsh conditions
            "valley": 16,            # Protected, fertile area
            "hills": 10,             # Moderate capacity
            "plains": 25             # Large, open area
        }
    
    def initialize_location_capacity(self, location: str, agents: List[Any]) -> CarryingCapacity:
        """Initialize carrying capacity for a location."""
        base_capacity = self.base_carrying_capacities.get(location, 10)
        
        # Calculate current capacity based on various factors
        technology_modifier = self._calculate_technology_modifier(location, agents)
        resource_modifier = self._calculate_resource_modifier(location)
        environmental_modifier = self._calculate_environmental_modifier(location)
        infrastructure_level = self._calculate_infrastructure_level(location, agents)
        
        current_capacity = int(base_capacity * technology_modifier * 
                             resource_modifier * environmental_modifier * 
                             (1 + infrastructure_level * 0.1))
        
        capacity = CarryingCapacity(
            location=location,
            base_capacity=base_capacity,
            current_capacity=current_capacity,
            technology_modifier=technology_modifier,
            resource_modifier=resource_modifier,
            environmental_modifier=environmental_modifier,
            infrastructure_level=infrastructure_level,
            last_updated=0
        )
        
        self.carrying_capacities[location] = capacity
        return capacity
    
    def _calculate_technology_modifier(self, location: str, agents: List[Any]) -> float:
        """Calculate technology impact on carrying capacity."""
        # Count agents with relevant technologies
        relevant_techs = ["agriculture", "construction", "medicine", "water_purification"]
        tech_count = 0
        
        location_agents = [a for a in agents if a.location == location and a.is_alive]
        for agent in location_agents:
            if hasattr(agent, 'technologies'):
                tech_count += len([t for t in agent.technologies if t in relevant_techs])
        
        # Technology increases capacity
        return 1.0 + min(tech_count * 0.1, 0.5)  # Max 50% increase from technology
    
    def _calculate_resource_modifier(self, location: str) -> float:
        """Calculate resource availability impact on carrying capacity."""
        # Location-specific resource availability
        resource_factors = {
            "village_center": 1.0,
            "forest": 1.2,        # Rich in materials
            "river": 1.3,         # Abundant water
            "mountains": 0.7,     # Limited resources
            "fields": 1.4,        # Good for food production
            "coastal": 1.1,       # Ocean resources
            "desert": 0.4,        # Very limited resources
            "valley": 1.2,        # Protected and fertile
            "hills": 0.9,         # Moderate resources
            "plains": 1.1         # Open space
        }
        
        return resource_factors.get(location, 1.0)
    
    def _calculate_environmental_modifier(self, location: str) -> float:
        """Calculate environmental condition impact on carrying capacity."""
        # This could be expanded to include weather, climate, disasters
        environmental_factors = {
            "village_center": 1.0,
            "forest": 0.9,        # Some environmental challenges
            "river": 1.1,         # Good water access
            "mountains": 0.8,     # Harsh conditions
            "fields": 1.0,        # Stable environment
            "coastal": 0.95,      # Some weather exposure
            "desert": 0.6,        # Very harsh
            "valley": 1.1,        # Protected environment
            "hills": 0.9,         # Moderate challenges
            "plains": 0.95        # Some exposure
        }
        
        return environmental_factors.get(location, 1.0)
    
    def _calculate_infrastructure_level(self, location: str, agents: List[Any]) -> int:
        """Calculate infrastructure development level."""
        # Count agents with construction/crafting skills
        location_agents = [a for a in agents if a.location == location and a.is_alive]
        infrastructure_score = 0
        
        for agent in location_agents:
            if hasattr(agent, 'skills'):
                construction_skill = agent.skills.get('construction', 0)
                crafting_skill = agent.skills.get('crafting', 0)
                if isinstance(construction_skill, float):
                    infrastructure_score += construction_skill
                if isinstance(crafting_skill, float):
                    infrastructure_score += crafting_skill
        
        # Convert to infrastructure level (0-5)
        return min(int(infrastructure_score / 2), 5)
    
    def process_daily_population_pressure(self, agents: List[Any], world_resources: Dict[str, float], 
                                        current_day: int) -> List[Dict[str, Any]]:
        """Process daily population pressure effects."""
        pressure_events = []
        
        # Update population data for all locations
        self._update_population_data(agents, current_day)
        
        # Process pressure effects for each location
        for location, pop_data in self.population_data.items():
            location_events = self._process_location_pressure(location, pop_data, agents, 
                                                            world_resources, current_day)
            pressure_events.extend(location_events)
        
        # Process migration attempts
        migration_events = self._process_migration_attempts(agents, current_day)
        pressure_events.extend(migration_events)
        
        # Check for resource conflicts
        conflict_events = self._check_resource_conflicts(agents, current_day)
        pressure_events.extend(conflict_events)
        
        return pressure_events
    
    def _update_population_data(self, agents: List[Any], current_day: int):
        """Update population data for all locations."""
        # Count population by location
        location_populations = {}
        for agent in agents:
            if agent.is_alive:
                location = agent.location
                location_populations[location] = location_populations.get(location, 0) + 1
        
        # Update population data for each location
        for location, population in location_populations.items():
            # Initialize capacity if needed
            if location not in self.carrying_capacities:
                self.initialize_location_capacity(location, agents)
            
            capacity = self.carrying_capacities[location].current_capacity
            pressure_score = population / capacity if capacity > 0 else 2.0
            
            # Determine pressure level
            if pressure_score < self.pressure_thresholds["sustainable_max"]:
                pressure_level = PopulationPressureLevel.SUSTAINABLE
            elif pressure_score < self.pressure_thresholds["approaching_limit"]:
                pressure_level = PopulationPressureLevel.APPROACHING_LIMIT
            elif pressure_score < self.pressure_thresholds["overpopulated"]:
                pressure_level = PopulationPressureLevel.OVERPOPULATED
            elif pressure_score < self.pressure_thresholds["critical"]:
                pressure_level = PopulationPressureLevel.CRITICALLY_OVERPOPULATED
            else:
                pressure_level = PopulationPressureLevel.CRITICALLY_OVERPOPULATED
            
            # Check for underpopulation
            if pressure_score < 0.3:  # Less than 30% of capacity
                pressure_level = PopulationPressureLevel.UNDERPOPULATED
            
            # Calculate resource shortages
            resource_shortage = self._calculate_resource_shortages(location, population, capacity)
            
            # Calculate growth rate (simplified)
            prev_data = self.population_data.get(location)
            growth_rate = 0.0
            if prev_data:
                # Simple growth rate calculation - this would be improved with better time tracking
                growth_rate = (population - prev_data.current_population) / max(1, current_day - 1)
            
            self.population_data[location] = PopulationPressureData(
                location=location,
                current_population=population,
                carrying_capacity=capacity,
                pressure_level=pressure_level,
                pressure_score=pressure_score,
                resource_shortage=resource_shortage,
                growth_rate=growth_rate,
                sustainability_trend=self._assess_sustainability_trend(location, pressure_score)
            )
    
    def _calculate_resource_shortages(self, location: str, population: int, capacity: int) -> Dict[str, float]:
        """Calculate resource shortage ratios for a location."""
        shortages = {}
        
        if population <= capacity:
            # No shortages if under capacity
            return {"food": 1.0, "water": 1.0, "shelter": 1.0, "materials": 1.0, "space": 1.0}
        
        # Calculate shortage based on overpopulation
        overpopulation_ratio = population / capacity
        base_shortage = max(0.0, 1.0 - (1.0 / overpopulation_ratio))
        
        # Location-specific resource variations
        location_factors = {
            "forest": {"materials": 0.8, "shelter": 0.9},  # Better materials/shelter
            "river": {"water": 0.7},                       # Better water access
            "fields": {"food": 0.8},                       # Better food production
            "mountains": {"food": 1.2, "water": 1.1},      # Worse food/water
            "desert": {"water": 1.5, "food": 1.3}          # Much worse water/food
        }
        
        resource_types = ["food", "water", "shelter", "materials", "space"]
        for resource in resource_types:
            shortage = base_shortage
            
            # Apply location-specific factors
            if location in location_factors:
                factor = location_factors[location].get(resource, 1.0)
                shortage *= factor
            
            # Resource availability ratio (1.0 = fully available, 0.0 = completely unavailable)
            shortages[resource] = max(0.0, min(1.0, 1.0 - shortage))
        
        return shortages
    
    def _assess_sustainability_trend(self, location: str, pressure_score: float) -> str:
        """Assess sustainability trend for a location."""
        prev_data = self.population_data.get(location)
        if not prev_data:
            return "stable"
        
        if pressure_score > prev_data.pressure_score + 0.1:
            return "declining"
        elif pressure_score < prev_data.pressure_score - 0.1:
            return "improving"
        else:
            return "stable"
    
    def _process_location_pressure(self, location: str, pop_data: PopulationPressureData, 
                                 agents: List[Any], world_resources: Dict[str, float], 
                                 current_day: int) -> List[Dict[str, Any]]:
        """Process population pressure effects for a specific location."""
        events = []
        
        if pop_data.pressure_level in [PopulationPressureLevel.OVERPOPULATED, 
                                      PopulationPressureLevel.CRITICALLY_OVERPOPULATED]:
            
            # Resource scarcity events
            for resource, availability in pop_data.resource_shortage.items():
                if availability < 0.7:  # Less than 70% availability
                    events.append({
                        "type": "resource_scarcity",
                        "location": location,
                        "resource": resource,
                        "availability": availability,
                        "population": pop_data.current_population,
                        "capacity": pop_data.carrying_capacity,
                        "day": current_day
                    })
            
            # Health impacts from overcrowding
            if pop_data.pressure_score > 1.2:  # 120% of capacity
                overcrowding_health_impact = (pop_data.pressure_score - 1.0) * 0.01
                location_agents = [a for a in agents if a.location == location and a.is_alive]
                
                for agent in location_agents:
                    if random.random() < overcrowding_health_impact:
                        agent.health = max(0.0, agent.health - random.uniform(0.01, 0.03))
                        agent.memory.store_memory(
                            f"Health affected by overcrowding in {location}",
                            importance=0.6,
                            memory_type="health"
                        )
                
                events.append({
                    "type": "overcrowding_health_impact",
                    "location": location,
                    "affected_agents": len(location_agents),
                    "pressure_score": pop_data.pressure_score,
                    "day": current_day
                })
            
            # Social stress and conflicts
            if pop_data.pressure_score > 1.3:  # 130% of capacity
                stress_level = min(pop_data.pressure_score - 1.0, 1.0)
                
                events.append({
                    "type": "population_stress",
                    "location": location,
                    "stress_level": stress_level,
                    "description": f"High population density causing social stress in {location}",
                    "day": current_day
                })
        
        elif pop_data.pressure_level == PopulationPressureLevel.UNDERPOPULATED:
            # Benefits of underpopulation
            events.append({
                "type": "abundant_resources",
                "location": location,
                "population": pop_data.current_population,
                "capacity": pop_data.carrying_capacity,
                "description": f"Abundant resources available in sparsely populated {location}",
                "day": current_day
            })
        
        return events
    
    def _process_migration_attempts(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process agents attempting to migrate due to population pressure."""
        migration_events = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            current_location = agent.location
            pop_data = self.population_data.get(current_location)
            
            if not pop_data:
                continue
            
            # Calculate migration probability based on pressure
            migration_probability = 0.0
            
            if pop_data.pressure_level == PopulationPressureLevel.CRITICALLY_OVERPOPULATED:
                migration_probability = 0.15  # 15% chance per day
            elif pop_data.pressure_level == PopulationPressureLevel.OVERPOPULATED:
                migration_probability = 0.08  # 8% chance per day
            elif pop_data.pressure_level == PopulationPressureLevel.APPROACHING_LIMIT:
                migration_probability = 0.03  # 3% chance per day
            
            # Additional factors affecting migration
            if pop_data.resource_shortage.get("food", 1.0) < 0.5:
                migration_probability += 0.05  # Food shortage increases migration
            if pop_data.resource_shortage.get("water", 1.0) < 0.5:
                migration_probability += 0.05  # Water shortage increases migration
            
            # Personality factors
            if hasattr(agent, 'traits'):
                if "adventurous" in agent.traits:
                    migration_probability *= 1.5
                if "cautious" in agent.traits:
                    migration_probability *= 0.7
            
            # Social connections reduce migration
            if hasattr(agent, 'relationships'):
                local_connections = len([r for r in agent.relationships.values() 
                                       if r in ["friend", "family", "spouse"]])
                migration_probability *= max(0.3, 1.0 - local_connections * 0.1)
            
            if random.random() < migration_probability:
                migration_event = self._attempt_migration(agent, current_day)
                if migration_event:
                    migration_events.append(migration_event)
        
        return migration_events
    
    def _attempt_migration(self, agent: Any, current_day: int) -> Optional[Dict[str, Any]]:
        """Attempt migration for an agent."""
        current_location = agent.location
        
        # Find potential destinations
        possible_destinations = []
        for location, pop_data in self.population_data.items():
            if location != current_location:
                if pop_data.pressure_level in [PopulationPressureLevel.SUSTAINABLE, 
                                             PopulationPressureLevel.UNDERPOPULATED]:
                    possible_destinations.append(location)
        
        # Add unexplored locations
        all_locations = list(self.base_carrying_capacities.keys())
        for location in all_locations:
            if location not in self.population_data and location != current_location:
                possible_destinations.append(location)
        
        if not possible_destinations:
            return None  # No suitable destinations
        
        # Choose destination
        destination = random.choice(possible_destinations)
        
        # Determine migration cause
        current_pop_data = self.population_data.get(current_location)
        if current_pop_data:
            if current_pop_data.pressure_level in [PopulationPressureLevel.OVERPOPULATED, 
                                                  PopulationPressureLevel.CRITICALLY_OVERPOPULATED]:
                cause = MigrationCause.OVERPOPULATION
            elif min(current_pop_data.resource_shortage.values()) < 0.6:
                cause = MigrationCause.RESOURCE_SCARCITY
            else:
                cause = MigrationCause.OPPORTUNITY_SEEKING
        else:
            cause = MigrationCause.EXPLORATION
        
        # Check for family migration
        migrants = [agent.name]
        group_migration = False
        
        if hasattr(agent, 'family') and random.random() < self.migration_patterns["family_cohesion"]:
            # Family members might migrate together
            family_members = agent.family.get("children", []) + agent.family.get("parents", [])
            for member_name in family_members:
                # Find family member agent
                member_agent = next((a for a in self._get_all_agents() if a.name == member_name), None)
                if member_agent and member_agent.location == current_location and random.random() < 0.7:
                    migrants.append(member_name)
                    group_migration = True
        
        # Calculate success probability
        success_probability = 0.8  # Base success rate
        
        # Factors affecting success
        if hasattr(agent, 'skills'):
            survival_skill = agent.skills.get('survival', 0)
            if isinstance(survival_skill, float):
                success_probability += survival_skill * 0.2
        
        if hasattr(agent, 'health'):
            success_probability *= agent.health
        
        # Distance/difficulty factors (simplified)
        success_probability *= random.uniform(0.7, 1.0)
        
        # Execute migration if successful
        if random.random() < success_probability:
            # Successful migration
            agent.location = destination
            
            # Update other migrating family members
            for migrant_name in migrants[1:]:  # Skip the main agent
                migrant_agent = next((a for a in self._get_all_agents() if a.name == migrant_name), None)
                if migrant_agent:
                    migrant_agent.location = destination
            
            # Add migration memory
            agent.memory.store_memory(
                f"Migrated from {current_location} to {destination} due to {cause.value}",
                importance=0.8,
                memory_type="major_life_event"
            )
            
            return {
                "type": "successful_migration",
                "migrants": migrants,
                "origin": current_location,
                "destination": destination,
                "cause": cause.value,
                "group_migration": group_migration,
                "day": current_day
            }
        else:
            # Failed migration attempt
            agent.memory.store_memory(
                f"Attempted to migrate from {current_location} but failed",
                importance=0.6,
                memory_type="experience"
            )
            
            return {
                "type": "failed_migration",
                "agent": agent.name,
                "origin": current_location,
                "intended_destination": destination,
                "cause": cause.value,
                "day": current_day
            }
    
    def _get_all_agents(self) -> List[Any]:
        """Get all agents - this would be passed from the main system."""
        # This is a placeholder - in the actual implementation, this would be provided
        return []
    
    def _check_resource_conflicts(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Check for conflicts arising from resource scarcity."""
        conflict_events = []
        
        for location, pop_data in self.population_data.items():
            if pop_data.pressure_level in [PopulationPressureLevel.OVERPOPULATED, 
                                          PopulationPressureLevel.CRITICALLY_OVERPOPULATED]:
                
                # Check if any resource is critically scarce
                critical_resources = [resource for resource, availability in pop_data.resource_shortage.items()
                                    if availability < 0.4]  # Less than 40% availability
                
                if critical_resources:
                    location_agents = [a for a in agents if a.location == location and a.is_alive]
                    
                    if len(location_agents) >= 2:
                        # Potential for resource conflict
                        conflict_probability = len(critical_resources) * 0.1 * pop_data.pressure_score
                        
                        if random.random() < conflict_probability:
                            # Resource conflict occurs
                            involved_agents = random.sample(location_agents, 
                                                           min(random.randint(2, 4), len(location_agents)))
                            
                            conflict_events.append({
                                "type": "resource_conflict",
                                "location": location,
                                "involved_agents": [a.name for a in involved_agents],
                                "scarce_resources": critical_resources,
                                "pressure_level": pop_data.pressure_level.value,
                                "day": current_day
                            })
                            
                            # Add memories to involved agents
                            for agent in involved_agents:
                                agent.memory.store_memory(
                                    f"Involved in conflict over {', '.join(critical_resources)} in {location}",
                                    importance=0.7,
                                    memory_type="conflict"
                                )
        
        return conflict_events
    
    def get_population_summary(self) -> Dict[str, Any]:
        """Get comprehensive population pressure summary."""
        total_population = sum(data.current_population for data in self.population_data.values())
        total_capacity = sum(data.carrying_capacity for data in self.population_data.values())
        
        pressure_distribution = {}
        for level in PopulationPressureLevel:
            count = len([data for data in self.population_data.values() 
                        if data.pressure_level == level])
            pressure_distribution[level.value] = count
        
        return {
            "total_population": total_population,
            "total_carrying_capacity": total_capacity,
            "overall_pressure_score": total_population / total_capacity if total_capacity > 0 else 0,
            "locations_tracked": len(self.population_data),
            "pressure_distribution": pressure_distribution,
            "migration_events": len(self.migration_history),
            "resource_conflicts": len(self.resource_conflicts),
            "sustainability_outlook": self._assess_overall_sustainability()
        }
    
    def _assess_overall_sustainability(self) -> str:
        """Assess overall population sustainability."""
        if not self.population_data:
            return "insufficient_data"
        
        critical_locations = len([data for data in self.population_data.values()
                                if data.pressure_level == PopulationPressureLevel.CRITICALLY_OVERPOPULATED])
        overpopulated_locations = len([data for data in self.population_data.values()
                                     if data.pressure_level == PopulationPressureLevel.OVERPOPULATED])
        
        total_locations = len(self.population_data)
        
        if critical_locations > total_locations * 0.3:
            return "crisis"
        elif overpopulated_locations > total_locations * 0.5:
            return "concerning"
        elif critical_locations == 0 and overpopulated_locations < total_locations * 0.2:
            return "sustainable"
        else:
            return "moderate_pressure"
    
    def get_location_details(self, location: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific location."""
        if location not in self.population_data:
            return None
        
        pop_data = self.population_data[location]
        capacity_data = self.carrying_capacities.get(location)
        
        return {
            "population_data": asdict(pop_data),
            "capacity_data": asdict(capacity_data) if capacity_data else None,
            "migration_in": len([m for m in self.migration_history 
                               if m.destination_location == location]),
            "migration_out": len([m for m in self.migration_history 
                                if m.origin_location == location]),
            "recent_conflicts": len([c for c in self.resource_conflicts 
                                   if c.get("location") == location])
        } 