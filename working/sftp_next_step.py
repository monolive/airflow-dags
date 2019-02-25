#from airflow.contrib.operators import KubernetesOperator
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.sensors.sftp_sensor import SFTPSensor
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.secret import Secret

# Under admin section in UI, create variable called ssh_key_beefy with value of ssh_key
secret_env  = Secret('env', 'ssh_key', 'airflow-secrets', ssh_key_beefy)

volume_mount = VolumeMount('test-volume',
                            mount_path='/root/mount_file',
                            sub_path=None,
                            read_only=True)

volume_config= {
    'persistentVolumeClaim':
      {
        'claimName': 'test-volume'
      }
    }
volume = Volume(name='test-volume', configs=volume_config)


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

nextStep = KubernetesPodOperator(
    namespace='airflow',
    image="chartedcode/alpine-sftp-client:latest",
    image_pull_policy="Always",
    secrets=[secret_env],
    arguments=
    name="sftp-client",
    task_id="sftpClient",
    is_delete_operator_pod=True,
    hostnetwork=False,
    dag=dag,
    in_cluster=False,
    )

sftp.set_upstream(start)
nextStep.set_upstream(sftp)
S
