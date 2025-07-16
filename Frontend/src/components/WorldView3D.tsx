import { useRef, useState, useMemo } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Environment, Text, Sphere, Box, Cylinder, Plane } from '@react-three/drei';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { 
  Globe, 
  RotateCcw, 
  Eye, 
  EyeOff,
  Pause,
  Play,
  Zap
} from 'lucide-react';
import * as THREE from 'three';

interface Agent {
  id: string;
  name: string;
  tribe: string;
  position: { x: number; y: number };
  status: string;
  age: number;
}

interface WorldView3DProps {
  agents: Agent[];
  onAgentClick: (agent: Agent) => void;
  isRunning: boolean;
}

// Enhanced terrain with multiple levels and features
function EnhancedTerrain() {
  const meshRef = useRef<THREE.Mesh>(null);
  
  // Create height map for terrain
  const geometry = useMemo(() => {
    const geo = new THREE.PlaneGeometry(40, 40, 64, 64);
    const vertices = geo.attributes.position.array as Float32Array;
    
    // Generate realistic terrain heights
    for (let i = 0; i < vertices.length; i += 3) {
      const x = vertices[i];
      const y = vertices[i + 1];
      
      // Create hills and valleys using multiple noise functions
      const height = 
        Math.sin(x * 0.1) * Math.cos(y * 0.1) * 2 +
        Math.sin(x * 0.2) * Math.cos(y * 0.2) * 1 +
        Math.sin(x * 0.05) * Math.cos(y * 0.05) * 3 +
        Math.random() * 0.5;
      
      vertices[i + 2] = height;
    }
    
    geo.computeVertexNormals();
    return geo;
  }, []);

  return (
    <mesh ref={meshRef} geometry={geometry} rotation={[-Math.PI / 2, 0, 0]} position={[0, -2, 0]}>
      <meshLambertMaterial 
        color="#2d5016"
        wireframe={false}
        transparent={false}
      />
    </mesh>
  );
}

// Water bodies
function WaterFeatures() {
  const waterRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (waterRef.current && waterRef.current.material instanceof THREE.ShaderMaterial) {
      waterRef.current.material.uniforms.time.value = state.clock.elapsedTime;
    }
  });

  const waterMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      uniforms: {
        time: { value: 0 },
        color: { value: new THREE.Color('#1e40af') }
      },
      vertexShader: `
        uniform float time;
        varying vec2 vUv;
        varying vec3 vPosition;
        
        void main() {
          vUv = uv;
          vPosition = position;
          
          vec3 pos = position;
          pos.z += sin(pos.x * 2.0 + time) * 0.1;
          pos.z += cos(pos.y * 2.0 + time * 0.5) * 0.05;
          
          gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
        }
      `,
      fragmentShader: `
        uniform float time;
        uniform vec3 color;
        varying vec2 vUv;
        varying vec3 vPosition;
        
        void main() {
          vec3 waterColor = color;
          float wave = sin(vPosition.x * 4.0 + time) * 0.1 + 0.9;
          gl_FragColor = vec4(waterColor * wave, 0.7);
        }
      `,
      transparent: true
    });
  }, []);

  return (
    <>
      {/* River */}
      <mesh ref={waterRef} material={waterMaterial} position={[5, -1.5, -8]} rotation={[-Math.PI / 2, 0, 0.3]}>
        <planeGeometry args={[12, 3]} />
      </mesh>
      
      {/* Lake */}
      <mesh material={waterMaterial} position={[-8, -1.5, 6]} rotation={[-Math.PI / 2, 0, 0]}>
        <circleGeometry args={[4, 32]} />
      </mesh>
    </>
  );
}

// Enhanced vegetation
function Vegetation() {
  const trees = useMemo(() => {
    const treePositions = [];
    for (let i = 0; i < 25; i++) {
      treePositions.push({
        x: (Math.random() - 0.5) * 35,
        z: (Math.random() - 0.5) * 35,
        height: 2 + Math.random() * 3,
        type: Math.random() > 0.7 ? 'pine' : 'oak'
      });
    }
    return treePositions;
  }, []);

  return (
    <group>
      {trees.map((tree, index) => (
        <group key={index} position={[tree.x, -1, tree.z]}>
          {/* Tree trunk */}
          <Cylinder args={[0.2, 0.3, tree.height * 0.6]} position={[0, tree.height * 0.3, 0]}>
            <meshLambertMaterial color="#4a5d23" />
          </Cylinder>
          
          {/* Tree foliage */}
          {tree.type === 'pine' ? (
            <mesh position={[0, tree.height * 0.8, 0]}>
              <coneGeometry args={[1.2, tree.height * 0.8, 8]} />
              <meshLambertMaterial color="#1e4d2b" />
            </mesh>
          ) : (
            <Sphere args={[1.5]} position={[0, tree.height * 0.9, 0]}>
              <meshLambertMaterial color="#2d5a27" />
            </Sphere>
          )}
        </group>
      ))}
    </group>
  );
}

