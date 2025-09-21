import json
import random
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data.get("message", "").strip()

        if not message_content:
            return

        # For demo purposes, create/use a default user and room
        user, _ = await self.get_or_create_user()
        room, _ = await self.get_or_create_room()

        # Save user message to database
        user_message = await self.save_message(room, user, message_content)

        # Echo user's message back with read status
        await self.send(json.dumps({
            "type": "user",
            "message": message_content,
            "id": user_message.id,
            "timestamp": user_message.timestamp.isoformat()
        }))

        # Mark message as read (since it's being sent to the client)
        await self.mark_as_read(user_message)

        # Bot responses
        bot_responses = [
            "Hi there! How can I help you today?",
            "I'm here to assist you. What do you need help with?",
            "That's intriguing! Could you elaborate more?",
            "Great point! Let me know if there's anything you'd like to discuss further.",
        ]
        bot_message_content = random.choice(bot_responses)

        # Save bot message to database
        bot_message = await self.save_message(room, user, bot_message_content, is_bot=True)

        # Simulate bot typing delay
        await asyncio.sleep(1.5)
        await self.send(json.dumps({
            "type": "bot",
            "message": bot_message_content,
            "id": bot_message.id,
            "timestamp": bot_message.timestamp.isoformat()
        }))

        # Mark bot message as read
        await self.mark_as_read(bot_message)

    async def get_or_create_user(self):
        # For demo purposes, create a default user
        user, created = await User.objects.aget_or_create(
            username="demo_user",
            defaults={"email": "demo@example.com"}
        )
        return user, created

    async def get_or_create_room(self):
        # For demo purposes, create a default room
        room, created = await Room.objects.aget_or_create(
            name="General Chat",
            defaults={"description": "General discussion room"}
        )
        return room, created

    async def save_message(self, room, user, content, is_bot=False):
        # For bot messages, we could create a bot user, but for simplicity we'll use the same user
        message = await Message.objects.acreate(
            room=room,
            user=user,
            content=content
        )
        return message

    async def mark_as_read(self, message):
        message.read_at = timezone.now()
        await message.asave()


"""
TODO: Future Steps to Implement OpenAI Integration:
1. Install the OpenAI Python SDK: `pip install openai`
2. Import the `openai` library.
3. Set up your OpenAI API key securely.
4. Replace the random bot responses with an OpenAI API call, passing the user_message as input.
5. Parse the OpenAI API response and send it back to the client.
6. Test the integration to ensure proper error handling and response generation.
"""
