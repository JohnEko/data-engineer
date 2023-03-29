import os
from datetime import timedelta, datetime
from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator 



GOOGLE_CONN_ID = "google_cloud_default"
PROJECT_ID ="de-projects-373304"
BUCKET_NAME = "de-pipelines"
GS_PATH = "gasprice/"
STAGING_DATASET = "gasprice_dataset"
DATASET = "gasprices_data"
LOCATION = "europe-west1"
BQ_DATASET = "gasprices_production"



default_args = {
    'owner': 'Zino',
    'start_date' : days_ago(2),
    'retries' : 2,
    'retries_delay': timedelta(minutes=3)
}

with DAG(
    dag_id="GasPriceDag",
    default_args=default_args,
    schedule_interval=timedelta(days=1), 
       
) as dag:
    
    start_pipeline = BashOperator(
        task_id="staging_dataset",
        bash_command="echo 'starting pipeline on staging operator'",
        dag=dag
    )

    load_dataset = BashOperator(
        task_id="load_dataset",
        bash_command="echo 'loading dataset to staging operator'",
        dag=dag
    )
    
    #Moving dataset from GCS TO BIGQUERY

    load_dataset_gasprice = GCSToBigQueryOperator(
        task_id = "load_dataset_gasprice",
        bucket = BUCKET_NAME,
        source_objects = ['gasprice/weekly-gasoline.csv'],
        destination_project_dataset_table = f'{PROJECT_ID}:{STAGING_DATASET}.weekly-gasoline',
        write_disposition = 'WRITE_TRUNCATE',
        source_format = 'csv',
        field_delimiter =',',
        skip_leading_rows = 1,
        autodetect=True
       
        
    )
     #CHECKING THE DATASET NUMBERS OF ROLES IN THE TABLE ON GOOGLE BIGQUERY
    check_dataset_gasprice = BigQueryCheckOperator(
        task_id='checking_gasprice_dataset',
        use_legacy_sql=False,
        location=LOCATION,
        sql =  f'SELECT count(*) FROM `{PROJECT_ID}.{STAGING_DATASET}.weekly-gasoline`'

    )
    create_table_items = BashOperator(
        task_id = 'creating_table_items',
        bash_command="echo 'New_table_items'",
        dag=dag
    )
    check_gasprice_from_year = BigQueryOperator(
        task_id = "check_gasprice_from_year",
        sql = '''
        SELECT
            Current_Year_Production,
            Previous_Year_Production,
            Fiscal_Year,
            Fiscal_Week,
        FROM 
            `de-projects-373304.gasprice_dataset.weekly-gasoline` 
            WHERE Current_Year_Production < Previous_Year_Production
        
        ''',
        destination_dataset_table=f'{PROJECT_ID}.{BQ_DATASET}.weekly-gasoline',
        write_disposition = 'WRITE_TRUNCATE',
        allow_large_results=True,
        use_legacy_sql=False,
        dag=dag
    )

    check_percentage_growth = BigQueryOperator(
        task_id = "check_percentage_growth",
        sql = '''
            SELECT 
               Fiscal_Year,
               Fiscal_Week,
               Current_Year_Production,
               Previous_Year_Production,
               (Current_Year_Production - LAG (Previous_Year_Production) OVER (ORDER BY Fiscal_Week ASC))/LAG (Previous_Year_Production) OVER (ORDER BY Fiscal_Week ASC)*100 AS Production_growth,
               (Current_Year_Production - LAG (Previous_Year_Production) OVER (ORDER BY Fiscal_Year ASC))/LAG (Previous_Year_Production) OVER (ORDER BY Fiscal_Week ASC)*100 AS  Percentage_growth,
               LEAD (Previous_Year_Production, 12) OVER (ORDER BY Fiscal_Week ASC) AS next_year_Production
            FROM 
                `de-projects-373304.gasprice_dataset.weekly-gasoline`
                where Current_Year_Production > Previous_Year_Production
                order by Fiscal_Week

        ''',
        destination_dataset_table=f'{PROJECT_ID}.gasoline_percentage.weekly-gasoline',
        write_disposition = 'WRITE_TRUNCATE',
        allow_large_results=True,
        use_legacy_sql=False,
        dag=dag


    )

    create_table_gasprice =  BigQueryOperator(
        task_id='create_table_gasprice',
        use_legacy_sql = False,
        location=LOCATION,
        sql='./sql/weekly-gasoline.sql'
    )

    create_fact_table_gasprice =  BigQueryOperator(
        task_id='create_fact_table_gasprice',
        use_legacy_sql = False,
        location=LOCATION,
        sql='./sql/weekly-gasoline.sql'
    )

    check_gasprice_fact_dataset =  BigQueryOperator(
        task_id='checking_gasprice_fact_dataset',
        use_legacy_sql=False,
        location=LOCATION,
        sql = f'SELECT count(*) FROM `{PROJECT_ID}.{DATASET}.weekly-gasoline`'

     )

    finish_pipeline = BashOperator(
        task_id = "Final_pipeline",
        bash_command = "echo 'pipleline has finish loading'",
        dag=dag
    )

    

    start_pipeline >> load_dataset

    load_dataset >> [load_dataset_gasprice]

    load_dataset_gasprice >> check_dataset_gasprice 

    create_table_items >> check_gasprice_from_year >> check_percentage_growth >>  create_table_gasprice 

    create_fact_table_gasprice >> check_gasprice_fact_dataset >> finish_pipeline




      

   





