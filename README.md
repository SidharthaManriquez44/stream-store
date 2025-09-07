# Kafka + Python (docker-compose) — Local Demo

This project gives you a **ready-to-run** Apache Kafka broker (KRaft mode) with a web UI and two simple Python apps (producer & consumer).

## What you get
- **Kafka (KRaft, no ZooKeeper)** — single broker for local dev
- **Kafka UI** — nice web interface at http://localhost:8080
- **Python examples** using `kafka-python` (pure Python, no native deps)

## Quick start

1) Start the stack:
```bash
docker compose up -d
```

2) Open the UI at:
- http://localhost:8080  (Kafka UI)
  - Broker: `kafka:9092`
  - External: `localhost:29092`

3) (Optional) Create topic `demo-topic` in the UI (Topics → Create)  
   *Auto-creation is also enabled, so producing will create it if missing.*

4) Install Python deps (if you want to run producer/consumer on your host):
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

5) In one terminal, run the **consumer**:
```bash
python src/consumer.py
```

6) In another terminal, run the **producer** (sends 10 messages):
```bash
python src/producer.py
```

You should see messages arriving in the consumer.

## Using Docker to run the apps (optional)

If you prefer to run the producer/consumer in containers (no local Python needed):

```bash
    # Build
    docker build -t kafka-demo-app .
    
    # Consumer
    docker run --rm --network host -e BOOTSTRAP=localhost:29092 -e TOPIC=demo-topic kafka-demo-app python src/consumer.py
    
    # Producer
    docker run --rm --network host -e BOOTSTRAP=localhost:29092 -e TOPIC=demo-topic kafka-demo-app python src/producer.py
```

> We use `--network host` for simplicity so the app can reach `localhost:29092` on your machine. On macOS/Windows with Docker Desktop, `--network host` behaves differently; you can instead pass `-e BOOTSTRAP=kafka:9092 --network kafka-python-demo_default` and run from within the compose network:
> 
> ```bash
> # docker
> docker network ls  # find the network name; typically kafka-python-demo_default
> docker run --rm --network kafka-python-demo_default -e BOOTSTRAP=kafka:9092 -e TOPIC=demo-topic kafka-demo-app python src/producer.py
> ```

## Helpful commands

```bash
    docker compose logs -f kafka
    docker compose ps
    docker compose down -v
```

## Files

- `docker-compose.yml` — Kafka (KRaft) + Kafka UI
- `src/producer.py` — sends example messages
- `src/consumer.py` — prints messages from a topic
- `requirements.txt` — Python dependencies
- `Dockerfile` — container for Python app (optional)
- `.env` — defaults for topic & bootstrap servers

---

### Troubleshooting

- If the consumer shows no messages:
  - Confirm the topic exists (Kafka UI) and bootstrap address matches your run mode.
  - If you recreated the broker, the offsets may be gone; restart consumer.
- Port already in use? Change the mapped ports in `docker-compose.yml` (29092/8080).
- Windows PowerShell tip: use `python` or `py -m venv .venv` accordingly.
