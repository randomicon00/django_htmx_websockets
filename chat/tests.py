from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Room, Message
from channels.testing import WebsocketCommunicator
from websocket_demo.asgi import application
import asyncio


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
        self.user = User.objects.create_user(username="testuser", email="test@example.com")
        self.message = Message.objects.create(room=self.room, user=self.user, content="Hello, world!")

    def test_message_str(self):
        self.assertIn("Message by testuser in Test Room", str(self.message))
        self.assertIn("Hello, world!", str(self.message))

    def test_message_repr(self):
        self.assertIn("<Message(user='testuser', room='Test Room'", repr(self.message))
        self.assertIn("content_preview='Hello, world!'", repr(self.message))

    def test_read_at_initially_none(self):
        """Test that read_at is None when message is first created"""
        self.assertIsNone(self.message.read_at)

    def test_mark_as_read(self):
        """Test that read_at is set when message is marked as read"""
        before_time = timezone.now()
        self.message.read_at = timezone.now()
        self.message.save()

        self.message.refresh_from_db()
        self.assertIsNotNone(self.message.read_at)
        self.assertGreaterEqual(self.message.read_at, before_time)

    def test_read_status_filtering(self):
        """Test filtering messages by read status"""
        # Create another message
        message2 = Message.objects.create(room=self.room, user=self.user, content="Second message")

        # Initially no messages are read
        unread_messages = Message.objects.filter(read_at__isnull=True)
        self.assertEqual(unread_messages.count(), 2)

        # Mark first message as read
        self.message.read_at = timezone.now()
        self.message.save()

        # Now one message is read, one is unread
        read_messages = Message.objects.filter(read_at__isnull=False)
        unread_messages = Message.objects.filter(read_at__isnull=True)

        self.assertEqual(read_messages.count(), 1)
        self.assertEqual(unread_messages.count(), 1)
        self.assertIn(self.message, read_messages)
        self.assertIn(message2, unread_messages)


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
    def setUp(self):
        self.user = User.objects.create_user(username="demo_user", email="demo@example.com")
        self.room = Room.objects.create(name="General Chat", description="General discussion room")

    async def test_chat_consumer_message_persistence_and_read_status(self):
        """Test that messages are saved to database and marked as read"""
        communicator = WebsocketCommunicator(application, "/ws/chat/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Initially no messages in database
        initial_count = await Message.objects.acount()
        self.assertEqual(initial_count, 0)

        # Send a message
        user_message = "Hello, bot!"
        await communicator.send_json_to({"message": user_message})

        # Receive user message response (should include id and timestamp)
        user_response = await communicator.receive_json_from()
        self.assertEqual(user_response["type"], "user")
        self.assertEqual(user_response["message"], user_message)
        self.assertIn("id", user_response)
        self.assertIn("timestamp", user_response)

        # Receive bot response (should include id and timestamp)
        bot_response = await communicator.receive_json_from()
        self.assertEqual(bot_response["type"], "bot")
        self.assertIn("message", bot_response)
        self.assertIn("id", bot_response)
        self.assertIn("timestamp", bot_response)

        # Check that messages were saved to database
        final_count = await Message.objects.acount()
        self.assertEqual(final_count, 2)  # user message + bot message

        # Check that messages are marked as read
        messages = [msg async for msg in Message.objects.all()]
        for message in messages:
            self.assertIsNotNone(message.read_at, f"Message {message.id} should be marked as read")

        await communicator.disconnect()

    async def test_empty_message_not_saved(self):
        """Test that empty messages are not saved to database"""
        communicator = WebsocketCommunicator(application, "/ws/chat/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        initial_count = await Message.objects.acount()

        # Send empty message
        await communicator.send_json_to({"message": ""})

        # Should not receive any response for empty message
        # Wait a bit to ensure no message is processed
        await asyncio.sleep(0.1)

        final_count = await Message.objects.acount()
        self.assertEqual(final_count, initial_count)  # No new messages

        await communicator.disconnect()
