from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
token = os.getenv("TOKEN")

TOKEN: Final = token
BOT_USERNAME: Final = '@studysge_bot'

flashcards = {}
shared_resources = {}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""Hello! Welcome to Study Buddy Bot. 📚✨
I'm here to assist you with your studies! Whether you need help organizing your schedule, creating flashcards, practicing quizzes, or sharing resources, I've got you covered.
Feel free to explore the features available and let me know how I can help you achieve your learning goals. Just type /help to see all available commands.
Happy studying! 🎓""")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""/start - Starts the bot
/help - Lists all commands
/create_flashcard - Creates a flashcard
/view_flashcards - Shows all flashcards
/timer - Sets time
/share_resource - Upload your resources
/view_resources - Shows all resources
""")

async def create_flashcard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Flashcard has been Created")
    question, answer = context.args
    flashcards[update.message.from_user.id] = (question, answer)
    print(question,answer)


async def view_flashcards_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    flashcard_list = "\n".join(
        f"Q: {flashcards[user][0]}\nA: {flashcards[user][1]}" for user in flashcards)
    await update.message.reply_text("Here are your saved flashcards:\n" + flashcard_list)


async def share_resource_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Let's share a study resource. Please upload the file or provide a link.")
    resources = context.args
    shared_resources[update.message.from_user.id] = (resources)
    print(shared_resources)
    # Logic to handle resource sharing
    # Example: Save the shared resource to a storage and provide a link

async def view_resource_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    shared_resources_list = "\n".join(
        f"R: {shared_resources[user]}" for user in shared_resources)
    await update.message.reply_text("Here are your saved resources:\n" + shared_resources_list)


async def send_audio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the user sent an audio file
    if update.message.audio:
        audio_file_id = update.message.audio.file_id
        await update.message.reply_audio(audio=audio_file_id)
    else:
        await update.message.reply_text("Please upload an audio file to send.")


async def timer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        time_in_seconds = int(context.args[0])
        await update.message.reply_text(
            f"Timer set for {time_in_seconds} seconds.")
        await asyncio.sleep(time_in_seconds)
        await update.message.reply_text("Timer ended. Time's up!")
    except (IndexError, ValueError):
        await update.message.reply_text("Please provide a valid time in seconds.")


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('create_flashcard', create_flashcard_command))
    app.add_handler(CommandHandler('view_flashcards', view_flashcards_command))
    app.add_handler(CommandHandler('share_resource', share_resource_command))
    app.add_handler(CommandHandler('view_resources',view_resource_command))
    app.add_handler(CommandHandler('help',help_command)) 
    app.add_handler(CommandHandler('send_audio', send_audio_command))
    app.add_handler(CommandHandler('timer', timer_command))

    app.run_polling(poll_interval=3)
