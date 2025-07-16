"""
SimuLife Engine Package
Main simulation engine components for the virtual world.
"""

from .simulation_loop import SimulationEngine
from .world_state import WorldState, WorldEvent
from .advanced_events import AdvancedEventSystem, EventType
from .cultural_system import CulturalSystem
from .resource_system import ResourceSystem
from .environmental_system import EnvironmentalSystem

# Phase 4: Advanced Behaviors Systems
from .skill_system import SkillSystem, SkillCategory, Skill
from .specialization_system import SpecializationSystem, SpecializationType, Specialization
from .conflict_system import ConflictSystem, ConflictType, ConflictSeverity
from .cultural_artifacts import CulturalArtifactSystem, ArtifactType, CulturalArtifact

# Phase 5: Group Dynamics Systems
from .group_dynamics import GroupDynamicsSystem, GroupType, GroupStatus, AllianceType

# Phase 6: Technology and Innovation Systems
from .technology_system import TechnologySystem, TechnologyCategory, ResearchStatus, InnovationType, Technology, ResearchProject, Innovation

__all__ = [
    'SimulationEngine',
    'WorldState', 
    'WorldEvent',
    'AdvancedEventSystem',
    'EventType',
    'CulturalSystem',
    'ResourceSystem', 
    'EnvironmentalSystem',
    # Phase 4 Systems
    'SkillSystem',
    'SkillCategory',
    'Skill',
    'SpecializationSystem',
    'SpecializationType', 
    'Specialization',
    'ConflictSystem',
    'ConflictType',
    'ConflictSeverity',
    'CulturalArtifactSystem',
    'ArtifactType',
    'CulturalArtifact',
    # Phase 5 Systems
    'GroupDynamicsSystem',
    'GroupType',
    'GroupStatus',
    'AllianceType',
    # Phase 6 Systems
    'TechnologySystem',
    'TechnologyCategory',
    'ResearchStatus',
    'InnovationType',
    'Technology',
    'ResearchProject',
    'Innovation'
] 