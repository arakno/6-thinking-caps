import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent, Agent
from google.adk.runners import InMemoryRunner
from google.adk.events import Event
from google.adk.apps import App
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
GEMINI_MODEL = "gemini-2.0-flash"  # Using Gemini 2.0 Flash model
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please add it to your .env file.")

# Note: Make sure your Gemini API key has available quota. 
# Parallel execution makes multiple concurrent requests and may hit quota limits faster.


def check_gemini_availability():
    """Check if Gemini API key is available"""
    return GEMINI_API_KEY is not None

# Define 6 Thinking Hats agents
white_hat = LlmAgent(
    name="WhiteHat",
    model=GEMINI_MODEL,
    instruction="""You are the White Hat — facts-first, neutral summarizer.
    Focus on objective facts and data about the decision."""
)

red_hat = LlmAgent(
    name="RedHat",
    model=GEMINI_MODEL,
    instruction="""You are the Red Hat — capture emotions, tone, and intuition.
    Express how you feel about this decision."""
)

black_hat = LlmAgent(
    name="BlackHat",
    model=GEMINI_MODEL,
    instruction="""You are the Black Hat — find potential problems and risks.
    Identify what could go wrong and potential drawbacks."""
)

yellow_hat = LlmAgent(
    name="YellowHat",
    model=GEMINI_MODEL,
    instruction="""You are the Yellow Hat — identify positives and potential value.
    Focus on the benefits and opportunities."""
)

green_hat = LlmAgent(
    name="GreenHat",
    model=GEMINI_MODEL,
    instruction="""You are the Green Hat — creative thinker. Generate innovative ideas.
    Suggest creative alternatives and new possibilities."""
)

blue_hat = LlmAgent(
    name="BlueHat",
    model=GEMINI_MODEL,
    instruction="""You are the Blue Hat — orchestrator that synthesizes outputs.
    Review all perspectives and provide a balanced recommendation."""
)

# Create ParallelAgent for parallel execution
parallel_hats = ParallelAgent(
    name="ParallelHats",
    sub_agents=[white_hat, red_hat, black_hat, yellow_hat, green_hat]
)

# Create SequentialAgent for the workflow
workflow = SequentialAgent(
    name="SixHatsWorkflow",
    sub_agents=[parallel_hats, blue_hat]
)

# Create ADK App instance
app = App(name="six_hats", root_agent=workflow)

async def run_six_hats_workflow(user_prompt: str) -> dict:
    """
    Execute the Six Hats workflow asynchronously using ADK runner.

    Returns: Dictionary with results from all agents
    """
    try:
        logging.info(f"Initializing workflow for prompt: {user_prompt}")

        # Create InMemoryRunner with the app
        runner = InMemoryRunner(app=app)

        # Run the workflow using debug mode (simpler approach)
        logging.info("Starting workflow execution...")
        result = await runner.run_debug(user_prompt)

        # Parse the result - parallel execution provides synthesized output
        results = {
            "final_synthesis": result.content if result and hasattr(result, 'content') else str(result) if result else "No result",
        }

        logging.info("Workflow execution completed")
        return results

    except Exception as e:
        logging.error(f"Workflow execution failed: {str(e)}")
        raise

async def main():
    """Test the Six Thinking Hats workflow"""
    logging.info("Starting Six Thinking Hats workflow test...")
    
    # Check if Gemini API key is available
    if not check_gemini_availability():
        logging.error("Gemini API key is not available")
        print("Please ensure GEMINI_API_KEY is set in your .env file.")
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
                # Truncate long responses for better readability
                display_value = value[:800] + "..." if len(str(value)) > 800 else str(value)
                print(f"  {display_value}")
        
        print("\n" + "="*60)
        
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        print(f"Workflow failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
