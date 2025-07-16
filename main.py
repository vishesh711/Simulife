#!/usr/bin/env python3
"""
SimuLife - Multi-Agent LLM Simulation
Main entry point for running the simulation.

Usage:
    python main.py                    # Run with default settings
    python main.py --days 10         # Run for 10 days
    python main.py --load save_name   # Load a previous simulation
"""

import argparse
import glob
import os
import sys
from typing import List

# Add the simulife package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from simulife.engine.simulation_loop import SimulationEngine
from simulife.agents.base_agent import BaseAgent


def print_welcome():
    """Print the welcome message and simulation info."""
    print("""
🌍 ===== SIMULIFE: Multi-Agent LLM Simulation =====

Welcome to SimuLife - a persistent virtual world where AI agents live,
learn, form relationships, build societies, and evolve over time.

Each agent has:
• Personality traits and emotions
• Vector-based memory (FAISS)
• Goals and motivations  
• Relationships with other agents
• The ability to form factions, beliefs, and customs

Watch as your digital civilization emerges...
    """)


def get_agent_configs(agent_dir: str = "data/agent_configs") -> List[str]:
    """Get all agent configuration files."""
    if not os.path.exists(agent_dir):
        print(f"❌ Agent config directory not found: {agent_dir}")
        return []
    
    config_files = glob.glob(os.path.join(agent_dir, "*.json"))
    if not config_files:
        print(f"❌ No agent config files found in {agent_dir}")
        return []
    
    return config_files


def run_simulation(args):
    """Run the main simulation."""
    print_welcome()
    
    # Get agent configurations
    agent_configs = get_agent_configs()
    if not agent_configs:
        print("Cannot run simulation without agent configurations.")
        return
    
    print(f"📋 Found {len(agent_configs)} agent configurations:")
    for config in agent_configs:
        agent_name = os.path.basename(config).replace('.json', '')
        print(f"   • {agent_name}")
    
    # Initialize simulation engine
    engine = SimulationEngine(
        agent_config_paths=agent_configs,
        save_dir=args.save_dir
    )
    
    # Load previous simulation if requested
    if args.load:
        if engine.load_simulation(args.load):
            print(f"📂 Loaded simulation: {args.load}")
        else:
            print(f"❌ Failed to load simulation: {args.load}")
            return
    
    # Run simulation
    try:
        print(f"\n🚀 Starting simulation for {args.days} days...")
        print("   Press Ctrl+C to pause and save at any time")
        print("=" * 60)
        
        daily_summaries = engine.run_simulation(
            days=args.days,
            verbose=args.verbose,
            save_interval=args.save_interval
        )
        
        print(f"\n✅ Simulation completed successfully!")
        
        # Show final summary
        if args.summary:
            print_final_summary(engine, daily_summaries)
            
    except KeyboardInterrupt:
        print(f"\n⏸️  Simulation interrupted by user")
        print("   All progress has been auto-saved")
    except Exception as e:
        print(f"\n❌ Simulation error: {e}")
        print("   Check your configuration files and try again")


def print_final_summary(engine: SimulationEngine, daily_summaries: List):
    """Print a summary of the simulation results."""
    print("\n" + "=" * 60)
    print("📊 SIMULATION SUMMARY")
    print("=" * 60)
    
    # World statistics
    world = engine.world
    print(f"🌍 World State:")
    print(f"   • Final Day: {world.current_day}")
    print(f"   • Season: {world.season}, Year: {world.year}")
    print(f"   • Weather: {world.weather}")
    print(f"   • Total Events: {len(world.events)}")
    print(f"   • Active Factions: {len(world.factions)}")
    print(f"   • Belief Systems: {len(world.beliefs)}")
    
    # Agent statistics
    print(f"\n👥 Population:")
    alive_agents = [a for a in engine.agents if a.is_alive]
    print(f"   • Total Agents: {len(alive_agents)}")
    
    if alive_agents:
        avg_age = sum(a.age for a in alive_agents) / len(alive_agents)
        print(f"   • Average Age: {avg_age:.1f}")
        
        # Most social agent
        most_social = max(alive_agents, key=lambda a: len(a.relationships))
        print(f"   • Most Social: {most_social.name} ({len(most_social.relationships)} relationships)")
        
        # Most memories
        most_memories = max(alive_agents, key=lambda a: a.memory.get_memory_stats().get('total_memories', 0))
        memory_count = most_memories.memory.get_memory_stats().get('total_memories', 0)
        print(f"   • Most Memories: {most_memories.name} ({memory_count} memories)")
    
    # Recent significant events
    important_events = world.get_important_events(threshold=0.7)
    if important_events:
        print(f"\n🎭 Significant Events:")
        for event in important_events[-3:]:  # Show last 3 important events
            print(f"   • Day {event.day}: {event.description}")
    
    # Factions
    if world.factions:
        print(f"\n🏛️ Factions:")
        for name, faction in world.factions.items():
            print(f"   • {name}: Led by {faction['leader']} ({len(faction['members'])} members)")
    
    print("\n" + "=" * 60)


