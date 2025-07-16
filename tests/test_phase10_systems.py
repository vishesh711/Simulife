"""
Test suite for Phase 10: Deep Human Emotions & Life Purpose systems
"""

import pytest
import json
from unittest.mock import Mock, patch
from simulife.engine import (
    LoveRomanceSystem, LifePurposeSystem, 
    DeepFamilyBondsSystem, EmotionalComplexitySystem,
    PurposeCategory, EmotionType, BondType
)


class TestLoveRomanceSystem:
    """Test the Love & Romance System"""
    
    def test_system_initialization(self):
        """Test that the romance system initializes correctly"""
        system = LoveRomanceSystem()
        assert system is not None
        assert system.romantic_attractions == {}
        assert system.active_relationships == {}
        assert system.attraction_base_chance == 0.1
    
    def test_romantic_compatibility_calculation(self):
        """Test romantic compatibility calculation"""
        system = LoveRomanceSystem()
        
        # Create mock agents
        agent1 = Mock()
        agent1.name = "TestAgent1"
        agent1.age = 25
        agent1.personality_scores = {"openness": 0.7, "agreeableness": 0.8}
        agent1.traits = ["creative", "caring"]
        agent1.reputation = 0.8
        agent1.location = "village"
        
        agent2 = Mock()
        agent2.name = "TestAgent2"
        agent2.age = 27
        agent2.personality_scores = {"openness": 0.6, "agreeableness": 0.7}
        agent2.traits = ["artistic", "gentle"]
        agent2.reputation = 0.7
        agent2.location = "village"
        
        compatibility = system._calculate_romantic_compatibility(agent1, agent2)
        assert 0.0 <= compatibility <= 1.0
        assert compatibility > 0.5  # Should be compatible given similar traits
    
    def test_age_compatibility(self):
        """Test age compatibility checking"""
        system = LoveRomanceSystem()
        
        # Compatible ages
        agent1 = Mock()
        agent1.age = 25
        agent2 = Mock()
        agent2.age = 30
        
        assert system._age_compatible(agent1, agent2) == True
        
        # Too young
        agent1.age = 15
        assert system._age_compatible(agent1, agent2) == False
        
        # Too large age gap
        agent1.age = 25
        agent2.age = 50
        assert system._age_compatible(agent1, agent2) == False


class TestLifePurposeSystem:
    """Test the Life Purpose & Meaning System"""
    
    def test_system_initialization(self):
        """Test that the purpose system initializes correctly"""
        system = LifePurposeSystem()
        assert system is not None
        assert system.agent_purposes == {}
        assert system.existential_moments == []
        assert len(system.purpose_descriptions) == len(PurposeCategory)
    
    def test_purpose_category_determination(self):
        """Test purpose category assignment based on personality"""
        system = LifePurposeSystem()
        
        # Creative agent
        agent = Mock()
        agent.personality_scores = {"openness": 0.9, "conscientiousness": 0.6}
        agent.traits = ["creative", "artistic"]
        
        purpose = system._determine_purpose_category(agent)
        assert purpose in PurposeCategory
    
    def test_ready_for_purpose_discovery(self):
        """Test readiness for purpose discovery"""
        system = LifePurposeSystem()
        
        # Too young
        agent = Mock()
        agent.age = 16
        agent.memory = Mock()
        agent.memory.get_recent_memories.return_value = [Mock() for _ in range(60)]
        agent.advanced_skills = {"skill1": Mock(level=0.5), "skill2": Mock(level=0.4)}
        
        assert system._is_ready_for_purpose_discovery(agent) == False
        
        # Right age and experience
        agent.age = 25
        assert system._is_ready_for_purpose_discovery(agent) == True
    
    def test_existential_moment_creation(self):
        """Test creation of existential moments"""
        system = LifePurposeSystem()
        
        agent = Mock()
        agent.name = "TestAgent"
        agent.age = 30
        agent.personality_scores = {"openness": 0.8, "neuroticism": 0.6}
        agent.memory = Mock()
        agent.memory.get_recent_memories.return_value = [Mock(content="test memory", emotion="sad")]
        
        moment = system._create_existential_moment(agent, 100)
        assert moment is not None
        assert moment.agent_name == "TestAgent"
        assert moment.day == 100
        assert len(moment.questions_raised) > 0


