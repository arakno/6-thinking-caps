"""Agent orchestrator for coordinating multi-agent execution."""
import asyncio
from typing import Dict, List
from backend.agents.white_hat import WhiteHatAgent
from backend.agents.red_hat import RedHatAgent
from backend.agents.black_hat import BlackHatAgent
from backend.agents.yellow_hat import YellowHatAgent
from backend.agents.green_hat import GreenHatAgent
from backend.agents.blue_hat import BlueHatAgent
from backend.models.session import SessionContext, AgentResult
from backend.services.llm_client import LLMClient
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class AgentOrchestrator:
    """Orchestrates execution of all thinking hat agents."""

    def __init__(self, llm_client: LLMClient):
        """Initialize orchestrator with LLM client."""
        self.llm_client = llm_client
        self.agents = {
            "white": WhiteHatAgent(llm_client),
            "red": RedHatAgent(llm_client),
            "black": BlackHatAgent(llm_client),
            "yellow": YellowHatAgent(llm_client),
            "green": GreenHatAgent(llm_client),
            "blue": BlueHatAgent(llm_client),
        }
        logger.info("Initialized AgentOrchestrator with 6 agents")

    async def execute_parallel(
        self, context: SessionContext, hat_colors: List[str] = None
    ) -> Dict[str, AgentResult]:
        """Execute specified agents in parallel.
        
        Args:
            context: Session context
            hat_colors: List of hat colors to execute (default: all except blue)
            
        Returns:
            Dictionary mapping hat colors to results
        """
        if hat_colors is None:
            hat_colors = ["white", "red", "black", "yellow", "green"]

        logger.info(f"Starting parallel execution of {len(hat_colors)} agents")
        
        tasks = [
            (color, self.agents[color].execute(context))
            for color in hat_colors
            if color in self.agents
        ]

        results = {}
        try:
            # Execute all tasks concurrently using gather
            task_list = [task for _, task in tasks]
            all_results = await asyncio.gather(*task_list, return_exceptions=True)
            
            # Store results and handle any exceptions
            for (color, _), result in zip(tasks, all_results):
                if isinstance(result, Exception):
                    error_msg = f"{self.agents[color].agent_name} failed: {type(result).__name__}: {str(result)}"
                    logger.error(f"✗ {error_msg}")
                    context.agent_results[color] = None
                    # Store error in context for debugging
                    if not hasattr(context, 'agent_errors'):
                        context.agent_errors = {}
                    context.agent_errors[color] = error_msg
                else:
                    results[color] = result
                    context.agent_results[color] = result
                    logger.info(f"✓ {self.agents[color].agent_name} completed successfully")
        except Exception as e:
            logger.error(f"Error during parallel execution: {str(e)}")
            raise

        return results

    async def execute_synthesis(self, context: SessionContext) -> AgentResult:
        """Execute Blue Hat agent to synthesize results.
        
        Args:
            context: Session context with other hat results
            
        Returns:
            Blue Hat synthesis result
        """
        logger.info("Starting synthesis (Blue Hat)")
        
        try:
            result = await self.agents["blue"].execute(context)
            context.agent_results["blue"] = result
            context.synthesis_result = result
            logger.info("✓ Blue Hat synthesis completed")
            return result
        except Exception as e:
            logger.error(f"Error during synthesis: {str(e)}")
            raise

    async def execute_full_cycle(self, context: SessionContext) -> SessionContext:
        """Execute full thinking cycle: 5 hats in parallel + blue hat synthesis.
        
        Args:
            context: Session context
            
        Returns:
            Updated context with all results
        """
        logger.info(f"Starting full cycle for session: {context.session_id}")
        context.status = "processing"

        try:
            # Phase 1: Execute first 5 hats in parallel
            await self.execute_parallel(context)
            
            # Phase 2: Execute Blue Hat synthesis
            await self.execute_synthesis(context)
            
            context.status = "completed"
            logger.info(f"✓ Full cycle completed for session: {context.session_id}")
            return context

        except Exception as e:
            context.status = "failed"
            logger.error(f"Full cycle failed: {str(e)}")
            raise


# Global orchestrator instance
_orchestrator: AgentOrchestrator | None = None


def get_orchestrator() -> AgentOrchestrator:
    """Get or create global orchestrator."""
    global _orchestrator
    if _orchestrator is None:
        from backend.services.llm_factory import create_llm_client
        llm_client = create_llm_client()
        _orchestrator = AgentOrchestrator(llm_client)
    return _orchestrator
