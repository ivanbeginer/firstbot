from telegram.ext import BaseHandler,CommandHandler
from app.hendlers.commands import start, Leha
HANDLERS: tuple[BaseHandler] = (CommandHandler('start',start),CommandHandler('Leha',Leha),)


