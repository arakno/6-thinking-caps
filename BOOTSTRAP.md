# 🎩 Bootstrap Guide - Project Setup Complete!

## ✅ Project Structure Created

Your 6 Thinking Hats Multi-Agent System is ready to start development! Here's what has been scaffolded:

```
6-thinking-caps/
├── backend/                         # Python FastAPI backend
│   ├── agents/                      # 6 Thinking Hat agents
│   │   ├── base_agent.py           # Base agent class
│   │   ├── white_hat.py            # Facts & data
│   │   ├── red_hat.py              # Emotions & intuition
│   │   ├── black_hat.py            # Critical analysis
│   │   ├── yellow_hat.py           # Vision & opportunities
│   │   ├── green_hat.py            # Creativity & ideas
│   │   └── blue_hat.py             # Synthesis & control
│   │
│   ├── api/                         # API routes
│   │   ├── routes.py               # FastAPI endpoints
│   │   └── schemas.py              # Pydantic models
│   │
│   ├── services/                    # Business logic
│   │   ├── gemini_client.py        # Google Gemini API wrapper
│   │   ├── orchestrator.py         # Agent coordinator
│   │   └── session_manager.py      # Session management
│   │
│   ├── models/                      # Data models
│   │   └── session.py              # SessionContext, AgentResult
│   │
│   ├── utils/                       # Utilities
│   │   └── logger.py               # Logging setup
│   │
│   ├── static/                      # React build output (production)
│   ├── app.py                       # FastAPI application entry point
│   ├── config.py                    # Configuration & settings
│   ├── requirements.txt             # Python dependencies
│   └── .env                         # Environment variables
│
├── frontend/                        # React + Vite frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── InputForm.jsx       # Problem input form
│   │   │   ├── ProgressTracker.jsx # Real-time progress
│   │   │   └── ResultsDisplay.jsx  # Results visualization
│   │   │
│   │   ├── styles/
│   │   │   ├── App.css             # Main styles
│   │   │   ├── InputForm.css
│   │   │   ├── ProgressTracker.css
│   │   │   └── ResultsDisplay.css
│   │   │
│   │   ├── main.jsx                # React entry point
│   │   └── App.jsx                 # Main app component
│   │
│   ├── public/                      # Static assets
│   ├── index.html                   # HTML template
│   ├── package.json                 # Node dependencies
│   └── vite.config.js              # Vite build config
│
├── tests/                           # Unit tests
│   ├── test_agents.py
│   ├── test_orchestrator.py
│   └── test_session_manager.py
│
├── DEVELOPMENT_PLAN.md              # Detailed dev roadmap
├── BOOTSTRAP.md                     # This file
├── README.md                        # Quick start guide
├── .env.example                     # Example env template
└── setup.sh                         # Setup script
```

## 🚀 Getting Started

### Step 1: Install Dependencies

#### Option A: Using the setup script (Recommended)
```bash
chmod +x setup.sh
./setup.sh
```

#### Option B: Manual setup
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Step 2: Configure API Key

```bash
# Edit backend/.env
cd backend
nano .env  # or use your preferred editor

# Add your Google Gemini API key:
# GOOGLE_API_KEY=your_api_key_here
```

Get your API key from: https://ai.google.dev/

### Step 3: Run the Application

#### Option A: Parallel Development (Recommended for coding)
```bash
# Terminal 1 - Backend
cd backend
uvicorn app:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev

# Open http://localhost:5173 in your browser
```

**Benefits:**
- Hot reload for both frontend and backend
- Easier debugging
- Frontend dev server features (HMR, etc.)

#### Option B: Single Server (Like production)
```bash
# Build frontend
cd frontend
npm run build

# Start backend (serves React + API)
cd backend
uvicorn app:app --reload

# Open http://localhost:8000
```

**Benefits:**
- Single entry point (like production)
- No CORS issues
- Test actual deployment setup

## 📊 Architecture Overview

### Request Flow

```
User Browser
    ↓
    ↓ POST /api/sessions
    ↓ {problem_statement, background_context}
    ↓
FastAPI + Uvicorn Server
    ↓
SessionManager (create session, store context)
    ↓
BackgroundTask: Agent Orchestrator
    ├─→ White Hat Agent  ──┐
    ├─→ Red Hat Agent    ──┤
    ├─→ Black Hat Agent  ──├─→ Parallel Execution
    ├─→ Yellow Hat Agent ──┤
    ├─→ Green Hat Agent  ──┘
    ↓ (All 5 complete)
    └─→ Blue Hat Agent (Synthesis)
    ↓
Session updated with results
    ↓
Frontend polls: GET /api/sessions/{id}/progress
    ↓
When complete: GET /api/sessions/{id}/results
    ↓
Display results to user
```

### Session Lifecycle

