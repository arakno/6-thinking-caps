# 6 Thinking Hats Multi-Agent System - Development Plan

## Project Overview
A production-ready web application implementing the **6 Thinking Hats** decision-making framework as a multi-agent system enhanced with automatic **solution generation**. Seven specialized agents analyze problems: six thinking hats provide diverse perspectives, followed by a solution generator that creates concrete action plans. Supports both cloud (Google Gemini) and local (LM Studio) AI models for flexibility and privacy.

---

## 1. System Architecture

### 1.1 High-Level Architecture (Single Server)
```
                         ┌──────────────────────────────┐
                         │    User Browser              │
                         │  (Single Entry Point)        │
                         └──────────┬───────────────────┘
                                    │
┌───────────────────────────────────▼──────────────────────────────────┐
│                  FastAPI + Uvicorn Server                             │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  Static File Server                                         │    │
│  │  • GET /          → index.html (React SPA)                 │    │
│  │  • GET /static/*  → CSS, JS, Assets                        │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  API Routes (/api/*)                                        │    │
│  │  • POST /api/sessions                                       │    │
│  │  • GET  /api/sessions/{id}/progress                         │    │
│  │  • GET  /api/sessions/{id}/results                          │    │
│  │  • WebSocket /ws/sessions/{id}  (Real-time updates)        │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  Multi-Agent Orchestrator Layer (3-Phase Execution)        │    │
│  │  • Session Manager (60-min TTL)                            │    │
│  │  • Agent Coordinator (asyncio.gather for parallelism)      │    │
│  │  • Context Management                                      │    │
│  └──────────────┬──────────────────────────────────────────────┘    │
│                 │                                                    │
│   Phase 1: Parallel Execution (5 hats simultaneously)               │
│   ┌─────────────┼─────────────────────────┐                         │
│   │             │                         │                         │
│  ┌▼──────┐  ┌──▼──────┐  ┌──────────┐  ┌─▼─────────┐               │
│  │White  │  │Red      │  │Black     │  │ Yellow    │               │
│  │Hat    │  │Hat      │  │Hat       │  │ Hat       │               │
│  └───┬───┘  └────┬────┘  └────┬─────┘  └──┬────────┘               │
│      │           │            │           │                        │
│  ┌───▼────┐                                                         │
│  │Green   │  Phase 2: Synthesis                                     │
│  │Hat     │  ┌──────────┐                                           │
│  └────┬───┘  │Blue Hat  │  (Aggregates all 5 perspectives)         │
│       └──────►          │                                           │
│              └─────┬────┘                                            │
│                    │                                                │
│              Phase 3: Solution Generation                           │
│              ┌─────▼──────┐                                         │
│              │  Solution  │  (7th Agent - Action Plan)              │
│              │  Generator │                                         │
│              └────────────┘                                         │
│                                                                       │
└───────────────────────────┬───────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
      ┌─────▼────┐   ┌────▼──────┐   ┌───▼────────┐
      │In-Memory │   │LLM Factory│   │  Logging   │
      │ Sessions │   │(Provider) │   │            │
      └──────────┘   └──────┬────┘   └────────────┘
                             │
                    ┌────────┴─────────┐
                    │                  │
           ┌────────▼────────┐  ┌─────▼─────────┐
           │  Gemini API     │  │  LM Studio    │
           │ (Cloud - Fast)  │  │ (Local - Free)│
           └─────────────────┘  └───────────────┘
```

**Key Improvements:**
- ✅ Single server (localhost:8000)
- ✅ No CORS complexity
- ✅ Static file serving built-in
- ✅ WebSocket support for real-time updates
- ✅ Easy deployment (single container)
- ✅ Perfect for MVP/POC

### 1.2 Component Breakdown

**Single FastAPI + Uvicorn Server:**
- Unified application serving both frontend and API
- Static file serving (React build) at `/` and `/static/*`
- RESTful API endpoints at `/api/*`
- WebSocket support for real-time progress updates
- Session management with in-memory store (dict/cache)
- No separate frontend/backend servers needed

**Frontend Layer (React):**
- Served as static files from `backend/static/`
- Single-Page Application (SPA) with Vite build
- Real-time progress tracking via WebSocket
- Input form for problem statement
- Results display with tabbed views (per-hat + synthesis)

**Agent Layer:**
- 6 Independent agents (one per thinking hat)
- Shared context object (session-level)
- Agent interface abstraction

**External:**
- Google Gemini API (1.5 Pro model recommended for reasoning)

---

## 2. The 6 Thinking Hats Framework + Solution Generation

