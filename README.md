# RabbitMQ Chat Application

> Aplikasi chat real-time menggunakan RabbitMQ sebagai message broker dan WebSocket untuk komunikasi client-server.

[English](#english-documentation) | [Indonesian](#dokumentasi-bahasa-indonesia)

---

## Dokumentasi Bahasa Indonesia

### 📋 Deskripsi Proyek

RabbitMQ Chat adalah aplikasi web real-time yang memungkinkan multiple user untuk berkomunikasi melalui antarmuka web. Aplikasi ini menggunakan:
- **FastAPI** untuk backend API
- **WebSocket** untuk komunikasi real-time
- **RabbitMQ** sebagai message broker untuk persistensi pesan
- **Jinja2** untuk template HTML front-end

### ✨ Fitur

- ✅ Chat real-time antar pengguna
- ✅ Pesan disimpan dalam RabbitMQ queue
- ✅ WebSocket connection untuk live updates
- ✅ Multiple user support (User1, User2, dll)
- ✅ UI yang responsif dan modern
- ✅ Auto-scroll untuk pesan baru
- ✅ Validasi input pesan

### 🏗️ Arsitektur

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   User1     │         │   User2      │         │   UserN     │
│  (Port 8281)│         │  (Port 8282) │         │  (Port...)  │
└──────┬──────┘         └──────┬───────┘         └──────┬──────┘
       │                       │                        │
       └───────────┬───────────┴────────────────────────┘
                   │
        ┌──────────▼───────────┐
        │       Receiver       │
        │     (Port 8888)      │
        │ WebSocket + RabbitMQ │
        └─────┬──────────┬─────┘
              │          │
        ┌─────▼────┐  ┌──▼────────┐
        │WebSocket │  │ RabbitMQ  │
        │Handler   │  │ Queue     │
        └──────────┘  └───────────┘
```

### 📦 Requirements

- Python >= 3.13
- RabbitMQ Server (running di localhost:5672)
- FastAPI
- Uvicorn
- Pika (RabbitMQ client)
- Jinja2

### 🚀 Instalasi & Setup

#### 1. Clone Repository
```bash
git clone <your-repo-url>
cd rabbitmq-py
```

#### 2. Setup Python Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# atau
.venv\Scripts\activate  # Windows
```

#### 3. Install Dependencies
```bash
pip install -e .
# atau jika menggunakan uv
uv sync
```

#### 4. Setup RabbitMQ

Pastikan RabbitMQ server berjalan di `localhost:5672` dengan credentials:
- Username: `root`
- Password: `forward098`

```bash
# Jika menggunakan Docker
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 \
  -e RABBITMQ_DEFAULT_USER=root \
  -e RABBITMQ_DEFAULT_PASS=forward098 \
  rabbitmq:latest
```

### 🏃 Cara Menjalankan Aplikasi

Aplikasi terdiri dari 3 komponen yang harus dijalankan di terminal terpisah:

#### Terminal 1: Jalankan Receiver (Message Hub)
```bash
cd /path/to/rabbitmq-py
uv run uvicorn receiver:app --port 8888
```

Output:
```
INFO:     Started server process [PID]
INFO:     Uvicorn running on http://127.0.0.1:8888
```

#### Terminal 2: Jalankan User1 Chat Client
```bash
cd /path/to/rabbitmq-py/user1
uv run uvicorn main:app --port 8281
```

Output:
```
INFO:     Started server process [PID]
INFO:     Uvicorn running on http://127.0.0.1:8281
```

#### Terminal 3: Jalankan User2 Chat Client (Optional)
```bash
cd /path/to/rabbitmq-py/user2
uv run uvicorn main:app --port 8282
```

#### Buka di Browser
- User1: http://localhost:8281
- User2: http://localhost:8282
- Receiver: http://localhost:8888

### 📁 Struktur Proyek

```
rabbitmq-py/
├── README.md                 # Dokumentasi
├── pyproject.toml           # Dependency & project config
├── receiver.py              # Central message hub
├── user1/
│   ├── main.py             # FastAPI app untuk User1
│   └── templates/
│       └── index.html      # Chat UI
├── user2/
│   ├── main.py             # FastAPI app untuk User2
│   └── templates/
│       └── index.html      # Chat UI
└── .venv/                   # Virtual environment
```

### 🔄 Cara Kerja Aplikasi

1. **User mengirim pesan** via form di browser
2. **Client script** mengirim HTTP POST request ke `/send` endpoint
3. **FastAPI app** menerima pesan dan publish ke RabbitMQ queue `rabbitmqpy`
4. **RabbitMQ** menyimpan pesan dalam queue
5. **Receiver service** consume pesan dari RabbitMQ
6. **Receiver** broadcast pesan ke semua WebSocket clients yang connected
7. **Client browser** menerima pesan via WebSocket dan display di chat

### 📝 File-File Penting

#### `receiver.py`
- Central hub yang manage WebSocket connections
- Consume messages dari RabbitMQ queue
- Broadcast incoming messages ke semua connected clients

#### `user1/main.py` & `user2/main.py`
- FastAPI application untuk setiap user
- Handle GET `/` untuk render chat UI
- Handle POST `/send` untuk publish pesan ke RabbitMQ

#### `user1/templates/index.html` & `user2/templates/index.html`
- Frontend HTML + CSS + JavaScript
- WebSocket connection ke receiver
- Send message form dengan fetch API
- Real-time message display

### ⚙️ Konfigurasi

Untuk mengubah RabbitMQ credentials, edit file yang berisi:

**receiver.py** & **user1/main.py** & **user2/main.py**:
```python
credentials = pika.PlainCredentials("root", "forward098")
connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost", 5672, credentials=credentials)
)
```

Queue name: `rabbitmqpy`
Queue type: `quorum` (durable, replicated)

### 🐛 Troubleshooting

#### Error: Connection refused to localhost:5672
- Pastikan RabbitMQ server sudah running
- Check port dengan: `netstat -an | grep 5672`

#### Error: unhashable type: 'dict'
- Pastikan menggunakan Starlette terbaru
- Update dependencies: `pip install --upgrade fastapi starlette`

#### WebSocket connection failed
- Pastikan receiver service running di port 8888
- Check firewall settings

#### Template not found
- Pastikan folder `templates/` ada di folder yang sama dengan `main.py`
- Check path di `BASE_DIR` variable

### 📚 Dependencies

Lihat `pyproject.toml` untuk daftar lengkap dependencies:
- fastapi >= 0.135.3
- uvicorn[standard] >= 0.44.0
- jinja2 >= 3.1.6
- pika >= 1.3.2
- python-multipart >= 0.0.26

---

## English Documentation

### 📋 Project Description

RabbitMQ Chat is a real-time web application that allows multiple users to communicate through a web interface. The application uses:
- **FastAPI** for backend API
- **WebSocket** for real-time communication
- **RabbitMQ** as message broker for message persistence
- **Jinja2** for front-end HTML templates

### ✨ Features

- ✅ Real-time chat between users
- ✅ Messages stored in RabbitMQ queue
- ✅ WebSocket connection for live updates
- ✅ Multiple user support (User1, User2, etc)
- ✅ Responsive and modern UI
- ✅ Auto-scroll for new messages
- ✅ Message input validation

### 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   User1     │         │   User2      │         │   UserN     │
│  (Port 8281)│         │  (Port 8282) │         │  (Port...)  │
└──────┬──────┘         └──────┬───────┘         └──────┬──────┘
       │                       │                        │
       └───────────┬───────────┴────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │      Receiver       │
        │    (Port 8888)      │
        │ WebSocket + RabbitMQ│
        └─────┬──────────┬────┘
              │          │
        ┌─────▼────┐  ┌──▼────────┐
        │WebSocket │  │ RabbitMQ  │
        │Handler   │  │ Queue     │
        └──────────┘  └───────────┘
```

### 📦 Requirements

- Python >= 3.13
- RabbitMQ Server (running on localhost:5672)
- FastAPI
- Uvicorn
- Pika (RabbitMQ client)
- Jinja2

### 🚀 Installation & Setup

#### 1. Clone Repository
```bash
git clone <your-repo-url>
cd rabbitmq-py
```

#### 2. Setup Python Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

#### 3. Install Dependencies
```bash
pip install -e .
# or using uv
uv sync
```

#### 4. Setup RabbitMQ

Ensure RabbitMQ server is running on `localhost:5672` with credentials:
- Username: `root`
- Password: `forward098`

```bash
# Using Docker
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 \
  -e RABBITMQ_DEFAULT_USER=root \
  -e RABBITMQ_DEFAULT_PASS=forward098 \
  rabbitmq:latest
```

### 🏃 Running the Application

The application consists of 3 components that should run in separate terminals:

#### Terminal 1: Run Receiver (Message Hub)
```bash
cd /path/to/rabbitmq-py
uv run uvicorn receiver:app --port 8888
```

Output:
```
INFO:     Started server process [PID]
INFO:     Uvicorn running on http://127.0.0.1:8888
```

#### Terminal 2: Run User1 Chat Client
```bash
cd /path/to/rabbitmq-py/user1
uv run uvicorn main:app --port 8281
```

Output:
```
INFO:     Started server process [PID]
INFO:     Uvicorn running on http://127.0.0.1:8281
```

#### Terminal 3: Run User2 Chat Client (Optional)
```bash
cd /path/to/rabbitmq-py/user2
uv run uvicorn main:app --port 8282
```

#### Open in Browser
- User1: http://localhost:8281
- User2: http://localhost:8282
- Receiver: http://localhost:8888

### 📁 Project Structure

```
rabbitmq-py/
├── README.md                 # Documentation
├── pyproject.toml           # Dependency & project config
├── receiver.py              # Central message hub
├── user1/
│   ├── main.py             # FastAPI app for User1
│   └── templates/
│       └── index.html      # Chat UI
├── user2/
│   ├── main.py             # FastAPI app for User2
│   └── templates/
│       └── index.html      # Chat UI
└── .venv/                   # Virtual environment
```

### 🔄 How the Application Works

1. **User sends message** via form in browser
2. **Client script** sends HTTP POST request to `/send` endpoint
3. **FastAPI app** receives message and publishes to RabbitMQ queue `rabbitmqpy`
4. **RabbitMQ** stores message in queue
5. **Receiver service** consumes message from RabbitMQ
6. **Receiver** broadcasts message to all connected WebSocket clients
7. **Client browser** receives message via WebSocket and displays in chat

### 📝 Important Files

#### `receiver.py`
- Central hub that manages WebSocket connections
- Consumes messages from RabbitMQ queue
- Broadcasts incoming messages to all connected clients

#### `user1/main.py` & `user2/main.py`
- FastAPI application for each user
- Handles GET `/` to render chat UI
- Handles POST `/send` to publish message to RabbitMQ

#### `user1/templates/index.html` & `user2/templates/index.html`
- Frontend HTML + CSS + JavaScript
- WebSocket connection to receiver
- Send message form with fetch API
- Real-time message display

### ⚙️ Configuration

To change RabbitMQ credentials, edit files containing:

**receiver.py** & **user1/main.py** & **user2/main.py**:
```python
credentials = pika.PlainCredentials("root", "forward098")
connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost", 5672, credentials=credentials)
)
```

Queue name: `rabbitmqpy`
Queue type: `quorum` (durable, replicated)

### 🐛 Troubleshooting

#### Error: Connection refused to localhost:5672
- Ensure RabbitMQ server is running
- Check port with: `netstat -an | grep 5672`

#### Error: unhashable type: 'dict'
- Ensure using latest Starlette version
- Update dependencies: `pip install --upgrade fastapi starlette`

#### WebSocket connection failed
- Ensure receiver service is running on port 8888
- Check firewall settings

#### Template not found
- Ensure `templates/` folder exists in the same directory as `main.py`
- Check `BASE_DIR` variable path

### 📚 Dependencies

See `pyproject.toml` for full list of dependencies:
- fastapi >= 0.135.3
- uvicorn[standard] >= 0.44.0
- jinja2 >= 3.1.6
- pika >= 1.3.2
- python-multipart >= 0.0.26

### 📄 License

This project is open source and available for anyone to use.

### 👤 Author

Created for RabbitMQ + FastAPI learning purposes.