1. **Create** → POST /api/sessions
2. **Analyze** → POST /api/sessions/{id}/analyze
3. **Monitor** → GET /api/sessions/{id}/progress
4. **Retrieve** → GET /api/sessions/{id}/results
5. **Cleanup** → Sessions auto-expire after 60 minutes

## 🔑 Key Configuration

### Backend (.env)
```
GOOGLE_API_KEY=your_api_key_here
DEBUG=True              # Set to False in production
ENVIRONMENT=development
```

### Frontend (vite.config.js)
- Builds to: `../backend/static/`
- Dev server proxy: `/api/*` → `http://localhost:8000/api/*`

### FastAPI (app.py)
- Serves React from `/` (index.html)
- API endpoints at `/api/*`
- Static files at `/static/*`
- CORS enabled for development

## 📝 API Examples

### Create a session
```bash
curl -X POST http://localhost:8000/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "problem_statement": "Should we expand to the European market?",
    "background_context": "We currently operate in North America with 50% market share"
  }'
```

Response:
```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "initialized",
  "problem_statement": "Should we expand to the European market?",
  "created_at": "2025-12-07T10:30:00",
  "updated_at": "2025-12-07T10:30:00"
}
```

### Start analysis
```bash
curl -X POST http://localhost:8000/api/sessions/123e4567-e89b-12d3-a456-426614174000/analyze
```

### Check progress
```bash
curl http://localhost:8000/api/sessions/123e4567-e89b-12d3-a456-426614174000/progress
```

Response:
```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "processing",
  "agents_completed": ["white", "red"],
  "agents_processing": ["black"],
  "agents_pending": ["yellow", "green", "blue"],
  "timestamp": "2025-12-07T10:35:00"
}
```

### Get results
```bash
curl http://localhost:8000/api/sessions/123e4567-e89b-12d3-a456-426614174000/results
```

## 🧪 Running Tests

```bash
# Backend unit tests
cd backend
pytest tests/ -v

# Specific test file
pytest tests/test_session_manager.py -v

# With coverage
pytest tests/ --cov=backend
```

## 🛠️ Development Workflow

### Working on Agents
1. Edit `backend/agents/white_hat.py` (or any hat)
2. Update the `build_prompt()` method to refine instructions
3. Update `parse_response()` to extract better insights
4. Restart backend: Ctrl+C and run again
5. Test via UI or API calls

### Working on Frontend
1. Edit `frontend/src/components/InputForm.jsx` (or any component)
2. Changes hot-reload automatically in npm dev
3. No need to restart backend

### Working on API
1. Edit `backend/api/routes.py`
2. Restart backend: Ctrl+C and run again
3. Test with curl or UI

## 📚 Documentation Structure

- **DEVELOPMENT_PLAN.md** - Comprehensive roadmap and architecture
- **README.md** - Quick start guide
- **BOOTSTRAP.md** - This setup guide
- **Code comments** - Inline documentation

## 🔄 Next Steps

1. ✅ Project scaffolding complete
2. ⬜ Add your Google API key to `backend/.env`
3. ⬜ Run `pip install -r backend/requirements.txt`
4. ⬜ Run `cd frontend && npm install`
5. ⬜ Start the application (see Step 3 above)
6. ⬜ Test with a sample problem
7. ⬜ Review agent outputs
8. ⬜ Customize prompts in `backend/agents/`
9. ⬜ Deploy when ready

## 🚨 Troubleshooting

### ImportError: No module named 'fastapi'
- Make sure you're in the `.venv` environment
- Run: `pip install -r backend/requirements.txt`

### Cannot find module 'react'
- Make sure you installed frontend dependencies
- Run: `cd frontend && npm install`

### Gemini API errors
- Check that `GOOGLE_API_KEY` is set in `backend/.env`
- Test key validity at https://ai.google.dev/

### Port 8000 already in use
- Change port: `uvicorn app:app --port 8001 --reload`

### Frontend not loading on localhost:8000
- Make sure you built the frontend: `cd frontend && npm run build`
- Check that `backend/static/` has files

## 📦 Technology Stack Installed

**Backend:**
- fastapi==0.104.1
- uvicorn==0.24.0
- pydantic==2.5.0
- google-generativeai==0.3.0
- pytest==7.4.3

**Frontend:**
- react==18.2.0
- react-dom==18.2.0
- vite==5.0.8

## 🎯 Success Criteria

Your project is successfully set up when:

✅ Backend starts without errors: `uvicorn app:app --reload`
✅ Frontend builds successfully: `npm run build`
✅ You can submit a problem via the UI
✅ Agents execute and return results
✅ Blue Hat synthesis provides recommendations
✅ All 6 hat perspectives are visible in results

## 📞 Support

For issues:
1. Check DEVELOPMENT_PLAN.md for architecture details
2. Review code comments for implementation details
3. Test endpoints individually with curl
4. Check backend logs in terminal

---

**Ready to analyze problems with 6 thinking perspectives!** 🎩
