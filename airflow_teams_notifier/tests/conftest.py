"""
Pytest configuration and fixtures.
"""
import os
import sys
from pathlib import Path

# Add src directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set test environment variables
os.environ['TEAMS_WEBHOOK_URL'] = 'https://test.webhook.office.com/test'
os.environ['LOG_LEVEL'] = 'DEBUG'
