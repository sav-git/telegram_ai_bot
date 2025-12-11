# 🤖 AI Telegram Assistant

An intelligent Telegram bot with conversation history preservation. Uses OpenRouter API for generating context-aware responses and SQLite for storing each user's message history.

## ✨ Features

- **📝 Contextual conversations** - The bot remembers previous user messages
- **🗃️ Local storage** - All history stored in SQLite database
- **🎯 Personalization** - Each user has their own independent history
- **⚡ Fast responses** - Asynchronous message processing
- **🔧 Easy setup** - Minimal environment requirements

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A Telegram account
- API key from [OpenRouter.ai](https://openrouter.ai)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/telegram-ai-bot.git
cd telegram-ai-bot
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
   - Create a `.env` file in the project root
   - Copy the content from `.env.example`
   - Fill in your data:

```env
# Bot token from @BotFather
TELEGRAM_BOT_TOKEN=your_bot_token

# API key from OpenRouter
OpenRouter_API_KEY=your_api_key

# Database file name (default)
DATABASE_URL=chat_history.db
```

4. **Initialize the database:**
```bash
python init_db.py
```

5. **Run the bot:**
```bash
python bot.py
```

## 📁 Project Structure

```
telegram-ai-bot/
├── bot.py              # Main bot file
├── db.py               # Database module
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── .env.example        # Configuration example
├── .gitignore          # Git ignore file
└── README.md           # Documentation
```

## 🛠️ Bot Commands

- `/start` - Start the bot
- `/help` - Get help on commands
- Send any text message to chat with AI

## 🔧 Technical Details

### Database

The bot uses SQLite to store message history. The `chat_history` table structure:

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Unique identifier |
| user_id | TEXT | Telegram user ID |
| role | TEXT | Sender role (user/assistant) |
| message | TEXT | Message text |
| timestamp | DATETIME | Message timestamp |

### Conversation Context

The bot stores the last 20 messages of each user to maintain conversation context. History is automatically updated with each new message.

## ⚙️ AI Model Configuration

By default, the model `meta-llama/llama-3-8b-instruct` is used. To change the model, edit the line in `bot.py`:

```python
response = client.chat.completions.create(
    model="meta-llama/llama-3-8b-instruct",  # ← Replace with desired model
    messages=messages,
)
```

Available models can be found at [OpenRouter Models](https://openrouter.ai/models).

## 🔄 Extending Functionality

### Adding New Commands

To add a new command, edit the `bot.py` file:

```python
async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for new command"""
    await update.message.reply_text("Response text")

# Add in main() function:
application.add_handler(CommandHandler("newcommand", new_command))
```

### Changing History Limit

To change the number of stored messages, modify the `limit` parameter in the `get_user_history` function in `db.py`.

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**AI Telegram Bot | Context Preservation | Local Data Storage**

*Made with ❤️ for developers*