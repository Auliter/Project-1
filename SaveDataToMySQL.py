import mysql.connector as cnt
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
import warnings
from datetime import datetime
import pandas as pd
import sys

spark = SparkSession.builder \
    .master("local[4]") \
    .appName("Spark Test") \
    .config("spark.driver.memory", "8G") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.kryoserializer.buffer.max", "2000M") \
    .config("spark.driver.maxResultSize", "2G") \
    .getOrCreate()

current_date = datetime.now().strftime("%Y-%m-%d")
directory = "hdfs://localhost:9000/data/alphavantage/"+current_date
df = spark.read.json(directory)
df.show()
data_collect = df.collect()

cnx = cnt.connect(user='testUser',password='123456',host='47.250.52.110',database='NasdaqLinkData')
mycursor = cnx.cursor()
for row in data_collect:
    sql = "INSERT INTO stockPrice (compnumber, reportid, mapcode, amount, reportdate, reporttype, auditorstatus, currency, consolidated, longname, city, statecode, country) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (row["compnumber"],row["reportid"],row["mapcode"],row["amount"],row["reportdate"],row["reporttype"],row["auditorstatus"],row["currency"],row["consolidated"],row["longname"],row["city"],row["statecode"],row["country"])
    try:
        mycursor.execute(sql,val)
        cnx.commit()
    except:
        print("Record already exist")
