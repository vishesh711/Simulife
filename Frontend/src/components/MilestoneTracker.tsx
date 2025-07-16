import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { ScrollArea } from './ui/scroll-area';
import { Trophy, CheckCircle, Circle, Clock, Target } from 'lucide-react';

interface Milestone {
  id: string;
  title: string;
  description: string;
  status: 'completed' | 'in-progress' | 'upcoming';
  progress?: number;
  completedAt?: number;
  category: 'social' | 'technological' | 'cultural' | 'biological';
}

export const MilestoneTracker = () => {
  const milestones: Milestone[] = [
    {
      id: 'milestone_001',
      title: 'First Self-Awareness',
      description: 'An agent develops consciousness of their own existence and mortality.',
      status: 'completed',
      completedAt: Date.now() - 86400000 * 30,
      category: 'biological'
    },
    {
      id: 'milestone_002',
      title: 'First Tool Creation',
      description: 'Innovation leads to the creation of the first purpose-built tool.',
      status: 'completed',
      completedAt: Date.now() - 86400000 * 25,
      category: 'technological'
    },
    {
      id: 'milestone_003',
      title: 'First Communication',
      description: 'Two agents successfully communicate complex ideas using symbols.',
      status: 'completed',
      completedAt: Date.now() - 86400000 * 20,
      category: 'social'
    },
    {
      id: 'milestone_004',
      title: 'First Stable Partnership',
      description: 'Long-term pair bonding emerges between two agents.',
      status: 'completed',
      completedAt: Date.now() - 86400000 * 15,
      category: 'social'
    },
    {
      id: 'milestone_005',
      title: 'First Family Formation',
      description: 'Multi-generational family unit forms with offspring.',
      status: 'completed',
      completedAt: Date.now() - 86400000 * 10,
      category: 'social'
    },
    {
      id: 'milestone_006',
      title: 'First Group Leadership',
      description: 'Natural leader emerges to guide group decisions.',
      status: 'in-progress',
      progress: 75,
      category: 'social'
    },
    {
      id: 'milestone_007',
      title: 'First Trade Exchange',
      description: 'Economic system begins with resource trading between groups.',
      status: 'in-progress',
      progress: 45,
      category: 'social'
    },
    {
      id: 'milestone_008',
      title: 'First Inter-Tribal Contact',
      description: 'Peaceful contact established between separate tribal groups.',
      status: 'upcoming',
      category: 'social'
    },
    {
      id: 'milestone_009',
      title: 'First Artistic Expression',
      description: 'Creative expression emerges through art, music, or storytelling.',
      status: 'upcoming',
      category: 'cultural'
    },
    {
      id: 'milestone_010',
      title: 'First Religious Belief',
      description: 'Spiritual or religious concepts develop within the population.',
      status: 'upcoming',
      category: 'cultural'
    }
  ];

  const getStatusIcon = (status: string) => {
    const icons = {
      'completed': CheckCircle,
      'in-progress': Clock,
      'upcoming': Circle
    };
    return icons[status as keyof typeof icons] || Circle;
  };

  const getStatusColor = (status: string) => {
    const colors = {
      'completed': 'status-active',
      'in-progress': 'status-warning',
      'upcoming': 'muted-foreground'
    };
    return colors[status as keyof typeof colors] || 'muted-foreground';
  };

  const getCategoryColor = (category: string) => {
    const colors = {
      'social': 'cosmic-blue',
      'technological': 'cosmic-orange',
      'cultural': 'cosmic-purple',
      'biological': 'cosmic-green'
    };
    return colors[category as keyof typeof colors] || 'cosmic-blue';
  };

  const formatDate = (timestamp: number) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric'
    });
  };

  const completedCount = milestones.filter(m => m.status === 'completed').length;
  const totalCount = milestones.length;
  const completionPercentage = Math.round((completedCount / totalCount) * 100);

  return (
    <Card className="observatory-card h-[500px]">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Trophy className="w-5 h-5 text-cosmic-orange" />
          Milestone Tracker
          <Badge variant="secondary" className="ml-auto">
            {completedCount}/{totalCount}
          </Badge>
        </CardTitle>
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">Civilization Progress</span>
            <span className="text-foreground font-mono">{completionPercentage}%</span>
          </div>
          <Progress value={completionPercentage} className="h-2" />
        </div>
      </CardHeader>
      <CardContent className="p-0">
        <ScrollArea className="h-[350px] px-6">
          <div className="space-y-3 pb-4">
            {milestones.map((milestone, index) => {
              const StatusIcon = getStatusIcon(milestone.status);
              return (
                <div
                  key={milestone.id}
                  className="flex items-start gap-3 p-3 rounded-lg transition-all duration-200 hover:bg-secondary/30"
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  <div className={`mt-0.5 text-${getStatusColor(milestone.status)}`}>
                    <StatusIcon className="w-4 h-4" />
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className="text-sm font-medium text-foreground">
                        {milestone.title}
                      </h4>
                      <Badge 
                        variant="outline" 
                        className={`text-xs text-${getCategoryColor(milestone.category)}`}
                      >
                        {milestone.category}
                      </Badge>
                    </div>
                    
                    <p className="text-xs text-muted-foreground mb-2 line-clamp-2">
                      {milestone.description}
                    </p>
                    
                    {milestone.status === 'completed' && milestone.completedAt && (
                      <div className="flex items-center gap-1">
                        <CheckCircle className="w-3 h-3 text-status-active" />
                        <span className="text-xs text-status-active">
                          Completed {formatDate(milestone.completedAt)}
                        </span>
                      </div>
                    )}
                    
                    {milestone.status === 'in-progress' && milestone.progress !== undefined && (
                      <div className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span className="text-muted-foreground">Progress</span>
                          <span className="text-foreground font-mono">{milestone.progress}%</span>
                        </div>
                        <Progress value={milestone.progress} className="h-1" />
                      </div>
                    )}
                    
                    {milestone.status === 'upcoming' && (
                      <div className="flex items-center gap-1">
                        <Target className="w-3 h-3 text-muted-foreground" />
                        <span className="text-xs text-muted-foreground">
                          Awaiting conditions
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};