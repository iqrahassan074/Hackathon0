"""
Tests for AI endpoints
"""
import pytest
from fastapi import status


class TestAIRecommendations:
    """Test AI recommendation endpoint"""

    def test_get_recommendations(self, client, auth_headers):
        """Test getting AI recommendations"""
        response = client.post(
            "/api/v1/ai/recommend",
            json={},
            headers=auth_headers
        )
        # Should return fallback recommendations if AI unavailable
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "recommendations" in data
        assert isinstance(data["recommendations"], list)

    def test_get_recommendations_with_context(self, client, auth_headers):
        """Test getting recommendations with context"""
        response = client.post(
            "/api/v1/ai/recommend",
            json={"context": "Help me prioritize my work tasks"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK


class TestAIOptimize:
    """Test task optimization endpoint"""

    def test_optimize_task(self, client, auth_headers, db_session, test_user):
        """Test optimizing a task"""
        from app.models.task import Task
        task = Task(user_id=test_user.id, title="Test Task")
        db_session.add(task)
        db_session.commit()
        
        response = client.post(
            "/api/v1/ai/optimize",
            json={"task_id": str(task.id)},
            headers=auth_headers
        )
        # May return fallback if AI unavailable
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_503_SERVICE_UNAVAILABLE]


class TestAIHistory:
    """Test AI history endpoint"""

    def test_get_history(self, client, auth_headers):
        """Test getting AI history"""
        response = client.get("/api/v1/ai/history", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
