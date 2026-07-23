import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token from environment variable
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN environment variable is not set!")
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when /start is issued."""
    await update.message.reply_text(
        f"Hi {update.effective_user.first_name}! 🎉\n\n"
        "I'm Nexora3Bot! I'm alive and running on Railway!\n\n"
        "Commands:\n"
        "/start - Welcome message\n"
        "/help - Show help\n"
        "/ping - Check if bot is alive"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message."""
    await update.message.reply_text(
        "🤖 **Nexora3Bot Help**\n\n"
        "Here are all my commands:\n\n"
        "📝 **Text Tools**\n"
        "/wordcount [text] - Count words and characters\n"
        "/plagiarism [text] - Check for plagiarism\n"
        "/translate [text] to [lang] - Translate text\n\n"
        "🔗 **Link Tools**\n"
        "/shorten [url] - Shorten a URL\n\n"
        "🖼️ **Image Tools**\n"
        "/convert - Convert image format\n"
        "/compress - Compress image\n\n"
        "ℹ️ **Info**\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/ping - Check if bot is alive\n"
        "/about - About this bot",
        parse_mode='Markdown'
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check if bot is alive."""
    await update.message.reply_text("🏓 Pong! I'm alive and well!")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send about message."""
    await update.message.reply_text(
        "⚡ **Nexora3Bot v2.0**\n\n"
        "Deployed on Railway\n"
        "Built with Python and python-telegram-bot\n\n"
        "All features are free! 🎉",
        parse_mode='Markdown'
    )

async def wordcount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Count words in text."""
    if not context.args:
        await update.message.reply_text(
            "Please provide text to count.\n"
            "Example: /wordcount Hello world!"
        )
        return
    
    text = ' '.join(context.args)
    words = len(text.split())
    chars = len(text)
    
    await update.message.reply_text(
        f"📝 **Text Statistics**\n\n"
        f"Words: {words}\n"
        f"Characters: {chars}\n\n"
        f"Text: {text}",
        parse_mode='Markdown'
    )

def main() -> None:
    """Start the bot."""
    try:
        # Create the Application
        application = Application.builder().token(TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("ping", ping))
        application.add_handler(CommandHandler("about", about))
        application.add_handler(CommandHandler("wordcount", wordcount))

        # Start the Bot
        logger.info("🤖 Nexora3Bot is starting...")
        logger.info(f"Bot Token: {TOKEN[:15]}...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == '__main__':
    main()
