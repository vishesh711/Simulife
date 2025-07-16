"""
Group Dynamics System for SimuLife
Manages complex group formation, alliances, trade guilds, cultural institutions, and collective memory.
"""

import random
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum


class GroupType(Enum):
    """Types of groups that can form in SimuLife."""
    FACTION = "faction"                # Political/ideological groups
    GUILD = "guild"                   # Trade and economic groups
    ALLIANCE = "alliance"             # Multi-faction partnerships
    INSTITUTION = "institution"       # Cultural institutions (schools, temples, etc.)
    COUNCIL = "council"               # Governance bodies
    CLAN = "clan"                     # Extended family groups
    SECT = "sect"                     # Religious/spiritual groups


class GroupStatus(Enum):
    """Status levels for groups."""
    FORMING = "forming"               # Just established, unstable
    STABLE = "stable"                 # Well-established and functioning
    INFLUENTIAL = "influential"       # Major influence in community
    DOMINANT = "dominant"             # Controls significant resources/territory
    DECLINING = "declining"           # Losing members or influence
    DISBANDED = "disbanded"           # No longer active


class AllianceType(Enum):
    """Types of alliances between groups."""
    TRADE_PARTNERSHIP = "trade_partnership"    # Economic cooperation
    MUTUAL_DEFENSE = "mutual_defense"          # Military/security alliance
    CULTURAL_EXCHANGE = "cultural_exchange"    # Knowledge/cultural sharing
    POLITICAL_COALITION = "political_coalition" # Joint governance/decision making
    RESOURCE_SHARING = "resource_sharing"      # Shared access to resources
    NON_AGGRESSION = "non_aggression"          # Peace treaty


@dataclass
class GroupMember:
    """Represents a member of a group with their role and standing."""
    name: str
    role: str                    # leader, elder, member, apprentice, etc.
    joined_day: int
    loyalty: float              # 0.0-1.0 how loyal to the group
    contribution: float         # 0.0-1.0 how much they contribute
    influence: float            # 0.0-1.0 their influence within group
    status: str = "active"      # active, inactive, exiled


@dataclass
class GroupAlliance:
    """Represents an alliance between two groups."""
    group1: str
    group2: str
    alliance_type: AllianceType
    formed_day: int
    strength: float             # 0.0-1.0 how strong the alliance is
    duration: Optional[int] = None  # None = permanent, int = days remaining
    terms: List[str] = None     # Specific terms of the alliance
    violations: int = 0         # Number of times alliance has been broken


@dataclass
class CulturalInstitution:
    """Represents a cultural institution."""
    name: str
    institution_type: str       # school, temple, library, workshop, etc.
    purpose: str               # Primary function/mission
    founded_day: int
    location: str
    leaders: List[str]         # Agents who run the institution
    members: List[str]         # Agents who participate
    resources: Dict[str, float] # Resources controlled by institution
    knowledge_domains: List[str] # Types of knowledge maintained
    influence: float           # 0.0-1.0 influence in community
    capacity: int              # Maximum members it can support


@dataclass
class CollectiveMemory:
    """Represents shared knowledge and culture of a group."""
    group_name: str
    shared_knowledge: Dict[str, Any]  # Knowledge shared by all members
    cultural_artifacts: List[str]     # Names of artifacts owned by group
    traditions: List[str]             # Group traditions and customs
    myths_and_stories: List[str]      # Shared narratives
    values: List[str]                 # Core group values
    taboos: List[str]                 # Things the group avoids/forbids
    historical_events: List[Dict]     # Important events in group history


