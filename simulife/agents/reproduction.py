"""
Agent Reproduction and Family Systems for SimuLife
Enables agents to form families, reproduce, and create multi-generational societies.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime


class GeneticSystem:
    """
    Handles trait inheritance and genetic combination for offspring.
    """
    
    @staticmethod
    def combine_traits(parent1_traits: List[str], parent2_traits: List[str], 
                      mutation_rate: float = 0.1) -> List[str]:
        """
        Combine traits from two parents to create offspring traits.
        
        Args:
            parent1_traits: Traits from first parent
            parent2_traits: Traits from second parent
            mutation_rate: Chance for random mutation/new traits
            
        Returns:
            List of traits for offspring
        """
        # Combine parent traits
        all_traits = list(set(parent1_traits + parent2_traits))
        
        # Child inherits 60-80% of combined parent traits
        inheritance_rate = random.uniform(0.6, 0.8)
        num_inherited = int(len(all_traits) * inheritance_rate)
        inherited_traits = random.sample(all_traits, min(num_inherited, len(all_traits)))
        
        # Possible mutations (new traits)
        possible_mutations = [
            "creative", "analytical", "spiritual", "practical", "diplomatic",
            "rebellious", "cautious", "bold", "compassionate", "logical",
            "artistic", "strategic", "independent", "collaborative", "innovative"
        ]
        
        # Add mutations
        if random.random() < mutation_rate:
            available_mutations = [t for t in possible_mutations if t not in inherited_traits]
            if available_mutations:
                mutation = random.choice(available_mutations)
                inherited_traits.append(mutation)
        
        # Ensure child has 2-5 traits
        while len(inherited_traits) < 2:
            trait = random.choice(possible_mutations)
            if trait not in inherited_traits:
                inherited_traits.append(trait)
        
        return inherited_traits[:5]  # Max 5 traits
    
    @staticmethod
    def combine_personality_scores(parent1_scores: Dict[str, float], 
                                 parent2_scores: Dict[str, float],
                                 variance: float = 0.2) -> Dict[str, float]:
        """
        Combine personality scores with some variance.
        """
        combined_scores = {}
        
        for trait in ["openness", "conscientiousness", "extraversion", 
                     "agreeableness", "neuroticism"]:
            p1_score = parent1_scores.get(trait, 0.5)
            p2_score = parent2_scores.get(trait, 0.5)
            
            # Average parent scores with random variance
            base_score = (p1_score + p2_score) / 2
            variance_amount = random.uniform(-variance, variance)
            final_score = max(0.0, min(1.0, base_score + variance_amount))
            
            combined_scores[trait] = final_score
        
        return combined_scores
    
    @staticmethod
    def inherit_goals(parent1_goals: List[str], parent2_goals: List[str],
                     agent_traits: List[str]) -> List[str]:
        """
        Create goals for child based on parent goals and child's traits.
        """
        # Possible inherited goals
        inherited_goals = []
        
        # 30% chance to inherit each parent goal
        for goal in parent1_goals + parent2_goals:
            if random.random() < 0.3:
                inherited_goals.append(goal)
        
        # Generate trait-based goals
        trait_goals = {
            "curious": ["explore new places", "learn about the world", "discover secrets"],
            "kind": ["help others", "protect the innocent", "spread kindness"],
            "ambitious": ["gain recognition", "achieve greatness", "lead others"],
            "creative": ["create beautiful things", "express myself", "inspire others"],
            "protective": ["defend family", "maintain security", "guard traditions"],
            "rebellious": ["challenge authority", "fight injustice", "change the world"],
            "spiritual": ["understand the divine", "find inner peace", "guide others"]
        }
        
        for trait in agent_traits:
            if trait in trait_goals and random.random() < 0.4:
                goal = random.choice(trait_goals[trait])
                if goal not in inherited_goals:
                    inherited_goals.append(goal)
        
        # Ensure child has at least 1-3 goals
        if not inherited_goals:
            default_goals = ["find happiness", "make friends", "grow strong"]
            inherited_goals = [random.choice(default_goals)]
        
        return inherited_goals[:3]  # Max 3 goals


class FamilyManager:
    """
    Manages family relationships, reproduction, and lineage tracking.
    """
    
    def __init__(self):
        self.next_agent_id = 1000  # Start offspring IDs from 1000
        self.family_trees = {}  # agent_id -> family tree data
        
    def can_reproduce(self, agent1: Any, agent2: Any, world_day: int) -> Tuple[bool, str]:
        """
        Check if two agents can reproduce together.
        
        Returns:
            Tuple of (can_reproduce: bool, reason: str)
        """
        # Basic requirements
        if not (agent1.is_alive and agent2.is_alive):
            return False, "One or both agents are not alive"
        
        # Age requirements (must be adults)
        if agent1.age < 18 or agent2.age < 18:
            return False, "Agents must be adults (18+) to reproduce"
        
        # Health requirements
        if agent1.health < 0.3 or agent2.health < 0.3:
            return False, "Agents must be healthy enough to reproduce"
        
        # Relationship requirements
        relationship = agent1.relationships.get(agent2.name, "stranger")
        if relationship not in ["friend", "partner", "spouse"]:
            return False, f"Relationship '{relationship}' not suitable for reproduction"
        
        # Check for family relations (prevent incest)
        if self._are_related(agent1, agent2):
            return False, "Agents are too closely related"
        
        # Check if either agent has reproduced recently (cooldown period)
        if self._recently_reproduced(agent1, world_day) or self._recently_reproduced(agent2, world_day):
            return False, "One or both agents have reproduced recently"
        
        return True, "All requirements met"
    
    def _are_related(self, agent1: Any, agent2: Any) -> bool:
        """Check if two agents are closely related (siblings, parent-child)."""
        # Check if they share parents
        agent1_parents = set(agent1.family.get("parents", []))
        agent2_parents = set(agent2.family.get("parents", []))
        
        if agent1_parents & agent2_parents:  # Shared parents = siblings
            return True
        
        # Check parent-child relationships
        if agent1.name in agent2.family.get("parents", []):
            return True
        if agent2.name in agent1.family.get("parents", []):
            return True
        
        return False
    
    def _recently_reproduced(self, agent: Any, world_day: int, cooldown_days: int = 365) -> bool:
        """Check if agent has reproduced within cooldown period."""
        # Check if agent has children and when the last one was born
        children = agent.family.get("children", [])
        if not children:
            return False
        
        # For now, assume we don't track birth dates precisely
        # In a full implementation, you'd check the actual birth dates
        return False
    
    def create_offspring(self, parent1: Any, parent2: Any, world_day: int, 
                        simulation_engine: Any = None) -> Dict[str, Any]:
        """
        Create a new agent offspring from two parents.
        
        Returns:
            Configuration dictionary for the new agent
        """
        # Generate basic info
        child_id = f"agent_{self.next_agent_id}"
        self.next_agent_id += 1
        
        # Choose name (could be more sophisticated)
        possible_names = [
            "Alex", "Jordan", "Riley", "Casey", "Avery", "Quinn", "Sage", "River",
            "Emery", "Rowan", "Skyler", "Phoenix", "Blair", "Reese", "Cameron"
        ]
        child_name = random.choice(possible_names)
        
        # Ensure unique name
        if simulation_engine:
            existing_names = [agent.name for agent in simulation_engine.agents]
            while child_name in existing_names:
                child_name = random.choice(possible_names) + str(random.randint(1, 99))
        
        # Genetic combination
        child_traits = GeneticSystem.combine_traits(parent1.traits, parent2.traits)
        child_personality = GeneticSystem.combine_personality_scores(
            parent1.personality_scores, parent2.personality_scores
        )
        child_goals = GeneticSystem.inherit_goals(parent1.goals, parent2.goals, child_traits)
        
        # Determine location (same as parents initially)
        child_location = parent1.location
        
        # Basic starting stats for newborn
        child_config = {
            "id": child_id,
            "name": child_name,
            "age": 0,  # Newborn
            "birth_day": world_day,
            "traits": child_traits,
            "personality_scores": child_personality,
            "goals": child_goals,
            "current_goal": child_goals[0] if child_goals else "grow up",
            "emotion": "curious",
            "emotion_intensity": 0.6,
            "relationships": {
                parent1.name: "parent",
                parent2.name: "parent"
            },
            "family": {
                "parents": [parent1.name, parent2.name],
                "siblings": [],
                "children": []
            },
            "location": child_location,
            "health": 1.0,
            "energy": 0.8,
            "skills": {},  # Will develop over time
            "beliefs": {},  # Will develop based on parents/community
            "values": [],   # Will develop over time
            "reputation": 0.5,
            "life_satisfaction": 0.8,
            "is_alive": True
        }
        
        # Update parent family records
        parent1.family.setdefault("children", []).append(child_name)
        parent2.family.setdefault("children", []).append(child_name)
        
        # Add child as relationship
        parent1.relationships[child_name] = "child"
        parent2.relationships[child_name] = "child"
        
        # Update siblings relationships
        self._update_sibling_relationships(child_config, [parent1, parent2], simulation_engine)
        
        # Store family tree data
        self.family_trees[child_id] = {
            "parents": [parent1.id, parent2.id],
            "birth_day": world_day,
            "generation": self._calculate_generation(parent1, parent2) + 1
        }
        
        return child_config
    
    def _update_sibling_relationships(self, child_config: Dict[str, Any], 
                                    parents: List[Any], simulation_engine: Any) -> None:
        """Update sibling relationships for new child and existing children."""
        if not simulation_engine:
            return
        
        # Find existing children of these parents
        parent_names = [p.name for p in parents]
        
        for agent in simulation_engine.agents:
            agent_parents = agent.family.get("parents", [])
            
            # Check if this agent shares at least one parent
            if any(parent in parent_names for parent in agent_parents):
                if agent.name != child_config["name"]:
                    # Add as sibling
                    child_config["family"]["siblings"].append(agent.name)
                    child_config["relationships"][agent.name] = "sibling"
                    
                    # Update existing agent's records
                    agent.family.setdefault("siblings", []).append(child_config["name"])
                    agent.relationships[child_config["name"]] = "sibling"
    
    def _calculate_generation(self, parent1: Any, parent2: Any) -> int:
        """Calculate generation number for offspring."""
        # Simple generation calculation
        p1_gen = self.family_trees.get(parent1.id, {}).get("generation", 0)
        p2_gen = self.family_trees.get(parent2.id, {}).get("generation", 0)
        return max(p1_gen, p2_gen)
    
    def attempt_reproduction(self, agent1: Any, agent2: Any, world_day: int,
                           simulation_engine: Any = None) -> Optional[Dict[str, Any]]:
        """
        Attempt reproduction between two agents.
        
        Returns:
            New agent config if successful, None if failed
        """
        can_reproduce, reason = self.can_reproduce(agent1, agent2, world_day)
        
        if not can_reproduce:
            return None
        
        # Base reproduction chance (could be modified by traits, health, etc.)
        base_chance = 0.1  # 10% chance per attempt
        
        # Modify chance based on relationship strength
        relationship = agent1.relationships.get(agent2.name, "stranger")
        if relationship == "spouse":
            base_chance *= 1.5
        elif relationship == "partner":
            base_chance *= 1.2
        
        # Modify chance based on health and age
        health_modifier = (agent1.health + agent2.health) / 2
        age_modifier = max(0.5, 1.0 - (max(agent1.age, agent2.age) - 25) * 0.02)
        
        final_chance = base_chance * health_modifier * age_modifier
        
        if random.random() < final_chance:
            child_config = self.create_offspring(agent1, agent2, world_day, simulation_engine)
            
            # Store memories of the birth
            birth_memory = f"Had a child named {child_config['name']} with {agent2.name if agent1 else agent1.name}"
            agent1.memory.store_memory(birth_memory, importance=0.9, emotion="joyful", memory_type="experience")
            agent2.memory.store_memory(birth_memory, importance=0.9, emotion="joyful", memory_type="experience")
            
            return child_config
        
        return None
    
    def get_family_tree(self, agent_id: str, depth: int = 3) -> Dict[str, Any]:
        """
        Get family tree information for an agent.
        
        Args:
            agent_id: ID of the agent
            depth: How many generations to include (both up and down)
            
        Returns:
            Family tree data
        """
        if agent_id not in self.family_trees:
            return {"error": "Agent not found in family trees"}
        
        tree_data = self.family_trees[agent_id].copy()
        
        # Could expand this to include full ancestry/descendant data
        # For now, return basic information
        return tree_data
    
    def get_population_genetics_stats(self, agents: List[Any]) -> Dict[str, Any]:
        """
        Analyze population genetics and family statistics.
        """
        stats = {
            "total_agents": len(agents),
            "families": 0,
            "children": 0,
            "adults": 0,
            "elders": 0,
            "trait_distribution": {},
            "average_age": 0,
            "generations": set()
        }
        
        if not agents:
            return stats
        
        total_age = 0
        trait_counts = {}
        
        for agent in agents:
            total_age += agent.age
            
            # Age categories
            if agent.age < 18:
                stats["children"] += 1
            elif agent.age < 60:
                stats["adults"] += 1
            else:
                stats["elders"] += 1
            
            # Trait distribution
            for trait in agent.traits:
                trait_counts[trait] = trait_counts.get(trait, 0) + 1
            
            # Family tracking
            if agent.family.get("children"):
                stats["families"] += 1
            
            # Generation tracking
            if agent.id in self.family_trees:
                gen = self.family_trees[agent.id].get("generation", 0)
                stats["generations"].add(gen)
        
        stats["average_age"] = total_age / len(agents)
        stats["trait_distribution"] = {trait: count/len(agents) for trait, count in trait_counts.items()}
        stats["max_generation"] = max(stats["generations"]) if stats["generations"] else 0
        
        return stats 