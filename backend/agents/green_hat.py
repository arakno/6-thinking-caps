"""Green Hat Agent - Creative Innovation."""
from backend.agents.base_agent import BaseAgent
from backend.models.session import SessionContext


class GreenHatAgent(BaseAgent):
    """Green Hat: Focuses on creativity, alternatives, and new ideas."""

    def __init__(self, gemini_client):
        super().__init__(gemini_client)
        self.hat_color = "green"
        self.agent_name = "Green Hat (Creativity & Innovation)"

    def build_prompt(self, context: SessionContext) -> str:
        """Build prompt for creative thinking."""
        prompt = f"""You are a creative, innovative analyst using the Green Hat thinking approach.

Problem Statement:
{context.problem_statement}

Background Context:
{context.background_context if context.background_context else "None provided"}

Your task is to generate creative ideas and alternatives:
1. What unconventional approaches could work?
2. What new ideas haven't been considered?
3. How could we completely rethink this?
4. What if we removed constraints?
5. What creative solutions are possible?
6. What lateral thinking approaches apply?

Generate multiple creative ideas and alternative approaches. Think outside the box."""
        return prompt

    def parse_response(self, response: str) -> dict:
        """Parse Green Hat response."""
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        insights = lines[:5] if lines else ["Generated creative alternatives"]
        recommendations = lines[5:10] if len(lines) > 5 else ["Test creative ideas", "Combine best ideas"]
        
        return {
            "insights": insights[:5],
            "recommendations": recommendations[:5],
            "confidence": "medium",
        }
