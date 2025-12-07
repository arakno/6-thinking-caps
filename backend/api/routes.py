"""API routes for the application."""
from datetime import datetime
from fastapi import APIRouter, HTTPException, BackgroundTasks
from backend.api.schemas import (
    CreateSessionRequest,
    SessionStatusResponse,
    ProgressResponse,
    ResultsResponse,
    AgentResultResponse,
)
from backend.services.session_manager import get_session_manager
from backend.services.orchestrator import get_orchestrator
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()


@router.post("/sessions", response_model=SessionStatusResponse)
async def create_session(request: CreateSessionRequest):
    """Create a new analysis session."""
    try:
        session_manager = get_session_manager()
        session_id = session_manager.create_session(
            problem_statement=request.problem_statement,
            background_context=request.background_context or "",
        )
        
        context = session_manager.get_session(session_id)
        
        return SessionStatusResponse(
            session_id=session_id,
            status=context.status,
            problem_statement=context.problem_statement,
            created_at=context.created_at.isoformat(),
            updated_at=context.updated_at.isoformat(),
        )
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sessions/{session_id}/analyze")
async def start_analysis(session_id: str, background_tasks: BackgroundTasks):
    """Start the full analysis for a session."""
    try:
        session_manager = get_session_manager()
        context = session_manager.get_session(session_id)
        
        if not context:
            raise HTTPException(status_code=404, detail="Session not found")
        
        if context.status == "processing":
            raise HTTPException(status_code=400, detail="Analysis already in progress")
        
        orchestrator = get_orchestrator()
        
        # Run analysis in background
        background_tasks.add_task(
            _run_analysis, orchestrator, session_manager, context
        )
        
        return {
            "session_id": session_id,
            "status": "initiated",
            "message": "Analysis started"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def _run_analysis(orchestrator, session_manager, context):
    """Background task to run the full analysis."""
    try:
        logger.info(f"Running analysis for session: {context.session_id}")
        result_context = await orchestrator.execute_full_cycle(context)
        session_manager.update_session(context.session_id, result_context)
        logger.info(f"Analysis completed for session: {context.session_id}")
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        context.status = "failed"
        context.error_message = str(e)
        session_manager.update_session(context.session_id, context)


@router.get("/sessions/{session_id}/progress", response_model=ProgressResponse)
async def get_progress(session_id: str):
    """Get progress of an ongoing analysis."""
    try:
        session_manager = get_session_manager()
        context = session_manager.get_session(session_id)
        
        if not context:
            raise HTTPException(status_code=404, detail="Session not found")
        
        completed = [
            color for color, result in context.agent_results.items()
            if result is not None
        ]
        pending = [
            color for color, result in context.agent_results.items()
            if result is None
        ]
        
        return ProgressResponse(
            session_id=session_id,
            status=context.status,
            agents_completed=completed,
            agents_processing=[],
            agents_pending=pending,
            error_message=context.error_message,
            timestamp=datetime.utcnow().isoformat(),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting progress: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}/results", response_model=ResultsResponse)
async def get_results(session_id: str):
    """Get results of a completed analysis."""
    try:
        session_manager = get_session_manager()
        context = session_manager.get_session(session_id)
        
        if not context:
            raise HTTPException(status_code=404, detail="Session not found")
        
        if context.status != "completed":
            raise HTTPException(
                status_code=400,
                detail=f"Analysis not completed. Current status: {context.status}"
            )
        
        # Convert agent results to response format
        results = {}
        for color, agent_result in context.agent_results.items():
            if agent_result:
                results[color] = AgentResultResponse(
                    hat_color=agent_result.hat_color,
                    agent_name=agent_result.agent_name,
                    key_insights=agent_result.key_insights,
                    recommendations=agent_result.recommendations,
                    confidence_level=agent_result.confidence_level,
                    execution_time_ms=agent_result.execution_time_ms,
                )
        
        return ResultsResponse(
            session_id=session_id,
            problem_statement=context.problem_statement,
            background_context=context.background_context,
            status=context.status,
            results=results,
            error_message=context.error_message,
            created_at=context.created_at.isoformat(),
            updated_at=context.updated_at.isoformat(),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting results: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@router.get("/sessions/{session_id}/debug")
async def debug_session(session_id: str):
    """Debug endpoint to see agent execution details."""
    try:
        session_manager = get_session_manager()
        context = session_manager.get_session(session_id)
        
        if not context:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Return detailed info about each agent
        agent_status = {}
        for color, result in context.agent_results.items():
            if result:
                agent_status[color] = {
                    "status": "completed",
                    "agent_name": result.agent_name,
                    "execution_time_ms": result.execution_time_ms,
                }
            else:
                agent_status[color] = {
                    "status": "failed",
                    "error": getattr(context, 'agent_errors', {}).get(color, 'Unknown error'),
                }
        
        return {
            "session_id": session_id,
            "overall_status": context.status,
            "agent_status": agent_status,
            "error_message": context.error_message,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting debug info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
