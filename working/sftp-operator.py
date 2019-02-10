#from airflow.contrib.operators import KubernetesOperator
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.sensors.sftp_sensor import SFTPSensor

yesterday = datetime.combine(datetime.today() - timedelta(1), datetime.min.time())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': yesterday,
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


dag = DAG( 'sftpSensorTest', default_args=default_args, schedule_interval=timedelta(days=1), dagrun_timeout=timedelta(minutes=5),)

start = DummyOperator(task_id='run_this_first', dag=dag)

sftp = SFTPSensor(
	task_id = 'sftp_check',
	path = 'data/filelist.txt',
	sftp_conn_id = 'sftp_beefy',
        poke_interval = 10,
        mode = 'poke',
        soft_fail = False,
	dag = dag,
	)

nextStep = KubernetesPodOperator(namespace='airflow',
                        image="python:3.6-stretch",
                        image_pull_policy="Always",
                        cmds=["python","-c"],
                        arguments=["print('hello world')"],
                        name="python",
                        task_id="startPython",
                        is_delete_operator_pod=True,
                        hostnetwork=False,
                        dag=dag,
                        in_cluster=False,
                        )

sftp.set_upstream(start)
nextStep.set_upstream(sftp)
