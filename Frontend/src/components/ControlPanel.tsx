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

  const handleSave = () => {
    console.log('💾 Save simulation requested');
    // TODO: Implement save functionality
    alert('Save functionality coming soon!');
  };

  const handleExport = () => {
    console.log('📤 Export data requested');
    // TODO: Implement export functionality
    alert('Export functionality coming soon!');
  };

  const handleAnalytics = () => {
    console.log('📊 Analytics view requested');
    // TODO: Implement analytics view
    alert('Analytics view coming soon!');
  };

  const handleSpawnAgent = () => {
    console.log('👤 Spawn agent requested');
    // TODO: Implement spawn agent functionality
    alert('Spawn agent functionality coming soon!');
  };

  const handleTriggerEvent = () => {
    console.log('⚡ Trigger event requested');
    // TODO: Implement trigger event functionality
    alert('Trigger event functionality coming soon!');
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
              onClick={() => onControl(isRunning ? 'pause' : 'start')}
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
              onClick={() => onControl('step')}
              className="control-button"
            >
              <FastForward className="w-4 h-4 mr-2" />
              Step
            </Button>
            
            <Button
              variant="outline"
              onClick={() => onControl('stop')}
              className="control-button col-span-2"
            >
              <RotateCcw className="w-4 h-4 mr-2" />
              Stop Simulation
            </Button>
          </div>
        </div>

        <Separator />

        {/* Data Management */}
        <div className="space-y-3">
          <div className="text-sm font-medium text-foreground">Data Management</div>
          <div className="grid grid-cols-2 gap-2">
            <Button variant="outline" className="control-button" onClick={handleSave}>
              <Save className="w-4 h-4 mr-2" />
              Save
            </Button>
            
            <Button variant="outline" className="control-button" onClick={handleExport}>
              <Cloud className="w-4 h-4 mr-2" />
              Export
            </Button>
            
            <Button variant="outline" className="control-button col-span-2" onClick={handleAnalytics}>
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
            <Button variant="outline" className="control-button" onClick={handleSpawnAgent}>
              <Users className="w-4 h-4 mr-2" />
              Spawn Agent
            </Button>
            
            <Button variant="outline" className="control-button" onClick={handleTriggerEvent}>
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