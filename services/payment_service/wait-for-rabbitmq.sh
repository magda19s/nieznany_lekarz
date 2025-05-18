#!/bin/sh

# Czekaj aż RabbitMQ będzie nasłuchiwał na porcie 5672
echo "Waiting for RabbitMQ..."

while ! nc -z rabbitmq 5672; do
  sleep 1
done

echo "RabbitMQ is up!"