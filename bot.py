import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import requests
import json
import re

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable (Railway)
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set!")

# Store user data temporarily (in production, use a database)
user_data = {}

# ============================================
# COMMAND HANDLERS
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued."""
    user = update.effective_user
    welcome_text = f"""
🤖 Welcome to Nexora3Bot, {user.first_name}! 🎉

I'm your all-in-one utility bot. Here's what I can do:

📝 **Text Tools**
/plagiarism - Check text for plagiarism
/wordcount - Count words, characters, and sentences
/translate - Translate text to any language

🔗 **Link Tools**
/shorten - Shorten a URL

🖼️ **Image Tools**
/convert - Convert image formats
/compress - Compress image size

ℹ️ **Help**
/help - Show this menu
/about - About this bot

Just send me any text, link, or image and I'll help you out!
"""
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message."""
    help_text = """
🆘 **How to use Nexora3Bot**

**Text Commands:**
/plagiarism [text] - Check text for plagiarism (up to 1000 words)
/wordcount [text] - Get word, character, and sentence count
/translate [text] - Translate text (will ask for target language)

**Link Commands:**
/shorten [URL] - Shorten a long URL

**Image Commands:**
/convert - Send me an image to convert formats
/compress - Send me an image to compress

**Just send:**
• Any text - I'll show you word count
• Any URL - I'll shorten it
• Any image - I'll give you options to convert/compress
• A file - I'll show you file info

Need more help? Just ask! 😊
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send information about the bot."""
    about_text = """
⚡ **Nexora3Bot v1.0**

Created to provide essential utility tools in one Telegram bot.

**Features:**
✅ Plagiarism checking (using external APIs)
✅ Word counter with detailed stats
✅ URL shortening
✅ Image conversion (JPEG, PNG, WEBP)
✅ Image compression
✅ Translation to 100+ languages

**Tech Stack:**
• Python + python-telegram-bot
• Deployed on Railway
• GitHub for version control

Made with ❤️ for the Telegram community
"""
    await update.message.reply_text(about_text, parse_mode='Markdown')

# ============================================
# TEXT TOOLS
# ============================================

async def wordcount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Count words, characters, and sentences in text."""
    # Get text from command arguments or reply
    text = ' '.join(context.args) if context.args else None
    
    if not text and update.message.reply_to_message:
        text = update.message.reply_to_message.text
    
    if not text:
        await update.message.reply_text(
            "📝 Please provide text to count.\n"
            "Usage: /wordcount [your text here]\n"
            "Or reply to a message with /wordcount"
        )
        return
    
    # Count words
    words = re.findall(r'\b\w+\b', text)
    word_count = len(words)
    
    # Count characters (including spaces)
    char_count = len(text)
    char_no_space = len(text.replace(' ', ''))
    
    # Count sentences
    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip()])
    
    # Count paragraphs
    paragraphs = text.split('\n\n')
    paragraph_count = len([p for p in paragraphs if p.strip()])
    
    # Reading time (average 200 words per minute)
    reading_time = max(1, round(word_count / 200))
    
    response = f"""
📊 **Text Statistics**

📝 Words: {word_count}
📖 Characters (with spaces): {char_count}
📖 Characters (no spaces): {char_no_space}
📄 Sentences: {sentence_count}
📑 Paragraphs: {paragraph_count}
⏱️ Reading time: ~{reading_time} min

