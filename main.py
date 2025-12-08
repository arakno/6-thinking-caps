import asyncio
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent, Agent
from google.adk.runners import InMemoryRunner  # ← ADD THIS
from google.adk.events import Event  # ← ADD THIS
from dotenv import load_dotenv
import os
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Load environment variables
load_dotenv()

# Configuration
OLLAMA_MODEL = "granite4:350m"
OLLAMA_BASE_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")


async def check_ollama_health():
    """Check if Ollama is running and accessible"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            return response.status_code == 200
    except Exception:
        return False

# Define 6 Thinking Hats agents
white_hat = LlmAgent(
    name="WhiteHat",
    model=OLLAMA_MODEL,
    instruction="""You are the White Hat — facts-first, neutral summarizer.
    Focus on objective facts and data about the decision."""
)

red_hat = LlmAgent(
    name="RedHat",
    model=OLLAMA_MODEL,
    instruction="""You are the Red Hat — capture emotions, tone, and intuition.
    Express how you feel about this decision."""
)

black_hat = LlmAgent(
    name="BlackHat",
    model=OLLAMA_MODEL,
    instruction="""You are the Black Hat — find potential problems and risks.
    Identify what could go wrong and potential drawbacks."""
)

yellow_hat = LlmAgent(
    name="YellowHat",
    model=OLLAMA_MODEL,
    instruction="""You are the Yellow Hat — identify positives and potential value.
    Focus on the benefits and opportunities."""
)

green_hat = LlmAgent(
    name="GreenHat",
    model=OLLAMA_MODEL,
    instruction="""You are the Green Hat — creative thinker. Generate innovative ideas.
    Suggest creative alternatives and new possibilities."""
)

blue_hat = LlmAgent(
    name="BlueHat",
    model=OLLAMA_MODEL,
    instruction="""You are the Blue Hat — orchestrator that synthesizes outputs.
    Review all perspectives and provide a balanced recommendation."""
)

# Create ParallelAgent for parallel execution
parallel_hats = ParallelAgent(
    name="ParallelHats",
    sub_agents=[white_hat, red_hat, black_hat, yellow_hat, green_hat]
)

# Create SequentialAgent for the workflow
sequential_workflow = SequentialAgent(
    name="SixHatsWorkflow",
    sub_agents=[parallel_hats, blue_hat]
)

async def run_six_hats_workflow(user_prompt: str) -> dict:
    """
    Execute the Six Hats workflow asynchronously using ADK runner.

    Returns: Dictionary with results from all agents
    """
    try:
        logging.info(f"Initializing workflow for prompt: {user_prompt}")

        # Create InMemoryRunner with the sequential workflow
        runner = InMemoryRunner(sequential_workflow)

        # Run the workflow using debug mode (simpler approach)
        logging.info("Starting workflow execution...")
        result = await runner.run_debug(user_prompt)

        # Parse the result
        results = {
            "white_output": None,
            "red_output": None,
            "black_output": None,
            "yellow_output": None,
            "green_output": None,
            "blue_output": None,
        }

        # The result should contain the final output from the blue hat
        if result and hasattr(result, 'content'):
            results["blue_output"] = result.content
        elif isinstance(result, str):
            results["blue_output"] = result
        else:
            # If result is a dict or other structure, extract as needed
            results.update(result if isinstance(result, dict) else {"result": str(result)})

        logging.info("Workflow execution completed")
        return results

    except Exception as e:
        logging.error(f"Workflow execution failed: {str(e)}")
        raise

async def main():
    """Test the Six Thinking Hats workflow"""
    logging.info("Starting Six Thinking Hats workflow test...")
    
    # Check if Ollama is running
    if not await check_ollama_health():
        logging.error("Ollama service is not available")
        print("Please ensure Ollama is running and the granite4:350m model is pulled.")
        return
    
    try:
        test_prompt = "Should I invest in renewable energy stocks?"
        logging.info(f"Running workflow for prompt: {test_prompt}")
        
        # Execute the workflow
        results = await run_six_hats_workflow(test_prompt)
        
        print("\n" + "="*60)
        print("WORKFLOW COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\nPrompt: {test_prompt}\n")
        
        print("Results:")
        for key, value in results.items():
            if value:
                print(f"\n{key.upper()}:")
                print(f"  {value[:200]}..." if len(str(value)) > 200 else f"  {value}")
        
        print("\n" + "="*60)
        
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        print(f"Workflow failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
