import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { ScrollArea } from './ui/scroll-area';
import { Trophy, CheckCircle, Circle, Clock, Target } from 'lucide-react';
import { useSimulationState, useAgents, usePhase10Stats } from '@/services/api';

interface Milestone {
  id: string;
  title: string;
  description: string;
  status: 'completed' | 'in-progress' | 'upcoming';
  progress?: number;
  completedAt?: number;
  category: 'social' | 'technological' | 'cultural' | 'biological' | 'phase10';
}

export const MilestoneTracker = () => {
  const { data: simulationData } = useSimulationState();
  const { data: agentsData } = useAgents();
  const { data: phase10Data } = usePhase10Stats();

  const simulation = simulationData || { day: 0, population: 0, phase: '', phaseProgress: 0 };
  const agents = agentsData?.agents || [];
  const phase10Stats = phase10Data?.phase10_systems;

  // Generate dynamic milestones based on actual simulation state
  const generateMilestones = (): Milestone[] => {
    const milestones: Milestone[] = [];
    
    // Basic Population Milestones
    milestones.push({
      id: 'pop_5',
      title: 'Population of 5',
      description: 'The initial group reaches 5 agents.',
      status: simulation.population >= 5 ? 'completed' : 'upcoming',
      category: 'biological'
    });

    if (simulation.population >= 5) {
      milestones.push({
        id: 'pop_10',
        title: 'Population Growth',
        description: 'Population expands to 10 agents through reproduction.',
        status: simulation.population >= 10 ? 'completed' : simulation.population > 5 ? 'in-progress' : 'upcoming',
        progress: simulation.population > 5 ? Math.min(100, ((simulation.population - 5) / 5) * 100) : 0,
        category: 'biological'
      });
    }

    // Phase Milestones
    const phaseNumber = extractPhaseNumber(simulation.phase);
    
    for (let i = 1; i <= 10; i++) {
      const phaseNames = {
        1: 'Basic Survival',
        2: 'Resource Discovery', 
        3: 'Social Formation',
        4: 'Specialization',
        5: 'Inter-Tribal Contact',
        6: 'Crisis Management',
        7: 'Population Dynamics',
        8: 'Emergent Phenomena',
        9: 'Advanced AI & Meta-Cognition',
        10: 'Deep Human Emotions'
      };

      milestones.push({
        id: `phase_${i}`,
        title: `Phase ${i}: ${phaseNames[i as keyof typeof phaseNames]}`,
        description: `Civilization advances to Phase ${i}.`,
        status: phaseNumber > i ? 'completed' : phaseNumber === i ? 'in-progress' : 'upcoming',
        progress: phaseNumber === i ? simulation.phaseProgress : undefined,
        category: i <= 5 ? 'social' : i <= 8 ? 'technological' : 'phase10'
      });
    }

    // Phase 10 Specific Milestones
    if (phase10Stats) {
      milestones.push({
        id: 'first_romance',
        title: 'First Romantic Bond',
        description: 'Agents develop romantic attraction and partnership.',
        status: phase10Stats.love_romance.active_relationships > 0 ? 'completed' : 'upcoming',
        category: 'phase10'
      });

      milestones.push({
        id: 'family_formation',
        title: 'Family Formation',
        description: 'Strong family bonds and units emerge.',
        status: phase10Stats.family_bonds.family_units > 1 ? 'completed' : 'upcoming',
        category: 'phase10'
      });

      milestones.push({
        id: 'emotional_awareness',
        title: 'Emotional Awareness',
        description: 'Agents develop empathy and emotional intelligence.',
        status: phase10Stats.emotional_complexity.avg_empathy > 60 ? 'completed' : 'in-progress',
        progress: Math.min(100, phase10Stats.emotional_complexity.avg_empathy),
        category: 'phase10'
      });

      milestones.push({
        id: 'life_purpose',
        title: 'Life Purpose Discovery',
        description: 'Agents find meaning and purpose in their existence.',
        status: phase10Stats.life_purpose.agents_with_purpose > 0 ? 'completed' : 'upcoming',
        category: 'phase10'
      });

      if (phase10Stats.love_romance.pregnancies > 0) {
        milestones.push({
          id: 'new_generation',
          title: 'New Generation',
          description: 'First children born through Phase 10 reproduction system.',
          status: 'completed',
          category: 'phase10'
        });
      }
    }

    // Survival Milestones based on simulation days
    if (simulation.day >= 30) {
      milestones.push({
        id: 'survival_30',
        title: '30 Days Survival',
        description: 'The civilization survives its first month.',
        status: 'completed',
        category: 'biological'
      });
    }

    if (simulation.day >= 100) {
      milestones.push({
        id: 'survival_100',
        title: '100 Days Milestone',
        description: 'Long-term stability achieved after 100 days.',
        status: 'completed',
        category: 'social'
      });
    }

    if (simulation.day >= 365) {
      milestones.push({
        id: 'survival_year',
        title: 'One Year Anniversary',
        description: 'The civilization completes its first full year.',
        status: 'completed',
        category: 'cultural'
      });
    }

    return milestones.sort((a, b) => {
      const statusOrder = { 'completed': 0, 'in-progress': 1, 'upcoming': 2 };
      return statusOrder[a.status] - statusOrder[b.status];
    });
  };

  const extractPhaseNumber = (phase: string): number => {
    const match = phase.match(/Phase (\d+)/);
    return match ? parseInt(match[1]) : 0;
  };

  const milestones = generateMilestones();

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-400" />;
      case 'in-progress':
        return <Clock className="h-4 w-4 text-blue-400" />;
      default:
        return <Circle className="h-4 w-4 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-400 border-green-400';
      case 'in-progress':
        return 'text-blue-400 border-blue-400';
      default:
        return 'text-gray-400 border-gray-400';
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'social':
        return 'bg-blue-500/20 text-blue-300';
      case 'technological':
        return 'bg-purple-500/20 text-purple-300';
      case 'cultural':
        return 'bg-orange-500/20 text-orange-300';
      case 'biological':
        return 'bg-green-500/20 text-green-300';
      case 'phase10':
        return 'bg-pink-500/20 text-pink-300';
      default:
        return 'bg-gray-500/20 text-gray-300';
    }
  };

  const formatDate = (timestamp: number) => {
    return new Date(timestamp).toLocaleDateString();
  };

  const completedCount = milestones.filter(m => m.status === 'completed').length;
  const totalCount = milestones.length;

  return (
    <Card className="glass-card bg-black/20 border-white/10">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-white">
          <Trophy className="h-5 w-5 text-yellow-400" />
          Civilization Milestones
          <Badge variant="outline" className="ml-auto text-yellow-200 border-yellow-400">
            {completedCount}/{totalCount}
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[300px] pr-4">
          <div className="space-y-4">
            {milestones.map((milestone) => (
              <div
                key={milestone.id}
                className="p-4 rounded-lg border border-white/10 bg-white/5 hover:bg-white/10 transition-colors"
              >
                <div className="flex items-start gap-3">
                  {getStatusIcon(milestone.status)}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <h4 className="font-medium text-white truncate">
                        {milestone.title}
                      </h4>
                      <Badge
                        variant="outline"
                        className={`ml-2 text-xs ${getCategoryColor(milestone.category)}`}
                      >
                        {milestone.category}
                      </Badge>
                    </div>
                    <p className="text-sm text-blue-200 mt-1">
                      {milestone.description}
                    </p>
                    
                    {milestone.status === 'in-progress' && milestone.progress !== undefined && (
                      <div className="mt-2">
                        <div className="flex items-center justify-between text-xs text-blue-300 mb-1">
                          <span>Progress</span>
                          <span>{Math.round(milestone.progress)}%</span>
                        </div>
                        <Progress value={milestone.progress} className="h-1" />
                      </div>
                    )}
                    
                    {milestone.completedAt && (
                      <div className="text-xs text-green-300 mt-1">
                        Completed: {formatDate(milestone.completedAt)}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};