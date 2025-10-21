"""
Tests for data models.
"""
import pytest
from datetime import datetime
from src.models.servicenow_ticket import ServiceNowTicket
from src.models.airflow_failure import AirflowDagFailure


class TestServiceNowTicket:
    """Tests for ServiceNowTicket model."""

    def test_create_ticket(self):
        """Test creating a ServiceNow ticket."""
        ticket = ServiceNowTicket(
            ticket_number="INC0012345",
            description="Test incident",
            priority="P1",
            assigned_to="John Doe",
            status="New"
        )

        assert ticket.ticket_number == "INC0012345"
        assert ticket.description == "Test incident"
        assert ticket.priority == "P1"
        assert ticket.assigned_to == "John Doe"
        assert ticket.status == "New"


class TestAirflowDagFailure:
    """Tests for AirflowDagFailure model."""

    def test_create_failure(self):
        """Test creating an Airflow DAG failure."""
        execution_date = datetime(2024, 1, 1, 12, 0, 0)
        failure = AirflowDagFailure(
            dag_id="test_dag",
            task_id="test_task",
            execution_date=execution_date,
            error_message="Test error"
        )

        assert failure.dag_id == "test_dag"
        assert failure.task_id == "test_task"
        assert failure.execution_date == execution_date
        assert failure.error_message == "Test error"
