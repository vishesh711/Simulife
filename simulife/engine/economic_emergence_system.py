"""
Economic Emergence System for SimuLife
Creates complex economic patterns, markets, trade networks, and financial institutions
that emerge naturally from agent trading behaviors and specialization.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict
import math


class MarketType(Enum):
    """Types of markets that can emerge."""
    INFORMAL_TRADING = "informal_trading"       # Casual agent-to-agent trades
    LOCAL_MARKET = "local_market"               # Organized local marketplace
    SPECIALIZED_MARKET = "specialized_market"   # Markets for specific goods/services
    REGIONAL_HUB = "regional_hub"               # Major trading center
    FINANCIAL_CENTER = "financial_center"       # Banking and investment center


class CurrencyType(Enum):
    """Types of currency systems."""
    BARTER = "barter"                           # Direct goods exchange
    COMMODITY_MONEY = "commodity_money"         # Valuable items as currency
    TOKEN_CURRENCY = "token_currency"           # Standardized tokens
    CREDIT_SYSTEM = "credit_system"             # Debt-based transactions
    MIXED_ECONOMY = "mixed_economy"             # Multiple systems coexist


class EconomicRole(Enum):
    """Specialized economic roles that emerge."""
    PRODUCER = "producer"                       # Creates goods/services
    TRADER = "trader"                           # Facilitates exchange
    BANKER = "banker"                           # Manages currency/credit
    REGULATOR = "regulator"                     # Oversees market fairness
    INVESTOR = "investor"                       # Provides capital
    CONSUMER = "consumer"                       # End user of goods/services


class TradeGoodCategory(Enum):
    """Categories of tradeable goods."""
    FOOD = "food"                              # Consumable sustenance
    MATERIALS = "materials"                     # Raw building/crafting materials
    TOOLS = "tools"                            # Functional implements
    CRAFTS = "crafts"                          # Artisan-made items
    SERVICES = "services"                      # Labor and expertise
    LUXURY = "luxury"                          # Non-essential valuable items
    KNOWLEDGE = "knowledge"                    # Information and skills
    SPIRITUAL = "spiritual"                    # Religious/ceremonial items


@dataclass
class TradeGood:
    """Represents a tradeable good or service."""
    id: str
    name: str
    category: TradeGoodCategory
    base_value: float                          # Intrinsic value
    current_price: float                       # Market price
    supply: float                              # Available quantity
    demand: float                              # Market demand
    production_difficulty: float               # How hard to produce (0.0-1.0)
    perishability: float                      # How quickly it degrades (0.0-1.0)
    transportability: float                    # How easy to move (0.0-1.0)
    seasonality: Dict[str, float]             # Season-based value modifiers
    producers: Set[str]                        # Agents who can produce this
    primary_locations: Set[str]                # Where it's commonly found


@dataclass
class MarketPlace:
    """Represents an emergent marketplace."""
    id: str
    name: str
    market_type: MarketType
    location: str
    established_day: int
    
    # Market characteristics
    goods_traded: Set[str]                     # Trade good IDs
    regular_traders: Set[str]                  # Agent names
    daily_volume: float                        # Average daily trade value
    specializations: List[TradeGoodCategory]   # Market specialties
    
    # Market structure
    currency_systems: List[CurrencyType]       # Accepted currencies
    price_index: Dict[str, float]             # Price history
    trade_regulations: List[str]               # Market rules
    market_makers: Set[str]                    # Agents who facilitate trades
    
    # Market dynamics
    competition_level: float                   # 0.0-1.0 market competition
    trust_level: float                         # 0.0-1.0 market trust
    transaction_costs: float                   # Cost to trade (0.0-1.0)
    market_efficiency: float                   # How well prices reflect value
    
    # Economic networks
    connected_markets: Set[str]                # Other connected markets
    trade_routes: Dict[str, Dict[str, Any]]    # Routes to other markets
    supply_chains: Dict[str, List[str]]        # Goods production chains


@dataclass
class TradeRoute:
    """Represents a trade route between locations."""
    id: str
    origin: str
    destination: str
    established_day: int
    
    # Route characteristics
    distance_difficulty: float                # Travel difficulty (0.0-1.0)
    goods_flow: Dict[str, float]              # Goods traded along route
    regular_traders: Set[str]                 # Agents who use this route
    
    # Route economics
    transport_costs: float                     # Cost to use route
    travel_time: int                          # Days to complete journey
    safety_level: float                       # Route security (0.0-1.0)
    profitability: float                      # Route profitability
    
    # Route infrastructure
    infrastructure_level: float               # Road quality, waypoints, etc.
    services_available: List[str]             # Support services along route


@dataclass
class EconomicAgent:
    """Represents an agent's economic behavior and status."""
    agent_name: str
    economic_role: EconomicRole
    specializations: List[TradeGoodCategory]
    
    # Economic status
    wealth_level: float                       # 0.0-1.0 relative wealth
    credit_rating: float                      # 0.0-1.0 creditworthiness
    trade_reputation: float                   # 0.0-1.0 trading reputation
    
    # Economic relationships
    trading_partners: Set[str]                # Regular trade partners
    debtors: Dict[str, float]                 # Money owed to this agent
    creditors: Dict[str, float]               # Money this agent owes
    
    # Economic activities
    production_capacity: Dict[str, float]     # Goods this agent can produce
    consumption_needs: Dict[str, float]       # Goods this agent needs
    trade_history: List[Dict[str, Any]]       # Recent trading activity
    
    # Market participation
    preferred_markets: Set[str]               # Markets agent frequents
    market_influence: Dict[str, float]        # Influence in different markets


