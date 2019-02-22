#
# NOT WORKING NEED TO ENABLE KUBECTL TO ACCESS ACR
#
#from airflow.contrib.operators import KubernetesOperator
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.secret import Secret

seven_days_ago = datetime.combine(datetime.today() - timedelta(7), datetime.min.time())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date':  seven_days_ago,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}


dag = DAG( 'azureUbuntu', default_args=default_args, schedule_interval=timedelta(days=1))

run_this = BashOperator(
            task_id='run_first',
            bash_command='echo 1',
            dag=dag
            )

boom = KubernetesPodOperator(namespace='airflow',
                        image="monolive.azurecr.io/ubuntu:v1",
                        image_pull_policy="Always",
                        cmds=["bash", "-cx"],
                        arguments=["echo", "10"],
                        name="azure",
                        task_id="azureUbuntu",
                        is_delete_operator_pod=True,
                        hostnetwork=False,
                        dag=dag,
                        in_cluster=False
                        )
boom >> run_this
