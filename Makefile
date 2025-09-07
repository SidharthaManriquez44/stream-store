.PHONY: up down logs producer consumer build

up:
	docker compose up -d

down:
	docker compose down -v

logs:
	docker compose logs -f kafka

build:
	docker build -t kafka-demo-app .

producer:
	python src/producer.py

consumer:
	python src/consumer.py
