# Setting Up Gemini API for StrokeShield Chatbot

## Quick Setup

### Option 1: Using API Key Directly (Easiest)

1. **Get your Gemini API Key**:
   - Go to https://aistudio.google.com/app/apikey
   - Click "Create API key"
   - Copy the API key

2. **Set the environment variable** (Windows PowerShell):
   ```powershell
   $env:GOOGLE_GENAI_API_KEY="your-api-key-here"
   ```

3. **Restart the server**:
   ```powershell
   python app.py
   ```

### Option 2: Using .env File (Recommended for Production)

1. Create a file named `.env` in your project root:
   ```
   GOOGLE_GENAI_API_KEY=your-api-key-here
   ```

2. Install python-dotenv:
   ```powershell
   pip install python-dotenv
   ```

3. The app will automatically load the API key from `.env`

## Verification

Once set up, you should see in the terminal:
```
Gemini API client initialized successfully
```

## Testing the Chatbot

1. Navigate to http://localhost:5000/chatbot
2. Ask stroke-related questions like:
   - "What are the warning signs of a stroke?"
   - "How can I prevent a stroke?"
   - "What is the FAST acronym?"
   - "What are the risk factors for stroke?"

## Features

✅ **AI-Powered**: Uses Gemini 2.0 Flash for intelligent responses
✅ **Stroke-Specialized**: System prompt optimized for stroke awareness
✅ **Professional UI**: Matches your website's teal/cyan theme
✅ **Dark Mode**: Full dark mode support
✅ **Dedicated Page**: Separate from assessment at `/chatbot`
✅ **Smart Context**: Emphasizes F.A.S.T., emergency care, disclaimers

## Troubleshooting

### "Error initializing Gemini client"
- Make sure you've set the `GOOGLE_GENAI_API_KEY` environment variable
- Verify the API key is correct
- Restart your terminal/PowerShell and server

### "AI service not available"
- The API key wasn't set correctly
- Follow Option 1 above to set it quickly

## API Key Security

⚠️ **IMPORTANT**: Never commit your API key to version control
- Add `.env` to your `.gitignore` file
- Use environment variables in production
