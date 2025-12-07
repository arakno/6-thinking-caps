"""Red Hat Agent - Emotions and Intuition."""
from backend.agents.base_agent import BaseAgent
from backend.models.session import SessionContext


class RedHatAgent(BaseAgent):
    """Red Hat: Focuses on emotions, intuitions, and gut feelings."""

    def __init__(self, gemini_client):
        super().__init__(gemini_client)
        self.hat_color = "red"
        self.agent_name = "Red Hat (Emotions & Intuition)"

    def build_prompt(self, context: SessionContext) -> str:
        """Build prompt for emotional/intuitive analysis."""
        prompt = f"""You are an intuitive, emotionally-aware analyst using the Red Hat thinking approach.

Problem Statement:
{context.problem_statement}

Background Context:
{context.background_context if context.background_context else "None provided"}

Your task is to analyze this problem from an emotional and intuitive perspective:
1. What are your gut feelings about this situation?
2. What emotional dimensions are present?
3. What concerns or fears might stakeholders have?
4. What opportunities generate excitement?
5. How do people likely feel about potential solutions?

Provide your analysis focusing on emotions, feelings, hunches, and intuitive insights."""
        return prompt

    def parse_response(self, response: str) -> dict:
        """Parse Red Hat response."""
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        insights = lines[:5] if lines else ["Analyzed from emotional perspective"]
        recommendations = lines[5:10] if len(lines) > 5 else ["Address emotional concerns", "Foster enthusiasm"]
        
        return {
            "insights": insights[:5],
            "recommendations": recommendations[:5],
            "confidence": "medium",
        }
