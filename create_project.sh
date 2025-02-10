#!/bin/bash

# create_project.sh
# Create base project directory
PROJECT_NAME="airflow_teams_notifier"
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME

# Create project structure
mkdir -p src/models src/notifiers
touch src/__init__.py src/models/__init__.py src/notifiers/__init__.py

# Create requirements.txt
cat > requirements.txt << 'EOL'
requests>=2.25.1
EOL

# Create src/models/servicenow_ticket.py
cat > src/models/servicenow_ticket.py << 'EOL'
class ServiceNowTicket:
    def __init__(self, ticket_number: str, description: str, priority: str, 
                 assigned_to: str, status: str):
        """
        Initialize ServiceNow ticket information
        """
        self.ticket_number = ticket_number
        self.description = description
        self.priority = priority
        self.assigned_to = assigned_to
        self.status = status
EOL

# Create src/models/airflow_failure.py
cat > src/models/airflow_failure.py << 'EOL'
from datetime import datetime

class AirflowDagFailure:
    def __init__(self, dag_id: str, task_id: str, execution_date: datetime, 
                 error_message: str):
        """
        Initialize Airflow DAG failure information
        """
        self.dag_id = dag_id
        self.task_id = task_id
        self.execution_date = execution_date
        self.error_message = error_message
EOL

# Create src/notifiers/teams_notifier.py
cat > src/notifiers/teams_notifier.py << 'EOL'
class TeamsNotifier:
    def __init__(self, webhook_url: str):
        """
        Initialize Teams notifier
        Args:
            webhook_url (str): Microsoft Teams webhook URL
        """
        self.webhook_url = webhook_url
EOL

# Create src/notifiers/notification_manager.py
cat > src/notifiers/notification_manager.py << 'EOL'
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
EOL

# Create src/config.py
cat > src/config.py << 'EOL'
# Configuration settings
TEAMS_WEBHOOK_URL = "your_teams_webhook_url"
EOL

# Create main.py
cat > main.py << 'EOL'
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
EOL

# Make the project a Python package
touch src/__init__.py

echo "Project $PROJECT_NAME has been created successfully!"