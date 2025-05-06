from telebot import types
from file_data import file_data  # Ensure this imports your current dict
import re

def register_add_handler(bot):
    @bot.message_handler(commands=['add'])
    def handle_add(message):
        try:
            # Split and validate message
            parts = message.text.split(' /')
            if len(parts) != 4:
                bot.reply_to(message, "Incorrect format. Use:\n/add section /filename /drive_link")
                return

            section, filename, link = parts[1], parts[2], parts[3]

            # Extract file ID from Google Drive link
            match = re.search(r'/d/([a-zA-Z0-9_-]+)', link)
            if not match:
                bot.reply_to(message, "Invalid Google Drive link.")
                return
            file_id = match.group(1)
            download_link = f"https://drive.google.com/uc?id={file_id}&export=download"

            # Add to file_data
            if section not in file_data:
                file_data[section] = {}
            file_data[section][filename] = download_link

            # Append to file_data.py (persistent)
            with open("file_data.py", "a") as f:
                if section not in open("file_data.py").read():
                    f.write(f"\nfile_data['{section}'] = {{}}\n")
                f.write(f"file_data['{section}']['{filename}'] = '{download_link}'\n")

            bot.reply_to(message, f"Added:\nSection: {section}\nFile: {filename}")
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")
