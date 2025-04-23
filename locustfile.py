from locust import User, task, between
import websocket
import json
import time

class ChatbotUser(User):
    # Simulate a wait time between tasks (e.g., 1 to 3 seconds)
    wait_time = between(1, 3)

    def on_start(self):
        """
        This method is called when a simulated user starts.
        It establishes a WebSocket connection to the chatbot server.
        """
        self.ws = websocket.WebSocket()
        try:
            # Connect to the WebSocket server
            self.ws.connect("ws://localhost:8000/ws/query")
            print("✅ WebSocket connection established.")
        except Exception as e:
            print(f"❌ Failed to connect to WebSocket: {e}")

    def on_stop(self):
        """
        This method is called when a simulated user stops.
        It closes the WebSocket connection.
        """
        try:
            self.ws.close()
            print("🔴 WebSocket connection closed.")
        except Exception as e:
            print(f"❌ Failed to close WebSocket: {e}")

    @task
    def send_query(self):
        """
        Simulates a user sending a query to the chatbot.
        """
        query = "What is the capital of France?"
        message = {
            "query": query,
            "prompt": "Assistant",
            "param": {"stream": True}
        }

        try:
            # Send the query as a JSON message
            self.ws.send(json.dumps(message))
            print(f"📤 Sent query: {query}")

            # Receive and process the response
            start_time = time.time()
            while True:
                response = self.ws.recv()
                data = json.loads(response)
                if data["type"] == "token":
                    print(f"📥 Received token: {data['value']}")
                elif data["type"] == "metadata":
                    print(f"⏱ Metadata: {data}")
                    break
                elif data["type"] == "error":
                    print(f"❌ Error: {data['message']}")
                    break
            end_time = time.time()
            print(f"✅ Query completed in {round(end_time - start_time, 2)} seconds.")
        except Exception as e:
            print(f"❌ Error during WebSocket communication: {e}")