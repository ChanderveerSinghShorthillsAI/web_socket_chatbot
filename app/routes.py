from fastapi import APIRouter, WebSocket
from app.models import WebSocketQuery
from app.handler import handle_stream

import logging
logger = logging.getLogger("chatbot") # Set up a logger for the chatbot application.
logging.basicConfig(level=logging.INFO) # Set up logging configuration

router = APIRouter() # Create a new router instance for defining API routes.

@router.websocket("/ws/query") 
async def websocket_query(websocket: WebSocket): # WebSocket endpoint for handling queries.
    """
    Handles WebSocket connections for querying.

    This WebSocket endpoint is designed to accept incoming WebSocket connections,
    receive JSON-encoded queries, process them, and send responses back to the client.
    It also handles errors gracefully and ensures the WebSocket connection is closed
    properly in case of an exception.

    Args:
        websocket (WebSocket): The WebSocket connection instance provided by FastAPI.

    Workflow:
    1. Accepts the WebSocket connection and logs the successful connection.
    2. Enters an infinite loop to continuously listen for incoming JSON messages.
    3. Parses the received JSON data into a `WebSocketQuery` object.
    4. Passes the parsed query, prompt, and parameters to the `handle_stream` function
       for further processing and streaming responses back to the client.
    5. Handles any exceptions that occur during the WebSocket communication or processing:
       - Logs the error with detailed information.
       - Sends an error message back to the client in JSON format.
       - Closes the WebSocket connection and logs the closure.

    Raises:
        Exception: Any exception that occurs during WebSocket communication or query handling
        is caught and logged, and the WebSocket connection is closed.

    Logging:
    - Logs the acceptance of the WebSocket connection.
    - Logs each received query in JSON format.
    - Logs any errors encountered during processing.
    - Logs the closure of the WebSocket connection in case of an error.

    Note:
    - The `WebSocketQuery` class is expected to define the structure of the incoming JSON data.
    - The `handle_stream` function is responsible for processing the query and sending responses.
    """
    await websocket.accept() # Accept the WebSocket connection.
    # Log the acceptance of the connection.
    logger.info("🟢 WebSocket connection accepted.") 
    try:
        while True:
            data = await websocket.receive_json() # Receive JSON data from the WebSocket.
            logger.info(f"📥 Received query: {data}") 
            query_data = WebSocketQuery(**data) # Parse the received data into a WebSocketQuery object.
            await handle_stream(websocket, query_data.query, query_data.prompt, query_data.param)  # Handle the query and stream the response.
    except Exception as e:
        logger.error(f"❌ Error handling WebSocket: {e}", exc_info=True)
        await websocket.send_json({"type": "error", "message": str(e)}) # Send an error message back to the client.
        await websocket.close() # Close the WebSocket connection.
        logger.info("🔴 WebSocket connection closed due to error.")


