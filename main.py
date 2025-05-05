import telebot
from config import BOT_TOKEN
from handlers.start_handler import register_start_handler
from handlers.list_handler import register_list_handler
from handlers.get_handler import register_get_handler
from handlers.menu_handler import register_menu_handler
from keep_alive import keep_alive

bot = telebot.TeleBot(BOT_TOKEN)

# Register all handlers
register_start_handler(bot)
register_list_handler(bot)
register_get_handler(bot)
register_menu_handler(bot)

# Start the keep-alive server (Flask)
keep_alive()

# Start polling for bot messages
bot.infinity_polling()