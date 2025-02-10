import requests
from typing import Dict
from ..models.servicenow_ticket import ServiceNowTicket
from ..models.airflow_failure import AirflowDagFailure
from .teams_notifier import TeamsNotifier

class NotificationManager:
    def __init__(self, teams_notifier: TeamsNotifier):
        self.teams_notifier = teams_notifier

    def create_teams_message(self, snow_ticket: ServiceNowTicket, 
                           dag_failure: AirflowDagFailure) -> Dict:
        """
        Create Teams message format
        """
        return {
            "type": "message",
            "attachments": [{
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": [
                        {
                            "type": "TextBlock",
                            "size": "Large",
                            "weight": "Bolder",
                            "text": f"🚨 Airflow DAG Failure Alert"
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
                        },
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
                    ],
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.2"
                }
            }]
        }

    def send_notification(self, snow_ticket: ServiceNowTicket, 
                         dag_failure: AirflowDagFailure) -> bool:
        """
        Send Teams notification
        Returns:
            bool: True if notification was sent successfully
        """
        try:
            message = self.create_teams_message(snow_ticket, dag_failure)
            response = requests.post(
                self.teams_notifier.webhook_url,
                json=message,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error sending Teams notification: {str(e)}")
            return False
