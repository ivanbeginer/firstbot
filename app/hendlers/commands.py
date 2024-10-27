from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context:ContextTypes.DEFAULT_TYPE)->None:
    if update.effective_chat and update.effective_user:
        await context.application.user_service.register_visitor(update.effective_user.id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Добро пожаловать!')

async def Leha(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:
    if update.effective_chat:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Леха гей биг стар')

