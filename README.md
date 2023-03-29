# Course Project - Gasoline Production
### Overview
This project was done to analyze the increase in Gas Production, The data source was collected from Kaggle dataset. The aim of this project was to see the effect of production of gasoline during the war till now, Things which i learned from  DataTalks.Club are applied on this project but i used google composer rader than VM, this course has helped me to  build an end-to-end data pipeline using Apache airflow.
Project description
The project is connected to gasoline production. What is the cause of high gas prices and why has it caused inflation in the world? It describes the weekly increase and decrease of production during the war in Ukraine and after the sanction The giving data will help you see the percentage increase and decrease of production which has caused price increase in consumers and the answers to these dataset and more.
The main focus of the project are:
Create a data pipeline that can help individual and companies processing data on  batch processing on a weekly and yearly basis;
Build a dashboard that will be easy to determine the trends and digest the insights on the decrease and increase in production.


# Dataset
The dataset used on this project can be found in kaggle.
The dataset consist of 7 different  columns:
Fiscal_Year
Fiscal_Week
Current_Year_Production
Previous_Year_Production
Difference_From_Same_Week_Last_Year
Current_Year_Cumulative_Production
Cumulative_Difference


# Technologies Used
Cloud: GCP
Data Lake (DL): GCS
Data Warehouse (DWH): BigQuery
Workflow orchestration: Airflow
Data Visualization: Google Data Studio
Project Workflow:
End-to-End data pipeline:
downloading, processing and uploading of the initial dataset to a DL;
Transferring the data from the lake to a data warehouse
Data transformation from data Warehouse and cleansing it ready for google dashboard studio;
Creating a dashboard.
You can find the detailed information on the diagram below: 

# Projects
This project contains instructions which you can follow to get the results.
1. Pre-requisites
Make sure you have the following pre-installed components:
GCP account
Apache Airflow
2. Google Cloud Platform
To set up GCP, please follow the steps below:
If you don't have a GCP account, please create a free trial.
Setup new project and write down your Project ID.
Configure service account to get access to this project and download auth-keys (.json). Please check the service account has all the permissions below:
Viewer
Storage Admin
Storage Object Admin
BigQuery Admin
Download SDK for local setup.
Set environment variable to point to your downloaded auth-keys:


# Airflow
The next steps provide you with the instructions of running Apache Airflow, which will allow you to run the entire orchestration, taking into account that you have already set up a GCP account on Cloud Composer


Setup
Go to composer create an Environment on composer: here you can find the Airflow dag on google composer, make sure that your region is same thing with your bucket region and things you need to specify before runing your dag are your Project ID (GCP_PROJECT_ID) and Cloud Storage name (GCP_GCS_BUCKET) in the  on ypur python file.
After creating the composer and connecting uploading your python file to your bucket, you can test you dags

Running DAGs
Click the AIRFLOW UI on your composer and it will take you to airflow webservice, then run your Dags


# Google Data Studio
After your data has been run successfully and your transformation are in Big Query then start building your dashboard for visualization.
This dashboard is build with Data Studio. The aim of dashboard is to give understanding insight of the data and how production has been so anyone can understand the data
And the final dashboard includes the following diagrams:
Fiscal_Year
Fiscal_Week
Current_Year_Production
Previouse_Year_Production
Percentage_growth
Record_count


# Pandas and Spark library
Using Pyspark  and Pandas  to structure the data, This data was taking from kaggle, preprocess the data and using the data to predict features on gas production, with the exploratory analysis





