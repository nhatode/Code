"""
Example of using the notifier as an Airflow callback function.

This example shows how to integrate the notifier with Airflow DAGs
to automatically send Teams notifications on failure.
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


def send_teams_failure_notification(context):
    """
    Airflow callback function to send Teams notification on task failure.

    This function can be used as on_failure_callback in your Airflow DAGs.

    Args:
        context: Airflow context dictionary containing task instance info

    Example usage in DAG:
        ```python
        from airflow import DAG
        from examples.airflow_callback import send_teams_failure_notification

        default_args = {
            'on_failure_callback': send_teams_failure_notification,
        }

        dag = DAG(
            'my_dag',
            default_args=default_args,
            ...
        )
        ```
    """
    # Extract information from Airflow context
    task_instance = context.get('task_instance')
    exception = context.get('exception')

    # Create DAG failure object
    dag_failure = AirflowDagFailure(
        dag_id=task_instance.dag_id,
        task_id=task_instance.task_id,
        execution_date=task_instance.execution_date,
        error_message=str(exception) if exception else "Task failed"
    )

    # Initialize notifier
    teams_notifier = TeamsNotifier(TEAMS_WEBHOOK_URL)
    notification_manager = NotificationManager(teams_notifier)

    # Send notification
    notification_manager.send_notification(
        snow_ticket=None,
        dag_failure=dag_failure
    )


# Example DAG definition (commented out - this is just for reference)
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': send_teams_failure_notification,
}

dag = DAG(
    'example_dag_with_teams_notification',
    default_args=default_args,
    description='Example DAG with Teams notifications',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

def my_failing_task():
    raise Exception("This task failed!")

task = PythonOperator(
    task_id='failing_task',
    python_callable=my_failing_task,
    dag=dag,
)
"""
