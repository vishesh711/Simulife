"""
SimuLife API Server
FastAPI backend to serve simulation data to the frontend dashboard
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
import json
import uvicorn
from typing import List, Dict, Any, Optional
from datetime import datetime
import os

# Import our SimuLife components
from simulife.engine.simulation_loop import SimulationEngine
from simulife.engine.world_state import WorldState
from simulife.agents.base_agent import BaseAgent

app = FastAPI(title="SimuLife API", description="Real-time simulation data API", version="1.0.0")

# CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global simulation state
simulation_engine: Optional[SimulationEngine] = None
world_state: Optional[WorldState] = None
is_running: bool = False
simulation_speed: float = 1.0
connected_clients: List[WebSocket] = []

@app.on_event("startup")
async def startup_event():
    """Initialize the simulation on startup"""
    global simulation_engine, world_state
    
    # Check if we have a config file
    if not os.path.exists("config.py"):
        print("⚠️  Warning: No config.py found. Please copy config.py.example to config.py and add your API key.")
        print("   The API server will still run but simulation features requiring LLM will be disabled.")
    
    try:
        simulation_engine = SimulationEngine()
        world_state = simulation_engine.world_state
        print("✅ SimuLife API Server initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize simulation: {e}")
        print("   API server will run with mock data only.")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "SimuLife API Server",
        "version": "1.0.0",
        "status": "running",
        "simulation_active": is_running,
        "endpoints": {
            "simulation": "/api/simulation",
            "agents": "/api/agents",
            "events": "/api/events",
            "phase10": "/api/phase10",
            "control": "/api/control",
            "websocket": "/ws"
        }
    }

@app.get("/api/simulation")
async def get_simulation_state():
    """Get current simulation state"""
    global world_state, is_running, simulation_speed
    
    if world_state is None:
        return get_mock_simulation_state()
    
    try:
        agents = world_state.agents
        return {
            "day": world_state.current_day,
            "population": len(agents),
            "phase": world_state.current_phase,
            "phaseProgress": min(95, world_state.current_day * 2),  # Mock progress
            "isRunning": is_running,
            "speed": simulation_speed,
            "totalEvents": len(world_state.event_history),
            "worldStats": {
                "totalActivities": len(world_state.event_history),
                "tribalGroups": len(set(agent.tribe for agent in agents if hasattr(agent, 'tribe'))),
                "technologies": len(getattr(world_state, 'technologies', [])),
                "culturalArtifacts": len(getattr(world_state, 'cultural_artifacts', []))
            }
        }
    except Exception as e:
        print(f"Error getting simulation state: {e}")
        return get_mock_simulation_state()

@app.get("/api/agents")
async def get_agents():
    """Get all agents with their current state"""
    global world_state
    
    if world_state is None:
        return get_mock_agents()
    
    try:
        agents_data = []
        for agent in world_state.agents:
            # Get Phase 10 emotional data
            emotions = getattr(agent, 'emotions', {})
            life_purpose = getattr(agent, 'life_purpose', None)
            family_bonds = getattr(agent, 'family_bonds', {})
            
            agent_data = {
                "id": agent.id,
                "name": agent.name,
                "age": agent.age,
                "tribe": getattr(agent, 'tribe', 'Independent'),
                "position": {
                    "x": getattr(agent, 'x', 50),
                    "y": getattr(agent, 'y', 50)
                },
                "status": getattr(agent, 'status', 'active'),
                "traits": agent.traits if hasattr(agent, 'traits') else [],
                "relationships": getattr(agent, 'relationships', {}),
                "skills": getattr(agent, 'skills', {}),
                "memories_count": len(agent.memory_manager.memories) if hasattr(agent, 'memory_manager') else 0,
                
                # Phase 10 Data
                "emotions": {
                    "current_mood": emotions.get('current_mood', 'neutral'),
                    "dominant_emotion": emotions.get('dominant_emotion', 'calm'),
                    "emotional_stability": emotions.get('stability', 70),
                    "empathy_level": emotions.get('empathy', 50)
                },
                "lifePurpose": {
                    "category": life_purpose.get('category') if life_purpose else None,
                    "description": life_purpose.get('description') if life_purpose else None,
                    "clarity": life_purpose.get('clarity', 0) if life_purpose else 0,
                    "fulfillment": life_purpose.get('fulfillment', 0) if life_purpose else 0
                },
                "familyBonds": {
                    "children": family_bonds.get('children', []),
                    "parents": family_bonds.get('parents', []),
                    "siblings": family_bonds.get('siblings', []),
                    "partner": family_bonds.get('partner'),
                    "bond_strength": family_bonds.get('total_strength', 0)
                }
            }
            agents_data.append(agent_data)
        
        return {"agents": agents_data}
    except Exception as e:
        print(f"Error getting agents: {e}")
        return get_mock_agents()

@app.get("/api/events")
async def get_recent_events(limit: int = 20):
    """Get recent simulation events"""
    global world_state
    
    if world_state is None:
        return get_mock_events()
    
    try:
        recent_events = world_state.event_history[-limit:] if world_state.event_history else []
        
        events_data = []
        for event in recent_events:
            event_data = {
                "id": f"event_{len(events_data)}",
                "type": categorize_event_type(event.get('type', 'discovery')),
                "title": event.get('title', 'Unknown Event'),
                "description": event.get('description', ''),
                "timestamp": event.get('timestamp', datetime.now().timestamp() * 1000),
                "agents": event.get('agents', []),
                "phase10_category": get_phase10_category(event)
            }
            events_data.append(event_data)
        
        return {"events": events_data}
    except Exception as e:
        print(f"Error getting events: {e}")
        return get_mock_events()

@app.get("/api/phase10")
async def get_phase10_stats():
    """Get Phase 10 specific statistics"""
    global world_state
    
    if world_state is None:
        return get_mock_phase10_stats()
    
    try:
        agents = world_state.agents
        
        # Count Phase 10 activities
        romance_events = len([e for e in world_state.event_history if 'romance' in str(e).lower() or 'love' in str(e).lower()])
        family_events = len([e for e in world_state.event_history if 'family' in str(e).lower() or 'bond' in str(e).lower()])
        emotional_events = len([e for e in world_state.event_history if 'emotion' in str(e).lower() or 'empathy' in str(e).lower()])
        purpose_events = len([e for e in world_state.event_history if 'purpose' in str(e).lower() or 'meaning' in str(e).lower()])
        
        # Life purpose distribution
        purpose_distribution = {}
        for agent in agents:
            life_purpose = getattr(agent, 'life_purpose', None)
            if life_purpose and life_purpose.get('category'):
                category = life_purpose['category']
                purpose_distribution[category] = purpose_distribution.get(category, 0) + 1
        
        return {
            "phase10_systems": {
                "love_romance": {
                    "active_relationships": len([a for a in agents if getattr(a, 'partner', None)]),
                    "total_events": romance_events,
                    "pregnancies": len([a for a in agents if getattr(a, 'is_pregnant', False)])
                },
                "family_bonds": {
                    "family_units": len(set(getattr(a, 'family_id', a.id) for a in agents)),
                    "total_events": family_events,
                    "avg_bond_strength": sum(getattr(a, 'family_bonds', {}).get('total_strength', 0) for a in agents) / max(len(agents), 1)
                },
                "emotional_complexity": {
                    "total_events": emotional_events,
                    "avg_empathy": sum(getattr(a, 'emotions', {}).get('empathy', 50) for a in agents) / max(len(agents), 1),
                    "emotional_range": len(set(getattr(a, 'emotions', {}).get('dominant_emotion', 'neutral') for a in agents))
                },
                "life_purpose": {
                    "agents_with_purpose": len([a for a in agents if getattr(a, 'life_purpose', None)]),
                    "total_events": purpose_events,
                    "purpose_distribution": purpose_distribution
                }
            }
        }
    except Exception as e:
        print(f"Error getting Phase 10 stats: {e}")
        return get_mock_phase10_stats()

@app.post("/api/control/{action}")
async def control_simulation(action: str):
    """Control simulation (start, stop, pause, step)"""
    global is_running, simulation_speed
    
    if action == "start":
        is_running = True
        await broadcast_message({"type": "simulation_control", "action": "started"})
        return {"status": "started", "isRunning": True}
    elif action == "stop":
        is_running = False
        await broadcast_message({"type": "simulation_control", "action": "stopped"})
        return {"status": "stopped", "isRunning": False}
    elif action == "pause":
        is_running = False
        await broadcast_message({"type": "simulation_control", "action": "paused"})
        return {"status": "paused", "isRunning": False}
    elif action == "step":
        # Run one simulation step
        if simulation_engine:
            try:
                simulation_engine.run_single_day()
                await broadcast_simulation_update()
                return {"status": "step_complete", "day": world_state.current_day if world_state else 0}
            except Exception as e:
                return {"status": "error", "message": str(e)}
    else:
        return {"status": "error", "message": f"Unknown action: {action}"}

@app.post("/api/control/speed/{speed}")
async def set_simulation_speed(speed: float):
    """Set simulation speed"""
    global simulation_speed
    simulation_speed = max(0.1, min(10.0, speed))  # Clamp between 0.1x and 10x
    await broadcast_message({"type": "speed_change", "speed": simulation_speed})
    return {"status": "speed_set", "speed": simulation_speed}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    connected_clients.append(websocket)
    
    try:
        # Send initial data
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to SimuLife API"
        })
        
        # Keep connection alive and handle messages
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                if message.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
                elif message.get("type") == "request_update":
                    await send_simulation_update(websocket)
                    
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "message": "Invalid JSON"})
            except Exception as e:
                await websocket.send_json({"type": "error", "message": str(e)})
                
    except WebSocketDisconnect:
        pass
    finally:
        if websocket in connected_clients:
            connected_clients.remove(websocket)

async def broadcast_message(message: dict):
    """Broadcast message to all connected clients"""
    if connected_clients:
        disconnected = []
        for client in connected_clients:
            try:
                await client.send_json(message)
            except WebSocketDisconnect:
                disconnected.append(client)
            except Exception:
                disconnected.append(client)
        
        # Remove disconnected clients
        for client in disconnected:
            if client in connected_clients:
                connected_clients.remove(client)

async def broadcast_simulation_update():
    """Broadcast simulation state update to all clients"""
    try:
        simulation_data = await get_simulation_state()
        agents_data = await get_agents()
        events_data = await get_recent_events(10)
        
        update_message = {
            "type": "simulation_update",
            "data": {
                "simulation": simulation_data,
                "agents": agents_data,
                "events": events_data
            }
        }
        
        await broadcast_message(update_message)
    except Exception as e:
        print(f"Error broadcasting simulation update: {e}")

async def send_simulation_update(websocket: WebSocket):
    """Send simulation update to specific client"""
    try:
        simulation_data = await get_simulation_state()
        agents_data = await get_agents()
        events_data = await get_recent_events(10)
        
        await websocket.send_json({
            "type": "simulation_update",
            "data": {
                "simulation": simulation_data,
                "agents": agents_data,
                "events": events_data
            }
        })
    except Exception as e:
        print(f"Error sending simulation update: {e}")

# Utility functions for data processing
def categorize_event_type(event_type: str) -> str:
    """Categorize event type for frontend"""
    event_type = event_type.lower()
    if any(word in event_type for word in ['birth', 'born', 'child']):
        return 'birth'
    elif any(word in event_type for word in ['conflict', 'fight', 'war', 'dispute']):
        return 'conflict'
    elif any(word in event_type for word in ['celebration', 'festival', 'party', 'joy']):
        return 'celebration'
    else:
        return 'discovery'

def get_phase10_category(event: dict) -> Optional[str]:
    """Determine if event belongs to Phase 10 systems"""
    description = str(event.get('description', '')).lower()
    if any(word in description for word in ['love', 'romance', 'attraction', 'marriage']):
        return 'romance'
    elif any(word in description for word in ['family', 'parent', 'child', 'sibling']):
        return 'family'
    elif any(word in description for word in ['emotion', 'empathy', 'feeling', 'mood']):
        return 'emotional'
    elif any(word in description for word in ['purpose', 'meaning', 'calling', 'mission']):
        return 'purpose'
    return None

# Mock data functions for when simulation is not available
def get_mock_simulation_state():
    return {
        "day": 347,
        "population": 8,
        "phase": "Phase 10: Deep Human Emotions",
        "phaseProgress": 85,
        "isRunning": False,
        "speed": 1.0,
        "totalEvents": 156,
        "worldStats": {
            "totalActivities": 156,
            "tribalGroups": 2,
            "technologies": 15,
            "culturalArtifacts": 8
        }
    }

def get_mock_agents():
    return {
        "agents": [
            {
                "id": "aedan",
                "name": "Aedan",
                "age": 45,
                "tribe": "Storm Tribe",
                "position": {"x": 45, "y": 60},
                "status": "active",
                "traits": ["curious", "brave", "leader"],
                "relationships": {"kara": "partner", "nyla": "daughter"},
                "skills": {"hunting": 85, "leadership": 90, "toolmaking": 70},
                "memories_count": 234,
                "emotions": {
                    "current_mood": "content",
                    "dominant_emotion": "protective",
                    "emotional_stability": 85,
                    "empathy_level": 75
                },
                "lifePurpose": {
                    "category": "Leader",
                    "description": "Guide and protect the tribe",
                    "clarity": 90,
                    "fulfillment": 85
                },
                "familyBonds": {
                    "children": ["nyla"],
                    "parents": [],
                    "siblings": [],
                    "partner": "kara",
                    "bond_strength": 95
                }
            }
        ]
    }

def get_mock_events():
    return {
        "events": [
            {
                "id": "event_001",
                "type": "celebration",
                "title": "Aedan and Kara's bond deepened",
                "description": "Their relationship has grown stronger through shared experiences and mutual support.",
                "timestamp": datetime.now().timestamp() * 1000,
                "agents": ["Aedan", "Kara"],
                "phase10_category": "romance"
            }
        ]
    }

def get_mock_phase10_stats():
    return {
        "phase10_systems": {
            "love_romance": {
                "active_relationships": 3,
                "total_events": 12,
                "pregnancies": 1
            },
            "family_bonds": {
                "family_units": 2,
                "total_events": 18,
                "avg_bond_strength": 82
            },
            "emotional_complexity": {
                "total_events": 25,
                "avg_empathy": 68,
                "emotional_range": 6
            },
            "life_purpose": {
                "agents_with_purpose": 5,
                "total_events": 8,
                "purpose_distribution": {
                    "Leader": 2,
                    "Creator": 1,
                    "Protector": 1,
                    "Teacher": 1
                }
            }
        }
    }

# Background task for running simulation
async def simulation_loop():
    """Background task that runs the simulation"""
    while True:
        if is_running and simulation_engine:
            try:
                simulation_engine.run_single_day()
                await broadcast_simulation_update()
                await asyncio.sleep(1.0 / simulation_speed)  # Adjust speed
            except Exception as e:
                print(f"Error in simulation loop: {e}")
                await asyncio.sleep(1.0)
        else:
            await asyncio.sleep(0.1)

# Start background task
@app.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(simulation_loop())

if __name__ == "__main__":
    print("🚀 Starting SimuLife API Server...")
    print("📊 Dashboard will be available at: http://localhost:8000")
    print("🌐 API docs available at: http://localhost:8000/docs")
    print("⚡ WebSocket endpoint: ws://localhost:8000/ws")
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 