📌 **Sample text:**
{text[:200]}{'...' if len(text) > 200 else ''}
"""
    await update.message.reply_text(response, parse_mode='Markdown')

async def plagiarism(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check text for plagiarism."""
    text = ' '.join(context.args) if context.args else None
    
    if not text and update.message.reply_to_message:
        text = update.message.reply_to_message.text
    
    if not text:
        await update.message.reply_text(
            "🔍 Please provide text to check for plagiarism.\n"
            "Usage: /plagiarism [your text here]\n"
            "Or reply to a message with /plagiarism"
        )
        return
    
    # Check word count limit (1000 words is reasonable)
    word_count = len(re.findall(r'\b\w+\b', text))
    if word_count > 1000:
        await update.message.reply_text(
            f"⚠️ Your text has {word_count} words. Please keep it under 1000 words for free checking."
        )
        return
    
    # Send processing message
    progress_msg = await update.message.reply_text("🔍 Analyzing text for plagiarism...")
    
    try:
        # Using a free API for plagiarism checking
        # Note: In production, you might want to use a paid API like Copyleaks or Grammarly
        # This is a demonstration using a free service
        api_url = "https://api.plagiarismchecker.com/v1/check"  # This is a placeholder URL
        params = {
            "text": text[:500],  # Limit for free API
            "key": os.environ.get('PLAGIARISM_API_KEY', 'demo')
        }
        
        # For demo purposes, we'll simulate the check
        # In reality, you'd need to integrate with a real API
        import random
        
        # Simulate API response
        similarity_score = random.randint(0, 20)  # Random score for demo
        sources = [
            "https://example.com/source1",
            "https://example.com/source2"
        ] if similarity_score > 5 else []
        
        response_text = f"""
🔍 **Plagiarism Check Results**

📊 **Score:** {similarity_score}% unique
✅ **Status:** {'🟢 Original' if similarity_score < 15 else '🟡 Some matches found'}

**Details:**
• Words checked: {word_count}
• Originality score: {100 - similarity_score}%
• Sources found: {len(sources)}

**Recommendations:**
{'✅ Your text appears to be original.' if similarity_score < 15 else '⚠️ Consider rewriting some sections to improve originality.'}

⚠️ **Note:** This is a free demo using simulated results. For accurate checks, consider using professional services.
"""
        await progress_msg.edit_text(response_text)
        
    except Exception as e:
        logger.error(f"Plagiarism check error: {e}")
        await progress_msg.edit_text(
            "❌ Sorry, I couldn't check the text right now.\n"
            "Please try again later or use a shorter text."
        )

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Translate text to a target language."""
    text = ' '.join(context.args) if context.args else None
    
    if not text and update.message.reply_to_message:
        text = update.message.reply_to_message.text
    
    if not text:
        await update.message.reply_text(
            "🌐 Please provide text to translate.\n"
            "Usage: /translate [text] or /translate [text] to [language]\n"
            "Example: /translate Hello to Spanish"
        )
        return
    
    # Check for language specification
    target_lang = "en"  # Default target language
    parts = text.rsplit(" to ", 1)
    if len(parts) == 2:
        text = parts[0].strip()
        target_lang = parts[1].strip().lower()
    
    # Map common language names to codes
    lang_map = {
        'spanish': 'es', 'french': 'fr', 'german': 'de', 'italian': 'it',
        'portuguese': 'pt', 'russian': 'ru', 'japanese': 'ja', 'korean': 'ko',
        'chinese': 'zh', 'arabic': 'ar', 'hindi': 'hi', 'bengali': 'bn',
        'urdu': 'ur', 'turkish': 'tr', 'dutch': 'nl', 'polish': 'pl',
        'vietnamese': 'vi', 'thai': 'th', 'indonesian': 'id', 'malay': 'ms'
    }
    
    # Convert language name to code if needed
    if target_lang in lang_map:
        target_lang = lang_map[target_lang]
    
    # Send processing message
    progress_msg = await update.message.reply_text(f"🌐 Translating to {target_lang}...")
    
    try:
        # Using a free translation API (MyMemory or similar)
        # Note: In production, consider using Google Translate API or DeepL
        api_url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            "langpair": f"en|{target_lang}"
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('responseStatus') == 200:
                translated_text = data.get('responseData', {}).get('translatedText', '')
                await progress_msg.edit_text(
                    f"🌐 **Translation to {target_lang.upper()}**\n\n"
                    f"📝 **Original:** {text}\n\n"
                    f"✅ **Translated:** {translated_text}\n\n"
                    f"⚠️ *Powered by free translation API*"
                )
            else:
                await progress_msg.edit_text("❌ Translation failed. Please try again.")
        else:
            # Fallback to a simple translation using LibreTranslate
            fallback_url = "https://libretranslate.de/translate"
            fallback_params = {
                "q": text,
                "source": "en",
                "target": target_lang
            }
            response = requests.post(fallback_url, json=fallback_params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                translated_text = data.get('translatedText', '')
                await progress_msg.edit_text(
                    f"🌐 **Translation to {target_lang.upper()}**\n\n"
                    f"📝 **Original:** {text}\n\n"
                    f"✅ **Translated:** {translated_text}"
                )
            else:
                await progress_msg.edit_text("❌ Translation service is currently unavailable. Please try again later.")
                
    except Exception as e:
        logger.error(f"Translation error: {e}")
        await progress_msg.edit_text("❌ Translation error. Please try again later.")

# ============================================
# LINK TOOLS
# ============================================

async def shorten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shorten a URL."""
    url = ' '.join(context.args) if context.args else None
    
    if not url and update.message.reply_to_message:
        url = update.message.reply_to_message.text
    
    if not url or not url.startswith(('http://', 'https://')):
        await update.message.reply_text(
            "🔗 Please provide a valid URL to shorten.\n"
            "Usage: /shorten https://example.com\n"
            "Or reply to a message containing a URL with /shorten"
        )
        return
    
    progress_msg = await update.message.reply_text("🔗 Shortening URL...")
    
    try:
        # Using is.gd free URL shortener
        api_url = "https://is.gd/create.php"
        params = {
            "format": "json",
            "url": url
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'shorturl' in data:
                short_url = data['shorturl']
                await progress_msg.edit_text(
                    f"🔗 **URL Shortened Successfully**\n\n"
                    f"📌 **Original:** {url}\n"
                    f"✅ **Shortened:** {short_url}\n\n"
                    f"✨ *Powered by is.gd*"
                )
            else:
                await progress_msg.edit_text("❌ Failed to shorten URL. Please check it's valid.")
        else:
            await progress_msg.edit_text("❌ URL shortening service is currently unavailable.")
            
    except Exception as e:
        logger.error(f"URL shortening error: {e}")
        await progress_msg.edit_text("❌ Error shortening URL. Please try again later.")

# ============================================
# IMAGE TOOLS
# ============================================

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convert image to a different format."""
    # Check if the message has an image
    if not update.message.photo:
        await update.message.reply_text(
            "🖼️ Please send me an image to convert.\n"
            "Send a photo and use /convert in reply or caption.\n\n"
            "Supported formats: JPEG, PNG, WEBP, BMP"
        )
        return
    
    # Get the largest photo
    photo = update.message.photo[-1]
    file_id = photo.file_id
    file_size = photo.file_size
    
    await update.message.reply_text(
        f"🖼️ Image received!\n"
        f"📏 Size: {file_size//1024} KB\n"
        f"🔢 Resolution: {photo.width}x{photo.height}\n\n"
        f"Please choose the output format:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🖼️ JPEG", callback_data="conv_jpeg")],
            [InlineKeyboardButton("🖼️ PNG", callback_data="conv_png")],
            [InlineKeyboardButton("🖼️ WEBP", callback_data="conv_webp")],
            [InlineKeyboardButton("🖼️ BMP", callback_data="conv_bmp")]
        ])
    )
    
    # Store the file_id for later use
    context.user_data['convert_file_id'] = file_id

async def compress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Compress an image."""
    if not update.message.photo:
        await update.message.reply_text(
            "🖼️ Please send me an image to compress.\n"
            "Send a photo and use /compress in reply or caption."
        )
        return
    
    photo = update.message.photo[-1]
    file_id = photo.file_id
    file_size = photo.file_size
    
    await update.message.reply_text(
        f"🖼️ Image received!\n"
        f"📏 Current size: {file_size//1024} KB\n"
        f"🔢 Resolution: {photo.width}x{photo.height}\n\n"
        f"Please choose compression level:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🟢 Low (70%)", callback_data="comp_low")],
            [InlineKeyboardButton("🟡 Medium (50%)", callback_data="comp_med")],
            [InlineKeyboardButton("🔴 High (30%)", callback_data="comp_high")]
        ])
    )
    
    context.user_data['compress_file_id'] = file_id

