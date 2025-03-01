import logging
import os

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()

assert os.getenv("PROJECT_ABS_PATH") in os.getcwd(), "Didn't read '.env' file correctly!"
