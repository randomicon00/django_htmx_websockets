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

        # BOT responses
        bot_responses = [
            "Hello there! How can I assist you?",
            "I'm just a bot, but I try my best!",
            "Interesting... tell me more!",
            "That's a great point.",
        ]
        bot_message = random.choice(bot_responses)

        # Simulate bot typing delay
        await asyncio.sleep(1.5)  # Delay for 1.5 seconds
        await self.send(json.dumps({"type": "bot", "message": bot_message}))
