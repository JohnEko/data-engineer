from airflow import DAG

from datetime import datetime
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator



local_workflow = DAG(
    "LocalInjestionDag",
     schedule_interval="0 6 2 * *", 
     start_date=datetime(2023, 1, 1)

)

with  local_workflow:

    wget_test = BashOperator(
        task_id='wget',
        bash_command="echo 'hello-world'"
        
     
       
      )

    injest_task = BashOperator(
        injest_id='wget',
        bash_command ='echo "Injest-hello-world"'
    
     
        )
    
    #Making the table to dimentional table and fact table
    create_table_items = BashOperator(
        task_id = 'creating_table_items',
        bash_command="echo 'New_table_items'",
        dag=dag
    )

    create_table_stockmarket = BigQueryCheckOperator(
        task_id='create_table_stockmarket',
        use_legacy_sql = False,
        location=LOCATION,
        sql='./dags/sql/stockmarket.sql'
    )

    create_fact_table_stockmarket = BigQueryCheckOperator(
        task_id='create_fact_table_stockmarket',
        use_legacy_sql = False,
        location=LOCATION,
        sql='./dags/sql/stockmarket.sql'
    )

    check_stock_fact_dataset = BigQueryCheckOperator(
        task_id='checking_stock_fact_dataset',
        use_legacy_sql=False,
        location=LOCATION,
        sql = f'select count(*) from {PROJECT_ID}.{DATASET}.fact_dataset_stockmarket'

     )
    wget_test >> injest_task

        #[check_dataset_stockmarket]

    create_table_items >> [create_table_stockmarket]

    create_fact_table_stockmarket >> check_stock_fact_dataset >> finish_pipeline