def interactive_mode(engine: SimulationEngine):
    """Run the simulation in interactive mode."""
    print("\n🎮 Interactive Mode")
    print("Commands: 'run [days]', 'status', 'agent <name>', 'save <name>', 'quit'")
    
    while True:
        try:
            command = input("\nSimuLife> ").strip().split()
            
            if not command:
                continue
            
            if command[0] == 'quit' or command[0] == 'exit':
                break
            elif command[0] == 'run':
                days = int(command[1]) if len(command) > 1 else 1
                engine.run_simulation(days, verbose=True)
            elif command[0] == 'status':
                print(f"\n🌍 World Status:")
                print(f"   Day: {engine.world.current_day}")
                print(f"   Population: {len([a for a in engine.agents if a.is_alive])}")
                print(f"   Factions: {len(engine.world.factions)}")
                print(f"   Recent Events: {len(engine.world.get_recent_events(7))}")
            elif command[0] == 'agent' and len(command) > 1:
                agent_name = command[1]
                summary = engine.get_agent_summary(agent_name)
                if summary:
                    print(f"\n👤 Agent: {agent_name}")
                    print(f"   Age: {summary['basic_info']['age']}")
                    print(f"   Traits: {', '.join(summary['basic_info']['traits'])}")
                    print(f"   Emotion: {summary['basic_info']['emotion']}")
                    print(f"   Goal: {summary['basic_info']['current_goal']}")
                    print(f"   Relationships: {len(summary['social']['relationships'])}")
                    print(f"   Memories: {summary['memory'].get('total_memories', 0)}")
                else:
                    print(f"❌ Agent '{agent_name}' not found")
            elif command[0] == 'save' and len(command) > 1:
                save_name = command[1]
                engine.save_simulation(save_name)
            else:
                print("❌ Unknown command. Try 'run [days]', 'status', 'agent <name>', 'save <name>', or 'quit'")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("👋 Goodbye!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="SimuLife - Multi-Agent LLM Simulation")
    
    parser.add_argument("--days", type=int, default=5,
                       help="Number of days to simulate (default: 5)")
    parser.add_argument("--save-dir", type=str, default="data/saves",
                       help="Directory for save files (default: data/saves)")
    parser.add_argument("--load", type=str,
                       help="Load a previous simulation save")
    parser.add_argument("--save-interval", type=int, default=10,
                       help="Auto-save every N days (default: 10)")
    parser.add_argument("--no-verbose", action="store_false", dest="verbose",
                       help="Disable verbose output")
    parser.add_argument("--no-summary", action="store_false", dest="summary",
                       help="Disable final summary")
    parser.add_argument("--interactive", action="store_true",
                       help="Run in interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive:
        # Interactive mode
        agent_configs = get_agent_configs()
        if not agent_configs:
            return
        
        engine = SimulationEngine(
            agent_config_paths=agent_configs,
            save_dir=args.save_dir
        )
        
        if args.load:
            engine.load_simulation(args.load)
        
        interactive_mode(engine)
    else:
        # Standard simulation mode
        run_simulation(args)


if __name__ == "__main__":
    main() 