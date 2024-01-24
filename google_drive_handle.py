from dotenv import load_dotenv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import OAuth2Credentials
import os

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
REDIRECT_URI = os.getenv('REDIRECT_URIS').split(',')[0]  # Access the first URI

def authenticate_google_drive():
    gauth = GoogleAuth()
    gauth.credentials = OAuth2Credentials(None, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, None,
                                         "https://accounts.google.com/o/oauth2/token", None, "web")
    drive = GoogleDrive(gauth)
    return drive

drive = authenticate_google_drive()

def upload_file_to_drive(drive, file_path, folder_id=None):
    if not os.path.exists(file_path):
        print(f"Cannot upload, file does not exist at path: {file_path}")
        return None

    try:
        file_metadata = {'title': os.path.basename(file_path)}
        if folder_id:
            file_metadata['parents'] = [{'id': folder_id}]

        upload_file = drive.CreateFile(file_metadata)

        # Check if the file already exists on Google Drive
        existing_files = drive.ListFile({'q': f"title='{upload_file['title']}'"}).GetList()
        if existing_files:
            # File with the same name already exists, update the existing file
            upload_file = existing_files[0]
            print(f"File already exists on Drive. Updating file with ID: {upload_file['id']}")
        else:
            print("Uploading a new file to Drive.")

        upload_file.SetContentFile(file_path)
        upload_file.Upload()
        print(f"File uploaded successfully. File ID: {upload_file['id']}")
        return upload_file['id']
    except Exception as e:
        print(f"An error occurred during file upload: {e}")
        return None


def get_drive_download_link(drive, file_id):
    try:
        file = drive.CreateFile({'id': file_id})
        file.Upload() # Make sure the file exists on Drive
        file.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'})
        return "https://drive.google.com/uc?export=download&id=" + file_id
    except Exception as e:
        print(f"Error fetching download link: {e}")
        return None
