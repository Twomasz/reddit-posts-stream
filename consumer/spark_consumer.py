import os
import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType

import config

logger = logging.getLogger(__name__)



# Initialize Spark Session
spark = SparkSession.builder \
    .appName("TwitterKafkaConsumer") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/spark-checkpoints") \
    .getOrCreate()

# Kafka Parameters
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

# Define Schema for Tweets
schema = StructType([
    StructField("id", StringType(), True),
    StructField("text", StringType(), True),
    StructField("author", StringType(), True)
])

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "latest") \
    .load()

# Deserialize JSON messages
tweets_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Process Tweets (Example: Count words)
word_count_df = tweets_df.selectExpr("explode(split(text, ' ')) as word") \
    .groupBy("word") \
    .count() \
    .orderBy(col("count").desc())

# Write to Console
query = word_count_df.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()