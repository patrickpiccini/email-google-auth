import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def authenticator(client_secret_file, api_service_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_service_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    creds = None

    if os.path.exists('DocGoogle/token.json'):
        creds = Credentials.from_authorized_user_file(
            'DocGoogle/token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('DocGoogle/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
        print(API_SERVICE_NAME, 'service created successfully')
        return service

    except HttpError as error:
        # TO DO(developer) - Handle errors from gmail API.
        print('An error occurred: {}'.format(error))