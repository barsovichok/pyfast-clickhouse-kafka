from http import HTTPStatus

import prometheus_client
from fastapi import APIRouter

from app.database.clickhouse.clickhouse_engine import clickhouse_client
from app.metrics.count import REQUEST_COUNT
from app.models.Event import Event
from app.kafka.Producer import kafka_producer, delivery_report

router = APIRouter(prefix="/api/data")


@router.post("/send_event", status_code=HTTPStatus.CREATED)
def send_event(event: Event):
    event_data = {
        "event_type": event.event_type,
        "description": event.description
    }
    kafka_producer.produce('events_topic', key=event.event_type, value=str(event_data), callback=delivery_report)
    kafka_producer.flush()
    return {"status": "Event sent to Kafka"}


@router.get("/get_events", status_code=HTTPStatus.OK)
def get_events():
    query = "SELECT * FROM events"
    events = clickhouse_client.execute(query)
    return {"events": events}


@router.get("/metrics")
def metrics():
    REQUEST_COUNT.inc()
    return prometheus_client.generate_latest()