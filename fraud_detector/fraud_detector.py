import time

from solace.messaging.messaging_service import MessagingService, RetryStrategy
from solace.messaging.config.solace_properties import transport_layer_properties, service_properties, authentication_properties
from solace.messaging.publisher.persistent_message_publisher import PersistentMessagePublisher
from solace.messaging.receiver.inbound_message import InboundMessage
from solace.messaging.receiver.persistent_message_receiver import PersistentMessageReceiver
from solace.messaging.config.transport_security_strategy import TLS
from solace.messaging.resources.topic import Topic
from solace.messaging.resources.queue import Queue
from config import SOLACE_CONFIG, INPUT_QUEUE_NAME, OUTPUT_TOPIC_NAME, NOTIFICATION_TOPIC_NAME, TRUSTSTORE_FILEPATH
from collections import defaultdict
from solace.messaging.receiver.message_receiver import MessageHandler
import json
import numpy as np
from sklearn.ensemble import IsolationForest

class FraudDetectorHandler(MessageHandler):
    """this method is an call back handler to receive message"""

    def __init__(self, receiver: PersistentMessageReceiver=None, ack=True, publisher: PersistentMessagePublisher=None, source_topic='', test_callback=None):
        super().__init__()
        self._receiver = receiver
        self._publisher = publisher
        self._ack = ack
        self._source_topic = source_topic
        self._receive_count = 0
        self._exception = ''
        self._assertion_error = []
        self._test_callback = test_callback
        self._message_received_on_topics = defaultdict(int)
        self._model = IsolationForest(contamination=0.1)
        self._model.fit(np.array([[1000, 1], [1200, 1], [950, 2], [1300, 3], [2000, 4], [5000, 5], [3500,6], [7000, 7]]))
        self.topic_checked = Topic.of(OUTPUT_TOPIC_NAME)
        self.topic_fraud_detected = Topic.of(NOTIFICATION_TOPIC_NAME)

    @property
    def total_message_received_count(self):
        return self._receive_count

    @property
    def callback_exception(self):
        return self._exception

    @property
    def message_received_on_topics(self):
        return self._message_received_on_topics

    @property
    def assertion_error(self):
        return self._assertion_error

    def on_msg_receive(self, message: 'InboundMessage'):
        """ Extensible function for processing message received """
        # increment simple counter, extended implementation can override
        # and use more complex counters using message fields
        self._receive_count += 1

    def reset(self):
        self._receive_count = 0
        self._exception = ''
        self._assertion_error = []

    def on_message(self, message: 'InboundMessage'):
        """
        MessageHandler on_message function
        provides skeleton message handler execution
        can be overridden if needed
        """
        try:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>INCOMING MESSAGE<<<<<<<<<<<<<<<<<<<')
            payload = message.get_payload_as_string() if message.get_payload_as_string() is not None else message.get_payload_as_bytes()
            payload_as_bytearray = True if isinstance(payload, bytearray) else False
            if payload_as_bytearray:
                print(f"Received a message of type: {type(payload)}. Decoding to string")
                payload = payload.decode("utf-8")
            data = json.loads(payload)
            transaction_id = data["transactionNum"]
            transaction_data = np.array([[data["amount"], data["accountNum"]]])
            # Predict Fraud
            prediction = self._model.predict(transaction_data)
            fraud_detected = True if prediction == -1 else False
            data["checked"] = True
            data["fraudulous"] = fraud_detected
            print(f'Payload = {payload}')
            message_from_topic = message.get_destination_name()
            self._message_received_on_topics[message_from_topic] += 1
            self.on_msg_receive(message)
            if self._receiver and self._ack:
                self._receiver.ack(message)

            if self._source_topic != '' and self._source_topic != message_from_topic:
                self._assertion_error.append(f'Message sent in [{self._source_topic}, '
                                             f'but received from different topic [{message_from_topic}]]')
            if self._test_callback:
                self._test_callback(self, message)
            if self._publisher:
                print(f"Publishing transaction {transaction_id}  to Mongo")
                pub_message = bytearray(json.dumps(data).encode("utf-8")) if payload_as_bytearray else json.dumps(data).encode("utf-8")
                self._publisher.publish(pub_message, self.topic_checked)
                if fraud_detected:
                    print(f"Suspicious transaction {transaction_id}")
                    self._publisher.publish(pub_message, self.topic_fraud_detected)
        except Exception as unexpected_error:
            print(f"EXCEPTION {transaction_id} ERROR: {str(unexpected_error)}")
            self._exception += str(unexpected_error)

print(f"Running the fraud detector with broker-config {SOLACE_CONFIG}")
# Create the messaging service
transport_security_strategy = TLS.create().with_certificate_validation(True, False, trust_store_file_path=f"{TRUSTSTORE_FILEPATH}")

service = (MessagingService.builder().from_properties({
    transport_layer_properties.HOST: SOLACE_CONFIG["host"],
    service_properties.VPN_NAME: SOLACE_CONFIG["vpn"],
    authentication_properties.SCHEME_BASIC_USER_NAME: SOLACE_CONFIG["username"],
    authentication_properties.SCHEME_BASIC_PASSWORD: SOLACE_CONFIG["password"]
    })
    .with_reconnection_retry_strategy(RetryStrategy.parametrized_retry(20,3))
    .with_transport_security_strategy(transport_security_strategy)
    .build()
)

service.connect()
print("Connected to Solace.")

# Create a persistent message publisher
publisher = service.create_persistent_message_publisher_builder().build()
publisher.start()

# Define queue receiver
queue = Queue.durable_exclusive_queue(INPUT_QUEUE_NAME)
receiver = service.create_persistent_message_receiver_builder().with_message_auto_acknowledgement().build(queue)
receiver.start()

print(f"Listening on queue '{INPUT_QUEUE_NAME}'...")

# Bind callback
message_receiver = FraudDetectorHandler(publisher=publisher)
receiver.receive_async(message_receiver)

# Keep running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    receiver.terminate()
    publisher.terminate()
    service.disconnect()