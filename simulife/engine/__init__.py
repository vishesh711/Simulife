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

# Phase 7: Population Dynamics Systems
from .mortality_system import MortalitySystem, DeathCause, LifeStage, DeathRecord, AgingEffect
from .genetic_disease_system import GeneticDiseaseSystem, DiseaseType, InheritancePattern, DiseaseSeverity, GeneticDisease, GeneticCarrier
from .population_pressure_system import PopulationPressureSystem, PopulationPressureLevel, MigrationCause, ResourceScarcityType, CarryingCapacity, MigrationEvent
from .generational_culture_system import GenerationalCultureSystem, CultureType, TransmissionType, CulturalEvolution, CulturalElement, GenerationData

# Phase 8: Emergent Phenomena Systems
from .social_institutions_system import SocialInstitutionsSystem, InstitutionType, GovernanceType, InstitutionStatus, SocialInstitution, InstitutionalCrisis
from .economic_emergence_system import EconomicEmergenceSystem, MarketType, CurrencyType, EconomicRole, TradeGoodCategory, TradeGood, MarketPlace, TradeRoute, EconomicAgent
from .cultural_movements_system import CulturalMovementsSystem, MovementType, MovementStage, BeliefIntensity, PropagationMethod, CulturalBelief, CulturalMovement, CulturalConflict
from .civilizational_milestones_system import CivilizationalMilestonesSystem, MilestoneCategory, MilestoneSignificance, MilestoneStatus, CivilizationalMilestone, MilestoneProgression
from .crisis_response_system import CrisisResponseSystem, CrisisType, CrisisSeverity, ResponsePhase, ResponseStrategy, ResponseEffectiveness, SocietalCrisis, CrisisResponse, ResilienceCapacity
from .inter_group_diplomacy_system import InterGroupDiplomacySystem, DiplomaticStatus, TreatyType, NegotiationPhase, DiplomaticAction, DiplomaticRelation, DiplomaticTreaty, DiplomaticNegotiation, DiplomaticAgent

# Phase 9: Advanced AI & Meta-Cognition Systems
from .self_awareness_system import SelfAwarenessSystem, IdentityAspect, SelfReflectionType, ConsciousnessLevel, IdentityComponent, SelfReflection, IdentityCrisis, SelfModel
from .meta_cognition_system import MetaCognitionSystem, CognitiveProcess, MetaCognitiveSkill, CognitiveBias, MetaCognitiveInsight, CognitiveBiasRecognition, MetaCognitiveStrategy, ThinkingPattern, MetaCognitiveProfile
from .consciousness_metrics_system import ConsciousnessMetricsSystem, ConsciousnessAspect, ConsciousnessEvent, ConsciousnessProfile, ConsciousnessBreakthrough, ExistentialMoment, CollectiveConsciousnessEvent

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
    'Innovation',
    # Phase 7 Systems
    'MortalitySystem',
    'DeathCause',
    'LifeStage',
    'DeathRecord',
    'AgingEffect',
    'GeneticDiseaseSystem',
    'DiseaseType',
    'InheritancePattern',
    'DiseaseSeverity',
    'GeneticDisease',
    'GeneticCarrier',
    'PopulationPressureSystem',
    'PopulationPressureLevel',
    'MigrationCause',
    'ResourceScarcityType',
    'CarryingCapacity',
    'MigrationEvent',
    'GenerationalCultureSystem',
    'CultureType',
    'TransmissionType',
    'CulturalEvolution',
    'CulturalElement',
    'GenerationData',
    # Phase 8 Systems
    'SocialInstitutionsSystem',
    'InstitutionType',
    'GovernanceType',
    'InstitutionStatus',
    'SocialInstitution',
    'InstitutionalCrisis',
    'EconomicEmergenceSystem',
    'MarketType',
    'CurrencyType',
    'EconomicRole',
    'TradeGoodCategory',
    'TradeGood',
    'MarketPlace',
    'TradeRoute',
    'EconomicAgent',
    'CulturalMovementsSystem',
    'MovementType',
    'MovementStage',
    'BeliefIntensity',
    'PropagationMethod',
    'CulturalBelief',
    'CulturalMovement',
    'CulturalConflict',
    'CivilizationalMilestonesSystem',
    'MilestoneCategory',
    'MilestoneSignificance',
    'MilestoneStatus',
    'CivilizationalMilestone',
    'MilestoneProgression',
    'CrisisResponseSystem',
    'CrisisType',
    'CrisisSeverity',
    'ResponsePhase',
    'ResponseStrategy',
    'ResponseEffectiveness',
    'SocietalCrisis',
    'CrisisResponse',
    'ResilienceCapacity',
    'InterGroupDiplomacySystem',
    'DiplomaticStatus',
    'TreatyType',
    'NegotiationPhase',
    'DiplomaticAction',
    'DiplomaticRelation',
    'DiplomaticTreaty',
    'DiplomaticNegotiation',
    'DiplomaticAgent',
    # Phase 9 Systems
    'SelfAwarenessSystem',
    'IdentityAspect',
    'SelfReflectionType',
    'ConsciousnessLevel',
    'IdentityComponent',
    'SelfReflection',
    'IdentityCrisis',
    'SelfModel',
    'MetaCognitionSystem',
    'CognitiveProcess',
    'MetaCognitiveSkill',
    'CognitiveBias',
    'MetaCognitiveInsight',
    'CognitiveBiasRecognition',
    'MetaCognitiveStrategy',
    'ThinkingPattern',
    'MetaCognitiveProfile',
    'ConsciousnessMetricsSystem',
    'ConsciousnessAspect',
    'ConsciousnessEvent',
    'ConsciousnessProfile',
    'ConsciousnessBreakthrough',
    'ExistentialMoment',
    'CollectiveConsciousnessEvent'
] 