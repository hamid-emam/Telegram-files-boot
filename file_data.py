from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to the service account JSON key
SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Authenticate and build the service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

def list_subfolders(main_folder_id):
    """
    List all subfolders inside the main folder.
    """
    query = f"'{main_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def list_files_in_folder(folder_id):
    """
    List all files in a given folder (subfolder).
    """
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def organize_files(main_folder_id):
    """
    Organize files from subfolders within a main folder into sections.
    """
    file_data = {}

    # Get all subfolders (sections) within the main folder
    subfolders = list_subfolders(main_folder_id)

    for subfolder in subfolders:
        section_name = subfolder['name']
        section_id = subfolder['id']
        
        # Get files inside this subfolder (section)
        files = list_files_in_folder(section_id)

        section_files = {}
        for file in files:
            # Construct the link to download the file
            file_link = f"https://drive.google.com/uc?export=download&id={file['id']}"
            section_files[file['name']] = file_link

        # Add the section and files to the file_data dictionary
        file_data[section_name] = section_files

    return file_data

# Test the script with your main folder ID
main_folder_id = "your_main_folder_id_here"  # Replace with your main folder ID
file_data = organize_files(main_folder_id)

# Print the file_data or use it in your bot
print(file_data)
