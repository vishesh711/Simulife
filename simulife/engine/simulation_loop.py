"""
Simulation Loop for SimuLife
Main engine that runs the world in ticks and coordinates agent actions.
"""

import json
import random
import time
import os
from typing import Dict, List, Any, Optional, Tuple
from ..agents.base_agent import BaseAgent
from ..agents.reproduction import FamilyManager
from .world_state import WorldState, WorldEvent
from .advanced_events import AdvancedEventSystem
from .cultural_system import CulturalSystem
from .resource_system import ResourceSystem
from .environmental_system import EnvironmentalSystem
# Phase 4: Advanced Behaviors Systems
from .skill_system import SkillSystem
from .specialization_system import SpecializationSystem
from .conflict_system import ConflictSystem
from .cultural_artifacts import CulturalArtifactSystem
# Phase 5: Group Dynamics Systems
from .group_dynamics import GroupDynamicsSystem
# Phase 6: Technology and Innovation Systems
from .technology_system import TechnologySystem
# Phase 7: Population Dynamics Systems
from .mortality_system import MortalitySystem
from .genetic_disease_system import GeneticDiseaseSystem
from .population_pressure_system import PopulationPressureSystem
from .generational_culture_system import GenerationalCultureSystem
# Phase 8: Emergent Phenomena Systems
from .social_institutions_system import SocialInstitutionsSystem
from .economic_emergence_system import EconomicEmergenceSystem
from .cultural_movements_system import CulturalMovementsSystem
from .civilizational_milestones_system import CivilizationalMilestonesSystem
from .crisis_response_system import CrisisResponseSystem
from .inter_group_diplomacy_system import InterGroupDiplomacySystem
# Phase 9: Advanced AI & Meta-Cognition Systems
from .self_awareness_system import SelfAwarenessSystem
from .meta_cognition_system import MetaCognitionSystem
from .consciousness_metrics_system import ConsciousnessMetricsSystem


