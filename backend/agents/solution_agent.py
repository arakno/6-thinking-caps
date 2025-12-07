"""Solution Agent - Final Actionable Solution."""
from backend.agents.base_agent import BaseAgent
from backend.models.session import SessionContext


class SolutionAgent(BaseAgent):
    """Solution Agent: Generates concrete actionable solution based on all perspectives."""

    def __init__(self, llm_client):
        super().__init__(llm_client)
        self.hat_color = "solution"
        self.agent_name = "Solution Generator"

    def build_prompt(self, context: SessionContext) -> str:
        """Build prompt for solution generation."""
        # Build summary of all hat results
        hat_summaries = []
        
        if context.agent_results.get("white"):
            hat_summaries.append(f"WHITE HAT (Facts):\n{context.agent_results['white'].thinking_process[:800]}")
        
        if context.agent_results.get("red"):
            hat_summaries.append(f"RED HAT (Emotions):\n{context.agent_results['red'].thinking_process[:800]}")
        
        if context.agent_results.get("black"):
            hat_summaries.append(f"BLACK HAT (Risks):\n{context.agent_results['black'].thinking_process[:800]}")
        
        if context.agent_results.get("yellow"):
            hat_summaries.append(f"YELLOW HAT (Opportunities):\n{context.agent_results['yellow'].thinking_process[:800]}")
        
        if context.agent_results.get("green"):
            hat_summaries.append(f"GREEN HAT (Creativity):\n{context.agent_results['green'].thinking_process[:800]}")
        
        if context.agent_results.get("blue"):
            hat_summaries.append(f"BLUE HAT (Synthesis):\n{context.agent_results['blue'].thinking_process[:800]}")

        all_perspectives = "\n\n".join(hat_summaries)

        prompt = f"""You are a strategic decision-making expert. Based on the comprehensive 6 Thinking Hats analysis below, provide a CONCRETE, ACTIONABLE SOLUTION to the problem.

ORIGINAL PROBLEM:
{context.problem_statement}

BACKGROUND:
{context.background_context if context.background_context else "None provided"}

ANALYSIS FROM ALL PERSPECTIVES:
{all_perspectives}

Your task is to synthesize all the above perspectives and provide a CLEAR, ACTIONABLE SOLUTION that includes:

1. RECOMMENDED DECISION: A clear yes/no/conditional recommendation with specific conditions
2. ACTION PLAN: Step-by-step implementation plan with timeline (be specific - include months/quarters)
3. RESOURCE REQUIREMENTS: What resources, budget, team members are needed
4. RISK MITIGATION: Top 3 risks and how to address each one
5. SUCCESS METRICS: How to measure if this solution is working (specific KPIs)
6. NEXT STEPS: Immediate actions to take in the next 30 days

Be specific, practical, and actionable. Focus on what to DO, not just what to think about.
Format your response with clear sections and bullet points."""
        return prompt

    def parse_response(self, response: str) -> dict:
        """Parse Solution response."""
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        
        # Try to extract key sections
        insights = []
        recommendations = []
        
        for i, line in enumerate(lines):
            # Look for action-oriented content
            if any(keyword in line.lower() for keyword in ['recommend', 'decision', 'action', 'step']):
                if len(insights) < 5:
                    insights.append(line)
            elif any(keyword in line.lower() for keyword in ['should', 'must', 'need to', 'implement']):
                if len(recommendations) < 5:
                    recommendations.append(line)
        
        # Fallback if extraction didn't work well
        if not insights:
            insights = lines[:5] if lines else ["Solution generated based on analysis"]
        if not recommendations:
            recommendations = lines[5:10] if len(lines) > 5 else ["Follow the implementation plan", "Monitor progress regularly"]
        
        return {
            "insights": insights[:5],
            "recommendations": recommendations[:5],
            "confidence": "high",
        }
