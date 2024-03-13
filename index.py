from typing import Final
from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes
import os
from dotenv import load_dotenv


load_dotenv()
token = os.getenv("TOKEN_NAME")

TOKEN:Final = token
BOT_USERNAME:Final= '@studysge_bot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""Hello! Welcome to Study Buddy Bot. 📚✨
I'm here to assist you with your studies! Whether you need help organizing your schedule, creating flashcards, practicing quizzes, or sharing resources, I've got you covered.
Feel free to explore the features available and let me know how I can help you achieve your learning goals. Just type /help to see all available commands.
Happy studying! 🎓""")
    
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start',start_command))

    app.run_polling(poll_interval=3)