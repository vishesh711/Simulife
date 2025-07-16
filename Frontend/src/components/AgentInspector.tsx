import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Separator } from './ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { ScrollArea } from './ui/scroll-area';
import { Progress } from './ui/progress';
import { 
  X, 
  User, 
  Brain, 
  Heart, 
  Target, 
  BookOpen, 
  Network,
  TrendingUp,
  Calendar
} from 'lucide-react';

interface Agent {
  id: string;
  name: string;
  tribe: string;
  position: { x: number; y: number };
  status: 'active' | 'resting' | 'exploring';
  traits: string[];
  relationships: Record<string, string>;
  age: number;
  skills: Record<string, number>;
  memories_count: number;
}

interface AgentInspectorProps {
  agent: Agent;
  onClose: () => void;
}

export const AgentInspector = ({ agent, onClose }: AgentInspectorProps) => {
  const [activeTab, setActiveTab] = useState("overview");

  // Use real agent data instead of mock data
  const getRelationshipColor = (type: string) => {
    const colors = {
      'partner': 'text-pink-400',
      'daughter': 'text-green-400',
      'son': 'text-green-400',
      'mother': 'text-purple-400',
      'father': 'text-purple-400',
      'mentor': 'text-blue-400',
      'rival': 'text-red-400',
      'friend': 'text-cyan-400'
    };
    return colors[type as keyof typeof colors] || 'text-blue-400';
  };

  const getSkillColor = (level: number) => {
    if (level >= 80) return 'text-green-400';
    if (level >= 60) return 'text-blue-400';
    if (level >= 40) return 'text-yellow-400';
    return 'text-gray-400';
  };

  const getSkillLabel = (level: number) => {
    if (level >= 90) return 'Expert';
    if (level >= 75) return 'Advanced';
    if (level >= 50) return 'Intermediate';
    if (level >= 25) return 'Beginner';
    return 'Novice';
  };

  // Extract real agent data
  const relationships = Object.entries(agent.relationships || {});
  const skills = Object.entries(agent.skills || {});
  const traits = agent.traits || [];
  const memories = agent.memories_count || 0;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-4xl max-h-[90vh] overflow-hidden bg-slate-900/95 border-slate-700">
        <CardHeader className="border-b border-slate-700">
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center">
                <User className="w-5 h-5 text-white" />
              </div>
              <div>
                <div className="text-xl font-bold text-white">{agent.name}</div>
                <div className="text-sm text-slate-400">Agent Inspector</div>
              </div>
            </CardTitle>
            <Button variant="ghost" size="icon" onClick={onClose} className="text-slate-400 hover:text-white">
              <X className="w-5 h-5" />
            </Button>
          </div>
          <div className="flex items-center gap-3 mt-4">
            <Badge variant="secondary" className="bg-blue-500/20 text-blue-300 border-blue-500/30">
              {agent.tribe}
            </Badge>
            <Badge variant="outline" className="capitalize border-slate-600 text-slate-300">
              {agent.status}
            </Badge>
            <Badge variant="outline" className="border-slate-600 text-slate-300">
              {agent.age} days old
            </Badge>
            <Badge variant="outline" className="border-slate-600 text-slate-300">
              {memories} memories
            </Badge>
          </div>
        </CardHeader>

        <CardContent className="p-0">
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-5 mx-6 mt-2">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="personality">Personality</TabsTrigger>
              <TabsTrigger value="relationships">Relationships</TabsTrigger>
              <TabsTrigger value="memories">Memories</TabsTrigger>
              <TabsTrigger value="skills">Skills</TabsTrigger>
            </TabsList>

            <ScrollArea className="h-[500px] mt-4">
              <div className="px-6 pb-6">
                <TabsContent value="overview" className="space-y-6">
                  {/* Basic Info */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="metric-card">
                      <div className="flex items-center gap-2">
                        <Target className="w-4 h-4 text-cosmic-orange" />
                        <div className="text-sm font-medium">Current Goals</div>
                      </div>
                      <div className="mt-2 space-y-1">
                        {/* Goals are not directly available in the agent interface, so this will be empty */}
                      </div>
                    </div>

                    <div className="metric-card">
                      <div className="flex items-center gap-2">
                        <Brain className="w-4 h-4 text-cosmic-purple" />
                        <div className="text-sm font-medium">Key Traits</div>
                      </div>
                      <div className="mt-2 flex flex-wrap gap-1">
                        {traits.map(trait => (
                          <Badge key={trait} variant="outline" className="text-xs">
                            {trait}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Status Summary */}
                  <div className="bg-secondary/30 rounded-lg p-4 border border-border">
                    <div className="text-sm font-medium mb-2">Current Status</div>
                    <div className="text-sm text-muted-foreground">
                      {agent.name} is currently {agent.status} within the {agent.tribe} territory. 
                      They are focused on family protection and knowledge sharing with tribe members.
                    </div>
                  </div>

                  {/* Quick Stats */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="metric-card text-center">
                      <div className="text-2xl font-bold text-cosmic-blue">4</div>
                      <div className="text-xs text-muted-foreground">Relationships</div>
                    </div>
                    <div className="metric-card text-center">
                      <div className="text-2xl font-bold text-cosmic-green">12</div>
                      <div className="text-xs text-muted-foreground">Memories</div>
                    </div>
                    <div className="metric-card text-center">
                      <div className="text-2xl font-bold text-cosmic-orange">4</div>
                      <div className="text-xs text-muted-foreground">Skills</div>
                    </div>
                    <div className="metric-card text-center">
                      <div className="text-2xl font-bold text-cosmic-purple">847</div>
                      <div className="text-xs text-muted-foreground">Age (days)</div>
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="personality" className="space-y-4">
                  <div className="space-y-4">
                    <div className="flex items-center gap-2">
                      <Brain className="w-5 h-5 text-cosmic-purple" />
                      <div className="text-lg font-medium">Personality Profile</div>
                    </div>
                    
                    {/* Personality traits are not directly available in the agent interface, so this will be empty */}
                  </div>
                </TabsContent>

                <TabsContent value="relationships" className="space-y-4">
                  <div className="space-y-4">
                    <div className="flex items-center gap-2">
                      <Heart className="w-5 h-5 text-cosmic-pink" />
                      <div className="text-lg font-medium">Relationship Network</div>
                    </div>
                    
                    {relationships.map(([name, type]) => (
                      <div key={name} className="flex items-center justify-between p-3 bg-secondary/20 rounded-lg">
                        <div className="flex items-center gap-3">
                          <div className="w-3 h-3 bg-cosmic-blue rounded-full"></div>
                          <div>
                            <div className="text-sm font-medium">{name}</div>
                            <Badge variant="outline" className={`text-xs text-${getRelationshipColor(type)}`}>
                              {type}
                            </Badge>
                          </div>
                        </div>
                        <div className="text-sm text-muted-foreground">
                          {/* Bond strength is not directly available in the agent interface, so this will be empty */}
                        </div>
                      </div>
                    ))}
                  </div>
                </TabsContent>

                <TabsContent value="memories" className="space-y-4">
                  <div className="space-y-4">
                    <div className="flex items-center gap-2">
                      <BookOpen className="w-5 h-5 text-cosmic-teal" />
                      <div className="text-lg font-medium">Recent Memories</div>
                    </div>
                    
                    {/* Memories are not directly available in the agent interface, so this will be empty */}
                  </div>
                </TabsContent>

                <TabsContent value="skills" className="space-y-4">
                  <div className="space-y-4">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="w-5 h-5 text-cosmic-green" />
                      <div className="text-lg font-medium">Skills & Knowledge</div>
                    </div>
                    
                    {skills.map(([name, level]) => (
                      <div key={name} className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm font-medium">{name}</span>
                          <div className="flex items-center gap-2">
                            <Badge variant="outline" className={`text-xs text-${getSkillColor(level)}`}>
                              {getSkillLabel(level)}
                            </Badge>
                            <span className="text-sm text-muted-foreground">{level}%</span>
                          </div>
                        </div>
                        <Progress value={level} className="h-2" />
                      </div>
                    ))}
                  </div>
                </TabsContent>
              </div>
            </ScrollArea>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};