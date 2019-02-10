#from airflow.contrib.operators import KubernetesOperator
from datetime import datetime, timedelta
from airflow import DAG

from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.secret import Secret

yesterday = datetime.combine(datetime.today() - timedelta(1), datetime.min.time())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date':  yesterday,
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


dag = DAG( 'kubernetes_sample_3', default_args=default_args, schedule_interval=timedelta(minutes=10))

boom = KubernetesPodOperator(namespace='airflow',
                        image="registry.hub.docker.com/debian:latest",
                        image_pull_policy="Always",
                        cmds=["bash", "-cx"],
                        arguments=["echo", "10"],
                        name="test",
                        task_id="startUbuntu",
                        is_delete_operator_pod=True,
                        hostnetwork=False,
                        dag=dag,
                        in_cluster=False
                        )
