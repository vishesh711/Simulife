# 🌍 SimuLife: Multi-Agent LLM Simulation

> *A persistent virtual world populated by AI agents with personalities, emotions, and memory*

SimuLife is an ambitious simulation where AI agents live, learn, form relationships, build societies, and evolve over time. Watch as digital civilizations emerge from simple interactions between autonomous agents powered by Large Language Models.

## ✨ What Makes SimuLife Special

🧠 **Intelligent Agents**: Each agent has personality traits, emotions, goals, and vector-based memory (FAISS)  
🤝 **Emergent Relationships**: Agents form friendships, rivalries, families, and factions organically  
🏛️ **Society Building**: Watch factions, belief systems, customs, and governance structures emerge  
⏰ **Persistent Evolution**: The world runs continuously, with agents aging, learning, and changing  
💾 **Full Persistence**: Save and reload entire civilizations, including agent memories and world state  
🎭 **Rich Interactions**: Agents negotiate, debate, collaborate, and build culture through language  

## 🧬 Core Architecture

### Agent System
Each agent is a complete AI entity with:
- **Identity**: Name, age, personality traits, values
- **Memory**: FAISS vector store for experiences, relationships, reflections
- **Emotions**: Dynamic emotional states that affect decision-making
- **Goals**: Personal objectives that drive behavior
- **Relationships**: Complex social networks with other agents
- **Skills & Beliefs**: Evolving capabilities and worldview

### World Simulation
- **Time Progression**: Day/night cycles, seasons, years
- **Environment**: Dynamic weather, resources, multiple locations
- **Events**: Random world events that affect all agents
- **Persistence**: Complete world state saved to disk

### Memory & Learning
- **Vector Memory**: Semantic search through past experiences
- **Reflection System**: Agents contemplate and learn from experiences
- **Relationship Tracking**: Dynamic social network evolution
- **Cultural Memory**: Shared beliefs and customs emerge organically

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/simulife
cd simulife

# Install dependencies
pip install -r requirements.txt

# Run your first simulation
python main.py --days 5
```

## 📚 Documentation

**New to SimuLife?** Check out our comprehensive documentation:

- **🚀 [Quick Start Guide](QUICK_START_GUIDE.md)** - Get running in 5 minutes (no API keys needed!)
- **📋 [Development Log](DEVELOPMENT_LOG.md)** - Complete phase-wise development progress and current capabilities  
- **📁 [Documentation System](docs/README.md)** - Organized docs with templates for tracking development

**Key Points:**
- ✅ **Works immediately** without any API keys using intelligent MockLLMProvider
- 🔧 **Optional LLM integration** with OpenAI or Groq for enhanced AI responses
- 📈 **5/9 development phases complete** with sophisticated agent behaviors
- 🧬 **Reproduction system** with genetic inheritance and family trees
- 🎭 **Advanced events** including cultural, political, and discovery mechanics

### Basic Usage

```bash
# Run a 10-day simulation
python main.py --days 10

# Run in interactive mode
python main.py --interactive

# Load a previous simulation
python main.py --load my_save --days 5

# Disable verbose output
python main.py --no-verbose --days 20
```

## 📁 Project Structure

```
simulife/
├── agents/                    # Agent system
│   ├── base_agent.py         # Core agent class
│   ├── memory_manager.py     # FAISS-based memory
│   └── __init__.py
├── engine/                    # Simulation engine
│   ├── simulation_loop.py    # Main simulation loop
│   ├── world_state.py        # World management
│   └── __init__.py
└── __init__.py

data/
├── agent_configs/             # Agent configuration files
│   ├── lara.json             # Sample agent: Lara (curious mage)
│   ├── aedan.json            # Sample agent: Aedan (protective brother)
│   ├── kara.json             # Sample agent: Kara (ambitious rival)
│   ├── nyla.json             # Sample agent: Nyla (wise healer)
│   └── theron.json           # Sample agent: Theron (young explorer)
├── memory_faiss/             # Agent memory storage
└── saves/                    # Simulation save files

