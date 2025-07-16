import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { ScrollArea } from './ui/scroll-area';
import { Clock, Eye, BarChart3, PartyPopper, Swords, Lightbulb, Baby } from 'lucide-react';

interface Event {
  id: string;
  type: 'celebration' | 'conflict' | 'discovery' | 'birth';
  title: string;
  description: string;
  timestamp: number;
  agents: string[];
}

interface RecentEventsProps {
  events: Event[];
}

export const RecentEvents = ({ events }: RecentEventsProps) => {
  const getEventIcon = (type: string) => {
    const icons = {
      'celebration': PartyPopper,
      'conflict': Swords,
      'discovery': Lightbulb,
      'birth': Baby
    };
    return icons[type as keyof typeof icons] || PartyPopper;
  };

  const getEventColor = (type: string) => {
    const colors = {
      'celebration': 'cosmic-green',
      'conflict': 'status-error',
      'discovery': 'cosmic-blue',
      'birth': 'cosmic-pink'
    };
    return colors[type as keyof typeof colors] || 'cosmic-blue';
  };

  const getEventBadgeVariant = (type: string): "default" | "secondary" | "destructive" | "outline" => {
    const variants = {
      'celebration': 'secondary' as const,
      'conflict': 'destructive' as const,
      'discovery': 'secondary' as const,
      'birth': 'secondary' as const
    };
    return variants[type as keyof typeof variants] || 'secondary';
  };

  const formatTimeAgo = (timestamp: number) => {
    const now = Date.now();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    return 'Just now';
  };

  return (
    <Card className="observatory-card h-[500px]">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Clock className="w-5 h-5 text-cosmic-orange" />
          Recent Events
          <Badge variant="outline" className="ml-auto">
            {events.length} total
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <ScrollArea className="h-[400px] px-6">
          <div className="space-y-4 pb-4">
            {events.map((event, index) => {
              const Icon = getEventIcon(event.type);
              return (
                <div
                  key={event.id}
                  className={`event-notification event-${event.type} animate-slide-in`}
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="flex items-start gap-3">
                    <div className={`p-2 rounded-lg bg-${getEventColor(event.type)}/20`}>
                      <Icon className={`w-4 h-4 text-${getEventColor(event.type)}`} />
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h4 className="text-sm font-medium text-foreground truncate">
                          {event.title}
                        </h4>
                        <Badge variant={getEventBadgeVariant(event.type)} className="text-xs">
                          {event.type}
                        </Badge>
                      </div>
                      
                      <p className="text-xs text-muted-foreground mb-2 line-clamp-2">
                        {event.description}
                      </p>
                      
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-1">
                          {event.agents.slice(0, 3).map((agent, i) => (
                            <Badge key={i} variant="outline" className="text-xs">
                              {agent}
                            </Badge>
                          ))}
                          {event.agents.length > 3 && (
                            <span className="text-xs text-muted-foreground">
                              +{event.agents.length - 3} more
                            </span>
                          )}
                        </div>
                        <span className="text-xs text-muted-foreground">
                          {formatTimeAgo(event.timestamp)}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
            
            {events.length === 0 && (
              <div className="text-center py-8">
                <Clock className="w-12 h-12 text-muted-foreground mx-auto mb-2 opacity-50" />
                <p className="text-sm text-muted-foreground">No recent events</p>
                <p className="text-xs text-muted-foreground mt-1">
                  Events will appear here as your civilization develops
                </p>
              </div>
            )}
          </div>
        </ScrollArea>
        
        <div className="p-4 border-t border-border">
          <div className="flex gap-2">
            <Button variant="outline" size="sm" className="flex-1">
              <Eye className="w-3 h-3 mr-1" />
              View Timeline
            </Button>
            <Button variant="outline" size="sm" className="flex-1">
              <BarChart3 className="w-3 h-3 mr-1" />
              Analytics
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};