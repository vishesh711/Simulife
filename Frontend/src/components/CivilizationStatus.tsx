import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { BarChart3, Users, Sword, Heart, TrendingUp } from 'lucide-react';

interface CivilizationStatusProps {
  phase: string;
  phaseProgress: number;
  population: number;
  activeGroups: number;
  conflicts: number;
  relationships: number;
}

export const CivilizationStatus = ({ 
  phase, 
  phaseProgress, 
  population, 
  activeGroups, 
  conflicts, 
  relationships 
}: CivilizationStatusProps) => {
  const getPhaseColor = (phase: string) => {
    const colors = {
      'Genesis': 'cosmic-purple',
      'Pair Bonding': 'cosmic-pink',
      'Tribal Formation': 'cosmic-blue',
      'Complex Society': 'cosmic-teal',
      'Civilization': 'cosmic-green'
    };
    return colors[phase as keyof typeof colors] || 'cosmic-blue';
  };

  const getNextMilestone = (progress: number) => {
    if (progress < 90) return 'First Trade Exchange';
    return 'Cultural Renaissance';
  };

  return (
    <Card className="observatory-card h-[500px]">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-cosmic-teal" />
          Civilization Status
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        
        {/* Current Phase */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-foreground">Current Phase</span>
            <Badge variant="secondary" className={`text-${getPhaseColor(phase)}`}>
              {phase}
            </Badge>
          </div>
          
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Progress</span>
              <span className="text-foreground font-mono">{phaseProgress}%</span>
            </div>
            <Progress value={phaseProgress} className="h-2" />
          </div>
          
          <div className="text-sm text-muted-foreground">
            Next Milestone: <span className="text-cosmic-orange">{getNextMilestone(phaseProgress)}</span>
          </div>
        </div>

        {/* Population Stats */}
        <div className="grid grid-cols-2 gap-4">
          <div className="metric-card">
            <div className="flex items-center gap-2">
              <Users className="w-4 h-4 text-cosmic-blue" />
              <div>
                <div className="text-2xl font-bold text-foreground">{population}</div>
                <div className="text-xs text-muted-foreground">Population</div>
              </div>
            </div>
            <div className="mt-2 flex items-center gap-1">
              <TrendingUp className="w-3 h-3 text-status-active" />
              <span className="text-xs text-status-active">+5.2%</span>
            </div>
          </div>

          <div className="metric-card">
            <div className="flex items-center gap-2">
              <Users className="w-4 h-4 text-cosmic-teal" />
              <div>
                <div className="text-2xl font-bold text-foreground">{activeGroups}</div>
                <div className="text-xs text-muted-foreground">Active Groups</div>
              </div>
            </div>
            <div className="mt-2 flex items-center gap-1">
              <TrendingUp className="w-3 h-3 text-status-active" />
              <span className="text-xs text-status-active">Growing</span>
            </div>
          </div>
        </div>

        {/* Social Metrics */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sword className="w-4 h-4 text-status-error" />
              <span className="text-sm text-foreground">Active Conflicts</span>
            </div>
            <Badge variant={conflicts > 0 ? "destructive" : "secondary"}>
              {conflicts}
            </Badge>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Heart className="w-4 h-4 text-cosmic-pink" />
              <span className="text-sm text-foreground">Relationships</span>
            </div>
            <div className="text-sm font-mono text-foreground">{relationships}</div>
          </div>
        </div>

        {/* Development Indicators */}
        <div className="space-y-3">
          <div className="text-sm font-medium text-foreground">Development Indicators</div>
          
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Social Complexity</span>
              <span className="text-cosmic-blue">Advanced</span>
            </div>
            <Progress value={85} className="h-1" />
          </div>
          
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Tool Development</span>
              <span className="text-cosmic-green">Intermediate</span>
            </div>
            <Progress value={65} className="h-1" />
          </div>
          
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Communication</span>
              <span className="text-cosmic-purple">Expert</span>
            </div>
            <Progress value={92} className="h-1" />
          </div>
        </div>

        {/* Status Summary */}
        <div className="bg-secondary/30 rounded-lg p-3 border border-border">
          <div className="text-xs text-muted-foreground mb-1">Current Status</div>
          <div className="text-sm text-foreground">
            The civilization is in active tribal formation with strong social bonds and emerging leadership structures. 
            Communication systems are highly developed, enabling complex coordination between groups.
          </div>
        </div>
      </CardContent>
    </Card>
  );
};