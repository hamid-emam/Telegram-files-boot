import re
import json
from file_data import files_by_section

def build_download_link(link):
    match = re.search(r'https://docs\.google\.com/(\w+)/d/([a-zA-Z0-9_-]+)', link)
    if not match:
        return None

    file_type, file_id = match.groups()

    if file_type == 'presentation':
        return f"https://docs.google.com/presentation/d/{file_id}/export/pdf"
    elif file_type == 'document':
        return f"https://docs.google.com/document/d/{file_id}/export?format=pdf"
    elif file_type == 'spreadsheets':
        return f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=pdf"
    else:
        return f"https://drive.google.com/uc?export=download&id={file_id}"

def save_to_file():
    with open("file_data.py", "w", encoding="utf-8") as f:
        f.write("files_by_section = ")
        json.dump(files_by_section, f, indent=4, ensure_ascii=False)

def register_add_handler(bot):
    @bot.message_handler(commands=["add"])
    def add_file(message):
        parts = message.text.split(" /")
        if len(parts) != 4:
            bot.reply_to(message, "Use the format:\n`/add section /filename /url`", parse_mode="Markdown")
            return

        _, section = parts[0].split(maxsplit=1)
        filename = parts[1].strip()
        url = parts[2].strip()

        download_url = build_download_link(url)
        if not download_url:
            bot.reply_to(message, "Invalid or unsupported Google Drive link.")
            return

        if section not in files_by_section:
            files_by_section[section] = {}

        files_by_section[section][filename] = download_url
        save_to_file()

        bot.reply_to(message, f"File '{filename}' added successfully under section '{section}'.")
