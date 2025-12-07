"""White Hat Agent - Facts and Information."""
from backend.agents.base_agent import BaseAgent
from backend.models.session import SessionContext


class WhiteHatAgent(BaseAgent):
    """White Hat: Focuses on facts, data, and objective information."""

    def __init__(self, gemini_client):
        super().__init__(gemini_client)
        self.hat_color = "white"
        self.agent_name = "White Hat (Facts & Data)"

    def build_prompt(self, context: SessionContext) -> str:
        """Build prompt for factual analysis."""
        prompt = f"""You are a logical, objective analyst using the White Hat thinking approach.

Problem Statement:
{context.problem_statement}

Background Context:
{context.background_context if context.background_context else "None provided"}

Your task is to analyze this problem objectively and extract:
1. Known facts and verifiable data
2. Information sources and their reliability
3. Data gaps that need to be addressed
4. Assumptions being made
5. What we don't know

Provide your analysis in a structured format with clear sections for Facts, Data Gaps, and Key Assumptions."""
        return prompt

    def parse_response(self, response: str) -> dict:
        """Parse White Hat response."""
        # Extract lines from response and use them as insights
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        insights = lines[:5] if lines else ["Analyzed from factual perspective"]
        recommendations = lines[5:10] if len(lines) > 5 else ["Gather missing data", "Verify assumptions"]
        
        return {
            "insights": insights[:5],
            "recommendations": recommendations[:5],
            "confidence": "high",
        }
