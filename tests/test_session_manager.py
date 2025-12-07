"""Tests for session management."""
import pytest
from backend.services.session_manager import SessionManager


def test_create_session():
    """Test creating a new session."""
    manager = SessionManager()
    session_id = manager.create_session(
        problem_statement="Test problem",
        background_context="Test context"
    )
    
    assert session_id is not None
    context = manager.get_session(session_id)
    assert context is not None
    assert context.problem_statement == "Test problem"
    assert context.background_context == "Test context"


def test_get_nonexistent_session():
    """Test getting a session that doesn't exist."""
    manager = SessionManager()
    context = manager.get_session("nonexistent")
    assert context is None


def test_update_session():
    """Test updating a session."""
    manager = SessionManager()
    session_id = manager.create_session("Test problem")
    context = manager.get_session(session_id)
    
    context.status = "processing"
    manager.update_session(session_id, context)
    
    updated = manager.get_session(session_id)
    assert updated.status == "processing"


def test_delete_session():
    """Test deleting a session."""
    manager = SessionManager()
    session_id = manager.create_session("Test problem")
    
    deleted = manager.delete_session(session_id)
    assert deleted is True
    
    context = manager.get_session(session_id)
    assert context is None


def test_delete_nonexistent_session():
    """Test deleting a session that doesn't exist."""
    manager = SessionManager()
    deleted = manager.delete_session("nonexistent")
    assert deleted is False
