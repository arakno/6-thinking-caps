"""Session manager for handling user sessions."""
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional
from backend.models.session import SessionContext
from backend.config import settings
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class SessionManager:
    """Manages user sessions with TTL-based cleanup."""

    def __init__(self):
        """Initialize session manager."""
        self._sessions: Dict[str, SessionContext] = {}
        logger.info("SessionManager initialized")

    def create_session(self, problem_statement: str, background_context: str = "") -> str:
        """Create a new session.
        
        Args:
            problem_statement: The problem to analyze
            background_context: Optional background information
            
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        context = SessionContext(
            session_id=session_id,
            problem_statement=problem_statement,
            background_context=background_context,
        )
        self._sessions[session_id] = context
        logger.info(f"Created session: {session_id}")
        return session_id

    def get_session(self, session_id: str) -> Optional[SessionContext]:
        """Get a session by ID.
        
        Args:
            session_id: The session ID
            
        Returns:
            SessionContext or None if not found
        """
        return self._sessions.get(session_id)

    def update_session(self, session_id: str, context: SessionContext) -> None:
        """Update a session.
        
        Args:
            session_id: The session ID
            context: Updated context
        """
        context.updated_at = datetime.utcnow()
        self._sessions[session_id] = context
        logger.debug(f"Updated session: {session_id}")

    def cleanup_old_sessions(self) -> int:
        """Remove sessions older than TTL.
        
        Returns:
            Number of sessions cleaned up
        """
        now = datetime.utcnow()
        ttl = timedelta(minutes=settings.session_ttl_minutes)
        
        to_delete = [
            sid for sid, ctx in self._sessions.items()
            if now - ctx.updated_at > ttl
        ]
        
        for sid in to_delete:
            del self._sessions[sid]
        
        if to_delete:
            logger.info(f"Cleaned up {len(to_delete)} old sessions")
        
        return len(to_delete)

    def get_all_sessions(self) -> Dict[str, SessionContext]:
        """Get all sessions (for debugging)."""
        return self._sessions.copy()

    def delete_session(self, session_id: str) -> bool:
        """Delete a session.
        
        Args:
            session_id: The session ID
            
        Returns:
            True if deleted, False if not found
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info(f"Deleted session: {session_id}")
            return True
        return False


# Global session manager instance
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """Get or create global session manager."""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
