# Surprise Telegram Selfie Bot 🎭

A Telegram bot that transforms selfies into hilarious, ridiculous styles using OpenAI's DALL-E API. The bot accepts selfies, applies a random funny transformation, and sends back the original and edited images side by side.

## Features

- 🔐 **Phone Number Authorization**: Only authorized phone numbers can use the bot
- 🎨 **20 Funny Styles**: Random selection from styles like Renaissance painting, 80s glamour shot, medieval knight, cyberpunk, and more
- 🖼️ **Side-by-Side Comparison**: See the original and transformed image together
- 🤖 **Easy to Use**: Just send a selfie and get instant results
- ✨ **Powered by DALL-E 3**: High-quality AI-generated transformations

## Setup

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- OpenAI API Key (from [OpenAI Platform](https://platform.openai.com/))

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
OPENAI_API_KEY=your_openai_api_key_here
```

**Important**: Add phone numbers with country codes (e.g., `+1234567890`). Separate multiple numbers with commas.

### Creating a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the instructions
3. Choose a name and username for your bot
4. Copy the bot token provided by BotFather
5. Paste it in your `.env` file as `TELEGRAM_BOT_TOKEN`

### Getting an OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy it and paste in your `.env` file as `OPENAI_API_KEY`

**Note**: Using DALL-E 3 costs money. Check [OpenAI's pricing](https://openai.com/pricing) for current rates.

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
2. **Authorize**: Send `/authorize` and follow instructions to share your phone number
3. **Send a selfie**: Once authorized, send any photo
4. **Wait**: The bot will process your image (takes 10-30 seconds)
5. **Enjoy**: Receive your transformed selfie side-by-side with the original!

### Commands

- `/start` - Welcome message and introduction
- `/authorize` - Get authorization instructions
- `/help` - Show help and usage information

## Configuration

### Customizing Funny Styles

Edit the `FUNNY_STYLES` list in `config.py` to add or modify transformation styles:

```python
FUNNY_STYLES = [
    "as a Renaissance oil painting with dramatic lighting",
    "as a 1980s glamour shot with neon colors",
    # Add your own styles here!
]
```

## Project Structure

```
surprise_telegram_bot/
├── bot.py              # Main bot implementation
├── config.py           # Configuration and styles
├── openai_service.py   # OpenAI API integration
├── image_utils.py      # Image processing utilities
├── pyproject.toml      # Poetry dependencies and project config
├── poetry.lock         # Locked dependency versions
├── env.example         # Example environment variables
└── README.md          # This file
```

## How It Works

1. **Authorization**: Users share their phone number, which is checked against the authorized list
2. **Image Reception**: When a user sends a photo, the bot downloads it
3. **Style Selection**: A random funny style is chosen from the configured list
4. **AI Transformation**: The image and style are sent to OpenAI's DALL-E 3 API
5. **Image Combination**: The original and transformed images are combined side-by-side
6. **Response**: The combined image is sent back to the user

## Cost Considerations

- **DALL-E 3**: ~$0.04 per image (1024x1024, standard quality)
- **Telegram Bot**: Free
- **Hosting**: Depends on your hosting solution

Consider implementing rate limiting or usage quotas if you expect high usage.

## Troubleshooting

### Bot doesn't respond
- Check that your `TELEGRAM_BOT_TOKEN` is correct
- Ensure the bot is running (`python bot.py`)
- Check the console for error messages

### Authorization fails
- Verify phone numbers in `.env` include country codes with `+`
- Make sure you're sharing YOUR contact, not someone else's
- Check that the phone number format matches exactly

### Image processing fails
- Verify your `OPENAI_API_KEY` is valid and has credits
- Check your OpenAI account for API usage limits
- Ensure you have a stable internet connection

### Images look wrong
- DALL-E 3 generates new images based on prompts, not direct edits
- Results may vary - the AI interprets the style creatively
- Try different photos or wait for different random styles

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secret
- Regularly rotate your API keys
- Monitor your OpenAI usage to prevent unexpected charges
- Only share the bot with trusted users

## License

MIT License - feel free to modify and use as you wish!

## Contributing

Contributions are welcome! Feel free to:
- Add new funny styles
- Improve image processing
- Add new features
- Fix bugs
- Improve documentation

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the logs in the console
3. Verify your configuration in `.env`
4. Check OpenAI and Telegram API status

Enjoy transforming your selfies! 🎭✨

