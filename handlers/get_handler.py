from file_data import files_by_section

def register_get_handler(bot):
    @bot.message_handler(commands=['get'])
    def get_file(message):
        try:
            filename = message.text.split(maxsplit=1)[1].strip()
        except IndexError:
            bot.reply_to(message, "Please use the format: /get filename")
            return

        for section in files_by_section.values():
            if filename in section:
                bot.reply_to(message, f"Here’s your file:\n{section[filename]}")
                return

        bot.reply_to(message, "File not found. Use /menu to explore sections or /list to view names.")