import os
import logging
import asyncio
from datetime import datetime
from openai import AsyncOpenAI
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import db

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Configuration
OPENROUTER_API_KEY = os.getenv("OpenRouter_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-8b-instruct")
MAX_HISTORY_MESSAGES = 20
MAX_MESSAGE_LENGTH = 4000  # Leave some room for safety

# Initialize AsyncOpenAI client
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


async def chat_with_gpt(prompt: str, user_id: int) -> str:
    """
    Get response from OpenRouter API with user history.
    Saves both user message and assistant response in a transaction.
    """
    # Save user message first (immediately)
    db.save_user_message(user_id, "user", prompt)

    # Retrieve conversation history
    try:
        user_history = db.get_user_history(user_id, limit=MAX_HISTORY_MESSAGES)
        messages = user_history + [{"role": "user", "content": prompt}]
    except Exception as e:
        logger.error(f"Error retrieving user history: {e}")
        messages = [{"role": "user", "content": prompt}]

    try:
        # Call OpenRouter asynchronously
        response = await client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=messages,
        )
        assistant_reply = response.choices[0].message.content

        # Save assistant response
        db.save_user_message(user_id, "assistant", assistant_reply)

        return assistant_reply

    except Exception as e:
        logger.error(f"Error calling OpenRouter API: {e}")
        # Save a fallback message as assistant response to maintain conversation flow
        fallback = "Sorry, I'm having trouble processing your request right now."
        db.save_user_message(user_id, "assistant", fallback)
        return fallback


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular text messages."""
    # Ignore messages in groups that don't mention the bot (optional)
    if update.effective_chat.type != "private":
        # In groups, only respond if the bot username is mentioned
        bot_username = context.bot.username
        if bot_username and f"@{bot_username}" not in update.message.text:
            return

    user_message = update.message.text
    user_id = update.effective_user.id

    # Check message length
    if len(user_message) > MAX_MESSAGE_LENGTH:
        await update.message.reply_text(
            f"Your message is too long ({len(user_message)} characters). "
            f"Please keep it under {MAX_MESSAGE_LENGTH} characters."
        )
        return

    # Send typing action
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    try:
        response = await chat_with_gpt(user_message, user_id)
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await update.message.reply_text("An unexpected error occurred. Please try again later.")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    await update.message.reply_text(
        "🤖 Hello! I'm your AI assistant bot. I remember our conversation context.\n\n"
        "Commands:\n"
        "/start - Show this message\n"
        "/help - Get help\n"
        "/clear - Clear your conversation history"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    await update.message.reply_text(
        "Send me any message and I'll respond! I keep track of the last "
        f"{MAX_HISTORY_MESSAGES} messages to maintain context.\n\n"
        "Use /clear to reset the conversation."
    )


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /clear command to erase user history."""
    user_id = update.effective_user.id
    deleted = db.clear_user_history(user_id)
    await update.message.reply_text(
        f"✅ Your conversation history has been cleared ({deleted} messages removed)."
    )


def main() -> None:
    """Start the bot."""
    if not all([OPENROUTER_API_KEY, TELEGRAM_BOT_TOKEN]):
        logger.error("Missing required environment variables: OpenRouter_API_KEY, TELEGRAM_BOT_TOKEN")
        return

    # Initialize database
    db.init_db()

    # Build application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_command))

    # Add message handler for text (excluding commands)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Start bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()