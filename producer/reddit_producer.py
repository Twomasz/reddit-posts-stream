import json
import logging
import os
import sys
import time

import praw
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from retry import retry


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)8s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# init Reddit API
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_API_SECRET")
REDDIT_USER_AGENT = "KafkaRedditStream"

# Kafka config
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")


def setup() -> None:
    """
    Create Kafka topic if it doesn't exist.
    """
    time.sleep(10)
    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_BROKER,
        client_id='kafka_topic_initializer'
    )
    if KAFKA_TOPIC in admin_client.list_topics():
        logger.info(f"Topic '{KAFKA_TOPIC}' already exists.")
        return

    topic = NewTopic(
        name=KAFKA_TOPIC,
        num_partitions=1,
        replication_factor=1
    )
    admin_client.create_topics(new_topics=[topic], validate_only=False)
    logger.info(f"Topic '{KAFKA_TOPIC}' created successfully.")
    return


@retry(delay=60, logger=logger)
def main(subreddit_topic: str = 'technology') -> None:
    """
    Stream in loop comments from Reddit and send them to Kafka
    """
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda x: json.dumps(x).encode("utf-8")
    )

    subreddit = reddit.subreddit(subreddit_topic)
    logger.info(f"Streaming comments from {subreddit_topic}...")

    for comment in subreddit.stream.comments(skip_existing=True):
        data = {
            "comment_id": comment.id,
            "message": comment.body,
            "username": str(comment.author)
        }
        logger.info(f"Sending comment: {data['message']}")
        producer.send(KAFKA_TOPIC, data)


if __name__ == "__main__":
    setup()
    main()