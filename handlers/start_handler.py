def register_start_handler(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "Welcome to the File Bot! Send /menu to see available sections or /get filename or /list to see all files.")
