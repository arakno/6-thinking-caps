"""Tests for agents."""
from unittest.mock import AsyncMock, MagicMock
import pytest
from backend.agents.white_hat import WhiteHatAgent
from backend.models.session import SessionContext


@pytest.mark.asyncio
async def test_white_hat_build_prompt():
    """Test White Hat prompt building."""
    mock_client = MagicMock()
    agent = WhiteHatAgent(mock_client)
    
    context = SessionContext(
        session_id="test",
        problem_statement="Test problem",
        background_context="Test context"
    )
    
    prompt = agent.build_prompt(context)
    assert "White Hat" in prompt
    assert "Test problem" in prompt
    assert "facts" in prompt.lower()


def test_white_hat_parse_response():
    """Test White Hat response parsing."""
    mock_client = MagicMock()
    agent = WhiteHatAgent(mock_client)
    
    parsed = agent.parse_response("Test response")
    
    assert "insights" in parsed
    assert "recommendations" in parsed
    assert "confidence" in parsed
    assert parsed["confidence"] == "high"
