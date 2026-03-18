# 🤖 AI Telegram Assistant

An intelligent Telegram bot with conversation history preservation. Uses OpenRouter API for generating context-aware responses and SQLite for storing each user's message history.

## ✨ Features

- **📝 Contextual conversations** – The bot remembers previous user messages
- **🗃️ Local storage** – All history stored in SQLite database
- **🎯 Personalization** – Each user has their own independent history
- **⚡ Fast responses** – Asynchronous message processing
- **🔧 Easy setup** – Minimal environment requirements
- **🛡️ Privacy controls** – Commands to clear personal data
- **🧹 Automatic cleanup** – Old records deleted automatically

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

3. **Create a Telegram bot** via [@BotFather](https://t.me/botfather) and obtain your bot token.

4. **Configure environment variables:**
   - Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
   - Edit `.env` with your data:
```env
# Telegram Bot Token (from @BotFather)
TELEGRAM_BOT_TOKEN=your_bot_token_here

# OpenRouter API Key (from https://openrouter.ai/keys)
OPENROUTER_API_KEY=your_api_key_here

# Database file (SQLite)
DATABASE_URL=chat_history.db

# Optional: Change the LLM model (see OpenRouter models)
OPENROUTER_MODEL=meta-llama/llama-3-8b-instruct

# Number of messages to keep in context
MAX_HISTORY_MESSAGES=20
```

5. **Initialize the database:**
```bash
python3 init_db.py
```

6. **Run the bot:**
```bash
python3 bot.py
```

## 📁 Project Structure

```
telegram-ai-bot/
├── bot.py              # Main bot file
├── db.py               # Database module (async SQLite)
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── .env.example        # Configuration example
├── .gitignore          # Git ignore file
└── README.md           # Documentation
```

## 🛠️ Bot Commands

- `/start` – Start the bot and see welcome message
- `/help` – Get help on available commands
- `/clear` – Clear your conversation history
- `/delete_my_data` – Permanently delete all your data from the bot
- *(any text message)* – Chat with the AI assistant

## ⚙️ Configuration

The bot is configured via environment variables (set in `.env` file):

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token (from @BotFather) | **Required** |
| `OPENROUTER_API_KEY` | Your OpenRouter API key | **Required** |
| `DATABASE_URL` | Path to SQLite database file | `chat_history.db` |
| `OPENROUTER_MODEL` | LLM model to use (see [OpenRouter models](https://openrouter.ai/models)) | `minimax/m2.5` |
| `MAX_HISTORY_MESSAGES` | Number of previous messages to remember per user | `20` |
| `MAX_MESSAGE_LENGTH` | Maximum allowed length for user messages | `4000` |

## 🔧 Technical Details

### Database

The bot uses **SQLite** with **asynchronous access** (`aiosqlite`) to avoid blocking during concurrent requests.  
The `chat_history` table structure:

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Unique identifier |
| user_id | TEXT | Telegram user ID |
| role | TEXT | Sender role (`user` / `assistant`) |
| message | TEXT | Message text |
| timestamp | DATETIME | Message timestamp |

Indexes are created on `user_id` and `timestamp` for fast queries and automatic cleanup.

### Conversation Context

For each user, the bot stores the last `MAX_HISTORY_MESSAGES` messages (default 20). History is automatically updated with every new exchange, ensuring smooth, contextual conversations.

### Automatic Cleanup

A background job runs daily at 3:00 AM to delete records older than 30 days, keeping the database size manageable and respecting user privacy.

## 🤖 AI Model Configuration

You can change the underlying LLM model by setting the `OPENROUTER_MODEL` environment variable.  
For example, to use a powerful free model during testing:

```env
OPENROUTER_MODEL=stepfun/step-3-5-flash
```

For production, popular choices include `minimax/m2.5`, `google/gemini-3-flash-preview`, or `deepseek/deepseek-v3.2`.  
Browse all available models at [OpenRouter Models](https://openrouter.ai/models).

## 🔄 Extending Functionality

### Adding New Commands

To add a new command, edit `bot.py`:

```python
async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for new command"""
    await update.message.reply_text("Response text")

# Add in main() function:
application.add_handler(CommandHandler("newcommand", new_command))
```

### Changing History Limit

Modify the `MAX_HISTORY_MESSAGES` variable in your `.env` file. The bot will automatically use the new value after restart.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**AI Telegram Bot | Context Preservation | Local Data Storage**

*Made with ❤️ for developers*