| Hat | Color | Thinking Style | Role | Focus |
|-----|-------|-----------------|------|-------|
| 1 | White | Factual | Information Agent | Facts, data, what we know |
| 2 | Red | Emotional | Sentiment Agent | Intuition, feelings, hunches |
| 3 | Black | Critical | Analysis Agent | Risks, problems, weaknesses |
| 4 | Yellow | Optimistic | Vision Agent | Benefits, opportunities, positives |
| 5 | Green | Creative | Innovation Agent | Ideas, alternatives, possibilities |
| 6 | Blue | Control | Synthesis Agent | Summary, conclusions, next steps |
| 7 | Green | Actionable | Solution Generator | Concrete action plan, timeline, metrics |

**3-Phase Execution Model:**
1. **Phase 1 (Parallel):** White, Red, Black, Yellow, Green hats execute simultaneously using `asyncio.gather()`
2. **Phase 2 (Synthesis):** Blue Hat analyzes all 5 perspectives and creates strategic overview
3. **Phase 3 (Solution):** Solution Generator creates concrete action plan with implementation steps

---

## 3. Technology Stack

### Core Technologies
- **Language:** Python 3.10+ (tested with 3.10.18)
- **Backend Framework:** FastAPI (async/await) + Uvicorn
- **Frontend Framework:** React 18+ with Vite
- **Static File Serving:** FastAPI built-in (starlette)
- **LLM Providers:**
  - **Google Gemini:** google-generativeai SDK (models/gemini-flash-lite-latest)
  - **LM Studio:** OpenAI-compatible API via httpx (local models, 300s timeout)
- **Session Storage:** In-memory dict with 60-minute TTL cleanup
- **Real-time Updates:** HTTP polling (WebSocket optional)
- **Async Execution:** asyncio.gather() for true parallel agent execution
- **Package Manager:** uv (recommended) or pip

### Single-Server Setup Benefits
- ✅ No CORS issues (same origin)
- ✅ Simpler deployment (one container)
- ✅ WebSocket without proxy complexity
- ✅ Perfect for MVP/POC
- ✅ Easy to migrate to microservices later if needed

### Recommended Framework Decision
- **NOT LangChain/LlamaIndex:** Overkill for this POC, adds complexity
- **NOT CrewAI:** Good but heavier, more suitable for complex agent dependencies
- **APPROACH:** Custom orchestrator (lightweight, clear control flow)

---

## 4. Project Structure

```
6-thinking-caps/
├── backend/
│   ├── app.py                      # FastAPI app entry point
│   ├── config.py                   # Configuration & env vars
│   ├── requirements.txt            # Python dependencies
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py              # API endpoints (/api/*)
│   │   └── schemas.py             # Request/response models
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py          # Base agent class
│   │   ├── white_hat.py           # Information agent
│   │   ├── red_hat.py             # Sentiment agent
│   │   ├── black_hat.py           # Analysis agent
│   │   ├── yellow_hat.py          # Vision agent
│   │   ├── green_hat.py           # Innovation agent
│   │   ├── blue_hat.py            # Synthesis agent
│   │   └── solution_agent.py      # Solution generator (7th agent)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── orchestrator.py        # Agent orchestrator (3-phase execution)
│   │   ├── llm_factory.py         # LLM provider factory
│   │   ├── gemini_client.py       # Gemini API wrapper
│   │   ├── lmstudio_client.py     # LM Studio API wrapper
│   │   └── session_manager.py     # Session context management (TTL cleanup)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── session.py             # Session data models
│   │
│   ├── static/                    # React build output (served by FastAPI)
│   │   └── index.html
│   │
│   └── utils/
│       ├── __init__.py
│       └── logger.py              # Logging setup
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── InputForm.jsx
│   │   │   ├── ProgressTracker.jsx
│   │   │   └── ResultsDisplay.jsx
│   │   ├── hooks/
│   │   │   └── useApiCall.js
│   │   ├── pages/
│   │   │   └── MainPage.jsx
│   │   └── styles/
│   │       └── App.css
│   ├── package.json
│   └── vite.config.js            # Build config (outputs to ../backend/static)
│
├── tests/
│   ├── test_agents.py
│   ├── test_orchestrator.py
│   └── test_api.py
│
├── DEVELOPMENT_PLAN.md
├── README.md
├── .env.example
└── pyproject.toml                # If using uv/poetry
```

**Key Changes:**
- Frontend built files go to `backend/static/`
- Single `app.py` serves both API and static files
- No separate frontend server needed
- React uses `vite` for faster builds

---

## 5. Implementation Phases

