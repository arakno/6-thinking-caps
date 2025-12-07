"""Session and context models."""
from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class AgentResult(BaseModel):
    """Result from a single thinking hat agent."""

    hat_color: str
    agent_name: str
    thinking_process: str
    key_insights: list[str]
    recommendations: list[str]
    confidence_level: str  # high/medium/low
    tokens_used: int = 0
    execution_time_ms: float = 0.0


class SessionContext(BaseModel):
    """Session context containing problem statement and agent results."""

    session_id: str
    problem_statement: str
    background_context: str = ""
    agent_results: Dict[str, Optional[AgentResult]] = Field(
        default_factory=lambda: {
            "white": None,
            "red": None,
            "black": None,
            "yellow": None,
            "green": None,
            "blue": None,
            "solution": None,
        }
    )
    synthesis_result: Optional[AgentResult] = None
    solution_result: Optional[AgentResult] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "initialized"  # initialized, processing, completed, failed

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
