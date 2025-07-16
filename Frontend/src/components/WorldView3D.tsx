import { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame, extend } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Globe, RotateCcw, Eye, EyeOff } from 'lucide-react';

// Extend Three.js objects for React Three Fiber
extend(THREE);

interface Agent {
  id: string;
  name: string;
  tribe: string;
  position: { x: number; y: number };
  status: 'active' | 'resting' | 'exploring';
  traits: string[];
  relationships: Record<string, string>;
}

interface WorldView3DProps {
  agents: Agent[];
  onAgentClick: (agent: Agent) => void;
  isRunning: boolean;
}

// Simple Terrain Component
function Terrain() {
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.5, 0]} receiveShadow>
      <planeGeometry args={[40, 40]} />
      <meshLambertMaterial color="#4a7c59" />
    </mesh>
  );
}

// Simple Agent Component
function AgentMesh({ agent, onClick }: { agent: Agent; onClick: () => void }) {
  const meshRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (meshRef.current) {
      // Gentle floating animation
      meshRef.current.position.y = 0.5 + Math.sin(state.clock.elapsedTime * 2 + parseInt(agent.id)) * 0.1;
    }
  });

  const getTribeColor = (tribe: string) => {
    const colors = {
      'Storm Tribe': 0x00ffff,
      'River Tribe': 0x4682b4, 
      'Hill Tribe': 0x32cd32,
      'Rock Tribe': 0x8a2be2
    };
    return colors[tribe as keyof typeof colors] || 0x00ffff;
  };

  // Convert 2D position to 3D world coordinates
  const worldX = (agent.position.x - 50) * 0.3;
  const worldZ = (agent.position.y - 50) * 0.3;

  return (
    <mesh 
      ref={meshRef}
      position={[worldX, 0.5, worldZ]}
      onClick={onClick}
      castShadow
    >
      <sphereGeometry args={[0.3, 16, 16]} />
      <meshLambertMaterial 
        color={getTribeColor(agent.tribe)}
      />
    </mesh>
  );
}

// Environmental Features
function EnvironmentalFeatures() {
  return (
    <group>
      {/* Trees */}
      <mesh position={[-10, 0, -10]}>
        <cylinderGeometry args={[0.3, 0.3, 2]} />
        <meshLambertMaterial color="#8B4513" />
      </mesh>
      <mesh position={[-10, 2, -10]}>
        <sphereGeometry args={[1.5]} />
        <meshLambertMaterial color="#228B22" />
      </mesh>
      
      <mesh position={[-8, 0, -12]}>
        <cylinderGeometry args={[0.3, 0.3, 2]} />
        <meshLambertMaterial color="#8B4513" />
      </mesh>
      <mesh position={[-8, 2, -12]}>
        <sphereGeometry args={[1.5]} />
        <meshLambertMaterial color="#228B22" />
      </mesh>

      {/* Mountains */}
      <mesh position={[10, 2, 10]}>
        <coneGeometry args={[3, 4, 8]} />
        <meshLambertMaterial color="#696969" />
      </mesh>
      
      {/* Water */}
      <mesh position={[10, 0.1, -10]} rotation={[-Math.PI / 2, 0, 0]}>
        <circleGeometry args={[3]} />
        <meshLambertMaterial color="#4169E1" transparent opacity={0.6} />
      </mesh>
    </group>
  );
}

// Territory Boundaries
function Territories({ show }: { show: boolean }) {
  if (!show) return null;
  
  return (
    <group>
      {[
        { pos: [-8, 0.02, -8] as [number, number, number], color: 0x00ffff },
        { pos: [8, 0.02, -8] as [number, number, number], color: 0xff00ff },
        { pos: [-8, 0.02, 8] as [number, number, number], color: 0xffff00 },
        { pos: [8, 0.02, 8] as [number, number, number], color: 0xff8000 },
      ].map((territory, index) => (
        <mesh key={index} position={territory.pos} rotation={[-Math.PI / 2, 0, 0]}>
          <ringGeometry args={[5, 6, 32]} />
          <meshBasicMaterial 
            color={territory.color}
            transparent
            opacity={0.3}
            side={THREE.DoubleSide}
          />
        </mesh>
      ))}
    </group>
  );
}

