import os, uuid, json, pytest
try:
    from kafka import KafkaProducer, KafkaConsumer
except Exception:
    KafkaProducer = KafkaConsumer = None
@pytest.mark.integration
def test_produce_and_consume_roundtrip():
    if KafkaProducer is None: pytest.skip("kafka-python not installed")
    bootstrap=os.getenv("BOOTSTRAP","127.0.0.1:29092"); topic=os.getenv("TOPIC","demo-topic"); gid=f"pytest-{uuid.uuid4().hex[:8]}"
    try:
        p = KafkaProducer(bootstrap_servers=bootstrap, value_serializer=lambda d: json.dumps(d).encode("utf-8"), retries=1, acks="all")
    except Exception as e:
        pytest.skip(f"Cannot connect to Kafka at {bootstrap}: {e}")
    payload={"test":"ok","uuid":uuid.uuid4().hex}; p.send(topic,payload).get(timeout=10); p.flush()
    c = KafkaConsumer(topic, bootstrap_servers=bootstrap, group_id=gid, auto_offset_reset="earliest", enable_auto_commit=False,
                      value_deserializer=lambda b: json.loads(b.decode("utf-8")), consumer_timeout_ms=5000)
    for msg in c:
        if isinstance(msg.value, dict) and msg.value.get("uuid")==payload["uuid"]: break
    else: pytest.fail("Did not receive produced message within timeout")