// Mountains in the background
function Mountains() {
  return (
    <group>
      {/* Mountain range */}
      <mesh position={[15, 2, -15]}>
        <coneGeometry args={[4, 8, 6]} />
        <meshLambertMaterial color="#6b7280" />
      </mesh>
      <mesh position={[18, 1.5, -12]}>
        <coneGeometry args={[3, 6, 6]} />
        <meshLambertMaterial color="#9ca3af" />
      </mesh>
      <mesh position={[12, 2.5, -18]}>
        <coneGeometry args={[3.5, 7, 6]} />
        <meshLambertMaterial color="#4b5563" />
      </mesh>
      
      {/* Distant mountains */}
      <mesh position={[-20, 1, -20]}>
        <coneGeometry args={[5, 6, 6]} />
        <meshLambertMaterial color="#374151" />
      </mesh>
      <mesh position={[-25, 0.5, -15]}>
        <coneGeometry args={[3, 4, 6]} />
        <meshLambertMaterial color="#6b7280" />
      </mesh>
    </group>
  );
}

// Enhanced Agent representation
function AgentSphere({ agent, onClick }: { agent: Agent; onClick: () => void }) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);
  
  useFrame((state) => {
    if (meshRef.current) {
      // Floating animation
      meshRef.current.position.y = Math.sin(state.clock.elapsedTime * 2 + parseInt(agent.id)) * 0.2 + 1;
      
      // Gentle rotation
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.5;
      
      // Scale on hover
      const targetScale = hovered ? 1.3 : 1;
      meshRef.current.scale.lerp(new THREE.Vector3(targetScale, targetScale, targetScale), 0.1);
    }
  });

  const getTribeColor = (tribe: string) => {
    const colors = {
      'Storm Tribe': '#06b6d4',
      'River Tribe': '#3b82f6', 
      'Hill Tribe': '#10b981',
      'Rock Tribe': '#8b5cf6'
    };
    return colors[tribe as keyof typeof colors] || '#06b6d4';
  };

  // Convert 2D position to 3D world coordinates
  const worldX = (agent.position.x - 50) * 0.4;
  const worldZ = (agent.position.y - 50) * 0.4;

  return (
    <group position={[worldX, 0, worldZ]}>
      {/* Main agent sphere */}
      <mesh 
        ref={meshRef}
        onClick={onClick}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
        castShadow
      >
        <sphereGeometry args={[0.4, 16, 16]} />
        <meshPhongMaterial 
          color={getTribeColor(agent.tribe)}
          shininess={100}
          transparent={true}
          opacity={0.9}
        />
      </mesh>
      
      {/* Glow effect */}
      <mesh scale={1.2}>
        <sphereGeometry args={[0.4, 16, 16]} />
        <meshBasicMaterial 
          color={getTribeColor(agent.tribe)}
          transparent={true}
          opacity={0.2}
        />
      </mesh>
      
      {/* Floating name tag */}
      {hovered && (
        <Text
          position={[0, 2, 0]}
          fontSize={0.3}
          color="white"
          anchorX="center"
          anchorY="middle"
        >
          {agent.name}
        </Text>
      )}
      
      {/* Status indicator */}
      <mesh position={[0, 1.2, 0]}>
        <sphereGeometry args={[0.1, 8, 8]} />
        <meshBasicMaterial color={agent.status === 'active' ? '#10b981' : '#ef4444'} />
      </mesh>
    </group>
  );
}

// Tribal territories
function Territories({ show }: { show: boolean }) {
  if (!show) return null;
  
  const territories = useMemo(() => [
    { tribe: 'Storm Tribe', center: [-8, 8], color: '#06b6d4', radius: 6 },
    { tribe: 'River Tribe', center: [8, -8], color: '#3b82f6', radius: 5 },
    { tribe: 'Hill Tribe', center: [-6, -10], color: '#10b981', radius: 5.5 },
    { tribe: 'Rock Tribe', center: [10, 10], color: '#8b5cf6', radius: 4.5 }
  ], []);

  return (
    <group>
      {territories.map((territory, index) => (
        <mesh
          key={index}
          position={[territory.center[0] * 0.4, -1.8, territory.center[1] * 0.4]}
          rotation={[-Math.PI / 2, 0, 0]}
        >
          <ringGeometry args={[territory.radius * 0.4, territory.radius * 0.4 + 0.2, 32]} />
          <meshBasicMaterial 
            color={territory.color}
            transparent={true}
            opacity={0.3}
          />
        </mesh>
      ))}
    </group>
  );
}

