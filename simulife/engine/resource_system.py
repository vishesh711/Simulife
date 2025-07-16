"""
Resource and Economic System for SimuLife
Manages resource-based decision making, trade, scarcity effects, and economic pressure.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ResourceType(Enum):
    """Types of resources in the world."""
    FOOD = "food"
    WATER = "water"
    SHELTER = "shelter"
    MATERIALS = "materials"
    KNOWLEDGE = "knowledge"
    ENERGY = "energy"
    TOOLS = "tools"


@dataclass
class ResourceTransaction:
    """Represents a trade or resource exchange."""
    day: int
    giver: str
    receiver: str
    resource_type: str
    amount: float
    trade_value: float  # What was exchanged for it
    reason: str  # trade, gift, payment, etc.


@dataclass
class ResourceNeed:
    """Represents an agent's resource need."""
    resource_type: str
    current_level: float
    desired_level: float
    urgency: float  # 0-1, how urgent the need is
    willing_to_trade: List[str]  # Resources willing to trade for this


class ResourceSystem:
    """
    Manages resource-based decision making and economic interactions.
    """
    
    def __init__(self):
        self.transactions: List[ResourceTransaction] = []
        self.resource_history = {}  # Track resource levels over time
        self.market_prices = {  # Dynamic pricing based on scarcity
            "food": 1.0,
            "water": 1.0, 
            "shelter": 1.0,
            "materials": 1.0,
            "knowledge": 1.0,
            "energy": 1.0,
            "tools": 1.0
        }
        self.resource_specialists = {}  # Track who specializes in what
        
    def initialize_agent_resources(self, agent: Any) -> None:
        """Initialize an agent's personal resource tracking."""
        if not hasattr(agent, 'personal_resources'):
            agent.personal_resources = {
                "food": random.uniform(0.5, 0.8),
                "water": random.uniform(0.6, 0.9),
                "shelter": random.uniform(0.4, 0.7),
                "materials": random.uniform(0.2, 0.5),
                "knowledge": random.uniform(0.3, 0.6),
                "energy": random.uniform(0.6, 1.0),
                "tools": random.uniform(0.1, 0.4)
            }
        
        if not hasattr(agent, 'resource_preferences'):
            agent.resource_preferences = self._generate_resource_preferences(agent)

    def _generate_resource_preferences(self, agent: Any) -> Dict[str, float]:
        """Generate agent's preferences for different resources based on traits."""
        preferences = {
            "food": 0.8,  # Base importance
            "water": 0.9,
            "shelter": 0.7,
            "materials": 0.5,
            "knowledge": 0.6,
            "energy": 0.7,
            "tools": 0.4
        }
        
        # Modify based on traits
        if "curious" in agent.traits:
            preferences["knowledge"] += 0.3
        if "practical" in agent.traits:
            preferences["tools"] += 0.4
            preferences["materials"] += 0.3
        if "protective" in agent.traits:
            preferences["shelter"] += 0.3
            preferences["food"] += 0.2
        if "ambitious" in agent.traits:
            preferences["knowledge"] += 0.2
            preferences["materials"] += 0.2
        if "creative" in agent.traits:
            preferences["materials"] += 0.3
            preferences["tools"] += 0.2
            
        return preferences

    def assess_agent_needs(self, agent: Any, world_resources: Dict[str, float]) -> List[ResourceNeed]:
        """Assess what resources an agent currently needs."""
        self.initialize_agent_resources(agent)
        
        needs = []
        for resource_type, current_level in agent.personal_resources.items():
            desired_level = agent.resource_preferences.get(resource_type, 0.5)
            
            if current_level < desired_level:
                # Calculate urgency based on how far below desired level
                deficit = desired_level - current_level
                urgency = min(1.0, deficit * 2.0)  # Higher deficit = more urgent
                
                # Increase urgency if world resources are also scarce
                world_level = world_resources.get(resource_type, 0.5)
                if world_level < 0.4:
                    urgency = min(1.0, urgency + 0.3)
                
                # Determine what agent is willing to trade
                willing_to_trade = []
                for other_resource, other_level in agent.personal_resources.items():
                    if (other_level > agent.resource_preferences.get(other_resource, 0.5) and
                        other_resource != resource_type):
                        willing_to_trade.append(other_resource)
                
                needs.append(ResourceNeed(
                    resource_type=resource_type,
                    current_level=current_level,
                    desired_level=desired_level,
                    urgency=urgency,
                    willing_to_trade=willing_to_trade
                ))
        
        # Sort by urgency
        needs.sort(key=lambda n: n.urgency, reverse=True)
        return needs

    def modify_action_for_resources(self, agent: Any, base_action: str, 
                                  world_resources: Dict[str, float]) -> str:
        """Modify an agent's action based on resource needs."""
        needs = self.assess_agent_needs(agent, world_resources)
        
        if not needs:
            return base_action  # No pressing needs
            
        urgent_need = needs[0]
        
        # If need is very urgent (>0.7), override action
        if urgent_need.urgency > 0.7:
            return self._generate_resource_seeking_action(agent, urgent_need, world_resources)
        
        # If moderately urgent (>0.4), modify action if it makes sense
        elif urgent_need.urgency > 0.4:
            modified_action = self._modify_action_for_need(agent, base_action, urgent_need)
            if modified_action != base_action:
                return modified_action
                
        return base_action

    def _generate_resource_seeking_action(self, agent: Any, need: ResourceNeed, 
                                        world_resources: Dict[str, float]) -> str:
        """Generate an action focused on obtaining a needed resource."""
        resource_actions = {
            "food": [
                f"{agent.name} desperately searches for food in the {agent.location}",
                f"{agent.name} attempts to gather edible plants and hunt",
                f"{agent.name} looks for someone willing to share food"
            ],
            "water": [
                f"{agent.name} urgently seeks a source of clean water",
                f"{agent.name} travels to the river to collect water",
                f"{agent.name} asks others about water sources"
            ],
            "shelter": [
                f"{agent.name} works on improving their shelter against the elements",
                f"{agent.name} gathers materials to build better protection",
                f"{agent.name} seeks help from others to construct shelter"
            ],
            "materials": [
                f"{agent.name} scavenges for useful materials and resources",
                f"{agent.name} explores the area looking for raw materials",
                f"{agent.name} attempts to trade for needed materials"
            ],
            "knowledge": [
                f"{agent.name} seeks out others who might teach them new skills",
                f"{agent.name} carefully observes others to learn new techniques",
                f"{agent.name} experiments and tries to discover new knowledge"
            ],
            "energy": [
                f"{agent.name} rests to recover energy and strength",
                f"{agent.name} takes time to restore their vitality",
                f"{agent.name} finds a quiet place to recuperate"
            ],
            "tools": [
                f"{agent.name} attempts to craft or find useful tools",
                f"{agent.name} looks for materials to make better implements",
                f"{agent.name} asks others about tool-making techniques"
            ]
        }
        
        actions = resource_actions.get(need.resource_type, [
            f"{agent.name} focuses on addressing their {need.resource_type} shortage"
        ])
        
        return random.choice(actions)

    def _modify_action_for_need(self, agent: Any, base_action: str, need: ResourceNeed) -> str:
        """Modify a base action to incorporate resource considerations."""
        # If action involves socializing, mention the need
        if "socialize" in base_action or "conversation" in base_action:
            return f"{agent.name} socializes with others, hoping to learn about {need.resource_type} sources"
        
        # If action involves exploring, focus on resource finding
        if "explore" in base_action:
            return f"{agent.name} explores the area, particularly looking for {need.resource_type}"
        
        # If action involves helping, mention resource exchange
        if "help" in base_action:
            return f"{agent.name} offers help to others, hoping they might share {need.resource_type}"
            
        return base_action

    def attempt_resource_trade(self, agent1: Any, agent2: Any, world_day: int) -> Optional[ResourceTransaction]:
        """Attempt a trade between two agents."""
        # Both agents need to have resource tracking
        self.initialize_agent_resources(agent1)
        self.initialize_agent_resources(agent2)
        
        # Get what each agent needs and can offer
        agent1_needs = self.assess_agent_needs(agent1, {})
        agent2_needs = self.assess_agent_needs(agent2, {})
        
        if not agent1_needs or not agent2_needs:
            return None
            
        # Find mutually beneficial trades
        for need1 in agent1_needs:
            for need2 in agent2_needs:
                # Check if agent1 can provide what agent2 needs
                if (need2.resource_type in need1.willing_to_trade and
                    need1.resource_type in need2.willing_to_trade):
                    
                    # Calculate trade amounts
                    trade_amount = min(0.2, need1.urgency * 0.3, need2.urgency * 0.3)
                    
                    # Check if both agents actually have resources to trade
                    if (agent1.personal_resources.get(need2.resource_type, 0) > trade_amount and
                        agent2.personal_resources.get(need1.resource_type, 0) > trade_amount):
                        
                        # Execute the trade
                        self._execute_trade(agent1, agent2, need1.resource_type, 
                                          need2.resource_type, trade_amount, world_day)
                        
                        return ResourceTransaction(
                            day=world_day,
                            giver=agent1.name,
                            receiver=agent2.name,
                            resource_type=need1.resource_type,
                            amount=trade_amount,
                            trade_value=trade_amount,  # 1:1 trade for simplicity
                            reason="trade"
                        )
        
        return None

    def _execute_trade(self, agent1: Any, agent2: Any, resource1: str, 
                      resource2: str, amount: float, world_day: int) -> None:
        """Execute a trade between two agents."""
        # Transfer resources
        agent1.personal_resources[resource1] += amount
        agent1.personal_resources[resource2] -= amount
        agent2.personal_resources[resource1] -= amount  
        agent2.personal_resources[resource2] += amount
        
        # Ensure resources don't go negative or above 1.0
        for agent in [agent1, agent2]:
            for resource_type in agent.personal_resources:
                agent.personal_resources[resource_type] = max(0.0, min(1.0, 
                    agent.personal_resources[resource_type]))
        
        # Create memories of the trade
        trade_memory1 = f"Traded {resource2} with {agent2.name} for {resource1}"
        trade_memory2 = f"Traded {resource1} with {agent1.name} for {resource2}"
        
        agent1.memory.store_memory(trade_memory1, importance=0.5, 
                                 emotion="satisfied", memory_type="experience")
        agent2.memory.store_memory(trade_memory2, importance=0.5,
                                 emotion="satisfied", memory_type="experience")
        
        # Improve relationship slightly
        current_rel1 = agent1.relationships.get(agent2.name, "stranger")
        current_rel2 = agent2.relationships.get(agent1.name, "stranger")
        
        if current_rel1 == "stranger":
            agent1.relationships[agent2.name] = "acquaintance"
        if current_rel2 == "stranger":
            agent2.relationships[agent1.name] = "acquaintance"

    def process_resource_consumption(self, agent: Any, world_day: int) -> None:
        """Process daily resource consumption for an agent."""
        self.initialize_agent_resources(agent)
        
        # Base consumption rates
        consumption = {
            "food": 0.05,
            "water": 0.08, 
            "energy": 0.1,
            "shelter": 0.02,  # Gradual wear
            "tools": 0.01,    # Very slow wear
            "materials": 0.0,  # No passive consumption
            "knowledge": 0.0   # No passive consumption
        }
        
        # Modify consumption based on agent activity and traits
        if "active" in agent.last_action.lower() or "explore" in agent.last_action.lower():
            consumption["food"] += 0.02
            consumption["water"] += 0.03
            consumption["energy"] += 0.05
        
        if agent.health < 0.5:  # Sick agents need more resources
            consumption["food"] += 0.02
            consumption["water"] += 0.02
            
        # Apply consumption
        for resource_type, rate in consumption.items():
            if resource_type in agent.personal_resources:
                agent.personal_resources[resource_type] -= rate
                agent.personal_resources[resource_type] = max(0.0, 
                    agent.personal_resources[resource_type])
        
        # Health effects from resource levels
        self._apply_resource_health_effects(agent)

    def _apply_resource_health_effects(self, agent: Any) -> None:
        """Apply health effects based on resource levels."""
        # Critical resources affecting health
        food_level = agent.personal_resources.get("food", 0.5)
        water_level = agent.personal_resources.get("water", 0.5)
        shelter_level = agent.personal_resources.get("shelter", 0.5)
        
        # Health impact calculation
        health_impact = 0
        
        if food_level < 0.2:
            health_impact -= 0.02  # Starving
        elif food_level < 0.4:
            health_impact -= 0.01  # Hungry
            
        if water_level < 0.2:
            health_impact -= 0.03  # Dehydrated
        elif water_level < 0.4:
            health_impact -= 0.015  # Thirsty
            
        if shelter_level < 0.3:
            health_impact -= 0.01  # Exposed to elements
            
        # Apply health changes
        agent.health = max(0.1, min(1.0, agent.health + health_impact))
        
        # Emotional effects
        if health_impact < -0.02:
            agent.emotion = "suffering"
            agent.emotion_intensity = 0.8
        elif health_impact < 0:
            if agent.emotion not in ["suffering", "worried"]:
                agent.emotion = "worried"
                agent.emotion_intensity = min(1.0, agent.emotion_intensity + 0.2)

    def generate_resource_specialization(self, agent: Any, world_day: int) -> Optional[str]:
        """Generate resource specialization for agents based on their traits and experience."""
        # Check if agent already has specialization
        if hasattr(agent, 'resource_specialization') and agent.resource_specialization:
            return None
            
        # Determine specialization based on traits and skills
        specialization_map = {
            "practical": ["food_production", "shelter_building", "tool_crafting"],
            "curious": ["knowledge_gathering", "exploration", "innovation"],
            "kind": ["resource_sharing", "community_support", "healing"],
            "creative": ["tool_crafting", "innovation", "cultural_creation"],
            "protective": ["shelter_building", "resource_protection", "security"],
            "wise": ["knowledge_gathering", "teaching", "resource_management"]
        }
        
        possible_specializations = []
        for trait in agent.traits:
            if trait in specialization_map:
                possible_specializations.extend(specialization_map[trait])
        
        if not possible_specializations:
            return None
            
        # Choose specialization and apply it
        specialization = random.choice(possible_specializations)
        agent.resource_specialization = specialization
        
        # Give bonus to related resource generation
        self._apply_specialization_bonus(agent, specialization)
        
        return specialization

    def _apply_specialization_bonus(self, agent: Any, specialization: str) -> None:
        """Apply bonuses to agent based on their specialization."""
        self.initialize_agent_resources(agent)
        
        specialization_bonuses = {
            "food_production": {"food": 0.3},
            "shelter_building": {"shelter": 0.4, "materials": 0.2},
            "tool_crafting": {"tools": 0.4, "materials": 0.1},
            "knowledge_gathering": {"knowledge": 0.3},
            "resource_sharing": {},  # Social bonus handled elsewhere
            "innovation": {"knowledge": 0.2, "tools": 0.2},
            "resource_management": {"materials": 0.2},
            "healing": {"knowledge": 0.1}
        }
        
        bonuses = specialization_bonuses.get(specialization, {})
        for resource_type, bonus in bonuses.items():
            if resource_type in agent.personal_resources:
                agent.personal_resources[resource_type] = min(1.0, 
                    agent.personal_resources[resource_type] + bonus)

    def update_market_prices(self, world_resources: Dict[str, float]) -> None:
        """Update market prices based on resource scarcity."""
        for resource_type, world_level in world_resources.items():
            if resource_type in self.market_prices:
                # Price inversely related to availability
                if world_level < 0.3:
                    self.market_prices[resource_type] *= 1.2  # Price increase
                elif world_level > 0.8:
                    self.market_prices[resource_type] *= 0.95  # Price decrease
                
                # Keep prices within reasonable bounds
                self.market_prices[resource_type] = max(0.5, min(3.0, 
                    self.market_prices[resource_type]))

    def process_daily_resources(self, agents: List[Any], world_resources: Dict[str, float], 
                              world_day: int) -> List[Dict[str, Any]]:
        """Process all daily resource activities."""
        resource_events = []
        alive_agents = [a for a in agents if a.is_alive]
        
        # 1. Process resource consumption for all agents
        for agent in alive_agents:
            self.process_resource_consumption(agent, world_day)
        
        # 2. Update market prices
        self.update_market_prices(world_resources)
        
        # 3. Generate specializations for agents
        for agent in alive_agents:
            specialization = self.generate_resource_specialization(agent, world_day)
            if specialization:
                resource_events.append({
                    "type": "specialization",
                    "agent": agent.name,
                    "specialization": specialization,
                    "day": world_day
                })
        
        # 4. Attempt trades between agents
        for i, agent1 in enumerate(alive_agents):
            for agent2 in alive_agents[i+1:]:
                if agent1.location == agent2.location and random.random() < 0.15:
                    trade = self.attempt_resource_trade(agent1, agent2, world_day)
                    if trade:
                        self.transactions.append(trade)
                        resource_events.append({
                            "type": "trade",
                            "participants": [agent1.name, agent2.name],
                            "resource": trade.resource_type,
                            "amount": trade.amount,
                            "day": world_day
                        })
        
        return resource_events

    def get_resource_summary(self) -> Dict[str, Any]:
        """Get summary of current resource system state."""
        return {
            "total_transactions": len(self.transactions),
            "recent_trades": len([t for t in self.transactions[-10:]]),
            "market_prices": self.market_prices.copy(),
            "active_specialists": len(self.resource_specialists)
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize resource system state."""
        return {
            "transactions": [
                {
                    "day": t.day,
                    "giver": t.giver,
                    "receiver": t.receiver,
                    "resource_type": t.resource_type,
                    "amount": t.amount,
                    "trade_value": t.trade_value,
                    "reason": t.reason
                } for t in self.transactions
            ],
            "market_prices": self.market_prices,
            "resource_specialists": self.resource_specialists
        } 