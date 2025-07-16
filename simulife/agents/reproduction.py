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
    def combine_genetic_traits(parent1_genetics: Dict[str, Any], 
                              parent2_genetics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Combine genetic traits from two parents using realistic inheritance patterns.
        """
        combined_genetics = {}
        
        # Height - average with some variance
        p1_height = parent1_genetics.get("height", 170)
        p2_height = parent2_genetics.get("height", 170) 
        base_height = (p1_height + p2_height) / 2
        combined_genetics["height"] = random.uniform(base_height - 10, base_height + 10)
        
        # Build - inherit from one parent or be intermediate
        builds = [parent1_genetics.get("build", "average"), parent2_genetics.get("build", "average")]
        if random.random() < 0.3:  # 30% chance of intermediate build
            combined_genetics["build"] = "average"
        else:
            combined_genetics["build"] = random.choice(builds)
        
        # Eye color - simple dominant/recessive model
        eye_colors = [parent1_genetics.get("eye_color", "brown"), parent2_genetics.get("eye_color", "brown")]
        if "brown" in eye_colors:
            combined_genetics["eye_color"] = "brown" if random.random() < 0.7 else random.choice(eye_colors)
        else:
            combined_genetics["eye_color"] = random.choice(eye_colors)
        
        # Hair color - simple inheritance
        hair_colors = [parent1_genetics.get("hair_color", "brown"), parent2_genetics.get("hair_color", "brown")]
        combined_genetics["hair_color"] = random.choice(hair_colors)
        
        # Genetic predispositions - can inherit from either parent
        p1_predispositions = parent1_genetics.get("genetic_predispositions", [])
        p2_predispositions = parent2_genetics.get("genetic_predispositions", [])
        all_predispositions = list(set(p1_predispositions + p2_predispositions))
        # Inherit 50-80% of parental predispositions
        num_inherit = int(len(all_predispositions) * random.uniform(0.5, 0.8))
        combined_genetics["genetic_predispositions"] = random.sample(
            all_predispositions, min(num_inherit, len(all_predispositions))
        )
        
        # Genetic weaknesses - unfortunately, can also be inherited
        p1_weaknesses = parent1_genetics.get("genetic_weaknesses", [])
        p2_weaknesses = parent2_genetics.get("genetic_weaknesses", [])
        all_weaknesses = list(set(p1_weaknesses + p2_weaknesses))
        # 30% chance to inherit each weakness
        inherited_weaknesses = [w for w in all_weaknesses if random.random() < 0.3]
        combined_genetics["genetic_weaknesses"] = inherited_weaknesses
        
        return combined_genetics
    
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
        self.pregnancy_manager = PregnancyManager()  # Manage pregnancies
        
    def can_reproduce(self, agent1: Any, agent2: Any, world_day: int) -> Tuple[bool, str]:
        """
        Check if two agents can reproduce together.
        
        Returns:
            Tuple of (can_reproduce: bool, reason: str)
        """
        # Basic requirements
        if not (agent1.is_alive and agent2.is_alive):
            return False, "One or both agents are not alive"
        
        # Gender requirements (need male and female)
        if agent1.gender == agent2.gender:
            return False, "Both agents are the same gender"
        
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
        
        # Check if female agent is already pregnant
        female_agent = agent1 if agent1.gender == "female" else agent2
        if self.pregnancy_manager.is_pregnant(female_agent.name):
            return False, f"{female_agent.name} is already pregnant"
        
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
        
        # Generate child gender
        child_gender = random.choice(["male", "female"])
        
        # Choose name based on gender and cultural preferences
        male_names = [
            "Aiden", "Caleb", "Ethan", "Finn", "Gabriel", "Isaac", "Jasper", "Knox",
            "Liam", "Miles", "Noah", "Owen", "Phoenix", "River", "Sage", "Theo"
        ]
        female_names = [
            "Aria", "Blair", "Clara", "Eden", "Fiona", "Grace", "Harper", "Iris", 
            "Jade", "Kira", "Luna", "Maya", "Nora", "Olive", "Quinn", "River"
        ]
        
        if child_gender == "male":
            child_name = random.choice(male_names)
        else:
            child_name = random.choice(female_names)
        
        # Ensure unique name
        if simulation_engine:
            existing_names = [agent.name for agent in simulation_engine.agents]
            while child_name in existing_names:
                base_name = random.choice(male_names if child_gender == "male" else female_names)
                child_name = f"{base_name}{random.randint(1, 99)}"
        
        # Determine family name inheritance 
        # Children inherit family name from one parent (traditionally from father, but can vary)
        family_names = []
        if hasattr(parent1, 'family_name'):
            family_names.append(parent1.family_name)
        if hasattr(parent2, 'family_name'):
            family_names.append(parent2.family_name)
        
        if family_names:
            child_family_name = random.choice(family_names)
        else:
            # Create new family name if parents don't have one
            prefixes = ["Stone", "River", "Mountain", "Forest", "Star", "Moon", "Sun", "Wind"]
            suffixes = ["heart", "walker", "keeper", "born", "wise", "strong", "bright", "clan"]
            child_family_name = f"{random.choice(prefixes)}{random.choice(suffixes)}"
        
        # Genetic combination
        child_traits = GeneticSystem.combine_traits(parent1.traits, parent2.traits)
        child_personality = GeneticSystem.combine_personality_scores(
            parent1.personality_scores, parent2.personality_scores
        )
        child_goals = GeneticSystem.inherit_goals(parent1.goals, parent2.goals, child_traits)
        
        # Combine genetic traits from parents
        parent1_genetics = getattr(parent1, 'genetic_traits', {})
        parent2_genetics = getattr(parent2, 'genetic_traits', {})
        child_genetic_traits = GeneticSystem.combine_genetic_traits(parent1_genetics, parent2_genetics)
        
        # Calculate generation
        parent1_gen = getattr(parent1, 'generation', 1)
        parent2_gen = getattr(parent2, 'generation', 1) 
        child_generation = max(parent1_gen, parent2_gen) + 1
        
        # Determine location (same as parents initially)
        child_location = parent1.location
        
        # Basic starting stats for newborn
        child_config = {
            "id": child_id,
            "name": child_name,
            "age": 0,  # Newborn
            "birth_day": world_day,
            
            # Biological attributes
            "gender": child_gender,
            "fertility": 0.0,  # Infertile until maturity
            "genetic_traits": child_genetic_traits,
            "generation": child_generation,
            "family_name": child_family_name,
            "parents": [parent1.name, parent2.name],
            "children": [],
            
            # Inherited traits and personality
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
            Pregnancy data if conception successful, None if failed
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
        
        # Modify chance based on health, age, and fertility
        health_modifier = (agent1.health + agent2.health) / 2
        age_modifier = max(0.5, 1.0 - (max(agent1.age, agent2.age) - 25) * 0.02)
        fertility_modifier = (agent1.fertility + agent2.fertility) / 2
        
        final_chance = base_chance * health_modifier * age_modifier * fertility_modifier
        
        if random.random() < final_chance:
            # Conception successful! Start pregnancy
            mother = agent1 if agent1.gender == "female" else agent2
            father = agent2 if mother == agent1 else agent1
            
            pregnancy_data = self.pregnancy_manager.start_pregnancy(mother, father, world_day)
            
            # Store memories of conception
            conception_memory = f"Conceived a child with {father.name if mother else mother.name}"
            mother.memory.store_memory(conception_memory, importance=0.8, emotion="hopeful", memory_type="experience")
            father.memory.store_memory(f"My partner {mother.name} is pregnant with our child", importance=0.8, emotion="excited", memory_type="experience")
            
            return pregnancy_data
        
        return None
    
    def check_pregnancies(self, current_day: int, simulation_engine: Any = None) -> List[Dict[str, Any]]:
        """
        Check for pregnancies that are due and deliver babies.
        
        Returns:
            List of birth events
        """
        return self.pregnancy_manager.check_due_pregnancies(current_day, simulation_engine)
    
    def get_pregnancy_info(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get pregnancy information for an agent."""
        return self.pregnancy_manager.get_pregnancy_status(agent_name)
    
    def is_agent_pregnant(self, agent_name: str) -> bool:
        """Check if an agent is currently pregnant."""
        return self.pregnancy_manager.is_pregnant(agent_name)
    
    def get_all_pregnancies(self) -> Dict[str, Dict[str, Any]]:
        """Get all active pregnancies."""
        return self.pregnancy_manager.get_all_pregnancies()
    
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


class PregnancyManager:
    """
    Manages pregnancies with realistic 9-month gestation periods.
    """
    
    def __init__(self):
        self.active_pregnancies = {}  # agent_name -> pregnancy_data
    
    def start_pregnancy(self, mother: Any, father: Any, conception_day: int) -> Dict[str, Any]:
        """
        Start a pregnancy for a female agent.
        
        Returns:
            Pregnancy data dictionary
        """
        pregnancy_id = f"pregnancy_{conception_day}_{mother.name}_{father.name}"
        gestation_days = 270  # 9 months (30 days per month)
        due_date = conception_day + gestation_days
        
        pregnancy_data = {
            "id": pregnancy_id,
            "mother": mother.name,
            "father": father.name,
            "conception_day": conception_day,
            "due_date": due_date,
            "gestation_days": gestation_days,
            "status": "active",  # active, completed, miscarried
            "complications": [],
            "multiple_birth": random.random() < 0.03,  # 3% chance of twins
            "baby_gender": None,  # Determined later
            "baby_count": 2 if random.random() < 0.03 else 1
        }
        
        # Store pregnancy
        self.active_pregnancies[mother.name] = pregnancy_data
        
        # Update mother's status
        if not hasattr(mother, 'pregnancies'):
            mother.pregnancies = []
        mother.pregnancies.append(pregnancy_data)
        
        return pregnancy_data
    
    def check_due_pregnancies(self, current_day: int, simulation_engine: Any = None) -> List[Dict[str, Any]]:
        """
        Check for pregnancies that are due and deliver babies.
        
        Returns:
            List of birth events
        """
        births = []
        completed_pregnancies = []
        
        for mother_name, pregnancy_data in self.active_pregnancies.items():
            if pregnancy_data["status"] != "active":
                continue
                
            if current_day >= pregnancy_data["due_date"]:
                # Time to give birth!
                birth_events = self._deliver_baby(pregnancy_data, current_day, simulation_engine)
                births.extend(birth_events)
                completed_pregnancies.append(mother_name)
        
        # Remove completed pregnancies
        for mother_name in completed_pregnancies:
            self.active_pregnancies[mother_name]["status"] = "completed"
            del self.active_pregnancies[mother_name]
        
        return births
    
    def _deliver_baby(self, pregnancy_data: Dict[str, Any], birth_day: int, 
                     simulation_engine: Any = None) -> List[Dict[str, Any]]:
        """
        Deliver baby(ies) from a pregnancy.
        
        Returns:
            List of birth events
        """
        if not simulation_engine:
            return []
        
        # Find the parents
        mother = None
        father = None
        for agent in simulation_engine.agents:
            if agent.name == pregnancy_data["mother"]:
                mother = agent
            elif agent.name == pregnancy_data["father"]:
                father = agent
        
        if not (mother and father):
            return []
        
        birth_events = []
        baby_count = pregnancy_data["baby_count"]
        
        for baby_num in range(baby_count):
            # Create baby using existing offspring creation system
            family_manager = simulation_engine.family_manager
            child_config = family_manager.create_offspring(mother, father, birth_day, simulation_engine)
            
            # Create new agent and add to simulation
            new_agent = type(mother)(child_config, birth_day)
            
            # Initialize systems for child
            if hasattr(simulation_engine, 'genetic_disease_system'):
                child_genetics = simulation_engine.genetic_disease_system.inherit_diseases_from_parents(
                    new_agent, mother, father)
            
            if hasattr(simulation_engine, 'generational_culture_system'):
                child_culture = simulation_engine.generational_culture_system.initialize_agent_culture(
                    new_agent, birth_day)
            
            simulation_engine.agents.append(new_agent)
            
            # Log the birth event
            birth_event = {
                "child_name": child_config["name"],
                "parents": [mother.name, father.name],
                "location": mother.location,
                "birth_day": birth_day,
                "pregnancy_duration": birth_day - pregnancy_data["conception_day"],
                "baby_number": baby_num + 1,
                "total_babies": baby_count,
                "is_multiple": baby_count > 1
            }
            
            birth_events.append(birth_event)
            
            # Store memories of the birth
            birth_memory = f"Gave birth to {child_config['name']} after 9 months of pregnancy"
            mother.memory.store_memory(birth_memory, importance=0.95, emotion="joyful", memory_type="experience")
            
            father_memory = f"My child {child_config['name']} was born to {mother.name} after 9 months"
            father.memory.store_memory(father_memory, importance=0.9, emotion="joyful", memory_type="experience")
        
        return birth_events
    
    def get_pregnancy_status(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get current pregnancy status for an agent."""
        return self.active_pregnancies.get(agent_name)
    
    def is_pregnant(self, agent_name: str) -> bool:
        """Check if an agent is currently pregnant."""
        pregnancy = self.active_pregnancies.get(agent_name)
        return pregnancy is not None and pregnancy["status"] == "active"
    
    def get_all_pregnancies(self) -> Dict[str, Dict[str, Any]]:
        """Get all active pregnancies."""
        return self.active_pregnancies.copy() 