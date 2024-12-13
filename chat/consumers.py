import json
import random
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_message = data.get("message", "")

        # Echo user's message back
        await self.send(json.dumps({"type": "user", "message": user_message}))

        # Bot responses
        bot_responses = [
            "Hi there! How can I help you today?",
            "I'm here to assist you. What do you need help with?",
            "That's intriguing! Could you elaborate more?",
            "Great point! Let me know if there's anything you'd like to discuss further.",
        ]
        bot_message = random.choice(bot_responses)

        # Simulate bot typing delay
        await asyncio.sleep(1.5)  # Delay for 1.5 seconds
        await self.send(json.dumps({"type": "bot", "message": bot_message}))

    # Future Steps to Implement OpenAI Integration:
    # 1. Install the OpenAI Python SDK: `pip install openai`
    # 2. Import the `openai` library.
    # 3. Set up your OpenAI API key securely.
    # 4. Replace the random bot responses with an OpenAI API call, passing the user_message as input.
    # 5. Parse the OpenAI API response and send it back to the client.
    # 6. Test the integration thoroughly to ensure proper error handling and response generation.
