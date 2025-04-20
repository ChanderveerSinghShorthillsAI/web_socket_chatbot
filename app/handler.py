import time # Importing time for measuring execution time.
import asyncio # Importing asyncio for asynchronous programming.
from app.models import QueryParam  # Importing the QueryParam model for handling query parameters.
from app.s3 import S3Manager  # Importing S3Manager for handling AWS S3 operations.
from app.config import settings  # Importing application settings for configuration values.
import openai  # Importing the OpenAI library for interacting with OpenAI APIs.
import logging  # Importing logging for logging messages.
import os  # Importing os for environment variable access.

# Setting up a logger for the chatbot application.
logger = logging.getLogger("chatbot")

# Initialize OpenAI client with API key from application settings.
openai.api_key = settings.openai_api_key
from openai import AsyncOpenAI  # Importing the asynchronous OpenAI client.
print("openai.api_key", openai.api_key)  # Debugging line to print the OpenAI API key.
# Creating an instance of the asynchronous OpenAI client with the API key.
client = AsyncOpenAI(api_key=settings.openai_api_key)
# client = os.getenv("OPENAI_API_KEY")  # Fetching the OpenAI API key from environment variables.

# Function to handle the OpenAI stream response.
async def openai_stream(query: str, param: QueryParam, system_prompt: str):
    """
    Sends a query to OpenAI's chat completion API and streams the response.

    Args:
        query (str): The user's query.
        param (QueryParam): Query parameters including streaming preferences.
        system_prompt (str): The system prompt to guide the AI's behavior.

    Returns:
        token_stream (async generator): A generator that yields tokens from the OpenAI response.
        image_data (list): Placeholder for image data (currently unused).
    """
    # Sending the query to OpenAI's chat completion API with streaming enabled.
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",  # Specifying the model to use.
        messages=[
            {"role": "system", "content": system_prompt},  # System prompt for guiding the AI.
            {"role": "user", "content": query}  # User's query.
        ],
        stream=True  # Enabling streaming for the response.
    )

    # Asynchronous generator to yield tokens from the OpenAI response.
    async def token_stream():
        async for chunk in response:  # Iterating over the streamed response chunks.
            delta = chunk.choices[0].delta  # Extracting the delta (change) from the response.
            if delta and delta.content:  # If the delta contains content, yield it.
                yield delta.content
                await asyncio.sleep(0.01)  # Simulating a small delay for streaming.

    return token_stream(), []  # Returning the token stream and an empty list for image data.

# Function to handle WebSocket streaming for the client.
async def handle_stream(websocket, query: str, prompt: str, param: QueryParam):
    """
    Handles the WebSocket connection for streaming responses to the client.

    Args:
        websocket: The WebSocket connection object.
        query (str): The user's query.
        prompt (str): The system prompt to guide the AI's behavior.
        param (QueryParam): Query parameters including streaming preferences.
    """
    start_time = time.time()  # Record the start time for execution time calculation.
    logger.info(f"⚙️ Handling OpenAI stream for query: '{query}' with prompt: '{prompt}'")

    if param.stream:  # If streaming is enabled in the query parameters.
        try:
            # Get the OpenAI response stream and image data (if any).
            response_stream, image_data = await openai_stream(query, param=param, system_prompt=prompt)
            image_urls = []  # Initialize an empty list for image URLs.

            if image_data:  # If there is image data, upload it to S3 and get presigned URLs.
                try:
                    s3_manager = S3Manager(bucket_name=settings.aws_s3_bucket_name)  # Initialize S3 manager.
                    image_urls = s3_manager.get_presigned_urls("generated_images", image_data)  # Get presigned URLs.
                    logger.info(f"🖼️ Generated image URLs: {image_urls}")
                except Exception as e:
                    logger.error(f"❌ Error generating image URLs: {e}", exc_info=True)

            full_response = ""  # Initialize a variable to store the full response.
            async for token in response_stream:  # Iterate over the response tokens.
                full_response += token + " "  # Append each token to the full response.
                await websocket.send_json({"type": "token", "value": token})  # Send the token to the client.
                logger.debug(f"📤 Sent token: {token}")

            # Prepare metadata to send to the client after streaming is complete.
            metadata = {
                "type": "metadata",
                "execution_time": round(time.time() - start_time, 4),  # Calculate execution time.
                "image_urls": image_urls,  # Include image URLs (if any).
                "full_response": full_response.strip()  # Include the full response.
            }
            await websocket.send_json(metadata)  # Send the metadata to the client.
            logger.info("✅ Sent final metadata.")
        except Exception as e:  # Handle any exceptions during streaming.
            logger.error(f"❌ Streaming failed: {e}", exc_info=True)
            await websocket.send_json({"type": "error", "message": "Streaming failed"})  # Notify the client of the error.
            await websocket.close()  # Close the WebSocket connection.
    else:  # If streaming is not enabled, handle the response as a single result.
        try:
            # Get the OpenAI response stream and image data (if any).
            response_stream, image_data = await openai_stream(query, param=param, system_prompt=prompt)
            full_response = " ".join([t async for t in response_stream])  # Collect all tokens into a single response.
            image_urls = []  # Initialize an empty list for image URLs.

            if image_data:  # If there is image data, upload it to S3 and get presigned URLs.
                try:
                    s3_manager = S3Manager(bucket_name=settings.aws_s3_bucket_name)  # Initialize S3 manager.
                    image_urls = s3_manager.get_presigned_urls("generated_images", image_data)  # Get presigned URLs.
                    logger.info(f"🖼️ Generated image URLs: {image_urls}")
                except Exception as e:
                    logger.error(f"❌ Error generating image URLs: {e}", exc_info=True)

            # Send the full response and image URLs to the client.
            await websocket.send_json({
                "type": "full_result",
                "value": full_response,  # Include the full response.
                "image_urls": image_urls  # Include image URLs (if any).
            })
            logger.info("✅ Sent full result (non-streaming).")
        except Exception as e:  # Handle any exceptions during response handling.
            logger.error(f"❌ Streaming failed: {e}", exc_info=True)
            await websocket.send_json({"type": "error", "message": "Failed to fetch response"})  # Notify the client of the error.
            await websocket.close()  # Close the WebSocket connection.