class TestDeepFamilyBondsSystem:
    """Test the Deep Family Bonds System"""
    
    def test_system_initialization(self):
        """Test that the family bonds system initializes correctly"""
        system = DeepFamilyBondsSystem()
        assert system is not None
        assert system.family_bonds == {}
        assert system.family_traditions == {}
        assert system.bond_formation_chance == 0.8
    
    def test_family_relationship_determination(self):
        """Test determining family relationships"""
        system = DeepFamilyBondsSystem()
        
        # Parent-child relationship
        parent = Mock()
        parent.family = {"children": ["child1"]}
        child = Mock()
        child.name = "child1"
        child.family = {"parents": ["parent1"]}
        
        relationship = system._determine_family_relationship(parent, child)
        assert relationship == "parent_child"
        
        # Sibling relationship
        sibling1 = Mock()
        sibling1.family = {"siblings": ["sibling2"]}
        sibling2 = Mock()
        sibling2.name = "sibling2"
        sibling2.family = {"siblings": ["sibling1"]}
        
        relationship = system._determine_family_relationship(sibling1, sibling2)
        assert relationship == "sibling"
    
    def test_bond_type_assignment(self):
        """Test bond type assignment for relationships"""
        system = DeepFamilyBondsSystem()
        
        agent1 = Mock()
        agent1.personality_scores = {"agreeableness": 0.8}
        agent2 = Mock()
        agent2.personality_scores = {"agreeableness": 0.7}
        
        # Parent-child should be parental love
        bond_type = system._get_bond_type_for_relationship("parent_child", agent1, agent2)
        assert bond_type == BondType.PARENTAL_LOVE
        
        # Child-parent should be filial devotion
        bond_type = system._get_bond_type_for_relationship("child_parent", agent1, agent2)
        assert bond_type == BondType.FILIAL_DEVOTION
    
    def test_bond_strength_calculation(self):
        """Test bond strength calculation"""
        system = DeepFamilyBondsSystem()
        
        agent1 = Mock()
        agent1.age = 35
        agent1.personality_scores = {"agreeableness": 0.8, "conscientiousness": 0.7}
        
        agent2 = Mock()
        agent2.age = 10
        agent2.personality_scores = {"agreeableness": 0.6, "conscientiousness": 0.5}
        
        strength = system._calculate_bond_strength(agent1, agent2, BondType.PARENTAL_LOVE)
        assert 0.0 <= strength <= 1.0
        assert strength > 0.8  # Parental love should be very strong


