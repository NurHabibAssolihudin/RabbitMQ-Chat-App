import pika
import json
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
def main(request: Request):

    return templates.TemplateResponse(name="index.html", request=request, context={"ws_url": "ws://localhost:8888/ws"})

@app.post("/send")
async def send_message(request: Request):
    data = await request.json()
    credentials = pika.PlainCredentials("root", "forward098")
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost", 5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='rabbitmqpy', durable=True, arguments={
        'x-queue-type': 'quorum'
    })
    channel.basic_publish(
        exchange='',
        routing_key='rabbitmqpy',
        body=json.dumps(data),
    )
    print(f"[x] sending message {data['message']} from {data['user']}")
    connection.close()
    return {"status": "ok"}