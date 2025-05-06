import re
from file_data import file_data

def register_add_handler(bot):
    @bot.message_handler(commands=['add'])
    def handle_add(message):
        try:
            text = message.text
            match = re.match(r"/add (\w+) /(.+?) /(\S+)", text)
            if not match:
                bot.reply_to(message, "Incorrect format. Use:\n/add section /filename /drive_link")
                return

            section, filename, link = match.groups()

            # Extract file ID from Google Drive link
            file_id_match = re.search(r'/d/([a-zA-Z0-9_-]+)', link)
            if not file_id_match:
                bot.reply_to(message, "Invalid Google Drive link.")
                return

            file_id = file_id_match.group(1)
            download_link = f"https://drive.google.com/uc?id={file_id}&export=download"

            # Add to file_data
            if section not in file_data:
                file_data[section] = {}
            file_data[section][filename] = download_link

            # Persist to file_data.py
            with open("file_data.py", "a") as f:
                if section not in open("file_data.py").read():
                    f.write(f"\nfile_data['{section}'] = {{}}\n")
                f.write(f"file_data['{section}']['{filename}'] = '{download_link}'\n")

            bot.reply_to(message, f"Added:\nSection: {section}\nFile: {filename}")
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")