main.py                       # Main entry point
requirements.txt              # Dependencies
README.md                     # This file
```

## 🎮 Interactive Commands

When running with `--interactive`, you can use these commands:

- `run [days]` - Run simulation for N days (default: 1)
- `status` - Show current world status
- `agent <name>` - View detailed agent information
- `save <name>` - Save current simulation state
- `quit` - Exit simulation

## 🧪 Sample Agents

SimuLife comes with 5 pre-configured agents to get you started:

- **Lara**: A curious and ambitious mage seeking ancient knowledge
- **Aedan**: Lara's protective brother, focused on family and security  
- **Kara**: An ambitious rival with political aspirations
- **Nyla**: A wise healer who maintains community balance
- **Theron**: A young explorer seeking adventure and discovery

Each agent has unique traits, goals, relationships, and starting memories that create interesting dynamics.

## 📊 What Emerges Over Time

As your simulation runs, you'll witness:

### 🤝 Relationship Evolution
- Strangers become friends or rivals
- Romance and family formation
- Political alliances and conflicts
- Mentorship and knowledge transfer

### 🏛️ Society Formation  
- **Factions**: Groups form around shared goals or ideologies
- **Beliefs**: Agents develop shared worldviews and explanations
- **Customs**: Repeated behaviors become traditions
- **Leadership**: Natural leaders emerge and gain followers

### 🎭 Cultural Development
- **Mythology**: Agents create stories to explain world events
- **Values**: Collective moral and ethical systems develop
- **Knowledge**: Information spreads and evolves through the population
- **Conflict**: Disagreements lead to debates, negotiations, or conflicts

### 📈 Long-term Evolution
- Population growth through agent reproduction
- Technology and skill development
- Geographical expansion and territory claims
- Multi-generational storytelling and memory

## ⚙️ Configuration

### Creating New Agents

Create a JSON file in `data/agent_configs/`:

```json
{
  "id": "agent_006",
  "name": "YourAgent",
  "age": 25,
  "traits": ["creative", "social", "determined"],
  "goals": ["master artistry", "build community"],
  "current_goal": "master artistry",
  "emotion": "excited",
  "location": "village_center",
  "relationships": {
    "Lara": "friend"
  },
  "skills": {
    "artistry": 0.8,
    "social": 0.6
  }
}
```

### Simulation Settings

Modify these parameters in `main.py` or the simulation engine:

- `tick_delay`: Time between simulation steps
- `interactions_per_day`: How many interactions each agent can have
- `save_interval`: Auto-save frequency
- Memory retention and importance thresholds

## 🛠️ Advanced Features (Coming Soon)

### LLM Integration
- Connect to OpenAI GPT-4, Claude, or Groq for enhanced decision-making
- Natural language conversations between agents
- Dynamic goal and personality evolution

### Agent Reproduction & Genetics
- Agents can form families and have children
- Trait inheritance and genetic combination
- Multi-generational dynamics and family trees

### Advanced Society Features
- Economic systems and resource management
- Complex political structures and governance
- War, diplomacy, and territorial expansion
- Technology development and knowledge trees

### Visualization & Analysis
- Real-time network graphs of relationships
- Timeline visualization of major events
- Population statistics and demographic analysis
- Interactive world map and agent tracking

## 🤝 Contributing

SimuLife is an open-source project! Contributions are welcome:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Areas for Contribution
- LLM integration modules
- New agent behaviors and decision-making logic
- Visualization and analysis tools
- Performance optimizations
- Documentation and examples
- Agent reproduction and genetics system
- Web interface for simulation control

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Inspiration & Vision

SimuLife is inspired by:
- **The Sims** + **Civilization** gameplay
- **Westworld** and **Ex Machina** AI consciousness themes  
- **Academic research** in multi-agent systems and emergent behavior
- **Conway's Game of Life** and cellular automata

Our vision is to create a platform for:
- **AI Research**: Study emergent behavior and social dynamics
- **Storytelling**: Generate rich narratives from agent interactions
- **Education**: Teach concepts of sociology, psychology, and AI
- **Entertainment**: Watch fascinating digital worlds unfold
- **Experimentation**: Test theories about society and human behavior

## 🎯 Roadmap

### Phase 1: Foundation ✅
- [x] Core agent system with memory
- [x] Basic simulation loop
- [x] World state management
- [x] Save/load functionality
- [x] Interactive mode

### Phase 2: Intelligence 🚧
- [ ] LLM integration for decision-making
- [ ] Natural language agent conversations
- [ ] Advanced memory summarization
- [ ] Dynamic personality evolution

### Phase 3: Society 🔮
- [ ] Agent reproduction and families
- [ ] Economic systems
- [ ] Complex faction politics
- [ ] Cultural evolution tracking

### Phase 4: Interface 🔮
- [ ] Web-based simulation viewer
- [ ] Real-time visualization
- [ ] Agent behavior analytics
- [ ] Scenario editor

---

**Start your digital civilization today!** 🌍

```bash
python main.py --interactive
```

*Watch as consciousness emerges from code...*