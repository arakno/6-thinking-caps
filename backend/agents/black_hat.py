"""Black Hat Agent - Critical Analysis."""
from backend.agents.base_agent import BaseAgent
from backend.models.session import SessionContext


class BlackHatAgent(BaseAgent):
    """Black Hat: Focuses on critical analysis, risks, and problems."""

    def __init__(self, gemini_client):
        super().__init__(gemini_client)
        self.hat_color = "black"
        self.agent_name = "Black Hat (Critical Analysis)"

    def build_prompt(self, context: SessionContext) -> str:
        """Build prompt for critical analysis."""
        prompt = f"""You are a critical, skeptical analyst using the Black Hat thinking approach.

Problem Statement:
{context.problem_statement}

Background Context:
{context.background_context if context.background_context else "None provided"}

Your task is to analyze this problem critically and identify:
1. Potential risks and threats
2. Problems and weaknesses in approaches
3. What could go wrong?
4. Hidden challenges and obstacles
5. Why this might fail
6. Devil's advocate perspective

Be thorough and rigorous. Identify ALL potential issues and vulnerabilities."""
        return prompt

    def parse_response(self, response: str) -> dict:
        """Parse Black Hat response."""
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        insights = lines[:5] if lines else ["Identified critical risks"]
        recommendations = lines[5:10] if len(lines) > 5 else ["Mitigate identified risks", "Plan contingencies"]
        
        return {
            "insights": insights[:5],
            "recommendations": recommendations[:5],
            "confidence": "high",
        }
