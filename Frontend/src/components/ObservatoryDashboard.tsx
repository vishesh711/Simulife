import { useState } from 'react';
import { WorldView3D } from './WorldView3D';
import { CivilizationStatus } from './CivilizationStatus';
import { RecentEvents } from './RecentEvents';
import { MilestoneTracker } from './MilestoneTracker';
import { ControlPanel } from './ControlPanel';
import { AgentInspector } from './AgentInspector';
import { Badge } from './ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Activity, Globe, Users, Clock, Heart, Brain, Home, Target, Wifi, WifiOff, AlertCircle, BarChart3, Swords, TrendingUp, FastForward, Pause, Play, RotateCcw, Settings, Save, Cloud, Skull, Lightbulb } from 'lucide-react';
import { Alert, AlertDescription } from './ui/alert';
import { ScrollArea } from './ui/scroll-area';
import { 
  useSimulationState, 
  useAgents, 
  useEvents, 
  usePhase10Stats,
  useSimulationControl,
  useSimulationWebSocket,
  Agent,
  formatLifePurpose,
  formatEmotionalState
} from '@/services/api';

export const ObservatoryDashboard = () => {
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

  // API hooks
  const { data: simulationData, isLoading: simulationLoading, error: simulationError } = useSimulationState();
  const { data: agentsData, isLoading: agentsLoading, error: agentsError } = useAgents();
  const { data: eventsData, isLoading: eventsLoading, error: eventsError } = useEvents(15);
  const { data: phase10Data, isLoading: phase10Loading, error: phase10Error } = usePhase10Stats();
  const { mutate: controlSimulation } = useSimulationControl();
  const { isConnected: wsConnected, error: wsError } = useSimulationWebSocket();

  // Extract data with fallbacks
  const simulation = simulationData || {
    day: 0,
    population: 0,
    phase: 'Loading...',
    phaseProgress: 0,
    isRunning: false,
    speed: 1,
    totalEvents: 0,
    worldStats: { totalActivities: 0, tribalGroups: 0, technologies: 0, culturalArtifacts: 0 }
  };

  const agents = agentsData?.agents || [];
  const events = eventsData?.events || [];
  const phase10Stats = phase10Data?.phase10_systems;

  // Event handlers
  const handleAgentClick = (agent: Agent) => {
    setSelectedAgent(agent);
  };

  const handleSimulationControl = (action: string) => {
    console.log(`🎮 Control button clicked: ${action}`);
    
    controlSimulation(action, {
      onSuccess: (data) => {
        console.log(`✅ Simulation ${action} successful:`, data);
      },
      onError: (error) => {
        console.error(`❌ Simulation ${action} failed:`, error);
        alert(`Failed to ${action} simulation: ${error.message}`);
      }
    });
  };

  // Placeholder handlers for other functionality
  const handleSave = () => {
    console.log('💾 Save simulation requested');
    alert('Save functionality coming soon!');
  };

  const handleExport = () => {
    console.log('📤 Export data requested'); 
    alert('Export functionality coming soon!');
  };

  const handleAnalytics = () => {
    console.log('📊 Analytics view requested');
    alert('Analytics view coming soon!');
  };

  // Error handling
  const hasError = simulationError || agentsError || eventsError || phase10Error;
  const isLoading = simulationLoading || agentsLoading || eventsLoading || phase10Loading;

  if (hasError) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 p-6">
        <div className="max-w-4xl mx-auto">
          <Alert className="border-red-500 bg-red-500/10">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              <strong>Connection Error:</strong> Unable to connect to SimuLife API. 
              Please ensure the backend server is running on port 8000.
              <br />
              <code className="text-sm mt-2 block">python api_server.py</code>
            </AlertDescription>
          </Alert>
        </div>
      </div>
    );
  }

  const getEventIcon = (type: string) => {
    switch (type) {
      case 'birth':
        return Users;
      case 'death':
        return Skull;
      case 'trade':
        return TrendingUp;
      case 'fight':
        return Swords;
      case 'discovery':
        return Lightbulb;
      case 'technology':
        return Brain;
      case 'artifact':
        return Target;
      case 'relationship':
        return Heart;
      case 'migration':
        return Users;
      case 'settlement':
        return Home;
      default:
        return AlertCircle;
    }
  };

  const getEventStyle = (type: string) => {
    switch (type) {
      case 'birth':
      case 'trade':
      case 'discovery':
      case 'technology':
      case 'artifact':
      case 'relationship':
      case 'settlement':
        return 'event-success';
      case 'death':
      case 'fight':
      case 'migration':
        return 'event-danger';
      default:
        return '';
    }
  };

  const getEventIconColor = (type: string) => {
    switch (type) {
      case 'birth':
      case 'trade':
      case 'discovery':
      case 'technology':
      case 'artifact':
      case 'relationship':
      case 'settlement':
        return 'bg-green-500/20';
      case 'death':
      case 'fight':
      case 'migration':
        return 'bg-red-500/20';
      default:
        return 'bg-slate-700/50';
    }
  };



  return (
    <div className="min-h-screen">
      <div className="dashboard-container">
        {/* Header */}
        <header style={{ gridArea: 'header' }} className="observatory-card">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6 p-6">
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="w-14 h-14 rounded-3xl bg-gradient-to-br from-blue-500 via-purple-600 to-cyan-500 flex items-center justify-center shadow-2xl">
                  <Globe className="h-7 w-7 text-white" />
                </div>
                <div className="absolute -top-1 -right-1">
                  <div className={`status-dot ${wsConnected ? 'status-online' : 'status-offline'}`} />
                </div>
              </div>
              <div>
                <h1 className="text-4xl sm:text-5xl title-gradient">
                  SimuLife Observatory
                </h1>
                <p className="text-slate-400 text-base font-medium mt-1">
                  Real-time Multi-Agent Simulation Monitor
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="badge-modern badge-info">
                Day {simulation.day}
              </div>
              <div className="badge-modern" style={{ backgroundColor: 'rgba(147, 51, 234, 0.1)', color: 'rgb(196, 181, 253)', borderColor: 'rgba(147, 51, 234, 0.3)' }}>
                {simulation.phase}
              </div>
              <div className="text-sm text-slate-400">
                {wsConnected ? 'Connected' : 'Disconnected'}
              </div>
            </div>
          </div>
        </header>

        {/* Sidebar - Civilization Status & Events */}
        <div style={{ gridArea: 'sidebar' }} className="space-y-6">
          {/* Civilization Status */}
          <div className="observatory-card">
            <div className="p-6 border-b border-white/10">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center">
                  <BarChart3 className="h-5 w-5 text-white" />
                </div>
                <div>
                  <div className="section-title">Civilization Status</div>
                  <div className="text-xs text-slate-400">Phase Progress & Metrics</div>
                </div>
              </div>
            </div>
            
            <div className="p-6 space-y-6">
              {/* Current Phase */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="text-sm font-medium text-slate-300">Current Phase</div>
                  <div className="badge-modern" style={{ backgroundColor: 'rgba(147, 51, 234, 0.1)', color: 'rgb(196, 181, 253)', borderColor: 'rgba(147, 51, 234, 0.3)' }}>
                    {simulation.phase}
                  </div>
                </div>
                
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-400">Progress</span>
                    <span className="metric-value text-lg">{simulation.phaseProgress}%</span>
                  </div>
                  <div className="progress-professional h-3">
                    <div 
                      className="h-full rounded-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-1000"
                      style={{ width: `${simulation.phaseProgress}%` }}
                    />
                  </div>
                </div>
                
                <div className="text-xs text-slate-400 bg-slate-800/30 p-3 rounded-lg">
                  Next Milestone: First Trade Exchange
                </div>
              </div>

              {/* Key Metrics */}
              <div className="grid grid-cols-2 gap-4">
                <div className="metric-card">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center">
                      <Users className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <div className="metric-value text-xl">{simulation.population}</div>
                      <div className="metric-label">Population</div>
                      <div className="flex items-center gap-1 text-xs mt-1">
                        <TrendingUp className="h-3 w-3 text-green-400" />
                        <span className="text-green-400 font-medium">+5.2%</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="metric-card">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center">
                      <Users className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <div className="metric-value text-xl">{simulation.worldStats.tribalGroups}</div>
                      <div className="metric-label">Groups</div>
                      <div className="text-xs text-blue-400 font-medium mt-1">Growing</div>
                    </div>
                  </div>
                </div>

                <div className="metric-card">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-red-500 to-orange-600 flex items-center justify-center">
                      <Swords className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <div className="metric-value text-xl">{0}</div>
                      <div className="metric-label">Conflicts</div>
                    </div>
                  </div>
                </div>

                <div className="metric-card">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-pink-500 to-rose-600 flex items-center justify-center">
                      <Heart className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <div className="metric-value text-xl">{agents.filter(a => a.familyBonds?.partner).length}</div>
                      <div className="metric-label">Bonds</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Recent Events */}
          <div className="observatory-card h-[400px]">
            <div className="p-6 border-b border-white/10">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-500 to-amber-600 flex items-center justify-center">
                  <Clock className="h-5 w-5 text-white" />
                </div>
                <div>
                  <div className="section-title">Recent Events</div>
                  <div className="text-xs text-slate-400">Live Activity Feed</div>
                </div>
                <div className="badge-modern badge-info ml-auto">
                  {events.length} total
                </div>
              </div>
            </div>
            
            <ScrollArea className="h-[300px] px-6">
              <div className="space-y-3 py-4">
                {events.length === 0 ? (
                  <div className="flex flex-col items-center justify-center h-32 text-center">
                    <Clock className="h-8 w-8 text-slate-600 mb-2" />
                    <div className="text-sm text-slate-400">No recent events</div>
                    <div className="text-xs text-slate-500">Events will appear here as they happen</div>
                  </div>
                ) : (
                  events.map((event, index) => {
                    const Icon = getEventIcon(event.type);
                    return (
                      <div
                        key={event.id}
                        className={`event-notification ${getEventStyle(event.type)}`}
                        style={{ animationDelay: `${index * 100}ms` }}
                      >
                        <div className="flex items-start gap-3">
                          <div className={`w-8 h-8 rounded-lg bg-slate-800/50 flex items-center justify-center ${getEventIconColor(event.type)}`}>
                            <Icon className="h-4 w-4" />
                          </div>
                          
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-1">
                              <div className={`badge-modern text-xs capitalize ${getEventIconColor(event.type)}`}>
                                {event.type}
                              </div>
                              <div className="text-xs text-slate-500">
                                Just now
                              </div>
                            </div>
                            
                            <div className="text-sm text-slate-200 leading-relaxed mb-2">
                              {event.description}
                            </div>
                            
                            {event.agents && event.agents.length > 0 && (
                              <div className="flex items-center gap-2">
                                <div className="text-xs text-slate-500">Agents:</div>
                                <div className="flex gap-1">
                                  {event.agents.map((agent, i) => (
                                    <div 
                                      key={i} 
                                      className="badge-modern text-xs"
                                    >
                                      {agent}
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </ScrollArea>
          </div>
        </div>

        {/* Main Content - 3D World */}
        <div style={{ gridArea: 'main' }} className="observatory-card">
          <div className="p-6 border-b border-white/10">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center">
                <Globe className="h-5 w-5 text-white" />
              </div>
              <div>
                <div className="section-title">3D World Observatory</div>
                <div className="text-xs text-slate-400">Interactive Simulation Environment</div>
              </div>
              {isLoading && (
                <div className="badge-modern badge-warning ml-auto">
                  Loading...
                </div>
              )}
            </div>
          </div>
          <div className="p-6">
            <div className="world-container h-[600px]">
              <WorldView3D
                agents={agents}
                onAgentClick={handleAgentClick}
                isRunning={simulation.isRunning}
              />
            </div>
          </div>
        </div>

        {/* Metrics & Controls */}
        <div style={{ gridArea: 'metrics' }} className="space-y-6">
          {/* Key Metrics */}
          <div className="observatory-card">
            <div className="p-6 border-b border-white/10">
              <div className="section-title">Key Metrics</div>
              <div className="text-xs text-slate-400">System Overview</div>
            </div>
            <div className="p-6 space-y-4">
              <div className="metric-card">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center">
                    <Activity className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <div className="metric-value">{simulation.totalEvents}</div>
                    <div className="metric-label">Total Events</div>
                  </div>
                </div>
              </div>

              <div className="metric-card">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-violet-600 flex items-center justify-center">
                    <Brain className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <div className="metric-value">{simulation.worldStats.technologies}</div>
                    <div className="metric-label">Technologies</div>
                  </div>
                </div>
              </div>

              <div className="metric-card">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-500 to-red-600 flex items-center justify-center">
                    <Target className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <div className="metric-value">{simulation.worldStats.culturalArtifacts}</div>
                    <div className="metric-label">Cultural Artifacts</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Phase 10 Statistics */}
          {phase10Stats && (
            <div className="observatory-card">
              <div className="p-6 border-b border-white/10">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-pink-500 to-rose-600 flex items-center justify-center">
                    <Heart className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <div className="section-title">Deep Human Emotions</div>
                    <div className="text-xs text-slate-400">Phase 10 Systems</div>
                  </div>
                </div>
              </div>
              <div className="p-6">
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-4 rounded-lg bg-pink-500/5 border border-pink-500/20">
                    <div className="metric-value text-pink-300">
                      {phase10Stats.love_romance.active_relationships || 0}
                    </div>
                    <div className="metric-label">Relationships</div>
                  </div>
                  <div className="text-center p-4 rounded-lg bg-purple-500/5 border border-purple-500/20">
                    <div className="metric-value text-purple-300">
                      {phase10Stats.family_bonds.family_units || 0}
                    </div>
                    <div className="metric-label">Families</div>
                  </div>
                  <div className="text-center p-4 rounded-lg bg-blue-500/5 border border-blue-500/20">
                    <div className="metric-value text-blue-300">
                      {Math.round(phase10Stats.emotional_complexity.avg_empathy) || 0}%
                    </div>
                    <div className="metric-label">Avg Empathy</div>
                  </div>
                  <div className="text-center p-4 rounded-lg bg-cyan-500/5 border border-cyan-500/20">
                    <div className="metric-value text-cyan-300">
                      {phase10Stats.life_purpose.agents_with_purpose || 0}
                    </div>
                    <div className="metric-label">Found Purpose</div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Control Panel */}
          <div className="observatory-card">
            <div className="p-6 border-b border-white/10">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center">
                  <Settings className="h-5 w-5 text-white" />
                </div>
                <div>
                  <div className="section-title">Control Panel</div>
                  <div className="text-xs text-slate-400">Simulation Controls</div>
                </div>
                <div className={`badge-modern ml-auto ${simulation.isRunning ? 'badge-success' : 'badge-warning'}`}>
                  {simulation.isRunning ? 'Running' : 'Paused'}
                </div>
              </div>
            </div>
            <div className="p-6 space-y-6">
              {/* Primary Controls */}
              <div className="space-y-3">
                <div className="text-sm font-medium text-slate-300">Simulation Control</div>
                <div className="grid grid-cols-1 gap-3">
                  <button
                    onClick={() => handleSimulationControl(simulation.isRunning ? 'pause' : 'start')}
                    className={`control-button px-4 py-3 rounded-lg flex items-center justify-center gap-2 ${
                      simulation.isRunning ? 'bg-orange-500/10 border-orange-500/30' : 'bg-green-500/10 border-green-500/30'
                    }`}
                  >
                    {simulation.isRunning ? (
                      <>
                        <Pause className="w-4 h-4" />
                        Pause
                      </>
                    ) : (
                      <>
                        <Play className="w-4 h-4" />
                        Play
                      </>
                    )}
                  </button>
                  
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      onClick={() => handleSimulationControl('step')}
                      className="control-button px-3 py-2 rounded-lg flex items-center justify-center gap-2 text-sm"
                    >
                      <FastForward className="w-3 h-3" />
                      Step
                    </button>
                    
                    <button
                      onClick={() => handleSimulationControl('stop')}
                      className="control-button px-3 py-2 rounded-lg flex items-center justify-center gap-2 text-sm"
                    >
                      <RotateCcw className="w-3 h-3" />
                      Stop
                    </button>
                  </div>
                </div>
              </div>

              {/* Data Management */}
              <div className="space-y-3">
                <div className="text-sm font-medium text-slate-300">Data Management</div>
                <div className="grid grid-cols-2 gap-2">
                  <button onClick={handleSave} className="control-button px-3 py-2 rounded-lg flex items-center justify-center gap-2 text-sm">
                    <Save className="w-3 h-3" />
                    Save
                  </button>
                  
                  <button onClick={handleExport} className="control-button px-3 py-2 rounded-lg flex items-center justify-center gap-2 text-sm">
                    <Cloud className="w-3 h-3" />
                    Export
                  </button>
                </div>
                
                <button onClick={handleAnalytics} className="control-button w-full px-3 py-2 rounded-lg flex items-center justify-center gap-2 text-sm">
                  <BarChart3 className="w-3 h-3" />
                  View Analytics
                </button>
              </div>

              {/* System Status */}
              <div className="space-y-3">
                <div className="text-sm font-medium text-slate-300">System Status</div>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Speed</span>
                    <span className="text-white">Normal</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Memory</span>
                    <span className="text-white">47.2 MB</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">CPU</span>
                    <span className="text-white">12.4%</span>
                  </div>
                </div>
                
                <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-3">
                  <div className="text-xs font-medium text-green-300 mb-1">System Running Normally</div>
                  <div className="text-xs text-slate-400">All agents active and responding. Memory systems stable.</div>
                </div>
              </div>
            </div>
          </div>

          {/* Milestone Tracker */}
          <div className="observatory-card">
            <div className="p-6 border-b border-white/10">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-yellow-500 to-orange-600 flex items-center justify-center">
                  <Target className="h-5 w-5 text-white" />
                </div>
                <div>
                  <div className="section-title">Civilization Milestones</div>
                  <div className="text-xs text-slate-400">Progress Tracker</div>
                </div>
                <div className="badge-modern badge-info ml-auto">
                  17/19
                </div>
              </div>
            </div>
            <div className="p-6">
              <MilestoneTracker />
            </div>
          </div>
        </div>

        {/* Agent Inspector Modal */}
        {selectedAgent && (
          <AgentInspector
            agent={{
              ...selectedAgent,
              position: selectedAgent.position,
              status: selectedAgent.status,
              traits: selectedAgent.traits,
              relationships: selectedAgent.relationships,
              age: selectedAgent.age,
              skills: selectedAgent.skills || {},
              memories_count: selectedAgent.memories_count || 0
            }}
            onClose={() => setSelectedAgent(null)}
          />
        )}
      </div>
    </div>
  );
};