"""Tests for agent orchestrator."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from backend.services.orchestrator import AgentOrchestrator
from backend.models.session import SessionContext


@pytest.mark.asyncio
async def test_orchestrator_initialization():
    """Test orchestrator initializes with all agents."""
    mock_client = MagicMock()
    orchestrator = AgentOrchestrator(mock_client)
    
    assert len(orchestrator.agents) == 6
    assert "white" in orchestrator.agents
    assert "blue" in orchestrator.agents


@pytest.mark.asyncio
async def test_execute_parallel():
    """Test parallel execution of agents."""
    mock_client = MagicMock()
    mock_client.generate = AsyncMock(return_value="Test response")
    
    orchestrator = AgentOrchestrator(mock_client)
    
    context = SessionContext(
        session_id="test-123",
        problem_statement="Test problem",
    )
    
    results = await orchestrator.execute_parallel(context)
    
    assert len(results) == 5  # All except blue
    assert "white" in results
    assert "red" in results


@pytest.mark.asyncio
async def test_execute_synthesis():
    """Test blue hat synthesis execution."""
    mock_client = MagicMock()
    mock_client.generate = AsyncMock(return_value="Synthesis response")
    
    orchestrator = AgentOrchestrator(mock_client)
    
    context = SessionContext(
        session_id="test-123",
        problem_statement="Test problem",
    )
    
    # Add some dummy results
    for color in ["white", "red", "black", "yellow", "green"]:
        context.agent_results[color] = MagicMock()
    
    result = await orchestrator.execute_synthesis(context)
    
    assert result is not None
    assert context.agent_results["blue"] is not None
