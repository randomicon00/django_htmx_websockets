from django.test import TestCase, Client
from django.urls import reverse
from .models import Room, Message
from channels.testing import WebsocketCommunicator
from .routing import application


class RoomModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            name="Test Room", description="This is a test room."
        )

    def test_room_str(self):
        self.assertEqual(str(self.room), "Test Room")

    def test_room_repr(self):
        self.assertEqual(
            repr(self.room),
            "<Room(name='Test Room', description='This is a test room.')>",
        )


class MessageModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="Test Room")
        self.message = Message.objects.create(room=self.room, content="Hello, world!")

    def test_message_str(self):
        self.assertIn("Message in Test Room", str(self.message))
        self.assertIn("Hello, world!", str(self.message))

    def test_message_repr(self):
        self.assertIn("<Message(room='Test Room'", repr(self.message))
        self.assertIn("content_preview='Hello, world!'", repr(self.message))


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.room = Room.objects.create(name="Test Room")
        Message.objects.create(room=self.room, content="Hello, world!")

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, world!")


class ChatConsumerTest(TestCase):
    async def test_chat_consumer(self):
        communicator = WebsocketCommunicator(application, "/ws/chat/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Send a message
        user_message = "Hello, bot!"
        await communicator.send_json_to({"message": user_message})

        # Receive echo response
        response = await communicator.receive_json_from()
        self.assertEqual(response, {"type": "user", "message": user_message})

        # Receive bot response
        bot_response = await communicator.receive_json_from()
        self.assertEqual(bot_response["type"], "bot")
        self.assertIn("message", bot_response)

        await communicator.disconnect()
