"""
Tests for task endpoints
"""
import pytest
from fastapi import status
import uuid


class TestCreateTask:
    """Test task creation"""

    def test_create_task_success(self, client, auth_headers):
        """Test successful task creation"""
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": "pending",
            "priority": "medium"
        }
        response = client.post("/api/v1/tasks/", json=task_data, headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "Test description"
        assert "id" in data
        assert "user_id" in data

    def test_create_task_unauthorized(self, client):
        """Test task creation without authentication"""
        response = client.post("/api/v1/tasks/", json={"title": "Test"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_task_missing_title(self, client, auth_headers):
        """Test task creation without title"""
        response = client.post("/api/v1/tasks/", json={}, headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetTasks:
    """Test getting tasks"""

    def test_get_tasks_success(self, client, auth_headers):
        """Test getting all tasks"""
        response = client.get("/api/v1/tasks/", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_get_tasks_with_filter(self, client, auth_headers, test_user):
        """Test getting tasks with status filter"""
        # Create a task first
        client.post(
            "/api/v1/tasks/",
            json={"title": "Test", "status": "pending"},
            headers=auth_headers
        )
        response = client.get(
            "/api/v1/tasks/?status=pending",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        tasks = response.json()
        assert len(tasks) > 0
        assert all(t["status"] == "pending" for t in tasks)


class TestGetTask:
    """Test getting single task"""

    def test_get_task_success(self, client, auth_headers, db_session, test_user):
        """Test getting a specific task"""
        from app.models.task import Task
        task = Task(
            user_id=test_user.id,
            title="Test Task",
            description="Test"
        )
        db_session.add(task)
        db_session.commit()
        
        response = client.get(f"/api/v1/tasks/{task.id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == str(task.id)

    def test_get_task_not_found(self, client, auth_headers):
        """Test getting non-existent task"""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/tasks/{fake_id}", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateTask:
    """Test task update"""

    def test_update_task_success(self, client, auth_headers, db_session, test_user):
        """Test updating a task"""
        from app.models.task import Task
        task = Task(user_id=test_user.id, title="Original")
        db_session.add(task)
        db_session.commit()
        
        response = client.put(
            f"/api/v1/tasks/{task.id}",
            json={"title": "Updated"},
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "Updated"


class TestDeleteTask:
    """Test task deletion"""

    def test_delete_task_success(self, client, auth_headers, db_session, test_user):
        """Test deleting a task"""
        from app.models.task import Task
        task = Task(user_id=test_user.id, title="To Delete")
        db_session.add(task)
        db_session.commit()
        
        response = client.delete(f"/api/v1/tasks/{task.id}", headers=auth_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_mark_task_complete(self, client, auth_headers, db_session, test_user):
        """Test marking task as complete"""
        from app.models.task import Task, TaskStatus
        task = Task(user_id=test_user.id, title="Complete Me", status="pending")
        db_session.add(task)
        db_session.commit()
        
        response = client.patch(
            f"/api/v1/tasks/{task.id}/complete",
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "completed"
