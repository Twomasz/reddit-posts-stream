import json
import logging
import os

import praw
from kafka import KafkaProducer

import config

logger = logging.getLogger(__name__)

# Reddit API credentials
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_API_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USER_AGENT = "KafkaRedditStream"

# Kafka Configuration
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    # username=REDDIT_USERNAME,
    # password=REDDIT_PASSWORD,
    user_agent=REDDIT_USER_AGENT
)

# Stream comments from a subreddit
subreddit = reddit.subreddit("technology")  # Change to any subreddit
print("Streaming comments from r/technology...")

try:
    for comment in subreddit.stream.comments(skip_existing=True):
        data = {"id": comment.id, "text": comment.body, "author": str(comment.author)}
        print(f"Sending comment: {data['text']}")
        producer.send(KAFKA_TOPIC, data)
except KeyboardInterrupt:
    print("\nStopping stream...")
finally:
    print("Closing Kafka Producer...")
    producer.close()