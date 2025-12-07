"""Yellow Hat Agent - Optimistic Vision."""
from backend.agents.base_agent import BaseAgent
from backend.models.session import SessionContext


class YellowHatAgent(BaseAgent):
    """Yellow Hat: Focuses on optimism, benefits, and opportunities."""

    def __init__(self, gemini_client):
        super().__init__(gemini_client)
        self.hat_color = "yellow"
        self.agent_name = "Yellow Hat (Vision & Optimism)"

    def build_prompt(self, context: SessionContext) -> str:
        """Build prompt for optimistic vision."""
        prompt = f"""You are an optimistic, forward-thinking analyst using the Yellow Hat thinking approach.

Problem Statement:
{context.problem_statement}

Background Context:
{context.background_context if context.background_context else "None provided"}

Your task is to analyze this problem from an optimistic, opportunity-focused perspective:
1. What are the potential benefits and opportunities?
2. What positive outcomes are possible?
3. How could this create value?
4. What best-case scenarios exist?
5. What success would look like
6. How could this improve the situation?

Be constructive and focus on possibilities, benefits, and positive potential."""
        return prompt

    def parse_response(self, response: str) -> dict:
        """Parse Yellow Hat response."""
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        insights = lines[:5] if lines else ["Identified opportunities"]
        recommendations = lines[5:10] if len(lines) > 5 else ["Capitalize on opportunities", "Pursue initiatives"]
        
        return {
            "insights": insights[:5],
            "recommendations": recommendations[:5],
            "confidence": "high",
        }
