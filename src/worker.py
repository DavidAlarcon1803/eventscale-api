import asyncio
import json
import os
import aio_pika

RABBITMQ_URL = os.getenv("RABBITMQ_URL")

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = json.loads(message.body)
        print(f" [x] Recibido tarea: {body['type']} para {body['email']}")
        
        # Simular procesamiento pesado (generar PDF, enviar email)
        await asyncio.sleep(2) 
        
        print(f" [v] Correo enviado a {body['email']} - Ticket {body['ticket_id']}")

async def main():
    # Conexión resiliente (básica)
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    
    async with connection:
        channel = await connection.channel()
        
        # Declarar la cola (debe coincidir con el productor)
        queue = await channel.declare_queue("eventscale_queue", durable=True)
        
        print(" [*] Worker esperando mensajes...")
        
        # Consumir mensajes
        await queue.consume(process_message)
        
        # Mantener el script corriendo
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())