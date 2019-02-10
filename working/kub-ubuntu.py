#from airflow.contrib.operators import KubernetesOperator
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
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
    'pool': 'kube',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}


dag = DAG( 'ubuntuBash', default_args=default_args, schedule_interval=timedelta(days=1), dagrun_timeout=timedelta(minutes=5),)

start = DummyOperator(task_id='run_this_first', dag=dag)

boom = KubernetesPodOperator(namespace='airflow',
                        image="ubuntu:latest",
                        image_pull_policy="Always",
                        cmds=["bash","-cx"],
                        arguments=["echo","10"],
                        name="python",
                        task_id="startUbuntu",
                        is_delete_operator_pod=True,
                        hostnetwork=False,
                        dag=dag,
                        in_cluster=False,
                        )

boom.set_upstream(start)
