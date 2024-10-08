# creating a python virtual environment
python3 -m venv airflow_env

# activate python virtual environment 
source /Users/user/airflow/airflow_env/bin/activate

# download a apache-airflow using pip
pip install apache-airflow

# starting airflow webserver in first terminal 
export AIRFLOW_HOME=$(pwd)/airflow
airflow db init
airflow webserver -p 8080

# starting airflow scheduler in second terminal
export AIRFLOW_HOME=$(pwd)/airflow
airflow scheduler

# management of active ports
lsof -i :8080
kill -9 <PID>

