import { useState, useEffect } from 'react';
import { WorldView3D } from './WorldView3D';
import { CivilizationStatus } from './CivilizationStatus';
import { RecentEvents } from './RecentEvents';
import { MilestoneTracker } from './MilestoneTracker';
import { ControlPanel } from './ControlPanel';
import { AgentInspector } from './AgentInspector';
import { Badge } from './ui/badge';
import { Activity, Globe, Users, Clock } from 'lucide-react';

interface Agent {
  id: string;
  name: string;
  tribe: string;
  position: { x: number; y: number };
  status: 'active' | 'resting' | 'exploring';
  traits: string[];
  relationships: Record<string, string>;
}

interface SimulationState {
  day: number;
  population: number;
  phase: string;
  phaseProgress: number;
  isRunning: boolean;
  speed: number;
  agents: Agent[];
  events: Array<{
    id: string;
    type: 'celebration' | 'conflict' | 'discovery' | 'birth';
    title: string;
    description: string;
    timestamp: number;
    agents: string[];
  }>;
}

export const ObservatoryDashboard = () => {
  const [simulationState, setSimulationState] = useState<SimulationState>({
    day: 347,
    population: 127,
    phase: 'Tribal Formation',
    phaseProgress: 80,
    isRunning: true,
    speed: 1,
    agents: [
      {
        id: 'agent_001',
        name: 'Kira',
        tribe: 'Storm Tribe',
        position: { x: 45, y: 60 },
        status: 'active',
        traits: ['curious', 'brave', 'kind'],
        relationships: { 'agent_002': 'partner', 'agent_003': 'daughter' }
      },
      {
        id: 'agent_002',
        name: 'Zane',
        tribe: 'Storm Tribe',
        position: { x: 47, y: 62 },
        status: 'active',
        traits: ['protective', 'skilled', 'social'],
        relationships: { 'agent_001': 'partner', 'agent_003': 'daughter' }
      },
      {
        id: 'agent_003',
        name: 'Aria',
        tribe: 'Storm Tribe',
        position: { x: 46, y: 61 },
        status: 'resting',
        traits: ['young', 'learning', 'curious'],
        relationships: { 'agent_001': 'mother', 'agent_002': 'father' }
      }
    ],
    events: [
      {
        id: 'event_001',
        type: 'celebration',
        title: 'Kira and Zane formed partnership',
        description: 'A deep bond has formed between these two agents, marking the beginning of a new family unit.',
        timestamp: Date.now() - 300000,
        agents: ['Kira', 'Zane']
      },
      {
        id: 'event_002',
        type: 'conflict',
        title: 'Storm Tribe vs River Tribe',
        description: 'Territorial dispute over fishing grounds escalates into open conflict.',
        timestamp: Date.now() - 600000,
        agents: ['Kira', 'Thom', 'River Leader']
      },
      {
        id: 'event_003',
        type: 'discovery',
        title: 'New tool: Sharp Stone invented',
        description: 'Innovative toolmaking breakthrough increases hunting efficiency.',
        timestamp: Date.now() - 900000,
        agents: ['Kira']
      },
      {
        id: 'event_004',
        type: 'birth',
        title: 'New birth: Aria (Kira\'s child)',
        description: 'The first child born to the Storm Tribe, representing hope for the future.',
        timestamp: Date.now() - 1200000,
        agents: ['Kira', 'Zane', 'Aria']
      }
    ]
  });

  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

  // Simulate real-time updates
  useEffect(() => {
    if (!simulationState.isRunning) return;

    const interval = setInterval(() => {
      setSimulationState(prev => ({
        ...prev,
        agents: prev.agents.map(agent => ({
          ...agent,
          position: {
            x: Math.max(0, Math.min(100, agent.position.x + (Math.random() - 0.5) * 2)),
            y: Math.max(0, Math.min(100, agent.position.y + (Math.random() - 0.5) * 2))
          }
        }))
      }));
    }, 2000);

    return () => clearInterval(interval);
  }, [simulationState.isRunning]);

  const handleAgentClick = (agent: Agent) => {
    setSelectedAgent(agent);
  };

  const handleSimulationControl = (action: string) => {
    switch (action) {
      case 'play':
        setSimulationState(prev => ({ ...prev, isRunning: true }));
        break;
      case 'pause':
        setSimulationState(prev => ({ ...prev, isRunning: false }));
        break;
      case 'fast':
        setSimulationState(prev => ({ ...prev, speed: prev.speed === 3 ? 1 : 3 }));
        break;
      case 'restart':
        // Reset simulation logic here
        break;
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Professional Observatory Header */}
      <div className="observatory-header">
        <div className="flex items-center gap-6">
          <Globe className="w-8 h-8 text-electric-blue animate-pulse-glow" />
          <div>
            <h1 className="text-2xl font-display text-foreground">SimuLife Observatory</h1>
            <p className="text-sm text-muted-foreground font-medium">Digital Civilization Monitoring Station</p>
          </div>
        </div>
        
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-status-active/10 border border-status-active/20">
            <Activity className="w-3 h-3 text-status-active animate-pulse" />
            <span className="text-sm font-medium text-status-active">Live</span>
          </div>
          <div className="flex items-center gap-4 text-sm font-mono-data">
            <div className="flex items-center gap-1">
              <span className="text-muted-foreground">Day</span>
              <span className="text-foreground font-semibold">{simulationState.day}</span>
            </div>
            <div className="flex items-center gap-1">
              <span className="text-muted-foreground">Pop</span>
              <span className="text-foreground font-semibold">{simulationState.population}</span>
            </div>
            <div className="flex items-center gap-1">
              <span className="text-muted-foreground">Phase</span>
              <span className="text-electric-blue font-semibold">{simulationState.phase}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Dashboard Grid */}
      <div className="p-6 grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {/* 3D World View - Takes up 2 columns on xl screens */}
        <div className="xl:col-span-2">
          <WorldView3D 
            agents={simulationState.agents}
            onAgentClick={handleAgentClick}
            isRunning={simulationState.isRunning}
          />
        </div>

        {/* Civilization Status */}
        <div className="xl:col-span-1">
          <CivilizationStatus 
            phase={simulationState.phase}
            phaseProgress={simulationState.phaseProgress}
            population={simulationState.population}
            activeGroups={4}
            conflicts={2}
            relationships={847}
          />
        </div>

        {/* Recent Events */}
        <div className="lg:col-span-1">
          <RecentEvents events={simulationState.events} />
        </div>

        {/* Milestone Tracker */}
        <div className="lg:col-span-1">
          <MilestoneTracker />
        </div>

        {/* Control Panel */}
        <div className="lg:col-span-2 xl:col-span-1">
          <ControlPanel 
            isRunning={simulationState.isRunning}
            speed={simulationState.speed}
            onControl={handleSimulationControl}
          />
        </div>
      </div>

      {/* Agent Inspector Modal */}
      {selectedAgent && (
        <AgentInspector 
          agent={selectedAgent}
          onClose={() => setSelectedAgent(null)}
        />
      )}
    </div>
  );
};