class TestEmotionalComplexitySystem:
    """Test the Emotional Complexity System"""
    
    def test_system_initialization(self):
        """Test that the emotional complexity system initializes correctly"""
        system = EmotionalComplexitySystem()
        assert system is not None
        assert system.agent_emotional_states == {}
        assert system.emotional_growth_events == []
        assert len(system.complex_emotion_recipes) > 0
    
    def test_emotional_state_calculation(self):
        """Test emotional state calculation"""
        system = EmotionalComplexitySystem()
        
        agent = Mock()
        agent.name = "TestAgent"
        agent.personality_scores = {
            "extraversion": 0.7,
            "neuroticism": 0.3,
            "agreeableness": 0.8,
            "conscientiousness": 0.6,
            "openness": 0.5
        }
        agent.memory = Mock()
        agent.memory.get_recent_memories.return_value = [
            Mock(emotion="happy", importance=0.8, content="great day"),
            Mock(emotion="excited", importance=0.6, content="achievement")
        ]
        
        emotional_state = system._calculate_current_emotional_state(agent, 100)
        assert emotional_state.agent_name == "TestAgent"
        assert emotional_state.day == 100
        assert EmotionType.JOY in emotional_state.primary_emotions
        assert 0.0 <= emotional_state.emotional_intensity <= 1.0
    
    def test_complex_emotion_triggers(self):
        """Test complex emotion triggering"""
        system = EmotionalComplexitySystem()
        
        # Create emotional state with mixed emotions for bittersweet
        emotional_state = Mock()
        emotional_state.primary_emotions = {
            EmotionType.JOY: 0.7,
            EmotionType.SADNESS: 0.8,
            EmotionType.ANGER: 0.2,
            EmotionType.FEAR: 0.1,
            EmotionType.LOVE: 0.3
        }
        
        recipe = system.complex_emotion_recipes[system.ComplexEmotionType.BITTERSWEET]
        triggered = system._complex_emotion_triggered(emotional_state, recipe)
        assert triggered == True
        
        intensity = system._calculate_complex_emotion_intensity(emotional_state, recipe)
        assert 0.0 <= intensity <= 1.0
    
    def test_empathy_strength_calculation(self):
        """Test empathy strength calculation"""
        system = EmotionalComplexitySystem()
        
        empathizer = Mock()
        empathizer.name = "Empathizer"
        empathizer.age = 30
        empathizer.personality_scores = {"agreeableness": 0.9}
        empathizer.relationships = {"Target": "family"}
        
        target = Mock()
        target.name = "Target"
        
        strength = system._calculate_empathy_strength(empathizer, target, EmotionType.SADNESS)
        assert 0.0 <= strength <= 1.0
        assert strength > 0.5  # Should be high due to high agreeableness and family relationship


class TestSystemIntegration:
    """Test integration between Phase 10 systems"""
    
    def test_all_systems_can_be_imported(self):
        """Test that all Phase 10 systems can be imported successfully"""
        from simulife.engine import (
            LoveRomanceSystem, LifePurposeSystem,
            DeepFamilyBondsSystem, EmotionalComplexitySystem
        )
        
        # Should not raise any exceptions
        romance = LoveRomanceSystem()
        purpose = LifePurposeSystem()
        family = DeepFamilyBondsSystem()
        emotions = EmotionalComplexitySystem()
        
        assert all([romance, purpose, family, emotions])
    
    def test_systems_process_daily_events(self):
        """Test that all systems can process daily events without errors"""
        romance = LoveRomanceSystem()
        purpose = LifePurposeSystem()
        family = DeepFamilyBondsSystem()
        emotions = EmotionalComplexitySystem()
        
        # Create mock agents
        agents = []
        for i in range(3):
            agent = Mock()
            agent.name = f"Agent{i}"
            agent.age = 25 + i * 5
            agent.is_alive = True
            agent.location = "village"
            agent.personality_scores = {
                "openness": 0.5, "conscientiousness": 0.5,
                "extraversion": 0.5, "agreeableness": 0.5,
                "neuroticism": 0.5
            }
            agent.memory = Mock()
            agent.memory.get_recent_memories.return_value = []
            agent.memory.store_memory = Mock()
            agent.family = {"family_id": "test_family", "children": [], "parents": [], "siblings": []}
            agent.health = 1.0
            agent.reputation = 0.8
            agents.append(agent)
        
        current_day = 100
        
        # Test that each system can process events without crashing
        romance_events = romance.process_daily_romantic_development(agents, current_day)
        purpose_events = purpose.process_daily_purpose_development(agents, current_day)
        family_events = family.process_daily_family_bonds(agents, current_day)
        emotion_events = emotions.process_daily_emotional_complexity(agents, current_day)
        
        # Should return lists (may be empty)
        assert isinstance(romance_events, list)
        assert isinstance(purpose_events, list)
        assert isinstance(family_events, list)
        assert isinstance(emotion_events, list)


if __name__ == "__main__":
    pytest.main([__file__]) 