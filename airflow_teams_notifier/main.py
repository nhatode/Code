"""
Main entry point for Airflow Teams Notifier.

This script demonstrates basic usage of the notification system.
For production use, consider using the examples in the examples/ directory
or integrating directly with your Airflow DAGs.
"""
import argparse
import sys
from datetime import datetime
from src.models.servicenow_ticket import ServiceNowTicket
from src.models.airflow_failure import AirflowDagFailure
from src.notifiers.teams_notifier import TeamsNotifier
from src.notifiers.notification_manager import NotificationManager
from src.config import TEAMS_WEBHOOK_URL
from src.logger import logger


def send_test_notification(include_ticket: bool = False):
    """
    Send a test notification to verify configuration.

    Args:
        include_ticket: Whether to include ServiceNow ticket in notification

    Returns:
        bool: True if notification was sent successfully
    """
    try:
        # Initialize components
        logger.info("Initializing Teams notifier...")
        teams_notifier = TeamsNotifier(TEAMS_WEBHOOK_URL)
        notification_manager = NotificationManager(teams_notifier)

        # Create sample ServiceNow ticket if requested
        snow_ticket = None
        if include_ticket:
            logger.info("Creating sample ServiceNow ticket...")
            snow_ticket = ServiceNowTicket(
                ticket_number="INC0012345",
                description="Airflow DAG Failure Investigation (TEST)",
                priority="P2",
                assigned_to="Test User",
                status="In Progress"
            )

        # Create sample DAG failure info
        logger.info("Creating sample DAG failure...")
        dag_failure = AirflowDagFailure(
            dag_id="example_test_dag",
            task_id="test_task",
            execution_date=datetime.now(),
            error_message="This is a test notification - Task failed due to connection timeout"
        )

        # Send notification
        logger.info("Sending notification...")
        success = notification_manager.send_notification(snow_ticket, dag_failure)

        if success:
            logger.info("✅ Test notification sent successfully!")
            return True
        else:
            logger.error("❌ Failed to send test notification")
            return False

    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Airflow Teams Notifier - Send test notifications to Microsoft Teams'
    )
    parser.add_argument(
        '--with-ticket',
        action='store_true',
        help='Include ServiceNow ticket information in the notification'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Send a test notification to verify configuration'
    )

    args = parser.parse_args()

    # If no arguments provided, show help
    if not args.test:
        parser.print_help()
        print("\n" + "="*60)
        print("QUICK START:")
        print("="*60)
        print("1. Copy .env.example to .env: cp ../.env.example ../.env")
        print("2. Edit .env and add your Teams webhook URL")
        print("3. Run test: python main.py --test")
        print("4. For production use, see examples/ directory")
        print("="*60)
        sys.exit(0)

    # Send test notification
    success = send_test_notification(include_ticket=args.with_ticket)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
