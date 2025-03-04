import logging
import os
import sys

from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

load_dotenv()

assert os.getenv("REDDIT_CLIENT_ID") is not None, "Didn't read '.env' file correctly!"
