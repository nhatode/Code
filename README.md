# Airflow Teams Notifier

A Python-based notification system that automatically sends Microsoft Teams alerts for Airflow DAG failures with optional ServiceNow ticket information. This project provides a modular, configurable, and production-ready solution for integrating Airflow monitoring with Teams notifications.

## Features

- 🚀 Automated Teams notifications for Airflow DAG failures
- 🎯 Optional integration with ServiceNow ticket information
- 🔧 Modular and object-oriented design
- 🛡️ Robust error handling and logging
- ⚙️ Environment-based configuration (no hardcoded secrets!)
- 🔄 Easy to extend and customize
- 📦 Ready for production use
- ✅ Includes tests and examples

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/navalhatode/airflow_teams_notifier.git
cd airflow_teams_notifier
```

### 2. Set Up Environment

```bash
# Create virtual environment
cd airflow_teams_notifier
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp ../.env.example ../.env

# Edit .env and add your Teams webhook URL
# You can use any text editor:
nano ../.env
# or
vim ../.env
```

**Get your Teams Webhook URL:**
1. Go to your Teams channel
2. Click "..." next to the channel name
3. Select "Connectors"
4. Search for "Incoming Webhook" and click "Add"
5. Configure the webhook and copy the URL
6. Paste it in your `.env` file:
   ```
   TEAMS_WEBHOOK_URL=https://your-org.webhook.office.com/webhookb2/your-webhook-id
   ```

### 4. Test the Configuration

```bash
# Run a test notification
python main.py --test

# Run a test with ServiceNow ticket included
python main.py --test --with-ticket
```

## Project Structure

```
airflow_teams_notifier/
│
├── src/
│   ├── __init__.py
│   ├── config.py              # Environment-based configuration
│   ├── logger.py              # Logging setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── servicenow_ticket.py
│   │   └── airflow_failure.py
│   └── notifiers/
│       ├── __init__.py
│       ├── teams_notifier.py
│       └── notification_manager.py
│
├── examples/                   # Usage examples
│   ├── basic_usage.py
│   ├── with_servicenow.py
│   └── airflow_callback.py
│
├── tests/                      # Unit tests
│   ├── conftest.py
│   ├── test_models.py
│   └── test_notification.py
│
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── setup.py                    # Package setup
├── main.py                     # Main entry point
└── README.md
```

## Usage Examples

### Basic Usage (Without ServiceNow)

```python
from datetime import datetime
from src.models.airflow_failure import AirflowDagFailure
from src.notifiers.teams_notifier import TeamsNotifier
from src.notifiers.notification_manager import NotificationManager
from src.config import TEAMS_WEBHOOK_URL

# Initialize
teams_notifier = TeamsNotifier(TEAMS_WEBHOOK_URL)
notification_manager = NotificationManager(teams_notifier)

# Create DAG failure info
dag_failure = AirflowDagFailure(
    dag_id="my_etl_pipeline",
    task_id="extract_data",
    execution_date=datetime.now(),
    error_message="Connection timeout"
)

# Send notification
notification_manager.send_notification(None, dag_failure)
```

### With ServiceNow Ticket

```python
from src.models.servicenow_ticket import ServiceNowTicket

# Create ticket info
snow_ticket = ServiceNowTicket(
    ticket_number="INC0012345",
    description="Airflow DAG Failure Investigation",
    priority="P2",
    assigned_to="Data Team",
    status="In Progress"
)

# Send with ticket
notification_manager.send_notification(snow_ticket, dag_failure)
```

### As Airflow Callback Function

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Import the callback function
import sys
sys.path.insert(0, '/path/to/airflow_teams_notifier')
from examples.airflow_callback import send_teams_failure_notification

default_args = {
    'owner': 'data_team',
    'on_failure_callback': send_teams_failure_notification,
}

dag = DAG(
    'my_dag',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)
```

See the `examples/` directory for more usage examples.

## Configuration

All configuration is done through environment variables in the `.env` file:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TEAMS_WEBHOOK_URL` | Yes | - | Microsoft Teams webhook URL |
| `LOG_LEVEL` | No | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `LOG_FILE` | No | airflow_notifier.log | Log file path |
| `SERVICENOW_INSTANCE_URL` | No | - | ServiceNow instance URL (for future integration) |
| `AIRFLOW_BASE_URL` | No | http://localhost:8080 | Airflow base URL (for future integration) |

## Development

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_notification.py
```

### Code Quality

```bash
# Format code with black
black .

# Lint with flake8
flake8 src/

# Type checking with mypy
mypy src/
```

## Installation as Package

```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

## Troubleshooting

### "TEAMS_WEBHOOK_URL environment variable is required"

**Solution:** Make sure you've created a `.env` file in the project root (parent of `airflow_teams_notifier/`) and added your webhook URL.

### "Connection timeout" or "Failed to send notification"

**Solutions:**
1. Check your internet connection
2. Verify the webhook URL is correct
3. Ensure your Teams channel still has the webhook configured
4. Check firewall/proxy settings

### Import errors

**Solution:** Make sure you're running commands from the `airflow_teams_notifier/` directory and have activated your virtual environment.

## Requirements

- Python 3.7+
- requests>=2.25.1
- python-dotenv>=0.19.0
- Microsoft Teams access
- ServiceNow instance (optional)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is not yet licensed but we're working on making it open source.

## Acknowledgments

- Microsoft Teams API Documentation
- Apache Airflow Documentation
- ServiceNow API Documentation

## Contact

1. Naval Hatode - [@navalhatode](https://twitter.com/navalhatode) - navalhatode@gmail.com
2. Akshay Prabhu - [@akshayprabhu](https://www.linkedin.com/in/akshay-prabhu-0a757484/)

Project Link: [https://github.com/navalhatode/airflow_teams_notifier](https://github.com/navalhatode/airflow_teams_notifier)
