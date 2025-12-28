# Screenshots Directory

This directory contains screenshots for the project README.

## Required Screenshots

1. **chat-interface.png** - Main chat interface showing:
   - Multiple messages exchanged
   - Message timestamps
   - Send button and input field
   - Clean, modern UI

2. **admin-dashboard.png** - Django admin interface showing:
   - List of rooms or messages
   - Admin navigation
   - Search/filter capabilities

## How to Take Screenshots

### Option 1: Using Browser DevTools
1. Run the development server:
   ```bash
   python manage.py runserver
   ```

2. Navigate to http://localhost:8000/

3. Send a few test messages to populate the chat

4. Use browser screenshot tools:
   - **Chrome/Edge**: Press F12 → Click device icon → Click "..." → "Capture screenshot"
   - **Firefox**: Press F12 → Click "..." → "Take a screenshot"
   - **Safari**: Develop → Show Web Inspector → (requires enabling developer tools)

5. For admin screenshot:
   - Create a superuser if you haven't: `python manage.py createsuperuser`
   - Navigate to http://localhost:8000/admin/
   - Log in and navigate to Chat → Messages or Rooms
   - Take a screenshot

### Option 2: Using Screenshot Tools
- **Linux**: GNOME Screenshot, Flameshot, or Spectacle
- **macOS**: Cmd+Shift+4 for selection
- **Windows**: Snipping Tool or Win+Shift+S

### Tips for Great Screenshots
- Use a clean browser window (close unnecessary tabs/bookmarks bar)
- Zoom to 100% for clarity
- Include some sample conversations (3-5 messages)
- Show the typing indicator if possible (type but don't send)
- Crop to show just the relevant content
- Save as PNG for best quality

## After Taking Screenshots
Save your screenshots here with the exact filenames referenced in the main README:
- `chat-interface.png`
- `admin-dashboard.png`
- `typing-indicator.png` (optional)
