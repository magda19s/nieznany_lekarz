#!/bin/sh
echo "Running makemigrations..."
python manage.py makemigrations --noinput

echo "Running migrate..."
python manage.py migrate --noinput

echo "Creating superuser if not exists..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
EOF

echo "Waiting for RabbitMQ to be available..."
until nc -z rabbitmq 5672; do
  echo "RabbitMQ is unavailable - sleeping"
  sleep 2
done
echo "RabbitMQ is up!"

echo "Starting Emails consumer..."
python manage.py email_consumer &

echo "Waiting for RabbitMQ to be available..."
until nc -z rabbitmq 5672; do
  echo "RabbitMQ is unavailable - sleeping"
  sleep 2
done
echo "RabbitMQ is up!"

echo "Starting Notification Emails consumer..."
python manage.py notification_consumer &

echo "Waiting for RabbitMQ to be available..."
until nc -z rabbitmq 5672; do
  echo "RabbitMQ is unavailable - sleeping"
  sleep 2
done
echo "RabbitMQ is up!"

echo "Starting Doctor Emails consumer..."
python manage.py doctor_consumer &

echo "Waiting for RabbitMQ to be available..."
until nc -z rabbitmq 5672; do
  echo "RabbitMQ is unavailable - sleeping"
  sleep 2
done
echo "RabbitMQ is up!"

echo "Starting Notes Emails consumer..."
python manage.py notes_consumer &

echo "Starting Django server..."
exec "$@"
