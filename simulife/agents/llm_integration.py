"""
LLM Integration for SimuLife Agents
Provides intelligent decision-making and natural language capabilities.
"""

import os
import random
from typing import Dict, List, Any, Optional, Union
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate_response(self, prompt: str, max_tokens: int = 150, 
                         temperature: float = 0.7) -> str:
        """Generate a response using the LLM."""
        pass


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing and development without API costs."""
    
    def __init__(self):
        self.decision_templates = {
            "rest_and_think": [
                "seeks solitude to contemplate recent events",
                "finds a peaceful spot to reflect on life",
                "takes time to process their thoughts and feelings"
            ],
            "socialize_with_others": [
                "looks for interesting people to talk with",
                "approaches others with a friendly demeanor",
                "seeks meaningful conversation and connection"
            ],
            "work_on_skills": [
                "practices their craft with dedication",
                "studies intently to improve their abilities",
                "works on developing new talents"
            ],
            "explore_area": [
                "ventures into uncharted territory",
                "explores with curiosity and caution",
                "seeks new discoveries and adventures"
            ],
            "help_someone": [
                "looks for someone who needs assistance",
                "offers aid to those in distress",
                "extends a helping hand to the community"
            ],
            "pursue_personal_goal": [
                "works diligently toward their ambitions",
                "takes steps to achieve their dreams",
                "focuses on their personal mission"
            ]
        }
        
        self.conversation_starters = [
            "shares an interesting observation about recent events",
            "asks thoughtful questions about the other's experiences",
            "discusses their hopes and concerns",
            "exchanges stories and wisdom",
            "debates ideas and philosophies",
            "shares knowledge and skills",
            "discusses the future of their community"
        ]
        
        self.reflection_templates = [
            "Today taught me about {topic}. I feel {emotion} about {event}.",
            "I wonder what would happen if {speculation}. This makes me {emotion}.",
            "My relationship with {person} has {change}. I should {action}.",
            "The world seems to be {observation}. I must {response}.",
            "I remember when {memory}. Compared to now, {comparison}."
        ]

    def generate_response(self, prompt: str, max_tokens: int = 150, 
                         temperature: float = 0.7) -> str:
        """Generate a mock response based on prompt keywords."""
        prompt_lower = prompt.lower()
        
        # Decision-making responses
        for action, templates in self.decision_templates.items():
            if action.replace("_", " ") in prompt_lower:
                return random.choice(templates)
        
        # Conversation responses
        if "conversation" in prompt_lower or "talk" in prompt_lower:
            return random.choice(self.conversation_starters)
        
        # Reflection responses
        if "reflect" in prompt_lower or "think about" in prompt_lower:
            template = random.choice(self.reflection_templates)
            # Simple template filling
            if "{emotion}" in template:
                emotions = ["hopeful", "concerned", "excited", "thoughtful", "determined"]
                template = template.replace("{emotion}", random.choice(emotions))
            if "{topic}" in template:
                topics = ["trust", "cooperation", "change", "the future", "relationships"]
                template = template.replace("{topic}", random.choice(topics))
            return template
        
        # Generic response
        return "contemplates the situation carefully and considers their options"


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider (requires openai package and API key)."""
    
    def __init__(self, model: str = "gpt-3.5-turbo", api_key: Optional[str] = None):
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
            self.model = model
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    
    def generate_response(self, prompt: str, max_tokens: int = 150, 
                         temperature: float = 0.7) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Fallback to mock response if API fails
            print(f"OpenAI API error: {e}, falling back to mock response")
            return MockLLMProvider().generate_response(prompt, max_tokens, temperature)


class GroqProvider(LLMProvider):
    """Groq provider for fast inference (requires groq package and API key)."""
    
    def __init__(self, model: str = "mixtral-8x7b-32768", api_key: Optional[str] = None):
        try:
            import groq
            self.client = groq.Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))
            self.model = model
        except ImportError:
            raise ImportError("groq package not installed. Run: pip install groq")
    
    def generate_response(self, prompt: str, max_tokens: int = 150, 
                         temperature: float = 0.7) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Groq API error: {e}, falling back to mock response")
            return MockLLMProvider().generate_response(prompt, max_tokens, temperature)


