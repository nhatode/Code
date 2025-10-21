import requests
from typing import Dict, Optional
from ..models.servicenow_ticket import ServiceNowTicket
from ..models.airflow_failure import AirflowDagFailure
from .teams_notifier import TeamsNotifier
from ..logger import logger

class NotificationManager:
    def __init__(self, teams_notifier: TeamsNotifier):
        self.teams_notifier = teams_notifier

    def create_teams_message(self, snow_ticket: Optional[ServiceNowTicket],
                           dag_failure: AirflowDagFailure) -> Dict:
        """
        Create Teams message format

        Args:
            snow_ticket: ServiceNow ticket information (optional)
            dag_failure: Airflow DAG failure information

        Returns:
            Dict containing the Teams message payload
        """
        # Build the message body
        body = [
            {
                "type": "TextBlock",
                "size": "Large",
                "weight": "Bolder",
                "text": "🚨 Airflow DAG Failure Alert"
            },
            {
                "type": "FactSet",
                "facts": [
                    {"title": "DAG ID:", "value": dag_failure.dag_id},
                    {"title": "Task ID:", "value": dag_failure.task_id},
                    {"title": "Execution Date:",
                     "value": dag_failure.execution_date.strftime("%Y-%m-%d %H:%M:%S")},
                    {"title": "Error:", "value": dag_failure.error_message}
                ]
            }
        ]

        # Add ServiceNow ticket details if provided
        if snow_ticket:
            body.extend([
                {
                    "type": "TextBlock",
                    "size": "Medium",
                    "weight": "Bolder",
                    "text": "ServiceNow Ticket Details"
                },
                {
                    "type": "FactSet",
                    "facts": [
                        {"title": "Ticket Number:", "value": snow_ticket.ticket_number},
                        {"title": "Description:", "value": snow_ticket.description},
                        {"title": "Priority:", "value": snow_ticket.priority},
                        {"title": "Assigned To:", "value": snow_ticket.assigned_to},
                        {"title": "Status:", "value": snow_ticket.status}
                    ]
                }
            ])

        return {
            "type": "message",
            "attachments": [{
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": body,
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.2"
                }
            }]
        }

    def send_notification(self, snow_ticket: Optional[ServiceNowTicket],
                         dag_failure: AirflowDagFailure) -> bool:
        """
        Send Teams notification

        Args:
            snow_ticket: ServiceNow ticket information (optional)
            dag_failure: Airflow DAG failure information

        Returns:
            bool: True if notification was sent successfully
        """
        try:
            logger.info(f"Sending Teams notification for DAG: {dag_failure.dag_id}")
            message = self.create_teams_message(snow_ticket, dag_failure)

            response = requests.post(
                self.teams_notifier.webhook_url,
                json=message,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()

            logger.info(f"Teams notification sent successfully for DAG: {dag_failure.dag_id}")
            return True

        except requests.exceptions.Timeout:
            logger.error(f"Timeout while sending Teams notification for DAG: {dag_failure.dag_id}")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP error sending Teams notification: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Teams notification: {str(e)}", exc_info=True)
            return False
