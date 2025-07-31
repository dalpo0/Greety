import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, 
    Filters, CallbackContext
)
from bot.location import get_localized_welcome
from bot.database import UserDB

class GreetyBot:
    def __init__(self):
        self.db = UserDB()
        self.updater = Updater(os.getenv('BOT_TOKEN'))
        self._setup_handlers()

    def _setup_handlers(self):
        dp = self.updater.dispatcher
        dp.add_handler(MessageHandler(Filters.location, self.handle_location))
        dp.add_handler(CommandHandler("welcome", self.customize_welcome))
        
        # Admin commands
        dp.add_handler(CommandHandler("settings", self.settings_panel))

    async def handle_location(self, update: Update, context: CallbackContext):
        user = update.effective_user
        location = update.message.location
        
        # Save to database
        self.db.save_location(
            user.id, 
            location.latitude, 
            location.longitude
        )
        
        # Generate personalized welcome
        welcome_msg = await get_localized_welcome(user, location)
        await update.message.reply_text(welcome_msg)

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    GreetyBot().run()
