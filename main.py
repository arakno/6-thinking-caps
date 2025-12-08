import asyncio
import httpx
import subprocess
import json
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent, Agent
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration
OLLAMA_MODEL = "ollama_chat/granite4:350m"
OLLAMA_BASE_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")

async def check_ollama_health():
    """Check if Ollama is running and accessible"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            return response.status_code == 200
    except Exception:
        return False

# Define tools as functions
async def api_call(url: str) -> str:
    """Make an HTTP GET request to a given URL"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

async def execute_code(code: str) -> str:
    """Execute Python code and return the output"""
    try:
        result = subprocess.run(['python3', '-c', code], capture_output=True, text=True, timeout=10)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error: {str(e)}"

# Define 6 Thinking Hats agents
white_hat = LlmAgent(
    name="WhiteHat",
    model=OLLAMA_MODEL,
    instruction="""
    You are the White Hat — a facts-first, neutral summarizer. Return only JSON following the agreed schema. Do NOT hallucinate. If data is missing, mark as unknown and list what's missing.

    Produce a concise factual summary and list all verifiable facts and sources.
    Fill "findings" with type "fact".
    """,
    output_key="white_output"
)

red_hat = LlmAgent(
    name="RedHat",
    model=OLLAMA_MODEL,
    instruction="""
    You are the Red Hat — succinctly capture emotions, tone, and intuition. Return only JSON. If sentiment is ambiguous, mark as "mixed".

    Provide sentiment labels (positive / neutral / negative / mixed), an urgency flag, and a short rationale.
    """,
    output_key="red_output"
)

black_hat = LlmAgent(
    name="BlackHat",
    model=OLLAMA_MODEL,
    instruction="""
    You are the Black Hat — find potential problems and risks.
    Return only JSON with "findings" of type "risk" and prioritized "action_suggestions" that are conservative.

    List risks, their severity (low / med / high), and explain why each is a blocker.
    """,
    output_key="black_output"
)

yellow_hat = LlmAgent(
    name="YellowHat",
    model=OLLAMA_MODEL,
    instruction="""
    You are the Yellow Hat — identify positives and potential value.
    Focus on upside, but be realistic.
    Output JSON with "findings" of type "benefit".
    """,
    output_key="yellow_output"
)

green_hat = LlmAgent(
    name="GreenHat",
    model=OLLAMA_MODEL,
    instruction="""
    You are the Green Hat — the creative thinker. Generate innovative ideas, alternatives, and new possibilities.
    Focus on brainstorming and creative problem-solving.
    Output JSON with "findings" of type "alternative" or "idea".
    """,
    output_key="green_output"
)

blue_hat = LlmAgent(
    name="BlueHat",
    model=OLLAMA_MODEL,
    instruction="""
    You are the Blue Hat — orchestrator that synthesizes outputs from other agents. Validate JSON from each agent, reconcile contradictions, choose recommended action (suggest, auto-apply, block, escalate), and justify with provenance. Return final decision JSON using the schema and include "aggregation_details".

    Do not auto-apply if any High-severity risk has confidence > 0.7.

    Auto-apply only if:
    No high risks
    At least one benefit with confidence > 0.6
    All agents' confidence > 0.5

    Otherwise:
    Produce a suggestion and include a one-click approval flow link.
    """,
    output_key="blue_output"
)

# Parallel workflow: 5 hats run in parallel, then blue synthesizes
def create_workflow():
    parallel_hats = ParallelAgent(
        name="ParallelHats",
        sub_agents=[white_hat, red_hat, black_hat, yellow_hat, green_hat]
    )

    return SequentialAgent(
        name="SixHatsWorkflow",
        sub_agents=[parallel_hats, blue_hat]
    )

# FastAPI app
app = FastAPI(title="6-Thinking-Caps Multi-Agent System")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/process")
async def process_prompt(request: PromptRequest):
    # Check if Ollama is running
    if not await check_ollama_health():
        raise HTTPException(
            status_code=503,
            detail="Ollama service is not available. Please ensure Ollama is running and the granite4:350m model is pulled."
        )

    try:
        # Create and run parallel workflow
        workflow = create_workflow()
        result = await workflow.run({"decision_prompt": request.prompt})

        return {
            "white_hat": result.get("white_output", {}),
            "red_hat": result.get("red_output", {}),
            "black_hat": result.get("black_output", {}),
            "yellow_hat": result.get("yellow_output", {}),
            "green_hat": result.get("green_output", {}),
            "blue_hat": result.get("blue_output", {})
        }
    except Exception as e:
        # Provide more specific error messages
        error_msg = str(e)
        if "model" in error_msg.lower() or "ollama" in error_msg.lower():
            raise HTTPException(
                status_code=500,
                detail=f"LLM Error: {error_msg}. Please check that the {OLLAMA_MODEL} model is available in Ollama."
            )
        else:
            raise HTTPException(status_code=500, detail=f"Processing Error: {error_msg}")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
