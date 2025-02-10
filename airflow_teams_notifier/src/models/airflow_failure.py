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
