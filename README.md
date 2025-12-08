# 6-thinking-caps
https://www.mindtools.com/ajlpp1e/six-thinking-hats/

Multi-agent project to help make decisions

A system where an LLM uses **tools** and **control flow** to arrive at a decision given a single prompt.

## Architecture

```mermaid
graph TD
    A[User Decision Prompt] --> B[Parallel Agent Execution]
    B --> C[White Hat<br/>Facts & Data]
    B --> D[Red Hat<br/>Emotions & Intuition]
    B --> E[Black Hat<br/>Risks & Problems]
    B --> F[Yellow Hat<br/>Benefits & Value]
    B --> G[Green Hat<br/>Alternatives & Creativity]
    C --> H[Blue Hat<br/>Synthesis & Decision]
    D --> H
    E --> H
    F --> H
    G --> H
    H --> I[Final Recommendation<br/>JSON Output]
```

**Core ideas to explore:**

1. **Tool Use:** Give the model "hands" (e.g., ability to control a browser, run code, or query an API).
2. **Routing:** Have a "router" step that decides *which* specialized agent should handle a user request.

**Evaluation:**
Implement a parallel workflow where one agent gathers the output of 6 others.


## Prerequisites

1. **Install Ollama** (for local LLM):
   - Download from https://ollama.ai/
   - Run `ollama serve` to start the server

2. **Pull the required model**:
   ```bash
   ollama pull granite4:350m
   ```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/arakno/6-thinking-caps.git
   cd 6-thinking-caps
   ```

2. **Install dependencies using uv**:
   ```bash
   uv sync
   ```

## Running the Application

1. **Start the server**:
   ```bash
   uv run python main.py
   ```

2. **Open your browser** and navigate to `http://localhost:8000`

3. **Enter a decision prompt** in the text area and click "Process"

The system will analyze your prompt using 6 Thinking Hats methodology through multiple LLM agents.
