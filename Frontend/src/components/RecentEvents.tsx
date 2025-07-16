import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { ScrollArea } from './ui/scroll-area';
import { 
  Clock, 
  Heart, 
  Users, 
  Zap, 
  Star,
  Baby,
  Wrench,
  Sparkles
} from 'lucide-react';

interface Event {
  id: string;
  type: string;
  description: string;
  agents_involved: string[];
  timestamp: string;
  importance?: string;
}

interface RecentEventsProps {
  events: Event[];
}

export const RecentEvents = ({ events }: RecentEventsProps) => {
  const getEventIcon = (type: string) => {
    const icons = {
      'family': Heart,
      'emotional': Sparkles,
      'technological': Wrench,
      'social': Users,
      'cultural': Star,
      'celebration': Star,
      'birth': Baby,
      'conflict': Zap,
      'discovery': Star
    };
    return icons[type as keyof typeof icons] || Clock;
  };

  const getEventStyle = (type: string) => {
    const styles = {
      'family': 'border-l-pink-500 bg-pink-500/5 border-pink-500/20',
      'emotional': 'border-l-purple-500 bg-purple-500/5 border-purple-500/20',
      'technological': 'border-l-blue-500 bg-blue-500/5 border-blue-500/20',
      'social': 'border-l-green-500 bg-green-500/5 border-green-500/20',
      'cultural': 'border-l-orange-500 bg-orange-500/5 border-orange-500/20',
      'celebration': 'border-l-yellow-500 bg-yellow-500/5 border-yellow-500/20',
      'birth': 'border-l-pink-500 bg-pink-500/5 border-pink-500/20',
      'conflict': 'border-l-red-500 bg-red-500/5 border-red-500/20',
      'discovery': 'border-l-cyan-500 bg-cyan-500/5 border-cyan-500/20'
    };
    return styles[type as keyof typeof styles] || 'border-l-slate-500 bg-slate-500/5 border-slate-500/20';
  };

  const getEventIconColor = (type: string) => {
    const colors = {
      'family': 'text-pink-400',
      'emotional': 'text-purple-400',
      'technological': 'text-blue-400',
      'social': 'text-green-400',
      'cultural': 'text-orange-400',
      'celebration': 'text-yellow-400',
      'birth': 'text-pink-400',
      'conflict': 'text-red-400',
      'discovery': 'text-cyan-400'
    };
    return colors[type as keyof typeof colors] || 'text-slate-400';
  };

  const formatTimeAgo = (timestamp: string) => {
    // Simple time formatting - could be enhanced
    return 'Just now';
  };

  return (
    <Card className="observatory-card h-[500px]">
      <CardHeader className="border-b border-slate-700/50">
        <CardTitle className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-orange-500 to-amber-600 flex items-center justify-center">
            <Clock className="h-4 w-4 text-white" />
          </div>
          <div>
            <div className="text-white font-semibold">Recent Events</div>
            <div className="text-xs text-slate-400">Live Activity Feed</div>
          </div>
          <Badge variant="outline" className="ml-auto bg-orange-500/10 text-orange-300 border-orange-500/30">
            {events.length} total
          </Badge>
        </CardTitle>
      </CardHeader>
      
      <CardContent className="p-0">
        <ScrollArea className="h-[400px] px-6">
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
                    className={`p-4 rounded-lg border-l-4 transition-all duration-300 ${getEventStyle(event.type)}`}
                    style={{ animationDelay: `${index * 100}ms` }}
                  >
                    <div className="flex items-start gap-3">
                      <div className={`w-8 h-8 rounded-lg bg-slate-800/50 flex items-center justify-center ${getEventIconColor(event.type)}`}>
                        <Icon className="h-4 w-4" />
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <Badge 
                            variant="outline" 
                            className={`text-xs capitalize ${getEventIconColor(event.type)} border-current/30 bg-current/5`}
                          >
                            {event.type}
                          </Badge>
                          <div className="text-xs text-slate-500">
                            {formatTimeAgo(event.timestamp)}
                          </div>
                        </div>
                        
                        <div className="text-sm text-slate-200 leading-relaxed mb-2">
                          {event.description}
                        </div>
                        
                        {event.agents_involved && event.agents_involved.length > 0 && (
                          <div className="flex items-center gap-2">
                            <div className="text-xs text-slate-500">Agents:</div>
                            <div className="flex gap-1">
                              {event.agents_involved.map((agent, i) => (
                                <Badge 
                                  key={i} 
                                  variant="secondary" 
                                  className="text-xs bg-slate-800/50 text-slate-300 border-slate-600/50"
                                >
                                  {agent}
                                </Badge>
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
      </CardContent>
    </Card>
  );
};