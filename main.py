import asyncio
import httpx
import subprocess
import json
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent, Agent

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

# Define specialized agents
router = LlmAgent(
    name="Router",
    instruction="""
    Based on the user's prompt, decide which specialized agent should handle it.
    Options: 'info_gatherer' for information gathering tasks,
    'code_reviewer' for code review or coding tasks,
    'decision_maker' for general decision making.
    Respond with just the agent name.
    """,
    output_key="selected_agent"
)

info_gatherer = LlmAgent(
    name="InfoGatherer",
    instruction="Gather information on the given topic. You can use api_call tool if needed.",
    output_key="gathered_info"
)

code_reviewer = LlmAgent(
    name="CodeReviewer",
    instruction="Review or generate code based on the request. You can use execute_code tool if needed.",
    output_key="code_output"
)

decision_maker = LlmAgent(
    name="DecisionMaker",
    instruction="Make a decision or provide advice on the given problem.",
    output_key="decision"
)

# Critic agent for evaluation
critic = LlmAgent(
    name="Critic",
    instruction="Review the output from the previous agent. Provide feedback and suggest improvements.",
    output_key="critique"
)

# Evaluation loop: agent -> critic -> improved agent
class EvaluationLoopAgent(Agent):
    def __init__(self, sub_agent: Agent, critic: Agent, max_iterations: int = 3):
        self.sub_agent = sub_agent
        self.critic = critic
        self.max_iterations = max_iterations

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        current_output = await self.sub_agent.run(input_data)
        for i in range(self.max_iterations):
            critique = await self.critic.run({"output": current_output["output"]})
            if "good" in critique["critique"].lower():
                break
            # Improve the input based on critique
            improved_input = {**input_data, "critique": critique["critique"]}
            current_output = await self.sub_agent.run(improved_input)
        return current_output

# Main workflow
def create_workflow(selected_agent: str):
    agent_map = {
        "info_gatherer": info_gatherer,
        "code_reviewer": code_reviewer,
        "decision_maker": decision_maker
    }
    selected = agent_map.get(selected_agent, decision_maker)
    evaluated_agent = EvaluationLoopAgent(selected, critic)

    return SequentialAgent(
        name="MainWorkflow",
        sub_agents=[evaluated_agent]
    )

# FastAPI app
app = FastAPI(title="6-Thinking-Caps Multi-Agent System")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/process")
async def process_prompt(request: PromptRequest):
    try:
        # Route the request
        route_result = await router.run({"prompt": request.prompt})
        selected_agent = route_result["selected_agent"].strip().lower()

        # Create and run workflow
        workflow = create_workflow(selected_agent)
        result = await workflow.run({"prompt": request.prompt})

        return {
            "selected_agent": selected_agent,
            "result": result.get("output", "No output"),
            "critique": result.get("critique", "No critique")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
