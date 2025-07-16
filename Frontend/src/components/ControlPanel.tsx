import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { 
  Play, 
  Pause, 
  RotateCcw, 
  FastForward, 
  Settings, 
  Save, 
  BarChart3, 
  Zap,
  Users,
  Cloud
} from 'lucide-react';

interface ControlPanelProps {
  isRunning: boolean;
  speed: number;
  onControl: (action: string) => void;
}

export const ControlPanel = ({ isRunning, speed, onControl }: ControlPanelProps) => {
  const getSpeedLabel = (speed: number) => {
    const labels = {
      1: 'Normal',
      2: 'Fast',
      3: 'Hyper'
    };
    return labels[speed as keyof typeof labels] || 'Normal';
  };

  return (
    <Card className="observatory-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Settings className="w-5 h-5 text-cosmic-purple" />
          Control Panel
          <Badge variant={isRunning ? "secondary" : "outline"} className="ml-auto">
            {isRunning ? 'Running' : 'Paused'}
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        
        {/* Primary Controls */}
        <div className="space-y-3">
          <div className="text-sm font-medium text-foreground">Simulation Control</div>
          <div className="grid grid-cols-2 gap-2">
            <Button
              variant={isRunning ? "outline" : "default"}
              onClick={() => onControl(isRunning ? 'pause' : 'play')}
              className="control-button"
            >
              {isRunning ? (
                <>
                  <Pause className="w-4 h-4 mr-2" />
                  Pause
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 mr-2" />
                  Play
                </>
              )}
            </Button>
            
            <Button
              variant="outline"
              onClick={() => onControl('fast')}
              className="control-button"
            >
              <FastForward className="w-4 h-4 mr-2" />
              {getSpeedLabel(speed)}
            </Button>
            
            <Button
              variant="outline"
              onClick={() => onControl('restart')}
              className="control-button col-span-2"
            >
              <RotateCcw className="w-4 h-4 mr-2" />
              Restart Simulation
            </Button>
          </div>
        </div>

        <Separator />

        {/* Data Management */}
        <div className="space-y-3">
          <div className="text-sm font-medium text-foreground">Data Management</div>
          <div className="grid grid-cols-2 gap-2">
            <Button variant="outline" className="control-button">
              <Save className="w-4 h-4 mr-2" />
              Save
            </Button>
            
            <Button variant="outline" className="control-button">
              <Cloud className="w-4 h-4 mr-2" />
              Export
            </Button>
            
            <Button variant="outline" className="control-button col-span-2">
              <BarChart3 className="w-4 h-4 mr-2" />
              View Analytics
            </Button>
          </div>
        </div>

        <Separator />

        {/* Intervention Tools */}
        <div className="space-y-3">
          <div className="text-sm font-medium text-foreground">Intervention Tools</div>
          <div className="grid grid-cols-1 gap-2">
            <Button variant="outline" className="control-button">
              <Users className="w-4 h-4 mr-2" />
              Spawn Agent
            </Button>
            
            <Button variant="outline" className="control-button">
              <Zap className="w-4 h-4 mr-2" />
              Trigger Event
            </Button>
          </div>
        </div>

        <Separator />

        {/* Status Information */}
        <div className="space-y-3">
          <div className="text-sm font-medium text-foreground">System Status</div>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Simulation Speed</span>
              <Badge variant="outline" className="text-xs">
                {getSpeedLabel(speed)}x
              </Badge>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Memory Usage</span>
              <Badge variant="outline" className="text-xs">
                47.2 MB
              </Badge>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">CPU Usage</span>
              <Badge variant="outline" className="text-xs">
                12.4%
              </Badge>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Uptime</span>
              <Badge variant="outline" className="text-xs">
                2h 34m
              </Badge>
            </div>
          </div>
        </div>

        {/* Warning/Info Messages */}
        <div className="bg-secondary/30 border border-border rounded-lg p-3">
          <div className="flex items-start gap-2">
            <div className="w-2 h-2 bg-cosmic-blue rounded-full mt-1.5 animate-pulse"></div>
            <div>
              <div className="text-xs font-medium text-foreground mb-1">
                System Running Normally
              </div>
              <div className="text-xs text-muted-foreground">
                All agents are active and responding. Memory systems are stable.
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};