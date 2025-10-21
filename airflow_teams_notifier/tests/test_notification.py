"""
Tests for notification functionality.
"""
import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from src.models.servicenow_ticket import ServiceNowTicket
from src.models.airflow_failure import AirflowDagFailure
from src.notifiers.teams_notifier import TeamsNotifier
from src.notifiers.notification_manager import NotificationManager


class TestNotificationManager:
    """Tests for NotificationManager."""

    @pytest.fixture
    def teams_notifier(self):
        """Create a TeamsNotifier instance for testing."""
        return TeamsNotifier("https://test.webhook.url")

    @pytest.fixture
    def notification_manager(self, teams_notifier):
        """Create a NotificationManager instance for testing."""
        return NotificationManager(teams_notifier)

    @pytest.fixture
    def dag_failure(self):
        """Create a sample DAG failure."""
        return AirflowDagFailure(
            dag_id="test_dag",
            task_id="test_task",
            execution_date=datetime(2024, 1, 1, 12, 0, 0),
            error_message="Test error message"
        )

    @pytest.fixture
    def snow_ticket(self):
        """Create a sample ServiceNow ticket."""
        return ServiceNowTicket(
            ticket_number="INC0012345",
            description="Test incident",
            priority="P1",
            assigned_to="Test User",
            status="New"
        )

    def test_create_teams_message_without_ticket(self, notification_manager, dag_failure):
        """Test creating a Teams message without ServiceNow ticket."""
        message = notification_manager.create_teams_message(None, dag_failure)

        assert message["type"] == "message"
        assert len(message["attachments"]) == 1
        assert message["attachments"][0]["contentType"] == "application/vnd.microsoft.card.adaptive"

        body = message["attachments"][0]["content"]["body"]
        assert any("Airflow DAG Failure Alert" in str(item) for item in body)
        assert not any("ServiceNow" in str(item) for item in body)

    def test_create_teams_message_with_ticket(self, notification_manager, dag_failure, snow_ticket):
        """Test creating a Teams message with ServiceNow ticket."""
        message = notification_manager.create_teams_message(snow_ticket, dag_failure)

        body = message["attachments"][0]["content"]["body"]
        assert any("Airflow DAG Failure Alert" in str(item) for item in body)
        assert any("ServiceNow" in str(item) for item in body)

    @patch('src.notifiers.notification_manager.requests.post')
    def test_send_notification_success(self, mock_post, notification_manager, dag_failure):
        """Test successful notification sending."""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        result = notification_manager.send_notification(None, dag_failure)

        assert result is True
        mock_post.assert_called_once()

    @patch('src.notifiers.notification_manager.requests.post')
    def test_send_notification_failure(self, mock_post, notification_manager, dag_failure):
        """Test failed notification sending."""
        mock_post.side_effect = Exception("Network error")

        result = notification_manager.send_notification(None, dag_failure)

        assert result is False
