import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters
)
from bot.database import Database
from bot.location import LocationService
from bot.admin import AdminPanel

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class GreetyBot:
    def __init__(self):
        self.db = Database(os.getenv('DATABASE_URL'))
        self.geo = LocationService()
        self.admin = AdminPanel(self.db)
        self.app = self._create_application()

    def _create_application(self):
        return ApplicationBuilder() \
            .token(os.getenv('BOT_TOKEN')) \
            .post_init(self._on_startup) \
            .post_shutdown(self._on_shutdown) \
            .build()

    async def _on_startup(self, app):
        """Initialize webhook on startup"""
        await app.bot.set_webhook(
            url=f"{os.getenv('WEBHOOK_URL')}/telegram",
            secret_token=os.getenv('WEBHOOK_SECRET'),
            allowed_updates=Update.ALL_TYPES
        )
        logger.info("Webhook configured successfully")

    async def _on_shutdown(self, app):
        """Cleanup on shutdown"""
        await app.bot.delete_webhook()
        logger.info("Bot shutdown complete")

    def setup_handlers(self):
        """Register all handlers"""
        # Core functionality
        self.app.add_handler(MessageHandler(filters.LOCATION, self.handle_location))
        
        # Admin commands
        self.app.add_handler(CommandHandler("settings", self.admin.settings_panel))
        
        # Health check endpoint
        self.app.add_handler(CommandHandler("health", self.health_check))

    async def handle_location(self, update: Update, context: CallbackContext):
        """Process location updates"""
        user = update.effective_user
        location = update.message.location
        
        try:
            welcome_msg = await self.geo.generate_welcome(user, location)
            await update.message.reply_text(welcome_msg)
            self.db.log_location(user.id, location.latitude, location.longitude)
        except Exception as e:
            logger.error(f"Location handling failed: {e}")
            await update.message.reply_text("Welcome! (Location processing failed)")

    async def health_check(self, update: Update, context: CallbackContext):
        """Render health check endpoint"""
        await update.message.reply_text("✅ Bot is healthy")

    def run(self, use_webhook=True, port=10000):
        """Start the bot"""
        self.setup_handlers()
        
        if use_webhook:
            self.app.run_webhook(
                listen="0.0.0.0",
                port=port,
                webhook_url=f"{os.getenv('WEBHOOK_URL')}/telegram",
                secret_token=os.getenv('WEBHOOK_SECRET')
            )
        else:
            self.app.run_polling()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--webhook', action='store_true')
    parser.add_argument('--polling', action='store_true')
    parser.add_argument('--port', default=10000, type=int)
    args = parser.parse_args()
    
    bot = GreetyBot()
    bot.run(use_webhook=args.webhook, port=args.port)
