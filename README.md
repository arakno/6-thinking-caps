# 6 Thinking Hats Multi-Agent System

A multi-agent AI application that analyzes problems using the 6 Thinking Hats decision-making framework, powered by Google Gemini API or LM Studio (local models).

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- **Choose one:**
  - Google Gemini API key ([get one here](https://ai.google.dev/))
  - **OR** LM Studio with a local model ([download here](https://lmstudio.ai/))

### Setup

#### 1. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example .env

# Edit .env and configure your LLM provider:
# For Google Gemini: Set LLM_PROVIDER=gemini and add your GOOGLE_API_KEY
# For LM Studio: Set LLM_PROVIDER=lmstudio and configure LMSTUDIO_BASE_URL and LMSTUDIO_MODEL
```

**Using LM Studio?** See [LMSTUDIO_SETUP.md](./LMSTUDIO_SETUP.md) for detailed setup instructions.

#### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install
```

### Development

**Option A: Parallel Development (Recommended)**
```bash
# Terminal 1: Start backend
cd backend
uvicorn app:app --reload

# Terminal 2: Start frontend dev server
cd frontend
npm run dev

# Open http://localhost:5173
```

**Option B: Single Server (Production-like)**
```bash
# Build frontend
cd frontend
npm run build

# Start backend (serves built React + API)
cd backend
uvicorn app:app --reload

# Open http://localhost:8000
```

### Architecture

```
Single FastAPI + Uvicorn Server
├── /api/*      → REST API endpoints
├── /static/*   → React build files
└── /          → React SPA (index.html)
```

### API Endpoints

- `POST /api/sessions` - Create new analysis session
- `POST /api/sessions/{id}/analyze` - Start analysis
- `GET /api/sessions/{id}/progress` - Get progress
- `GET /api/sessions/{id}/results` - Get results

### LLM Provider Options

This application supports two LLM providers:

**Option 1: Google Gemini (Cloud)**
- Requires API key
- Fast and reliable
- Costs based on usage
- Configure with `LLM_PROVIDER=gemini` in `.env`

**Option 2: LM Studio (Local)**
- Run models locally on your machine
- Complete privacy - data never leaves your machine
- No API costs
- Supports models like `ibm/granite-4-h-tiny`
- Configure with `LLM_PROVIDER=lmstudio` in `.env`
- **See [LMSTUDIO_SETUP.md](./LMSTUDIO_SETUP.md) for detailed setup guide**

### Next Steps

1. Choose your LLM provider and configure `backend/.env`
2. Install dependencies: `pip install -r backend/requirements.txt` && `cd frontend && npm install`
3. If using LM Studio, follow the [LMSTUDIO_SETUP.md](./LMSTUDIO_SETUP.md) guide
4. Run the application (see Development section above)
5. Open your browser and start analyzing!

See [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md) for detailed development roadmap.

## License

MIT
