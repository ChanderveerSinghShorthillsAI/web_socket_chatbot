# WebSocket Chatbot Demo

This project is a WebSocket-based chatbot application that streams responses from OpenAI's GPT model. It includes a backend built with FastAPI and a frontend for interacting with the chatbot in real-time.

---

## Features

- **WebSocket Communication**: Real-time communication between the client and server using WebSockets.
- **Streaming Responses**: Token-by-token streaming of responses from OpenAI's GPT model.
- **Frontend**: A simple HTML/CSS/JavaScript-based interface for interacting with the chatbot.
- **Backend**: FastAPI-based backend for handling WebSocket connections and OpenAI API integration.

---

## Project Structure

```
web_socket/
├── README.md
├── app/
│   ├── config.py
│   ├── handler.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   └── s3.py
├── requirements.txt
└── static/
    └── client.html
```

---

## Prerequisites

- Python 3.9 or higher
- Node.js (optional, if you plan to extend the frontend)
- AWS credentials (for S3 integration)
- OpenAI API key

---

## ⚙️ Setup Instructions

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

Create a `.env` file in the `app/` directory with the following content:

```env
OPENAI_API_KEY=your-openai-api-key
```

### 5. Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The server will be available at:  
`http://localhost:8000`

---

## Frontend Usage

1. Open the `static/client.html` file in your browser.
2. Type a query in the input box and click **Send**.
3. View the chatbot's response in real-time.

---

## Key Files

### Backend

- `app/config.py`: Manages environment variables using Pydantic.
- `app/handler.py`: Handles OpenAI API streaming and WebSocket responses.
- `app/routes.py`: Defines the WebSocket route for handling queries.
- `app/s3.py`: Manages AWS S3 operations, including generating presigned URLs.

### Frontend

- `static/client.html`: Provides a simple interface for interacting with the chatbot.

---

## Deployment

### Deploying Backend

- Use a cloud provider like AWS, Azure, or Google Cloud to deploy the FastAPI backend.
- Use Docker for containerization if needed.

### Deploying Frontend

- Host the `client.html` file on a static hosting service like GitHub Pages, Netlify, or AWS S3.

---

## Security Notes

- **Do not commit sensitive files**: Ensure `.env` and `venv/` are listed in `.gitignore`.
- **Use HTTPS**: Always use secure WebSocket (`wss://`) in production.

---

## License

This project is licensed under the MIT License.  
See the [`LICENSE`](LICENSE) file for details.

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) — for the backend framework.
- [OpenAI](https://openai.com/) — for the GPT model.
- [AWS S3](https://aws.amazon.com/s3/) — for cloud storage.

---

## Author

- **Chanderveer Singh Chauhan**

