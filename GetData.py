import praw
import json
from datetime import datetime
import multiprocessing
import nasdaqdatalink
from pyspark.sql import SparkSession

nasdaqdatalink.ApiConfig.api_key = "LkenftFvK-KxnhWae16J"
current_date = datetime.now().strftime("%Y-%m-%d")

def captureCompData(compnum):
    data = nasdaqdatalink.get_table('MER/F1', compnumber=[str(compnum)], paginate=True)
    df = spark.createDataFrame(data)
    df.write.json("hdfs://localhost:9000/data/" + current_date + "/",mode="overwrite")

if __name__ == "__main__":
    spark = SparkSession.builder.appName("MyApp").getOrCreate()
    captureCompData(39102)
    captureCompData(2438)
    
