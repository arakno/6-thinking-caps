"""Base agent class."""
import time
from abc import ABC, abstractmethod
from typing import Optional

from backend.models.session import AgentResult, SessionContext
from backend.services.llm_client import LLMClient
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseAgent(ABC):
    """Base class for all thinking hat agents."""

    def __init__(self, llm_client: LLMClient):
        """Initialize agent with LLM client."""
        self.llm_client = llm_client
        self.hat_color: str = ""
        self.agent_name: str = ""

    @abstractmethod
    def build_prompt(self, context: SessionContext) -> str:
        """Build the prompt for this agent based on session context."""
        pass

    @abstractmethod
    def parse_response(self, response: str) -> dict:
        """Parse the Gemini API response into insights and recommendations."""
        pass

    async def execute(self, context: SessionContext) -> AgentResult:
        """Execute the agent and return results."""
        try:
            start_time = time.time()

            # Build prompt
            prompt = self.build_prompt(context)
            logger.info(f"Executing {self.agent_name} agent")

            # Call LLM API
            response = await self.llm_client.generate(prompt)

            # Parse response
            parsed = self.parse_response(response)

            execution_time = (time.time() - start_time) * 1000  # Convert to ms

            # Create result
            result = AgentResult(
                hat_color=self.hat_color,
                agent_name=self.agent_name,
                thinking_process=response,
                key_insights=parsed.get("insights", []),
                recommendations=parsed.get("recommendations", []),
                confidence_level=parsed.get("confidence", "medium"),
                execution_time_ms=execution_time,
            )

            logger.info(
                f"{self.agent_name} completed in {execution_time:.2f}ms"
            )
            return result

        except Exception as e:
            logger.error(f"Error in {self.agent_name}: {str(e)}")
            raise
