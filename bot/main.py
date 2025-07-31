import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)
from bot.database import Database
from bot.location import LocationService

class GreetyBot:
    def __init__(self):
        self.db = Database(os.getenv('DATABASE_URL'))
        self.geo = LocationService()
        self.app = ApplicationBuilder() \
            .token(os.getenv('BOT_TOKEN')) \
            .post_init(self._register_webhook) \
            .build()

    async def _register_webhook(self, app):
        await app.bot.set_webhook(
            url=f"https://{os.getenv('RENDER_EXTERNAL_URL')}/webhook",
            allowed_updates=Update.ALL_TYPES
        )

    def setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(MessageHandler(filters.LOCATION, self.handle_location))

    async def start(self, update: Update, context):
        await update.message.reply_text("Greety Bot Online! ✅")

    async def handle_location(self, update: Update, context):
        user = update.effective_user
        loc = update.message.location
        welcome = await self.geo.generate_welcome(user, loc)
        await update.message.reply_text(welcome)
        self.db.log_location(user.id, loc.latitude, loc.longitude)

    def run(self):
        self.setup_handlers()
        self.app.run_webhook(
            listen="0.0.0.0",
            port=int(os.getenv("PORT", 10000)),
            webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_URL')}/webhook",
            secret_token=os.getenv('WEBHOOK_SECRET')
        )

if __name__ == '__main__':
    GreetyBot().run()
