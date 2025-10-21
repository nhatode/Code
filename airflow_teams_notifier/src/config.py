"""
Configuration settings for Airflow Teams Notifier.
All settings are loaded from environment variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# Look for .env file in the project root (parent of airflow_teams_notifier)
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Required configurations
TEAMS_WEBHOOK_URL = os.getenv('TEAMS_WEBHOOK_URL')

# Optional: ServiceNow Configuration
SERVICENOW_INSTANCE_URL = os.getenv('SERVICENOW_INSTANCE_URL', '')
SERVICENOW_USERNAME = os.getenv('SERVICENOW_USERNAME', '')
SERVICENOW_PASSWORD = os.getenv('SERVICENOW_PASSWORD', '')

# Optional: Airflow Configuration
AIRFLOW_BASE_URL = os.getenv('AIRFLOW_BASE_URL', 'http://localhost:8080')
AIRFLOW_USERNAME = os.getenv('AIRFLOW_USERNAME', '')
AIRFLOW_PASSWORD = os.getenv('AIRFLOW_PASSWORD', '')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'airflow_notifier.log')

# Validation
def validate_config():
    """Validate that required configuration is present."""
    if not TEAMS_WEBHOOK_URL:
        raise ValueError(
            "TEAMS_WEBHOOK_URL environment variable is required. "
            "Please copy .env.example to .env and configure it."
        )

    if not TEAMS_WEBHOOK_URL.startswith('https://'):
        raise ValueError(
            "TEAMS_WEBHOOK_URL must be a valid HTTPS URL"
        )

# Validate on import
validate_config()
