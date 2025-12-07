"""API request and response schemas."""
from pydantic import BaseModel, Field
from typing import Optional


class CreateSessionRequest(BaseModel):
    """Request to create a new analysis session."""
    
    problem_statement: str = Field(..., min_length=10, description="The problem to analyze")
    background_context: Optional[str] = Field(None, description="Optional background information")


class SessionStatusResponse(BaseModel):
    """Response with session status."""
    
    session_id: str
    status: str
    problem_statement: str
    created_at: str
    updated_at: str


class AgentResultResponse(BaseModel):
    """Single agent result response."""
    
    hat_color: str
    agent_name: str
    key_insights: list[str]
    recommendations: list[str]
    confidence_level: str
    execution_time_ms: float


class ProgressResponse(BaseModel):
    """Progress update response."""
    
    session_id: str
    status: str
    agents_completed: list[str]
    agents_processing: list[str]
    agents_pending: list[str]
    error_message: Optional[str] = None
    timestamp: str


class ResultsResponse(BaseModel):
    """Full results response."""
    
    session_id: str
    problem_statement: str
    background_context: str
    status: str
    results: dict[str, AgentResultResponse]
    error_message: Optional[str] = None
    created_at: str
    updated_at: str
