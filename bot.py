"""Main Telegram bot implementation."""
import logging
import io
import random
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from config import TELEGRAM_BOT_TOKEN
from gemini_service import GeminiService
from image_utils import combine_images_side_by_side
from user_storage import UserStorage
from image_storage import ImageStorage

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Gemini service
gemini_service = GeminiService()

# Initialize user storage
user_storage = UserStorage()

# Initialize image storage
image_storage = ImageStorage()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    user_id = user.id
    
    # Initialize authorized_users set if it doesn't exist
    if 'authorized_users' not in context.bot_data:
        context.bot_data['authorized_users'] = user_storage.load_users()
    
    # Check if this is a new user
    is_new = user_id not in context.bot_data['authorized_users']
    
    # Automatically authorize the user and save to storage
    context.bot_data['authorized_users'] = user_storage.add_user(
        user_id, 
        context.bot_data['authorized_users']
    )
    
    if is_new:
        await update.message.reply_text(
            f"Hi {user.first_name}! 👋\n\n"
            "Welcome to the Surprise Selfie Bot! 🎭\n\n"
            "Send me a selfie and I'll transform it into something hilariously unexpected! 🎨✨\n\n"
            "Your transformed selfie will be sent to a random user (or back to you if you're the only one).\n\n"
            "Just send me a photo to get started! 📸",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            f"Welcome back, {user.first_name}! 👋\n\n"
            "Ready to create some surprises? Send me a selfie! 📸",
            reply_markup=ReplyKeyboardRemove()
        )
    
    logger.info(f"User {user_id} ({user.first_name}) started the bot")




async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle received photos."""
    user_id = update.effective_user.id
    
    # Initialize authorized_users set if it doesn't exist
    if 'authorized_users' not in context.bot_data:
        context.bot_data['authorized_users'] = user_storage.load_users()
    
    # Auto-authorize user if not already authorized
    if user_id not in context.bot_data['authorized_users']:
        context.bot_data['authorized_users'] = user_storage.add_user(
            user_id,
            context.bot_data['authorized_users']
        )
        logger.info(f"Auto-authorized user {user_id} on photo upload")
    
    try:
        # Send processing message
        processing_msg = await update.message.reply_text(
            "🎨 Processing your selfie... This might take a moment!\n"
            "Preparing something ridiculous... 😄"
        )
        
        # Get the photo file
        photo = update.message.photo[-1]  # Get highest resolution
        photo_file = await photo.get_file()
        
        # Download the photo
        photo_bytes = await photo_file.download_as_bytearray()
        photo_bytes = bytes(photo_bytes)
        
        # Get a random style
        style = gemini_service.get_random_style()
        
        await processing_msg.edit_text(
            f"🎨 Transforming your selfie...\n\n"
            "This may take 10-30 seconds... ⏳"
        )
        
        # Edit the image using Gemini
        edited_image, used_style = gemini_service.edit_image(photo_bytes, style)
        
        # Combine images side by side
        combined_bytes = combine_images_side_by_side(photo_bytes, edited_image.image_bytes)
        
        # Delete processing message
        await processing_msg.delete()
        
        # Get all authorized users except the sender
        authorized_users = context.bot_data.get('authorized_users', set())
        other_users = [uid for uid in authorized_users if uid != user_id]
        
        if other_users:
            # Pick a random authorized user to send the photo to
            random_user_id = random.choice(other_users)
            
            # Save the generated image to storage
            image_storage.save_image(
                combined_bytes,
                sender_id=user_id,
                receiver_id=random_user_id,
                style=used_style,
                image_type="combined"
            )
            
            try:
                # Send to the random user
                await context.bot.send_photo(
                    chat_id=random_user_id,
                    photo=io.BytesIO(combined_bytes),
                    caption=f"🎁 Surprise! A friend sent you a transformed selfie! 🎭"
                )
                
                # Confirm to the sender
                await update.message.reply_photo(
                    photo=io.BytesIO(combined_bytes),
                    caption="✨ Here us your transformation!\n\n"
                            "It was sent to a random friend! 🎭"
                )
                logger.info(f"Sent transformed image from user {user_id} to user {random_user_id}")
                
            except Exception as send_error:
                logger.error(f"Failed to send to user {random_user_id}: {send_error}")
                # If sending fails, send back to the original user
                await update.message.reply_photo(
                    photo=io.BytesIO(combined_bytes),
                    caption="✨ Your transformation!\n\n"
                            "(Couldn't send to a friend, so here it is!) 🎭"
                )
        else:
            # No other users, send back to sender
            # Save the image with sender as receiver
            image_storage.save_image(
                combined_bytes,
                sender_id=user_id,
                receiver_id=user_id,
                style=used_style,
                image_type="combined"
            )
            
            await update.message.reply_photo(
                photo=io.BytesIO(combined_bytes),
                caption="✨ Your transformation!\n\n"
                        "(You're the only authorized user, so no one to surprise yet!) 🎭"
            )
        
        logger.info(f"Successfully processed image for user {user_id} with style: {style}")
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        await update.message.reply_text(
            "😅 Oops! Something went wrong while processing your selfie.\n\n"
            f"Error: {str(e)}\n\n"
            "Please try again or contact the administrator if the problem persists."
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "🤖 Surprise Selfie Bot - Help\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/stats - View bot statistics\n"
        "/help - Show this help message\n\n"
        "How to use:\n"
        "1. Send a selfie (photo)\n"
        "2. Wait for the magic to happen! ✨\n"
        "3. Your transformed selfie will be sent to a random user!\n\n"
        "The bot will randomly select a funny style and transform your selfie "
        "into something hilarious, then surprise a random user with it! 🎭",
        reply_markup=ReplyKeyboardRemove()
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send statistics about the bot."""
    stats = image_storage.get_stats()
    
    # Get number of authorized users
    authorized_users = context.bot_data.get('authorized_users', set())
    num_users = len(authorized_users)
    
    await update.message.reply_text(
        "📊 Bot Statistics\n\n"
        f"👥 Total Users: {num_users}\n"
        f"🖼️ Images Generated: {stats['total_images']}\n"
        f"📤 Unique Senders: {stats['unique_senders']}\n"
        f"📥 Unique Receivers: {stats['unique_receivers']}\n\n"
        "All generated images are saved locally! 💾",
        reply_markup=ReplyKeyboardRemove()
    )


async def post_init(application: Application) -> None:
    """Initialize bot data after application is created."""
    # Load authorized users from storage
    authorized_users = user_storage.load_users()
    application.bot_data['authorized_users'] = authorized_users
    logger.info(f"Loaded {len(authorized_users)} authorized users from storage")


def main() -> None:
    """Start the bot."""
    # Validate configuration
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables")
    
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # Start the Bot
    logger.info("Bot started successfully!")
    logger.info("Open registration - anyone can use the bot!")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