class SimulationEngine:
    """
    Main simulation engine that orchestrates the SimuLife world.
    Manages agents, world state, time progression, and interactions.
    """
    
    def __init__(self, agent_config_paths: List[str] = None, 
                 world_config: Optional[Dict] = None,
                 save_dir: str = "data/saves"):
        # Initialize world state
        self.world = WorldState(world_config)
        
        # Initialize agents
        self.agents: List[BaseAgent] = []
        self.agent_config_paths = agent_config_paths or []
        self.save_dir = save_dir
        
        # Initialize family manager for reproduction
        self.family_manager = FamilyManager()
        
        # Initialize advanced event system
        self.event_system = AdvancedEventSystem()
        
        # Initialize Phase 3 completion systems
        self.cultural_system = CulturalSystem()
        self.resource_system = ResourceSystem()
        self.environmental_system = EnvironmentalSystem()
        
        # Initialize Phase 4: Advanced Behaviors systems
        self.skill_system = SkillSystem()
        self.specialization_system = SpecializationSystem()
        self.conflict_system = ConflictSystem()
        self.cultural_artifact_system = CulturalArtifactSystem()
        
        # Initialize Phase 5: Group Dynamics systems
        self.group_dynamics_system = GroupDynamicsSystem()
        
        # Initialize Phase 6: Technology and Innovation systems
        self.technology_system = TechnologySystem()
        
        # Initialize Phase 7: Population Dynamics systems
        self.mortality_system = MortalitySystem()
        self.genetic_disease_system = GeneticDiseaseSystem()
        self.population_pressure_system = PopulationPressureSystem()
        self.generational_culture_system = GenerationalCultureSystem()
        
        # Initialize Phase 8: Emergent Phenomena systems
        self.social_institutions_system = SocialInstitutionsSystem()
        self.economic_emergence_system = EconomicEmergenceSystem()
        self.cultural_movements_system = CulturalMovementsSystem()
        self.civilizational_milestones_system = CivilizationalMilestonesSystem()
        self.crisis_response_system = CrisisResponseSystem()
        self.inter_group_diplomacy_system = InterGroupDiplomacySystem()
        
        # Initialize Phase 9: Advanced AI & Meta-Cognition systems
        self.self_awareness_system = SelfAwarenessSystem()
        self.meta_cognition_system = MetaCognitionSystem()
        self.consciousness_metrics_system = ConsciousnessMetricsSystem()
        
        # Create save directory
        os.makedirs(save_dir, exist_ok=True)
        
        # Simulation settings
        self.tick_delay = 1.0  # Seconds between ticks
        self.interactions_per_day = 3  # Max interactions per agent per day
        self.max_agents_per_interaction = 4
        
        # Statistics
        self.stats = {
            "days_simulated": 0,
            "total_interactions": 0,
            "total_events": 0,
            "agent_births": 0,
            "agent_deaths": 0
        }
        
        # Load agents from configs
        self._load_agents()

    def _load_agents(self) -> None:
        """Load agents from configuration files."""
        for config_path in self.agent_config_paths:
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                agent = BaseAgent(config, self.world.current_day)
                self.agents.append(agent)
                
                print(f"✓ Loaded agent: {agent.name}")
                
            except Exception as e:
                print(f"✗ Failed to load agent from {config_path}: {e}")
        
        # Update world population stats
        self._update_population_stats()

    def _update_population_stats(self) -> None:
        """Update world population statistics."""
        if self.agents:
            avg_age = sum(agent.age for agent in self.agents) / len(self.agents)
        else:
            avg_age = 0
        
        self.world.update_population_stats(
            total_agents=len(self.agents),
            births=self.stats["agent_births"],
            deaths=self.stats["agent_deaths"],
            average_age=avg_age
        )

    def run_day(self, verbose: bool = True) -> Dict[str, Any]:
        """
        Run a single day of simulation.
        
        Returns:
            Dict containing summary of the day's events
        """
        day_summary = {"day": self.world.current_day}
        
        if verbose:
            season_info = f"{self.world.season}, {self.world.weather}"
            world_info = f"Day {self.world.current_day} of Year {self.world.year}, {season_info}. The weather is {self.world.weather}."
            
            # Add resource status
            resource_statuses = []
            for resource, level in self.world.resources.items():
                if level > 1.2:
                    status = "abundant"
                elif level > 0.8:
                    status = "adequate"
                elif level > 0.4:
                    status = "scarce"
                else:
                    status = "critically low"
                resource_statuses.append(f"{resource} is {status}")
            resource_status = ", ".join(resource_statuses)
            
            # Add recent events context
            recent_events = self.world.get_recent_events(3)
            events_context = ""
            if recent_events:
                # Handle WorldEvent objects properly
                first_event = recent_events[0]
                if hasattr(first_event, 'description'):
                    events_context = f" Recent events include: {first_event.description}"
                else:
                    events_context = f" Recent events include: {str(first_event)}"
            
            world_description = f"   {world_info} Resources: {resource_status}.{events_context}"
            print(f"\n🌅 Day {self.world.current_day} begins ({season_info})")
            print(world_description)
        
        # Step 1: Generate world events
        world_events = self.event_system.generate_daily_events(self.world, self.agents)
        for event in world_events:
            # Add event using the correct WorldState method
            event_participants = event.get('participants', [])
            self.world.add_agent_event(
                event_participants, 
                event.get('event_type', 'general'),
                event.get('description', 'Unknown event'),
                event.get('importance', 0.5)
            )
            if verbose:
                print(f"   🌍 World Event: {event.get('description', 'Unknown event')}")
        day_summary["world_events"] = world_events
        
        # Step 2: Process agent actions and interactions
        interactions = self._generate_interactions()
        day_summary["interactions"] = interactions
        
        # Step 3: Process Phase 3 systems (Cultural, Resource, Environmental)
        # 3a: Process cultural evolution and knowledge transfer
        cultural_events = self.cultural_system.process_cultural_evolution(
            self.agents, self.world.current_day, self.world)
        day_summary["cultural_events"] = cultural_events
        
        # 3b: Process resource management and trading
        resource_events = self.resource_system.process_daily_resources(
            self.agents, self.world.resources, self.world.current_day)
        day_summary["resource_events"] = resource_events
        
        # 3c: Process environmental effects and agent adaptation
        environmental_events = self.environmental_system.process_environmental_effects(
            self.agents, self.world, self.world.current_day)
        day_summary["environmental_events"] = environmental_events
        
        # Step 4: Process Phase 4: Advanced Behaviors systems
        # 4a: Process skill development and practice
        skill_events = self.skill_system.process_daily_skill_activities(
            self.agents, self.world.current_day)
        day_summary["skill_events"] = skill_events
        
        # 4b: Process specialization activities and advancement
        specialization_events = self.specialization_system.process_specialization_activities(
            self.agents, self.world.current_day)
        day_summary["specialization_events"] = specialization_events
        
        # 4c: Process conflicts and resolution attempts
        conflict_events = self.conflict_system.process_daily_conflicts(
            self.agents, self.world.current_day)
        day_summary["conflict_events"] = conflict_events
        
        # 4d: Process cultural artifact creation and preservation
        artifact_events = self.cultural_artifact_system.process_daily_artifacts(
            self.agents, self.world.current_day)
        day_summary["artifact_events"] = artifact_events
        
        # Step 5: Process Phase 5: Group Dynamics systems
        group_events = self.group_dynamics_system.process_daily_group_activities(
            self.agents, self.world.current_day)
        day_summary["group_events"] = group_events
        
        # Step 6: Process Phase 6: Technology and Innovation systems
        technology_events = self.technology_system.process_daily_technology_activities(
            self.agents, self.group_dynamics_system.groups, self.world.current_day)
        day_summary["technology_events"] = technology_events
        
        # Step 7: Process Phase 7: Population Dynamics systems
        # 7a: Process aging, death, and mortality
        aging_events = self.mortality_system.process_daily_aging(
            self.agents, self.world.current_day)
        day_summary["aging_events"] = aging_events
        
        # 7b: Process genetic diseases and health effects
        disease_events = self.genetic_disease_system.process_daily_disease_effects(
            self.agents, self.world.current_day)
        day_summary["disease_events"] = disease_events
        
        # 7c: Process population pressure and migration
        population_events = self.population_pressure_system.process_daily_population_pressure(
            self.agents, self.world.resources, self.world.current_day)
        day_summary["population_events"] = population_events
        
        # 7d: Process generational cultural transmission
        cultural_transmission_events = self.generational_culture_system.process_daily_cultural_transmission(
            self.agents, self.world.current_day)
        day_summary["cultural_transmission_events"] = cultural_transmission_events
        
        # Step 8: Process Phase 8: Emergent Phenomena systems
        # 8a: Process emergent social institutions (governments, schools, religions)
        institutional_events = self.social_institutions_system.process_daily_institutional_emergence(
            self.agents, self.group_dynamics_system.groups, self.world, self.world.current_day)
        day_summary["institutional_events"] = institutional_events
        
        # 8b: Process economic emergence (markets, currency, trade networks)
        economic_events = self.economic_emergence_system.process_daily_economic_emergence(
            self.agents, self.group_dynamics_system.groups, self.world, self.world.current_day)
        day_summary["economic_events"] = economic_events
        
        # 8c: Process cultural movements (ideologies, belief systems, social movements)
        movement_events = self.cultural_movements_system.process_daily_cultural_movements(
            self.agents, self.group_dynamics_system.groups, world_events, self.world.current_day)
        day_summary["movement_events"] = movement_events
        
        # 8d: Process civilizational milestones (major achievements and progress)
        milestone_events = self.civilizational_milestones_system.process_daily_milestone_analysis(
            self.agents, self.group_dynamics_system.groups, 
            getattr(self.social_institutions_system, 'institutions', {}),
            getattr(self.cultural_movements_system, 'movements', {}),
            self.economic_emergence_system.get_economic_summary(),
            self.technology_system.get_technology_summary(),
            self.world, self.world.current_day)
        day_summary["milestone_events"] = milestone_events
        
        # 8e: Process crisis response (collective adaptation to challenges)
        crisis_events = self.crisis_response_system.process_daily_crisis_response(
            self.agents, getattr(self.social_institutions_system, 'institutions', {}),
            self.group_dynamics_system.groups, world_events, self.world, self.world.current_day)
        day_summary["crisis_events"] = crisis_events
        
        # 8f: Process inter-group diplomacy (international relations and treaties)
        diplomacy_events = self.inter_group_diplomacy_system.process_daily_diplomacy(
            self.agents, self.group_dynamics_system.groups,
            getattr(self.social_institutions_system, 'institutions', {}),
            world_events, self.world.current_day)
        day_summary["diplomacy_events"] = diplomacy_events
        
        # Step 9: Process Phase 9: Advanced AI & Meta-Cognition systems
        # 9a: Process self-awareness and identity development
        self_awareness_events = self.self_awareness_system.process_daily_self_awareness_development(
            self.agents, self.world.current_day)
        day_summary["self_awareness_events"] = self_awareness_events
        
        # 9b: Process meta-cognitive development (thinking about thinking)
        metacognition_events = self.meta_cognition_system.process_daily_metacognitive_development(
            self.agents, self.world.current_day)
        day_summary["metacognition_events"] = metacognition_events
        
        # 9c: Process consciousness measurement and tracking
        consciousness_events = self.consciousness_metrics_system.process_daily_consciousness_measurement(
            self.agents, self.world.current_day)
        day_summary["consciousness_events"] = consciousness_events
        
        # Step 10: Process reproduction attempts (with genetic and health considerations)
        new_births = self._process_reproduction_attempts(verbose)
        day_summary["new_births"] = new_births
        
        # Step 11: Check for emergent phenomena (factions, beliefs, etc.)
        emergent_events = self._check_emergent_phenomena()
        day_summary.update(emergent_events)
        
        # Step 11: Advance world state and agent aging
        self.world.advance_day()
        self._update_population_stats()
        
        # Step 12: Update statistics
        self.stats["days_simulated"] += 1
        self.stats["total_interactions"] += len(interactions)
        self.stats["total_events"] += len(world_events)
        self.stats["cultural_activities"] = len(cultural_events)
        self.stats["resource_transactions"] = len(resource_events)
        self.stats["environmental_impacts"] = len(environmental_events)
        self.stats["skill_developments"] = len(skill_events)
        self.stats["specialization_advancements"] = len(specialization_events)
        self.stats["conflicts_processed"] = len(conflict_events)
        self.stats["artifacts_created"] = len(artifact_events)
        self.stats["group_activities"] = len(group_events)
        self.stats["technology_activities"] = len(technology_events)
        self.stats["aging_events"] = len(aging_events)
        self.stats["disease_events"] = len(disease_events)
        self.stats["population_events"] = len(population_events)
        self.stats["cultural_transmission_events"] = len(cultural_transmission_events)
        # Phase 8 statistics
        self.stats["institutional_events"] = len(institutional_events)
        self.stats["economic_events"] = len(economic_events)
        self.stats["movement_events"] = len(movement_events)
        self.stats["milestone_events"] = len(milestone_events)
        self.stats["crisis_events"] = len(crisis_events)
        self.stats["diplomacy_events"] = len(diplomacy_events)
        
        # Step 12: Daily summary output
        if verbose:
            total_activities = (len(interactions) + len(world_events) + len(cultural_events) + 
                              len(resource_events) + len(environmental_events) + len(skill_events) +
                              len(specialization_events) + len(conflict_events) + len(artifact_events) +
                              len(group_events) + len(technology_events) + len(aging_events) +
                              len(disease_events) + len(population_events) + len(cultural_transmission_events) +
                              len(institutional_events) + len(economic_events) + len(movement_events) +
                              len(milestone_events) + len(crisis_events) + len(diplomacy_events) +
                              len(self_awareness_events) + len(metacognition_events) + len(consciousness_events))
            
            print(f"   📊 {total_activities} total activities: {len(interactions)} interactions, " +
                  f"{len(world_events)} events, {len(cultural_events)} cultural, " +
                  f"{len(resource_events)} resource, {len(environmental_events)} environmental, " +
                  f"{len(skill_events)} skill, {len(specialization_events)} specialization, " +
                  f"{len(conflict_events)} conflict, {len(artifact_events)} artifact, " +
                  f"{len(group_events)} group, {len(technology_events)} technology, " +
                  f"{len(aging_events)} aging, {len(disease_events)} disease, " +
                  f"{len(population_events)} population, {len(cultural_transmission_events)} cultural transmission, " +
                  f"{len(institutional_events)} institutional, {len(economic_events)} economic, " +
                  f"{len(movement_events)} movement, {len(milestone_events)} milestone, " +
                  f"{len(crisis_events)} crisis, {len(diplomacy_events)} diplomacy, " +
                  f"{len(self_awareness_events)} self-awareness, {len(metacognition_events)} metacognition, " +
                  f"{len(consciousness_events)} consciousness")
        
        return day_summary

    def _generate_interactions(self) -> List[Dict[str, Any]]:
        """Generate interactions between agents for this day."""
        interactions = []
        
        # Group agents by location for proximity-based interactions
        location_groups = {}
        for agent in self.agents:
            if agent.is_alive:
                loc = agent.location
                if loc not in location_groups:
                    location_groups[loc] = []
                location_groups[loc].append(agent)
        
        # Generate interactions within each location
        for location, agents_here in location_groups.items():
            if len(agents_here) < 2:
                continue
            
            # Determine number of interactions for this location
            num_interactions = min(
                len(agents_here) // 2,
                self.interactions_per_day
            )
            
            for _ in range(num_interactions):
                # Randomly select agents for interaction
                if len(agents_here) >= 2:
                    participants = random.sample(agents_here, min(2, len(agents_here)))
                    
                    if len(participants) == 2:
                        agent1, agent2 = participants
                        
                        # Determine interaction type based on relationship and personalities
                        interaction_type = self._determine_interaction_type(agent1, agent2)
                        
                        # Execute interaction
                        interaction_result = agent1.interact_with(agent2, interaction_type)
                        
                        # Also update the other agent's memory
                        reverse_interaction = f"{agent2.name} {interaction_type} with {agent1.name}"
                        agent2.memory.store_memory(
                            reverse_interaction,
                            importance=0.4,
                            emotion=agent2.emotion,
                            memory_type="relationship"
                        )
                        
                        interactions.append({
                            "participants": [agent1.name, agent2.name],
                            "type": interaction_type,
                            "description": interaction_result,
                            "location": location
                        })
                        
                        # Chance for relationship changes or conflicts
                        if random.random() < 0.1:  # 10% chance for significant event
                            self._process_relationship_event(agent1, agent2, interaction_type)
        
        return interactions

    def _determine_interaction_type(self, agent1: BaseAgent, agent2: BaseAgent) -> str:
        """Determine the type of interaction between two agents."""
        relationship = agent1.relationships.get(agent2.name, "stranger")
        
        # Weight interaction types based on relationship and personality
        interaction_weights = {
            "conversation": 0.5,
            "collaboration": 0.2,
            "help": 0.2,
            "debate": 0.1
        }
        
        # Modify weights based on relationship
        if relationship == "friend":
            interaction_weights["collaboration"] += 0.3
            interaction_weights["help"] += 0.2
        elif relationship == "rival":
            interaction_weights["debate"] += 0.4
            interaction_weights["conversation"] -= 0.2
        elif relationship == "family":
            interaction_weights["help"] += 0.3
            interaction_weights["conversation"] += 0.2
        
        # Modify based on personality traits
        if "kind" in agent1.traits:
            interaction_weights["help"] += 0.2
        if "ambitious" in agent1.traits:
            interaction_weights["collaboration"] += 0.2
        
        # Choose interaction type
        interactions = list(interaction_weights.keys())
        weights = list(interaction_weights.values())
        
        return random.choices(interactions, weights=weights)[0]

    def _process_relationship_event(self, agent1: BaseAgent, agent2: BaseAgent, 
                                  interaction_type: str) -> None:
        """Process significant relationship events that might affect the world."""
        relationship = agent1.relationships.get(agent2.name, "stranger")
        
        if interaction_type == "debate" and relationship == "rival":
            # Potential for conflict or faction formation
            event_desc = f"{agent1.name} and {agent2.name} had a heated debate that drew attention"
            
            event = self.world.add_agent_event(
                agent_names=[agent1.name, agent2.name],
                event_type="conflict",
                description=event_desc,
                location=agent1.location,
                importance=0.6
            )
            
            # Other agents observe this conflict
            for agent in self.agents:
                if agent.name not in [agent1.name, agent2.name] and agent.location == agent1.location:
                    agent.observe_event(event_desc, importance=0.4, emotion_trigger="concerned")

    def _process_world_events(self) -> List[Dict[str, Any]]:
        """Process advanced world events and their effects on agents."""
        # Generate new events using the advanced event system
        new_events = self.event_system.generate_daily_events(self.world, self.agents)
        
        # Process existing world events from the world state
        recent_events = self.world.get_recent_events(days=1)
        processed_events = []
        
        # Handle new advanced events
        for event_data in new_events:
            # Add to world state for tracking
            world_event = self.world.add_agent_event(
                agent_names=event_data.get("participants", []),
                event_type=event_data["type"],
                description=event_data["description"],
                location=event_data["location"],
                importance=event_data["importance"]
            )
            
            # Notify affected agents
            for agent in self.agents:
                if (agent.is_alive and 
                    (not event_data["participants"] or agent.name in event_data["participants"] or
                     agent.location == event_data["location"])):
                    
                    # Determine emotional response based on event type
                    emotion_map = {
                        "natural": "concerned",
                        "social": "interested", 
                        "discovery": "excited",
                        "crisis": "worried",
                        "cultural": "curious",
                        "political": "alert",
                        "follow_up": "reflective"
                    }
                    
                    emotion = emotion_map.get(event_data["type"], "neutral")
                    agent.observe_event(event_data["description"], event_data["importance"], emotion)
            
            processed_events.append({
                "event": event_data["description"],
                "type": event_data["type"],
                "location": event_data["location"],
                "affected_agents": event_data["participants"],
                "importance": event_data["importance"],
                "source": "advanced_system"
            })
        
        # Handle traditional world events
        for event in recent_events:
            if event.day == self.world.current_day:
                # This is today's event, process it
                affected_agents = []
                
                # Find agents in the event location
                for agent in self.agents:
                    if agent.location == event.location:
                        affected_agents.append(agent)
                        
                        # Agent observes the event
                        emotion_map = {
                            "resource_discovery": "excited",
                            "natural_phenomenon": "curious",
                            "mysterious_occurrence": "intrigued",
                            "weather_change": "neutral"
                        }
                        
                        emotion = emotion_map.get(event.event_type, "neutral")
                        agent.observe_event(event.description, event.importance, emotion)
                
                processed_events.append({
                    "event": event.description,
                    "type": event.event_type,
                    "location": event.location,
                    "affected_agents": [a.name for a in affected_agents],
                    "importance": event.importance,
                    "source": "world_state"
                })
        
        return processed_events

    def _check_emergent_phenomena(self) -> Dict[str, List]:
        """Check for emergent phenomena like faction formation, new beliefs, etc."""
        new_factions = []
        new_beliefs = []
        new_customs = []
        
        # Check for potential faction formation
        # (Simplified logic - could be much more sophisticated)
        if len(self.agents) >= 3 and random.random() < 0.05:  # 5% chance per day
            # Look for agents with shared goals or strong relationships
            potential_leaders = [a for a in self.agents if "ambitious" in a.traits]
            
            if potential_leaders:
                leader = random.choice(potential_leaders)
                followers = []
                
                for agent in self.agents:
                    if (agent != leader and 
                        leader.relationships.get(agent.name) in ["friend", "family"] and
                        len(followers) < 3):
                        followers.append(agent.name)
                
                if len(followers) >= 2:
                    faction_name = f"{leader.name}'s Circle"
                    ideology = random.choice([
                        "Knowledge seekers",
                        "Community builders", 
                        "Tradition keepers",
                        "Innovation advocates"
                    ])
                    
                    self.world.add_faction(
                        name=faction_name,
                        leader=leader.name,
                        members=followers,
                        ideology=ideology,
                        location=leader.location
                    )
                    
                    new_factions.append({
                        "name": faction_name,
                        "leader": leader.name,
                        "members": followers,
                        "ideology": ideology
                    })
        
        # Check for new belief formation
        # (Triggered by significant events or agent discoveries)
        important_events = self.world.get_important_events(threshold=0.7)
        recent_important = [e for e in important_events if e.day >= self.world.current_day - 7]
        
        if recent_important and random.random() < 0.1:  # 10% chance if important event
            event = recent_important[-1]
            
            # Some agents might develop beliefs around this event
            believers = []
            for agent in self.agents:
                if (agent.location == event.location and 
                    "curious" in agent.traits and
                    random.random() < 0.3):
                    believers.append(agent.name)
            
            if len(believers) >= 2:
                belief_name = f"The {event.event_type.replace('_', ' ').title()} Phenomenon"
                description = f"A belief system that formed around {event.description}"
                
                self.world.add_belief(
                    belief_name=belief_name,
                    description=description,
                    believers=believers
                )
                
                new_beliefs.append({
                    "name": belief_name,
                    "believers": believers,
                    "origin_event": event.description
                })
        
        return {
            "new_factions": new_factions,
            "new_beliefs": new_beliefs,
            "new_customs": new_customs
        }

    def _process_reproduction_attempts(self, verbose: bool = False) -> List[Dict[str, Any]]:
        """Process potential reproduction between agents with genetic considerations."""
        new_births = []
        
        # Look for agents who might reproduce
        adult_agents = [a for a in self.agents if a.is_alive and a.age >= 18]
        
        for i, agent1 in enumerate(adult_agents):
            for agent2 in adult_agents[i+1:]:
                # Check if they have a suitable relationship
                relationship = agent1.relationships.get(agent2.name, "stranger")
                
                if relationship in ["friend", "partner", "spouse"]:
                    # Check genetic compatibility
                    compatibility, risk_factor, warnings = self.genetic_disease_system.check_reproduction_compatibility(
                        agent1, agent2)
                    
                    # Base reproduction chance
                    base_chance = 0.05  # 5% chance per day for suitable couples
                    
                    # Modify chance based on genetic compatibility
                    if not compatibility:
                        base_chance *= 0.5  # Reduced chance if genetic issues
                    
                    # Health-based modifications
                    health_factor = (agent1.health + agent2.health) / 2
                    base_chance *= health_factor
                    
                    if random.random() < base_chance:
                        # Attempt reproduction
                        can_reproduce, reason = self.family_manager.can_reproduce(
                            agent1, agent2, self.world.current_day)
                        
                        if can_reproduce:
                            # Create child
                            child_config = self.family_manager.create_offspring(
                                agent1, agent2, self.world.current_day, self)
                            
                            # Create new agent and add to simulation
                            new_agent = BaseAgent(child_config, self.world.current_day)
                            
                            # Initialize genetic profile for child
                            child_genetics = self.genetic_disease_system.inherit_diseases_from_parents(
                                new_agent, agent1, agent2)
                            
                            # Initialize cultural knowledge for child
                            child_culture = self.generational_culture_system.initialize_agent_culture(
                                new_agent, self.world.current_day)
                            
                            self.agents.append(new_agent)
                            
                            # Log the birth event
                            birth_event = {
                                "child_name": child_config["name"],
                                "parents": [agent1.name, agent2.name],
                                "location": agent1.location,
                                "day": self.world.current_day,
                                "genetic_diseases": len(child_genetics),
                                "cultural_elements": len(child_culture)
                            }
                            
                            new_births.append(birth_event)
                            
                            # Update statistics
                            self.stats["agent_births"] += 1
                            
                            if verbose:
                                print(f"   👶 Birth: {child_config['name']} born to {agent1.name} and {agent2.name}")
        
        return new_births

    def run_simulation(self, days: int, verbose: bool = True, 
                      save_interval: int = 10) -> List[Dict[str, Any]]:
        """
        Run the simulation for a specified number of days.
        """
        daily_summaries = []
        
        print(f"🌍 Starting SimuLife simulation for {days} days...")
        print(f"   Population: {len(self.agents)} agents")
        print(f"   Starting location: {self.world.season} season, Day {self.world.current_day}")
        
        try:
            for day in range(days):
                # Run one day
                summary = self.run_day(verbose=verbose)
                daily_summaries.append(summary)
                
                # Auto-save periodically
                if day % save_interval == 0:
                    self.save_simulation(f"auto_save_day_{self.world.current_day}")
                
                # Optional delay between days
                if self.tick_delay > 0:
                    time.sleep(self.tick_delay)
                
                # Check for early termination conditions
                alive_agents = [a for a in self.agents if a.is_alive]
                if len(alive_agents) == 0:
                    print("🚫 Simulation ended: No agents remaining")
                    break
        
        except KeyboardInterrupt:
            print("\n⏸️  Simulation paused by user")
        
        # Final save
        self.save_simulation(f"final_save_day_{self.world.current_day}")
        
        # Print final statistics
        self._print_final_stats()
        
        return daily_summaries

    def _print_final_stats(self) -> None:
        """Print final simulation statistics."""
        print(f"\n📊 Simulation Statistics:")
        print(f"   Days simulated: {self.stats['days_simulated']}")
        print(f"   Total interactions: {self.stats['total_interactions']}")
        print(f"   Total events: {self.stats['total_events']}")
        print(f"   Final population: {len([a for a in self.agents if a.is_alive])}")
        print(f"   Active factions: {len(self.world.factions)}")
        print(f"   Belief systems: {len(self.world.beliefs)}")
        print(f"   World events: {len(self.world.events)}")

    def get_agent_summary(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed summary of a specific agent."""
        agent = next((a for a in self.agents if a.name == agent_name), None)
        if not agent:
            return None
        
        memory_stats = agent.memory.get_memory_stats()
        
        return {
            "basic_info": {
                "name": agent.name,
                "age": agent.age,
                "traits": agent.traits,
                "current_goal": agent.current_goal,
                "emotion": f"{agent.emotion} ({agent.emotion_intensity:.1f})"
            },
            "status": {
                "health": agent.health,
                "energy": agent.energy,
                "location": agent.location,
                "life_satisfaction": agent.life_satisfaction
            },
            "social": {
                "relationships": agent.relationships,
                "family": agent.family,
                "faction": agent.faction,
                "reputation": agent.reputation
            },
            "memory": memory_stats,
            "recent_actions": agent.action_history[-5:] if agent.action_history else []
        }

    def save_simulation(self, save_name: str) -> None:
        """Save the complete simulation state."""
        save_path = os.path.join(self.save_dir, save_name)
        os.makedirs(save_path, exist_ok=True)
        
        # Save world state
        self.world.save_to_file(os.path.join(save_path, "world_state.json"))
        
        # Save agents
        agents_data = [agent.to_dict() for agent in self.agents]
        with open(os.path.join(save_path, "agents.json"), 'w') as f:
            json.dump(agents_data, f, indent=2)
        
        # Save simulation stats
        with open(os.path.join(save_path, "simulation_stats.json"), 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        print(f"💾 Simulation saved to {save_path}")

    def load_simulation(self, save_name: str) -> bool:
        """Load a previously saved simulation state."""
        save_path = os.path.join(self.save_dir, save_name)
        
        try:
            # Load world state
            world_file = os.path.join(save_path, "world_state.json")
            if os.path.exists(world_file):
                self.world = WorldState.load_from_file(world_file)
            
            # Load agents
            agents_file = os.path.join(save_path, "agents.json")
            if os.path.exists(agents_file):
                with open(agents_file, 'r') as f:
                    agents_data = json.load(f)
                
                self.agents = []
                for agent_data in agents_data:
                    agent = BaseAgent(agent_data, self.world.current_day)
                    self.agents.append(agent)
            
            # Load stats
            stats_file = os.path.join(save_path, "simulation_stats.json")
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    self.stats = json.load(f)
            
            print(f"📂 Simulation loaded from {save_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load simulation: {e}")
            return False 