"""
Advanced Conflict Resolution System for SimuLife
Manages disputes, negotiations, and various types of conflicts between agents.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum


class ConflictType(Enum):
    """Types of conflicts that can arise between agents."""
    RESOURCE_DISPUTE = "resource_dispute"       # Disagreement over resources
    PERSONAL_GRIEVANCE = "personal_grievance"   # Personal conflicts or insults
    IDEOLOGICAL = "ideological"                 # Different beliefs or values
    TERRITORIAL = "territorial"                 # Space or location disputes
    AUTHORITY = "authority"                     # Leadership or hierarchy disputes
    ROMANTIC = "romantic"                       # Love triangle or relationship issues
    FAMILY = "family"                          # Family disputes or inheritance
    PROFESSIONAL = "professional"               # Work-related conflicts
    ETHICAL = "ethical"                        # Moral disagreements


class ConflictSeverity(Enum):
    """Severity levels of conflicts."""
    MINOR = "minor"           # Small disagreements
    MODERATE = "moderate"     # Significant disputes
    MAJOR = "major"          # Serious conflicts
    SEVERE = "severe"        # Community-threatening conflicts


class ResolutionMethod(Enum):
    """Methods of conflict resolution."""
    DISCUSSION = "discussion"         # Direct talking
    MEDIATION = "mediation"          # Third party mediator
    NEGOTIATION = "negotiation"      # Formal bargaining
    COMMUNITY_DECISION = "community" # Community vote/decision
    AUTHORITY_RULING = "authority"   # Leader makes decision
    RITUAL_CHALLENGE = "ritual"      # Ceremonial competition
    SEPARATION = "separation"        # Avoid each other
    SUBMISSION = "submission"        # One party yields


@dataclass
class Conflict:
    """Represents an active conflict between agents."""
    id: str
    type: ConflictType
    severity: ConflictSeverity
    participants: List[str]        # Agent names involved
    primary_disputants: List[str]  # Main conflicting parties
    description: str
    underlying_cause: str
    started_day: int
    escalation_factors: List[str] = None
    resolution_attempts: List[Dict] = None
    status: str = "active"         # active, resolved, dormant
    community_impact: float = 0.0  # How much it affects others
    
    def __post_init__(self):
        if self.escalation_factors is None:
            self.escalation_factors = []
        if self.resolution_attempts is None:
            self.resolution_attempts = []


@dataclass
class ResolutionAttempt:
    """Represents an attempt to resolve a conflict."""
    method: ResolutionMethod
    participants: List[str]
    mediator: Optional[str] = None
    success_probability: float = 0.5
    outcome: Optional[str] = None
    day_attempted: int = 0


class ConflictSystem:
    """
    Manages conflicts, disputes, and their resolution in the community.
    """
    
    def __init__(self):
        self.active_conflicts = {}  # id -> Conflict
        self.resolved_conflicts = []
        self.conflict_history = {}  # Track past conflicts between agents
        self.conflict_counter = 0
        
    def _generate_conflict_id(self) -> str:
        """Generate a unique conflict ID."""
        self.conflict_counter += 1
        return f"conflict_{self.conflict_counter:03d}"
    
    def detect_potential_conflicts(self, agents: List, current_day: int) -> List[Dict[str, Any]]:
        """Detect potential conflicts based on agent states and relationships."""
        potential_conflicts = []
        
        for i, agent1 in enumerate(agents):
            if not agent1.is_alive:
                continue
                
            for j, agent2 in enumerate(agents[i+1:], i+1):
                if not agent2.is_alive:
                    continue
                
                # Check relationship tension
                conflict_chance = self._calculate_conflict_probability(agent1, agent2, current_day)
                
                if conflict_chance > 0.1 and random.random() < conflict_chance:
                    conflict_data = self._generate_conflict(agent1, agent2, current_day)
                    if conflict_data:
                        potential_conflicts.append(conflict_data)
        
        return potential_conflicts
    
    def _calculate_conflict_probability(self, agent1, agent2, current_day: int) -> float:
        """Calculate the probability of conflict between two agents."""
        base_probability = 0.02  # 2% base chance per day
        
        # Get relationship if it exists
        relationship_strength = 0.0
        if agent2.name in agent1.relationships:
            rel = agent1.relationships[agent2.name]
            if isinstance(rel, dict):
                relationship_strength = rel.get("strength", 0.0)
            else:
                # Convert simple relationship strings to numeric values
                relationship_map = {
                    "friend": 0.7, "close_friend": 0.8, "best_friend": 0.9,
                    "brother": 0.6, "sister": 0.6, "family": 0.6,
                    "rival": -0.3, "enemy": -0.7,
                    "neutral": 0.0, "acquaintance": 0.2
                }
                relationship_strength = relationship_map.get(str(rel).lower(), 0.0)
        
        # Negative relationships increase conflict chance
        if relationship_strength < -0.3:
            base_probability += abs(relationship_strength) * 0.1
        
        # Positive relationships decrease conflict chance
        if relationship_strength > 0.5:
            base_probability *= 0.3
        
        # Personality factors
        personality_tension = 0.0
        
        # Conflicting traits
        conflict_traits = {
            "aggressive": ["peaceful", "gentle"],
            "selfish": ["generous", "altruistic"],
            "stubborn": ["flexible", "adaptable"],
            "competitive": ["cooperative", "supportive"]
        }
        
        for trait1 in agent1.traits:
            if trait1 in conflict_traits:
                for trait2 in agent2.traits:
                    if trait2 in conflict_traits[trait1]:
                        personality_tension += 0.05
        
        # Same conflicting traits (e.g., two aggressive agents)
        aggressive_traits = ["aggressive", "ambitious", "competitive", "stubborn"]
        agent1_aggressive = sum(1 for trait in agent1.traits if trait in aggressive_traits)
        agent2_aggressive = sum(1 for trait in agent2.traits if trait in aggressive_traits)
        
        if agent1_aggressive >= 2 and agent2_aggressive >= 2:
            personality_tension += 0.03
        
        # Emotional state factors
        emotional_factor = 0.0
        if hasattr(agent1, 'emotion') and agent1.emotion in ["angry", "frustrated", "jealous"]:
            emotional_factor += 0.02
        if hasattr(agent2, 'emotion') and agent2.emotion in ["angry", "frustrated", "jealous"]:
            emotional_factor += 0.02
        
        # Resource scarcity increases conflicts
        scarcity_factor = 0.0
        if hasattr(agent1, 'resources') and hasattr(agent2, 'resources'):
            for resource in ['food', 'water', 'shelter']:
                if (agent1.resources.get(resource, 1.0) < 0.3 and 
                    agent2.resources.get(resource, 1.0) < 0.3):
                    scarcity_factor += 0.01
        
        total_probability = base_probability + personality_tension + emotional_factor + scarcity_factor
        return min(0.3, max(0.0, total_probability))  # Cap at 30%
    
    def _generate_conflict(self, agent1, agent2, current_day: int) -> Optional[Dict[str, Any]]:
        """Generate a specific conflict between two agents."""
        # Determine conflict type based on context
        possible_conflicts = []
        
        # Resource disputes (common during scarcity)
        if hasattr(agent1, 'resources') and hasattr(agent2, 'resources'):
            agent1_poor = any(agent1.resources.get(r, 1.0) < 0.4 for r in ['food', 'water', 'shelter'])
            agent2_poor = any(agent2.resources.get(r, 1.0) < 0.4 for r in ['food', 'water', 'shelter'])
            if agent1_poor or agent2_poor:
                possible_conflicts.append((ConflictType.RESOURCE_DISPUTE, 0.4))
        
        # Personal grievances (based on negative relationship)
        rel = agent1.relationships.get(agent2.name, None)
        relationship_strength = 0.0
        if rel:
            if isinstance(rel, dict):
                relationship_strength = rel.get("strength", 0.0)
            else:
                # Convert simple relationship strings to numeric values
                relationship_map = {
                    "friend": 0.7, "close_friend": 0.8, "best_friend": 0.9,
                    "brother": 0.6, "sister": 0.6, "family": 0.6,
                    "rival": -0.3, "enemy": -0.7,
                    "neutral": 0.0, "acquaintance": 0.2
                }
                relationship_strength = relationship_map.get(str(rel).lower(), 0.0)
        
        if relationship_strength < -0.2:
            possible_conflicts.append((ConflictType.PERSONAL_GRIEVANCE, 0.3))
        
        # Authority disputes (if both have leadership traits)
        if ("ambitious" in agent1.traits and "ambitious" in agent2.traits):
            possible_conflicts.append((ConflictType.AUTHORITY, 0.2))
        
        # Professional conflicts (if both specialized)
        if (hasattr(agent1, 'specialization') and hasattr(agent2, 'specialization') and
            agent1.specialization and agent2.specialization):
            if agent1.specialization.type == agent2.specialization.type:
                possible_conflicts.append((ConflictType.PROFESSIONAL, 0.25))
        
        # Ideological conflicts (different worldviews)
        possible_conflicts.append((ConflictType.IDEOLOGICAL, 0.15))
        
        # Territorial disputes
        if agent1.location == agent2.location:
            possible_conflicts.append((ConflictType.TERRITORIAL, 0.1))
        
        if not possible_conflicts:
            return None
        
        # Weight-based selection
        total_weight = sum(weight for _, weight in possible_conflicts)
        r = random.uniform(0, total_weight)
        current_weight = 0
        
        selected_type = ConflictType.PERSONAL_GRIEVANCE  # default
        for conflict_type, weight in possible_conflicts:
            current_weight += weight
            if r <= current_weight:
                selected_type = conflict_type
                break
        
        # Determine severity
        severity = self._determine_conflict_severity(agent1, agent2, selected_type)
        
        # Generate description
        description = self._generate_conflict_description(agent1, agent2, selected_type)
        
        # Create conflict object
        conflict_id = self._generate_conflict_id()
        conflict = Conflict(
            id=conflict_id,
            type=selected_type,
            severity=severity,
            participants=[agent1.name, agent2.name],
            primary_disputants=[agent1.name, agent2.name],
            description=description,
            underlying_cause=self._determine_underlying_cause(agent1, agent2, selected_type),
            started_day=current_day
        )
        
        self.active_conflicts[conflict_id] = conflict
        
        # Add memories to both agents
        agent1.add_memory(f"Got into a {selected_type.value} with {agent2.name}: {description}", importance=0.7)
        agent2.add_memory(f"Got into a {selected_type.value} with {agent1.name}: {description}", importance=0.7)
        
        # Affect relationship
        self._affect_relationship(agent1, agent2, -0.2)
        
        return {
            "type": "conflict_started",
            "conflict_id": conflict_id,
            "conflict_type": selected_type.value,
            "severity": severity.value,
            "participants": [agent1.name, agent2.name],
            "description": description
        }
    
    def _determine_conflict_severity(self, agent1, agent2, conflict_type: ConflictType) -> ConflictSeverity:
        """Determine how severe a conflict is."""
        base_severity = {
            ConflictType.RESOURCE_DISPUTE: ConflictSeverity.MODERATE,
            ConflictType.PERSONAL_GRIEVANCE: ConflictSeverity.MINOR,
            ConflictType.IDEOLOGICAL: ConflictSeverity.MODERATE,
            ConflictType.TERRITORIAL: ConflictSeverity.MODERATE,
            ConflictType.AUTHORITY: ConflictSeverity.MAJOR,
            ConflictType.ROMANTIC: ConflictSeverity.MODERATE,
            ConflictType.FAMILY: ConflictSeverity.MAJOR,
            ConflictType.PROFESSIONAL: ConflictSeverity.MODERATE,
            ConflictType.ETHICAL: ConflictSeverity.MAJOR
        }
        
        severity = base_severity.get(conflict_type, ConflictSeverity.MINOR)
        
        # Personality factors can escalate
        escalating_traits = ["aggressive", "stubborn", "hot-tempered", "prideful"]
        agent1_escalates = any(trait in agent1.traits for trait in escalating_traits)
        agent2_escalates = any(trait in agent2.traits for trait in escalating_traits)
        
        if agent1_escalates and agent2_escalates:
            # Escalate by one level
            severity_order = [ConflictSeverity.MINOR, ConflictSeverity.MODERATE, 
                            ConflictSeverity.MAJOR, ConflictSeverity.SEVERE]
            current_index = severity_order.index(severity)
            if current_index < len(severity_order) - 1:
                severity = severity_order[current_index + 1]
        
        return severity
    
    def _generate_conflict_description(self, agent1, agent2, conflict_type: ConflictType) -> str:
        """Generate a description for the conflict."""
        descriptions = {
            ConflictType.RESOURCE_DISPUTE: [
                f"disagreement over resource allocation",
                f"dispute about access to essential supplies",
                f"argument over who gets limited resources"
            ],
            ConflictType.PERSONAL_GRIEVANCE: [
                f"personal disagreement escalated into conflict",
                f"long-standing tensions finally erupted",
                f"personal insult led to heated argument"
            ],
            ConflictType.IDEOLOGICAL: [
                f"fundamental disagreement about community values",
                f"clash over different worldviews",
                f"argument about the right way to live"
            ],
            ConflictType.AUTHORITY: [
                f"dispute over leadership roles",
                f"disagreement about who should make decisions",
                f"conflict over authority and responsibility"
            ],
            ConflictType.PROFESSIONAL: [
                f"professional rivalry turned contentious",
                f"disagreement over work methods",
                f"competition for recognition became hostile"
            ],
            ConflictType.TERRITORIAL: [
                f"dispute over space and territory",
                f"disagreement about area boundaries",
                f"conflict over access to locations"
            ]
        }
        
        options = descriptions.get(conflict_type, ["general disagreement"])
        return random.choice(options)
    
    def _determine_underlying_cause(self, agent1, agent2, conflict_type: ConflictType) -> str:
        """Determine the deeper cause of the conflict."""
        causes = {
            ConflictType.RESOURCE_DISPUTE: "scarcity and survival pressure",
            ConflictType.PERSONAL_GRIEVANCE: "personality clash and accumulated grievances",
            ConflictType.IDEOLOGICAL: "fundamental differences in values and beliefs",
            ConflictType.AUTHORITY: "ambition and desire for control",
            ConflictType.PROFESSIONAL: "competition and professional jealousy",
            ConflictType.TERRITORIAL: "need for space and security"
        }
        return causes.get(conflict_type, "misunderstanding and miscommunication")
    
    def _affect_relationship(self, agent1, agent2, change: float):
        """Modify the relationship between two agents."""
        # Helper function to convert string relationships to dict format
        def ensure_relationship_dict(agent, other_name):
            if other_name not in agent.relationships:
                agent.relationships[other_name] = {"strength": 0.0, "type": "neutral"}
            elif isinstance(agent.relationships[other_name], str):
                # Convert string relationship to dict
                old_rel = agent.relationships[other_name]
                relationship_map = {
                    "friend": 0.7, "close_friend": 0.8, "best_friend": 0.9,
                    "brother": 0.6, "sister": 0.6, "family": 0.6,
                    "rival": -0.3, "enemy": -0.7,
                    "neutral": 0.0, "acquaintance": 0.2
                }
                strength = relationship_map.get(str(old_rel).lower(), 0.0)
                agent.relationships[other_name] = {"strength": strength, "type": str(old_rel).lower()}
        
        ensure_relationship_dict(agent1, agent2.name)
        ensure_relationship_dict(agent2, agent1.name)
        
        agent1.relationships[agent2.name]["strength"] += change
        agent2.relationships[agent1.name]["strength"] += change
        
        # Update relationship types based on strength
        for agent, other in [(agent1, agent2), (agent2, agent1)]:
            strength = agent.relationships[other.name]["strength"]
            if strength < -0.5:
                agent.relationships[other.name]["type"] = "enemy"
            elif strength < -0.2:
                agent.relationships[other.name]["type"] = "rival"
            elif strength > 0.5:
                agent.relationships[other.name]["type"] = "friend"
            else:
                agent.relationships[other.name]["type"] = "neutral"
    
    def attempt_conflict_resolution(self, conflict_id: str, agents: List, 
                                  current_day: int) -> Optional[Dict[str, Any]]:
        """Attempt to resolve an active conflict."""
        if conflict_id not in self.active_conflicts:
            return None
        
        conflict = self.active_conflicts[conflict_id]
        
        # Find available agents
        disputants = [agent for agent in agents if agent.name in conflict.primary_disputants and agent.is_alive]
        if len(disputants) < 2:
            return None  # Can't resolve without both parties
        
        # Determine best resolution method
        resolution_method = self._choose_resolution_method(conflict, agents)
        
        # Attempt resolution
        success, outcome = self._execute_resolution(conflict, resolution_method, agents, current_day)
        
        # Record attempt
        attempt = {
            "method": resolution_method.value,
            "day": current_day,
            "success": success,
            "outcome": outcome
        }
        conflict.resolution_attempts.append(attempt)
        
        if success:
            # Conflict resolved
            conflict.status = "resolved"
            self.resolved_conflicts.append(conflict)
            del self.active_conflicts[conflict_id]
            
            # Improve relationships if resolved amicably
            if resolution_method in [ResolutionMethod.DISCUSSION, ResolutionMethod.MEDIATION, 
                                   ResolutionMethod.NEGOTIATION]:
                for disputant in disputants:
                    for other in disputants:
                        if disputant != other:
                            self._affect_relationship(disputant, other, 0.1)
            
            # Add memories
            for agent in disputants:
                agent.add_memory(f"Resolved conflict with {', '.join(d.name for d in disputants if d != agent)} through {resolution_method.value}: {outcome}", importance=0.8)
        
        return {
            "type": "resolution_attempt",
            "conflict_id": conflict_id,
            "method": resolution_method.value,
            "success": success,
            "outcome": outcome,
            "participants": conflict.participants
        }
    
    def _choose_resolution_method(self, conflict: Conflict, agents: List) -> ResolutionMethod:
        """Choose the most appropriate resolution method."""
        # Consider conflict type and severity
        if conflict.severity == ConflictSeverity.MINOR:
            return random.choice([ResolutionMethod.DISCUSSION, ResolutionMethod.MEDIATION])
        
        elif conflict.severity == ConflictSeverity.MODERATE:
            return random.choice([ResolutionMethod.MEDIATION, ResolutionMethod.NEGOTIATION])
        
        elif conflict.severity == ConflictSeverity.MAJOR:
            return random.choice([ResolutionMethod.COMMUNITY_DECISION, ResolutionMethod.AUTHORITY_RULING])
        
        else:  # SEVERE
            return random.choice([ResolutionMethod.AUTHORITY_RULING, ResolutionMethod.SEPARATION])
    
    def _execute_resolution(self, conflict: Conflict, method: ResolutionMethod, 
                          agents: List, current_day: int) -> Tuple[bool, str]:
        """Execute a specific resolution method."""
        disputants = [agent for agent in agents if agent.name in conflict.primary_disputants]
        
        if method == ResolutionMethod.DISCUSSION:
            # Direct discussion between parties
            success_rate = 0.4
            for agent in disputants:
                if "diplomatic" in agent.traits or "empathetic" in agent.traits:
                    success_rate += 0.15
                if "stubborn" in agent.traits or "aggressive" in agent.traits:
                    success_rate -= 0.1
            
            success = random.random() < success_rate
            if success:
                return True, "The parties talked it out and reached understanding"
            else:
                return False, "Direct discussion failed to resolve differences"
        
        elif method == ResolutionMethod.MEDIATION:
            # Find a mediator
            potential_mediators = [agent for agent in agents 
                                 if agent.name not in conflict.participants and agent.is_alive]
            
            if not potential_mediators:
                return False, "No available mediator found"
            
            # Prefer agents with leadership or diplomatic skills
            best_mediators = []
            for agent in potential_mediators:
                score = 0
                if "diplomatic" in agent.traits:
                    score += 3
                if "wise" in agent.traits:
                    score += 2
                if "empathetic" in agent.traits:
                    score += 2
                if hasattr(agent, 'specialization') and agent.specialization:
                    if agent.specialization.type.value == "leader":
                        score += 3
                best_mediators.append((agent, score))
            
            best_mediators.sort(key=lambda x: x[1], reverse=True)
            mediator = best_mediators[0][0] if best_mediators else random.choice(potential_mediators)
            
            success_rate = 0.6 + (best_mediators[0][1] * 0.05 if best_mediators else 0)
            success = random.random() < success_rate
            
            if success:
                mediator.add_memory(f"Successfully mediated conflict between {', '.join(conflict.primary_disputants)}", importance=0.7)
                return True, f"{mediator.name} helped the parties find common ground"
            else:
                return False, f"Mediation by {mediator.name} was unsuccessful"
        
        elif method == ResolutionMethod.NEGOTIATION:
            # Formal negotiation with specific terms
            success_rate = 0.5
            
            # Negotiation skills matter
            for agent in disputants:
                if hasattr(agent, 'advanced_skills') and 'negotiation' in agent.advanced_skills:
                    skill_level = agent.advanced_skills['negotiation'].get_effective_level()
                    success_rate += skill_level * 0.05
            
            success = random.random() < success_rate
            if success:
                return True, "Formal negotiation resulted in mutually acceptable terms"
            else:
                return False, "Negotiations broke down without agreement"
        
        elif method == ResolutionMethod.COMMUNITY_DECISION:
            # Community votes or decides
            success_rate = 0.7  # Usually effective but may leave some unhappy
            success = random.random() < success_rate
            
            if success:
                return True, "The community reached a decision that resolved the conflict"
            else:
                return False, "Community could not reach consensus on resolution"
        
        elif method == ResolutionMethod.AUTHORITY_RULING:
            # A leader makes the decision
            leaders = [agent for agent in agents if hasattr(agent, 'specialization') 
                      and agent.specialization and agent.specialization.type.value == "leader"]
            
            if not leaders:
                return False, "No recognized authority figure available"
            
            leader = max(leaders, key=lambda x: x.specialization.level)
            success_rate = 0.8  # Authority is usually effective
            success = random.random() < success_rate
            
            if success:
                leader.add_memory(f"Made authoritative ruling to resolve conflict between {', '.join(conflict.primary_disputants)}", importance=0.8)
                return True, f"{leader.name} made an authoritative decision that resolved the matter"
            else:
                return False, f"{leader.name}'s ruling was rejected by the parties"
        
        elif method == ResolutionMethod.SEPARATION:
            # Parties agree to avoid each other
            success_rate = 0.9  # Almost always works but doesn't really solve anything
            success = random.random() < success_rate
            
            if success:
                return True, "The parties agreed to keep their distance from each other"
            else:
                return False, "Even separation could not prevent continued hostility"
        
        return False, "Resolution method failed"
    
    def process_daily_conflicts(self, agents: List, current_day: int) -> List[Dict[str, Any]]:
        """Process all conflict-related activities for the day."""
        conflict_events = []
        
        # Detect new conflicts
        new_conflicts = self.detect_potential_conflicts(agents, current_day)
        conflict_events.extend(new_conflicts)
        
        # Attempt to resolve existing conflicts
        for conflict_id in list(self.active_conflicts.keys()):
            # 30% chance per day to attempt resolution
            if random.random() < 0.3:
                resolution = self.attempt_conflict_resolution(conflict_id, agents, current_day)
                if resolution:
                    conflict_events.append(resolution)
        
        # Check for conflict escalation
        for conflict in self.active_conflicts.values():
            if current_day - conflict.started_day > 7:  # Conflicts get worse over time
                if random.random() < 0.2:  # 20% chance to escalate
                    escalation = self._escalate_conflict(conflict, agents, current_day)
                    if escalation:
                        conflict_events.append(escalation)
        
        return conflict_events
    
    def _escalate_conflict(self, conflict: Conflict, agents: List, current_day: int) -> Optional[Dict[str, Any]]:
        """Escalate an existing conflict."""
        if conflict.severity == ConflictSeverity.SEVERE:
            return None  # Already at maximum
        
        # Escalate severity
        severity_order = [ConflictSeverity.MINOR, ConflictSeverity.MODERATE, 
                         ConflictSeverity.MAJOR, ConflictSeverity.SEVERE]
        current_index = severity_order.index(conflict.severity)
        conflict.severity = severity_order[current_index + 1]
        
        # Add escalation factor
        escalation_reasons = [
            "stubbornness from both parties",
            "misunderstanding and poor communication",
            "outside pressure and stress",
            "wounded pride and ego",
            "involvement of other community members"
        ]
        
        reason = random.choice(escalation_reasons)
        conflict.escalation_factors.append(reason)
        
        # Affect more relationships
        disputants = [agent for agent in agents if agent.name in conflict.primary_disputants]
        for disputant in disputants:
            for other in disputants:
                if disputant != other:
                    self._affect_relationship(disputant, other, -0.1)
        
        return {
            "type": "conflict_escalation",
            "conflict_id": conflict.id,
            "new_severity": conflict.severity.value,
            "reason": reason,
            "participants": conflict.participants
        }
    
    def get_conflict_summary(self) -> Dict[str, Any]:
        """Get a summary of all conflicts in the community."""
        return {
            "active_conflicts": len(self.active_conflicts),
            "resolved_conflicts": len(self.resolved_conflicts),
            "conflict_types": {},
            "most_common_resolution": self._get_most_common_resolution(),
            "conflict_details": [
                {
                    "id": c.id,
                    "type": c.type.value,
                    "severity": c.severity.value,
                    "participants": c.participants,
                    "duration": 0  # Would need current_day to calculate
                }
                for c in self.active_conflicts.values()
            ]
        }
    
    def _get_most_common_resolution(self) -> str:
        """Find the most commonly used resolution method."""
        if not self.resolved_conflicts:
            return "none"
        
        methods = {}
        for conflict in self.resolved_conflicts:
            for attempt in conflict.resolution_attempts:
                if attempt["success"]:
                    method = attempt["method"]
                    methods[method] = methods.get(method, 0) + 1
        
        if not methods:
            return "none"
        
        return max(methods.items(), key=lambda x: x[1])[0] 