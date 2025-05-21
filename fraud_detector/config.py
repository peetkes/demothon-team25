import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

SOLACE_CONFIG = {
    "host": os.getenv("SOLACE_BROKER_SMF_URL"),
    "vpn": os.getenv("SOLACE_BROKER_VPN"),
    "username": os.getenv("SOLACE_BROKER_USERNAME"),
    "password": os.getenv("SOLACE_BROKER_PASSWORD"),
}

TRUSTSTORE_FILEPATH = os.getenv("TRUSTSTORE_FILEPATH")
INPUT_QUEUE_NAME = os.getenv("INPUT_QUEUE_NAME", "checkQueue")
OUTPUT_TOPIC_NAME = os.getenv("OUTPUT_TOPIC_NAME")
NOTIFICATION_TOPIC_NAME = os.getenv("NOTIFICATION_TOPIC_NAME")