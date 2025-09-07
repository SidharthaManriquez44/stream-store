import json
import os
import time
from datetime import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

BOOTSTRAP = os.getenv("BOOTSTRAP", "localhost:29092")
TOPIC = os.getenv("TOPIC", "demo-topic")

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

def main():
    print(f"[producer] Connecting to {BOOTSTRAP} ...")
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        value_serializer=json_serializer,
        linger_ms=10,
        retries=5,
        acks="all",
    )
    print(f"[producer] Ready. Sending 10 messages to '{TOPIC}' ...")

    for i in range(10):
        payload = {
            "id": i,
            "ts": datetime.utcnow().isoformat(),
            "message": f"Hello Kafka #{i}",
        }
        future = producer.send(TOPIC, value=payload)
        metadata = future.get(timeout=10)
        print(f"[producer] Sent to {metadata.topic} partition {metadata.partition} offset {metadata.offset}")
        time.sleep(0.3)

    print("[producer] Flushing...")
    producer.flush()
    print("[producer] Done.")

if __name__ == "__main__":
    main()
