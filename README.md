# 6 Thinking Hats Multi-Agent System

A production-ready multi-agent AI application that analyzes complex problems using the **6 Thinking Hats decision-making framework**, enhanced with automatic solution generation. Supports both cloud (Google Gemini) and local (LM Studio) AI models.

## ✨ Features

- **7 AI Agents**: 6 Thinking Hats + Solution Generator
  - ⚪ **White Hat**: Facts, data, and objective information
  - 🔴 **Red Hat**: Emotions, intuition, and gut feelings
  - ⚫ **Black Hat**: Critical analysis, risks, and challenges
  - 🟡 **Yellow Hat**: Opportunities, benefits, and optimism
  - 💚 **Green Hat**: Creative alternatives and innovation
  - 🔵 **Blue Hat**: Synthesis and strategic overview
  - ✅ **Solution Generator**: Concrete action plan with timeline
  
- **Parallel Processing**: All agents run simultaneously for fast analysis
- **Real-time Progress**: Live updates as each agent completes
- **Interactive UI**: Clean, modern interface with tab-based navigation
- **Flexible LLM Support**: Choose between cloud (Gemini) or local (LM Studio) models
- **Session Management**: Edit previous inputs or start fresh analyses
- **Complete Privacy**: Local model option keeps all data on your machine

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- **Choose one:**
  - Google Gemini API key ([get one free](https://ai.google.dev/))
  - **OR** LM Studio with a local model ([download free](https://lmstudio.ai/))

### Installation

#### 1. Clone & Setup Backend
```bash
git clone https://github.com/arakno/6-thinking-caps.git
cd 6-thinking-caps

# Install Python dependencies (using uv - recommended)
cd backend
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt

# Configure environment
cp ../.env.example backend/.env
# Edit backend/.env with your settings (see Configuration below)
```

#### 2. Setup Frontend
```bash
cd frontend
npm install
```

### Configuration

Edit `backend/.env`:

**For Google Gemini (Cloud):**
```bash
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_api_key_here
```

**For LM Studio (Local - Private):**
```bash
LLM_PROVIDER=lmstudio
LMSTUDIO_BASE_URL=http://127.0.0.1:1234
LMSTUDIO_MODEL=ibm/granite-4-h-tiny
```

See [LMSTUDIO_SETUP.md](./LMSTUDIO_SETUP.md) for detailed local setup instructions.

### Running the Application

**Development Mode (Recommended):**
```bash
# Terminal 1: Backend (from project root)
uv run uvicorn backend.app:app --reload --port 8000

# Terminal 2: Frontend (from project root)
cd frontend && npm run dev

# Open http://localhost:5173
```

**Production Mode:**
```bash
# Build frontend
cd frontend && npm run build

# Start unified server
cd .. && uv run uvicorn backend.app:app --port 8000

# Open http://localhost:8000
```

## 📖 How to Use

1. **Enter Your Problem**: Describe the decision or challenge you're facing
2. **Add Context** (optional): Provide background information, constraints, data
3. **Start Analysis**: Click "Start Analysis" and watch the agents work
4. **Review Results**: 
   - Click through each hat tab to see different perspectives
   - Read the Blue Hat synthesis for strategic overview
   - View the Solution tab for concrete action plan
5. **Take Action**: Use the generated implementation steps and timeline

### Sample Problems

See [SAMPLE_INPUTS.md](./SAMPLE_INPUTS.md) for ready-to-use examples:
- Company expansion decisions
- Product pivot strategies
- Work policy changes
- Pricing strategy updates
- Technology modernization

## 🏗️ Architecture

```
Single FastAPI + Uvicorn Server (localhost:8000)
├── /                    → React SPA (frontend)
├── /api/sessions        → Create analysis session
├── /api/sessions/{id}/analyze  → Start analysis (background)
├── /api/sessions/{id}/progress → Real-time progress polling
├── /api/sessions/{id}/results  → Final results
└── /api/sessions/{id}/debug    → Debug agent execution

Agent Execution Flow:
1. Phase 1: 5 hats execute in parallel (White, Red, Black, Yellow, Green)
2. Phase 2: Blue Hat synthesizes all perspectives
3. Phase 3: Solution Generator creates action plan
```

**Key Benefits:**
- ✅ Single server - no CORS issues
- ✅ Built-in WebSocket support
- ✅ Easy deployment (one container)
- ✅ Perfect for production and development

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern async web framework
- **Uvicorn** - Lightning-fast ASGI server
- **Pydantic** - Data validation and settings
- **google-generativeai** - Official Google AI SDK
- **httpx** - Async HTTP client for LM Studio

### Frontend
- **React 18** - UI framework
- **Vite** - Fast build tool and dev server
- **Modern CSS** - Gradient backgrounds, animations

### AI/ML
- **Google Gemini 2.0 Flash** - Fast, intelligent responses
- **LM Studio** - Local model support (any OpenAI-compatible model)

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/sessions` | Create new analysis session |
| POST | `/api/sessions/{id}/analyze` | Start background analysis |
| GET | `/api/sessions/{id}/progress` | Get real-time progress |
| GET | `/api/sessions/{id}/results` | Get complete results |
| GET | `/api/sessions/{id}/debug` | Debug agent execution |
| GET | `/health` | Health check |

## 🔧 Development

### Project Structure
```
6-thinking-caps/
├── backend/
│   ├── agents/           # 7 AI agents (6 hats + solution)
│   ├── api/              # FastAPI routes and schemas
│   ├── services/         # LLM clients, orchestrator, session manager
│   ├── models/           # Pydantic data models
│   ├── utils/            # Logging utilities
│   └── app.py            # Application entry point
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   └── styles/       # CSS files
│   └── vite.config.js    # Vite configuration
├── tests/                # Unit tests
├── SAMPLE_INPUTS.md      # Example problems
└── DEVELOPMENT_PLAN.md   # Detailed architecture docs
```

### Running Tests
```bash
cd backend
pytest tests/
```

### Adding a New Agent
1. Create agent file in `backend/agents/`
2. Inherit from `BaseAgent`
3. Implement `build_prompt()` and `parse_response()`
4. Register in `orchestrator.py`

## 🌟 Use Cases

- **Business Decisions**: Market expansion, product pivots, pricing changes
- **Strategy Planning**: Long-term planning, resource allocation
- **Risk Assessment**: Comprehensive risk analysis from multiple angles
- **Innovation**: Generate creative solutions with structured thinking
- **Team Alignment**: Get diverse perspectives before major decisions
- **Personal Decisions**: Career changes, major purchases, life planning

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📄 License

See [LICENSE](./LICENSE) file for details.

## 🙏 Acknowledgments

- Based on Edward de Bono's **Six Thinking Hats** methodology
- Powered by Google Gemini and LM Studio
- Built with FastAPI and React

## 📞 Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Made with ❤️ for better decision-making**
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