class LLMAgentBrain:
    """
    Enhanced agent decision-making using LLMs.
    Provides intelligent responses for decisions, conversations, and reflections.
    """
    
    def __init__(self, provider: LLMProvider = None):
        self.provider = provider or MockLLMProvider()
    
    def decide_action(self, agent_context: Dict[str, Any], 
                     available_actions: List[str], world_context: str = "") -> str:
        """Use LLM to decide what action the agent should take."""
        
        # Build a rich context prompt
        prompt = f"""You are {agent_context['name']}, a {agent_context['age']}-year-old person.

Your personality traits: {', '.join(agent_context.get('traits', []))}
Your current emotion: {agent_context.get('emotion', 'neutral')} (intensity: {agent_context.get('emotion_intensity', 0.5)})
Your main goal: {agent_context.get('current_goal', 'unclear')}
Your location: {agent_context.get('location', 'unknown')}

Recent memories: {agent_context.get('recent_memories', 'None')}
Current relationships: {agent_context.get('relationships_summary', 'None')}

World situation: {world_context}

Available actions: {', '.join(available_actions)}

Based on your personality, goals, emotions, and the current situation, what would you choose to do? 
Respond with just the action and a brief natural description of how you'd do it.
Keep it under 50 words and be specific to your character."""

        response = self.provider.generate_response(prompt, max_tokens=100, temperature=0.8)
        return response

    def generate_conversation(self, speaker_context: Dict[str, Any], 
                            listener_context: Dict[str, Any],
                            relationship: str = "stranger",
                            topic: str = "general") -> str:
        """Generate natural conversation between two agents."""
        
        prompt = f"""You are {speaker_context['name']}, talking to {listener_context['name']}.

Your traits: {', '.join(speaker_context.get('traits', []))}
Your emotion: {speaker_context.get('emotion', 'neutral')}
Your relationship with {listener_context['name']}: {relationship}

Their traits: {', '.join(listener_context.get('traits', []))}
Their emotion: {listener_context.get('emotion', 'neutral')}

Topic of conversation: {topic}

What would you say? Keep it natural, in character, and under 30 words.
Show personality through your speaking style."""

        response = self.provider.generate_response(prompt, max_tokens=80, temperature=0.9)
        return response

    def create_reflection(self, agent_context: Dict[str, Any], 
                         recent_events: List[str]) -> str:
        """Generate thoughtful reflection on recent experiences."""
        
        prompt = f"""You are {agent_context['name']}, reflecting on recent events.

Your personality: {', '.join(agent_context.get('traits', []))}
Your current emotion: {agent_context.get('emotion', 'neutral')}
Your goals: {', '.join(agent_context.get('goals', []))}

Recent events you experienced:
{chr(10).join(f'- {event}' for event in recent_events[-5:])}

Reflect on these experiences. What did you learn? How do you feel? What are you thinking about?
Write a brief, personal reflection (under 40 words) in first person."""

        response = self.provider.generate_response(prompt, max_tokens=80, temperature=0.7)
        return response

    def evolve_personality(self, agent_context: Dict[str, Any], 
                          significant_events: List[str]) -> Dict[str, Any]:
        """Suggest personality evolution based on major life events."""
        
        prompt = f"""You are analyzing personality development for {agent_context['name']}.

Current traits: {', '.join(agent_context.get('traits', []))}
Current goals: {', '.join(agent_context.get('goals', []))}

Major recent events:
{chr(10).join(f'- {event}' for event in significant_events)}

How might these events change their personality? Consider:
- Could they develop new traits or lose old ones?
- Might their goals shift or evolve?
- What new motivations could emerge?

Suggest specific changes in this format:
New trait: [trait name]
Modified goal: [goal]
Keep changes realistic and gradual."""

        response = self.provider.generate_response(prompt, max_tokens=120, temperature=0.6)
        
        # Parse response for actual personality changes
        # For now, return the raw response - could be enhanced with parsing
        return {"suggestion": response}

    def generate_faction_ideology(self, founder_context: Dict[str, Any],
                                 members_contexts: List[Dict[str, Any]],
                                 founding_event: str) -> Dict[str, str]:
        """Generate ideology and name for a new faction."""
        
        all_traits = []
        all_goals = []
        
        for member in [founder_context] + members_contexts:
            all_traits.extend(member.get('traits', []))
            all_goals.extend(member.get('goals', []))
        
        common_traits = list(set(all_traits))
        common_goals = list(set(all_goals))
        
        prompt = f"""A new group is forming led by {founder_context['name']}.

Group members' traits: {', '.join(common_traits)}
Group members' goals: {', '.join(common_goals)}
Founding event: {founding_event}

Create a faction identity:
1. Faction name (2-3 words, evocative)
2. Core ideology (1 sentence belief statement)
3. Primary goal (what they want to achieve)
4. Values (3 key principles)

Format:
Name: [name]
Ideology: [belief]
Goal: [objective]
Values: [value1], [value2], [value3]"""

        response = self.provider.generate_response(prompt, max_tokens=150, temperature=0.8)
        
        # Basic parsing - could be enhanced
        lines = response.split('\n')
        result = {"raw_response": response}
        
        for line in lines:
            if line.startswith("Name:"):
                result["name"] = line.replace("Name:", "").strip()
            elif line.startswith("Ideology:"):
                result["ideology"] = line.replace("Ideology:", "").strip()
            elif line.startswith("Goal:"):
                result["goal"] = line.replace("Goal:", "").strip()
            elif line.startswith("Values:"):
                result["values"] = line.replace("Values:", "").strip()
        
        return result


# Factory function for easy LLM provider creation
def create_llm_provider(provider_type: str = "mock", **kwargs) -> LLMProvider:
    """
    Factory function to create LLM providers.
    
    Args:
        provider_type: "mock", "openai", or "groq"
        **kwargs: Additional arguments for the provider
    
    Returns:
        LLMProvider instance
    """
    if provider_type.lower() == "mock":
        return MockLLMProvider()
    elif provider_type.lower() == "openai":
        return OpenAIProvider(**kwargs)
    elif provider_type.lower() == "groq":
        return GroqProvider(**kwargs)
    else:
        raise ValueError(f"Unknown provider type: {provider_type}")


# Example usage configurations
DEFAULT_CONFIG = {
    "provider_type": "mock",  # Start with mock for development
    "temperature": 0.7,
    "max_tokens": 150
}

CREATIVE_CONFIG = {
    "provider_type": "mock",
    "temperature": 0.9,  # More creative/random
    "max_tokens": 200
}

FOCUSED_CONFIG = {
    "provider_type": "mock", 
    "temperature": 0.3,  # More focused/deterministic
    "max_tokens": 100
} 