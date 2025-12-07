"""Blue Hat Agent - Synthesis and Control."""
from backend.agents.base_agent import BaseAgent
from backend.models.session import SessionContext


class BlueHatAgent(BaseAgent):
    """Blue Hat: Synthesis, control, and meta-analysis of all perspectives."""

    def __init__(self, gemini_client):
        super().__init__(gemini_client)
        self.hat_color = "blue"
        self.agent_name = "Blue Hat (Synthesis & Control)"

    def build_prompt(self, context: SessionContext) -> str:
        """Build prompt for synthesis and analysis."""
        # Build summary of all previous hat results
        other_results = []
        for color, result in context.agent_results.items():
            if result and color != "blue":
                other_results.append(
                    f"{result.hat_color}: {result.thinking_process[:500]}"
                )

        other_hats_summary = "\n\n".join(other_results)

        prompt = f"""You are a strategic synthesizer and controller using the Blue Hat thinking approach.

Problem Statement:
{context.problem_statement}

Background Context:
{context.background_context if context.background_context else "None provided"}

Previous Analysis from Other Hats:
{other_hats_summary}

Your task is to synthesize all perspectives and provide:
1. Summary of key findings from all perspectives
2. Common themes and agreements
3. Key conflicts and tensions
4. Risk assessment (combining all perspectives)
5. Opportunities assessment
6. Recommended next steps and action plan
7. Decision framework for implementation

Integrate all thinking styles into a coherent, actionable summary."""
        return prompt

    def parse_response(self, response: str) -> dict:
        """Parse Blue Hat response."""
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        insights = lines[:5] if lines else ["Synthesized all perspectives"]
        recommendations = lines[5:10] if len(lines) > 5 else ["Implement recommended actions", "Monitor outcomes"]
        
        return {
            "insights": insights[:5],
            "recommendations": recommendations[:5],
            "confidence": "high",
        }
