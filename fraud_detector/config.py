import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

SOLACE_CONFIG = {
    "host": os.getenv("SOLACE_BROKER_SMF_URL","tcp://localhost:55554"),
    "vpn": os.getenv("SOLACE_BROKER_VPN", "default"),
    "username": os.getenv("SOLACE_BROKER_USERNAME", "default"),
    "password": os.getenv("SOLACE_BROKER_PASSWORD", "default"),
}

INPUT_QUEUE_NAME = os.getenv("INPUT_QUEUE_NAME", "financeQueue")
OUTPUT_TOPIC_NAME = os.getenv("OUTPUT_TOPIC_NAME", "transaction/checked")