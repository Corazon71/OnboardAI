# OnboardAI Frontend

A modern, dark-themed web interface for the OnboardAI assistant.

## Features

- 🎨 **Modern Dark Theme** - Sleek, professional design with gradient accents
- 💬 **Real-time Chat** - Interactive conversation with AI assistant
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile
- ⚡ **Live Typing Indicators** - Visual feedback when AI is responding
- 🔍 **Character Counter** - Track message length (1000 char limit)
- 🌐 **Connection Status** - Real-time server connectivity indicator
- ⌨️ **Keyboard Shortcuts** - Enhanced productivity with hotkeys
- 📝 **Source Attribution** - See where AI responses come from

## Quick Start

1. **Start the Backend API:**
   ```bash
   cd d:\OnboardAI
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Open the Frontend:**
   - Open `index.html` in your web browser
   - Or use a live server extension in your IDE

## Keyboard Shortcuts

- `Enter` - Send message
- `Shift + Enter` - New line in input
- `Ctrl/Cmd + K` - Clear chat history
- `Ctrl/Cmd + /` - Focus input field
- `Escape` - Close error modal

## Configuration

The frontend connects to the backend API at `http://localhost:8000` by default. To change this:

1. Open `script.js`
2. Update the `API_BASE_URL` constant:
   ```javascript
   const API_BASE_URL = 'your-api-url';
   ```

## Features in Detail

### Chat Interface
- **User Messages**: Displayed on the right with green avatar
- **Bot Messages**: Displayed on the left with blue avatar
- **Typing Indicator**: Animated dots when AI is processing
- **Smooth Animations**: Messages slide in with fade effects

### Error Handling
- **Connection Errors**: User-friendly error modal
- **Network Issues**: Automatic connection status checking
- **Input Validation**: Character limit enforcement

### Responsive Design
- **Desktop**: Full-width layout with optimal spacing
- **Mobile**: Compact design with touch-friendly controls
- **Tablet**: Adaptive layout for medium screens

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Development

To modify the frontend:

1. **Styles**: Edit `styles.css` for visual changes
2. **Functionality**: Edit `script.js` for behavior changes
3. **Structure**: Edit `index.html` for layout changes

### Color Scheme
- Primary Background: `#0a0a0a`
- Secondary Background: `#1a1a1a`
- Accent Color: `#00d4ff`
- Success Color: `#00ff88`
- Error Color: `#ff4757`

### Font Stack
- Primary: Inter (web font)
- Fallback: System fonts (SF Pro, Segoe UI, Roboto)

## Deployment

### Static Hosting
The frontend can be deployed on any static hosting service:
- Netlify
- Vercel
- GitHub Pages
- Firebase Hosting

### Configuration for Production
1. Update `API_BASE_URL` to your production backend URL
2. Ensure HTTPS is used for production APIs
3. Test CORS settings on the backend

## Security Notes

- Session IDs are stored in localStorage
- No sensitive data is stored in the browser
- All API calls are made over HTTP (use HTTPS in production)

## Troubleshooting

### Common Issues

1. **"Failed to connect" error**
   - Check if backend is running on port 8000
   - Verify CORS settings in the backend

2. **Messages not sending**
   - Check browser console for errors
   - Verify API endpoint is accessible

3. **Styling issues**
   - Clear browser cache
   - Check if CSS file is loading properly

### Debug Mode
To enable debug logging, add this to `script.js`:
```javascript
const DEBUG = true;
```

Then check the browser console for detailed logs.