### Phase 1: Core Backend Setup (Week 1)
- [ ] Set up FastAPI project structure
- [ ] Create base agent class
- [ ] Implement Gemini API client wrapper
- [ ] Create orchestrator service
- [ ] Set up session management (in-memory)
- [ ] Create API endpoints (basic CRUD)
- [ ] Unit tests for agents

**Deliverable:** Working backend that processes one complete thinking cycle

### Phase 2: All 6 Agents Implementation (Week 1-2)
- [ ] White Hat Agent (Facts & Data)
- [ ] Red Hat Agent (Emotions & Intuition)
- [ ] Black Hat Agent (Critical Analysis)
- [ ] Yellow Hat Agent (Positive Vision)
- [ ] Green Hat Agent (Creative Ideas)
- [ ] Blue Hat Agent (Synthesis & Control)

**Deliverable:** All agents functional with individual prompts tested

### Phase 3: Agent Orchestration & Synthesis (Week 2)
- [ ] Implement parallel agent execution
- [ ] Add context sharing between agents
- [ ] Implement synthesis logic (Blue Hat aggregation)
- [ ] Error handling & retry logic
- [ ] Progress tracking system

**Deliverable:** Complete end-to-end pipeline working

### Phase 4: Frontend Development (Week 2-3)
- [ ] React app setup with Vite
- [ ] Input form component
- [ ] Real-time progress tracking via WebSocket
- [ ] Results display with multiple views
- [ ] Build React and configure output to `backend/static/`
- [ ] Styling & UX improvements

**Deliverable:** React frontend built and served by FastAPI

### Phase 5: Integration & Testing (Week 3)
- [ ] Full end-to-end testing (backend + frontend served together)
- [ ] Performance optimization (async agents, caching)
- [ ] API documentation (auto-generated by FastAPI)
- [ ] Frontend build optimization
- [ ] Single Docker container setup (optional for POC)

**Deliverable:** Production-ready POC/MVP with unified Uvicorn server

---

## 6. API Design

### Key Endpoints

**POST /api/sessions**
```json
{
  "problem_statement": "Should we expand to new market?",
  "context": "Current situation: 50% market share in Europe..."
}
```
Response: `{ session_id: "uuid", status: "initiated" }`

**GET /api/sessions/{session_id}/progress**
Response:
```json
{
  "session_id": "uuid",
  "status": "processing",
  "agents_completed": ["white_hat", "red_hat"],
  "agents_processing": ["black_hat"],
  "agents_pending": ["yellow_hat", "green_hat", "blue_hat"],
  "timestamp": "2024-12-07T10:30:00Z"
}
```

**GET /api/sessions/{session_id}/results**
Response:
```json
{
  "session_id": "uuid",
  "problem_statement": "...",
  "hats": {
    "white": { "thinking": "...", "insights": "..." },
    "red": { "thinking": "...", "insights": "..." },
    ...
  },
  "synthesis": {
    "summary": "...",
    "recommended_actions": [...],
    "key_considerations": [...]
  }
}
```

---

## 7. Agent Communication & Context Flow

### Session Context Object
```python
class SessionContext:
    session_id: str
    problem_statement: str
    background_context: str
    agent_results: Dict[str, AgentResult]  # Hat color -> Result
    created_at: datetime
    updated_at: datetime
```

### Agent Execution Flow
1. **Input:** User submits problem statement
2. **Initialization:** Create session context
3. **Parallel Execution:**
   - Launch 5 agents in parallel (White, Red, Black, Yellow, Green)
   - Each agent reads problem + existing results from context
   - Each agent generates perspective
4. **Synthesis:**
   - Blue Hat agent reads all 5 results
   - Synthesizes comprehensive response
5. **Output:** Return complete result set

---

## 8. Data Models & Prompts

### Agent Result Model
```python
class AgentResult:
    hat_color: str
    agent_name: str
    thinking_process: str      # Full reasoning
    key_insights: List[str]
    recommendations: List[str]
    confidence_level: str      # high/medium/low
    tokens_used: int
    execution_time_ms: int
```

### Sample Prompts

**White Hat (Facts):**
```
You are a logical, objective analyst. Analyze the following problem statement 
and extract all verifiable facts, data points, and information gaps.

Problem: {problem_statement}
Context: {context}

Provide:
1. Known facts and data
2. Information sources
3. Data gaps that need addressing
4. Assumptions being made
```

**Red Hat (Emotion):**
```
You are an intuitive, emotional thinker. What do your gut instincts tell you 
about this situation? Consider feelings, hunches, and emotional implications.

Problem: {problem_statement}
Context: {context}

What are the emotional dimensions, risks, and concerns?
```

