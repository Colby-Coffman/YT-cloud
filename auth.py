import google_auth_oauthlib.flow as oauthflow
import os
import google.oauth2.credentials as oauthcred
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError

SCOPES = ["https://www.googleapis.com/auth/youtube"]
CLIENT_SECRETS_FILE = None

def _credentials_flow(credentials_file):        
    flow = oauthflow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    credentials = flow.run_local_server()
    with open(credentials_file, "w") as file:
        file.write(credentials.to_json())
    return credentials

def get_credentials(credentials_file):
    credentials = None
    if os.path.isfile(credentials_file) and not os.path.islink(credentials_file):
        credentials = oauthcred.Credentials.from_authorized_user_file(credentials_file, scopes=SCOPES)
        if not credentials.valid:
            if not credentials.token:
                return _credentials_flow(credentials_file)
            try:
                credentials.refresh(Request())
            except RefreshError:
                return _credentials_flow(credentials_file)
            with open(credentials_file, "w") as file:
                file.write(credentials.to_json())
            return credentials
        return credentials
    else:
        return _credentials_flow(credentials_file)