class EconomicEmergenceSystem:
    """
    Manages the emergence of complex economic systems from simple trading behaviors.
    """
    
    def __init__(self):
        self.trade_goods: Dict[str, TradeGood] = {}
        self.marketplaces: Dict[str, MarketPlace] = {}
        self.trade_routes: Dict[str, TradeRoute] = {}
        self.economic_agents: Dict[str, EconomicAgent] = {}
        
        # Economic tracking
        self.trade_history: List[Dict[str, Any]] = []
        self.price_history: Dict[str, List[Tuple[int, float]]] = defaultdict(list)
        self.economic_events: List[Dict[str, Any]] = []
        
        # System configuration
        self.market_formation_thresholds = self._initialize_market_thresholds()
        self.currency_evolution_stages = self._initialize_currency_stages()
        self.economic_cycles = self._initialize_economic_cycles()
        
        # Initialize base trade goods
        self._initialize_trade_goods()
    
    def _initialize_trade_goods(self) -> None:
        """Initialize the base catalog of tradeable goods."""
        base_goods = [
            # Food
            TradeGood(
                id="food_basic", name="Basic Food", category=TradeGoodCategory.FOOD,
                base_value=1.0, current_price=1.0, supply=1.0, demand=1.0,
                production_difficulty=0.3, perishability=0.8, transportability=0.6,
                seasonality={"spring": 1.2, "summer": 1.0, "autumn": 0.8, "winter": 1.3},
                producers=set(), primary_locations={"fields", "forest"}
            ),
            TradeGood(
                id="food_preserved", name="Preserved Food", category=TradeGoodCategory.FOOD,
                base_value=1.5, current_price=1.5, supply=0.6, demand=0.8,
                production_difficulty=0.6, perishability=0.2, transportability=0.9,
                seasonality={"spring": 0.8, "summer": 0.9, "autumn": 1.2, "winter": 1.5},
                producers=set(), primary_locations={"village_center"}
            ),
            
            # Materials
            TradeGood(
                id="wood", name="Wood", category=TradeGoodCategory.MATERIALS,
                base_value=0.8, current_price=0.8, supply=1.2, demand=0.9,
                production_difficulty=0.4, perishability=0.1, transportability=0.4,
                seasonality={"spring": 1.1, "summer": 1.0, "autumn": 1.2, "winter": 0.8},
                producers=set(), primary_locations={"forest"}
            ),
            TradeGood(
                id="stone", name="Stone", category=TradeGoodCategory.MATERIALS,
                base_value=0.6, current_price=0.6, supply=1.0, demand=0.7,
                production_difficulty=0.7, perishability=0.0, transportability=0.2,
                seasonality={"spring": 1.0, "summer": 1.0, "autumn": 1.0, "winter": 1.0},
                producers=set(), primary_locations={"mountains", "hills"}
            ),
            
            # Tools
            TradeGood(
                id="simple_tools", name="Simple Tools", category=TradeGoodCategory.TOOLS,
                base_value=2.0, current_price=2.0, supply=0.5, demand=0.8,
                production_difficulty=0.7, perishability=0.1, transportability=0.8,
                seasonality={"spring": 1.0, "summer": 1.0, "autumn": 1.0, "winter": 1.0},
                producers=set(), primary_locations={"village_center"}
            ),
            
            # Crafts
            TradeGood(
                id="pottery", name="Pottery", category=TradeGoodCategory.CRAFTS,
                base_value=1.5, current_price=1.5, supply=0.4, demand=0.6,
                production_difficulty=0.8, perishability=0.0, transportability=0.6,
                seasonality={"spring": 1.0, "summer": 1.0, "autumn": 1.0, "winter": 1.0},
                producers=set(), primary_locations={"village_center"}
            ),
            
            # Services
            TradeGood(
                id="healing", name="Healing Services", category=TradeGoodCategory.SERVICES,
                base_value=3.0, current_price=3.0, supply=0.3, demand=0.7,
                production_difficulty=0.9, perishability=1.0, transportability=1.0,
                seasonality={"spring": 1.0, "summer": 0.8, "autumn": 1.1, "winter": 1.3},
                producers=set(), primary_locations=set()
            ),
            
            # Knowledge
            TradeGood(
                id="skills_training", name="Skills Training", category=TradeGoodCategory.KNOWLEDGE,
                base_value=2.5, current_price=2.5, supply=0.2, demand=0.5,
                production_difficulty=0.9, perishability=0.0, transportability=1.0,
                seasonality={"spring": 1.0, "summer": 1.0, "autumn": 1.0, "winter": 1.2},
                producers=set(), primary_locations=set()
            ),
            
            # Luxury
            TradeGood(
                id="decorative_items", name="Decorative Items", category=TradeGoodCategory.LUXURY,
                base_value=4.0, current_price=4.0, supply=0.1, demand=0.3,
                production_difficulty=0.9, perishability=0.0, transportability=0.8,
                seasonality={"spring": 1.0, "summer": 1.0, "autumn": 1.0, "winter": 1.0},
                producers=set(), primary_locations=set()
            )
        ]
        
        for good in base_goods:
            self.trade_goods[good.id] = good
    
    def _initialize_market_thresholds(self) -> Dict[str, Dict[str, Any]]:
        """Initialize thresholds for market formation."""
        return {
            "local_market": {
                "min_traders": 4,
                "min_trade_volume": 10,
                "min_good_variety": 3,
                "min_population": 8
            },
            "specialized_market": {
                "min_traders": 3,
                "min_trade_volume": 15,
                "specialization_ratio": 0.7,  # 70% of trades in one category
                "min_population": 6
            },
            "regional_hub": {
                "min_traders": 8,
                "min_trade_volume": 50,
                "min_connected_locations": 3,
                "min_population": 20
            },
            "financial_center": {
                "min_traders": 6,
                "min_trade_volume": 30,
                "min_credit_activity": 10,
                "min_population": 15
            }
        }
    
    def _initialize_currency_stages(self) -> List[Dict[str, Any]]:
        """Initialize currency evolution stages."""
        return [
            {
                "stage": CurrencyType.BARTER,
                "requirements": {"trade_volume": 0},
                "description": "Direct exchange of goods and services"
            },
            {
                "stage": CurrencyType.COMMODITY_MONEY,
                "requirements": {"trade_volume": 20, "trade_complexity": 0.3},
                "description": "Valuable items used as medium of exchange"
            },
            {
                "stage": CurrencyType.TOKEN_CURRENCY,
                "requirements": {"trade_volume": 50, "market_trust": 0.6, "institutions": 1},
                "description": "Standardized tokens representing value"
            },
            {
                "stage": CurrencyType.CREDIT_SYSTEM,
                "requirements": {"trade_volume": 100, "market_trust": 0.8, "financial_institutions": 1},
                "description": "Debt-based transactions and credit"
            }
        ]
    
    def _initialize_economic_cycles(self) -> Dict[str, Dict[str, Any]]:
        """Initialize economic cycle patterns."""
        return {
            "seasonal": {
                "period": 365,  # One year
                "amplitude": 0.2,  # 20% price variation
                "affected_categories": [TradeGoodCategory.FOOD, TradeGoodCategory.MATERIALS]
            },
            "boom_bust": {
                "period": 1095,  # Three years
                "amplitude": 0.4,  # 40% price variation
                "triggers": ["resource_discovery", "population_growth", "technological_advancement"]
            },
            "supply_shock": {
                "period": "random",
                "amplitude": 0.6,  # 60% price variation
                "triggers": ["natural_disaster", "conflict", "resource_depletion"]
            }
        }
    
    def process_daily_economic_emergence(self, agents: List[Any], groups: Dict[str, Any],
                                       world_state: Any, current_day: int) -> List[Dict[str, Any]]:
        """Process daily economic emergence activities."""
        events = []
        
        # Step 1: Update economic agent profiles
        self._update_economic_agents(agents, current_day)
        
        # Step 2: Process natural trading activities
        trading_events = self._process_natural_trading(agents, current_day)
        events.extend(trading_events)
        
        # Step 3: Update trade good supply, demand, and prices
        market_events = self._update_market_dynamics(agents, current_day)
        events.extend(market_events)
        
        # Step 4: Check for marketplace formation
        marketplace_events = self._check_marketplace_formation(agents, current_day)
        events.extend(marketplace_events)
        
        # Step 5: Develop trade routes
        route_events = self._develop_trade_routes(agents, current_day)
        events.extend(route_events)
        
        # Step 6: Evolve currency systems
        currency_events = self._evolve_currency_systems(current_day)
        events.extend(currency_events)
        
        # Step 7: Apply economic cycles and trends
        cycle_events = self._apply_economic_cycles(current_day)
        events.extend(cycle_events)
        
        # Step 8: Detect economic emergent phenomena
        emergence_events = self._detect_economic_emergence(agents, current_day)
        events.extend(emergence_events)
        
        return events
    
    def _update_economic_agents(self, agents: List[Any], current_day: int) -> None:
        """Update economic profiles for all agents."""
        for agent in agents:
            if not agent.is_alive:
                continue
            
            # Create or update economic agent profile
            if agent.name not in self.economic_agents:
                self.economic_agents[agent.name] = self._create_economic_agent_profile(agent)
            else:
                self._update_economic_agent_profile(agent, current_day)
    
    def _create_economic_agent_profile(self, agent: Any) -> EconomicAgent:
        """Create economic profile for a new agent."""
        # Determine economic role based on specialization and traits
        economic_role = self._determine_economic_role(agent)
        
        # Determine specializations based on skills and location
        specializations = self._determine_trade_specializations(agent)
        
        # Initial economic status
        wealth_level = random.uniform(0.3, 0.7)  # Start with moderate wealth
        
        return EconomicAgent(
            agent_name=agent.name,
            economic_role=economic_role,
            specializations=specializations,
            wealth_level=wealth_level,
            credit_rating=0.5,  # Neutral credit
            trade_reputation=0.5,  # Neutral reputation
            trading_partners=set(),
            debtors={},
            creditors={},
            production_capacity={},
            consumption_needs={},
            trade_history=[],
            preferred_markets=set(),
            market_influence={}
        )
    
    def _determine_economic_role(self, agent: Any) -> EconomicRole:
        """Determine an agent's primary economic role."""
        if hasattr(agent, 'specialization'):
            if agent.specialization == "merchant":
                return EconomicRole.TRADER
            elif agent.specialization == "artisan":
                return EconomicRole.PRODUCER
            elif agent.specialization == "leader":
                return random.choices([EconomicRole.REGULATOR, EconomicRole.INVESTOR],
                                    weights=[0.7, 0.3])[0]
        
        # Default role based on traits and skills
        if hasattr(agent, 'traits'):
            if "entrepreneurial" in agent.traits or "ambitious" in agent.traits:
                return EconomicRole.TRADER
            elif "creative" in agent.traits or "skilled" in agent.traits:
                return EconomicRole.PRODUCER
        
        return EconomicRole.CONSUMER  # Default role
    
    def _determine_trade_specializations(self, agent: Any) -> List[TradeGoodCategory]:
        """Determine what trade good categories an agent specializes in."""
        specializations = []
        
        # Based on location
        if hasattr(agent, 'location'):
            if agent.location == "forest":
                specializations.append(TradeGoodCategory.MATERIALS)  # Wood
            elif agent.location == "fields":
                specializations.append(TradeGoodCategory.FOOD)
            elif agent.location == "mountains":
                specializations.append(TradeGoodCategory.MATERIALS)  # Stone
        
        # Based on skills and specialization
        if hasattr(agent, 'specialization'):
            if agent.specialization == "artisan":
                specializations.extend([TradeGoodCategory.CRAFTS, TradeGoodCategory.TOOLS])
            elif agent.specialization == "healer":
                specializations.append(TradeGoodCategory.SERVICES)
            elif agent.specialization == "scholar":
                specializations.extend([TradeGoodCategory.KNOWLEDGE, TradeGoodCategory.SERVICES])
            elif agent.specialization == "mystic":
                specializations.append(TradeGoodCategory.SPIRITUAL)
        
        # Based on traits
        if hasattr(agent, 'traits'):
            if "creative" in agent.traits:
                specializations.append(TradeGoodCategory.CRAFTS)
            if "spiritual" in agent.traits:
                specializations.append(TradeGoodCategory.SPIRITUAL)
        
        # Ensure at least one specialization
        if not specializations:
            specializations.append(TradeGoodCategory.FOOD)  # Everyone needs/can trade food
        
        # Remove duplicates and limit to 3
        return list(set(specializations))[:3]
    
    def _update_economic_agent_profile(self, agent: Any, current_day: int) -> None:
        """Update existing economic agent profile."""
        econ_agent = self.economic_agents[agent.name]
        
        # Update wealth based on recent activities
        # This would integrate with resource system to track actual wealth
        
        # Update production capacity based on skills
        self._update_production_capacity(agent, econ_agent)
        
        # Update consumption needs based on agent status
        self._update_consumption_needs(agent, econ_agent)
        
        # Decay unused relationships and update active ones
        self._update_trading_relationships(econ_agent, current_day)
    
    def _update_production_capacity(self, agent: Any, econ_agent: EconomicAgent) -> None:
        """Update what goods an agent can produce and in what quantities."""
        econ_agent.production_capacity.clear()
        
        for specialization in econ_agent.specializations:
            for good_id, good in self.trade_goods.items():
                if good.category == specialization:
                    # Production capacity based on skills and specialization
                    base_capacity = 1.0
                    
                    if hasattr(agent, 'specialization') and agent.specialization:
                        if specialization.value in agent.specialization:
                            base_capacity *= 1.5
                    
                    # Skill modifiers
                    if hasattr(agent, 'skills'):
                        relevant_skills = self._get_relevant_skills_for_good(good)
                        for skill in relevant_skills:
                            if skill in agent.skills:
                                skill_value = agent.skills[skill]
                                if isinstance(skill_value, float):
                                    base_capacity *= (1.0 + skill_value * 0.5)
                    
                    # Health and energy modifiers
                    if hasattr(agent, 'health'):
                        base_capacity *= agent.health
                    if hasattr(agent, 'energy'):
                        base_capacity *= (0.5 + agent.energy * 0.5)
                    
                    econ_agent.production_capacity[good_id] = base_capacity
    
    def _get_relevant_skills_for_good(self, good: TradeGood) -> List[str]:
        """Get skills relevant to producing a trade good."""
        skill_mapping = {
            TradeGoodCategory.FOOD: ["foraging", "survival"],
            TradeGoodCategory.MATERIALS: ["survival", "construction"],
            TradeGoodCategory.TOOLS: ["toolmaking", "crafting"],
            TradeGoodCategory.CRAFTS: ["artistry", "crafting"],
            TradeGoodCategory.SERVICES: ["social", "medicine"],
            TradeGoodCategory.KNOWLEDGE: ["teaching", "research"],
            TradeGoodCategory.SPIRITUAL: ["spirituality", "social"],
            TradeGoodCategory.LUXURY: ["artistry", "crafting"]
        }
        return skill_mapping.get(good.category, [])
    
    def _update_consumption_needs(self, agent: Any, econ_agent: EconomicAgent) -> None:
        """Update what goods an agent needs to consume."""
        econ_agent.consumption_needs.clear()
        
        # Basic needs
        econ_agent.consumption_needs["food_basic"] = 1.0
        
        # Needs based on role and activities
        if econ_agent.economic_role == EconomicRole.PRODUCER:
            econ_agent.consumption_needs["simple_tools"] = 0.5
            econ_agent.consumption_needs["wood"] = 0.3
        elif econ_agent.economic_role == EconomicRole.TRADER:
            econ_agent.consumption_needs["food_preserved"] = 0.7
        
        # Luxury consumption based on wealth
        if econ_agent.wealth_level > 0.7:
            econ_agent.consumption_needs["decorative_items"] = 0.3
            econ_agent.consumption_needs["pottery"] = 0.2
        
        # Social status consumption
        if hasattr(agent, 'reputation') and agent.reputation > 0.7:
            econ_agent.consumption_needs["decorative_items"] = econ_agent.consumption_needs.get("decorative_items", 0) + 0.2
    
    def _update_trading_relationships(self, econ_agent: EconomicAgent, current_day: int) -> None:
        """Update trading relationships based on recent activity."""
        # This would track and update based on actual trade events
        # For now, simulate natural relationship evolution
        
        # Occasionally remove inactive partnerships
        if random.random() < 0.05:  # 5% chance
            if econ_agent.trading_partners:
                inactive_partner = random.choice(list(econ_agent.trading_partners))
                econ_agent.trading_partners.discard(inactive_partner)
    
    def _process_natural_trading(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process natural trading activities between agents."""
        events = []
        
        # Find potential trading pairs
        for i, agent1 in enumerate(agents):
            if not agent1.is_alive:
                continue
                
            econ_agent1 = self.economic_agents.get(agent1.name)
            if not econ_agent1:
                continue
            
            # Check for trading opportunities with other agents
            for agent2 in agents[i+1:]:
                if not agent2.is_alive or agent1.location != agent2.location:
                    continue
                
                econ_agent2 = self.economic_agents.get(agent2.name)
                if not econ_agent2:
                    continue
                
                # Check if they should trade
                trade_probability = self._calculate_trade_probability(agent1, agent2, econ_agent1, econ_agent2)
                
                if random.random() < trade_probability:
                    trade_event = self._execute_trade(agent1, agent2, econ_agent1, econ_agent2, current_day)
                    if trade_event:
                        events.append(trade_event)
        
        return events
    
    def _calculate_trade_probability(self, agent1: Any, agent2: Any, 
                                   econ_agent1: EconomicAgent, econ_agent2: EconomicAgent) -> float:
        """Calculate probability that two agents will trade."""
        base_probability = 0.1  # 10% base chance
        
        # Increase if they have complementary needs/production
        complementarity = self._calculate_trade_complementarity(econ_agent1, econ_agent2)
        base_probability += complementarity * 0.3
        
        # Increase based on relationship
        if hasattr(agent1, 'relationships') and agent2.name in agent1.relationships:
            relationship = agent1.relationships[agent2.name]
            if relationship in ["friend", "family"]:
                base_probability += 0.2
            elif relationship in ["ally", "partner"]:
                base_probability += 0.15
        
        # Increase if they're regular trading partners
        if agent2.name in econ_agent1.trading_partners:
            base_probability += 0.25
        
        # Merchant specialists trade more frequently
        if (econ_agent1.economic_role == EconomicRole.TRADER or 
            econ_agent2.economic_role == EconomicRole.TRADER):
            base_probability += 0.15
        
        # Reduce if recent trade (avoid over-trading)
        recent_trades = len([t for t in econ_agent1.trade_history[-5:] 
                           if t.get("partner") == agent2.name])
        if recent_trades > 0:
            base_probability *= (0.5 ** recent_trades)
        
        return min(base_probability, 0.8)  # Cap at 80%
    
    def _calculate_trade_complementarity(self, econ_agent1: EconomicAgent, 
                                       econ_agent2: EconomicAgent) -> float:
        """Calculate how complementary two agents' production and needs are."""
        complementarity = 0.0
        
        # Check if agent1 can produce what agent2 needs
        for good_id, need_amount in econ_agent2.consumption_needs.items():
            production_amount = econ_agent1.production_capacity.get(good_id, 0)
            if production_amount > 0:
                complementarity += min(need_amount, production_amount) * 0.5
        
        # Check if agent2 can produce what agent1 needs
        for good_id, need_amount in econ_agent1.consumption_needs.items():
            production_amount = econ_agent2.production_capacity.get(good_id, 0)
            if production_amount > 0:
                complementarity += min(need_amount, production_amount) * 0.5
        
        # Check for specialization complementarity
        agent1_categories = set(econ_agent1.specializations)
        agent2_categories = set(econ_agent2.specializations)
        
        if agent1_categories != agent2_categories:  # Different specializations
            complementarity += 0.3
        
        return min(complementarity, 1.0)
    
    def _execute_trade(self, agent1: Any, agent2: Any, econ_agent1: EconomicAgent, 
                      econ_agent2: EconomicAgent, current_day: int) -> Optional[Dict[str, Any]]:
        """Execute a trade between two agents."""
        # Find what goods to trade
        trade_goods = self._determine_trade_goods(econ_agent1, econ_agent2)
        
        if not trade_goods:
            return None
        
        # Calculate trade value and fairness
        trade_value = self._calculate_trade_value(trade_goods)
        fairness = self._calculate_trade_fairness(trade_goods, econ_agent1, econ_agent2)
        
        # Execute the trade
        success = self._perform_trade_exchange(agent1, agent2, econ_agent1, econ_agent2, trade_goods)
        
        if success:
            # Record trade in history
            trade_record = {
                "partner": agent2.name,
                "goods_given": trade_goods["agent1_gives"],
                "goods_received": trade_goods["agent2_gives"],
                "value": trade_value,
                "fairness": fairness,
                "day": current_day
            }
            
            econ_agent1.trade_history.append(trade_record)
            econ_agent2.trade_history.append({
                "partner": agent1.name,
                "goods_given": trade_goods["agent2_gives"],
                "goods_received": trade_goods["agent1_gives"],
                "value": trade_value,
                "fairness": fairness,
                "day": current_day
            })
            
            # Update trading relationships
            econ_agent1.trading_partners.add(agent2.name)
            econ_agent2.trading_partners.add(agent1.name)
            
            # Update trade reputation
            if fairness > 0.7:
                econ_agent1.trade_reputation = min(1.0, econ_agent1.trade_reputation + 0.02)
                econ_agent2.trade_reputation = min(1.0, econ_agent2.trade_reputation + 0.02)
            elif fairness < 0.3:
                econ_agent1.trade_reputation = max(0.0, econ_agent1.trade_reputation - 0.05)
                econ_agent2.trade_reputation = max(0.0, econ_agent2.trade_reputation - 0.05)
            
            # Add memories
            agent1.memory.store_memory(
                f"Traded {', '.join(trade_goods['agent1_gives'])} with {agent2.name} for {', '.join(trade_goods['agent2_gives'])}",
                importance=0.5,
                memory_type="economic"
            )
            
            agent2.memory.store_memory(
                f"Traded {', '.join(trade_goods['agent2_gives'])} with {agent1.name} for {', '.join(trade_goods['agent1_gives'])}",
                importance=0.5,
                memory_type="economic"
            )
            
            # Update global trade tracking
            self.trade_history.append({
                "day": current_day,
                "participants": [agent1.name, agent2.name],
                "location": agent1.location,
                "goods": trade_goods,
                "value": trade_value,
                "fairness": fairness
            })
            
            return {
                "type": "natural_trade",
                "participants": [agent1.name, agent2.name],
                "location": agent1.location,
                "goods_exchanged": trade_goods,
                "trade_value": trade_value,
                "fairness": fairness,
                "day": current_day
            }
        
        return None
    
    def _determine_trade_goods(self, econ_agent1: EconomicAgent, 
                             econ_agent2: EconomicAgent) -> Optional[Dict[str, List[str]]]:
        """Determine what goods should be traded between agents."""
        agent1_gives = []
        agent2_gives = []
        
        # Find goods agent1 can give that agent2 needs
        for good_id, need_amount in econ_agent2.consumption_needs.items():
            production_amount = econ_agent1.production_capacity.get(good_id, 0)
            if production_amount >= need_amount * 0.5:  # Can satisfy at least half the need
                agent1_gives.append(good_id)
                if len(agent1_gives) >= 2:  # Limit trade complexity
                    break
        
        # Find goods agent2 can give that agent1 needs
        for good_id, need_amount in econ_agent1.consumption_needs.items():
            production_amount = econ_agent2.production_capacity.get(good_id, 0)
            if production_amount >= need_amount * 0.5:
                agent2_gives.append(good_id)
                if len(agent2_gives) >= 2:
                    break
        
        # Must have something to trade from both sides
        if not agent1_gives or not agent2_gives:
            return None
        
        return {
            "agent1_gives": agent1_gives,
            "agent2_gives": agent2_gives
        }
    
    def _calculate_trade_value(self, trade_goods: Dict[str, List[str]]) -> float:
        """Calculate the total value of a trade."""
        total_value = 0.0
        
        for good_id in trade_goods["agent1_gives"] + trade_goods["agent2_gives"]:
            if good_id in self.trade_goods:
                total_value += self.trade_goods[good_id].current_price
        
        return total_value
    
    def _calculate_trade_fairness(self, trade_goods: Dict[str, List[str]], 
                                econ_agent1: EconomicAgent, econ_agent2: EconomicAgent) -> float:
        """Calculate how fair a trade is (0.0 = very unfair, 1.0 = perfectly fair)."""
        agent1_value = sum(self.trade_goods[good_id].current_price 
                          for good_id in trade_goods["agent1_gives"] 
                          if good_id in self.trade_goods)
        
        agent2_value = sum(self.trade_goods[good_id].current_price 
                          for good_id in trade_goods["agent2_gives"] 
                          if good_id in self.trade_goods)
        
        if agent1_value + agent2_value == 0:
            return 1.0  # No trade value, assume fair
        
        # Calculate fairness as 1 - (value difference / total value)
        value_difference = abs(agent1_value - agent2_value)
        total_value = agent1_value + agent2_value
        
        fairness = 1.0 - (value_difference / total_value)
        
        # Adjust for reputation differences
        rep_difference = abs(econ_agent1.trade_reputation - econ_agent2.trade_reputation)
        fairness *= (1.0 - rep_difference * 0.2)
        
        return max(0.0, min(1.0, fairness))
    
    def _perform_trade_exchange(self, agent1: Any, agent2: Any, econ_agent1: EconomicAgent, 
                              econ_agent2: EconomicAgent, trade_goods: Dict[str, List[str]]) -> bool:
        """Perform the actual exchange of goods in a trade."""
        # This would integrate with the actual resource system
        # For now, assume successful exchange and update economic tracking
        
        # Update wealth levels based on trade
        trade_value = self._calculate_trade_value(trade_goods)
        
        # Traders gain wealth from facilitating trades
        if econ_agent1.economic_role == EconomicRole.TRADER:
            econ_agent1.wealth_level = min(1.0, econ_agent1.wealth_level + trade_value * 0.05)
        if econ_agent2.economic_role == EconomicRole.TRADER:
            econ_agent2.wealth_level = min(1.0, econ_agent2.wealth_level + trade_value * 0.05)
        
        return True  # Assume successful trade
    
    def _update_market_dynamics(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Update supply, demand, and prices for all trade goods."""
        events = []
        
        for good_id, good in self.trade_goods.items():
            # Calculate new supply and demand
            new_supply = self._calculate_good_supply(good, agents)
            new_demand = self._calculate_good_demand(good, agents)
            
            # Update supply and demand
            old_supply = good.supply
            old_demand = good.demand
            
            good.supply = (good.supply * 0.7) + (new_supply * 0.3)  # Smooth changes
            good.demand = (good.demand * 0.7) + (new_demand * 0.3)
            
            # Calculate new price based on supply and demand
            old_price = good.current_price
            new_price = self._calculate_market_price(good, current_day)
            good.current_price = new_price
            
            # Record price history
            self.price_history[good_id].append((current_day, new_price))
            
            # Keep only recent price history
            if len(self.price_history[good_id]) > 100:
                self.price_history[good_id] = self.price_history[good_id][-100:]
            
            # Report significant market changes
            price_change = abs(new_price - old_price) / old_price if old_price > 0 else 0
            supply_change = abs(new_supply - old_supply) / old_supply if old_supply > 0 else 0
            demand_change = abs(new_demand - old_demand) / old_demand if old_demand > 0 else 0
            
            if price_change > 0.2 or supply_change > 0.3 or demand_change > 0.3:
                events.append({
                    "type": "market_dynamics_change",
                    "good": good.name,
                    "price_change": price_change,
                    "new_price": new_price,
                    "supply_change": supply_change,
                    "demand_change": demand_change,
                    "day": current_day
                })
        
        return events
    
    def _calculate_good_supply(self, good: TradeGood, agents: List[Any]) -> float:
        """Calculate current supply of a trade good."""
        total_supply = 0.0
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            econ_agent = self.economic_agents.get(agent.name)
            if econ_agent:
                production_capacity = econ_agent.production_capacity.get(good.id, 0)
                total_supply += production_capacity
        
        # Add base environmental supply for location-based goods
        if good.primary_locations:
            environmental_supply = len(good.primary_locations) * 0.2
            total_supply += environmental_supply
        
        # Apply seasonal modifiers
        current_season = self._get_current_season()  # Would get from world state
        seasonal_modifier = good.seasonality.get(current_season, 1.0)
        total_supply *= seasonal_modifier
        
        return max(0.1, total_supply)  # Minimum supply to prevent zero
    
    def _calculate_good_demand(self, good: TradeGood, agents: List[Any]) -> float:
        """Calculate current demand for a trade good."""
        total_demand = 0.0
        
        for agent in agents:
            if not agent.is_alive:
                continue
            
            econ_agent = self.economic_agents.get(agent.name)
            if econ_agent:
                consumption_need = econ_agent.consumption_needs.get(good.id, 0)
                total_demand += consumption_need
        
        # Add base demand for essential goods
        if good.category == TradeGoodCategory.FOOD:
            total_demand += len([a for a in agents if a.is_alive]) * 0.8
        
        # Luxury goods have demand based on wealth distribution
        if good.category == TradeGoodCategory.LUXURY:
            wealthy_agents = len([a for a in agents if a.is_alive and 
                                self.economic_agents.get(a.name) and 
                                self.economic_agents[a.name].wealth_level > 0.7])
            total_demand += wealthy_agents * 0.3
        
        return max(0.1, total_demand)
    
    def _calculate_market_price(self, good: TradeGood, current_day: int) -> float:
        """Calculate market price based on supply and demand."""
        # Basic supply and demand pricing
        if good.supply > 0:
            price_ratio = good.demand / good.supply
        else:
            price_ratio = 2.0  # High price if no supply
        
        # Apply to base value
        new_price = good.base_value * price_ratio
        
        # Apply production difficulty modifier
        difficulty_modifier = 1.0 + good.production_difficulty * 0.5
        new_price *= difficulty_modifier
        
        # Apply transportability modifier (harder to transport = higher price)
        transport_modifier = 1.0 + (1.0 - good.transportability) * 0.3
        new_price *= transport_modifier
        
        # Smooth price changes to avoid volatility
        if hasattr(good, 'current_price') and good.current_price > 0:
            max_change = 0.3  # Maximum 30% price change per day
            price_change = (new_price - good.current_price) / good.current_price
            if abs(price_change) > max_change:
                if price_change > 0:
                    new_price = good.current_price * (1 + max_change)
                else:
                    new_price = good.current_price * (1 - max_change)
        
        return max(0.1, new_price)  # Minimum price
    
    def _get_current_season(self) -> str:
        """Get current season - would integrate with world state."""
        seasons = ["spring", "summer", "autumn", "winter"]
        return random.choice(seasons)  # Placeholder
    
    def _check_marketplace_formation(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Check if conditions are right for marketplace formation."""
        events = []
        
        # Analyze trading activity by location
        location_trading = defaultdict(lambda: {
            "traders": set(),
            "trade_volume": 0.0,
            "goods_variety": set(),
            "population": 0
        })
        
        # Count recent trading activity
        recent_trades = [t for t in self.trade_history if current_day - t["day"] <= 30]
        
        for trade in recent_trades:
            location = trade["location"]
            location_trading[location]["trade_volume"] += trade["value"]
            location_trading[location]["traders"].update(trade["participants"])
            location_trading[location]["goods_variety"].update(
                trade["goods"]["agent1_gives"] + trade["goods"]["agent2_gives"])
        
        # Count population by location
        for agent in agents:
            if agent.is_alive:
                location_trading[agent.location]["population"] += 1
        
        # Check each location for marketplace formation opportunities
        for location, data in location_trading.items():
            # Skip if marketplace already exists
            if any(mp.location == location for mp in self.marketplaces.values()):
                continue
            
            marketplace_type = self._determine_marketplace_type(data)
            
            if marketplace_type:
                marketplace = self._create_marketplace(location, marketplace_type, data, current_day)
                events.append({
                    "type": "marketplace_formation",
                    "marketplace_name": marketplace.name,
                    "marketplace_type": marketplace_type.value,
                    "location": location,
                    "founders": list(data["traders"]),
                    "trade_volume": data["trade_volume"],
                    "day": current_day
                })
        
        return events
    
    def _determine_marketplace_type(self, location_data: Dict[str, Any]) -> Optional[MarketType]:
        """Determine what type of marketplace should form based on location data."""
        traders = len(location_data["traders"])
        volume = location_data["trade_volume"]
        variety = len(location_data["goods_variety"])
        population = location_data["population"]
        
        thresholds = self.market_formation_thresholds
        
        # Check for regional hub (highest requirements)
        if (traders >= thresholds["regional_hub"]["min_traders"] and
            volume >= thresholds["regional_hub"]["min_trade_volume"] and
            population >= thresholds["regional_hub"]["min_population"]):
            return MarketType.REGIONAL_HUB
        
        # Check for specialized market
        if (traders >= thresholds["specialized_market"]["min_traders"] and
            volume >= thresholds["specialized_market"]["min_trade_volume"]):
            # Check if trading is specialized (70% of goods in one category)
            if self._is_trading_specialized(location_data):
                return MarketType.SPECIALIZED_MARKET
        
        # Check for local market
        if (traders >= thresholds["local_market"]["min_traders"] and
            volume >= thresholds["local_market"]["min_trade_volume"] and
            variety >= thresholds["local_market"]["min_good_variety"] and
            population >= thresholds["local_market"]["min_population"]):
            return MarketType.LOCAL_MARKET
        
        return None
    
    def _is_trading_specialized(self, location_data: Dict[str, Any]) -> bool:
        """Check if trading in a location is specialized to one category."""
        # This would analyze the types of goods being traded
        # For simplicity, assume 30% chance of specialization
        return random.random() < 0.3
    
    def _create_marketplace(self, location: str, marketplace_type: MarketType, 
                          location_data: Dict[str, Any], current_day: int) -> MarketPlace:
        """Create a new marketplace."""
        marketplace_id = f"market_{location}_{current_day}"
        marketplace_name = f"{location.replace('_', ' ').title()} {marketplace_type.value.replace('_', ' ').title()}"
        
        marketplace = MarketPlace(
            id=marketplace_id,
            name=marketplace_name,
            market_type=marketplace_type,
            location=location,
            established_day=current_day,
            goods_traded=location_data["goods_variety"],
            regular_traders=location_data["traders"],
            daily_volume=location_data["trade_volume"] / 30,  # Average daily
            specializations=[],  # Would be determined from traded goods
            currency_systems=[CurrencyType.BARTER],  # Start with barter
            price_index={},
            trade_regulations=[],
            market_makers=set(),
            competition_level=0.5,
            trust_level=0.6,
            transaction_costs=0.1,
            market_efficiency=0.4,
            connected_markets=set(),
            trade_routes={},
            supply_chains={}
        )
        
        self.marketplaces[marketplace_id] = marketplace
        return marketplace
    
    def _develop_trade_routes(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Develop trade routes between different locations."""
        events = []
        
        # Find potential trade route opportunities
        location_pairs = self._identify_trade_route_opportunities(agents)
        
        for origin, destination in location_pairs:
            # Check if route already exists
            existing_route = self._find_existing_route(origin, destination)
            
            if not existing_route:
                # Check if conditions support route creation
                if self._should_create_trade_route(origin, destination, agents):
                    route = self._create_trade_route(origin, destination, current_day)
                    events.append({
                        "type": "trade_route_established",
                        "route_name": f"{origin} - {destination}",
                        "origin": origin,
                        "destination": destination,
                        "estimated_travel_time": route.travel_time,
                        "day": current_day
                    })
            else:
                # Update existing route usage
                self._update_trade_route_usage(existing_route, agents, current_day)
        
        return events
    
    def _identify_trade_route_opportunities(self, agents: List[Any]) -> List[Tuple[str, str]]:
        """Identify potential trade routes between locations."""
        # Get all locations with significant population
        locations = defaultdict(int)
        for agent in agents:
            if agent.is_alive:
                locations[agent.location] += 1
        
        # Filter to locations with 3+ people
        viable_locations = [loc for loc, pop in locations.items() if pop >= 3]
        
        # Generate location pairs
        location_pairs = []
        for i, loc1 in enumerate(viable_locations):
            for loc2 in viable_locations[i+1:]:
                location_pairs.append((loc1, loc2))
        
        return location_pairs
    
    def _find_existing_route(self, origin: str, destination: str) -> Optional[TradeRoute]:
        """Find existing trade route between two locations."""
        for route in self.trade_routes.values():
            if ((route.origin == origin and route.destination == destination) or
                (route.origin == destination and route.destination == origin)):
                return route
        return None
    
    def _should_create_trade_route(self, origin: str, destination: str, agents: List[Any]) -> bool:
        """Determine if a trade route should be created."""
        # Check for complementary economic activity
        origin_agents = [a for a in agents if a.is_alive and a.location == origin]
        dest_agents = [a for a in agents if a.is_alive and a.location == destination]
        
        # Need merchants or traders at both ends
        origin_traders = len([a for a in origin_agents if 
                            self.economic_agents.get(a.name) and
                            self.economic_agents[a.name].economic_role == EconomicRole.TRADER])
        dest_traders = len([a for a in dest_agents if 
                          self.economic_agents.get(a.name) and
                          self.economic_agents[a.name].economic_role == EconomicRole.TRADER])
        
        if origin_traders == 0 or dest_traders == 0:
            return False
        
        # Check for trade complementarity
        complementarity = self._calculate_location_complementarity(origin_agents, dest_agents)
        
        return complementarity > 0.3  # Threshold for route viability
    
    def _calculate_location_complementarity(self, origin_agents: List[Any], dest_agents: List[Any]) -> float:
        """Calculate economic complementarity between two locations."""
        origin_production = defaultdict(float)
        origin_consumption = defaultdict(float)
        dest_production = defaultdict(float)
        dest_consumption = defaultdict(float)
        
        # Aggregate production and consumption
        for agent in origin_agents:
            econ_agent = self.economic_agents.get(agent.name)
            if econ_agent:
                for good_id, amount in econ_agent.production_capacity.items():
                    origin_production[good_id] += amount
                for good_id, amount in econ_agent.consumption_needs.items():
                    origin_consumption[good_id] += amount
        
        for agent in dest_agents:
            econ_agent = self.economic_agents.get(agent.name)
            if econ_agent:
                for good_id, amount in econ_agent.production_capacity.items():
                    dest_production[good_id] += amount
                for good_id, amount in econ_agent.consumption_needs.items():
                    dest_consumption[good_id] += amount
        
        # Calculate complementarity
        complementarity = 0.0
        all_goods = set(origin_production.keys()) | set(dest_production.keys())
        
        for good_id in all_goods:
            origin_surplus = origin_production.get(good_id, 0) - origin_consumption.get(good_id, 0)
            dest_surplus = dest_production.get(good_id, 0) - dest_consumption.get(good_id, 0)
            
            # Complementarity when one has surplus and other has deficit
            if origin_surplus > 0 and dest_surplus < 0:
                complementarity += min(origin_surplus, abs(dest_surplus))
            elif origin_surplus < 0 and dest_surplus > 0:
                complementarity += min(abs(origin_surplus), dest_surplus)
        
        return min(1.0, complementarity / max(1, len(all_goods)))
    
    def _create_trade_route(self, origin: str, destination: str, current_day: int) -> TradeRoute:
        """Create a new trade route."""
        route_id = f"route_{origin}_{destination}_{current_day}"
        
        # Calculate route characteristics
        distance_difficulty = self._calculate_route_difficulty(origin, destination)
        travel_time = max(1, int(distance_difficulty * 10))  # 1-10 days
        transport_costs = 0.1 + distance_difficulty * 0.2
        safety_level = random.uniform(0.6, 0.9)
        
        route = TradeRoute(
            id=route_id,
            origin=origin,
            destination=destination,
            established_day=current_day,
            distance_difficulty=distance_difficulty,
            goods_flow={},
            regular_traders=set(),
            transport_costs=transport_costs,
            travel_time=travel_time,
            safety_level=safety_level,
            profitability=0.0,  # Will be calculated based on usage
            infrastructure_level=0.1,  # Starts basic
            services_available=[]
        )
        
        self.trade_routes[route_id] = route
        return route
    
    def _calculate_route_difficulty(self, origin: str, destination: str) -> float:
        """Calculate difficulty of travel between two locations."""
        # Simplified difficulty based on location types
        terrain_difficulty = {
            "village_center": 0.1,
            "fields": 0.2,
            "forest": 0.5,
            "river": 0.3,
            "mountains": 0.8,
            "hills": 0.6,
            "coast": 0.4,
            "desert": 0.9,
            "plains": 0.2
        }
        
        origin_difficulty = terrain_difficulty.get(origin, 0.5)
        dest_difficulty = terrain_difficulty.get(destination, 0.5)
        
        return (origin_difficulty + dest_difficulty) / 2
    
    def _update_trade_route_usage(self, route: TradeRoute, agents: List[Any], current_day: int):
        """Update trade route based on usage."""
        # Count traders using this route
        route_users = len([a for a in agents if a.is_alive and 
                         (a.location == route.origin or a.location == route.destination) and
                         self.economic_agents.get(a.name) and
                         self.economic_agents[a.name].economic_role == EconomicRole.TRADER])
        
        # Update route metrics
        if route_users > 0:
            route.infrastructure_level = min(1.0, route.infrastructure_level + 0.01)
            route.safety_level = min(1.0, route.safety_level + 0.005)
        else:
            route.infrastructure_level = max(0.0, route.infrastructure_level - 0.005)
            route.safety_level = max(0.3, route.safety_level - 0.002)
    
    def _evolve_currency_systems(self, current_day: int) -> List[Dict[str, Any]]:
        """Evolve currency systems based on trade complexity."""
        events = []
        
        # Calculate overall trade metrics
        trade_metrics = self._calculate_trade_complexity_metrics()
        
        # Check for currency evolution opportunities
        for stage_info in self.currency_evolution_stages:
            currency_type = stage_info["stage"]
            requirements = stage_info["requirements"]
            
            # Check if requirements are met
            if self._currency_requirements_met(requirements, trade_metrics):
                # Check if this currency type exists in any marketplace
                if not self._currency_type_exists(currency_type):
                    # Introduce new currency type
                    marketplace = self._select_marketplace_for_currency_evolution()
                    if marketplace:
                        marketplace.currency_systems.append(currency_type)
                        
                        events.append({
                            "type": "currency_evolution",
                            "new_currency": currency_type.value,
                            "marketplace": marketplace.name,
                            "description": stage_info["description"],
                            "day": current_day
                        })
        
        return events
    
    def _calculate_trade_complexity_metrics(self) -> Dict[str, float]:
        """Calculate metrics for trade complexity."""
        recent_trades = [t for t in self.trade_history if len(self.trade_history) - self.trade_history.index(t) <= 100]
        
        if not recent_trades:
            return {"trade_volume": 0, "trade_complexity": 0, "market_trust": 0}
        
        metrics = {
            "trade_volume": len(recent_trades),
            "trade_complexity": 0.0,
            "market_trust": 0.0,
            "institutions": len([mp for mp in self.marketplaces.values() 
                               if mp.market_type in [MarketType.LOCAL_MARKET, MarketType.REGIONAL_HUB]]),
            "financial_institutions": len([mp for mp in self.marketplaces.values() 
                                         if mp.market_type == MarketType.FINANCIAL_CENTER])
        }
        
        # Calculate trade complexity
        unique_goods = set()
        total_fairness = 0.0
        
        for trade in recent_trades:
            goods = trade["goods"]["agent1_gives"] + trade["goods"]["agent2_gives"]
            unique_goods.update(goods)
            total_fairness += trade["fairness"]
        
        metrics["trade_complexity"] = len(unique_goods) / max(1, len(self.trade_goods))
        metrics["market_trust"] = total_fairness / len(recent_trades) if recent_trades else 0.0
        
        return metrics
    
    def _currency_requirements_met(self, requirements: Dict[str, Any], 
                                 trade_metrics: Dict[str, float]) -> bool:
        """Check if requirements for currency evolution are met."""
        for req_name, req_value in requirements.items():
            if trade_metrics.get(req_name, 0) < req_value:
                return False
        return True
    
    def _currency_type_exists(self, currency_type: CurrencyType) -> bool:
        """Check if a currency type already exists in any marketplace."""
        for marketplace in self.marketplaces.values():
            if currency_type in marketplace.currency_systems:
                return True
        return False
    
    def _select_marketplace_for_currency_evolution(self) -> Optional[MarketPlace]:
        """Select the best marketplace for currency evolution."""
        if not self.marketplaces:
            return None
        
        # Prefer larger, more active marketplaces
        best_marketplace = None
        best_score = 0.0
        
        for marketplace in self.marketplaces.values():
            score = marketplace.daily_volume * marketplace.trust_level * marketplace.market_efficiency
            if score > best_score:
                best_score = score
                best_marketplace = marketplace
        
        return best_marketplace
    
    def _apply_economic_cycles(self, current_day: int) -> List[Dict[str, Any]]:
        """Apply economic cycles and fluctuations."""
        events = []
        
        # Apply seasonal cycles
        season_events = self._apply_seasonal_cycles(current_day)
        events.extend(season_events)
        
        # Check for boom/bust cycles
        boom_bust_events = self._check_boom_bust_cycles(current_day)
        events.extend(boom_bust_events)
        
        # Random supply shocks
        shock_events = self._check_supply_shocks(current_day)
        events.extend(shock_events)
        
        return events
    
    def _apply_seasonal_cycles(self, current_day: int) -> List[Dict[str, Any]]:
        """Apply seasonal economic effects."""
        events = []
        
        # This would integrate with world state seasons
        # For now, simulate seasonal effects
        season_cycle = (current_day % 365) / 365.0  # 0-1 through year
        
        for good_id, good in self.trade_goods.items():
            if good.category in [TradeGoodCategory.FOOD, TradeGoodCategory.MATERIALS]:
                # Apply seasonal price modifier
                seasonal_effect = math.sin(season_cycle * 2 * math.pi) * 0.2  # ±20%
                seasonal_price = good.base_value * (1 + seasonal_effect)
                
                # Smooth transition
                good.current_price = (good.current_price * 0.9) + (seasonal_price * 0.1)
        
        return events
    
    def _check_boom_bust_cycles(self, current_day: int) -> List[Dict[str, Any]]:
        """Check for boom/bust economic cycles."""
        events = []
        
        # Simple boom/bust cycle based on overall trade volume
        if len(self.trade_history) > 50:  # Need some history
            recent_volume = len([t for t in self.trade_history if current_day - t["day"] <= 30])
            historical_volume = len(self.trade_history) / max(1, current_day / 30)
            
            volume_ratio = recent_volume / max(1, historical_volume)
            
            if volume_ratio > 1.5:  # Boom
                events.append({
                    "type": "economic_boom",
                    "volume_increase": volume_ratio,
                    "description": "Economic activity surging above normal levels",
                    "day": current_day
                })
                
                # Boom increases prices
                for good in self.trade_goods.values():
                    good.current_price *= 1.1
                    
            elif volume_ratio < 0.6:  # Bust
                events.append({
                    "type": "economic_bust",
                    "volume_decrease": volume_ratio,
                    "description": "Economic activity declining below normal levels",
                    "day": current_day
                })
                
                # Bust decreases prices
                for good in self.trade_goods.values():
                    good.current_price *= 0.9
        
        return events
    
    def _check_supply_shocks(self, current_day: int) -> List[Dict[str, Any]]:
        """Check for random supply shocks."""
        events = []
        
        # 2% chance per day of supply shock
        if random.random() < 0.02:
            affected_good = random.choice(list(self.trade_goods.values()))
            shock_type = random.choice(["shortage", "surplus"])
            intensity = random.uniform(0.3, 0.7)
            
            if shock_type == "shortage":
                affected_good.supply *= (1 - intensity)
                affected_good.current_price *= (1 + intensity)
                description = f"Supply shortage of {affected_good.name}"
            else:
                affected_good.supply *= (1 + intensity)
                affected_good.current_price *= (1 - intensity * 0.5)
                description = f"Supply surplus of {affected_good.name}"
            
            events.append({
                "type": "supply_shock",
                "affected_good": affected_good.name,
                "shock_type": shock_type,
                "intensity": intensity,
                "description": description,
                "day": current_day
            })
        
        return events
    
    def _detect_economic_emergence(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Detect emergent economic phenomena."""
        events = []
        
        # Detect wealth stratification
        stratification_events = self._detect_wealth_stratification(agents, current_day)
        events.extend(stratification_events)
        
        # Detect economic specialization
        specialization_events = self._detect_economic_specialization(agents, current_day)
        events.extend(specialization_events)
        
        # Detect market dominance
        dominance_events = self._detect_market_dominance(agents, current_day)
        events.extend(dominance_events)
        
        return events
    
    def _detect_wealth_stratification(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Detect emergence of wealth classes."""
        events = []
        
        if len(self.economic_agents) < 5:
            return events
        
        # Calculate wealth distribution
        wealth_levels = [econ_agent.wealth_level for econ_agent in self.economic_agents.values()]
        if not wealth_levels:
            return events
        
        wealth_levels.sort()
        
        # Calculate Gini coefficient (inequality measure)
        n = len(wealth_levels)
        index = range(1, n + 1)
        gini = (2 * sum(index[i] * wealth_levels[i] for i in range(n))) / (n * sum(wealth_levels)) - (n + 1) / n
        
        if gini > 0.4:  # Significant inequality
            events.append({
                "type": "wealth_stratification",
                "gini_coefficient": gini,
                "wealth_inequality": "high" if gini > 0.6 else "moderate",
                "description": f"Wealth inequality detected (Gini: {gini:.2f})",
                "day": current_day
            })
        
        return events
    
    def _detect_economic_specialization(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Detect emergence of economic specialization."""
        events = []
        
        # Count agents by economic role
        role_counts = defaultdict(int)
        for econ_agent in self.economic_agents.values():
            role_counts[econ_agent.economic_role] += 1
        
        total_agents = len(self.economic_agents)
        if total_agents < 5:
            return events
        
        # Check for specialization (less than 50% consumers)
        consumer_ratio = role_counts[EconomicRole.CONSUMER] / total_agents
        
        if consumer_ratio < 0.5:
            events.append({
                "type": "economic_specialization",
                "consumer_ratio": consumer_ratio,
                "role_distribution": {role.value: count for role, count in role_counts.items()},
                "description": "Economy showing significant role specialization",
                "day": current_day
            })
        
        return events
    
    def _detect_market_dominance(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Detect market dominance by individual agents."""
        events = []
        
        # Analyze trade volume by agent
        agent_volumes = defaultdict(float)
        recent_trades = [t for t in self.trade_history if current_day - t["day"] <= 30]
        
        for trade in recent_trades:
            for participant in trade["participants"]:
                agent_volumes[participant] += trade["value"]
        
        if not agent_volumes:
            return events
        
        total_volume = sum(agent_volumes.values())
        
        # Check for dominance (>40% of trade volume)
        for agent_name, volume in agent_volumes.items():
            if volume / total_volume > 0.4:
                events.append({
                    "type": "market_dominance",
                    "dominant_agent": agent_name,
                    "market_share": volume / total_volume,
                    "description": f"{agent_name} dominates trade with {volume/total_volume:.1%} market share",
                    "day": current_day
                })
        
        return events
    
    def get_economic_summary(self) -> Dict[str, Any]:
        """Get comprehensive economic system summary."""
        summary = {
            "total_trade_goods": len(self.trade_goods),
            "active_marketplaces": len(self.marketplaces),
            "trade_routes": len(self.trade_routes),
            "economic_agents": len(self.economic_agents),
            "total_trades": len(self.trade_history),
            "recent_trade_volume": 0.0,
            "price_trends": {},
            "currency_systems": set(),
            "economic_complexity": 0.0
        }
        
        # Calculate recent trade volume
        recent_trades = self.trade_history[-30:] if len(self.trade_history) >= 30 else self.trade_history
        summary["recent_trade_volume"] = sum(trade["value"] for trade in recent_trades)
        
        # Price trends for key goods
        for good_id, good in list(self.trade_goods.items())[:5]:  # Top 5 goods
            if good_id in self.price_history and len(self.price_history[good_id]) >= 2:
                recent_price = self.price_history[good_id][-1][1]
                old_price = self.price_history[good_id][-2][1] if len(self.price_history[good_id]) >= 2 else recent_price
                change = (recent_price - old_price) / old_price if old_price > 0 else 0
                summary["price_trends"][good.name] = {
                    "current_price": recent_price,
                    "price_change": change
                }
        
        # Currency systems in use
        for marketplace in self.marketplaces.values():
            summary["currency_systems"].update(cs.value for cs in marketplace.currency_systems)
        
        # Economic complexity score
        complexity_factors = [
            len(self.marketplaces) / 5.0,  # Market development
            len(summary["currency_systems"]) / 4.0,  # Currency sophistication
            min(1.0, summary["recent_trade_volume"] / 100.0),  # Trade volume
            len(self.trade_routes) / 10.0  # Trade network
        ]
        summary["economic_complexity"] = min(1.0, sum(complexity_factors) / len(complexity_factors))
        
        return summary 