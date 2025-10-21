"""
Example with ServiceNow ticket integration.

This example shows how to send a Teams notification with ServiceNow ticket information.
"""
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.servicenow_ticket import ServiceNowTicket
from src.models.airflow_failure import AirflowDagFailure
from src.notifiers.teams_notifier import TeamsNotifier
from src.notifiers.notification_manager import NotificationManager
from src.config import TEAMS_WEBHOOK_URL


def main():
    """Send a notification with ServiceNow ticket details."""

    # Initialize components
    teams_notifier = TeamsNotifier(TEAMS_WEBHOOK_URL)
    notification_manager = NotificationManager(teams_notifier)

    # Create ServiceNow ticket information
    snow_ticket = ServiceNowTicket(
        ticket_number="INC0012345",
        description="Airflow DAG Failure - ETL Pipeline Investigation",
        priority="P2",
        assigned_to="Data Engineering Team",
        status="In Progress"
    )

    # Create DAG failure information
    dag_failure = AirflowDagFailure(
        dag_id="production_etl_pipeline",
        task_id="transform_customer_data",
        execution_date=datetime.now(),
        error_message="Data quality check failed: NULL values found in required fields"
    )

    # Send notification with ServiceNow ticket
    success = notification_manager.send_notification(
        snow_ticket=snow_ticket,
        dag_failure=dag_failure
    )

    if success:
        print("✅ Notification with ServiceNow ticket sent successfully!")
    else:
        print("❌ Failed to send notification")


if __name__ == "__main__":
    main()
