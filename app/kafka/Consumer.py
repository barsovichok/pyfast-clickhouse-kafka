import json
import logging
import threading
from datetime import datetime
import re

from confluent_kafka import Consumer
from app.database.clickhouse.clickhouse_engine import clickhouse_client

consumer = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['events_topic'])

stop_event = threading.Event()


def consume_messages():
    try:
        consumer.consume()
        while not stop_event.is_set():
            msg = consumer.poll()
            if msg is None:
                test_event = {"first_name": "string",
                              "avatar": "https://example.com/",
                              "id": 1,
                              "last_name": "string",
                              "email": "user@example.com"}
                logging.info(f"Received test_event: {test_event}")
                event_type = "test"
                description = str(test_event)
                query = "INSERT INTO default.events (event_type, description, timestamp) VALUES"
                data = [(event_type, description, datetime.now())]
                clickhouse_client.execute(query, data)
                logging.info(f"Stored event: {test_event}")
            if msg.error():
                logging.error(f"Consumer error: {msg.error()}")
                continue

            if msg is not None:
                logging.info(f"Received raw message: {msg.value()}")
                event = msg.value().decode('utf-8')
                event_type = msg.key().decode('utf-8') if msg.key() else 'unknown'
                logging.info(f"Received event: {event}")
                description = re.sub(r"'", r'"', event)
                logging.info(f"Description: {description}")
                try:
                    query = "INSERT INTO default.events (event_type, description, timestamp) VALUES"
                    data = [(event_type, description, datetime.now())]
                    clickhouse_client.execute(query, data)
                    logging.info(f"Stored event: {event}")
                except Exception as e:
                    logging.error(f"Failed to process message: {e}")
            else:
                logging.warning("Received empty message")
    finally:
        consumer.close()


def start_consumer():
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.daemon = True
    consumer_thread.start()
    return consumer_thread


def stop_consumer():
    stop_event.set()

