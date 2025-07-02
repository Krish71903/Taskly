from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from ..core.config import settings

def get_google_auth_flow():
    """Initializes and returns a Google OAuth2 flow."""
    client_config = {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
        }
    }
    flow = Flow.from_client_config(
        client_config,
        scopes=settings.GMAIL_SCOPES + settings.CALENDAR_SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )
    return flow

def get_auth_url():
    """Generates the Google OAuth2 authorization URL."""
    flow = get_google_auth_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    return authorization_url, state

def get_tokens_from_code(code: str, state: str):
    """Exchanges an authorization code for credentials."""
    flow = get_google_auth_flow()
    flow.fetch_token(code=code)
    credentials = flow.credentials
    # Here you would save the credentials securely
    # from ..core.security import store_tokens
    # store_tokens(user_id, credentials_to_dict(credentials))
    return credentials_to_dict(credentials)

def credentials_to_dict(credentials: Credentials) -> dict:
    """Converts Google Credentials object to a dictionary."""
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    } 