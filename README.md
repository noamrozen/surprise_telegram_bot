# Surprise Telegram Selfie Bot 🎭

A Telegram bot that transforms selfies into hilarious, ridiculous styles using Google Gemini's image generation API. The bot accepts selfies, applies a random funny transformation, and sends the result to a random user for a surprise!

## Features

- 🎨 **70+ Funny Styles**: Random selection from styles like Renaissance painting, 80s glamour shot, medieval knight, cyberpunk, disco dancer, literal couch potato, and many more ridiculous transformations
- 🎁 **Surprise Delivery**: Transformed selfies are sent to random users (not back to the sender)
- 🖼️ **Side-by-Side Comparison**: See the original and transformed image together
- 🔓 **Open Registration**: Anyone can use the bot - users are automatically authorized on first use
- 💾 **Persistent Storage**: All generated images and user data are saved locally
- 📊 **Statistics**: Track total images, users, and bot activity
- ✨ **Powered by Google Gemini**: High-quality AI-generated transformations using Imagen

## Setup

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Google API Key with Gemini API access (from [Google AI Studio](https://aistudio.google.com/))

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd surprise_telegram_bot
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create a `.env` file based on `env.example`:
```bash
cp env.example .env
```

4. Edit `.env` and add your credentials:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GOOGLE_API_KEY=your_google_api_key_here
```

### Creating a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the instructions
3. Choose a name and username for your bot
4. Copy the bot token provided by BotFather
5. Paste it in your `.env` file as `TELEGRAM_BOT_TOKEN`

### Getting a Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" in the left sidebar
4. Create a new API key or use an existing one
5. Copy it and paste in your `.env` file as `GOOGLE_API_KEY`

**Note**: Google Gemini API has free tier limits. Check [Google's pricing](https://ai.google.dev/pricing) for current rates and quotas.

## Usage

### Running the Bot

```bash
poetry run python bot.py
```

Or activate the Poetry shell first:

```bash
poetry shell
python bot.py
```

The bot will start and wait for messages.

### Using the Bot

1. **Start the bot**: Send `/start` to your bot on Telegram
2. **Send a selfie**: Once started, send any photo
3. **Wait**: The bot will process your image (takes 10-30 seconds)
4. **Surprise**: Your transformed selfie will be sent to a random user, and you'll get a copy too!

### Commands

- `/start` - Start the bot and get automatically authorized
- `/help` - Show help and usage information
- `/stats` - View bot statistics (total users, images generated, etc.)

## Configuration

### Customizing Funny Styles

Edit the `FUNNY_STYLES` list in `config.py` to add or modify transformation styles. The bot currently includes 70+ styles ranging from classic (Renaissance painting, Victorian aristocrat) to absurd (literal couch potato, potato ninja, sushi roll conductor).

```python
FUNNY_STYLES = [
    "as a Renaissance oil painting with dramatic lighting",
    "as a 1980s glamour shot with neon colors",
    "as a literal couch potato binging TV shows",
    # Add your own styles here!
]
```

## Project Structure

```
surprise_telegram_bot/
├── bot.py                    # Main bot implementation
├── config.py                 # Configuration and styles
├── gemini_service.py         # Google Gemini API integration
├── image_utils.py            # Image processing utilities
├── user_storage.py           # User persistence
├── image_storage.py          # Image and metadata storage
├── pyproject.toml            # Poetry dependencies and project config
├── poetry.lock               # Locked dependency versions
├── env.example               # Example environment variables
├── authorized_users.json     # Stored authorized user IDs (auto-generated)
├── generated_images/         # Directory for saved images (auto-generated)
│   └── metadata.json         # Image metadata (auto-generated)
└── README.md                 # This file
```

## How It Works

1. **Auto-Authorization**: When a user sends `/start` or a photo, they are automatically authorized and saved to `authorized_users.json`
2. **Image Reception**: When a user sends a photo, the bot downloads it
3. **Style Selection**: A random funny style is chosen from the configured list (70+ options)
4. **AI Transformation**: The image and style are sent to Google Gemini's image generation API
5. **Image Combination**: The original and transformed images are combined side-by-side
6. **Surprise Delivery**: The combined image is sent to a random authorized user (not the sender)
7. **Confirmation**: The sender also receives a copy of the transformation
8. **Persistent Storage**: All images are saved to `generated_images/` with metadata

## Storage

### User Storage
- Users are automatically saved to `authorized_users.json` on first interaction
- Persists across bot restarts
- No manual authorization needed

### Image Storage
- All generated images are saved to `generated_images/` directory
- Filenames include timestamp, sender ID, receiver ID, and image type
- Metadata is stored in `generated_images/metadata.json` with:
  - Timestamp
  - Sender and receiver IDs
  - Style applied
  - Image type

## Cost Considerations

- **Google Gemini API**: Free tier available with rate limits
- **Telegram Bot**: Free
- **Hosting**: Depends on your hosting solution

Consider implementing additional rate limiting if you expect very high usage.

## Troubleshooting

### Bot doesn't respond
- Check that your `TELEGRAM_BOT_TOKEN` is correct
- Ensure the bot is running (`poetry run python bot.py`)
- Check the console for error messages

### Image processing fails
- Verify your `GOOGLE_API_KEY` is valid
- Check your Google Cloud project has Gemini API enabled
- Ensure you haven't exceeded API rate limits
- Check you have a stable internet connection

### Images look wrong
- Gemini generates new images based on prompts and reference images
- Results may vary - the AI interprets the style creatively
- Try different photos or wait for different random styles

### Storage issues
- Ensure the bot has write permissions in its directory
- Check disk space for image storage
- `authorized_users.json` and `generated_images/` are created automatically

## Security Notes

- Never commit your `.env` file to version control (already in `.gitignore`)
- Keep your API keys secret
- Regularly rotate your API keys
- Monitor your Google API usage to prevent unexpected charges
- The bot is open to anyone who finds it - consider adding rate limiting for production use

## Statistics

Use the `/stats` command to view:
- Total number of users
- Total images generated
- Unique senders
- Unique receivers

All data is stored locally and persists across restarts.

## License

MIT License - feel free to modify and use as you wish!

## Contributing

Contributions are welcome! Feel free to:
- Add new funny styles
- Improve image processing
- Add new features (rate limiting, user preferences, etc.)
- Fix bugs
- Improve documentation

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the logs in the console
3. Verify your configuration in `.env`
4. Check Google Gemini API status and quotas
5. Ensure you have the latest dependencies (`poetry install`)

Enjoy surprising your friends with hilarious transformations! 🎭✨