// Main Scene Component
function Scene({ agents, onAgentClick, showTerritories }: { 
  agents: Agent[];
  onAgentClick: (agent: Agent) => void;
  showTerritories: boolean;
}) {
  return (
    <>
      {/* Basic lighting */}
      <ambientLight intensity={0.6} />
      <directionalLight 
        position={[10, 10, 5]} 
        intensity={0.8}
        castShadow
        shadow-mapSize={[1024, 1024]}
      />
      
      {/* Sky box */}
      <mesh>
        <boxGeometry args={[100, 100, 100]} />
        <meshBasicMaterial 
          color="#87CEEB" 
          side={THREE.BackSide}
        />
      </mesh>

      {/* Scene elements */}
      <Terrain />
      <EnvironmentalFeatures />
      <Territories show={showTerritories} />

      {/* Agents */}
      {agents.map(agent => (
        <AgentMesh
          key={agent.id}
          agent={agent}
          onClick={() => onAgentClick(agent)}
        />
      ))}
    </>
  );
}

export const WorldView3D = ({ agents, onAgentClick, isRunning }: WorldView3DProps) => {
  const [showTerritories, setShowTerritories] = useState(true);
  const [autoRotate, setAutoRotate] = useState(false);

  console.log('WorldView3D rendering with agents:', agents?.length || 0);

  return (
    <Card className="observatory-card h-[500px]">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Globe className="w-5 h-5 text-electric-blue" />
          3D World Observatory
          <Badge variant="secondary" className="ml-auto">
            {isRunning ? 'Live' : 'Paused'}
          </Badge>
        </CardTitle>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setAutoRotate(!autoRotate)}
            className="professional-button"
          >
            <RotateCcw className="w-3 h-3 mr-1" />
            {autoRotate ? 'Stop' : 'Rotate'}
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowTerritories(!showTerritories)}
            className="professional-button"
          >
            {showTerritories ? <EyeOff className="w-3 h-3 mr-1" /> : <Eye className="w-3 h-3 mr-1" />}
            Territories
          </Button>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        <div className="relative h-[400px] rounded-lg mx-6 mb-6 overflow-hidden bg-gradient-to-b from-sky-200 to-green-100">
          <Canvas
            camera={{ position: [0, 12, 15], fov: 75 }}
            shadows
            gl={{ antialias: true }}
          >
            <Scene 
              agents={agents || []}
              onAgentClick={onAgentClick}
              showTerritories={showTerritories}
            />
            <OrbitControls 
              enablePan={true}
              enableZoom={true}
              enableRotate={true}
              autoRotate={autoRotate}
              autoRotateSpeed={1}
              minDistance={8}
              maxDistance={30}
              maxPolarAngle={Math.PI / 2.2}
              minPolarAngle={0.1}
            />
          </Canvas>

          {/* UI Overlays */}
          <div className="absolute bottom-4 left-4 glass-card p-2 max-w-[140px]">
            <div className="text-xs font-medium text-foreground mb-1">Controls</div>
            <div className="space-y-0.5 text-xs text-muted-foreground">
              <div>• Drag to rotate</div>
              <div>• Scroll to zoom</div>
              <div>• Click agents</div>
            </div>
          </div>

          <div className="absolute top-4 right-4 glass-card p-2 max-w-[120px]">
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 bg-electric-blue rounded-full animate-pulse"></div>
              <div className="text-sm font-semibold text-foreground">{agents?.length || 0}</div>
              <div className="text-xs text-muted-foreground">agents</div>
            </div>
          </div>

          <div className="absolute top-4 left-4 glass-card p-2 max-w-[130px]">
            <div className="text-xs font-medium text-foreground mb-1">Environment</div>
            <div className="space-y-0.5">
              {[
                { name: 'Forest', color: 'bg-green-600' },
                { name: 'Water', color: 'bg-blue-500' },
                { name: 'Mountains', color: 'bg-gray-500' },
                { name: 'Grassland', color: 'bg-green-400' }
              ].map(env => (
                <div key={env.name} className="flex items-center gap-1 text-xs">
                  <div className={`w-1.5 h-1.5 rounded-full ${env.color} flex-shrink-0`}></div>
                  <span className="text-muted-foreground truncate">{env.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};