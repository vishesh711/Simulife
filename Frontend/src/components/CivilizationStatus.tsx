import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Progress } from './ui/progress';
import { Badge } from './ui/badge';
import { 
  TrendingUp, 
  Users, 
  Swords, 
  Heart,
  BarChart3,
  Wrench
} from 'lucide-react';

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
  return (
    <Card className="observatory-card">
      <CardHeader className="border-b border-slate-700/50">
        <CardTitle className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center">
            <BarChart3 className="h-4 w-4 text-white" />
          </div>
          <div>
            <div className="text-white font-semibold">Civilization Status</div>
            <div className="text-xs text-slate-400">Phase Progress & Metrics</div>
          </div>
        </CardTitle>
      </CardHeader>
      
      <CardContent className="p-6 space-y-6">
        {/* Current Phase */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="text-sm font-medium text-slate-300">Current Phase</div>
            <Badge variant="outline" className="bg-purple-500/10 text-purple-300 border-purple-500/30">
              {phase}
            </Badge>
          </div>
          
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-slate-400">Progress</span>
              <span className="text-white font-medium">{phaseProgress}%</span>
            </div>
            <div className="relative">
              <Progress value={phaseProgress} className="h-2 bg-slate-800" />
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 opacity-20 rounded-full" />
            </div>
          </div>
          
          <div className="text-xs text-slate-400">
            Next Milestone: First Trade Exchange
          </div>
        </div>

        {/* Population & Groups */}
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-3">
            <div className="flex items-center gap-3 p-4 rounded-lg bg-gradient-to-br from-green-500/10 to-emerald-500/5 border border-green-500/20">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center">
                <Users className="h-4 w-4 text-white" />
              </div>
              <div>
                <div className="text-lg font-bold text-white">{population}</div>
                <div className="text-xs text-slate-400">Population</div>
                <div className="flex items-center gap-1 text-xs">
                  <TrendingUp className="h-3 w-3 text-green-400" />
                  <span className="text-green-400 font-medium">+5.2%</span>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-3">
            <div className="flex items-center gap-3 p-4 rounded-lg bg-gradient-to-br from-blue-500/10 to-cyan-500/5 border border-blue-500/20">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center">
                <Users className="h-4 w-4 text-white" />
              </div>
              <div>
                <div className="text-lg font-bold text-white">{activeGroups}</div>
                <div className="text-xs text-slate-400">Active Groups</div>
                <div className="flex items-center gap-1 text-xs">
                  <TrendingUp className="h-3 w-3 text-blue-400" />
                  <span className="text-blue-400 font-medium">Growing</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Conflicts & Relationships */}
        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-center gap-3 p-4 rounded-lg bg-gradient-to-br from-red-500/10 to-orange-500/5 border border-red-500/20">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-red-500 to-orange-600 flex items-center justify-center">
              <Swords className="h-4 w-4 text-white" />
            </div>
            <div>
              <div className="text-lg font-bold text-white">{conflicts}</div>
              <div className="text-xs text-slate-400">Active Conflicts</div>
            </div>
          </div>

          <div className="flex items-center gap-3 p-4 rounded-lg bg-gradient-to-br from-pink-500/10 to-rose-500/5 border border-pink-500/20">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-pink-500 to-rose-600 flex items-center justify-center">
              <Heart className="h-4 w-4 text-white" />
            </div>
            <div>
              <div className="text-lg font-bold text-white">{relationships}</div>
              <div className="text-xs text-slate-400">Relationships</div>
            </div>
          </div>
        </div>

        {/* Development Indicators */}
        <div className="space-y-4">
          <div className="text-sm font-medium text-slate-300">Development Indicators</div>
          
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-400">Social Complexity</span>
              <span className="text-sm text-blue-300 font-medium">Advanced</span>
            </div>
            <div className="relative">
              <Progress value={85} className="h-2 bg-slate-800" />
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-500 opacity-30 rounded-full" />
            </div>
          </div>

          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-400">Tool Development</span>
              <span className="text-sm text-orange-300 font-medium">Intermediate</span>
            </div>
            <div className="relative">
              <Progress value={65} className="h-2 bg-slate-800" />
              <div className="absolute inset-0 bg-gradient-to-r from-orange-500 to-red-500 opacity-30 rounded-full" />
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};