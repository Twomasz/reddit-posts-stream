import os
import logging
import sys

import findspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, expr
from pyspark.sql.types import StructType, StringType, IntegerType


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)8s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

findspark.init()

# Kafka config
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

# postgreSQL params
POSTGRES_URL = os.getenv("POSTGRES_URL")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# init Spark Session
spark = SparkSession.builder \
    .appName("RedditKafkaConsumer") \
    .config("spark.jars", "/opt/spark/jars/kafka.jar,/opt/spark/jars/postgres.jar") \
    .config("spark.sql.extensions", "org.apache.spark.sql.kafka010.KafkaSourceProvider") \
    .getOrCreate()

# define schema from Kafka
schema = StructType() \
    .add("comment_id", StringType(), False) \
    .add("message", StringType(), False) \
    .add("username", StringType(), False)

# read data from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

# deserialize JSON from Kafka
df = df.select(from_json(col("value").cast("string"), schema).alias("parsed_value"))

# extract structured data
df = df.select(
    col("parsed_value.comment_id"),
    col("parsed_value.message"),
    col("parsed_value.username")
)

# simple aggregation: count words in message
df = df.withColumn("num_words", col("message").cast("string").substr(0, 10_000).alias("message").getField("length"))


def write_to_postgres(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", POSTGRES_URL) \
        .option("dbtable", "reddit_msgs") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

# write to PostgreSQL
df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .start() \
    .awaitTermination()