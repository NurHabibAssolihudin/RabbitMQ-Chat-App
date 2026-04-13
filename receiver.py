import pika
import threading

from fastapi import FastAPI, WebSocket

app = FastAPI()

ws_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    ws_connections.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        ws_connections.remove(websocket)

def rabbitmq_consumer():
    credentials = pika.PlainCredentials("root", "forward098")
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost", 5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='rabbitmqpy', durable=True, arguments={
        'x-queue-type': 'quorum'
    })

    def callback(ch, method, properties, body):
        message = body.decode()
        print(f'[x] Received {message}')
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        for ws in ws_connections:
            loop.run_until_complete(ws.send_text(f"{message}"))

    channel.basic_consume(
        queue='rabbitmqpy',
        auto_ack=True,
        on_message_callback=callback
    )

    print('[x] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

@app.on_event("startup")
def startup_event():
    threading.Thread(target=rabbitmq_consumer, daemon=True).start()