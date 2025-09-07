import json
import os
import signal
import sys
from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

BOOTSTRAP = os.getenv("BOOTSTRAP", "localhost:29092")
TOPIC = os.getenv("TOPIC", "demo-topic")
GROUP_ID = os.getenv("GROUP_ID", "demo-consumer")

running = True

def handle_signal(sig, frame):
    global running
    print("\n[consumer] Signal received, shutting down...")
    running = False

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)

def main():
    print(f"[consumer] Connecting to {BOOTSTRAP} ...")
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP,
        group_id=GROUP_ID,
        enable_auto_commit=True,
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        consumer_timeout_ms=0,  # block forever
    )

    print(f"[consumer] Subscribed to '{TOPIC}'. Waiting for messages...")
    try:
        while running:
            for msg in consumer:
                print(f"[consumer] topic={msg.topic} partition={msg.partition} offset={msg.offset} key={msg.key} value={msg.value}")
                if not running:
                    break
    finally:
        print("[consumer] Closing consumer...")
        consumer.close()

if __name__ == "__main__":
    main()
