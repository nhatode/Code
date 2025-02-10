from datetime import datetime
from src.models.servicenow_ticket import ServiceNowTicket
from src.models.airflow_failure import AirflowDagFailure
from src.notifiers.teams_notifier import TeamsNotifier
from src.notifiers.notification_manager import NotificationManager
from src.config import TEAMS_WEBHOOK_URL

def main():
    # Initialize components
    teams_notifier = TeamsNotifier(TEAMS_WEBHOOK_URL)
    notification_manager = NotificationManager(teams_notifier)
    
    # Create sample ticket and failure info
    snow_ticket = ServiceNowTicket(
        ticket_number="INC0012345",
        description="Airflow DAG Failure Investigation",
        priority="P2",
        assigned_to="John Doe",
        status="In Progress"
    )
    
    dag_failure = AirflowDagFailure(
        dag_id="example_dag",
        task_id="failed_task",
        execution_date=datetime.now(),
        error_message="Task failed due to connection timeout"
    )
    
    # Send notification
    success = notification_manager.send_notification(snow_ticket, dag_failure)
    print(f"Notification sent successfully: {success}")

if __name__ == "__main__":
    main()
