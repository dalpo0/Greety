import os
import logging
from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ChatMemberHandler
)
from bot.database import UserDatabase
from bot.location import LocationService
from bot.admin import AdminPanel

# Initialize services
db = UserDatabase()
geo = LocationService()
admin = AdminPanel(db)

class GreetyBot:
    def __init__(self):
        self.updater = Updater(os.getenv('BOT_TOKEN'))
        self._setup_handlers()
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                          level=logging.INFO)

    def _setup_handlers(self):
        dp = self.updater.dispatcher
        
        # Core functionality
        dp.add_handler(ChatMemberHandler(self._handle_chat_member))
        dp.add_handler(MessageHandler(Filters.location, self._handle_location))
        
        # Admin commands
        dp.add_handler(CommandHandler("settings", admin.settings_panel))
        dp.add_handler(CommandHandler("stats", admin.get_stats))
        
        # User commands
        dp.add_handler(CommandHandler("start", self._send_welcome))

    async def _handle_chat_member(self, update: Update, context: CallbackContext):
        """Handle new member joins"""
        new_member = update.chat_member.new_chat_member
        if new_member.status == 'member':
            user = new_member.user
            chat_id = update.chat_member.chat.id
            
            # Save user to database
            db.log_join(user.id, user.username, user.first_name, chat_id)
            
            # Request location
            await self._request_location(user.id, chat_id)

    async def _request_location(self, user_id: int, chat_id: int):
        """Send location request keyboard"""
        keyboard = [
            [KeyboardButton("📍 Share Location", request_location=True)]
        ]
        await self.updater.bot.send_message(
            chat_id=user_id,
            text="Help us welcome you properly!",
            reply_markup=ReplyKeyboardMarkup(
                keyboard, 
                one_time_keyboard=True,
                resize_keyboard=True
            )
        )

    async def _handle_location(self, update: Update, context: CallbackContext):
        """Process received location"""
        user = update.effective_user
        location = update.message.location
        
        # Get localized welcome
        welcome_msg = await geo.generate_welcome(user, location)
        
        # Send to group
        await update.message.reply_text(
            welcome_msg,
            reply_markup=ReplyKeyboardRemove()
        )
        
        # Update user record
        db.update_location(user.id, location.latitude, location.longitude)

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    GreetyBot().run()
