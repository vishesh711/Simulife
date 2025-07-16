# SimuLife Quick Start Guide

## No API Keys Required! 🎉

SimuLife is designed to work **immediately** without any API keys using our intelligent MockLLMProvider. You can run the full simulation and see all features working right away.

## Instant Setup (5 minutes)

### 1. Install Dependencies
```bash
cd /Users/vishesh/Documents/Github/Simulife
pip install -r requirements.txt
```

### 2. Run Your First Simulation
```bash
python main.py
```

### 3. Try These Commands
```
# Start a 1-day simulation
run 1

# Check agent status  
status

# Inspect an agent
inspect Lara

# Save the world
save test_world

# Load it back
load test_world

# Exit
quit
```

## What Works Without API Keys

✅ **Everything!** The MockLLMProvider provides:
- Intelligent agent decision-making
- Natural conversation between agents  
- Personality-driven responses
- Reflection and goal formation
- All simulation features

## Optional: Adding Real LLM Power

If you want even more sophisticated AI responses, you can add API keys:

### Option 1: OpenAI Integration
```bash
export OPENAI_API_KEY="your-key-here"
```

### Option 2: Groq Integration (Faster)
```bash
export GROQ_API_KEY="your-key-here"  
```

### Switching LLM Providers
The system automatically detects available API keys and uses them. You can also manually configure:

```python
# In your code or agent configs
agent.llm_brain = LLMAgentBrain(agent, OpenAIProvider())
# or
agent.llm_brain = LLMAgentBrain(agent, GroqProvider())
# or (default - no keys needed)
agent.llm_brain = LLMAgentBrain(agent, MockLLMProvider())
```

## Sample Simulation Results

With **no API keys**, you can still see:
- Agents forming relationships
- Complex family trees developing
- Cultural events and storytelling
- Political tensions and leadership
- Rich narrative progression

## Current Agent Roster

Your simulation includes 5 diverse agents:

1. **Lara** - Wise, nature-connected leader
2. **Aedan** - Ambitious, innovative strategist  
3. **Kara** - Empathetic, community-focused healer
4. **Nyla** - Adventurous, independent explorer
5. **Theron** - Logical, knowledge-seeking scholar

## Development Mode Benefits

The MockLLMProvider is actually **ideal for development** because:
- ⚡ Instant responses (no API latency)
- 💰 Zero cost
- 🔄 Consistent, predictable behavior for testing
- 🧪 Perfect for iterating on game mechanics

## Getting Help

- Check `DEVELOPMENT_LOG.md` for detailed feature documentation
- Use `PHASE_TRACKING_TEMPLATE.md` for tracking your own development
- All code is well-documented with docstrings
- Interactive mode has built-in help commands

## Next Steps

1. **Run a longer simulation**: Try `run 7` for a week-long simulation
2. **Explore the events**: Watch for mentorship, storytelling, discoveries
3. **Check family trees**: Some agents might have children!
4. **Experiment with saves**: Create different simulation branches
5. **Dive into the code**: Everything is modular and extensible

You now have a fully functional AI civilization at your fingertips! 🌟 