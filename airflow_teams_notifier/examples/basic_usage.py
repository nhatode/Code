"""
Basic usage example for Airflow Teams Notifier.

This example shows how to send a simple Teams notification for an Airflow DAG failure.
"""
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.airflow_failure import AirflowDagFailure
from src.notifiers.teams_notifier import TeamsNotifier
from src.notifiers.notification_manager import NotificationManager
from src.config import TEAMS_WEBHOOK_URL


def main():
    """Send a basic notification for an Airflow DAG failure."""

    # Initialize the Teams notifier
    teams_notifier = TeamsNotifier(TEAMS_WEBHOOK_URL)
    notification_manager = NotificationManager(teams_notifier)

    # Create DAG failure information
    dag_failure = AirflowDagFailure(
        dag_id="example_etl_pipeline",
        task_id="extract_data",
        execution_date=datetime.now(),
        error_message="Connection timeout while connecting to database"
    )

    # Send notification without ServiceNow ticket
    success = notification_manager.send_notification(
        snow_ticket=None,
        dag_failure=dag_failure
    )

    if success:
        print("✅ Notification sent successfully!")
    else:
        print("❌ Failed to send notification")


if __name__ == "__main__":
    main()
