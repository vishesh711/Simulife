/**
 * SimuLife API Service
 * Handles all communication with the FastAPI backend
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useEffect, useRef, useState } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';

// Type definitions for our API responses
export interface SimulationState {
  day: number;
  population: number;
  phase: string;
  phaseProgress: number;
  isRunning: boolean;
  speed: number;
  totalEvents: number;
  worldStats: {
    totalActivities: number;
    tribalGroups: number;
    technologies: number;
    culturalArtifacts: number;
  };
}

export interface Agent {
  id: string;
  name: string;
  age: number;
  tribe: string;
  position: { x: number; y: number };
  status: 'active' | 'resting' | 'exploring';
  traits: string[];
  relationships: Record<string, string>;
  skills: Record<string, number>;
  memories_count: number;
  emotions: {
    current_mood: string;
    dominant_emotion: string;
    emotional_stability: number;
    empathy_level: number;
  };
  lifePurpose: {
    category: string | null;
    description: string | null;
    clarity: number;
    fulfillment: number;
  };
  familyBonds: {
    children: string[];
    parents: string[];
    siblings: string[];
    partner: string | null;
    bond_strength: number;
  };
}

export interface SimulationEvent {
  id: string;
  type: 'celebration' | 'conflict' | 'discovery' | 'birth';
  title: string;
  description: string;
  timestamp: number;
  agents: string[];
  phase10_category?: string;
}

export interface Phase10Stats {
  phase10_systems: {
    love_romance: {
      active_relationships: number;
      total_events: number;
      pregnancies: number;
    };
    family_bonds: {
      family_units: number;
      total_events: number;
      avg_bond_strength: number;
    };
    emotional_complexity: {
      total_events: number;
      avg_empathy: number;
      emotional_range: number;
    };
    life_purpose: {
      agents_with_purpose: number;
      total_events: number;
      purpose_distribution: Record<string, number>;
    };
  };
}

// API functions
const apiCall = async <T>(endpoint: string, options: RequestInit = {}): Promise<T> => {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
};

// API endpoints
export const simulationApi = {
  getSimulationState: () => apiCall<SimulationState>('/api/simulation'),
  getAgents: () => apiCall<{ agents: Agent[] }>('/api/agents'),
  getEvents: (limit = 20) => apiCall<{ events: SimulationEvent[] }>(`/api/events?limit=${limit}`),
  getPhase10Stats: () => apiCall<Phase10Stats>('/api/phase10'),
  
  controlSimulation: (action: string) =>
    apiCall(`/api/control/${action}`, { method: 'POST' }),
  
  setSimulationSpeed: (speed: number) =>
    apiCall(`/api/control/speed/${speed}`, { method: 'POST' }),
};

// React Query hooks for data fetching
export const useSimulationState = () => {
  return useQuery({
    queryKey: ['simulation'],
    queryFn: simulationApi.getSimulationState,
    refetchInterval: 2000, // Refetch every 2 seconds
    staleTime: 1000, // Data is fresh for 1 second
  });
};

export const useAgents = () => {
  return useQuery({
    queryKey: ['agents'],
    queryFn: simulationApi.getAgents,
    refetchInterval: 3000, // Refetch every 3 seconds
    staleTime: 2000, // Data is fresh for 2 seconds
  });
};

export const useEvents = (limit = 20) => {
  return useQuery({
    queryKey: ['events', limit],
    queryFn: () => simulationApi.getEvents(limit),
    refetchInterval: 1000, // Refetch every 1 second for events
    staleTime: 500, // Data is fresh for 0.5 seconds
  });
};

export const usePhase10Stats = () => {
  return useQuery({
    queryKey: ['phase10'],
    queryFn: simulationApi.getPhase10Stats,
    refetchInterval: 5000, // Refetch every 5 seconds
    staleTime: 3000, // Data is fresh for 3 seconds
  });
};

// Mutation hooks for controlling the simulation
export const useSimulationControl = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (action: string) => simulationApi.controlSimulation(action),
    onSuccess: (data, action) => {
      // Invalidate and refetch simulation data
      queryClient.invalidateQueries({ queryKey: ['simulation'] });
      console.log(`✅ Simulation ${action} successful:`, data);
    },
    onError: (error, action) => {
      console.error(`❌ Simulation ${action} failed:`, error);
    },
  });
};

export const useSimulationSpeed = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (speed: number) => simulationApi.setSimulationSpeed(speed),
    onSuccess: () => {
      // Invalidate and refetch simulation data
      queryClient.invalidateQueries({ queryKey: ['simulation'] });
    },
  });
};

// WebSocket hook for real-time updates
export const useSimulationWebSocket = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const queryClient = useQueryClient();

  useEffect(() => {
    const connect = () => {
      try {
        const ws = new WebSocket(WS_URL);
        wsRef.current = ws;

        ws.onopen = () => {
          console.log('🔗 Connected to SimuLife WebSocket');
          setIsConnected(true);
          setError(null);
        };

        ws.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data);
            setLastMessage(message);

            // Handle different message types
            if (message.type === 'simulation_update') {
              // Update query cache with new data
              if (message.data.simulation) {
                queryClient.setQueryData(['simulation'], message.data.simulation);
              }
              if (message.data.agents) {
                queryClient.setQueryData(['agents'], message.data.agents);
              }
              if (message.data.events) {
                queryClient.setQueryData(['events', 10], message.data.events);
              }
            }
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        ws.onclose = () => {
          console.log('🔌 Disconnected from SimuLife WebSocket');
          setIsConnected(false);
          
          // Attempt to reconnect after 3 seconds
          setTimeout(connect, 3000);
        };

        ws.onerror = (error) => {
          console.error('❌ WebSocket error:', error);
          setError('WebSocket connection error');
        };

      } catch (error) {
        console.error('❌ Failed to create WebSocket connection:', error);
        setError('Failed to connect to WebSocket');
        setTimeout(connect, 5000);
      }
    };

    connect();

    // Cleanup on unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [queryClient]);

  const sendMessage = (message: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  };

  const requestUpdate = () => {
    sendMessage({ type: 'request_update' });
  };

  return {
    isConnected,
    lastMessage,
    error,
    sendMessage,
    requestUpdate,
  };
};

// Helper functions for data processing
export const getAgentStatusColor = (status: string) => {
  switch (status) {
    case 'active':
      return 'bg-green-500';
    case 'resting':
      return 'bg-blue-500';
    case 'exploring':
      return 'bg-yellow-500';
    default:
      return 'bg-gray-500';
  }
};

export const getEventTypeIcon = (type: string) => {
  switch (type) {
    case 'birth':
      return '👶';
    case 'celebration':
      return '🎉';
    case 'conflict':
      return '⚔️';
    case 'discovery':
      return '🔍';
    default:
      return '📝';
  }
};

export const getPhase10CategoryColor = (category: string) => {
  switch (category) {
    case 'romance':
      return 'text-pink-500';
    case 'family':
      return 'text-purple-500';
    case 'emotional':
      return 'text-blue-500';
    case 'purpose':
      return 'text-green-500';
    default:
      return 'text-gray-500';
  }
};

export const formatLifePurpose = (purpose: Agent['lifePurpose']) => {
  if (!purpose.category) return 'Seeking purpose...';
  return `${purpose.category}: ${purpose.description || 'Discovering their path'}`;
};

export const formatEmotionalState = (emotions: Agent['emotions']) => {
  const { current_mood, dominant_emotion, emotional_stability } = emotions;
  return `${current_mood} (${dominant_emotion}) - ${emotional_stability}% stable`;
};

// All types are already exported above with their interface declarations 