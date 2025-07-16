# SimuLife Frontend

A beautiful, real-time dashboard for monitoring the SimuLife multi-agent simulation.

## Features

- **Real-time Observatory Dashboard** - Live simulation monitoring with WebSocket connections
- **3D World Visualization** - Interactive 3D world view using React Three Fiber
- **Phase 10 Integration** - Deep Human Emotions tracking (Love & Romance, Family Bonds, Emotional Complexity, Life Purpose)
- **Agent Inspector** - Detailed agent profiles with Phase 10 emotional data
- **Control Panel** - Start/stop/pause simulation, speed control
- **Civilization Status** - Population, phase progress, tribal groups
- **Recent Events** - Live event feed with Phase 10 categorization
- **Milestone Tracker** - Civilization advancement tracking

## Technology Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **shadcn/ui** component library
- **React Query** for efficient data fetching and caching
- **React Three Fiber** for 3D visualization
- **WebSockets** for real-time updates

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- SimuLife backend server running on port 8000

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open your browser to [http://localhost:5173](http://localhost:5173)

### Backend Connection

The frontend connects to the SimuLife API server at `http://localhost:8000`. Make sure the backend is running:

```bash
# In the main SimuLife directory
python api_server.py
```

## API Endpoints

The frontend connects to these backend endpoints:

- `GET /api/simulation` - Current simulation state
- `GET /api/agents` - All agents with Phase 10 data
- `GET /api/events` - Recent simulation events
- `GET /api/phase10` - Phase 10 system statistics
- `POST /api/control/{action}` - Control simulation (start/stop/pause)
- `WebSocket /ws` - Real-time updates

## Development

### Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Lint code

### Environment Variables

Create a `.env` file for custom API URLs:

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
```

## Project Structure

```
src/
├── components/          # React components
│   ├── ui/             # Base UI components (shadcn/ui)
│   ├── AgentInspector.tsx
│   ├── CivilizationStatus.tsx
│   ├── ControlPanel.tsx
│   ├── MilestoneTracker.tsx
│   ├── ObservatoryDashboard.tsx
│   ├── RecentEvents.tsx
│   └── WorldView3D.tsx
├── services/           # API services
│   └── api.ts         # SimuLife API integration
├── hooks/             # Custom React hooks
├── pages/             # Page components
└── lib/               # Utilities
```

## Features in Detail

### Real-time Dashboard

- **Live Metrics**: Population, events, technologies, cultural artifacts
- **WebSocket Connection**: Real-time updates with connection status indicator
- **Beautiful Animations**: Smooth transitions and visual feedback

### Phase 10 Tracking

Monitor all four Phase 10 systems:

1. **Love & Romance**: Active relationships, pregnancies
2. **Family Bonds**: Family units, bond strength
3. **Emotional Complexity**: Empathy levels, emotional range
4. **Life Purpose**: Agents with purpose, purpose distribution

### Agent Inspector

Click any agent to see detailed information:
- Basic stats (age, tribe, status)
- Emotional state and mood
- Life purpose and clarity
- Family relationships and bonds
- Skills and memories

### 3D World View

- Interactive 3D visualization of the simulation world
- Agent positions and movements
- Tribal territories and boundaries
- Environmental features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

Part of the SimuLife project. See the main project for license information.