// Main scene
function Scene({ agents, onAgentClick, showTerritories }: { 
  agents: Agent[];
  onAgentClick: (agent: Agent) => void;
  showTerritories: boolean;
}) {
  return (
    <>
      {/* Enhanced lighting setup */}
      <ambientLight intensity={0.4} />
      <directionalLight 
        position={[10, 10, 5]} 
        intensity={1}
        castShadow
        shadow-mapSize={[2048, 2048]}
        shadow-camera-far={50}
        shadow-camera-left={-20}
        shadow-camera-right={20}
        shadow-camera-top={20}
        shadow-camera-bottom={-20}
      />
      <pointLight position={[-10, 10, -10]} intensity={0.5} color="#fbbf24" />
      <spotLight 
        position={[0, 15, 0]} 
        intensity={0.8}
        angle={Math.PI / 6}
        penumbra={0.5}
        castShadow
      />

      {/* Environment */}
      <Environment preset="sunset" />
      
      {/* Enhanced terrain and features */}
      <EnhancedTerrain />
      <WaterFeatures />
      <Vegetation />
      <Mountains />
      <Territories show={showTerritories} />

      {/* Agents */}
      {agents.map(agent => (
        <AgentSphere
          key={agent.id}
          agent={agent}
          onClick={() => onAgentClick(agent)}
        />
      ))}

      {/* Sky sphere */}
      <mesh>
        <sphereGeometry args={[100, 32, 32]} />
        <meshBasicMaterial 
          color="#1e293b" 
          side={THREE.BackSide}
          transparent={true}
          opacity={0.8}
        />
      </mesh>
    </>
  );
}

export const WorldView3D = ({ agents, onAgentClick, isRunning }: WorldView3DProps) => {
  const [showTerritories, setShowTerritories] = useState(true);
  const [autoRotate, setAutoRotate] = useState(false);
  const [cameraMode, setCameraMode] = useState<'overview' | 'close'>('overview');

  return (
    <div className="relative h-full w-full rounded-2xl overflow-hidden bg-gradient-to-b from-slate-900 to-slate-800">
      <Canvas
        camera={{ 
          position: cameraMode === 'overview' ? [0, 15, 20] : [0, 8, 12], 
          fov: 60 
        }}
        shadows
        gl={{ 
          antialias: true,
          toneMapping: THREE.ACESFilmicToneMapping,
          toneMappingExposure: 1.2
        }}
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
          autoRotateSpeed={0.5}
          minDistance={8}
          maxDistance={40}
          maxPolarAngle={Math.PI / 2.2}
          minPolarAngle={0.1}
          enableDamping={true}
          dampingFactor={0.05}
        />
      </Canvas>

      {/* Enhanced UI Overlays */}
      <div className="absolute top-4 left-4 glass-card p-3 max-w-[200px]">
        <div className="text-sm font-medium text-white mb-2">World Controls</div>
        <div className="space-y-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setAutoRotate(!autoRotate)}
            className="w-full justify-start text-xs"
          >
            {autoRotate ? <Pause className="w-3 h-3 mr-2" /> : <Play className="w-3 h-3 mr-2" />}
            {autoRotate ? 'Stop Rotation' : 'Auto Rotate'}
          </Button>
          
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowTerritories(!showTerritories)}
            className="w-full justify-start text-xs"
          >
            {showTerritories ? <EyeOff className="w-3 h-3 mr-2" /> : <Eye className="w-3 h-3 mr-2" />}
            {showTerritories ? 'Hide Territories' : 'Show Territories'}
          </Button>
          
          <Button
            variant="outline"
            size="sm"
            onClick={() => setCameraMode(cameraMode === 'overview' ? 'close' : 'overview')}
            className="w-full justify-start text-xs"
          >
            <Globe className="w-3 h-3 mr-2" />
            {cameraMode === 'overview' ? 'Close View' : 'Overview'}
          </Button>
        </div>
      </div>

      <div className="absolute top-4 right-4 glass-card p-3 max-w-[160px]">
        <div className="flex items-center gap-2 mb-2">
          <div className={`w-2 h-2 rounded-full ${isRunning ? 'bg-green-400 animate-pulse' : 'bg-orange-400'}`}></div>
          <div className="text-sm font-semibold text-white">
            {isRunning ? 'Live' : 'Paused'}
          </div>
        </div>
        <div className="text-xs text-slate-300">
          <div className="flex justify-between">
            <span>Agents:</span>
            <span className="font-mono">{agents?.length || 0}</span>
          </div>
          <div className="flex justify-between">
            <span>Active:</span>
            <span className="font-mono text-green-400">
              {agents?.filter(a => a.status === 'active').length || 0}
            </span>
          </div>
        </div>
      </div>

      <div className="absolute bottom-4 left-4 glass-card p-3 max-w-[180px]">
        <div className="text-xs font-medium text-white mb-2">Navigation</div>
        <div className="space-y-1 text-xs text-slate-300">
          <div>• Drag to rotate camera</div>
          <div>• Scroll to zoom in/out</div>
          <div>• Click agents to inspect</div>
          <div>• Right-click to pan view</div>
        </div>
      </div>

      {/* Tribe Legend */}
      <div className="absolute bottom-4 right-4 glass-card p-3 max-w-[160px]">
        <div className="text-xs font-medium text-white mb-2">Tribes</div>
        <div className="space-y-1">
          {[
            { name: 'Storm Tribe', color: '#06b6d4' },
            { name: 'River Tribe', color: '#3b82f6' },
            { name: 'Hill Tribe', color: '#10b981' },
            { name: 'Rock Tribe', color: '#8b5cf6' }
          ].map((tribe) => (
            <div key={tribe.name} className="flex items-center gap-2">
              <div 
                className="w-2 h-2 rounded-full" 
                style={{ backgroundColor: tribe.color }}
              />
              <span className="text-xs text-slate-300">{tribe.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};