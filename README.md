# Django HTMX WebSockets Chat

![Django CI](https://github.com/YOUR_USERNAME/django_htmx_websockets/workflows/Django%20CI/badge.svg)

A real-time chat application demonstrating modern web technologies: Django Channels for WebSocket support, HTMX for dynamic frontend interactions, and Tailwind CSS for styling. Built as a portfolio project showcasing full-stack development skills.

## Screenshots

### Chat Interface
![Chat Interface](docs/screenshots/chat-interface.png)
*Real-time messaging with typing indicators and auto-scroll*

### Admin Dashboard
![Admin Dashboard](docs/screenshots/admin-dashboard.png)
*Django admin interface for managing rooms and messages*

> **Note**: To add screenshots, run the application locally and capture images:
> 1. Start the server: `python manage.py runserver`
> 2. Navigate to http://localhost:8000/
> 3. Take screenshots and save them to `docs/screenshots/`
> 4. Recommended screenshot names:
>    - `chat-interface.png` - Main chat interface with some messages
>    - `admin-dashboard.png` - Django admin page showing rooms/messages
>    - `typing-indicator.png` (optional) - Showing typing indicator in action

## Features

- **Real-time messaging** - Instant message delivery using WebSockets
- **Auto-bot responses** - Simulated conversation partner with typing indicators
- **Message persistence** - SQLite database stores chat history
- **Read receipts** - Track message read status
- **Accessible UI** - WCAG-compliant interface with ARIA labels
- **Responsive design** - Mobile-friendly layout with Tailwind CSS
- **Auto-scroll behavior** - Smart scrolling with manual scroll button
- **Typing indicators** - Visual feedback during message composition
- **Admin interface** - Django admin for managing rooms and messages

## Technology Stack

### Backend
- **Django 5.1.3** - Web framework
- **Django Channels 4.2.0** - WebSocket and async support
- **Python 3.12+** - Programming language
- **SQLite** - Database (easily swappable for PostgreSQL/MySQL)

### Frontend
- **HTMX** - Dynamic HTML updates via WebSockets
- **Tailwind CSS** - Utility-first CSS framework
- **Vanilla JavaScript** - Minimal custom scripting

### Architecture
- **ASGI** - Asynchronous server gateway interface
- **Async/await** - Non-blocking database operations
- **WebSocket protocol** - Bidirectional real-time communication

## Project Structure

```
django_htmx_websockets/
├── chat/                       # Main Django app
│   ├── migrations/             # Database migrations
│   ├── templates/chat/         # HTML templates
│   ├── admin.py               # Admin configuration
│   ├── consumers.py           # WebSocket consumer (async)
│   ├── models.py              # Room and Message models
│   ├── routing.py             # WebSocket URL routing
│   ├── tests.py               # Unit and integration tests
│   ├── urls.py                # HTTP URL routing
│   └── views.py               # HTTP views
├── websocket_demo/            # Django project settings
│   ├── asgi.py                # ASGI configuration
│   ├── settings.py            # Django settings
│   └── urls.py                # Project URL routing
├── static/                    # Static files (CSS)
├── manage.py                  # Django management script
├── .env.example               # Environment variables template
└── requirements.txt           # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Virtual environment tool (venv, virtualenv, or conda)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd django_htmx_websockets
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Linux/macOS
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and set your SECRET_KEY
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Open your browser**
   - Chat interface: http://localhost:8000/
   - Admin interface: http://localhost:8000/admin/

## Usage

### Chat Interface

1. Navigate to http://localhost:8000/
2. Type a message in the input field
3. Press Enter or click Send
4. Watch as the bot responds automatically
5. Scroll through message history

### Admin Interface

1. Log in at http://localhost:8000/admin/
2. Manage chat rooms and messages
3. View message timestamps and read status
4. Search and filter conversations

## Running Tests

The project includes comprehensive test coverage for models, views, and WebSocket consumers.

```bash
# Run all tests
python manage.py test

# Run tests with verbose output
python manage.py test --verbosity=2

# Run specific test module
python manage.py test chat.tests
```

## Key Features Explained

### WebSocket Consumer ([chat/consumers.py](chat/consumers.py))
- Async message handling with Django's async ORM
- Automatic message persistence to database
- Bot response simulation with typing delay
- Channel layers for broadcasting messages

### Models ([chat/models.py](chat/models.py))
- **Room** - Chat room with unique slug generation
- **Message** - Messages with content, timestamps, and read status
- Helper methods for retrieving recent messages
- Database indexes for query optimization

### Frontend ([chat/templates/chat/index.html](chat/templates/chat/index.html))
- HTMX WebSocket extension for real-time updates
- Accessible UI with proper ARIA labels
- Smart auto-scroll with manual override
- Character limit validation (1000 chars)

## Development

### Database Schema

**Room Model:**
- `name` - Display name for the room
- `slug` - URL-friendly unique identifier (auto-generated)

**Message Model:**
- `room` - Foreign key to Room
- `user` - Foreign key to User (Django auth)
- `content` - Message text (max 1000 characters)
- `timestamp` - Creation datetime
- `read_at` - Read receipt timestamp (nullable)

### WebSocket Message Format

Messages sent to the WebSocket endpoint should be JSON:
```json
{
  "message": "Your message text here"
}
```

### Environment Variables

See `.env.example` for required configuration:
- `SECRET_KEY` - Django secret key (required for production)
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

### Continuous Integration

This project uses GitHub Actions for automated testing. On every push and pull request:
- Runs full test suite with Django's test framework
- Checks for missing migrations
- Lints code with flake8 for syntax errors

See [.github/workflows/django-tests.yml](.github/workflows/django-tests.yml) for the full CI configuration.

**Note**: Update the GitHub Actions badge URL at the top of this README by replacing `YOUR_USERNAME` with your GitHub username.

## Future Enhancements

- [ ] User authentication and registration
- [ ] Multiple chat rooms
- [ ] Private messaging
- [ ] File/image uploads
- [ ] Message editing and deletion
- [ ] Online user indicators
- [ ] Message reactions
- [ ] Integration with AI chat APIs (OpenAI, Anthropic)

## License

This project is open source and available for educational purposes.

## Author

Created as a portfolio project to demonstrate:
- Full-stack web development
- Real-time communication with WebSockets
- Modern Python async/await patterns
- Django best practices
- Accessible frontend design
- Test-driven development

## Acknowledgments

- Django and Django Channels documentation
- HTMX for simplifying real-time interactions
- Tailwind CSS for rapid UI development