**Blue Hat (Synthesis):**
```
You are a strategic thinker synthesizing perspectives from 5 other analysts:

White Hat (Facts): {white_results}
Red Hat (Emotion): {red_results}
Black Hat (Critical): {black_results}
Yellow Hat (Vision): {yellow_results}
Green Hat (Innovation): {green_results}

Now synthesize all perspectives into:
1. Key summary
2. Risk assessment
3. Opportunities
4. Recommended next steps
5. Decision framework
```

---

## 9. Session Management Strategy

### In-Memory Storage (POC)
```python
class SessionManager:
    _sessions: Dict[str, SessionContext] = {}
    
    def create_session(self, problem: str) -> str
    def get_session(self, session_id: str) -> SessionContext
    def update_session(self, session_id: str, data: dict)
    def cleanup_old_sessions(self, ttl_minutes: int = 60)
```

**Limitations:** Single process only, data lost on restart
**Upgrade Path:** Redis for distributed caching or database for persistence

---

## 10. Development Workflow

### Step 1: Environment Setup
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env
cp .env.example .env
# Add: GOOGLE_API_KEY=your_key_here
```

### Step 2: Development Workflow

**Option A: Parallel development (recommended for POC)**
```bash
# Terminal 1: FastAPI backend (with auto-reload)
cd backend
uvicorn app:app --reload
# Serves API at http://localhost:8000/api/*

# Terminal 2: React frontend dev server (with API proxy)
cd frontend
npm run dev
# Runs on http://localhost:5173 (Vite default)
# Proxies /api/* calls to http://localhost:8000/api/*
```

**Option B: Build and serve together (test production)**
```bash
# Terminal 1: Build React frontend
cd frontend
npm run build  # outputs to ../backend/static/

# Terminal 2: Run unified FastAPI + Uvicorn server
cd backend
uvicorn app:app --reload
# Now serves:
# - React SPA at http://localhost:8000/
# - API at http://localhost:8000/api/*
# - Static assets at http://localhost:8000/static/*
```

**For Production:**
```bash
# 1. Build frontend once
cd frontend
npm run build  # outputs to ../backend/static/

# 2. Run single Uvicorn server
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000
# Single entry point: http://your-domain.com/
```

### Step 3: Testing
```bash
# Backend API tests
cd backend
pytest tests/ -v

# Test with mock Gemini API
pytest tests/ -v --use-mocks

# Frontend tests (optional for POC)
cd frontend
npm test

# End-to-end test (full stack)
# Start backend: uvicorn app:app --reload
# In another terminal: npm run dev (frontend)
# Browser test at http://localhost:5173
```

---

## 11. Next Steps & Recommendations

1. **Before Coding:**
   - Create detailed system prompts for each hat
   - Design exact output format for consistency
   - Set up Google Cloud project & get API key

2. **First Sprint:**
   - Implement FastAPI scaffolding
   - Create Gemini API wrapper with error handling
   - Build base agent class
   - Configure FastAPI to serve React static files
   - Test single agent end-to-end

3. **Testing Strategy:**
   - Mock Gemini API responses initially
   - Unit tests for each agent
   - Integration tests for orchestrator
   - E2E tests with unified server (backend + frontend)
   - Use real API sparingly (monitor quotas)

4. **Performance Considerations:**
   - Parallel agent execution (asyncio)
   - Stream responses via WebSocket to frontend
   - Cache agent prompts
   - Monitor Gemini API usage/costs
   - Optimize React build (Vite)

5. **Future Enhancements:**
   - Database persistence
   - User authentication
   - Export results (PDF, JSON)
   - Session history
   - Customizable hat prompts
   - Multi-language support
   - Horizontal scaling (move from in-memory to Redis)

---

## 12. Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| API quota exceeded | Implement rate limiting, use lower token models |
| Session data loss | Add Redis/database persistence in Phase 4 |
| Slow agent execution | Parallel async execution, streaming responses |
| Complex agent coordination | Simple sequential/parallel pattern, avoid cyclic deps |
| Gemini API costs | Monitor usage, implement cost tracking |

---

## 13. Success Criteria for MVP

✓ All 6 agents produce meaningful outputs  
✓ Blue Hat synthesizes coherent final result  
✓ Single Uvicorn server serves both frontend + API  
✓ React SPA loads from `backend/static/`  
✓ WebSocket real-time progress updates work  
✓ Session-level context persistence works  
✓ Response time < 60 seconds per full cycle  
✓ API is documented (auto-generated by FastAPI)  
✓ No CORS issues (unified origin)  

---

## References & Resources

- **Google Gemini API:** https://ai.google.dev/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **6 Thinking Hats:** Edward de Bono's methodology
- **Async Python:** https://docs.python.org/3/library/asyncio.html

