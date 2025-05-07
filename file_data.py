import os
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'infra-upgrade-459008-m3-da0667ac04de.json'

# Scopes and folder ID
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
FOLDER_ID = '1cpPjG7_pQUi_je-bnyNXFSTUyuAr0ywB'  # Replace with your folder ID

# Authenticate
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

# Function to list subfolders in main folder
def get_subfolders(parent_id):
    results = service.files().list(
        q=f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed = false",
        fields="files(id, name)").execute()
    return results.get('files', [])

# Function to list files inside a folder
def get_files_in_folder(folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed = false",
        fields="files(id, name)").execute()
    return results.get('files', [])

# Build the dictionary
files_by_section = {}

subfolders = get_subfolders(FOLDER_ID)
for folder in subfolders:
    section_name = folder['name']
    files = get_files_in_folder(folder['id'])

    section_files = {}
    for file in files:
        file_name = os.path.splitext(file['name'])[0]
        file_id = file['id']
        download_link = f"https://drive.google.com/uc?export=download&id={file_id}"
        section_files[file_name] = download_link

    files_by_section[section_name] = section_files
