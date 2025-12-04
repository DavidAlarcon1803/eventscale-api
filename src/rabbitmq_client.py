import aio_pika
import os
import json

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")

async def publish_message(queue_name: str, message: dict):
    """
    Publica un mensaje en la cola especificada de RabbitMQ.
    """
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        
        # Declaramos la cola para asegurar que existe (durable=True para persistencia)
        await channel.declare_queue(queue_name, durable=True)
        
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=queue_name,
        )