class GroupDynamicsSystem:
    """
    Manages complex group dynamics including formation, alliances, institutions, and collective memory.
    """
    
    def __init__(self):
        self.groups: Dict[str, Dict[str, Any]] = {}
        self.alliances: Dict[str, GroupAlliance] = {}
        self.institutions: Dict[str, CulturalInstitution] = {}
        self.collective_memories: Dict[str, CollectiveMemory] = {}
        self.group_events: List[Dict[str, Any]] = []
        
        # Initialization templates for different group types
        self.group_templates = self._initialize_group_templates()
        self.institution_templates = self._initialize_institution_templates()
    
    def _initialize_group_templates(self) -> Dict[GroupType, Dict[str, Any]]:
        """Initialize templates for different group types."""
        return {
            GroupType.FACTION: {
                "min_members": 3,
                "max_members": 15,
                "formation_requirements": ["shared_ideology", "leader_with_charisma"],
                "typical_goals": ["political_influence", "territory_control", "ideology_spread"]
            },
            GroupType.GUILD: {
                "min_members": 4,
                "max_members": 20,
                "formation_requirements": ["shared_profession", "economic_need"],
                "typical_goals": ["economic_control", "skill_development", "trade_monopoly"]
            },
            GroupType.ALLIANCE: {
                "min_members": 2,  # Minimum 2 groups
                "max_members": 8,  # Maximum 8 groups in alliance
                "formation_requirements": ["mutual_benefit", "compatible_goals"],
                "typical_goals": ["mutual_protection", "resource_sharing", "joint_projects"]
            },
            GroupType.INSTITUTION: {
                "min_members": 2,
                "max_members": 25,
                "formation_requirements": ["specialized_knowledge", "community_need"],
                "typical_goals": ["knowledge_preservation", "skill_teaching", "cultural_continuity"]
            },
            GroupType.COUNCIL: {
                "min_members": 3,
                "max_members": 9,
                "formation_requirements": ["community_recognition", "decision_making_need"],
                "typical_goals": ["governance", "conflict_resolution", "resource_allocation"]
            },
            GroupType.CLAN: {
                "min_members": 3,
                "max_members": 30,
                "formation_requirements": ["family_bonds", "extended_relationships"],
                "typical_goals": ["family_protection", "resource_sharing", "tradition_keeping"]
            },
            GroupType.SECT: {
                "min_members": 3,
                "max_members": 12,
                "formation_requirements": ["shared_beliefs", "spiritual_leader"],
                "typical_goals": ["spiritual_growth", "ritual_practice", "belief_spread"]
            }
        }
    
    def _initialize_institution_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize templates for cultural institutions."""
        return {
            "school": {
                "purpose": "Education and knowledge transmission",
                "required_skills": ["teaching", "research"],
                "knowledge_domains": ["history", "skills", "traditions"],
                "capacity": 15
            },
            "temple": {
                "purpose": "Spiritual guidance and ritual practice",
                "required_skills": ["spirituality", "leadership"],
                "knowledge_domains": ["beliefs", "rituals", "meditation"],
                "capacity": 20
            },
            "library": {
                "purpose": "Knowledge preservation and research",
                "required_skills": ["research", "storytelling"],
                "knowledge_domains": ["history", "stories", "innovations"],
                "capacity": 10
            },
            "workshop": {
                "purpose": "Skill development and crafting",
                "required_skills": ["toolmaking", "teaching"],
                "knowledge_domains": ["crafting", "techniques", "innovations"],
                "capacity": 12
            },
            "council_hall": {
                "purpose": "Governance and decision making",
                "required_skills": ["leadership", "negotiation"],
                "knowledge_domains": ["law", "politics", "history"],
                "capacity": 8
            },
            "healing_center": {
                "purpose": "Health and wellness services",
                "required_skills": ["medicine", "foraging"],
                "knowledge_domains": ["medicine", "herbs", "healing"],
                "capacity": 18
            },
            "market": {
                "purpose": "Trade and economic activity",
                "required_skills": ["negotiation", "organization"],
                "knowledge_domains": ["trade", "economics", "resources"],
                "capacity": 25
            }
        }
    
    def process_daily_group_activities(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process all group-related activities for a day."""
        events = []
        
        # 1. Check for new group formation opportunities
        formation_events = self._check_group_formation(agents, current_day)
        events.extend(formation_events)
        
        # 2. Process existing group activities and maintenance
        maintenance_events = self._process_group_maintenance(agents, current_day)
        events.extend(maintenance_events)
        
        # 3. Check for alliance opportunities and tensions
        alliance_events = self._process_alliance_dynamics(current_day)
        events.extend(alliance_events)
        
        # 4. Process cultural institution activities
        institution_events = self._process_institution_activities(agents, current_day)
        events.extend(institution_events)
        
        # 5. Update collective memories
        memory_events = self._update_collective_memories(agents, current_day)
        events.extend(memory_events)
        
        # 6. Handle group conflicts and dissolution
        conflict_events = self._handle_group_conflicts(agents, current_day)
        events.extend(conflict_events)
        
        return events
    
    def _check_group_formation(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Check if conditions are right for new group formation."""
        events = []
        
        # Check each group type for formation opportunities
        for group_type in GroupType:
            if random.random() < 0.08:  # 8% daily chance per group type
                event = self._attempt_group_formation(agents, group_type, current_day)
                if event:
                    events.append(event)
        
        return events
    
    def _attempt_group_formation(self, agents: List[Any], group_type: GroupType, 
                                current_day: int) -> Optional[Dict[str, Any]]:
        """Attempt to form a new group of the specified type."""
        template = self.group_templates[group_type]
        
        # Find potential founding members
        eligible_agents = self._find_eligible_agents(agents, group_type, template)
        
        if len(eligible_agents) < template["min_members"]:
            return None
        
        # Select founding members
        num_founders = min(random.randint(template["min_members"], template["min_members"] + 2),
                          len(eligible_agents))
        founders = random.sample(eligible_agents, num_founders)
        
        # Create the group
        group_name = self._generate_group_name(group_type, founders)
        leader = self._select_group_leader(founders, group_type)
        
        group_data = {
            "name": group_name,
            "type": group_type.value,
            "status": GroupStatus.FORMING.value,
            "founded_day": current_day,
            "leader": leader.name,
            "members": {member.name: GroupMember(
                name=member.name,
                role="founder" if member == leader else "member",
                joined_day=current_day,
                loyalty=random.uniform(0.7, 0.9),
                contribution=random.uniform(0.6, 0.8),
                influence=0.8 if member == leader else random.uniform(0.3, 0.6)
            ) for member in founders},
            "goals": random.sample(template["typical_goals"], 
                                 random.randint(1, len(template["typical_goals"]))),
            "resources": {},
            "territory": [leader.location],
            "influence": 0.3,
            "reputation": 0.5
        }
        
        self.groups[group_name] = group_data
        
        # Update agent memberships
        for member in founders:
            if not hasattr(member, 'group_memberships'):
                member.group_memberships = []
            member.group_memberships.append(group_name)
            
            # Add memory
            member.memory.store_memory(
                f"Helped found {group_name}, a {group_type.value} focused on {', '.join(group_data['goals'])}",
                importance=0.8,
                memory_type="experience"
            )
        
        # Initialize collective memory
        self._initialize_collective_memory(group_name, founders, group_type, current_day)
        
        return {
            "type": "group_formation",
            "group_type": group_type.value,
            "group_name": group_name,
            "leader": leader.name,
            "founders": [f.name for f in founders],
            "goals": group_data["goals"],
            "day": current_day
        }
    
    def _find_eligible_agents(self, agents: List[Any], group_type: GroupType, 
                            template: Dict[str, Any]) -> List[Any]:
        """Find agents eligible to form a group of the specified type."""
        eligible = []
        
        for agent in agents:
            if not agent.is_alive:
                continue
                
            # Check if agent is already in too many groups
            if hasattr(agent, 'group_memberships') and len(agent.group_memberships) >= 3:
                continue
            
            # Type-specific eligibility checks
            if group_type == GroupType.FACTION:
                if ("ambitious" in agent.traits or "charismatic" in agent.traits or 
                    agent.personality_scores.get("extraversion", 0.5) > 0.6):
                    eligible.append(agent)
            
            elif group_type == GroupType.GUILD:
                if (hasattr(agent, 'specialization') and agent.specialization or
                    any(skill.get_effective_level() > 2.0 for skill in 
                        getattr(agent, 'advanced_skills', {}).values() if hasattr(skill, 'get_effective_level'))):
                    eligible.append(agent)
            
            elif group_type == GroupType.INSTITUTION:
                if (("wise" in agent.traits or "intelligent" in agent.traits) and
                    agent.personality_scores.get("openness", 0.5) > 0.6):
                    eligible.append(agent)
            
            elif group_type == GroupType.COUNCIL:
                if (("diplomatic" in agent.traits or "wise" in agent.traits) and
                    agent.reputation > 0.6):
                    eligible.append(agent)
            
            elif group_type == GroupType.CLAN:
                if len(agent.family) > 1:  # Has family connections
                    eligible.append(agent)
            
            elif group_type == GroupType.SECT:
                if ("spiritual" in agent.traits or "wise" in agent.traits):
                    eligible.append(agent)
            
            else:  # Default case
                eligible.append(agent)
        
        return eligible
    
    def _generate_group_name(self, group_type: GroupType, founders: List[Any]) -> str:
        """Generate a name for the new group."""
        leader = founders[0]  # Assume first founder is leader
        
        if group_type == GroupType.FACTION:
            prefixes = ["The", "Order of", "Circle of", "Brotherhood of", "Alliance of"]
            suffixes = ["Unity", "Progress", "Wisdom", "Power", "Truth", "Freedom"]
            return f"{random.choice(prefixes)} {random.choice(suffixes)}"
        
        elif group_type == GroupType.GUILD:
            crafts = ["Artisans", "Craftsmen", "Builders", "Traders", "Makers", "Workers"]
            return f"{random.choice(crafts)} Guild"
        
        elif group_type == GroupType.INSTITUTION:
            types = ["Academy", "Institute", "Center", "Hall", "House"]
            purposes = ["Learning", "Knowledge", "Wisdom", "Skills", "Arts"]
            return f"{random.choice(purposes)} {random.choice(types)}"
        
        elif group_type == GroupType.COUNCIL:
            return f"{leader.location.title()} Council"
        
        elif group_type == GroupType.CLAN:
            return f"Clan {leader.name}"
        
        elif group_type == GroupType.SECT:
            elements = ["Light", "Truth", "Path", "Way", "Circle", "Dawn"]
            return f"Seekers of {random.choice(elements)}"
        
        else:
            return f"{leader.name}'s Group"
    
    def _select_group_leader(self, candidates: List[Any], group_type: GroupType) -> Any:
        """Select the most suitable leader from candidates."""
        scored_candidates = []
        
        for candidate in candidates:
            score = 0.0
            
            # Base leadership potential
            score += candidate.personality_scores.get("extraversion", 0.5) * 0.3
            score += candidate.personality_scores.get("conscientiousness", 0.5) * 0.2
            score += candidate.reputation * 0.2
            
            # Trait bonuses
            if "charismatic" in candidate.traits:
                score += 0.15
            if "ambitious" in candidate.traits:
                score += 0.1
            if "wise" in candidate.traits:
                score += 0.1
            if "diplomatic" in candidate.traits:
                score += 0.1
            
            # Type-specific bonuses
            if group_type == GroupType.GUILD and hasattr(candidate, 'specialization'):
                score += 0.15
            elif group_type == GroupType.INSTITUTION and "intelligent" in candidate.traits:
                score += 0.15
            elif group_type == GroupType.COUNCIL and "diplomatic" in candidate.traits:
                score += 0.15
            
            scored_candidates.append((candidate, score))
        
        # Select leader (highest score with some randomness)
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        top_candidates = scored_candidates[:min(3, len(scored_candidates))]
        
        # Weighted random selection from top candidates
        weights = [score for _, score in top_candidates]
        total_weight = sum(weights)
        
        if total_weight > 0:
            r = random.uniform(0, total_weight)
            cumulative = 0
            for candidate, weight in top_candidates:
                cumulative += weight
                if r <= cumulative:
                    return candidate
        
        return scored_candidates[0][0]  # Fallback to highest scored
    
    def _initialize_collective_memory(self, group_name: str, founders: List[Any], 
                                    group_type: GroupType, current_day: int):
        """Initialize collective memory for a new group."""
        # Gather shared knowledge from founders
        shared_knowledge = {}
        cultural_artifacts = []
        
        for founder in founders:
            # Extract relevant knowledge based on group type
            if hasattr(founder, 'advanced_skills'):
                for skill_name, skill in founder.advanced_skills.items():
                    if skill.get_effective_level() > 2.0:
                        shared_knowledge[skill_name] = skill.get_effective_level()
            
            # Add cultural artifacts they possess
            if hasattr(founder, 'cultural_artifacts'):
                cultural_artifacts.extend(founder.cultural_artifacts)
        
        # Initialize collective memory
        collective_memory = CollectiveMemory(
            group_name=group_name,
            shared_knowledge=shared_knowledge,
            cultural_artifacts=list(set(cultural_artifacts)),
            traditions=[],
            myths_and_stories=[f"Foundation of {group_name} on day {current_day}"],
            values=self._determine_group_values(founders, group_type),
            taboos=[],
            historical_events=[{
                "day": current_day,
                "event": "group_founded",
                "description": f"{group_name} was founded by {', '.join([f.name for f in founders])}"
            }]
        )
        
        self.collective_memories[group_name] = collective_memory
    
    def _determine_group_values(self, founders: List[Any], group_type: GroupType) -> List[str]:
        """Determine the core values of a group based on its founders and type."""
        trait_counts = {}
        for founder in founders:
            for trait in founder.traits:
                trait_counts[trait] = trait_counts.get(trait, 0) + 1
        
        # Select most common traits as values
        common_traits = sorted(trait_counts.items(), key=lambda x: x[1], reverse=True)
        values = [trait for trait, count in common_traits[:3]]
        
        # Add type-specific values
        type_values = {
            GroupType.FACTION: ["loyalty", "unity", "progress"],
            GroupType.GUILD: ["craftsmanship", "cooperation", "quality"],
            GroupType.INSTITUTION: ["knowledge", "learning", "wisdom"],
            GroupType.COUNCIL: ["justice", "fairness", "order"],
            GroupType.CLAN: ["family", "tradition", "protection"],
            GroupType.SECT: ["spirituality", "truth", "enlightenment"]
        }
        
        if group_type in type_values:
            values.extend(type_values[group_type][:2])
        
        return list(set(values))[:5]  # Maximum 5 values
    
    def _process_group_maintenance(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process daily maintenance activities for existing groups."""
        events = []
        
        for group_name, group_data in self.groups.items():
            if group_data["status"] == GroupStatus.DISBANDED.value:
                continue
            
            # Update group stability and growth
            maintenance_event = self._update_group_status(group_name, group_data, agents, current_day)
            if maintenance_event:
                events.append(maintenance_event)
            
            # Handle member recruitment
            recruitment_event = self._handle_member_recruitment(group_name, group_data, agents, current_day)
            if recruitment_event:
                events.append(recruitment_event)
            
            # Process group projects and activities
            activity_event = self._process_group_activities(group_name, group_data, agents, current_day)
            if activity_event:
                events.append(activity_event)
        
        return events
    
    def _update_group_status(self, group_name: str, group_data: Dict[str, Any], 
                           agents: List[Any], current_day: int) -> Optional[Dict[str, Any]]:
        """Update the status and stability of a group."""
        active_members = []
        total_loyalty = 0.0
        total_contribution = 0.0
        
        # Check member activity and loyalty
        for member_name, member_data in group_data["members"].items():
            # Find the actual agent
            agent = next((a for a in agents if a.name == member_name), None)
            if agent and agent.is_alive:
                active_members.append(member_name)
                total_loyalty += member_data.loyalty
                total_contribution += member_data.contribution
                
                # Update loyalty based on recent activities
                if random.random() < 0.1:  # 10% chance for loyalty change
                    loyalty_change = random.uniform(-0.05, 0.05)
                    member_data.loyalty = max(0.0, min(1.0, member_data.loyalty + loyalty_change))
        
        if not active_members:
            # Group disbanded due to no active members
            group_data["status"] = GroupStatus.DISBANDED.value
            return {
                "type": "group_disbanded",
                "group_name": group_name,
                "reason": "no_active_members",
                "day": current_day
            }
        
        # Calculate group health metrics
        avg_loyalty = total_loyalty / len(active_members) if active_members else 0
        avg_contribution = total_contribution / len(active_members) if active_members else 0
        
        # Update group influence based on size, loyalty, and age
        size_factor = min(len(active_members) / 10.0, 1.0)  # Bonus for larger groups
        loyalty_factor = avg_loyalty
        age_factor = min((current_day - group_data["founded_day"]) / 100.0, 1.0)  # Bonus for older groups
        
        new_influence = (size_factor * 0.4 + loyalty_factor * 0.4 + age_factor * 0.2)
        group_data["influence"] = (group_data["influence"] + new_influence) / 2  # Smooth update
        
        # Determine new status
        old_status = group_data["status"]
        if avg_loyalty < 0.3:
            group_data["status"] = GroupStatus.DECLINING.value
        elif group_data["influence"] > 0.8:
            group_data["status"] = GroupStatus.DOMINANT.value
        elif group_data["influence"] > 0.6:
            group_data["status"] = GroupStatus.INFLUENTIAL.value
        elif avg_loyalty > 0.7 and (current_day - group_data["founded_day"]) > 30:
            group_data["status"] = GroupStatus.STABLE.value
        else:
            group_data["status"] = GroupStatus.FORMING.value
        
        if old_status != group_data["status"]:
            return {
                "type": "group_status_change",
                "group_name": group_name,
                "old_status": old_status,
                "new_status": group_data["status"],
                "influence": group_data["influence"],
                "day": current_day
            }
        
        return None
    
    def _handle_member_recruitment(self, group_name: str, group_data: Dict[str, Any], 
                                 agents: List[Any], current_day: int) -> Optional[Dict[str, Any]]:
        """Handle recruitment of new members to the group."""
        # Only recruit if group is stable and not too large
        if (group_data["status"] not in [GroupStatus.STABLE.value, GroupStatus.INFLUENTIAL.value] or
            len(group_data["members"]) >= 15):
            return None
        
        # Small chance for recruitment each day
        if random.random() > 0.15:
            return None
        
        # Find potential recruits
        potential_recruits = []
        for agent in agents:
            if (agent.is_alive and 
                agent.name not in group_data["members"] and
                not hasattr(agent, 'group_memberships') or len(agent.group_memberships) < 3):
                
                # Check compatibility with group
                compatibility = self._calculate_group_compatibility(agent, group_data)
                if compatibility > 0.6:
                    potential_recruits.append((agent, compatibility))
        
        if not potential_recruits:
            return None
        
        # Select recruit based on compatibility
        potential_recruits.sort(key=lambda x: x[1], reverse=True)
        recruit, compatibility = potential_recruits[0]
        
        # Add to group
        group_data["members"][recruit.name] = GroupMember(
            name=recruit.name,
            role="member",
            joined_day=current_day,
            loyalty=random.uniform(0.5, 0.8),
            contribution=random.uniform(0.4, 0.7),
            influence=random.uniform(0.1, 0.3)
        )
        
        # Update agent
        if not hasattr(recruit, 'group_memberships'):
            recruit.group_memberships = []
        recruit.group_memberships.append(group_name)
        
        recruit.memory.store_memory(
            f"Joined {group_name} as a new member, attracted by their values and goals",
            importance=0.7,
            memory_type="experience"
        )
        
        return {
            "type": "member_recruitment",
            "group_name": group_name,
            "new_member": recruit.name,
            "compatibility": compatibility,
            "day": current_day
        }
    
    def _calculate_group_compatibility(self, agent: Any, group_data: Dict[str, Any]) -> float:
        """Calculate how compatible an agent is with a group."""
        compatibility = 0.0
        
        # Check if in collective memory
        if group_data["name"] in self.collective_memories:
            collective_memory = self.collective_memories[group_data["name"]]
            
            # Value alignment
            shared_values = 0
            for value in collective_memory.values:
                if value in agent.traits:
                    shared_values += 1
            
            if collective_memory.values:
                compatibility += (shared_values / len(collective_memory.values)) * 0.4
            
            # Skill compatibility
            if hasattr(agent, 'advanced_skills'):
                shared_skills = 0
                for skill_name in collective_memory.shared_knowledge:
                    if skill_name in agent.advanced_skills:
                        shared_skills += 1
                
                if collective_memory.shared_knowledge:
                    compatibility += (shared_skills / len(collective_memory.shared_knowledge)) * 0.3
        
        # Location compatibility
        if agent.location in group_data.get("territory", []):
            compatibility += 0.2
        
        # Reputation factor
        compatibility += agent.reputation * 0.1
        
        return min(compatibility, 1.0)
    
    def _process_group_activities(self, group_name: str, group_data: Dict[str, Any], 
                                agents: List[Any], current_day: int) -> Optional[Dict[str, Any]]:
        """Process daily activities and projects for the group."""
        if random.random() > 0.2:  # 20% chance for activity each day
            return None
        
        # Select activity type based on group type
        group_type = group_data["type"]
        activity_types = {
            "faction": ["political_meeting", "influence_campaign", "territory_expansion"],
            "guild": ["skill_workshop", "trade_negotiation", "quality_improvement"],
            "institution": ["knowledge_session", "research_project", "cultural_preservation"],
            "council": ["governance_meeting", "dispute_resolution", "policy_making"],
            "clan": ["family_gathering", "tradition_ceremony", "resource_sharing"],
            "sect": ["spiritual_gathering", "ritual_practice", "enlightenment_session"]
        }
        
        possible_activities = activity_types.get(group_type, ["general_meeting"])
        activity_type = random.choice(possible_activities)
        
        # Get participating members
        active_members = []
        for member_name in group_data["members"]:
            agent = next((a for a in agents if a.name == member_name), None)
            if agent and agent.is_alive and random.random() < 0.7:  # 70% participation
                active_members.append(agent)
        
        if len(active_members) < 2:
            return None
        
        # Process the activity
        activity_result = self._execute_group_activity(group_name, activity_type, active_members, current_day)
        
        # Add memories to participants
        for member in active_members:
            member.memory.store_memory(
                f"Participated in {activity_type.replace('_', ' ')} with {group_name}",
                importance=0.5,
                memory_type="experience"
            )
        
        return {
            "type": "group_activity",
            "group_name": group_name,
            "activity_type": activity_type,
            "participants": [m.name for m in active_members],
            "result": activity_result,
            "day": current_day
        }
    
    def _execute_group_activity(self, group_name: str, activity_type: str, 
                              participants: List[Any], current_day: int) -> Dict[str, Any]:
        """Execute a specific group activity and return results."""
        result = {"success": True, "effects": []}
        
        if activity_type in ["political_meeting", "governance_meeting"]:
            # Increase group influence and member loyalty
            group_data = self.groups[group_name]
            group_data["influence"] = min(1.0, group_data["influence"] + 0.02)
            
            for participant in participants:
                member_data = group_data["members"][participant.name]
                member_data.loyalty = min(1.0, member_data.loyalty + 0.05)
            
            result["effects"].append("increased_influence")
            result["effects"].append("increased_loyalty")
        
        elif activity_type in ["skill_workshop", "knowledge_session"]:
            # Improve participant skills
            for participant in participants:
                if hasattr(participant, 'advanced_skills'):
                    skill_names = list(participant.advanced_skills.keys())
                    if skill_names:
                        skill_name = random.choice(skill_names)
                        skill = participant.advanced_skills[skill_name]
                        skill.experience += random.uniform(0.1, 0.3)
            
            result["effects"].append("skill_improvement")
        
        elif activity_type in ["trade_negotiation"]:
            # Improve group resources
            group_data = self.groups[group_name]
            if "resources" not in group_data:
                group_data["resources"] = {}
            
            resource_types = ["materials", "food", "knowledge", "influence"]
            resource = random.choice(resource_types)
            group_data["resources"][resource] = group_data["resources"].get(resource, 0) + random.uniform(0.1, 0.3)
            
            result["effects"].append(f"gained_{resource}")
        
        elif activity_type in ["tradition_ceremony", "ritual_practice"]:
            # Strengthen cultural bonds
            if group_name in self.collective_memories:
                collective_memory = self.collective_memories[group_name]
                
                # Chance to develop new tradition
                if random.random() < 0.3:
                    new_tradition = f"{activity_type.replace('_', ' ')} of {group_name}"
                    collective_memory.traditions.append(new_tradition)
                    result["effects"].append("new_tradition_formed")
            
            # Increase loyalty
            group_data = self.groups[group_name]
            for participant in participants:
                member_data = group_data["members"][participant.name]
                member_data.loyalty = min(1.0, member_data.loyalty + 0.08)
            
            result["effects"].append("strengthened_bonds")
        
        return result
    
    def _process_alliance_dynamics(self, current_day: int) -> List[Dict[str, Any]]:
        """Process alliance formation, maintenance, and dissolution."""
        events = []
        
        # Check for new alliance opportunities
        if random.random() < 0.05:  # 5% chance per day
            alliance_event = self._attempt_alliance_formation(current_day)
            if alliance_event:
                events.append(alliance_event)
        
        # Process existing alliances
        for alliance_id, alliance in list(self.alliances.items()):
            # Check alliance stability
            stability_event = self._update_alliance_stability(alliance_id, alliance, current_day)
            if stability_event:
                events.append(stability_event)
            
            # Check for duration expiry
            if alliance.duration and (current_day - alliance.formed_day) >= alliance.duration:
                dissolution_event = self._dissolve_alliance(alliance_id, alliance, "expired", current_day)
                events.append(dissolution_event)
        
        return events
    
    def _attempt_alliance_formation(self, current_day: int) -> Optional[Dict[str, Any]]:
        """Attempt to form a new alliance between compatible groups."""
        active_groups = [(name, data) for name, data in self.groups.items() 
                        if data["status"] not in [GroupStatus.DISBANDED.value, GroupStatus.DECLINING.value]]
        
        if len(active_groups) < 2:
            return None
        
        # Find compatible groups
        for i, (group1_name, group1_data) in enumerate(active_groups):
            for group2_name, group2_data in active_groups[i+1:]:
                # Check if they're already allied
                existing_alliance = any(
                    (alliance.group1 == group1_name and alliance.group2 == group2_name) or
                    (alliance.group1 == group2_name and alliance.group2 == group1_name)
                    for alliance in self.alliances.values()
                )
                
                if existing_alliance:
                    continue
                
                # Calculate compatibility
                compatibility = self._calculate_alliance_compatibility(group1_data, group2_data)
                
                if compatibility > 0.7 and random.random() < 0.3:  # 30% chance if compatible
                    # Form alliance
                    alliance_type = self._determine_alliance_type(group1_data, group2_data)
                    
                    alliance_id = f"{group1_name}_{group2_name}_{alliance_type.value}"
                    alliance = GroupAlliance(
                        group1=group1_name,
                        group2=group2_name,
                        alliance_type=alliance_type,
                        formed_day=current_day,
                        strength=compatibility,
                        terms=self._generate_alliance_terms(alliance_type)
                    )
                    
                    self.alliances[alliance_id] = alliance
                    
                    return {
                        "type": "alliance_formed",
                        "alliance_type": alliance_type.value,
                        "group1": group1_name,
                        "group2": group2_name,
                        "strength": compatibility,
                        "terms": alliance.terms,
                        "day": current_day
                    }
        
        return None
    
    def _calculate_alliance_compatibility(self, group1_data: Dict[str, Any], 
                                        group2_data: Dict[str, Any]) -> float:
        """Calculate compatibility between two groups for alliance formation."""
        compatibility = 0.0
        
        # Goal alignment
        shared_goals = set(group1_data["goals"]) & set(group2_data["goals"])
        total_goals = set(group1_data["goals"]) | set(group2_data["goals"])
        if total_goals:
            compatibility += (len(shared_goals) / len(total_goals)) * 0.3
        
        # Territory proximity
        shared_territory = set(group1_data.get("territory", [])) & set(group2_data.get("territory", []))
        if shared_territory:
            compatibility += 0.2
        
        # Status compatibility (similar status groups work better together)
        status_values = {
            GroupStatus.FORMING.value: 1,
            GroupStatus.STABLE.value: 2,
            GroupStatus.INFLUENTIAL.value: 3,
            GroupStatus.DOMINANT.value: 4,
            GroupStatus.DECLINING.value: 0
        }
        
        status1 = status_values.get(group1_data["status"], 1)
        status2 = status_values.get(group2_data["status"], 1)
        status_diff = abs(status1 - status2)
        compatibility += max(0, (4 - status_diff) / 4) * 0.2
        
        # Size balance
        size1 = len(group1_data["members"])
        size2 = len(group2_data["members"])
        size_ratio = min(size1, size2) / max(size1, size2) if max(size1, size2) > 0 else 1
        compatibility += size_ratio * 0.1
        
        # Influence factors
        avg_influence = (group1_data["influence"] + group2_data["influence"]) / 2
        compatibility += avg_influence * 0.2
        
        return min(compatibility, 1.0)
    
    def _determine_alliance_type(self, group1_data: Dict[str, Any], 
                               group2_data: Dict[str, Any]) -> AllianceType:
        """Determine the most appropriate alliance type for two groups."""
        # Base on group types and goals
        type1 = group1_data["type"]
        type2 = group2_data["type"]
        
        if "guild" in [type1, type2]:
            return AllianceType.TRADE_PARTNERSHIP
        elif "faction" in [type1, type2]:
            return AllianceType.POLITICAL_COALITION
        elif "institution" in [type1, type2]:
            return AllianceType.CULTURAL_EXCHANGE
        elif "council" in [type1, type2]:
            return AllianceType.MUTUAL_DEFENSE
        else:
            # Random selection from appropriate types
            return random.choice([
                AllianceType.TRADE_PARTNERSHIP,
                AllianceType.CULTURAL_EXCHANGE,
                AllianceType.RESOURCE_SHARING,
                AllianceType.NON_AGGRESSION
            ])
    
    def _generate_alliance_terms(self, alliance_type: AllianceType) -> List[str]:
        """Generate specific terms for an alliance."""
        terms = []
        
        if alliance_type == AllianceType.TRADE_PARTNERSHIP:
            terms = [
                "Preferential trading agreements",
                "Shared market access",
                "Joint resource ventures"
            ]
        elif alliance_type == AllianceType.MUTUAL_DEFENSE:
            terms = [
                "Military support in conflicts",
                "Shared intelligence",
                "Coordinated defense strategies"
            ]
        elif alliance_type == AllianceType.CULTURAL_EXCHANGE:
            terms = [
                "Knowledge sharing programs",
                "Cultural event participation",
                "Educational exchanges"
            ]
        elif alliance_type == AllianceType.POLITICAL_COALITION:
            terms = [
                "Coordinated political actions",
                "Shared governance decisions",
                "Joint policy development"
            ]
        elif alliance_type == AllianceType.RESOURCE_SHARING:
            terms = [
                "Shared access to resources",
                "Coordinated resource management",
                "Emergency resource assistance"
            ]
        else:  # NON_AGGRESSION
            terms = [
                "No hostile actions",
                "Peaceful dispute resolution",
                "Neutral territory respect"
            ]
        
        return terms[:random.randint(2, 3)]  # 2-3 terms per alliance
    
    def _update_alliance_stability(self, alliance_id: str, alliance: GroupAlliance, 
                                 current_day: int) -> Optional[Dict[str, Any]]:
        """Update the stability of an existing alliance."""
        # Check if both groups still exist and are active
        group1_data = self.groups.get(alliance.group1)
        group2_data = self.groups.get(alliance.group2)
        
        if (not group1_data or not group2_data or
            group1_data["status"] == GroupStatus.DISBANDED.value or
            group2_data["status"] == GroupStatus.DISBANDED.value):
            
            return self._dissolve_alliance(alliance_id, alliance, "group_disbanded", current_day)
        
        # Calculate current compatibility
        current_compatibility = self._calculate_alliance_compatibility(group1_data, group2_data)
        
        # Update alliance strength (moving average)
        alliance.strength = (alliance.strength + current_compatibility) / 2
        
        # Check for alliance breakdown
        if alliance.strength < 0.3:
            return self._dissolve_alliance(alliance_id, alliance, "incompatibility", current_day)
        
        # Check for violations (simplified - could be much more complex)
        if random.random() < 0.02:  # 2% chance of violation per day
            alliance.violations += 1
            
            if alliance.violations >= 3:
                return self._dissolve_alliance(alliance_id, alliance, "repeated_violations", current_day)
            
            return {
                "type": "alliance_violation",
                "alliance_id": alliance_id,
                "group1": alliance.group1,
                "group2": alliance.group2,
                "violations": alliance.violations,
                "day": current_day
            }
        
        return None
    
    def _dissolve_alliance(self, alliance_id: str, alliance: GroupAlliance, 
                         reason: str, current_day: int) -> Dict[str, Any]:
        """Dissolve an alliance."""
        del self.alliances[alliance_id]
        
        return {
            "type": "alliance_dissolved",
            "alliance_id": alliance_id,
            "group1": alliance.group1,
            "group2": alliance.group2,
            "reason": reason,
            "duration": current_day - alliance.formed_day,
            "day": current_day
        }
    
    def _process_institution_activities(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Process activities for cultural institutions."""
        events = []
        
        # Check for new institution formation
        if random.random() < 0.03:  # 3% chance per day
            institution_event = self._attempt_institution_formation(agents, current_day)
            if institution_event:
                events.append(institution_event)
        
        # Process existing institutions
        for institution_name, institution in self.institutions.items():
            activity_event = self._process_institution_activity(institution, agents, current_day)
            if activity_event:
                events.append(activity_event)
        
        return events
    
    def _attempt_institution_formation(self, agents: List[Any], current_day: int) -> Optional[Dict[str, Any]]:
        """Attempt to form a new cultural institution."""
        # Choose institution type based on community needs
        institution_types = list(self.institution_templates.keys())
        institution_type = random.choice(institution_types)
        template = self.institution_templates[institution_type]
        
        # Find suitable founders
        founders = []
        for agent in agents:
            if not agent.is_alive:
                continue
            
            # Check if agent has required skills
            has_skills = False
            if hasattr(agent, 'advanced_skills'):
                for required_skill in template["required_skills"]:
                    if (required_skill in agent.advanced_skills and
                        agent.advanced_skills[required_skill].get_effective_level() > 2.0):
                        has_skills = True
                        break
            
            if has_skills and agent.reputation > 0.6:
                founders.append(agent)
        
        if len(founders) < 2:
            return None
        
        # Select best founders
        founders.sort(key=lambda x: x.reputation, reverse=True)
        selected_founders = founders[:min(3, len(founders))]
        
        # Create institution
        leader = selected_founders[0]
        institution_name = f"{leader.location.title()} {institution_type.title()}"
        
        institution = CulturalInstitution(
            name=institution_name,
            institution_type=institution_type,
            purpose=template["purpose"],
            founded_day=current_day,
            location=leader.location,
            leaders=[f.name for f in selected_founders],
            members=[],
            resources={},
            knowledge_domains=template["knowledge_domains"].copy(),
            influence=0.3,
            capacity=template["capacity"]
        )
        
        self.institutions[institution_name] = institution
        
        # Add memories to founders
        for founder in selected_founders:
            founder.memory.store_memory(
                f"Helped establish {institution_name}, a {institution_type} dedicated to {template['purpose']}",
                importance=0.8,
                memory_type="experience"
            )
        
        return {
            "type": "institution_founded",
            "institution_name": institution_name,
            "institution_type": institution_type,
            "founders": [f.name for f in selected_founders],
            "location": leader.location,
            "purpose": template["purpose"],
            "day": current_day
        }
    
    def _process_institution_activity(self, institution: CulturalInstitution, 
                                    agents: List[Any], current_day: int) -> Optional[Dict[str, Any]]:
        """Process daily activities for a cultural institution."""
        if random.random() > 0.25:  # 25% chance for activity
            return None
        
        # Find participating agents
        participants = []
        
        # Leaders participate more often
        for leader_name in institution.leaders:
            leader = next((a for a in agents if a.name == leader_name), None)
            if leader and leader.is_alive and random.random() < 0.8:
                participants.append(leader)
        
        # Members participate
        for member_name in institution.members:
            member = next((a for a in agents if a.name == member_name), None)
            if member and member.is_alive and random.random() < 0.6:
                participants.append(member)
        
        # Non-members may visit
        for agent in agents:
            if (agent.is_alive and agent.location == institution.location and
                agent.name not in institution.leaders and agent.name not in institution.members and
                len(participants) < institution.capacity and random.random() < 0.2):
                participants.append(agent)
                
                # Chance to become member
                if len(institution.members) < institution.capacity and random.random() < 0.3:
                    institution.members.append(agent.name)
        
        if len(participants) < 2:
            return None
        
        # Determine activity type
        activity_types = {
            "school": ["knowledge_session", "skill_teaching", "research_project"],
            "temple": ["spiritual_gathering", "ceremony", "meditation_session"],
            "library": ["research", "knowledge_preservation", "storytelling"],
            "workshop": ["skill_workshop", "tool_creation", "technique_sharing"],
            "council_hall": ["governance_meeting", "dispute_resolution", "policy_discussion"],
            "healing_center": ["healing_session", "medicine_preparation", "health_education"],
            "market": ["trade_fair", "resource_exchange", "economic_planning"]
        }
        
        possible_activities = activity_types.get(institution.institution_type, ["general_gathering"])
        activity_type = random.choice(possible_activities)
        
        # Execute activity
        results = self._execute_institution_activity(institution, activity_type, participants, current_day)
        
        # Add memories
        for participant in participants:
            participant.memory.store_memory(
                f"Participated in {activity_type.replace('_', ' ')} at {institution.name}",
                importance=0.6,
                memory_type="experience"
            )
        
        return {
            "type": "institution_activity",
            "institution_name": institution.name,
            "institution_type": institution.institution_type,
            "activity_type": activity_type,
            "participants": [p.name for p in participants],
            "results": results,
            "day": current_day
        }
    
    def _execute_institution_activity(self, institution: CulturalInstitution, activity_type: str,
                                    participants: List[Any], current_day: int) -> Dict[str, Any]:
        """Execute a specific institution activity."""
        results = {"effects": []}
        
        if activity_type in ["knowledge_session", "research_project", "storytelling"]:
            # Knowledge sharing and preservation
            for participant in participants:
                if hasattr(participant, 'advanced_skills'):
                    # Skill improvement
                    for skill_name, skill in participant.advanced_skills.items():
                        if skill_name in institution.knowledge_domains:
                            skill.experience += random.uniform(0.05, 0.15)
            
            # Increase institution influence
            institution.influence = min(1.0, institution.influence + 0.01)
            results["effects"].append("knowledge_shared")
            results["effects"].append("skills_improved")
        
        elif activity_type in ["skill_teaching", "skill_workshop"]:
            # Focused skill development
            for participant in participants:
                if hasattr(participant, 'advanced_skills'):
                    # Higher skill gains for institutional learning
                    relevant_skills = [s for s in participant.advanced_skills 
                                     if any(domain in s for domain in institution.knowledge_domains)]
                    if relevant_skills:
                        skill_name = random.choice(relevant_skills)
                        skill = participant.advanced_skills[skill_name]
                        skill.experience += random.uniform(0.1, 0.25)
            
            results["effects"].append("intensive_skill_training")
        
        elif activity_type in ["spiritual_gathering", "ceremony", "meditation_session"]:
            # Spiritual and community bonding
            for participant in participants:
                # Improve emotional state and community bonds
                participant.emotion_intensity = max(0.0, participant.emotion_intensity - 0.1)
                participant.life_satisfaction = min(1.0, participant.life_satisfaction + 0.05)
                
                # Strengthen relationships
                for other_participant in participants:
                    if other_participant != participant:
                        current_relationship = participant.relationships.get(other_participant.name, "stranger")
                        if current_relationship in ["stranger", "acquaintance"]:
                            participant.relationships[other_participant.name] = "friend"
            
            results["effects"].append("spiritual_growth")
            results["effects"].append("community_bonding")
        
        elif activity_type in ["trade_fair", "resource_exchange"]:
            # Economic activity
            for participant in participants:
                # Improve economic resources
                if hasattr(participant, 'personal_resources'):
                    resource_types = list(participant.personal_resources.keys())
                    if resource_types:
                        resource = random.choice(resource_types)
                        participant.personal_resources[resource] += random.uniform(0.05, 0.15)
            
            # Improve institution resources
            institution.resources["influence"] = institution.resources.get("influence", 0) + 0.1
            results["effects"].append("economic_growth")
        
        return results
    
    def _update_collective_memories(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Update collective memories for all groups."""
        events = []
        
        for group_name, collective_memory in self.collective_memories.items():
            # Skip if group is disbanded
            if group_name not in self.groups or self.groups[group_name]["status"] == GroupStatus.DISBANDED.value:
                continue
            
            # Update shared knowledge
            knowledge_event = self._update_shared_knowledge(group_name, collective_memory, agents, current_day)
            if knowledge_event:
                events.append(knowledge_event)
            
            # Check for new cultural developments
            culture_event = self._develop_group_culture(group_name, collective_memory, agents, current_day)
            if culture_event:
                events.append(culture_event)
        
        return events
    
    def _update_shared_knowledge(self, group_name: str, collective_memory: CollectiveMemory,
                               agents: List[Any], current_day: int) -> Optional[Dict[str, Any]]:
        """Update the shared knowledge of a group."""
        group_data = self.groups[group_name]
        group_members = []
        
        # Find all group members
        for member_name in group_data["members"]:
            agent = next((a for a in agents if a.name == member_name), None)
            if agent and agent.is_alive:
                group_members.append(agent)
        
        if len(group_members) < 2:
            return None
        
        # Aggregate knowledge from all members
        new_knowledge = {}
        knowledge_contributors = []
        
        for member in group_members:
            if hasattr(member, 'advanced_skills'):
                for skill_name, skill in member.advanced_skills.items():
                    skill_level = skill.get_effective_level()
                    
                    # Only add to group knowledge if skill is sufficiently developed
                    if skill_level > 1.5:
                        if skill_name not in collective_memory.shared_knowledge:
                            new_knowledge[skill_name] = skill_level
                            knowledge_contributors.append(member.name)
                        elif skill_level > collective_memory.shared_knowledge[skill_name]:
                            # Update with higher level
                            collective_memory.shared_knowledge[skill_name] = skill_level
        
        if new_knowledge:
            collective_memory.shared_knowledge.update(new_knowledge)
            
            return {
                "type": "knowledge_shared",
                "group_name": group_name,
                "new_knowledge": list(new_knowledge.keys()),
                "contributors": list(set(knowledge_contributors)),
                "day": current_day
            }
        
        return None
    
    def _develop_group_culture(self, group_name: str, collective_memory: CollectiveMemory,
                             agents: List[Any], current_day: int) -> Optional[Dict[str, Any]]:
        """Develop new cultural elements for a group."""
        if random.random() > 0.1:  # 10% chance per day
            return None
        
        group_data = self.groups[group_name]
        development_type = random.choice(["tradition", "story", "value", "taboo"])
        
        if development_type == "tradition":
            # Develop new tradition based on group activities
            tradition_themes = {
                "faction": ["unity_ritual", "leadership_ceremony", "loyalty_oath"],
                "guild": ["skill_celebration", "craft_blessing", "trade_festival"],
                "institution": ["knowledge_ceremony", "learning_ritual", "wisdom_gathering"],
                "council": ["decision_ritual", "justice_ceremony", "governance_tradition"],
                "clan": ["family_gathering", "ancestor_honor", "kinship_ritual"],
                "sect": ["spiritual_observance", "enlightenment_practice", "sacred_meditation"]
            }
            
            group_type = group_data["type"]
            possible_traditions = tradition_themes.get(group_type, ["group_gathering"])
            new_tradition = random.choice(possible_traditions)
            
            if new_tradition not in collective_memory.traditions:
                collective_memory.traditions.append(new_tradition)
                
                return {
                    "type": "tradition_developed",
                    "group_name": group_name,
                    "tradition": new_tradition,
                    "day": current_day
                }
        
        elif development_type == "story":
            # Create new group story or myth
            group_age = current_day - group_data["founded_day"]
            if group_age > 20:  # Only developed groups create stories
                story_themes = [
                    f"The founding of {group_name}",
                    f"The great challenge of {group_name}",
                    f"The wisdom of {group_data['leader']}",
                    f"The prosperity of {group_name}"
                ]
                
                new_story = random.choice(story_themes)
                if new_story not in collective_memory.myths_and_stories:
                    collective_memory.myths_and_stories.append(new_story)
                    
                    return {
                        "type": "story_created",
                        "group_name": group_name,
                        "story": new_story,
                        "day": current_day
                    }
        
        elif development_type == "value":
            # Develop new group value
            potential_values = ["unity", "progress", "tradition", "innovation", "harmony", 
                              "strength", "wisdom", "prosperity", "justice", "freedom"]
            
            new_values = [v for v in potential_values if v not in collective_memory.values]
            if new_values:
                new_value = random.choice(new_values)
                collective_memory.values.append(new_value)
                
                return {
                    "type": "value_adopted",
                    "group_name": group_name,
                    "value": new_value,
                    "day": current_day
                }
        
        elif development_type == "taboo":
            # Develop new taboo or restriction
            potential_taboos = ["betrayal", "waste", "laziness", "dishonesty", "violence", 
                              "greed", "ignorance", "disrespect", "selfishness"]
            
            new_taboos = [t for t in potential_taboos if t not in collective_memory.taboos]
            if new_taboos:
                new_taboo = random.choice(new_taboos)
                collective_memory.taboos.append(new_taboo)
                
                return {
                    "type": "taboo_established",
                    "group_name": group_name,
                    "taboo": new_taboo,
                    "day": current_day
                }
        
        return None
    
    def _handle_group_conflicts(self, agents: List[Any], current_day: int) -> List[Dict[str, Any]]:
        """Handle conflicts between groups and internal group conflicts."""
        events = []
        
        # Inter-group conflicts
        if random.random() < 0.02:  # 2% chance per day
            conflict_event = self._process_inter_group_conflict(current_day)
            if conflict_event:
                events.append(conflict_event)
        
        # Internal group conflicts
        for group_name, group_data in self.groups.items():
            if group_data["status"] == GroupStatus.DISBANDED.value:
                continue
            
            if random.random() < 0.03:  # 3% chance per group per day
                internal_conflict = self._process_internal_group_conflict(group_name, group_data, agents, current_day)
                if internal_conflict:
                    events.append(internal_conflict)
        
        return events
    
    def _process_inter_group_conflict(self, current_day: int) -> Optional[Dict[str, Any]]:
        """Process conflicts between different groups."""
        active_groups = [(name, data) for name, data in self.groups.items() 
                        if data["status"] not in [GroupStatus.DISBANDED.value]]
        
        if len(active_groups) < 2:
            return None
        
        # Find groups with conflicting interests
        for i, (group1_name, group1_data) in enumerate(active_groups):
            for group2_name, group2_data in active_groups[i+1:]:
                # Check if they have an alliance
                has_alliance = any(
                    (alliance.group1 == group1_name and alliance.group2 == group2_name) or
                    (alliance.group1 == group2_name and alliance.group2 == group1_name)
                    for alliance in self.alliances.values()
                )
                
                if has_alliance:
                    continue  # Allied groups don't conflict directly
                
                # Calculate conflict probability
                conflict_probability = self._calculate_conflict_probability(group1_data, group2_data)
                
                if conflict_probability > 0.6 and random.random() < 0.2:
                    # Conflict occurs
                    conflict_type = self._determine_inter_group_conflict_type(group1_data, group2_data)
                    resolution = self._resolve_inter_group_conflict(group1_data, group2_data, conflict_type)
                    
                    return {
                        "type": "inter_group_conflict",
                        "group1": group1_name,
                        "group2": group2_name,
                        "conflict_type": conflict_type,
                        "resolution": resolution,
                        "day": current_day
                    }
        
        return None
    
    def _calculate_conflict_probability(self, group1_data: Dict[str, Any], 
                                      group2_data: Dict[str, Any]) -> float:
        """Calculate the probability of conflict between two groups."""
        probability = 0.0
        
        # Territory overlap increases conflict
        shared_territory = set(group1_data.get("territory", [])) & set(group2_data.get("territory", []))
        if shared_territory:
            probability += 0.3
        
        # Competing goals increase conflict
        shared_goals = set(group1_data["goals"]) & set(group2_data["goals"])
        if shared_goals:
            probability += 0.2
        
        # Power imbalance can cause conflict
        influence_diff = abs(group1_data["influence"] - group2_data["influence"])
        if influence_diff > 0.4:
            probability += 0.2
        
        # Group types matter
        if group1_data["type"] == "faction" or group2_data["type"] == "faction":
            probability += 0.1  # Factions are more prone to conflict
        
        return min(probability, 1.0)
    
    def _determine_inter_group_conflict_type(self, group1_data: Dict[str, Any], 
                                           group2_data: Dict[str, Any]) -> str:
        """Determine the type of conflict between groups."""
        conflict_types = []
        
        # Territory overlap suggests territorial conflict
        shared_territory = set(group1_data.get("territory", [])) & set(group2_data.get("territory", []))
        if shared_territory:
            conflict_types.append("territorial_dispute")
        
        # Similar goals suggest resource competition
        shared_goals = set(group1_data["goals"]) & set(group2_data["goals"])
        if shared_goals:
            conflict_types.append("resource_competition")
        
        # Different types may have ideological conflicts
        if group1_data["type"] != group2_data["type"]:
            conflict_types.append("ideological_difference")
        
        # Power struggle
        if abs(group1_data["influence"] - group2_data["influence"]) < 0.2:
            conflict_types.append("power_struggle")
        
        return random.choice(conflict_types) if conflict_types else "general_dispute"
    
    def _resolve_inter_group_conflict(self, group1_data: Dict[str, Any], 
                                    group2_data: Dict[str, Any], conflict_type: str) -> Dict[str, Any]:
        """Resolve a conflict between groups."""
        # Simple resolution based on group strength
        group1_strength = group1_data["influence"] * len(group1_data["members"])
        group2_strength = group2_data["influence"] * len(group2_data["members"])
        
        total_strength = group1_strength + group2_strength
        if total_strength > 0:
            group1_win_chance = group1_strength / total_strength
        else:
            group1_win_chance = 0.5
        
        winner = "group1" if random.random() < group1_win_chance else "group2"
        
        resolution = {
            "winner": winner,
            "method": random.choice(["negotiation", "contest", "mediation", "dominance"]),
            "outcome": {}
        }
        
        # Apply outcomes
        if winner == "group1":
            group1_data["influence"] = min(1.0, group1_data["influence"] + 0.05)
            group2_data["influence"] = max(0.0, group2_data["influence"] - 0.03)
            resolution["outcome"]["influence_shift"] = "group1_gains"
        else:
            group2_data["influence"] = min(1.0, group2_data["influence"] + 0.05)
            group1_data["influence"] = max(0.0, group1_data["influence"] - 0.03)
            resolution["outcome"]["influence_shift"] = "group2_gains"
        
        return resolution
    
    def _process_internal_group_conflict(self, group_name: str, group_data: Dict[str, Any],
                                       agents: List[Any], current_day: int) -> Optional[Dict[str, Any]]:
        """Process internal conflicts within a group."""
        # Find group members with low loyalty
        problematic_members = []
        for member_name, member_data in group_data["members"].items():
            if member_data.loyalty < 0.4:
                agent = next((a for a in agents if a.name == member_name), None)
                if agent and agent.is_alive:
                    problematic_members.append((agent, member_data))
        
        if not problematic_members:
            return None
        
        # Select a member to leave or cause problems
        problem_agent, member_data = random.choice(problematic_members)
        
        if member_data.loyalty < 0.2:
            # Member leaves the group
            del group_data["members"][problem_agent.name]
            
            if hasattr(problem_agent, 'group_memberships'):
                if group_name in problem_agent.group_memberships:
                    problem_agent.group_memberships.remove(group_name)
            
            problem_agent.memory.store_memory(
                f"Left {group_name} due to disagreements with their direction",
                importance=0.7,
                memory_type="experience"
            )
            
            return {
                "type": "member_departure",
                "group_name": group_name,
                "departing_member": problem_agent.name,
                "reason": "low_loyalty",
                "day": current_day
            }
        
        else:
            # Internal dispute but member stays
            member_data.loyalty = max(0.0, member_data.loyalty - 0.1)
            
            # Affect other members
            for other_member_data in group_data["members"].values():
                if random.random() < 0.3:
                    other_member_data.loyalty = max(0.0, other_member_data.loyalty - 0.05)
            
            return {
                "type": "internal_dispute",
                "group_name": group_name,
                "troublemaker": problem_agent.name,
                "loyalty_impact": -0.1,
                "day": current_day
            }
    
    def get_group_summary(self, group_name: str) -> Optional[Dict[str, Any]]:
        """Get a comprehensive summary of a group."""
        if group_name not in self.groups:
            return None
        
        group_data = self.groups[group_name]
        summary = {
            "basic_info": group_data,
            "collective_memory": None,
            "alliances": [],
            "institutions": []
        }
        
        # Add collective memory
        if group_name in self.collective_memories:
            summary["collective_memory"] = asdict(self.collective_memories[group_name])
        
        # Add alliances
        for alliance in self.alliances.values():
            if alliance.group1 == group_name or alliance.group2 == group_name:
                summary["alliances"].append(asdict(alliance))
        
        # Add institutions this group is involved with
        for institution in self.institutions.values():
            if any(member in group_data["members"] for member in institution.leaders + institution.members):
                summary["institutions"].append(asdict(institution))
        
        return summary
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall status of the group dynamics system."""
        return {
            "total_groups": len(self.groups),
            "active_groups": len([g for g in self.groups.values() 
                                if g["status"] != GroupStatus.DISBANDED.value]),
            "total_alliances": len(self.alliances),
            "total_institutions": len(self.institutions),
            "groups_by_type": {
                group_type.value: len([g for g in self.groups.values() if g["type"] == group_type.value])
                for group_type in GroupType
            },
            "groups_by_status": {
                status.value: len([g for g in self.groups.values() if g["status"] == status.value])
                for status in GroupStatus
            }
        } 