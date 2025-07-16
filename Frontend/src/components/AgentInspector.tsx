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
}

interface AgentInspectorProps {
  agent: Agent;
  onClose: () => void;
}

export const AgentInspector = ({ agent, onClose }: AgentInspectorProps) => {
  const [activeTab, setActiveTab] = useState("overview");

  // Mock data for demonstration
  const mockData = {
    age: 847,
    goals: [
      'Protect newborn child Aria',
      'Teach toolmaking to tribe members',
      'Find better shelter for family'
    ],
    relationships: [
      { name: 'Zane', type: 'partner', strength: 94 },
      { name: 'Aria', type: 'daughter', strength: 100 },
      { name: 'Elder Thom', type: 'mentor', strength: 78 },
      { name: 'Rix', type: 'rival', strength: 23 }
    ],
    memories: [
      {
        content: 'Taught Aria to make sharp stones',
        daysAgo: 2,
        importance: 'high'
      },
      {
        content: 'Argued with Rix about territory',
        daysAgo: 5,
        importance: 'medium'
      },
      {
        content: 'Discovered new water source',
        daysAgo: 8,
        importance: 'high'
      }
    ],
    skills: [
      { name: 'Toolmaking', level: 92 },
      { name: 'Communication', level: 81 },
      { name: 'Hunting', level: 67 },
      { name: 'Leadership', level: 45 }
    ],
    personality: [
      { trait: 'Curious', value: 85 },
      { trait: 'Brave', value: 72 },
      { trait: 'Kind', value: 91 },
      { trait: 'Social', value: 68 },
      { trait: 'Creative', value: 79 }
    ]
  };

  const getRelationshipColor = (type: string) => {
    const colors = {
      'partner': 'cosmic-pink',
      'daughter': 'cosmic-green',
      'son': 'cosmic-green',
      'mother': 'cosmic-purple',
      'father': 'cosmic-purple',
      'mentor': 'cosmic-blue',
      'rival': 'status-error',
      'friend': 'cosmic-teal'
    };
    return colors[type as keyof typeof colors] || 'cosmic-blue';
  };

  const getSkillColor = (level: number) => {
    if (level >= 80) return 'cosmic-green';
    if (level >= 60) return 'cosmic-blue';
    if (level >= 40) return 'cosmic-orange';
    return 'muted-foreground';
  };

  const getSkillLabel = (level: number) => {
    if (level >= 90) return 'Expert';
    if (level >= 75) return 'Advanced';
    if (level >= 50) return 'Intermediate';
    if (level >= 25) return 'Beginner';
    return 'Novice';
  };

  return (
    <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-4xl max-h-[90vh] overflow-hidden observatory-card">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <User className="w-5 h-5 text-cosmic-blue" />
              Agent Inspector: {agent.name}
            </CardTitle>
            <Button variant="ghost" size="icon" onClick={onClose}>
              <X className="w-4 h-4" />
            </Button>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="secondary">{agent.tribe}</Badge>
            <Badge variant="outline" className="capitalize">{agent.status}</Badge>
            <Badge variant="outline">{mockData.age} days old</Badge>
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
                        {mockData.goals.map((goal, i) => (
                          <div key={i} className="text-xs text-muted-foreground">
                            • {goal}
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="metric-card">
                      <div className="flex items-center gap-2">
                        <Brain className="w-4 h-4 text-cosmic-purple" />
                        <div className="text-sm font-medium">Key Traits</div>
                      </div>
                      <div className="mt-2 flex flex-wrap gap-1">
                        {agent.traits.map(trait => (
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
                    
                    {mockData.personality.map((trait) => (
                      <div key={trait.trait} className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm font-medium">{trait.trait}</span>
                          <span className="text-sm text-muted-foreground">{trait.value}%</span>
                        </div>
                        <Progress value={trait.value} className="h-2" />
                      </div>
                    ))}
                  </div>
                </TabsContent>

                <TabsContent value="relationships" className="space-y-4">
                  <div className="space-y-4">
                    <div className="flex items-center gap-2">
                      <Heart className="w-5 h-5 text-cosmic-pink" />
                      <div className="text-lg font-medium">Relationship Network</div>
                    </div>
                    
                    {mockData.relationships.map((rel) => (
                      <div key={rel.name} className="flex items-center justify-between p-3 bg-secondary/20 rounded-lg">
                        <div className="flex items-center gap-3">
                          <div className="w-3 h-3 bg-cosmic-blue rounded-full"></div>
                          <div>
                            <div className="text-sm font-medium">{rel.name}</div>
                            <Badge variant="outline" className={`text-xs text-${getRelationshipColor(rel.type)}`}>
                              {rel.type}
                            </Badge>
                          </div>
                        </div>
                        <div className="text-sm text-muted-foreground">
                          {rel.strength}% bond
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
                    
                    {mockData.memories.map((memory, i) => (
                      <div key={i} className="p-3 bg-secondary/20 rounded-lg">
                        <div className="text-sm font-medium mb-1">{memory.content}</div>
                        <div className="flex items-center gap-2">
                          <Badge variant="outline" className="text-xs">
                            {memory.daysAgo} days ago
                          </Badge>
                          <Badge variant="outline" className={`text-xs ${
                            memory.importance === 'high' ? 'text-cosmic-orange' :
                            memory.importance === 'medium' ? 'text-cosmic-blue' :
                            'text-muted-foreground'
                          }`}>
                            {memory.importance}
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                </TabsContent>

                <TabsContent value="skills" className="space-y-4">
                  <div className="space-y-4">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="w-5 h-5 text-cosmic-green" />
                      <div className="text-lg font-medium">Skills & Knowledge</div>
                    </div>
                    
                    {mockData.skills.map((skill) => (
                      <div key={skill.name} className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm font-medium">{skill.name}</span>
                          <div className="flex items-center gap-2">
                            <Badge variant="outline" className={`text-xs text-${getSkillColor(skill.level)}`}>
                              {getSkillLabel(skill.level)}
                            </Badge>
                            <span className="text-sm text-muted-foreground">{skill.level}%</span>
                          </div>
                        </div>
                        <Progress value={skill.level} className="h-2" />
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