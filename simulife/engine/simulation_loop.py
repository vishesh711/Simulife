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
        Returns a summary of the day's events.
        """
        day_summary = {
            "day": self.world.current_day,
            "agent_actions": [],
            "interactions": [],
            "world_events": [],
            "new_relationships": [],
            "status_changes": []
        }
        
        if verbose:
            print(f"\n🌅 Day {self.world.current_day} begins ({self.world.season}, {self.world.weather})")
            print(f"   {self.world.get_world_description()}")
        
        # Step 1: All agents reflect and decide actions
        for agent in self.agents:
            if not agent.is_alive:
                continue
            
            # Agent reflects on current situation
            world_context = self.world.get_world_description()
            reflection = agent.reflect(world_context)
            
            # Agent decides on action for the day
            action = agent.decide_action(world_state=self.world.to_dict())
            day_summary["agent_actions"].append({
                "agent": agent.name,
                "action": action,
                "emotion": agent.emotion
            })
            
            if verbose:
                print(f"   🎭 {action}")
            
            # Age the agent
            agent.age_one_day(self.world.current_day)
        
        # Step 2: Generate interactions between agents
        interactions = self._generate_interactions()
        day_summary["interactions"] = interactions
        
        # Step 3: Process world events and their effects
        world_events = self._process_world_events()
        day_summary["world_events"] = world_events
        
        # Step 4: Check for emergent phenomena (factions, beliefs, etc.)
        emergent_events = self._check_emergent_phenomena()
        day_summary.update(emergent_events)
        
        # Step 5: Process reproduction attempts
        new_births = self._process_reproduction_attempts()
        day_summary["new_births"] = new_births
        
        # Step 6: Advance world state
        self.world.advance_day()
        self._update_population_stats()
        
        # Step 7: Update statistics
        self.stats["days_simulated"] += 1
        self.stats["total_interactions"] += len(interactions)
        self.stats["total_events"] += len(world_events)
        
        if verbose:
            print(f"   📊 {len(interactions)} interactions, {len(world_events)} events")
        
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

    def _process_reproduction_attempts(self) -> List[Dict[str, Any]]:
        """Process potential reproduction between agents."""
        new_births = []
        
        # Look for agents who might reproduce
        adult_agents = [a for a in self.agents if a.is_alive and a.age >= 18]
        
        for i, agent1 in enumerate(adult_agents):
            for agent2 in adult_agents[i+1:]:
                # Check if they have a suitable relationship
                relationship = agent1.relationships.get(agent2.name, "stranger")
                
                if relationship in ["friend", "partner", "spouse"]:
                    # Small chance to attempt reproduction
                    if random.random() < 0.05:  # 5% chance per day for suitable couples
                        child_config = self.family_manager.attempt_reproduction(
                            agent1, agent2, self.world.current_day, self
                        )
                        
                        if child_config:
                            # Create new agent and add to simulation
                            new_agent = BaseAgent(child_config, self.world.current_day)
                            self.agents.append(new_agent)
                            
                            # Log the birth event
                            birth_event = self.world.add_agent_event(
                                agent_names=[agent1.name, agent2.name, child_config["name"]],
                                event_type="birth",
                                description=f"{child_config['name']} was born to {agent1.name} and {agent2.name}",
                                location=agent1.location,
                                importance=0.8
                            )
                            
                            new_births.append({
                                "child_name": child_config["name"],
                                "parents": [agent1.name, agent2.name],
                                "location": agent1.location,
                                "day": self.world.current_day
                            })
                            
                            # Update statistics
                            self.stats["agent_births"] += 1
                            
                            print(f"👶 Birth: {child_config['name']} born to {agent1.name} and {agent2.name}")
        
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