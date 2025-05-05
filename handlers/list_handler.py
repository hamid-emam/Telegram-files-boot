from file_data import files_by_section
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def register_list_handler(bot):
    @bot.message_handler(commands=['list'])
    def list_files(message):
        keyboard = InlineKeyboardMarkup()

        for section, files in files_by_section.items():
            for name in files:
                keyboard.add(InlineKeyboardButton(text=name, callback_data=f"get|{name}"))

        bot.send_message(message.chat.id, "Available files (click to get):", reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("get|"))
    def callback_get_file(call):
        filename = call.data.split("|", 1)[1]
        for section in files_by_section.values():
            if filename in section:
                bot.send_message(call.message.chat.id, f"Here’s your file:\n{section[filename]}")
                return
        bot.send_message(call.message.chat.id, "File not found.")