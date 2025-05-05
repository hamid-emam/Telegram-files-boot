import os
from flask import Flask, request
import telebot
from config import BOT_TOKEN
from handlers.start_handler import register_start_handler
from handlers.list_handler import register_list_handler
from handlers.get_handler import register_get_handler
from handlers.menu_handler import register_menu_handler
from handlers.add_handler import register_add_handler

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Register handlers
register_start_handler(bot)
register_list_handler(bot)
register_get_handler(bot)
register_menu_handler(bot)
register_add_handler(bot)

# Webhook route
@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        bot.process_new_updates([update])
        return '', 200
    return "Bot is running!", 200

# Set webhook when server starts
@app.before_first_request
def set_webhook():
    webhook_url = os.getenv("WEBHOOK_URL")  # you will set this on Cyclic
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)

if __name__ == "__main__":
    app.run()
