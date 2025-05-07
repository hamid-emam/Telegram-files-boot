import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load credentials from environment variable
creds_dict = json.loads(os.environ['GOOGLE_SERVICE_ACCOUNT'])
creds = service_account.Credentials.from_service_account_info(creds_dict)

# Initialize Drive API
drive_service = build('drive', 'v3', credentials=creds)

# Replace this with your main folder ID
MAIN_FOLDER_ID = '1cpPjG7_pQUi_je-bnyNXFSTUyuAr0ywB'

def get_subfolders(folder_id):
    query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def get_files_in_folder(folder_id):
    query = f"'{folder_id}' in parents and mimeType!='application/vnd.google-apps.folder' and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def build_files_by_section():
    files_by_section = {}
    subfolders = get_subfolders(MAIN_FOLDER_ID)

    for folder in subfolders:
        section_name = folder['name']
        files = get_files_in_folder(folder['id'])
        files_dict = {}

        for file in files:
            file_id = file['id']
            file_name = file['name']
            # Use export for Google Slides, fallback to direct link otherwise
            if file_name.endswith('.pptx') or file_name.endswith('.pdf'):
                url = f"https://drive.google.com/uc?export=download&id={file_id}"
            else:
                url = f"https://drive.google.com/uc?export=download&id={file_id}"
            files_dict[file_name] = url

        files_by_section[section_name] = files_dict

    return files_by_section

# Exported dictionary
files_by_section = build_files_by_section()
