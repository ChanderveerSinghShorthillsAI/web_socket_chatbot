# WebSocket Chatbot Demo 

This project is a  WebSocket-based chatbot app that streams OpenAI GPT responses in real-time. It supports optional image generation, AWS S3 uploads, and is built with a FastAPI backend and a simple HTML/CSS frontend.

---

##  Features

- **WebSocket Communication**: Real-time bi-directional messaging with FastAPI WebSockets.
- **Streaming Responses**: Token-by-token streaming from OpenAI's GPT model.
- **Horizontal Scalability**: Built to support multiple concurrent users with horizontal scaling.
- **S3 Integration**: Optional image upload and display support via AWS S3 with signed URLs.
- **OpenAI Image Handling**: Optionally generates images via DALL·E when prompted.
- **Frontend**: Basic HTML/JS UI for testing and interacting with the bot.
- **Production-Ready Architecture**: Designed with best practices for deployment, scalability, and security.
- **Load Testing**: Includes Locust-based load testing setup for performance benchmarking.

---

##  Project Structure

```
web_socket/
├── README.md
├── app/
│   ├── config.py            # Environment variable and settings management
│   ├── handler.py           # WebSocket message and OpenAI streaming handler
│   ├── image.py             # Image generation using OpenAI's image APIs
│   ├── main.py              # FastAPI app entrypoint
│   ├── models.py            # Pydantic models for messaging
│   ├── routes.py            # WebSocket endpoint routing
│   └── s3.py                # AWS S3 signed URL management
├── locustfile.py            # Load testing script using Locust
├── requirements.txt         # Python dependencies
└── static/
    └── client.html          # Basic frontend to test chatbot
```

---

##  Prerequisites

- Python 3.9 or higher
- OpenAI API key
- AWS credentials (for S3 integration)

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd web_socket
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `app/` directory with the following:

```env
OPENAI_API_KEY=your-openai-api-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_REGION=your-region
AWS_S3_BUCKET_NAME=your-bucket
```

### 5. Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` to ensure it’s running.

---

##  Frontend Usage

1. Open `static/client.html` in a browser.
2. Enter a prompt and click **Send**.
3. The chatbot streams responses in real time.
4. If image generation is enabled, images are generated and embedded in chat.

---

##  Load Testing with Locust

1. Install Locust if not already installed:

```bash
pip install locust
```

2. Run Locust from the project root:

```bash
locust -f locustfile.py
```

3. Open your browser at `http://localhost:8089` and start the test.

---

##  Key Files Explained

### Backend

- `main.py`: Starts the FastAPI app.
- `handler.py`: Core logic for token streaming and OpenAI chat interaction.
- `image.py`: Optional DALL·E image generation via OpenAI.
- `s3.py`: AWS S3 signed URL utilities.
- `routes.py`: WebSocket endpoint definition.
- `config.py`: Settings management via environment variables.
- `models.py`: Data models used for request/response validation.

### Frontend

- `client.html`: Basic interactive frontend for sending messages and viewing streamed responses/images.

### Testing

- `locustfile.py`: Simulates multiple concurrent WebSocket users for load testing.

---

##  Deployment

### Backend

- Use a cloud provider (e.g., AWS, GCP, Azure) to deploy the FastAPI backend.
- Use Docker and a process manager like Gunicorn with Uvicorn workers for production.
- Consider Kubernetes or AWS ECS/Fargate for horizontal scaling.

### Frontend

- Host `client.html` on a static site platform (e.g., Netlify, S3, GitHub Pages).

---

##  Security Notes

- Use `wss://` in production.
- Never commit `.env`, secrets, or AWS credentials.
- Limit OpenAI and AWS usage via quotas and IAM roles.
- Use rate limiting/load balancing in production.

---

##  License

MIT License. See [`LICENSE`](LICENSE) for details.

---

##  Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI](https://openai.com/)
- [Amazon S3](https://aws.amazon.com/s3/)
- [Locust](https://locust.io/)

---

##  Author

**Chanderveer Singh Chauhan**

