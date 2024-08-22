import json

from confluent_kafka import Producer

producer_config = {
    'bootstrap.servers': 'kafka:9092',
    'client.id': 'kafka-producer'

}
kafka_producer = Producer(producer_config)


def send_event_to_kafka(event_type: str, description: str):
    kafka_producer.produce('events_topic', key=event_type, value=description)
    kafka_producer.flush()


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
