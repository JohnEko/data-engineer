import os
import argparse

import pyspark 
from pyspark import SparkContext
from pyspark import SQLContext
import pandas as pd
from pyspark.sql import SparkSession

spark = SparkSession.builder \
        .master("local[*]") \
        .appName("data engineering projects") \
        .getOrCreate()

print("we good to go")

def main():

   df =spark.read.csv("de_project/stocks/A.csv", header=True, inferSchema=True)
   df.head(5)

main()