from aiokafka import AIOKafkaProducer
import json
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
ENABLE_KAFKA = os.getenv("ENABLE_KAFKA", "true").lower() == "true"
KAFKA_TOPIC = os.getenv("KAFKA_CUSTOMER_TOPIC", "customer-events")

producer = AIOKafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    enable_idempotence=True,
    acks='all',
    request_timeout_ms=30000,
)

async def start_producer():
    if not ENABLE_KAFKA:
        print("Kafka disabled")
        return
    for i in range(10):
        try:
            await producer.start()
            print(f"Kafka connected to {KAFKA_BOOTSTRAP}")
            return
        except Exception as e:
            print(f"Kafka retry {i+1}: {e}")
            await asyncio.sleep(3)
    print("Kafka unavailable - continuing without it")

async def stop_producer():
    if ENABLE_KAFKA and producer._client.is_connected():
        await producer.stop()
        print("Kafka producer stopped")

async def send_event(event_type: str, data: dict):
    if not ENABLE_KAFKA:
        return
    event = {
        "event_type": event_type,
        "timestamp": asyncio.get_event_loop().time(),
        "data": data
    }
    try:
        await producer.send_and_wait(KAFKA_TOPIC, json.dumps(event).encode("utf-8"))
        print(f"Event sent: {event_type}")
    except Exception as e:
        print(f"Kafka send failed: {e}")