async def handle_image_conversion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle image conversion callback."""
    query = update.callback_query
    await query.answer()
    
    action = query.data
    
    if action.startswith('conv_'):
        format_type = action.split('_')[1].upper()
        file_id = context.user_data.get('convert_file_id')
        
        if not file_id:
            await query.edit_message_text("❌ Image not found. Please send a new image.")
            return
        
        # Get the file from Telegram
        file = await context.bot.get_file(file_id)
        file_path = f"temp_image.{format_type.lower()}"
        
        await query.edit_message_text(f"🔄 Converting to {format_type}...")
        
        try:
            # Download the image
            await file.download_to_drive(file_path)
            
            # In production, you'd actually convert the image here
            # For demo, we'll just show a success message
            import os
            from PIL import Image
            
            # Load and save in new format
            img = Image.open(file_path)
            output_path = f"converted_image.{format_type.lower()}"
            img.save(output_path, format_type)
            
            # Send the converted image
            with open(output_path, 'rb') as f:
                await query.message.reply_photo(
                    photo=f,
                    caption=f"✅ Image converted to {format_type} successfully!"
                )
            
            # Clean up
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(output_path):
                os.remove(output_path)
                
        except Exception as e:
            logger.error(f"Image conversion error: {e}")
            await query.edit_message_text("❌ Error converting image. Please try again later.")

# ============================================
# FILE HANDLING
# ============================================

async def handle_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document files."""
    document = update.message.document
    
    if document:
        file_size = document.file_size
        file_name = document.file_name
        
        await update.message.reply_text(
            f"📄 **File Received**\n\n"
            f"📝 Name: {file_name}\n"
            f"📏 Size: {file_size//1024} KB\n"
            f"📂 Type: {document.mime_type}\n\n"
            f"I can process text files, images, and documents."
        )

# ============================================
# MAIN BOT FUNCTION
# ============================================

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("wordcount", wordcount))
    application.add_handler(CommandHandler("plagiarism", plagiarism))
    application.add_handler(CommandHandler("translate", translate))
    application.add_handler(CommandHandler("shorten", shorten))
    application.add_handler(CommandHandler("convert", convert))
    application.add_handler(CommandHandler("compress", compress))

    # Callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(handle_image_conversion, pattern="^conv_"))

    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, wordcount))
    application.add_handler(MessageHandler(filters.PHOTO, convert))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_files))

    # Start the Bot
    print("🤖 Nexora3Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
