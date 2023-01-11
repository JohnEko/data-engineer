import os
import argparse
import pyspark
from pyspark import SparkContext
from pyspark.sql import SQLContext
import pandas as pd

from pyspark.sql import SparkSession

spark = SparkSession.builder \
        .master("local[*]") \
        .appName("de_projects") \
        .getOrCreate()

print("Time to start projects")


df = pd.read_csv("stock/stock-market-dataset.csv")
print(df.head(5))